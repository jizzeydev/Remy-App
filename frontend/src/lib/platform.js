/**
 * Detección de plataforma de runtime para el shell de la app.
 *
 * `isNative` → corremos dentro de Capacitor (Android/iOS).
 * `isAndroid` / `isIOS` → plataforma específica.
 * `isWeb` → browser regular (Chrome desktop, Safari mobile, etc.).
 *
 * Por qué importa:
 * - Los stores (Apple, Google) prohíben mostrar botones de pago externos
 *   dentro de la app cuando la suscripción es digital. Hay que esconder
 *   las CTAs de "Suscribirse" o reemplazarlas por el flujo IAP nativo
 *   (Google Play Billing / StoreKit) — que vamos a integrar en F2.
 * - Mientras tanto (F0/F1), los CTAs simplemente desaparecen en mobile y
 *   redirigen a la web cuando el usuario llega a esas vistas.
 *
 * Implementación: Capacitor expone `Capacitor.isNativePlatform()` y
 * `Capacitor.getPlatform()`. Si Capacitor no está cargado (build web puro
 * en Vercel), las funciones devuelven el fallback web.
 */
import { Capacitor } from '@capacitor/core';

export const isNative = () => {
  try {
    return Capacitor?.isNativePlatform?.() ?? false;
  } catch {
    return false;
  }
};

export const getPlatform = () => {
  try {
    return Capacitor?.getPlatform?.() ?? 'web';
  } catch {
    return 'web';
  }
};

export const isAndroid = () => getPlatform() === 'android';
export const isIOS = () => getPlatform() === 'ios';
export const isWeb = () => getPlatform() === 'web';

/**
 * ¿La app puede mostrar CTAs de suscripción externa (Mercado Pago)?
 *
 * Devuelve `true` solo en web. En mobile (mientras no tengamos IAP nativo
 * implementado) devolvemos `false` para evitar:
 *  - Rechazo en review de Play / App Store por ofrecer pagos externos.
 *  - Que el alumno intente pagar desde la app y termine en una WebView
 *    pegada a MP que probablemente no convierte bien.
 *
 * Cuando tengamos Google Play Billing y StoreKit integrados (F2), este
 * helper se reemplaza por uno que devuelve `true` siempre y la UI usa el
 * flow correcto según plataforma.
 */
export const canShowExternalSubscriptionCTA = () => isWeb();
