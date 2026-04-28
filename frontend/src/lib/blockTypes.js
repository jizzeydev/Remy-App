/**
 * Lesson block schema for Remy.
 *
 * A lesson is `lesson.blocks: Block[]`. Each Block has:
 *   - id: string (uuid)
 *   - type: one of the keys in BLOCK_TYPES
 *   - ...type-specific fields (see schema below)
 *
 * The admin editor constructs blocks via typed forms, so the renderer trusts shape.
 * If a block has unknown type or missing fields, it renders a fallback (see BlockRenderer).
 */

export const BLOCK_TYPES = {
  texto: {
    label: 'Texto',
    description: 'Prosa narrativa con LaTeX inline.',
    icon: 'AlignLeft',
    defaultBlock: () => ({
      body_md: '',
    }),
  },
  definicion: {
    label: 'Definición',
    description: 'Concepto formal destacado. Lo que el alumno debe memorizar.',
    icon: 'BookMarked',
    defaultBlock: () => ({
      titulo: '',
      body_md: '',
    }),
  },
  teorema: {
    label: 'Teorema',
    description: 'Enunciado formal con hipótesis explícitas y demostración colapsable.',
    icon: 'Sigma',
    defaultBlock: () => ({
      nombre: '',
      hipotesis: [],
      enunciado_md: '',
      demostracion_md: '',
      demostracion_default_open: false,
    }),
  },
  intuicion: {
    label: 'Intuición',
    description: 'Explicación informal o visual antes del formalismo.',
    icon: 'Lightbulb',
    defaultBlock: () => ({
      titulo: '',
      body_md: '',
    }),
  },
  ejemplo_resuelto: {
    label: 'Ejemplo resuelto',
    description: 'Problema con pasos numerados (acción + justificación).',
    icon: 'PencilLine',
    defaultBlock: () => ({
      titulo: '',
      problema_md: '',
      pasos: [
        { accion_md: '', justificacion_md: '', es_resultado: false },
      ],
    }),
  },
  grafico_desmos: {
    label: 'Gráfico Desmos',
    description: 'Calculadora interactiva con guía de qué observar.',
    icon: 'LineChart',
    defaultBlock: () => ({
      // Si `desmos_url` está presente y no vacío, embebe ese calculator
      // preconfigurado (recomendado para gráficos complejos guardados en
      // desmos.com). Si no, se construye desde `expresiones[]` con la API.
      desmos_url: '',
      expresiones: [''],
      guia_md: '',
      altura: 400,
    }),
  },
  figura: {
    label: 'Figura',
    description: 'Imagen estática (Cloudinary) con caption + prompt de generación (admin only).',
    icon: 'Image',
    defaultBlock: () => ({
      image_url: '',
      caption_md: '',
      // Prompt para generar la imagen externamente (ej. ChatGPT Images).
      // Es metadata del admin — NO se muestra al alumno. Persiste en la lección
      // para poder regenerar la imagen más adelante con el mismo prompt.
      prompt_image_md: '',
    }),
  },
  verificacion: {
    label: 'Verificación',
    description: 'Mini-quiz inline con feedback inmediato (1-3 preguntas).',
    icon: 'CheckCircle2',
    defaultBlock: () => ({
      intro_md: 'Antes de seguir, asegurate de entender:',
      preguntas: [
        {
          enunciado_md: '',
          opciones_md: ['', '', '', ''],
          correcta: 'A',
          // pista_md: opcional. Si está, aparece un botón "Ver pista"
          // antes de "Verificar". No bloquea ni penaliza.
          pista_md: '',
          explicacion_md: '',
        },
      ],
    }),
  },
  ejercicio: {
    label: 'Ejercicio',
    description: 'Problema para que el alumno resuelva. Pistas progresivas y solución colapsables.',
    icon: 'Target',
    defaultBlock: () => ({
      titulo: '',
      enunciado_md: '',
      // Pistas en orden de menor a mayor revelación. Cada una se muestra
      // bajo demanda con un botón "Pista N". Pueden quedar vacías.
      pistas_md: [''],
      // Solución completa, colapsable. El alumno la abre cuando termina o se rinde.
      solucion_md: '',
    }),
  },
  errores_comunes: {
    label: 'Errores comunes',
    description: 'Pitfalls nombrados explícitamente.',
    icon: 'AlertTriangle',
    defaultBlock: () => ({
      items_md: [''],
    }),
  },
  resumen: {
    label: 'Resumen',
    description: 'Bullets clave al final de la lección.',
    icon: 'ListChecks',
    defaultBlock: () => ({
      puntos_md: [''],
    }),
  },
};

export const BLOCK_TYPE_KEYS = Object.keys(BLOCK_TYPES);

/**
 * Create a new block of the given type with a fresh uuid.
 * Uses crypto.randomUUID() (available in modern browsers; fallback to Math.random).
 */
export function createBlock(type) {
  const def = BLOCK_TYPES[type];
  if (!def) throw new Error(`Unknown block type: ${type}`);
  const id = (typeof crypto !== 'undefined' && crypto.randomUUID)
    ? crypto.randomUUID()
    : `b_${Math.random().toString(36).slice(2)}_${Date.now()}`;
  return { id, type, ...def.defaultBlock() };
}
