/**
 * Boot de Capacitor para Remy.
 *
 * Se ejecuta UNA vez al cargar el bundle. Detecta plataforma; si es nativa
 * (Android/iOS), inicializa los plugins de status bar y splash screen y
 * registra handlers de hardware-back. En web es no-op.
 *
 * Importado desde index.js antes de renderizar React, así el splash native
 * se oculta apenas el bundle JS está listo (en lugar de quedar con el splash
 * visible 3-4 segundos extras mientras Babel evalúa).
 */
import { Capacitor } from '@capacitor/core';
import { App as CapApp } from '@capacitor/app';
import { StatusBar, Style } from '@capacitor/status-bar';
import { SplashScreen } from '@capacitor/splash-screen';

let booted = false;

export async function bootCapacitor() {
  if (booted) return;
  booted = true;

  if (!Capacitor.isNativePlatform()) return;

  // Status bar: estilo dark sobre fondo oscuro de la app.
  // Falla silenciosamente en plataformas que no soportan el plugin.
  try {
    await StatusBar.setStyle({ style: Style.Dark });
    await StatusBar.setBackgroundColor({ color: '#0c0c0d' });
  } catch (e) {
    // No-op: algunos devices o configs sin SystemUI no soportan setStyle.
  }

  // Splash: hideomos en cuanto JS está listo (el splash queda visible
  // mientras Capacitor monta + Babel evalúa el bundle ~1-2s en cold start).
  try {
    await SplashScreen.hide({ fadeOutDuration: 300 });
  } catch (e) {
    // No-op.
  }

  // Hardware back: en Android, si estamos en la raíz, minimizar la app
  // en vez de cerrarla. Si estamos en una vista interior, dejar que
  // react-router maneje el back.
  CapApp.addListener('backButton', ({ canGoBack }) => {
    if (canGoBack) {
      window.history.back();
    } else {
      // Minimizar (no exit), comportamiento estándar Android.
      CapApp.minimizeApp().catch(() => {
        // Si minimizar falla (raro), no salimos: el usuario puede usar el
        // botón home del sistema.
      });
    }
  });
}
