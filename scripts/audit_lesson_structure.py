"""Auditoría de estructura de lecciones por curso (sin tocar MongoDB).

Importa cada `seed_capitulo_*.py` de un curso, llama a sus builders
y reporta bloques por tipo + cumplimiento de la estructura objetivo:

  contenido (texto/definicion/teorema/intuicion)
  -> ejemplos (ejemplo_resuelto)
  -> verificaciones (verificacion)
  -> ejercicios de desarrollo (ejercicio con pistas+solucion)
  -> figuras (figura) y/o graficos (grafico_desmos)

Uso:
  python scripts/audit_lesson_structure.py algebra-lineal
"""
import importlib.util
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


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = mod
    spec.loader.exec_module(mod)
    return mod


def collect_lessons(mod):
    """Devuelve lista de (lesson_dict) para builders detectados en el módulo.

    Convenio de los seeds: builders se llaman `lesson_<x>_<y>()` o similar y
    están listados en `builders` dentro de `main()`. Para no ejecutar main(),
    detectamos funciones top-level cuyo nombre empieza con `lesson_`.
    """
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
            out.append({"_error": f"{name}: {e}"})
            continue
        if isinstance(data, dict) and "blocks" in data:
            out.append(data)
    out.sort(key=lambda d: (d.get("order", 999), d.get("id", "")))
    return out


def analyze(lesson):
    blocks = lesson.get("blocks", [])
    counts = {}
    for blk in blocks:
        t = blk.get("type", "?")
        counts[t] = counts.get(t, 0) + 1

    missing = []
    for bucket, types in REQUIRED_BUCKETS.items():
        if not any(counts.get(t, 0) > 0 for t in types):
            missing.append(bucket)

    quality_issues = []
    for blk in blocks:
        if blk.get("type") == "ejercicio":
            pistas = blk.get("pistas_md") or []
            sol = blk.get("solucion_md") or ""
            if not pistas or all(not p.strip() for p in pistas):
                quality_issues.append(f"ejercicio '{blk.get('titulo','?')}' sin pistas")
            if not sol.strip():
                quality_issues.append(f"ejercicio '{blk.get('titulo','?')}' sin solución")
        if blk.get("type") == "figura":
            prompt = (blk.get("prompt_image_md") or "").strip()
            if not prompt:
                quality_issues.append("figura sin prompt_image_md")
        if blk.get("type") == "verificacion":
            preguntas = blk.get("preguntas") or []
            for i, p in enumerate(preguntas, 1):
                if not (p.get("explicacion_md") or "").strip():
                    quality_issues.append(f"verificación pregunta {i} sin explicación")
    return counts, missing, quality_issues


def main():
    if len(sys.argv) < 2:
        print(f"uso: python {sys.argv[0]} <curso-slug>")
        sys.exit(1)
    course_slug = sys.argv[1]
    course_dir = SEEDS / course_slug
    if not course_dir.exists():
        print(f"ERROR: no existe {course_dir}")
        sys.exit(1)

    seed_files = sorted(course_dir.glob("seed_capitulo_*.py"))
    print(f"== Auditoría: {course_slug} ({len(seed_files)} capítulos) ==\n")

    grand_total = {"lessons": 0, "ok": 0, "missing": 0, "quality": 0}

    for seed in seed_files:
        try:
            mod = load_module(seed)
        except Exception as e:
            print(f"!! No se pudo cargar {seed.name}: {e}\n")
            continue

        lessons = collect_lessons(mod)
        chap_title = getattr(mod, "CHAPTER_TITLE", "?")
        chap_id = getattr(mod, "CHAPTER_ID", "?")
        print(f"--- {seed.name} :: {chap_title} ({chap_id}) — {len(lessons)} lecciones")
        for lesson in lessons:
            grand_total["lessons"] += 1
            if "_error" in lesson:
                print(f"   [ERROR] {lesson['_error']}")
                continue
            counts, missing, issues = analyze(lesson)
            tag = "OK" if not missing and not issues else ("FALTA" if missing else "WARN")
            if not missing and not issues:
                grand_total["ok"] += 1
            if missing:
                grand_total["missing"] += 1
            if issues:
                grand_total["quality"] += 1
            print(f"   [{tag:5s}] {lesson['id']}  | {lesson['title']}")
            print(f"            bloques: {dict(sorted(counts.items()))}")
            if missing:
                print(f"            FALTA: {', '.join(missing)}")
            for iss in issues:
                print(f"            warn: {iss}")
        print()

    print("== Resumen ==")
    print(f"  lecciones totales : {grand_total['lessons']}")
    print(f"  lecciones OK      : {grand_total['ok']}")
    print(f"  con buckets faltantes : {grand_total['missing']}")
    print(f"  con warnings de calidad : {grand_total['quality']}")


if __name__ == "__main__":
    main()
