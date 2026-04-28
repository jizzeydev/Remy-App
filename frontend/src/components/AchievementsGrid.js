/**
 * Reusable grid of achievement badges.
 *
 * Renders both unlocked and locked badges. Locked ones are desaturated and the
 * description is hidden until unlocked (avoids spoiling surprises). The icon
 * comes as a string from the backend (lucide-react icon name) and we resolve
 * it via the icon map below — keep this map in sync with the backend registry.
 */
import { useState } from 'react';
import { motion } from 'framer-motion';
import * as Icons from 'lucide-react';
import { Lock } from 'lucide-react';

// Tailwind class lookups so PurgeCSS can statically pick them up.
const COLOR_BG = {
  cyan:    'bg-cyan-500/15 ring-cyan-400/40',
  blue:    'bg-blue-500/15 ring-blue-400/40',
  emerald: 'bg-emerald-500/15 ring-emerald-400/40',
  violet:  'bg-violet-500/15 ring-violet-400/40',
  amber:   'bg-amber-500/15 ring-amber-400/40',
  rose:    'bg-rose-500/15 ring-rose-400/40'
};

const COLOR_FG = {
  cyan:    'text-cyan-600 dark:text-cyan-300',
  blue:    'text-blue-600 dark:text-blue-300',
  emerald: 'text-emerald-600 dark:text-emerald-300',
  violet:  'text-violet-600 dark:text-violet-300',
  amber:   'text-amber-600 dark:text-amber-300',
  rose:    'text-rose-600 dark:text-rose-300'
};

const RARITY_LABEL = {
  common: 'Común',
  rare: 'Raro',
  epic: 'Épico',
  legendary: 'Legendario'
};

const RARITY_GLOW = {
  common: '',
  rare: 'shadow-md',
  epic: 'shadow-lg shadow-violet-500/20',
  legendary: 'shadow-xl shadow-amber-500/30 ring-2'
};

function ResolvedIcon({ name, size = 24, className = '' }) {
  const Cmp = Icons[name] || Icons.Award;
  return <Cmp size={size} className={className} aria-hidden="true" />;
}

function AchievementBadge({ ach, onClick }) {
  const colorBg = ach.unlocked ? COLOR_BG[ach.color] || COLOR_BG.cyan : 'bg-muted ring-border';
  const colorFg = ach.unlocked ? COLOR_FG[ach.color] || COLOR_FG.cyan : 'text-muted-foreground';
  const glow = ach.unlocked ? RARITY_GLOW[ach.rarity] || '' : 'opacity-60';

  return (
    <button
      type="button"
      onClick={() => onClick?.(ach)}
      className={`group relative flex flex-col items-center text-center p-3 rounded-2xl ring-1 transition-all hover:scale-[1.03] focus:outline-none focus-visible:ring-2 focus-visible:ring-primary ${colorBg} ${glow}`}
      data-testid={`achievement-${ach.id}`}
      title={ach.unlocked ? ach.name : 'Logro bloqueado'}
    >
      <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${colorBg} ${ach.unlocked ? '' : 'grayscale'}`}>
        {ach.unlocked
          ? <ResolvedIcon name={ach.icon} size={26} className={colorFg} />
          : <Lock size={22} className="text-muted-foreground" aria-hidden="true" />
        }
      </div>
      <p className={`mt-2 text-xs font-semibold leading-tight line-clamp-2 ${ach.unlocked ? 'text-foreground' : 'text-muted-foreground'}`}>
        {ach.name}
      </p>
    </button>
  );
}

function AchievementDetailModal({ ach, onClose }) {
  if (!ach) return null;
  const colorBg = ach.unlocked ? COLOR_BG[ach.color] || COLOR_BG.cyan : 'bg-muted';
  const colorFg = ach.unlocked ? COLOR_FG[ach.color] || COLOR_FG.cyan : 'text-muted-foreground';
  return (
    <div
      className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
    >
      <motion.div
        initial={{ scale: 0.92, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.92, opacity: 0 }}
        transition={{ duration: 0.18, ease: [0.22, 1, 0.36, 1] }}
        className="bg-card border border-border rounded-2xl p-6 max-w-sm w-full text-center shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className={`w-20 h-20 rounded-2xl mx-auto mb-4 ring-1 flex items-center justify-center ${colorBg}`}>
          {ach.unlocked
            ? <ResolvedIcon name={ach.icon} size={42} className={colorFg} />
            : <Lock size={36} className="text-muted-foreground" aria-hidden="true" />
          }
        </div>
        <p className="text-xs uppercase tracking-wider text-muted-foreground font-semibold mb-1">
          {RARITY_LABEL[ach.rarity] || 'Logro'}
        </p>
        <h3 className="text-xl font-bold text-foreground tracking-tight mb-2">
          {ach.unlocked ? ach.name : '¿?'}
        </h3>
        <p className="text-sm text-muted-foreground">
          {ach.unlocked ? ach.description : 'Sigue jugando para descubrirlo.'}
        </p>
        {ach.unlocked && ach.unlocked_at && (
          <p className="text-xs text-muted-foreground mt-4">
            Desbloqueado el {new Date(ach.unlocked_at).toLocaleDateString('es-CL', { day: 'numeric', month: 'long', year: 'numeric' })}
          </p>
        )}
      </motion.div>
    </div>
  );
}

export default function AchievementsGrid({ achievements, maxToShow }) {
  const [selected, setSelected] = useState(null);
  if (!Array.isArray(achievements) || achievements.length === 0) {
    return <p className="text-sm text-muted-foreground">No hay logros disponibles.</p>;
  }

  // When a maxToShow cap is set, prioritize unlocked ones first so the user
  // sees their accomplishments even when the grid is truncated.
  const sorted = [...achievements].sort((a, b) => {
    if (a.unlocked !== b.unlocked) return a.unlocked ? -1 : 1;
    return 0;
  });
  const list = maxToShow ? sorted.slice(0, maxToShow) : sorted;

  return (
    <>
      <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-3">
        {list.map((ach) => (
          <AchievementBadge key={ach.id} ach={ach} onClick={setSelected} />
        ))}
      </div>
      <AchievementDetailModal ach={selected} onClose={() => setSelected(null)} />
    </>
  );
}
