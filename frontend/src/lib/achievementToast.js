/**
 * Helper to show toast notifications when achievements unlock.
 *
 * Backend endpoints (quiz/submit, complete-lesson, enrollments POST) include
 * `newly_unlocked_achievements: [{ id, name, description, icon, category, rarity, color }]`.
 * Components don't need to know the structure — they just pass the array through.
 */
import { toast } from 'sonner';

const RARITY_COPY = {
  common: '¡Logro desbloqueado!',
  rare: '¡Logro raro!',
  epic: '¡Logro épico!',
  legendary: '¡Logro legendario!'
};

export function showAchievementToasts(unlocked) {
  if (!Array.isArray(unlocked) || unlocked.length === 0) return;
  unlocked.forEach((a, i) => {
    setTimeout(() => {
      toast.success(`🏆 ${RARITY_COPY[a.rarity] || '¡Logro!'} — ${a.name}`, {
        description: a.description,
        duration: 5000
      });
    }, i * 700); // Stagger so multi-unlocks don't pile up at once.
  });
}
