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
