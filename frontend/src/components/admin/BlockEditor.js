import { useState, useRef } from 'react';
import axios from 'axios';
import {
  Plus, Trash2, ChevronUp, ChevronDown, ChevronRight,
  AlignLeft, BookMarked, Sigma, Lightbulb, PencilLine, LineChart,
  Image as ImageIcon, CheckCircle2, AlertTriangle, ListChecks,
  Copy, Upload, Loader2, GripVertical, Target
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Switch } from '@/components/ui/switch';
import { toast } from 'sonner';
import { BLOCK_TYPES, BLOCK_TYPE_KEYS, createBlock } from '@/lib/blockTypes';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const ADMIN_API = `${BACKEND_URL}/api/admin`;

// Map block type to its lucide icon (matches BlockRenderer visual identity).
const TYPE_ICON = {
  texto: AlignLeft,
  definicion: BookMarked,
  teorema: Sigma,
  intuicion: Lightbulb,
  ejemplo_resuelto: PencilLine,
  grafico_desmos: LineChart,
  figura: ImageIcon,
  verificacion: CheckCircle2,
  ejercicio: Target,
  errores_comunes: AlertTriangle,
  resumen: ListChecks,
};

// ============ Generic small fields ============

const Field = ({ label, hint, children }) => (
  <div className="space-y-1">
    {label && <Label className="text-xs text-muted-foreground">{label}</Label>}
    {children}
    {hint && <p className="text-xs text-muted-foreground italic">{hint}</p>}
  </div>
);

// Editable list of plain string items rendered as textareas.
// Used by errores_comunes, resumen, hipótesis, expresiones.
const StringListField = ({ items, onChange, label, addLabel = 'Agregar', placeholder = '', minRows = 2, allowEmpty = true }) => {
  const update = (idx, value) => {
    const next = [...items];
    next[idx] = value;
    onChange(next);
  };
  const remove = (idx) => {
    if (!allowEmpty && items.length <= 1) return;
    onChange(items.filter((_, i) => i !== idx));
  };
  const add = () => onChange([...items, '']);
  const move = (idx, dir) => {
    const target = idx + dir;
    if (target < 0 || target >= items.length) return;
    const next = [...items];
    [next[idx], next[target]] = [next[target], next[idx]];
    onChange(next);
  };

  return (
    <Field label={label}>
      <div className="space-y-2">
        {items.map((it, i) => (
          <div key={i} className="flex items-start gap-2">
            <div className="flex flex-col gap-0.5 pt-1">
              <button type="button" onClick={() => move(i, -1)} disabled={i === 0} className="text-muted-foreground hover:text-foreground disabled:opacity-30">
                <ChevronUp size={14} />
              </button>
              <button type="button" onClick={() => move(i, 1)} disabled={i === items.length - 1} className="text-muted-foreground hover:text-foreground disabled:opacity-30">
                <ChevronDown size={14} />
              </button>
            </div>
            <Textarea
              value={it}
              onChange={(e) => update(i, e.target.value)}
              placeholder={placeholder}
              rows={minRows}
              className="font-mono text-sm flex-1"
            />
            <Button
              type="button"
              variant="ghost"
              size="sm"
              onClick={() => remove(i)}
              disabled={!allowEmpty && items.length <= 1}
              className="text-red-600 hover:text-red-700 mt-1"
            >
              <Trash2 size={14} />
            </Button>
          </div>
        ))}
        <Button type="button" variant="outline" size="sm" onClick={add}>
          <Plus size={14} className="mr-1" /> {addLabel}
        </Button>
      </div>
    </Field>
  );
};

