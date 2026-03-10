/**
 * Subscription Guard Component
 * Blocks access to content for non-subscribed users
 */
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Crown, Lock, Sparkles, BookOpen, ClipboardCheck, TrendingUp } from 'lucide-react';
import { Button } from '@/components/ui/button';

const SubscriptionRequired = ({ children, feature = "este contenido" }) => {
  const navigate = useNavigate();
  const { user, hasActiveSubscription, isAuthenticated } = useAuth();

  // If user has active subscription, show content
  if (hasActiveSubscription()) {
    return children;
  }

  // Otherwise, show paywall
  return (
    <div className="min-h-[70vh] flex items-center justify-center p-4">
      <div className="max-w-lg w-full text-center">
        {/* Animated lock icon */}
        <div className="relative mb-8">
          <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-blue-500 rounded-full blur-2xl opacity-20 animate-pulse" />
          <div className="relative bg-gradient-to-br from-slate-800 to-slate-900 w-24 h-24 rounded-full mx-auto flex items-center justify-center shadow-2xl">
            <Lock className="text-cyan-400" size={40} />
          </div>
        </div>

        <h2 className="text-2xl font-bold text-slate-900 mb-3">
          Contenido Premium
        </h2>
        
        <p className="text-slate-600 mb-8">
          Necesitas una suscripción activa para acceder a {feature}.
          Desbloquea todo el contenido y mejora tu aprendizaje.
        </p>

        {/* Benefits */}
        <div className="bg-gradient-to-br from-slate-50 to-cyan-50 rounded-2xl p-6 mb-8 text-left">
          <h3 className="font-semibold text-slate-900 mb-4 flex items-center gap-2">
            <Sparkles className="text-cyan-500" size={20} />
            Con tu suscripción obtienes:
          </h3>
          <ul className="space-y-3">
            {[
              { icon: BookOpen, text: "Acceso ilimitado a todos los cursos" },
              { icon: ClipboardCheck, text: "Simulacros de práctica ilimitados" },
              { icon: TrendingUp, text: "Seguimiento detallado de tu progreso" },
              { icon: Crown, text: "Soporte prioritario" }
            ].map((item, idx) => (
              <li key={idx} className="flex items-center gap-3 text-slate-700">
                <div className="bg-cyan-100 rounded-lg p-1.5">
                  <item.icon size={16} className="text-cyan-600" />
                </div>
                {item.text}
              </li>
            ))}
          </ul>
        </div>

        {/* Pricing preview */}
        <div className="flex gap-4 justify-center mb-6">
          <div className="bg-white rounded-xl p-4 shadow-sm border flex-1 max-w-[160px]">
            <p className="text-xs text-slate-500 mb-1">Mensual</p>
            <p className="text-xl font-bold text-slate-900">$9.990</p>
            <p className="text-xs text-slate-400">CLP/mes</p>
          </div>
          <div className="bg-gradient-to-br from-cyan-500 to-blue-600 rounded-xl p-4 shadow-lg flex-1 max-w-[160px] text-white relative overflow-hidden">
            <div className="absolute top-0 right-0 bg-yellow-400 text-yellow-900 text-[10px] font-bold px-2 py-0.5 rounded-bl">
              -50%
            </div>
            <p className="text-xs text-cyan-100 mb-1">Semestral</p>
            <p className="text-xl font-bold">$29.990</p>
            <p className="text-xs text-cyan-200">CLP/6 meses</p>
          </div>
        </div>

        <Button 
          size="lg"
          className="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white px-8 py-6 text-lg rounded-full shadow-lg shadow-cyan-500/30 w-full max-w-xs"
          onClick={() => navigate('/subscribe')}
        >
          <Crown className="mr-2" size={20} />
          Suscribirme ahora
        </Button>

        {!isAuthenticated && (
          <p className="text-sm text-slate-500 mt-4">
            ¿Ya tienes cuenta?{' '}
            <button 
              onClick={() => navigate('/auth')}
              className="text-cyan-600 hover:underline font-medium"
            >
              Inicia sesión
            </button>
          </p>
        )}
      </div>
    </div>
  );
};

export default SubscriptionRequired;
