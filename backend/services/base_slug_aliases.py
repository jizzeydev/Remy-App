"""Mapeo de slugs canónicos de splits-remy.md / .jsx ↔ slugs reales de los
cursos base en Remy.

Por qué existe: las investigaciones de Cowork (`docs/splits-data/*.jsx`)
usan los slugs del catálogo Se Remonta (`precalculo-cero`, `calculo-1var-gen`,
etc.). Remy tiene los mismos cursos con slugs sin sufijo (`precalculo`,
`calculo-diferencial`, etc.) y CONTENIDO REAL ya curado bajo esos slugs. Cuando
parseamos un .jsx y leemos `match: ["calculo-1var-gen"]`, hay que resolverlo a
los slugs Remy correspondientes — para `calculo-1var-gen` son DOS cursos en
Remy porque allá vive partido.

Decisión 2026-05-14 (Jesús): aliases en código (no en DB) porque es metadata
estática de la integración. Si en el futuro un alias cambia o aparece uno
nuevo, se edita este archivo + nuevo commit. No requiere endpoint.

Sobre `nivelacion-ing`: el doc lo lista como curso base separado pero Remy NO
lo tiene grabado todavía. Por ahora se mapea a `precalculo` (la mejor segunda
opción). Cuando se grabe el curso de nivelación dedicado, se cambia este
mapping a `["nivelacion-ing"]`.
"""

# spec_slug → list[remy_real_slug]
# El primero es el base "principal" para `base_course_id` singular; todos
# juntos van a `base_course_ids` plural. La unión se hace en orden, deduplica.
BASE_SLUG_ALIASES: dict[str, list[str]] = {
    "precalculo-cero":     ["precalculo"],
    "nivelacion-ing":      ["precalculo"],
    "calculo-dif-gen":     ["calculo-diferencial"],
    "calculo-int-gen":     ["calculo-integral"],
    "calculo-1var-gen":    ["calculo-diferencial", "calculo-integral"],
    "algebra-lineal-gen":  ["algebra-lineal"],
    "calculo-vvar-gen":    ["calculo-multivariable"],
    "calculo-vec-gen":     ["calculo-vectorial"],
    "ec-dif-gen":          ["ecuaciones-diferenciales"],
}


def resolve_base_slugs(spec_slugs: list[str]) -> list[str]:
    """Resuelve los slugs del .jsx a los slugs reales de Remy, en orden y
    sin duplicados.

    Si un slug del .jsx no está en el map, se pasa tal cual — útil para tolerar
    casos en que el .jsx ya use el slug Remy. Si el resultado contiene slugs
    desconocidos, el caller (seed) debe loggear warning."""
    out: list[str] = []
    seen: set[str] = set()
    for spec in spec_slugs:
        targets = BASE_SLUG_ALIASES.get(spec, [spec])
        for t in targets:
            if t not in seen:
                seen.add(t)
                out.append(t)
    return out