// Image upload via /api/admin/upload-image (Cloudinary).
const ImageUploadField = ({ url, onChange }) => {
  const inputRef = useRef(null);
  const [uploading, setUploading] = useState(false);

  const handleFile = async (file) => {
    if (!file) return;
    if (!file.type.startsWith('image/')) {
      toast.error('Solo se permiten archivos de imagen');
      return;
    }
    setUploading(true);
    try {
      const token = localStorage.getItem('admin_token');
      const fd = new FormData();
      fd.append('file', file);
      const res = await axios.post(`${ADMIN_API}/upload-image`, fd, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });
      const newUrl = res.data.image_url;
      // Normalize: backend may return /api/uploads/... or full Cloudinary URL.
      const fullUrl = newUrl.startsWith('/api') ? `${BACKEND_URL}${newUrl}` : newUrl;
      onChange(fullUrl);
      toast.success('Imagen subida');
    } catch (e) {
      console.error(e);
      toast.error('Error al subir imagen');
    } finally {
      setUploading(false);
      if (inputRef.current) inputRef.current.value = '';
    }
  };

  return (
    <Field label="Imagen">
      <div className="flex items-start gap-3">
        <div className="w-32 h-24 rounded border border-border bg-secondary/30 flex items-center justify-center overflow-hidden shrink-0">
          {url ? (
            <img src={url} alt="" className="w-full h-full object-contain" onError={(e) => { e.currentTarget.style.display = 'none'; }} />
          ) : (
            <ImageIcon size={28} className="text-muted-foreground opacity-50" />
          )}
        </div>
        <div className="flex-1 space-y-2">
          <input
            ref={inputRef}
            type="file"
            accept="image/*"
            onChange={(e) => handleFile(e.target.files?.[0])}
            className="hidden"
            id={`upload-${Math.random()}`}
          />
          <div className="flex gap-2">
            <Button type="button" variant="outline" size="sm" onClick={() => inputRef.current?.click()} disabled={uploading}>
              {uploading ? <><Loader2 size={14} className="mr-1 animate-spin" /> Subiendo...</> : <><Upload size={14} className="mr-1" /> Subir archivo</>}
            </Button>
            {url && (
              <Button type="button" variant="ghost" size="sm" onClick={() => onChange('')} className="text-red-600">
                <Trash2 size={14} className="mr-1" /> Quitar
              </Button>
            )}
          </div>
          <Input
            value={url}
            onChange={(e) => onChange(e.target.value)}
            placeholder="O pegar URL de imagen"
            className="text-xs font-mono"
          />
        </div>
      </div>
    </Field>
  );
};

// ============ Forms per block type ============

const TextoForm = ({ block, onChange }) => (
  <Field label="Contenido (Markdown + LaTeX inline con $...$)">
    <Textarea
      value={block.body_md}
      onChange={(e) => onChange({ ...block, body_md: e.target.value })}
      rows={6}
      className="font-mono text-sm"
      placeholder="Texto narrativo. Usar $...$ para fórmulas inline y $$...$$ para fórmulas en bloque."
    />
  </Field>
);

const TitledBodyForm = ({ block, onChange, tituloLabel = 'Título', bodyLabel = 'Cuerpo' }) => (
  <div className="space-y-3">
    <Field label={tituloLabel}>
      <Input
        value={block.titulo || ''}
        onChange={(e) => onChange({ ...block, titulo: e.target.value })}
        placeholder="Ej: Derivada en un punto"
      />
    </Field>
    <Field label={bodyLabel}>
      <Textarea
        value={block.body_md}
        onChange={(e) => onChange({ ...block, body_md: e.target.value })}
        rows={6}
        className="font-mono text-sm"
      />
    </Field>
  </div>
);

const TeoremaForm = ({ block, onChange }) => (
  <div className="space-y-3">
    <Field label="Nombre del teorema">
      <Input
        value={block.nombre || ''}
        onChange={(e) => onChange({ ...block, nombre: e.target.value })}
        placeholder="Ej: Teorema del Valor Medio"
      />
    </Field>
    <StringListField
      label="Hipótesis (cada una se renderiza como ítem en checklist)"
      items={block.hipotesis || []}
      onChange={(hipotesis) => onChange({ ...block, hipotesis })}
      addLabel="Agregar hipótesis"
      placeholder="$f$ continua en $[a,b]$"
      minRows={1}
    />
    <Field label="Enunciado">
      <Textarea
        value={block.enunciado_md}
        onChange={(e) => onChange({ ...block, enunciado_md: e.target.value })}
        rows={4}
        className="font-mono text-sm"
        placeholder="Si... entonces..."
      />
    </Field>
    <Field label="Demostración (opcional, colapsable en la vista del alumno)">
      <Textarea
        value={block.demostracion_md || ''}
        onChange={(e) => onChange({ ...block, demostracion_md: e.target.value })}
        rows={6}
        className="font-mono text-sm"
        placeholder="Demostración paso a paso. Si se deja vacío, no aparece el botón de demostración."
      />
    </Field>
    <div className="flex items-center gap-3">
      <Switch
        checked={!!block.demostracion_default_open}
        onCheckedChange={(v) => onChange({ ...block, demostracion_default_open: v })}
      />
      <Label className="text-sm font-normal cursor-pointer">Mostrar demostración expandida por defecto</Label>
    </div>
  </div>
);

