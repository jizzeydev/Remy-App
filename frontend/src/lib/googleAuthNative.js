/**
 * Google Sign-In nativo para Capacitor (Android/iOS).
 *
 * Razón de existir: `@react-oauth/google` carga el script GIS de
 * `accounts.google.com` y requiere que el origin (`https://app.remy.local`
 * dentro del WebView) esté en "Authorized JavaScript origins". Google no
 * permite registrar dominios `.local`, así que el flujo web falla en mobile.
 *
 * El plugin nativo abre Google Sign-In del sistema operativo y devuelve un
 * ID token JWT firmado con `aud = serverClientId`. Como serverClientId es
 * el mismo Web client_id (`REACT_APP_GOOGLE_CLIENT_ID`), el backend valida
 * estos tokens igual que los emitidos por GIS web — sin cambios.
 *
 * Requisitos previos en Google Cloud Console:
 *   1. Crear un "OAuth client ID" tipo Android con package
 *      `cl.seremonta.remy` y SHA-1 del keystore (debug y release).
 *   2. El Web client_id se sigue usando como `clientId` (= server side).
 */
import { isNative } from './platform';

let initPromise = null;

const importPlugin = () => import('@codetrix-studio/capacitor-google-auth');

export const initGoogleAuthNative = () => {
  if (!isNative()) return Promise.resolve();
  if (initPromise) return initPromise;

  initPromise = (async () => {
    const { GoogleAuth } = await importPlugin();
    await GoogleAuth.initialize({
      clientId: process.env.REACT_APP_GOOGLE_CLIENT_ID,
      scopes: ['profile', 'email'],
      grantOfflineAccess: false,
    });
  })().catch((err) => {
    initPromise = null;
    throw err;
  });

  return initPromise;
};

export const signInWithGoogleNative = async () => {
  if (!isNative()) {
    throw new Error('signInWithGoogleNative solo debe llamarse en plataformas nativas');
  }
  await initGoogleAuthNative();
  const { GoogleAuth } = await importPlugin();
  const user = await GoogleAuth.signIn();
  return user?.authentication?.idToken || null;
};
