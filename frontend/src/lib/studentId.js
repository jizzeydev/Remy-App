/**
 * Canonical student-id resolver.
 *
 * Earlier code generated random `student_TIMESTAMP` IDs in localStorage. That
 * pre-dated authentication and now creates a split-brain bug: writes used the
 * localStorage ID while reads (Progreso, achievements) used the auth user_id,
 * so progress appeared to never accumulate.
 *
 * Going forward, prefer the auth user.user_id whenever available; fall back to
 * the legacy localStorage ID only for unauthenticated flows (which shouldn't
 * happen on the protected student app, but kept as a safety net).
 *
 * Pages should call `getStudentId(user)` with the user from useAuth() — this
 * keeps the resolver in a single place so future migrations stay easy.
 */
export function getStudentId(user) {
  // Authenticated user: use the canonical user_id (or `id` as a fallback).
  if (user) {
    if (user.user_id) return user.user_id;
    if (user.id) return user.id;
  }

  // Legacy localStorage ID — only relevant if somehow we render before auth
  // has resolved. Do NOT generate a new one; if there's nothing here we'd
  // rather return null and let the caller bail than write under a phantom id.
  if (typeof window !== 'undefined') {
    return window.localStorage.getItem('student_id') || null;
  }
  return null;
}