const EjemploResueltoForm = ({ block, onChange }) => {
  const updatePaso = (idx, patch) => {
    const next = [...block.pasos];
    next[idx] = { ...next[idx], ...patch };
    onChange({ ...block, pasos: next });
  };
  const addPaso = () => onChange({ ...block, pasos: [...block.pasos, { accion_md: '', justificacion_md: '', es_resultado: false }] });
  const removePaso = (idx) => onChange({ ...block, pasos: block.pasos.filter((_, i) => i !== idx) });
  const movePaso = (idx, dir) => {
    const target = idx + dir;
    if (target < 0 || target >= block.pasos.length) return;
    const next = [...block.pasos];
    [next[idx], next[target]] = [next[target], next[idx]];
    onChange({ ...block, pasos: next });
  };

  return (
    <div className="space-y-3">
      <Field label="Título (opcional)">
        <Input
          value={block.titulo || ''}
          onChange={(e) => onChange({ ...block, titulo: e.target.value })}
          placeholder="Ej: Derivada de $x^3$ en $x=1$"
        />
      </Field>
      <Field label="Enunciado del problema">
        <Textarea
          value={block.problema_md}
          onChange={(e) => onChange({ ...block, problema_md: e.target.value })}
          rows={2}
          className="font-mono text-sm"
        />
      </Field>
      <Field label={`Pasos (${block.pasos?.length || 0})`}>
        <div className="space-y-3">
          {(block.pasos || []).map((paso, i) => (
            <div key={i} className="border border-border rounded-md p-3 bg-secondary/20 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-muted-foreground">Paso {i + 1}{paso.es_resultado ? ' · resultado' : ''}</span>
                <div className="flex items-center gap-1">
                  <button type="button" onClick={() => movePaso(i, -1)} disabled={i === 0} className="text-muted-foreground hover:text-foreground disabled:opacity-30 p-1">
                    <ChevronUp size={14} />
                  </button>
                  <button type="button" onClick={() => movePaso(i, 1)} disabled={i === block.pasos.length - 1} className="text-muted-foreground hover:text-foreground disabled:opacity-30 p-1">
                    <ChevronDown size={14} />
                  </button>
                  <button type="button" onClick={() => removePaso(i)} className="text-red-600 hover:text-red-700 p-1">
                    <Trash2 size={14} />
                  </button>
                </div>
              </div>
              <Field label="Acción">
                <Textarea
                  value={paso.accion_md || ''}
                  onChange={(e) => updatePaso(i, { accion_md: e.target.value })}
                  rows={2}
                  className="font-mono text-xs"
                />
              </Field>
              <Field label="Justificación (por qué se hace este paso)" hint="Opcional pero recomendado: ayuda al alumno a entender el procedimiento.">
                <Textarea
                  value={paso.justificacion_md || ''}
                  onChange={(e) => updatePaso(i, { justificacion_md: e.target.value })}
                  rows={2}
                  className="font-mono text-xs"
                />
              </Field>
              <div className="flex items-center gap-3">
                <Switch
                  checked={!!paso.es_resultado}
                  onCheckedChange={(v) => updatePaso(i, { es_resultado: v })}
                />
                <Label className="text-xs font-normal cursor-pointer">Marcar como paso final / resultado</Label>
              </div>
            </div>
          ))}
          <Button type="button" variant="outline" size="sm" onClick={addPaso}>
            <Plus size={14} className="mr-1" /> Agregar paso
          </Button>
        </div>
      </Field>
    </div>
  );
};

