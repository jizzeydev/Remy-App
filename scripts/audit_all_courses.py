"""Audit todos los cursos generales y emite un JSON por curso/lección.

Uso:
  python scripts/audit_all_courses.py > audit_report.json
"""
import importlib.util
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SEEDS = REPO / "backend" / "seeds"

REQUIRED_BUCKETS = {
    "contenido": {"texto", "definicion", "teorema", "intuicion"},
    "ejemplos": {"ejemplo_resuelto"},
    "verificaciones": {"verificacion"},
    "ejercicios": {"ejercicio"},
    "figuras_o_graficos": {"figura", "grafico_desmos"},
}

COURSES = [
    "algebra-lineal",
    "calculo-diferencial",
    "calculo-integral",
    "calculo-multivariable",
    "calculo-vectorial",
    "ecuaciones-diferenciales",
    "intro-al-algebra",
    "intro-calculo",
    "precalculo",
]


def load_module(path: Path):
    name = f"{path.parent.name}__{path.stem}"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def collect_lessons(mod):
    out = []
    for name in dir(mod):
        if not name.startswith("lesson_"):
            continue
        fn = getattr(mod, name)
        if not callable(fn):
            continue
        try:
            data = fn()
        except Exception as e:
            out.append({"_fn": name, "_error": str(e)})
            continue
        if isinstance(data, dict) and "blocks" in data:
            data["_fn"] = name
            out.append(data)
    out.sort(key=lambda d: (d.get("order", 999), d.get("id", "")))
    return out


def analyze_lesson(lesson):
    blocks = lesson.get("blocks", [])
    counts = {}
    for blk in blocks:
        t = blk.get("type", "?")
        counts[t] = counts.get(t, 0) + 1
    missing = []
    for bucket, types in REQUIRED_BUCKETS.items():
        if not any(counts.get(t, 0) > 0 for t in types):
            missing.append(bucket)
    issues = []
    for blk in blocks:
        if blk.get("type") == "ejercicio":
            pistas = blk.get("pistas_md") or []
            sol = blk.get("solucion_md") or ""
            if not pistas or all(not (p or "").strip() for p in pistas):
                issues.append(f"ejercicio_sin_pistas:{blk.get('titulo','?')[:40]}")
            if not (sol or "").strip():
                issues.append(f"ejercicio_sin_solucion:{blk.get('titulo','?')[:40]}")
        if blk.get("type") == "figura":
            prompt = (blk.get("prompt_image_md") or "").strip()
            if not prompt:
                issues.append("figura_sin_prompt")
        if blk.get("type") == "verificacion":
            preguntas = blk.get("preguntas") or []
            for i, p in enumerate(preguntas, 1):
                if not (p.get("explicacion_md") or "").strip():
                    issues.append(f"verif_q{i}_sin_explicacion")
    return {"counts": counts, "missing_buckets": missing, "quality_issues": issues}


def main():
    report = {}
    for course in COURSES:
        course_dir = SEEDS / course
        if not course_dir.exists():
            continue
        seeds = sorted(course_dir.glob("seed_capitulo_*.py"))
        course_report = {"chapters": [], "totals": {"lessons": 0, "ok": 0, "missing": 0, "warn": 0}}
        for seed in seeds:
            try:
                mod = load_module(seed)
            except Exception as e:
                course_report["chapters"].append({
                    "file": seed.name, "error": str(e), "lessons": []
                })
                continue
            chap = {
                "file": seed.name,
                "chapter_id": getattr(mod, "CHAPTER_ID", None),
                "chapter_title": getattr(mod, "CHAPTER_TITLE", None),
                "lessons": [],
            }
            for lesson in collect_lessons(mod):
                if "_error" in lesson:
                    chap["lessons"].append({"fn": lesson["_fn"], "error": lesson["_error"]})
                    continue
                a = analyze_lesson(lesson)
                course_report["totals"]["lessons"] += 1
                if not a["missing_buckets"] and not a["quality_issues"]:
                    course_report["totals"]["ok"] += 1
                if a["missing_buckets"]:
                    course_report["totals"]["missing"] += 1
                if a["quality_issues"]:
                    course_report["totals"]["warn"] += 1
                chap["lessons"].append({
                    "fn": lesson.get("_fn"),
                    "id": lesson.get("id"),
                    "title": lesson.get("title"),
                    **a,
                })
            course_report["chapters"].append(chap)
        report[course] = course_report
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    main()
