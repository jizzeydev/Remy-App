"""
Splits Universitarios — endpoints públicos y admin.

Modelo (sin duplicar lo que ya existe):
  - Universidades: colección `library_universities` (id, name, short_name, tier).
  - Ramos universitarios: colección `courses` con `university_id` no nulo.
      Campos de split que vienen de docs/splits-remy.md:
        code, semester, prereq_course_ids, base_course_ids,
        match_level, source, coverage_status, notes, alt_slugs.
  - Ejes textuales del syllabus: colección `course_axes`
      ({id, course_id, order, text, created_at}).
  - Reutilización de contenido: chapters linkeados via `template_chapter_id`
      (ya existente — ver server.py / link-chapters).

Estos endpoints NO crean ramos. Para seed/upsert usar
scripts/seed_splits_universitarios.py. El admin UI sólo lee.
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, List, Dict, Any
import os
from jose import JWTError, jwt

router = APIRouter()
security = HTTPBearer()
db = None

SECRET_KEY = os.environ.get('ADMIN_SECRET_KEY')
ALGORITHM = "HS256"


def set_db(database):
    global db
    db = database


async def verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        token_type = payload.get("type", "admin")
        if token_type == "google_admin":
            email = payload.get("email")
            if email == "seremonta.cl@gmail.com":
                return email
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


# ==================== PÚBLICOS ====================

@router.get("/universities")
async def list_universities():
    """Universidades activas con conteo de ramos seedeados."""
    unis = await db.library_universities.find(
        {"is_active": True}, {"_id": 0}
    ).sort([("tier", 1), ("name", 1)]).to_list(100)

    out = []
    for u in unis:
        courses_count = await db.courses.count_documents({"university_id": u["id"]})
        out.append({**u, "courses_count": courses_count})
    return out


@router.get("/universities/{university_id}/courses")
async def list_university_courses(
    university_id: str,
    semester: Optional[int] = Query(None),
):
    """Ramos de una universidad, opcionalmente filtrados por semestre.

    Devuelve sólo cursos visibles a estudiantes salvo que el caller use el
    endpoint admin (ver `/admin/universities/{id}/courses-all`)."""
    query: Dict[str, Any] = {
        "university_id": university_id,
        "visible_to_students": {"$ne": False},
    }
    if semester is not None:
        query["semester"] = semester
    courses = await db.courses.find(query, {"_id": 0}).sort([("semester", 1), ("title", 1)]).to_list(500)
    return courses


@router.get("/university-courses/{course_id}/syllabus")
async def get_course_syllabus(course_id: str):
    """Syllabus del ramo: ejes oficiales + estado de cobertura.

    Estado por eje:
      - "covered" cuando `match_level == "alto"`.
      - "pending" cuando `match_level == "medio"`.
    Si más adelante se quiere granularidad por eje (algunos covered, otros
    pending dentro del mismo ramo medio), el modelo `course_axes` soporta
    agregar un campo `status` sin cambios de schema.
    """
    course = await db.courses.find_one({"id": course_id}, {"_id": 0})
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    axes = await db.course_axes.find({"course_id": course_id}, {"_id": 0}).sort("order", 1).to_list(200)
    match_level = course.get("match_level")
    default_status = "covered" if match_level == "alto" else "pending" if match_level == "medio" else "covered"
    for ax in axes:
        ax.setdefault("status", default_status)

    # Chapters de este curso (linkeados o propios). Adjuntamos info del base
    # para que el frontend pueda mostrar "viene de Álgebra Lineal (general)".
    chapters = await db.chapters.find(
        {"course_id": course_id},
        {"_id": 0, "id": 1, "title": 1, "order": 1, "template_chapter_id": 1}
    ).sort("order", 1).to_list(200)

    template_ids = [c["template_chapter_id"] for c in chapters if c.get("template_chapter_id")]
    template_chapters = {}
    if template_ids:
        for tc in await db.chapters.find(
            {"id": {"$in": template_ids}},
            {"_id": 0, "id": 1, "course_id": 1, "title": 1}
        ).to_list(500):
            template_chapters[tc["id"]] = tc

    base_ids = course.get("base_course_ids", []) or []
    base_courses = {}
    for bc in await db.courses.find(
        {"id": {"$in": base_ids}}, {"_id": 0, "id": 1, "title": 1}
    ).to_list(50):
        base_courses[bc["id"]] = bc

    return {
        "course": course,
        "axes": axes,
        "chapters": chapters,
        "template_chapters": template_chapters,
        "base_courses": base_courses,
    }


@router.get("/landing/courses-index")
async def landing_courses_index():
    """Endpoint público optimizado para la landing page.

    Devuelve:
      - universidades activas con logo (para grid de logos en hero/social-proof).
      - lista plana de cursos universitarios + generales con info mínima
        (id, title, code, semester, university_short_name, base_titles)
        para alimentar el buscador "¿Está tu ramo en Remy?".

    Sin paginación: el volumen actual (~200 cursos) cabe en un solo response.
    Cacheable a nivel HTTP en futuro si crece.
    """
    unis = await db.library_universities.find(
        {"is_active": True},
        {"_id": 0, "id": 1, "short_name": 1, "name": 1, "tier": 1, "logo_url": 1},
    ).sort([("tier", 1), ("short_name", 1)]).to_list(100)
    uni_by_id = {u["id"]: u for u in unis}

    base_titles: dict[str, str] = {}
    async for b in db.courses.find(
        {"$or": [{"university_id": None}, {"university_id": {"$exists": False}}]},
        {"_id": 0, "id": 1, "title": 1},
    ):
        base_titles[b["id"]] = b["title"]

    courses = await db.courses.find(
        {"visible_to_students": {"$ne": False}},
        {
            "_id": 0, "id": 1, "title": 1, "code": 1, "semester": 1,
            "university_id": 1, "base_course_ids": 1,
        },
    ).to_list(1000)

    rows = []
    for c in courses:
        uni = uni_by_id.get(c.get("university_id")) if c.get("university_id") else None
        rows.append({
            "id": c["id"],
            "title": c.get("title") or "",
            "code": c.get("code"),
            "semester": c.get("semester"),
            "university_short_name": uni["short_name"] if uni else None,
            "university_logo_url": uni.get("logo_url") if uni else None,
            "university_tier": uni.get("tier") if uni else None,
            "base_course_ids": c.get("base_course_ids") or [],
            "base_course_titles": [base_titles.get(b, b) for b in (c.get("base_course_ids") or [])],
        })

    uni_summary = []
    for u in unis:
        n = sum(1 for r in rows if r["university_short_name"] == u["short_name"])
        if n == 0:
            continue
        uni_summary.append({
            "short_name": u["short_name"],
            "name": u["name"],
            "tier": u.get("tier"),
            "logo_url": u.get("logo_url"),
            "courses_count": n,
        })

    return {
        "universities": uni_summary,
        "courses": rows,
        "totals": {
            "courses": len(rows),
            "universities": len(uni_summary),
            "with_university": sum(1 for r in rows if r["university_short_name"]),
            "general": sum(1 for r in rows if not r["university_short_name"]),
        },
    }


# ==================== ADMIN ====================

@router.get("/admin/splits-coverage")
async def splits_coverage(_: str = Depends(verify_admin_token)):
    """Reporte de cobertura por universidad.

    Útil para ver, por U: cuántos ramos, cuántos completos vs parciales,
    cuántos ejes pendientes. La página admin (cuando exista) consume esto.
    """
    unis = await db.library_universities.find({}, {"_id": 0}).sort([("tier", 1), ("name", 1)]).to_list(100)
    rows = []
    totals = {"universities": 0, "courses": 0, "complete": 0, "partial": 0, "pending_axes": 0, "axes_total": 0}
    for u in unis:
        courses = await db.courses.find({"university_id": u["id"]}, {"_id": 0}).to_list(500)
        if not courses:
            continue
        complete = sum(1 for c in courses if (c.get("coverage_status") or "complete") == "complete")
        partial = sum(1 for c in courses if c.get("coverage_status") == "partial")
        course_ids = [c["id"] for c in courses]
        axes_total = await db.course_axes.count_documents({"course_id": {"$in": course_ids}})
        # Ejes pendientes = ejes de cursos con match_level=medio (heurística por curso)
        partial_course_ids = [c["id"] for c in courses if c.get("coverage_status") == "partial"]
        pending_axes = await db.course_axes.count_documents({"course_id": {"$in": partial_course_ids}}) if partial_course_ids else 0
        rows.append({
            "university_id": u["id"],
            "short_name": u["short_name"],
            "name": u["name"],
            "tier": u.get("tier"),
            "courses_total": len(courses),
            "courses_complete": complete,
            "courses_partial": partial,
            "axes_total": axes_total,
            "axes_pending": pending_axes,
        })
        totals["universities"] += 1
        totals["courses"] += len(courses)
        totals["complete"] += complete
        totals["partial"] += partial
        totals["axes_total"] += axes_total
        totals["pending_axes"] += pending_axes

    return {"rows": rows, "totals": totals}


@router.get("/admin/splits-courses")
async def splits_courses(_: str = Depends(verify_admin_token)):
    """Tabla plana de cursos universitarios con sus campos clave para el
    dashboard `/admin/splits`. Incluye listas auxiliares para los filtros
    (universidades, cursos base) en un solo round-trip."""
    # Cursos universitarios
    courses = await db.courses.find(
        {"university_id": {"$ne": None}},
        {
            "_id": 0,
            "id": 1, "title": 1, "code": 1, "semester": 1, "university_id": 1,
            "match_level": 1, "coverage_status": 1, "base_course_ids": 1,
            "alt_slugs": 1, "notes": 1, "product_slug": 1,
            "published_at_seremonta_store": 1, "visible_to_students": 1,
        },
    ).to_list(1000)

    # Map de universidades (id → short_name, tier)
    unis = await db.library_universities.find(
        {}, {"_id": 0, "id": 1, "short_name": 1, "name": 1, "tier": 1, "logo_url": 1}
    ).sort([("tier", 1), ("short_name", 1)]).to_list(100)
    uni_by_id = {u["id"]: u for u in unis}

    # Map de cursos base (id → title) para mostrar legible
    bases = await db.courses.find(
        {"$or": [{"university_id": None}, {"university_id": {"$exists": False}}]},
        {"_id": 0, "id": 1, "title": 1},
    ).to_list(50)
    base_by_id = {b["id"]: b["title"] for b in bases}

    # Conteos por curso (axes, chapters)
    course_ids = [c["id"] for c in courses]
    axes_count: dict[str, int] = {}
    pipeline = [
        {"$match": {"course_id": {"$in": course_ids}}},
        {"$group": {"_id": "$course_id", "n": {"$sum": 1}}},
    ]
    async for row in db.course_axes.aggregate(pipeline):
        axes_count[row["_id"]] = row["n"]

    chapters_count: dict[str, int] = {}
    pipeline = [
        {"$match": {"course_id": {"$in": course_ids}}},
        {"$group": {"_id": "$course_id", "n": {"$sum": 1}}},
    ]
    async for row in db.chapters.aggregate(pipeline):
        chapters_count[row["_id"]] = row["n"]

    # Construir filas planas
    rows = []
    for c in courses:
        u = uni_by_id.get(c.get("university_id"), {})
        bases_for_course = c.get("base_course_ids", []) or []
        rows.append({
            "id": c["id"],
            "title": c.get("title"),
            "code": c.get("code"),
            "semester": c.get("semester"),
            "university_short_name": u.get("short_name"),
            "university_name": u.get("name"),
            "university_tier": u.get("tier"),
            "match_level": c.get("match_level"),
            "coverage_status": c.get("coverage_status") or "complete",
            "base_course_ids": bases_for_course,
            "base_course_titles": [base_by_id.get(b, b) for b in bases_for_course],
            "axes_count": axes_count.get(c["id"], 0),
            "chapters_count": chapters_count.get(c["id"], 0),
            "alt_slugs_count": len(c.get("alt_slugs") or []),
            "product_slug": c.get("product_slug"),
            "published_at_seremonta_store": c.get("published_at_seremonta_store") or False,
            "visible_to_students": c.get("visible_to_students", True),
            "notes": c.get("notes"),
        })
    # Orden por U, semestre, código, título
    rows.sort(key=lambda r: (
        r["university_tier"] or 99,
        r["university_short_name"] or "",
        r["semester"] or 99,
        r["code"] or "",
        r["title"] or "",
    ))

    # Listas auxiliares para los filtros del frontend
    universities = [{
        "short_name": u["short_name"],
        "name": u["name"],
        "tier": u.get("tier"),
        "logo_url": u.get("logo_url"),
        "courses_count": sum(1 for r in rows if r["university_short_name"] == u["short_name"]),
    } for u in unis]
    universities = [u for u in universities if u["courses_count"] > 0]

    base_courses = [{
        "id": bid,
        "title": base_by_id[bid],
        "courses_count": sum(1 for r in rows if bid in r["base_course_ids"]),
    } for bid in base_by_id]
    base_courses = [b for b in base_courses if b["courses_count"] > 0]
    base_courses.sort(key=lambda b: b["title"])

    return {
        "courses": rows,
        "universities": universities,
        "base_courses": base_courses,
        "totals": {
            "courses": len(rows),
            "complete": sum(1 for r in rows if r["coverage_status"] == "complete"),
            "partial": sum(1 for r in rows if r["coverage_status"] == "partial"),
            "alto": sum(1 for r in rows if r["match_level"] == "alto"),
            "medio": sum(1 for r in rows if r["match_level"] == "medio"),
        },
    }