const GraficoDesmosForm = ({ block, onChange }) => {
  const usingUrl = !!(block.desmos_url && block.desmos_url.trim());
  return (
    <div className="space-y-3">
      <Field
        label="URL de Desmos (recomendado)"
        hint="Pega un link de calculator preconfigurado de desmos.com (ej: https://www.desmos.com/calculator/abc123). Si está presente, se usa este calculator y se ignoran las expresiones de abajo."
      >
        <Input
          value={block.desmos_url || ''}
          onChange={(e) => onChange({ ...block, desmos_url: e.target.value })}
          placeholder="https://www.desmos.com/calculator/..."
          className="font-mono text-sm"
        />
      </Field>
      <div className={usingUrl ? 'opacity-50 pointer-events-none' : ''}>
        <StringListField
          label="O bien — Expresiones de Desmos (una por línea)"
          items={block.expresiones || []}
          onChange={(expresiones) => onChange({ ...block, expresiones })}
          addLabel="Agregar expresión"
          placeholder="f(x) = x^2"
          minRows={1}
          allowEmpty={false}
        />
      </div>
      <Field label="Guía para el alumno (qué observar / mover)" hint="Sin guía, el gráfico es decoración. Indicar qué slider mover y qué buscar.">
        <Textarea
          value={block.guia_md || ''}
          onChange={(e) => onChange({ ...block, guia_md: e.target.value })}
          rows={3}
          className="font-mono text-sm"
        />
      </Field>
      <Field label="Altura (px)">
        <Input
          type="number"
          min="200"
          max="800"
          value={block.altura || 400}
          onChange={(e) => onChange({ ...block, altura: parseInt(e.target.value) || 400 })}
          className="w-32"
        />
      </Field>
    </div>
  );
};

const FiguraForm = ({ block, onChange }) => {
  const copyPrompt = async () => {
    if (!block.prompt_image_md) {
      toast.info('No hay prompt para copiar');
      return;
    }
    try {
      await navigator.clipboard.writeText(block.prompt_image_md);
      toast.success('Prompt copiado al portapapeles');
    } catch {
      toast.error('No se pudo copiar');
    }
  };

  return (
    <div className="space-y-3">
      <ImageUploadField
        url={block.image_url || ''}
        onChange={(image_url) => onChange({ ...block, image_url })}
      />
      <Field label="Caption (visible al alumno, opcional)">
        <Textarea
          value={block.caption_md || ''}
          onChange={(e) => onChange({ ...block, caption_md: e.target.value })}
          rows={2}
          className="font-mono text-sm"
          placeholder="Pie de figura. Ej: La función $|x|$ es continua pero no derivable en $0$."
        />
      </Field>
      <div className="border-t border-border pt-3">
        <div className="flex items-center justify-between mb-1">
          <Label className="text-xs text-muted-foreground">
            Prompt para generar la imagen <span className="text-orange-600">(no visible al alumno)</span>
          </Label>
          <Button type="button" variant="ghost" size="sm" onClick={copyPrompt} disabled={!block.prompt_image_md}>
            <Copy size={14} className="mr-1" /> Copiar
          </Button>
        </div>
        <Textarea
          value={block.prompt_image_md || ''}
          onChange={(e) => onChange({ ...block, prompt_image_md: e.target.value })}
          rows={5}
          className="font-mono text-xs"
          placeholder="Describe la imagen para ChatGPT Images. Ej: Gráfico didáctico de f(x)=|x| en color cyan, con vértice marcado..."
        />
        <p className="text-xs text-muted-foreground italic mt-1">
          Flujo: escribe el prompt → copia → genera la imagen en ChatGPT Images → descarga → sube el archivo arriba.
        </p>
      </div>
    </div>
  );
};

