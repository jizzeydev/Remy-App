import type { CapacitorConfig } from '@capacitor/cli';

/**
 * Capacitor config para Remy Android.
 *
 * Modelo: la app embebe el bundle de React (frontend/build/) como assets
 * locales — NO carga desde remy.seremonta.store. La API sí apunta a prod
 * (https://api.remy.seremonta.store), configurada vía REACT_APP_BACKEND_URL
 * al hacer `yarn build` antes del `cap sync`.
 *
 * Por qué no usar server.url: cargar desde el host web haría que la app sea
 * un wrapper de WebView puro (lento en cold start, depende de red para todo,
 * Apple/Google lo tratan como "no nativo"). Con assets locales cargamos
 * instant y solo la data viaja por red.
 *
 * androidScheme: 'https' es necesario para que cookies con SameSite=None y
 * los flujos de auth con Google funcionen igual que en web.
 */
const config: CapacitorConfig = {
  appId: 'cl.seremonta.remy',
  appName: 'Remy',
  webDir: 'build',
  android: {
    // 'https' permite que el WebView se identifique como contexto seguro
    // (necesario para cookies SameSite=None que usa nuestro auth).
    allowMixedContent: false,
  },
  server: {
    androidScheme: 'https',
    // hostname interno del WebView; cualquier llamada relativa caerá acá.
    // Las llamadas absolutas a https://api.remy.seremonta.store atraviesan
    // a la red real sin pasar por este host.
    hostname: 'app.remy.local',
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 1500,
      backgroundColor: '#0c0c0d',
      androidSplashResourceName: 'splash',
      androidScaleType: 'CENTER_CROP',
      showSpinner: false,
      splashFullScreen: true,
      splashImmersive: true,
    },
  },
};

export default config;
