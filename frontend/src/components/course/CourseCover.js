/**
 * Portada de curso reutilizable.
 *
 * Prioridad de renderizado:
 *   1. Si la universidad tiene logo_url → logo grande sobre fondo blanco con padding.
 *   2. Si la universidad tiene short_name (≠ 'GEN') → sigla en blanco sobre gradient.
 *   3. Fallback → primera letra del título sobre gradient.
 *
 * `size`:
 *   - "hero" (default): aspect-video, sirve para cards grandes (Biblioteca).
 *   - "thumb": cuadrado pequeño (Dashboard, mini-listings).
 */

const SIZES = {
  hero: {
    container: 'aspect-video rounded-lg',
    logoPadding: 'p-6',
    siglaText: 'text-5xl font-bold tracking-tight',
    fallbackText: 'text-4xl font-bold tracking-tight',
  },
  thumb: {
    container: 'w-16 h-16 rounded-xl',
    logoPadding: 'p-2',
    siglaText: 'text-sm font-bold tracking-tight',
    fallbackText: 'text-xl font-bold',
  },
};

const CourseCover = ({ course, size = 'hero', className = '' }) => {
  const cfg = SIZES[size] || SIZES.hero;
  const university = course?.university;
  const hasLogo = !!university?.logo_url;
  const hasSigla = university?.short_name && university.short_name !== 'GEN';

  if (hasLogo) {
    return (
      <div className={`${cfg.container} relative overflow-hidden bg-white border border-border ${className}`}>
        <div className={`absolute inset-0 flex items-center justify-center ${cfg.logoPadding}`}>
          <img
            src={university.logo_url}
            alt={university.short_name || university.name || ''}
            className="max-h-full max-w-full object-contain"
          />
        </div>
      </div>
    );
  }

  return (
    <div className={`${cfg.container} relative overflow-hidden bg-gradient-to-br from-cyan-400 via-cyan-500 to-blue-600 ${className}`}>
      {/* Decorative gloss */}
      <div className="absolute inset-0 bg-gradient-to-tr from-white/0 via-white/10 to-white/20 pointer-events-none" aria-hidden="true" />
      <div className="absolute inset-0 flex items-center justify-center">
        <span className={`text-white ${hasSigla ? cfg.siglaText : cfg.fallbackText} relative z-10`}>
          {hasSigla ? university.short_name : (course?.title || '').charAt(0)}
        </span>
      </div>
    </div>
  );
};

export default CourseCover;