const VerificacionForm = ({ block, onChange }) => {
  const updateP = (idx, patch) => {
    const next = [...block.preguntas];
    next[idx] = { ...next[idx], ...patch };
    onChange({ ...block, preguntas: next });
  };
  const updateOpt = (pIdx, oIdx, value) => {
    const next = [...block.preguntas];
    const opciones = [...(next[pIdx].opciones_md || ['', '', '', ''])];
    opciones[oIdx] = value;
    next[pIdx] = { ...next[pIdx], opciones_md: opciones };
    onChange({ ...block, preguntas: next });
  };
  const addP = () => onChange({
    ...block,
    preguntas: [...(block.preguntas || []), { enunciado_md: '', opciones_md: ['', '', '', ''], correcta: 'A', pista_md: '', explicacion_md: '' }]
  });
  const removeP = (idx) => onChange({ ...block, preguntas: block.preguntas.filter((_, i) => i !== idx) });
  const moveP = (idx, dir) => {
    const target = idx + dir;
    if (target < 0 || target >= block.preguntas.length) return;
    const next = [...block.preguntas];
    [next[idx], next[target]] = [next[target], next[idx]];
    onChange({ ...block, preguntas: next });
  };

  return (
    <div className="space-y-3">
      <Field label="Introducción (opcional)">
        <Textarea
          value={block.intro_md || ''}
          onChange={(e) => onChange({ ...block, intro_md: e.target.value })}
          rows={2}
          className="font-mono text-sm"
          placeholder="Ej: Antes de avanzar, conviene verificar..."
        />
      </Field>
      <Field label={`Preguntas (${block.preguntas?.length || 0})`}>
        <div className="space-y-3">
          {(block.preguntas || []).map((p, i) => (
            <div key={i} className="border border-border rounded-md p-3 bg-secondary/20 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-muted-foreground">Pregunta {i + 1}</span>
                <div className="flex items-center gap-1">
                  <button type="button" onClick={() => moveP(i, -1)} disabled={i === 0} className="text-muted-foreground hover:text-foreground disabled:opacity-30 p-1">
                    <ChevronUp size={14} />
                  </button>
                  <button type="button" onClick={() => moveP(i, 1)} disabled={i === block.preguntas.length - 1} className="text-muted-foreground hover:text-foreground disabled:opacity-30 p-1">
                    <ChevronDown size={14} />
                  </button>
                  <button type="button" onClick={() => removeP(i)} className="text-red-600 hover:text-red-700 p-1">
                    <Trash2 size={14} />
                  </button>
                </div>
              </div>
              <Field label="Enunciado">
                <Textarea
                  value={p.enunciado_md || ''}
                  onChange={(e) => updateP(i, { enunciado_md: e.target.value })}
                  rows={2}
                  className="font-mono text-xs"
                />
              </Field>
              <div className="grid grid-cols-2 gap-2">
                {['A', 'B', 'C', 'D'].map((letter, oIdx) => (
                  <Field key={letter} label={`Opción ${letter}`}>
                    <Input
                      value={p.opciones_md?.[oIdx] || ''}
                      onChange={(e) => updateOpt(i, oIdx, e.target.value)}
                      className="font-mono text-xs"
                    />
                  </Field>
                ))}
              </div>
              <div className="grid grid-cols-2 gap-3">
                <Field label="Respuesta correcta">
                  <Select value={p.correcta || 'A'} onValueChange={(v) => updateP(i, { correcta: v })}>
                    <SelectTrigger className="h-9">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {['A', 'B', 'C', 'D'].map(l => <SelectItem key={l} value={l}>{l}</SelectItem>)}
                    </SelectContent>
                  </Select>
                </Field>
              </div>
              <Field label="Pista (opcional, se muestra antes de responder)" hint="Aparece un botón 'Ver pista' junto a 'Verificar'. Útil para guiar sin spoilear la respuesta.">
                <Textarea
                  value={p.pista_md || ''}
                  onChange={(e) => updateP(i, { pista_md: e.target.value })}
                  rows={2}
                  className="font-mono text-xs"
                  placeholder="Ej: Recordá la identidad pitagórica..."
                />
              </Field>
              <Field label="Explicación (se muestra tras responder)">
                <Textarea
                  value={p.explicacion_md || ''}
                  onChange={(e) => updateP(i, { explicacion_md: e.target.value })}
                  rows={2}
                  className="font-mono text-xs"
                />
              </Field>
            </div>
          ))}
          <Button type="button" variant="outline" size="sm" onClick={addP}>
            <Plus size={14} className="mr-1" /> Agregar pregunta
          </Button>
        </div>
      </Field>
    </div>
  );
};

