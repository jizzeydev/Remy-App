/**
 * Auth Callback Handler for Google OAuth
 * Processes session_id from Emergent Auth redirect
 * Optimized for mobile (iOS Safari compatibility)
 */
import { useEffect, useRef, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { toast } from 'sonner';

const AuthCallback = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { processGoogleCallback } = useAuth();
  const hasProcessed = useRef(false);
  const [status, setStatus] = useState('processing');
  const [errorMsg, setErrorMsg] = useState('');

  useEffect(() => {
    // Prevent double processing in StrictMode
    if (hasProcessed.current) return;
    hasProcessed.current = true;

    const processCallback = async () => {
      // Try multiple ways to get session_id (for iOS compatibility)
      let sessionId = null;
      
      // Method 1: From hash
      const hash = window.location.hash;
      if (hash) {
        const params = new URLSearchParams(hash.replace('#', ''));
        sessionId = params.get('session_id');
      }
      
      // Method 2: From search params (some redirects use this)
      if (!sessionId) {
        const searchParams = new URLSearchParams(window.location.search);
        sessionId = searchParams.get('session_id');
      }
      
      // Method 3: From location state (if passed via navigate)
      if (!sessionId && location.state?.session_id) {
        sessionId = location.state.session_id;
      }

      console.log('Auth callback - session_id found:', !!sessionId);

      if (!sessionId) {
        setStatus('error');
        setErrorMsg('No se recibió código de autenticación');
        toast.error('Error de autenticación: Intenta de nuevo');
        setTimeout(() => navigate('/auth'), 2000);
        return;
      }

      try {
        console.log('Processing Google callback...');
        const result = await processGoogleCallback(sessionId);
        
        if (result.success) {
          setStatus('success');
          toast.success('¡Bienvenido!');
          // Small delay to show success state
          setTimeout(() => {
            navigate('/dashboard', { replace: true });
          }, 500);
        } else {
          console.error('Google callback failed:', result.error);
          setStatus('error');
          setErrorMsg(result.error || 'Error de autenticación');
          toast.error(result.error || 'Error de autenticación');
          setTimeout(() => navigate('/auth'), 2000);
        }
      } catch (error) {
        console.error('Auth callback exception:', error);
        setStatus('error');
        setErrorMsg('Error de conexión. Intenta de nuevo.');
        toast.error('Error de conexión. Intenta de nuevo.');
        setTimeout(() => navigate('/auth'), 2000);
      }
    };

    // Small delay to ensure URL hash is fully loaded (helps on iOS)
    setTimeout(processCallback, 100);
  }, [processGoogleCallback, navigate, location]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-cyan-900 flex items-center justify-center p-4">
      <div className="text-center bg-white/10 backdrop-blur-lg rounded-2xl p-8 max-w-sm w-full">
        {status === 'processing' && (
          <>
            <img 
              src="/remy-logo.png" 
              alt="Remy" 
              className="w-20 h-20 mx-auto mb-6 animate-pulse"
            />
            <div className="animate-spin w-8 h-8 border-4 border-cyan-500 border-t-transparent rounded-full mx-auto mb-4" />
            <p className="text-white text-lg">Autenticando...</p>
            <p className="text-white/60 text-sm mt-2">Esto tomará solo un momento</p>
          </>
        )}
        
        {status === 'success' && (
          <>
            <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <p className="text-white text-lg font-semibold">¡Bienvenido!</p>
            <p className="text-white/60 text-sm mt-2">Redirigiendo...</p>
          </>
        )}
        
        {status === 'error' && (
          <>
            <div className="w-16 h-16 bg-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <p className="text-white text-lg font-semibold">Error</p>
            <p className="text-red-300 text-sm mt-2">{errorMsg}</p>
            <p className="text-white/60 text-sm mt-4">Redirigiendo al login...</p>
          </>
        )}
      </div>
    </div>
  );
};

export default AuthCallback;
