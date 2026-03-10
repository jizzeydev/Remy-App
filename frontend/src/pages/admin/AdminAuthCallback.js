/**
 * Admin Auth Callback Handler for Google OAuth
 * Processes session_id from Emergent Auth redirect for admin login
 */
import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { toast } from 'sonner';
import { Loader2 } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const AdminAuthCallback = () => {
  const navigate = useNavigate();
  const hasProcessed = useRef(false);
  const [status, setStatus] = useState('processing');
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    // Prevent double processing in StrictMode
    if (hasProcessed.current) return;
    hasProcessed.current = true;

    const processCallback = async () => {
      // Extract session_id from URL hash
      const hash = window.location.hash;
      console.log('Processing admin callback with hash:', hash);
      
      const params = new URLSearchParams(hash.replace('#', ''));
      const sessionId = params.get('session_id');

      if (!sessionId) {
        setStatus('error');
        setErrorMessage('No se recibió session_id');
        toast.error('Error de autenticación: No se recibió session_id');
        setTimeout(() => navigate('/admin/login'), 2000);
        return;
      }

      try {
        console.log('Sending session_id to backend...');
        const response = await axios.post(`${BACKEND_URL}/api/admin/google-login`, {
          session_id: sessionId
        });

        if (response.data.access_token) {
          localStorage.setItem('admin_token', response.data.access_token);
          setStatus('success');
          toast.success('¡Bienvenido, Admin!');
          setTimeout(() => navigate('/admin/dashboard', { replace: true }), 500);
        } else {
          throw new Error('No access token received');
        }
      } catch (error) {
        console.error('Admin auth callback error:', error);
        const message = error.response?.data?.detail || 'Error de autenticación con Google';
        setStatus('error');
        setErrorMessage(message);
        toast.error(message);
        setTimeout(() => navigate('/admin/login'), 2000);
      }
    };

    // Small delay to ensure hash is fully loaded
    setTimeout(processCallback, 100);
  }, [navigate]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
      <div className="text-center p-8 bg-white/10 backdrop-blur-lg rounded-2xl">
        {status === 'processing' && (
          <>
            <Loader2 className="w-12 h-12 text-cyan-500 animate-spin mx-auto mb-4" />
            <p className="text-white text-lg">Verificando acceso de administrador...</p>
          </>
        )}
        
        {status === 'success' && (
          <>
            <div className="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <p className="text-white text-lg">¡Acceso autorizado!</p>
            <p className="text-gray-400 text-sm mt-2">Redirigiendo al panel...</p>
          </>
        )}
        
        {status === 'error' && (
          <>
            <div className="w-12 h-12 bg-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <p className="text-white text-lg">Error de autenticación</p>
            <p className="text-red-400 text-sm mt-2">{errorMessage}</p>
            <p className="text-gray-400 text-sm mt-4">Redirigiendo al login...</p>
          </>
        )}
      </div>
    </div>
  );
};

export default AdminAuthCallback;