const EjercicioForm = ({ block, onChange }) => (
  <div className="space-y-3">
    <Field label="Título (opcional)">
      <Input
        value={block.titulo || ''}
        onChange={(e) => onChange({ ...block, titulo: e.target.value })}
        placeholder="Ej: Calcular el límite por factorización"
      />
    </Field>
    <Field label="Enunciado del ejercicio">
      <Textarea
        value={block.enunciado_md || ''}
        onChange={(e) => onChange({ ...block, enunciado_md: e.target.value })}
        rows={3}
        className="font-mono text-sm"
        placeholder="Ej: Calcular $\\lim_{x\\to 2} \\dfrac{x^2 - 4}{x - 2}$."
      />
    </Field>
    <StringListField
      label="Pistas progresivas (de menor a mayor revelación)"
      items={block.pistas_md || ['']}
      onChange={(pistas_md) => onChange({ ...block, pistas_md })}
      addLabel="Agregar pista"
      placeholder="Ej (pista 1): Sustitución directa da $0/0$, así hay que factorizar."
      minRows={2}
      allowEmpty={true}
    />
    <Field label="Solución completa (colapsable)" hint="El alumno la abre cuando termina o se rinde. Puede ser igual de detallada que un ejemplo resuelto.">
      <Textarea
        value={block.solucion_md || ''}
        onChange={(e) => onChange({ ...block, solucion_md: e.target.value })}
        rows={5}
        className="font-mono text-sm"
        placeholder="Ej: Factorizamos $x^2 - 4 = (x-2)(x+2)$..."
      />
    </Field>
  </div>
);

const ErroresComunesForm = ({ block, onChange }) => (
  <StringListField
    label="Errores comunes (cada uno es un ítem)"
    items={block.items_md || []}
    onChange={(items_md) => onChange({ ...block, items_md })}
    addLabel="Agregar error"
    placeholder="**Continua no implica derivable.** $|x|$ es continua pero..."
    minRows={2}
    allowEmpty={false}
  />
);

const ResumenForm = ({ block, onChange }) => (
  <StringListField
    label="Puntos clave del resumen"
    items={block.puntos_md || []}
    onChange={(puntos_md) => onChange({ ...block, puntos_md })}
    addLabel="Agregar punto"
    placeholder="Punto clave..."
    minRows={2}
    allowEmpty={false}
  />
);

// Dispatch table
const FORMS = {
  texto: TextoForm,
  definicion: (props) => <TitledBodyForm {...props} tituloLabel="Título" bodyLabel="Cuerpo de la definición" />,
  teorema: TeoremaForm,
  intuicion: (props) => <TitledBodyForm {...props} tituloLabel="Título (opcional)" bodyLabel="Explicación informal" />,
  ejemplo_resuelto: EjemploResueltoForm,
  grafico_desmos: GraficoDesmosForm,
  figura: FiguraForm,
  verificacion: VerificacionForm,
  ejercicio: EjercicioForm,
  errores_comunes: ErroresComunesForm,
  resumen: ResumenForm,
};

// ============ Block shell (header + collapsible body) ============

const blockSummary = (block) => {
  switch (block.type) {
    case 'texto':
      return (block.body_md || '').slice(0, 80).replace(/\s+/g, ' ').trim() || '(vacío)';
    case 'definicion':
    case 'intuicion':
      return block.titulo || '(sin título)';
    case 'teorema':
      return block.nombre || '(sin nombre)';
    case 'ejemplo_resuelto':
      return block.titulo || (block.problema_md || '').slice(0, 60) || '(sin enunciado)';
    case 'grafico_desmos':
      return (block.expresiones || []).filter(Boolean)[0] || '(sin expresiones)';
    case 'figura':
      return block.image_url ? 'Imagen subida' : (block.prompt_image_md ? 'Prompt sin imagen aún' : '(vacío)');
    case 'verificacion':
      return `${(block.preguntas || []).length} pregunta(s)`;
    case 'ejercicio':
      return block.titulo || (block.enunciado_md || '').slice(0, 60) || '(sin enunciado)';
    case 'errores_comunes':
      return `${(block.items_md || []).length} ítem(s)`;
    case 'resumen':
      return `${(block.puntos_md || []).length} punto(s)`;
    default:
      return '';
  }
};

