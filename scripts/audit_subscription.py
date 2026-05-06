"""Auditoría y reconciliación de suscripciones MP vs estado local.

Toma un email, consulta el preapproval en Mercado Pago, lista los pagos
asociados (vía external_reference) y compara con el estado en `users` y
`subscriptions` de Atlas. Si MP no tiene ningún pago aprobado (todos
rejected/cancelled) pero la sub local está `active`, ofrece reconciliar
(setear user.subscription_status = inactive y subscription.status = el
último estado real del payment).

Uso:
    # Dry-run, solo reporta el estado
    python scripts/audit_subscription.py rodgracha@gmail.com

    # Aplicar fix si MP no tiene pagos aprobados pero local está active
    python scripts/audit_subscription.py rodgracha@gmail.com --fix
"""
import io
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import asyncio
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import mercadopago


def fmt(d, max_len=80):
    s = repr(d)
    return s if len(s) <= max_len else s[: max_len - 3] + "..."


async def main():
    load_dotenv(Path(__file__).parent.parent / "backend" / ".env")
    args = sys.argv[1:]
    fix = "--fix" in args
    args = [a for a in args if a != "--fix"]
    if not args:
        print("uso: python scripts/audit_subscription.py <email> [--fix]")
        sys.exit(1)
    email = args[0]

    atlas_uri = os.environ.get("ATLAS_URL") or os.environ["MONGO_URL"]
    db_name = os.environ["DB_NAME"]
    db = AsyncIOMotorClient(atlas_uri)[db_name]

    sdk = mercadopago.SDK(os.environ["MERCADOPAGO_ACCESS_TOKEN"])

    print(f"=== Auditoría suscripción {email} ===")
    print(f"DB    : {atlas_uri.split('@')[-1] if '@' in atlas_uri else atlas_uri}")
    print(f"Mode  : {'FIX (--fix)' if fix else 'DRY-RUN'}")
    print()

    user = await db.users.find_one({"email": email}, {"_id": 0})
    if not user:
        print(f"ERROR: user con email {email} no existe en {db_name}.users")
        sys.exit(1)
    print("[users]")
    for k in (
        "user_id",
        "name",
        "subscription_status",
        "subscription_type",
        "subscription_plan",
        "subscription_id",
        "subscription_end",
    ):
        print(f"  {k:<22s} = {fmt(user.get(k))}")
    print()

    subs = await db.subscriptions.find({"user_email": email}, {"_id": 0}).to_list(50)
    if not subs:
        print(f"[subscriptions]: ninguna doc en {db_name}.subscriptions")
        sys.exit(0)
    sub = sorted(subs, key=lambda s: s.get("created_at", ""), reverse=True)[0]
    print(f"[subscriptions] (última de {len(subs)})")
    for k in (
        "id",
        "plan",
        "status",
        "mercadopago_id",
        "amount",
        "start_date",
        "end_date",
        "created_at",
    ):
        print(f"  {k:<22s} = {fmt(sub.get(k))}")
    print()

    pre_id = sub.get("mercadopago_id")
    if not pre_id:
        print("ERROR: subscription sin mercadopago_id, no puedo reconciliar")
        sys.exit(1)

    print(f"[MP preapproval {pre_id}]")
    pre_res = sdk.preapproval().get(pre_id)
    if pre_res["status"] not in (200, 201):
        print(f"  ERROR de MP: {pre_res}")
        sys.exit(1)
    pre = pre_res["response"]
    for k in ("status", "reason", "external_reference", "next_payment_date", "last_modified"):
        print(f"  {k:<22s} = {fmt(pre.get(k))}")
    print()

    ext_ref = pre.get("external_reference") or ""
    print(f"[MP payments con external_reference={ext_ref}]")
    if not ext_ref:
        print("  (sin external_reference — saltando)")
        payments = []
    else:
        pay_res = sdk.payment().search({"external_reference": ext_ref, "limit": 50})
        if pay_res["status"] != 200:
            print(f"  ERROR de MP: {pay_res}")
            payments = []
        else:
            payments = pay_res["response"].get("results", [])
    print(f"  total: {len(payments)}")
    for p in payments:
        print(
            f"  - id={p.get('id')} status={p.get('status')!r} detail={p.get('status_detail')!r} "
            f"amount={p.get('transaction_amount')} created={p.get('date_created')} approved={p.get('date_approved')}"
        )
    print()

    approved = [p for p in payments if p.get("status") == "approved"]
    rejected = [p for p in payments if p.get("status") in ("rejected", "cancelled", "refunded", "charged_back")]
    last_real = None
    if payments:
        last_real = sorted(payments, key=lambda p: p.get("date_last_updated") or "", reverse=True)[0]

    print("=== Diagnóstico ===")
    if approved:
        print(f"  ✓ {len(approved)} pago(s) aprobado(s). Subscripción activa es válida.")
        diagnosis = "ok"
    elif rejected and not approved:
        print(f"  ✗ {len(rejected)} pago(s) inválido(s) y CERO aprobados.")
        print(f"  ✗ La sub local está '{user.get('subscription_status')}' pero MP nunca cobró.")
        diagnosis = "needs_fix"
    else:
        print("  · Sin pagos. Probablemente nunca se intentó cobrar.")
        diagnosis = "needs_review"

    if diagnosis == "needs_fix" and fix:
        target_status = last_real.get("status") if last_real else "rejected"
        print()
        print(f"=== Aplicando fix (--fix) ===")
        print(f"  user.subscription_status: '{user.get('subscription_status')}' → 'inactive'")
        print(f"  subscriptions.status    : '{sub.get('status')}' → '{target_status}'")

        await db.users.update_one(
            {"user_id": user["user_id"]},
            {"$set": {"subscription_status": "inactive"}},
        )
        await db.subscriptions.update_one(
            {"id": sub["id"]},
            {
                "$set": {
                    "status": target_status,
                    "last_payment_id": str(last_real.get("id")) if last_real else None,
                    "last_payment_status": last_real.get("status") if last_real else None,
                    "last_payment_status_detail": last_real.get("status_detail") if last_real else None,
                    "last_payment_at": datetime.now(timezone.utc).isoformat(),
                    "reconciled_by_audit_script": True,
                }
            },
        )
        print("  ✓ Aplicado.")
    elif diagnosis == "needs_fix":
        print()
        print("Re-ejecutá con --fix para reconciliar. Trial gratuito (si lo tiene) NO se toca.")


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    asyncio.run(main())
