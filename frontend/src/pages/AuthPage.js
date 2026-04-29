/**
 * Authentication Page for Remy Platform
 * Google Identity Services (popup-based, no redirect).
 */
import { useEffect } from 'react';
import { useNavigate, Link, useSearchParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { GoogleLogin } from '@react-oauth/google';
import { toast } from 'sonner';
import { useAuth } from '../contexts/AuthContext';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import {
  ArrowLeft, Loader2, BookOpen, Target, BarChart3, ShieldCheck
} from 'lucide-react';

const fadeUp = (i = 0) => ({
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.5, delay: i * 0.06, ease: [0.22, 1, 0.36, 1] }
});

const VALUE_PROPS = [
  { icon: BookOpen, title: 'Lecciones claras', desc: 'Contenido organizado y al grano para tu ramo.' },
  { icon: Target, title: 'Simulacros instantáneos', desc: 'Práctica tipo prueba real cuando lo necesites.' },
  { icon: BarChart3, title: 'Progreso que se ve', desc: 'Notas, lecciones y tendencias en un solo lugar.' }
];

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
      <div
        className="min-h-screen bg-background flex items-center justify-center"
        role="status"
        aria-live="polite"
      >
        <Loader2 className="w-8 h-8 text-primary animate-spin" />
        <span className="sr-only">Cargando</span>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background relative overflow-hidden">
      {/* Ambient decoration (visible mainly in dark mode) */}
      <div
        className="absolute inset-0 pointer-events-none opacity-60 dark:opacity-100"
        aria-hidden="true"
      >
        <div className="absolute top-0 -left-40 w-[600px] h-[600px] bg-primary/12 dark:bg-primary/15 rounded-full blur-[140px]" />
        <div className="absolute bottom-0 -right-40 w-[500px] h-[500px] bg-blue-500/10 dark:bg-blue-500/15 rounded-full blur-[140px]" />
      </div>

      <Link
        to="/"
        className="absolute top-5 left-5 md:top-6 md:left-6 z-20 inline-flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors px-2 py-1.5 rounded-md focus:outline-none focus-visible:ring-2 focus-visible:ring-primary"
      >
        <ArrowLeft size={18} aria-hidden="true" />
        <span className="text-sm md:text-base">Volver al inicio</span>
      </Link>

      <div className="relative z-10 min-h-screen flex items-center justify-center px-4 py-16 md:py-20">
        <div className="w-full max-w-5xl grid lg:grid-cols-2 gap-10 lg:gap-16 items-center">
          {/* Left — value props (hidden on mobile) */}
          <motion.div {...fadeUp(0)} className="hidden lg:block">
            <div className="flex items-center gap-3 mb-6">
              <img src="/remy-logo.png" alt="" className="w-12 h-12 object-contain" />
              <div>
                <h2 className="text-2xl font-bold text-foreground tracking-tight">Remy</h2>
                <p className="text-xs text-muted-foreground">by Se Remonta</p>
              </div>
            </div>

            <h1 className="text-3xl xl:text-4xl font-bold text-foreground tracking-tight leading-tight mb-4">
              Tu plataforma de estudio para la <span className="text-primary">universidad</span>.
            </h1>
            <p className="text-base xl:text-lg text-muted-foreground mb-10 leading-relaxed">
              Lecciones, simulacros y progreso. Todo lo que necesitas para aprobar tus ramos en un solo
              lugar.
            </p>

            <ul className="space-y-5">
              {VALUE_PROPS.map((prop, idx) => {
                const Icon = prop.icon;
                return (
                  <motion.li key={idx} {...fadeUp(idx + 1)} className="flex items-start gap-4">
                    <div
                      className="flex-shrink-0 w-10 h-10 rounded-xl bg-primary/15 ring-1 ring-primary/30 flex items-center justify-center text-primary"
                      aria-hidden="true"
                    >
                      <Icon size={20} />
                    </div>
                    <div>
                      <h3 className="font-semibold text-foreground">{prop.title}</h3>
                      <p className="text-sm text-muted-foreground">{prop.desc}</p>
                    </div>
                  </motion.li>
                );
              })}
            </ul>

            <div className="mt-10 flex items-center gap-2 text-xs text-muted-foreground">
              <ShieldCheck size={14} className="text-emerald-500 dark:text-emerald-400" aria-hidden="true" />
              <span>Inicio seguro con tu cuenta de Google</span>
            </div>
          </motion.div>

          {/* Right — sign-in card */}
          <motion.div {...fadeUp(1)} className="w-full">
            <Card className="w-full max-w-md mx-auto bg-card border-border shadow-xl">
              <CardHeader className="text-center space-y-3 pt-8">
                <img
                  src="/remy-logo.png"
                  alt=""
                  className="w-14 h-14 md:w-16 md:h-16 mx-auto lg:hidden"
                />
                <div className="space-y-1.5">
                  <CardTitle className="text-2xl text-foreground tracking-tight">
                    Bienvenido a Remy
                  </CardTitle>
                  <CardDescription className="text-muted-foreground">
                    Tu plataforma de estudio inteligente
                  </CardDescription>
                </div>
              </CardHeader>

              <CardContent className="space-y-6 pb-8">
                <div className="flex justify-center" data-testid="google-login-btn">
                  <GoogleLogin
                    onSuccess={handleSuccess}
                    onError={handleError}
                    theme="filled_blue"
                    size="large"
                    shape="pill"
                    text="continue_with"
                    locale="es"
                  />
                </div>

                <div className="flex items-center gap-3" aria-hidden="true">
                  <div className="h-px bg-border flex-1" />
                  <span className="text-xs text-muted-foreground uppercase tracking-wider">
                    Continúa con Google
                  </span>
                  <div className="h-px bg-border flex-1" />
                </div>

                <p className="text-center text-xs text-muted-foreground leading-relaxed">
                  Al continuar, aceptas nuestros{' '}
                  <a href="#" className="text-primary hover:underline font-medium">
                    términos de servicio
                  </a>{' '}
                  y{' '}
                  <a href="#" className="text-primary hover:underline font-medium">
                    política de privacidad
                  </a>
                  .
                </p>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default AuthPage;
