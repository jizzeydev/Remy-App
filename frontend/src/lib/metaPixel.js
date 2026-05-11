/**
 * Meta Pixel + Conversions API (dual tracking).
 *
 * Estrategia: cada evento se dispara DOS veces:
 *   1. Browser-side via `window.fbq` (Pixel).
 *   2. Server-side POST a `/api/meta/track` (Conversions API).
 *
 * Ambos comparten el mismo `event_id` para que Meta deduplique. Server-side
 * resiste ad-blockers e iOS ITP, browser-side mejora attribution match
 * cuando hay cookies first-party (_fbp/_fbc).
 *
 * Si REACT_APP_META_PIXEL_ID no está seteado, todo queda como no-op silencioso.
 */
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const PIXEL_ID =
  process.env.REACT_APP_META_PIXEL_ID ||
  (typeof window !== 'undefined' ? window.__REMY_META_PIXEL_ID__ : '');

export const isMetaPixelEnabled = () => !!PIXEL_ID && typeof window !== 'undefined' && !!window.fbq;

const genEventId = () => {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) return crypto.randomUUID();
  return `${Date.now()}-${Math.random().toString(36).slice(2, 10)}`;
};

const readCookie = (name) => {
  if (typeof document === 'undefined') return null;
  const match = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'));
  return match ? decodeURIComponent(match[1]) : null;
};

/**
 * Dispara un evento estándar de Meta (browser + server).
 *
 * @param {string} eventName  Standard event: PageView, Lead, CompleteRegistration,
 *                             StartTrial, InitiateCheckout, Subscribe, Purchase, etc.
 * @param {object} options
 * @param {object} [options.customData]  value/currency/content_ids/etc.
 * @param {object} [options.userData]    email/external_id (sin hashear; el backend hashea).
 * @param {boolean}[options.serverOnly]  Si true, no dispara fbq (usar para eventos que ya
 *                                       reporta el backend de manera autoritativa, p.ej.
 *                                       Purchase via webhook MP).
 */
export const trackMetaEvent = (eventName, options = {}) => {
  if (!PIXEL_ID) return null;
  const { customData = {}, userData = {}, serverOnly = false } = options;
  const eventId = genEventId();

  // 1. Browser pixel.
  if (!serverOnly && typeof window !== 'undefined' && window.fbq) {
    try {
      window.fbq('track', eventName, customData, { eventID: eventId });
    } catch (e) {
      // fbq puede tirar si el script aún no terminó de cargar; no romper UX.
    }
  }

  // 2. Server-side (Conversions API). Fire-and-forget.
  const payload = {
    event_name: eventName,
    event_id: eventId,
    event_source_url: typeof window !== 'undefined' ? window.location.href : null,
    custom_data: customData,
    user_data: {
      email: userData.email || null,
      external_id: userData.external_id || null,
      fbp: readCookie('_fbp'),
      fbc: readCookie('_fbc'),
    },
  };

  // En prod backend ≠ frontend origin → cookies no viajan. Pasamos el bearer
  // para que el backend pueda resolver email desde la sesión si el caller no
  // adjuntó userData.email (mejor match rate en eventos internos como PageView).
  const sessionToken = typeof localStorage !== 'undefined'
    ? localStorage.getItem('remy_session_token')
    : null;
  const headers = sessionToken ? { Authorization: `Bearer ${sessionToken}` } : {};

  axios.post(`${API}/meta/track`, payload, { timeout: 4000, headers }).catch(() => {
    // No bloquear UX por fallos de tracking.
  });

  return eventId;
};

export const trackPageView = () => trackMetaEvent('PageView');