const BlockShell = ({ block, idx, total, onUpdate, onRemove, onMove, expanded, onToggle }) => {
  const Icon = TYPE_ICON[block.type] || AlignLeft;
  const Form = FORMS[block.type];
  const meta = BLOCK_TYPES[block.type];

  return (
    <div className="border border-border rounded-lg bg-background overflow-hidden">
      <button
        type="button"
        onClick={onToggle}
        className="w-full flex items-center gap-2 px-3 py-2 bg-secondary/40 hover:bg-secondary/70 text-left"
      >
        <span className="text-muted-foreground shrink-0">
          {expanded ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
        </span>
        <Icon size={16} className="text-primary shrink-0" />
        <span className="text-xs font-bold uppercase tracking-wider text-primary shrink-0">
          {meta?.label || block.type}
        </span>
        <span className="text-sm text-muted-foreground truncate flex-1">
          — {blockSummary(block)}
        </span>
        <span className="flex items-center gap-0.5 shrink-0" onClick={(e) => e.stopPropagation()}>
          <Button type="button" variant="ghost" size="sm" onClick={() => onMove(-1)} disabled={idx === 0} className="h-7 w-7 p-0">
            <ChevronUp size={14} />
          </Button>
          <Button type="button" variant="ghost" size="sm" onClick={() => onMove(1)} disabled={idx === total - 1} className="h-7 w-7 p-0">
            <ChevronDown size={14} />
          </Button>
          <Button type="button" variant="ghost" size="sm" onClick={onRemove} className="h-7 w-7 p-0 text-red-600 hover:text-red-700">
            <Trash2 size={14} />
          </Button>
        </span>
      </button>
      {expanded && (
        <div className="p-4 border-t border-border">
          {Form ? <Form block={block} onChange={onUpdate} /> : (
            <div className="text-sm text-red-600">Form no implementado para tipo "{block.type}"</div>
          )}
        </div>
      )}
    </div>
  );
};

// ============ Add-block dropdown ============

const AddBlockMenu = ({ onAdd }) => {
  const [open, setOpen] = useState(false);
  return (
    <div className="relative">
      <Button type="button" variant="outline" onClick={() => setOpen(o => !o)} className="w-full justify-start">
        <Plus size={16} className="mr-2" />
        Agregar bloque
      </Button>
      {open && (
        <>
          <div className="fixed inset-0 z-10" onClick={() => setOpen(false)} />
          <div className="absolute z-20 mt-1 w-full max-w-md bg-popover border border-border rounded-md shadow-lg overflow-hidden">
            <div className="grid grid-cols-2 gap-1 p-1 max-h-96 overflow-y-auto">
              {BLOCK_TYPE_KEYS.map((type) => {
                const meta = BLOCK_TYPES[type];
                const Icon = TYPE_ICON[type] || AlignLeft;
                return (
                  <button
                    key={type}
                    type="button"
                    onClick={() => { onAdd(type); setOpen(false); }}
                    className="text-left p-2 hover:bg-secondary rounded flex items-start gap-2"
                  >
                    <Icon size={16} className="text-primary mt-0.5 shrink-0" />
                    <div className="min-w-0">
                      <div className="text-sm font-semibold">{meta.label}</div>
                      <div className="text-xs text-muted-foreground line-clamp-2">{meta.description}</div>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

// ============ Main editor ============

export default function BlockEditor({ blocks = [], onChange }) {
  const [expandedId, setExpandedId] = useState(null);

  const updateBlock = (idx, newBlock) => {
    const next = [...blocks];
    next[idx] = newBlock;
    onChange(next);
  };

  const removeBlock = (idx) => {
    onChange(blocks.filter((_, i) => i !== idx));
  };

  const moveBlock = (idx, dir) => {
    const target = idx + dir;
    if (target < 0 || target >= blocks.length) return;
    const next = [...blocks];
    [next[idx], next[target]] = [next[target], next[idx]];
    onChange(next);
  };

  const addBlock = (type) => {
    const newBlock = createBlock(type);
    onChange([...blocks, newBlock]);
    setExpandedId(newBlock.id); // expand newly added
  };

  return (
    <div className="space-y-3">
      {blocks.length === 0 ? (
        <div className="text-center py-8 text-muted-foreground text-sm border border-dashed border-border rounded-lg">
          La lección está vacía. Agrega tu primer bloque para comenzar.
        </div>
      ) : (
        <div className="space-y-2">
          {blocks.map((block, idx) => (
            <BlockShell
              key={block.id || idx}
              block={block}
              idx={idx}
              total={blocks.length}
              expanded={expandedId === block.id}
              onToggle={() => setExpandedId(prev => prev === block.id ? null : block.id)}
              onUpdate={(b) => updateBlock(idx, b)}
              onRemove={() => removeBlock(idx)}
              onMove={(dir) => moveBlock(idx, dir)}
            />
          ))}
        </div>
      )}
      <AddBlockMenu onAdd={addBlock} />
    </div>
  );
}
