/**
 * Trial Banner Component
 * Displays trial status, days remaining, and simulations remaining
 */
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Clock, Zap, AlertTriangle, Crown, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';

const TrialBanner = () => {
  const navigate = useNavigate();
  const { 
    user, 
    hasActiveSubscription, 
    hasActiveTrial, 
    getTrialDaysRemaining, 
    getTrialSimulationsRemaining 
  } = useAuth();

  // Don't show if user has active subscription
  if (hasActiveSubscription) {
    return null;
  }

  const isTrialActive = hasActiveTrial();
  const daysRemaining = getTrialDaysRemaining();
  const simulationsRemaining = getTrialSimulationsRemaining();
  const simulationsUsed = user?.trial_simulations_used || 0;
  const simulationsLimit = user?.trial_simulations_limit || 10;
  const simulationsProgress = (simulationsUsed / simulationsLimit) * 100;

  // Trial expired
  if (!isTrialActive && user?.trial_active === false) {
    return (
      <Card className="bg-gradient-to-r from-slate-800 to-slate-900 text-white border-0 shadow-lg overflow-hidden">
        <CardContent className="flex flex-col sm:flex-row items-center justify-between py-6 gap-4 relative">
          <div className="absolute top-0 right-0 w-32 h-32 bg-white/5 rounded-full -translate-y-1/2 translate-x-1/2" />
          <div className="flex items-center gap-4 z-10">
            <div className="bg-red-500/20 rounded-full p-3">
              <AlertTriangle size={24} className="text-red-400" />
            </div>
            <div>
              <h3 className="font-bold text-lg">Tu prueba gratuita terminó</h3>
              <p className="text-slate-300 text-sm">
                Suscríbete para seguir accediendo a los simulacros y contenido premium
              </p>
            </div>
          </div>
          <Button 
            className="bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-semibold px-6 z-10"
            onClick={() => navigate('/subscribe')}
            data-testid="trial-expired-subscribe-btn"
          >
            <Crown size={18} className="mr-2" />
            Suscribirme ahora
          </Button>
        </CardContent>
      </Card>
    );
  }

  // No trial yet (shouldn't happen for new users, but handle edge case)
  if (!isTrialActive && !user?.trial_active) {
    return null;
  }

  // Warning banner when 2 or less days remaining
  if (daysRemaining <= 2) {
    return (
      <Card className="bg-gradient-to-r from-amber-500 to-orange-500 text-white border-0 shadow-lg overflow-hidden">
        <CardContent className="py-5 px-6">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="bg-white/20 rounded-full p-3">
                <AlertTriangle size={24} />
              </div>
              <div>
                <h3 className="font-bold text-lg flex items-center gap-2">
                  Tu prueba gratuita está por terminar
                </h3>
                <p className="text-amber-100 text-sm">
                  Te {daysRemaining === 1 ? 'queda' : 'quedan'} <span className="font-bold">{daysRemaining} {daysRemaining === 1 ? 'día' : 'días'}</span> y <span className="font-bold">{simulationsRemaining} simulacros</span> disponibles
                </p>
              </div>
            </div>
            <Button 
              className="bg-white hover:bg-amber-50 text-amber-600 font-semibold px-6"
              onClick={() => navigate('/subscribe')}
              data-testid="trial-warning-subscribe-btn"
            >
              Suscribirse y no perder acceso
              <ChevronRight size={18} className="ml-1" />
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  // Normal trial banner
  return (
    <Card className="bg-gradient-to-r from-cyan-500 to-blue-600 text-white border-0 shadow-lg overflow-hidden">
      <CardContent className="py-5 px-6">
        <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <div className="bg-white/20 rounded-full p-3">
              <Zap size={24} />
            </div>
            <div>
              <h3 className="font-bold text-lg">
                Estás usando la prueba gratuita de Remy
              </h3>
              <p className="text-cyan-100 text-sm">
                Te quedan <span className="font-bold">{daysRemaining} días</span> de prueba gratuita y <span className="font-bold">{simulationsRemaining} simulacros</span> disponibles
              </p>
            </div>
          </div>
          
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-4 w-full lg:w-auto">
            {/* Simulation progress */}
            <div className="bg-white/10 rounded-xl px-4 py-3 min-w-[180px]">
              <div className="flex items-center justify-between text-xs mb-1.5">
                <span className="text-cyan-100">Simulacros</span>
                <span className="font-medium">{simulationsUsed}/{simulationsLimit}</span>
              </div>
              <Progress 
                value={simulationsProgress} 
                className="h-2 bg-white/20"
              />
            </div>
            
            <Button 
              variant="secondary"
              className="bg-white hover:bg-cyan-50 text-cyan-600 font-semibold px-5"
              onClick={() => navigate('/subscribe')}
              data-testid="trial-subscribe-btn"
            >
              Ver planes
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default TrialBanner;
