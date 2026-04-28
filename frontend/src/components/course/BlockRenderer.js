import { useState, lazy, Suspense } from 'react';
import {
  BookMarked, Sigma, Lightbulb, PencilLine, Image as ImageIcon,
  CheckCircle2, AlertTriangle, ListChecks, ChevronDown, ChevronRight,
  Check, X, Target, HelpCircle, Eye
} from 'lucide-react';
import MarkdownRenderer from './MarkdownRenderer';
import InlineMd from './InlineMd';

const DesmosEmbed = lazy(() => import('./DesmosEmbed'));

/**
 * BlockRenderer — renders a lesson's typed content blocks for students.
 * Each block type has its own visual treatment optimized for advanced math.
 */

// ============ helpers ============

// Block-level markdown (full prose styling, paragraphs allowed).
// Routes through MarkdownRenderer which also handles [DESMOS:...] etc.
const Md = ({ children, className = '' }) => {
  if (!children) return null;
  return (
    <div className={`prose prose-slate dark:prose-invert max-w-none ${className}`}>
      <MarkdownRenderer content={children} />
    </div>
  );
};

// ============ block components ============

const TextoBlock = ({ block }) => (
  <div className="my-6">
    <Md>{block.body_md}</Md>
  </div>
);

const DefinicionBlock = ({ block }) => (
  <div className="my-6 border-l-4 border-cyan-500 bg-cyan-50/60 dark:bg-cyan-950/20 rounded-r-lg p-5">
    <div className="flex items-center gap-2 mb-2 text-cyan-700 dark:text-cyan-300 flex-wrap">
      <BookMarked size={18} />
      <span className="text-xs font-bold uppercase tracking-wider">Definición</span>
      {block.titulo && (
        <span className="text-sm font-semibold text-foreground">— <InlineMd>{block.titulo}</InlineMd></span>
      )}
    </div>
    <Md>{block.body_md}</Md>
  </div>
);

