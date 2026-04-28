# Carpeta de Contexto — Remy App

Documentos de referencia para entender el proyecto sin tener que leer todo el código. Pensados para que cualquier agente o colaborador nuevo (incluido Claude en futuras conversaciones) entre en contexto rápido.

## Índice

| Archivo | Contenido |
|---|---|
| [00-vision.md](00-vision.md) | Qué es Remy, propuesta de valor, encaje en el ecosistema Se Remonta, modelo de negocio |
| [01-usuarios.md](01-usuarios.md) | Personas: estudiante, admin, lead sin suscripción |
| [02-funcionalidades.md](02-funcionalidades.md) | Features completas (estudiante + admin) |
| [03-stack-tecnico.md](03-stack-tecnico.md) | Stack frontend, backend, integraciones, despliegue, branding |
| [04-modelo-datos.md](04-modelo-datos.md) | Jerarquía de contenido, entidades, endpoints clave |
| [05-estado-actual.md](05-estado-actual.md) | Qué está en producción, backlog, decisiones registradas |

## Cómo usar esta carpeta

- **Punto de partida**: leer `00-vision.md`. Da el panorama en 2 minutos.
- **Para tareas de producto/UX**: `01-usuarios.md` + `02-funcionalidades.md`.
- **Para tareas técnicas**: `03-stack-tecnico.md` + `04-modelo-datos.md`.
- **Para planificar trabajo nuevo**: `05-estado-actual.md` antes de proponer features (no duplicar lo ya hecho).

## Otras fuentes complementarias en el repo

- `README.md` — instrucciones de instalación y endpoints en formato técnico.
- `memory/PRD.md` — PRD vivo con decisiones por fecha.
- `memory/CHANGELOG.md` — historial de cambios.
- `design_guidelines.json` — branding y design tokens canónicos.
- `docs/` — credenciales locales y prompt de generación de preguntas.

## Cuándo actualizar estos documentos

Cuando cambie algo **estructural** (no cada commit):
- Nueva feature mayor → actualizar `02-funcionalidades.md` y `05-estado-actual.md`.
- Cambio de stack o integración → `03-stack-tecnico.md`.
- Nueva entidad o cambio en jerarquía → `04-modelo-datos.md`.
- Cambio de modelo de negocio o pricing → `00-vision.md`.

El día a día va en `memory/CHANGELOG.md`, no aquí.
