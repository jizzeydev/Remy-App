/**
 * Authentication Page for Remy Platform
 * Google Identity Services (popup-based, no redirect).
 */
import { useEffect } from 'react';
import { useNavigate, Link, useSearchParams } from 'react-router-dom';
import { GoogleLogin } from '@react-oauth/google';
import { toast } from 'sonner';
import { useAuth } from '../contexts/AuthContext';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowLeft, Loader2 } from 'lucide-react';

const AuthPage = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { loginWithGoogleCredential, isAuthenticated, loading } = useAuth();

  const redirectUrl = searchParams.get('redirect') || '/dashboard';

  useEffect(() => {
    if (!loading && isAuthenticated) {
      navigate(redirectUrl, { replace: true });
    }
  }, [isAuthenticated, loading, navigate, redirectUrl]);

  const handleSuccess = async (credentialResponse) => {
    if (!credentialResponse?.credential) {
      toast.error('No se recibió credencial de Google');
      return;
    }
    const result = await loginWithGoogleCredential(credentialResponse.credential);
    if (result.success) {
      toast.success('¡Bienvenido!');
      navigate(redirectUrl, { replace: true });
    } else {
      toast.error(result.error || 'Error de autenticación');
    }
  };

  const handleError = () => {
    toast.error('No se pudo iniciar sesión con Google');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-cyan-900 flex items-center justify-center">
        <Loader2 className="w-8 h-8 text-cyan-500 animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-cyan-900 flex items-center justify-center p-4">
      <Link
        to="/"
        className="absolute top-6 left-6 text-white/80 hover:text-white flex items-center gap-2 transition-colors"
      >
        <ArrowLeft size={20} />
        <span>Volver al inicio</span>
      </Link>

      <Card className="w-full max-w-md">
        <CardHeader className="text-center space-y-4">
          <img src="/remy-logo.png" alt="Remy" className="w-16 h-16 mx-auto" />
          <div>
            <CardTitle className="text-2xl">Bienvenido a Remy</CardTitle>
            <CardDescription>Tu plataforma de estudio inteligente</CardDescription>
          </div>
        </CardHeader>

        <CardContent className="space-y-6">
          <div className="flex justify-center" data-testid="google-login-btn">
            <GoogleLogin
              onSuccess={handleSuccess}
              onError={handleError}
              useOneTap
              theme="filled_blue"
              size="large"
              shape="pill"
              text="continue_with"
              locale="es"
            />
          </div>

          <p className="text-center text-sm text-slate-500">
            Al continuar, aceptas nuestros{' '}
            <a href="#" className="text-cyan-600 hover:underline">términos de servicio</a>
            {' '}y{' '}
            <a href="#" className="text-cyan-600 hover:underline">política de privacidad</a>.
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

export default AuthPage;