const TeoremaBlock = ({ block }) => {
  const [openProof, setOpenProof] = useState(!!block.demostracion_default_open);
  const hasProof = !!(block.demostracion_md && block.demostracion_md.trim());

  return (
    <div className="my-6 border-l-4 border-amber-500 bg-amber-50/60 dark:bg-amber-950/20 rounded-r-lg p-5">
      <div className="flex items-center gap-2 mb-2 text-amber-700 dark:text-amber-300 flex-wrap">
        <Sigma size={18} />
        <span className="text-xs font-bold uppercase tracking-wider">Teorema</span>
        {block.nombre && (
          <span className="text-sm font-semibold text-foreground">— <InlineMd>{block.nombre}</InlineMd></span>
        )}
      </div>

      {block.hipotesis && block.hipotesis.length > 0 && (
        <div className="mb-3">
          <div className="text-xs font-semibold text-muted-foreground mb-1">Hipótesis:</div>
          <ul className="space-y-1">
            {block.hipotesis.map((h, i) => (
              <li key={i} className="flex items-start gap-2 text-sm">
                <Check size={16} className="mt-0.5 shrink-0 text-amber-600" />
                <span className="flex-1"><InlineMd>{h}</InlineMd></span>
              </li>
            ))}
          </ul>
        </div>
      )}

      <Md>{block.enunciado_md}</Md>

      {hasProof && (
        <div className="mt-4 border-t border-amber-200 dark:border-amber-800 pt-3">
          <button
            type="button"
            onClick={() => setOpenProof(o => !o)}
            className="flex items-center gap-2 text-sm font-semibold text-amber-700 dark:text-amber-300 hover:text-amber-900 dark:hover:text-amber-100"
          >
            {openProof ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
            Demostración
          </button>
          {openProof && (
            <div className="mt-2 pl-6 border-l-2 border-amber-200 dark:border-amber-800">
              <Md>{block.demostracion_md}</Md>
              <div className="text-right text-amber-700 dark:text-amber-300 font-bold mt-2">∎</div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

const IntuicionBlock = ({ block }) => (
  <div className="my-6 border border-yellow-200 dark:border-yellow-800/50 bg-yellow-50/40 dark:bg-yellow-950/10 rounded-lg p-5">
    <div className="flex items-center gap-2 mb-2 text-yellow-700 dark:text-yellow-300 flex-wrap">
      <Lightbulb size={18} />
      <span className="text-xs font-bold uppercase tracking-wider">Intuición</span>
      {block.titulo && (
        <span className="text-sm font-semibold text-foreground">— <InlineMd>{block.titulo}</InlineMd></span>
      )}
    </div>
    <Md>{block.body_md}</Md>
  </div>
);

const EjemploResueltoBlock = ({ block }) => (
  <div className="my-6 border border-emerald-200 dark:border-emerald-800/50 bg-emerald-50/40 dark:bg-emerald-950/10 rounded-lg overflow-hidden">
    <div className="px-5 py-3 bg-emerald-100/60 dark:bg-emerald-900/30 border-b border-emerald-200 dark:border-emerald-800/50">
      <div className="flex items-center gap-2 text-emerald-700 dark:text-emerald-300 flex-wrap">
        <PencilLine size={18} />
        <span className="text-xs font-bold uppercase tracking-wider">Ejemplo resuelto</span>
        {block.titulo && (
          <span className="text-sm font-semibold text-foreground">— <InlineMd>{block.titulo}</InlineMd></span>
        )}
      </div>
    </div>
    <div className="p-5">
      {block.problema_md && (
        <div className="mb-4">
          <div className="text-xs font-semibold text-muted-foreground mb-1">Problema:</div>
          <Md>{block.problema_md}</Md>
        </div>
      )}

      {block.pasos && block.pasos.length > 0 && (
        <ol className="space-y-3 list-none p-0 m-0">
          {block.pasos.map((paso, i) => (
            <li key={i} className={`flex gap-3 ${paso.es_resultado ? 'pt-3 border-t-2 border-emerald-300 dark:border-emerald-700' : ''}`}>
              <div className={`shrink-0 w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold ${
                paso.es_resultado
                  ? 'bg-emerald-600 text-white'
                  : 'bg-emerald-200 dark:bg-emerald-800 text-emerald-800 dark:text-emerald-200'
              }`}>
                {paso.es_resultado ? '✓' : i + 1}
              </div>
              <div className="flex-1 min-w-0">
                <Md className="!mt-0">{paso.accion_md}</Md>
                {paso.justificacion_md && (
                  <div className="mt-1 text-sm text-muted-foreground italic">
                    <InlineMd>{paso.justificacion_md}</InlineMd>
                  </div>
                )}
              </div>
            </li>
          ))}
        </ol>
      )}
    </div>
  </div>
);

// Normalize a desmos.com calculator URL to its /embed form.
// Examples:
//   https://www.desmos.com/calculator/abc123          → https://www.desmos.com/calculator/abc123/embed
//   https://www.desmos.com/calculator/abc123?lang=es  → https://www.desmos.com/calculator/abc123/embed?lang=es
//   https://www.desmos.com/calculator/abc123/embed    → unchanged
function buildDesmosEmbedUrl(rawUrl) {
  if (!rawUrl) return '';
  try {
    const url = new URL(rawUrl);
    if (!url.pathname.endsWith('/embed')) {
      url.pathname = url.pathname.replace(/\/?$/, '/embed');
    }
    return url.toString();
  } catch {
    return rawUrl;
  }
}

const GraficoDesmosBlock = ({ block }) => {
  const altura = block.altura || 400;
  const hasUrl = block.desmos_url && block.desmos_url.trim();

  return (
    <div className="my-6">
      <div className="rounded-lg overflow-hidden border border-border">
        {hasUrl ? (
          <iframe
            src={buildDesmosEmbedUrl(block.desmos_url.trim())}
            title="Gráfico Desmos"
            width="100%"
            height={altura}
            style={{ border: 0, display: 'block' }}
            allowFullScreen
          />
        ) : (
          <Suspense fallback={
            <div className="p-8 bg-secondary text-center text-muted-foreground">Cargando gráfico...</div>
          }>
            <DesmosEmbed
              equation={(block.expresiones || []).filter(Boolean).join('; ')}
              height={altura}
            />
          </Suspense>
        )}
      </div>
      {block.guia_md && (
        <div className="mt-3 p-3 bg-secondary/40 rounded text-sm">
          <Md>{block.guia_md}</Md>
        </div>
      )}
    </div>
  );
};

const FiguraBlock = ({ block }) => {
  // Note: prompt_image_md is admin-only metadata and is intentionally NOT rendered
  // for students. It only appears in the admin block editor.
  return (
    <figure className="my-6">
      {block.image_url ? (
        <div className="rounded-lg overflow-hidden border border-border bg-white">
          <img
            src={block.image_url}
            alt={block.caption_md || ''}
            className="w-full h-auto"
            onError={(e) => { e.currentTarget.style.display = 'none'; }}
          />
        </div>
      ) : (
        <div className="rounded-lg border-2 border-dashed border-border bg-secondary/30 p-12 flex flex-col items-center justify-center text-muted-foreground">
          <ImageIcon size={32} className="mb-2 opacity-50" />
          <span className="text-sm italic">Imagen pendiente</span>
        </div>
      )}
      {block.caption_md && (
        <figcaption className="mt-2 text-sm text-muted-foreground text-center italic">
          <InlineMd>{block.caption_md}</InlineMd>
        </figcaption>
      )}
    </figure>
  );
};

const VerificacionPregunta = ({ pregunta, idx }) => {
  const [selected, setSelected] = useState(null);
  const [showFeedback, setShowFeedback] = useState(false);
  const [showHint, setShowHint] = useState(false);

  const letters = ['A', 'B', 'C', 'D'];
  const isCorrect = selected === pregunta.correcta;
  const hasHint = !!(pregunta.pista_md && pregunta.pista_md.trim());

  return (
    <div className="border border-purple-200 dark:border-purple-800/50 rounded-md p-4 bg-white dark:bg-slate-900/40">
      <div className="text-xs font-semibold text-muted-foreground mb-2">Pregunta {idx + 1}</div>
      <Md>{pregunta.enunciado_md}</Md>

      <div className="mt-3 space-y-2">
        {(pregunta.opciones_md || []).slice(0, 4).map((opt, i) => {
          const letter = letters[i];
          const isSelected = selected === letter;
          const showResult = showFeedback;
          let cls = 'border-border hover:border-purple-400 bg-background';
          if (showResult) {
            if (letter === pregunta.correcta) cls = 'border-emerald-500 bg-emerald-50 dark:bg-emerald-950/30';
            else if (isSelected) cls = 'border-red-500 bg-red-50 dark:bg-red-950/30';
            else cls = 'border-border opacity-60';
          } else if (isSelected) {
            cls = 'border-purple-500 bg-purple-50 dark:bg-purple-950/30';
          }
          return (
            <button
              key={i}
              type="button"
              disabled={showFeedback}
              onClick={() => setSelected(letter)}
              className={`w-full text-left p-3 rounded-md border-2 transition-colors flex items-start gap-3 ${cls}`}
            >
              <span className="shrink-0 w-6 h-6 rounded-full bg-secondary flex items-center justify-center text-xs font-bold">
                {letter}
              </span>
              <span className="flex-1 min-w-0 text-sm">
                <InlineMd>{opt}</InlineMd>
              </span>
              {showResult && letter === pregunta.correcta && <Check size={18} className="text-emerald-600 shrink-0" />}
              {showResult && isSelected && letter !== pregunta.correcta && <X size={18} className="text-red-600 shrink-0" />}
            </button>
          );
        })}
      </div>

      {hasHint && showHint && (
        <div className="mt-3 p-3 rounded-md bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800/40 text-sm">
          <div className="flex items-center gap-2 text-amber-700 dark:text-amber-300 font-semibold text-xs uppercase tracking-wide mb-1">
            <HelpCircle size={14} /> Pista
          </div>
          <Md>{pregunta.pista_md}</Md>
        </div>
      )}

      {!showFeedback ? (
        <div className="mt-3 flex items-center gap-2 flex-wrap">
          {hasHint && !showHint && (
            <button
              type="button"
              onClick={() => setShowHint(true)}
              className="px-3 py-2 rounded-md text-sm font-medium border border-amber-300 dark:border-amber-700 text-amber-700 dark:text-amber-300 hover:bg-amber-50 dark:hover:bg-amber-950/30 inline-flex items-center gap-1.5"
            >
              <HelpCircle size={14} /> Ver pista
            </button>
          )}
          <button
            type="button"
            disabled={!selected}
            onClick={() => setShowFeedback(true)}
            className="px-4 py-2 rounded-md text-sm font-semibold bg-purple-600 text-white hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Verificar
          </button>
        </div>
      ) : (
        <div className={`mt-3 p-3 rounded-md text-sm ${
          isCorrect
            ? 'bg-emerald-50 dark:bg-emerald-950/30 text-emerald-900 dark:text-emerald-100'
            : 'bg-red-50 dark:bg-red-950/30 text-red-900 dark:text-red-100'
        }`}>
          <div className="font-semibold mb-1">
            {isCorrect ? '¡Correcto!' : `Respuesta correcta: ${pregunta.correcta}`}
          </div>
          {pregunta.explicacion_md && <Md>{pregunta.explicacion_md}</Md>}
        </div>
      )}
    </div>
  );
};

const VerificacionBlock = ({ block }) => (
  <div className="my-6 bg-purple-50/40 dark:bg-purple-950/10 border border-purple-200 dark:border-purple-800/50 rounded-lg p-5">
    <div className="flex items-center gap-2 mb-3 text-purple-700 dark:text-purple-300">
      <CheckCircle2 size={18} />
      <span className="text-xs font-bold uppercase tracking-wider">Verificación</span>
    </div>
    {block.intro_md && (
      <div className="mb-3 text-sm text-muted-foreground">
        <InlineMd>{block.intro_md}</InlineMd>
      </div>
    )}
    <div className="space-y-3">
      {(block.preguntas || []).map((p, i) => (
        <VerificacionPregunta key={i} pregunta={p} idx={i} />
      ))}
    </div>
  </div>
);

const ErroresComunesBlock = ({ block }) => (
  <div className="my-6 border-l-4 border-red-500 bg-red-50/60 dark:bg-red-950/20 rounded-r-lg p-5">
    <div className="flex items-center gap-2 mb-2 text-red-700 dark:text-red-300">
      <AlertTriangle size={18} />
      <span className="text-xs font-bold uppercase tracking-wider">Errores comunes</span>
    </div>
    <ul className="space-y-2">
      {(block.items_md || []).map((item, i) => (
        <li key={i} className="flex items-start gap-2 text-sm">
          <span className="shrink-0 mt-1 text-red-600">•</span>
          <span className="flex-1"><InlineMd>{item}</InlineMd></span>
        </li>
      ))}
    </ul>
  </div>
);

const EjercicioBlock = ({ block }) => {
  const pistas = (block.pistas_md || []).filter(p => p && p.trim());
  const [revealed, setRevealed] = useState(0); // cuántas pistas mostradas
  const [showSolution, setShowSolution] = useState(false);
  const hasSolution = !!(block.solucion_md && block.solucion_md.trim());

  return (
    <div className="my-6 border-l-4 border-emerald-500 bg-emerald-50/50 dark:bg-emerald-950/15 rounded-r-lg p-5">
      <div className="flex items-center gap-2 mb-2 text-emerald-700 dark:text-emerald-300 flex-wrap">
        <Target size={18} />
        <span className="text-xs font-bold uppercase tracking-wider">Ejercicio</span>
        {block.titulo && (
          <span className="text-sm font-semibold text-foreground">— <InlineMd>{block.titulo}</InlineMd></span>
        )}
      </div>
      <Md>{block.enunciado_md}</Md>

      {pistas.length > 0 && (
        <div className="mt-4 space-y-2">
          {pistas.slice(0, revealed).map((p, i) => (
            <div key={i} className="p-3 rounded-md bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800/40 text-sm">
              <div className="flex items-center gap-2 text-amber-700 dark:text-amber-300 font-semibold text-xs uppercase tracking-wide mb-1">
                <HelpCircle size={14} /> Pista {i + 1}
              </div>
              <Md>{p}</Md>
            </div>
          ))}
          {revealed < pistas.length && (
            <button
              type="button"
              onClick={() => setRevealed(revealed + 1)}
              className="px-3 py-2 rounded-md text-sm font-medium border border-amber-300 dark:border-amber-700 text-amber-700 dark:text-amber-300 hover:bg-amber-50 dark:hover:bg-amber-950/30 inline-flex items-center gap-1.5"
            >
              <HelpCircle size={14} />
              {revealed === 0 ? 'Ver pista' : `Ver pista ${revealed + 1}`}
            </button>
          )}
        </div>
      )}

      {hasSolution && (
        <div className="mt-4">
          <button
            type="button"
            onClick={() => setShowSolution(!showSolution)}
            className="px-3 py-2 rounded-md text-sm font-medium border border-emerald-400 dark:border-emerald-700 text-emerald-700 dark:text-emerald-300 hover:bg-emerald-100 dark:hover:bg-emerald-950/40 inline-flex items-center gap-1.5"
          >
            <Eye size={14} />
            {showSolution ? 'Ocultar solución' : 'Ver solución'}
            {showSolution ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
          </button>
          {showSolution && (
            <div className="mt-3 p-4 rounded-md bg-white dark:bg-slate-900/50 border border-emerald-200 dark:border-emerald-800/50">
              <div className="text-xs font-semibold text-emerald-700 dark:text-emerald-300 uppercase tracking-wide mb-2">Solución</div>
              <Md>{block.solucion_md}</Md>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

const ResumenBlock = ({ block }) => (
  <div className="my-6 bg-slate-100 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 rounded-lg p-5">
    <div className="flex items-center gap-2 mb-3 text-slate-700 dark:text-slate-300">
      <ListChecks size={18} />
      <span className="text-xs font-bold uppercase tracking-wider">Resumen</span>
    </div>
    <ul className="space-y-2">
      {(block.puntos_md || []).map((punto, i) => (
        <li key={i} className="flex items-start gap-2">
          <span className="shrink-0 mt-1 w-1.5 h-1.5 rounded-full bg-slate-500 mt-2" />
          <div className="flex-1"><InlineMd>{punto}</InlineMd></div>
        </li>
      ))}
    </ul>
  </div>
);

// ============ dispatch ============

const RENDERERS = {
  texto: TextoBlock,
  definicion: DefinicionBlock,
  teorema: TeoremaBlock,
  intuicion: IntuicionBlock,
  ejemplo_resuelto: EjemploResueltoBlock,
  grafico_desmos: GraficoDesmosBlock,
  figura: FiguraBlock,
  verificacion: VerificacionBlock,
  ejercicio: EjercicioBlock,
  errores_comunes: ErroresComunesBlock,
  resumen: ResumenBlock,
};

export default function BlockRenderer({ blocks }) {
  if (!Array.isArray(blocks) || blocks.length === 0) {
    return (
      <div className="text-center py-12 text-muted-foreground italic">
        Esta lección aún no tiene contenido.
      </div>
    );
  }

  return (
    <div className="lesson-blocks">
      {blocks.map((block, i) => {
        const Renderer = RENDERERS[block.type];
        if (!Renderer) {
          return (
            <div key={block.id || i} className="my-4 p-3 border border-dashed border-red-400 rounded text-sm text-red-700 bg-red-50 dark:bg-red-950/20">
              <strong>Bloque desconocido:</strong> tipo "{block.type}" no implementado.
            </div>
          );
        }
        return <Renderer key={block.id || i} block={block} />;
      })}
    </div>
  );
}
