/**
 * Auth Callback Handler for Google OAuth
 * Processes session_id from Emergent Auth redirect
 */
import { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { toast } from 'sonner';

const AuthCallback = () => {
  const navigate = useNavigate();
  const { processGoogleCallback } = useAuth();
  const hasProcessed = useRef(false);

  useEffect(() => {
    // Use useRef to prevent double processing in StrictMode
    if (hasProcessed.current) return;
    hasProcessed.current = true;

    const processCallback = async () => {
      // Extract session_id from URL hash
      const hash = window.location.hash;
      const params = new URLSearchParams(hash.replace('#', ''));
      const sessionId = params.get('session_id');

      if (!sessionId) {
        toast.error('Error de autenticación: No se recibió session_id');
        navigate('/auth');
        return;
      }

      try {
        const result = await processGoogleCallback(sessionId);
        
        if (result.success) {
          toast.success('¡Bienvenido!');
          // Navigate to dashboard
          navigate('/dashboard', { 
            state: { user: result.user },
            replace: true 
          });
        } else {
          toast.error(result.error || 'Error de autenticación');
          navigate('/auth');
        }
      } catch (error) {
        console.error('Auth callback error:', error);
        toast.error('Error al procesar la autenticación');
        navigate('/auth');
      }
    };

    processCallback();
  }, [processGoogleCallback, navigate]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-cyan-900 flex items-center justify-center">
      <div className="text-center">
        <img 
          src="/remy-logo.png" 
          alt="Remy" 
          className="w-24 h-24 mx-auto mb-6 animate-pulse"
        />
        <div className="animate-spin w-8 h-8 border-4 border-cyan-500 border-t-transparent rounded-full mx-auto mb-4" />
        <p className="text-white text-lg">Autenticando...</p>
      </div>
    </div>
  );
};

export default AuthCallback;
