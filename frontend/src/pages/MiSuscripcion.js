/**
 * Mi Suscripción - User Subscription Management Page
 * Beautiful redesigned version with modern UI
 */
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';
import { 
  Crown, Calendar, CreditCard, Clock, AlertTriangle,
  CheckCircle, XCircle, Loader2, ArrowLeft, RefreshCw,
  Shield, Zap, Sparkles, Star, Gift, ChevronRight
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const MiSuscripcion = () => {
  const navigate = useNavigate();
  const { user, refreshUser, hasActiveSubscription } = useAuth();
  const [subscription, setSubscription] = useState(null);
  const [loading, setLoading] = useState(true);
  const [cancelling, setCancelling] = useState(false);

  useEffect(() => {
    fetchSubscription();
  }, []);

  const fetchSubscription = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/payments/subscription`, {
        withCredentials: true
      });
      setSubscription(response.data);
    } catch (error) {
      console.error('Error fetching subscription:', error);
      if (error.response?.status === 401) {
        navigate('/auth');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCancelSubscription = async () => {
    setCancelling(true);
    try {
      const response = await axios.post(`${API}/payments/cancel`, {}, {
        withCredentials: true
      });
      
      toast.success(response.data.message || 'Suscripción cancelada');
      await refreshUser();
      await fetchSubscription();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Error al cancelar la suscripción');
    } finally {
      setCancelling(false);
    }
  };

  const calculateDaysRemaining = () => {
    if (!subscription?.subscription_end) return 0;
    const endDate = new Date(subscription.subscription_end);
    const now = new Date();
    const diffTime = endDate - now;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return Math.max(0, diffDays);
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return '-';
    return new Date(dateStr).toLocaleDateString('es-CL', {
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    });
  };

  const getPlanDetails = (plan) => {
    const plans = {
      'monthly': { name: 'Plan Mensual', price: '$9.990', period: 'mes', color: 'from-cyan-500 to-blue-600' },
      'semestral': { name: 'Plan Semestral', price: '$29.990', period: '6 meses', color: 'from-purple-500 to-pink-600' }
    };
    return plans[plan] || { name: 'Plan', price: '-', period: '', color: 'from-slate-500 to-slate-600' };
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="animate-spin text-cyan-500" size={32} />
      </div>
    );
  }

  const isActive = subscription?.subscription_status === 'active';
  const daysRemaining = calculateDaysRemaining();
  const planDetails = getPlanDetails(subscription?.subscription_plan);

  // ==================== NO SUBSCRIPTION VIEW ====================
  if (!isActive) {
    return (
      <div className="max-w-4xl mx-auto space-y-8 pb-24 lg:pb-8" data-testid="mi-suscripcion-page">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">Mi Suscripción</h1>
            <p className="text-slate-500 mt-1">Gestiona tu plan de Remy</p>
          </div>
          <Button variant="ghost" onClick={() => navigate('/biblioteca')}>
            <ArrowLeft size={18} className="mr-2" />
            Volver
          </Button>
        </div>

        {/* No Subscription Card */}
        <Card className="overflow-hidden border-0 shadow-xl">
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 p-8 text-white text-center">
            <div className="w-20 h-20 bg-white/10 rounded-full mx-auto mb-6 flex items-center justify-center">
              <Crown size={40} className="text-cyan-400" />
            </div>
            <h2 className="text-2xl font-bold mb-2">Sin suscripción activa</h2>
            <p className="text-slate-300 max-w-md mx-auto">
              Desbloquea todo el potencial de Remy con una suscripción premium
            </p>
          </div>
          
          <CardContent className="p-8">
            {/* Benefits Grid */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
              {[
                { icon: Sparkles, label: 'Cursos ilimitados', color: 'text-cyan-500' },
                { icon: ClipboardCheck, label: 'Simulacros', color: 'text-purple-500' },
                { icon: TrendingUp, label: 'Progreso', color: 'text-green-500' },
                { icon: Zap, label: 'Soporte 24/7', color: 'text-yellow-500' }
              ].map((item, idx) => (
                <div key={idx} className="text-center p-4 rounded-xl bg-slate-50">
                  <item.icon className={`mx-auto mb-2 ${item.color}`} size={24} />
                  <p className="text-sm font-medium text-slate-700">{item.label}</p>
                </div>
              ))}
            </div>

            {/* Plans */}
            <div className="grid md:grid-cols-2 gap-4 mb-8">
              {/* Monthly */}
              <div 
                className="relative p-6 rounded-2xl border-2 border-slate-200 hover:border-cyan-300 cursor-pointer transition-all hover:shadow-lg"
                onClick={() => navigate('/subscribe?plan=monthly')}
              >
                <h3 className="font-bold text-lg mb-1">Plan Mensual</h3>
                <p className="text-3xl font-bold text-slate-900 mb-2">
                  $9.990 <span className="text-sm font-normal text-slate-500">CLP/mes</span>
                </p>
                <p className="text-sm text-slate-500">Flexibilidad total, cancela cuando quieras</p>
                <ChevronRight className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-300" size={24} />
              </div>

              {/* Semestral */}
              <div 
                className="relative p-6 rounded-2xl border-2 border-cyan-500 bg-gradient-to-br from-cyan-50 to-blue-50 cursor-pointer transition-all hover:shadow-lg"
                onClick={() => navigate('/subscribe?plan=semestral')}
              >
                <div className="absolute -top-3 right-4 bg-gradient-to-r from-cyan-500 to-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full">
                  AHORRA 50%
                </div>
                <h3 className="font-bold text-lg mb-1">Plan Semestral</h3>
                <p className="text-3xl font-bold text-slate-900 mb-2">
                  $29.990 <span className="text-sm font-normal text-slate-500">CLP/6 meses</span>
                </p>
                <p className="text-sm text-slate-500">El mejor valor para tu aprendizaje</p>
                <ChevronRight className="absolute right-4 top-1/2 -translate-y-1/2 text-cyan-500" size={24} />
              </div>
            </div>

            <Button 
              size="lg"
              className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white py-6 text-lg rounded-xl shadow-lg"
              onClick={() => navigate('/subscribe')}
            >
              <Crown className="mr-2" size={20} />
              Comenzar mi suscripción
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  // ==================== ACTIVE SUBSCRIPTION VIEW ====================
  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-24 lg:pb-8" data-testid="mi-suscripcion-page">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Mi Suscripción</h1>
          <p className="text-slate-500 mt-1">Gestiona tu plan de Remy</p>
        </div>
        <Button variant="ghost" onClick={() => navigate('/biblioteca')}>
          <ArrowLeft size={18} className="mr-2" />
          Volver
        </Button>
      </div>

      {/* Main Subscription Card */}
      <Card className="overflow-hidden border-0 shadow-xl">
        <div className={`bg-gradient-to-r ${planDetails.color} p-8 text-white relative overflow-hidden`}>
          {/* Background decoration */}
          <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/2" />
          <div className="absolute bottom-0 left-0 w-32 h-32 bg-white/10 rounded-full translate-y-1/2 -translate-x-1/2" />
          
          <div className="relative z-10">
            <div className="flex items-start justify-between mb-6">
              <div>
                <Badge className="bg-white/20 text-white mb-3 px-3 py-1">
                  <Star size={12} className="mr-1" fill="currentColor" />
                  PREMIUM ACTIVO
                </Badge>
                <h2 className="text-3xl font-bold mb-1">{planDetails.name}</h2>
                <p className="text-white/80">{planDetails.price} CLP/{planDetails.period}</p>
              </div>
              <div className="text-right">
                <div className="text-5xl font-bold">{daysRemaining}</div>
                <div className="text-white/80 text-sm">días restantes</div>
              </div>
            </div>

            {/* Progress bar */}
            <div className="bg-white/20 rounded-full h-2 overflow-hidden">
              <div 
                className="bg-white h-full rounded-full transition-all duration-500"
                style={{ width: `${Math.max(5, (daysRemaining / (subscription?.subscription_plan === 'monthly' ? 30 : 180)) * 100)}%` }}
              />
            </div>
            <p className="text-white/70 text-sm mt-2">
              Se renueva el {formatDate(subscription?.subscription_end)}
            </p>
          </div>
        </div>

        <CardContent className="p-6 space-y-6">
          {/* Info Grid */}
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center p-4 bg-slate-50 rounded-xl">
              <Calendar className="mx-auto mb-2 text-slate-400" size={20} />
              <p className="text-xs text-slate-500 mb-1">Inicio</p>
              <p className="font-semibold text-sm text-slate-900">
                {formatDate(user?.subscription_start || subscription?.subscription_details?.start_date)}
              </p>
            </div>
            <div className="text-center p-4 bg-slate-50 rounded-xl">
              <RefreshCw className="mx-auto mb-2 text-slate-400" size={20} />
              <p className="text-xs text-slate-500 mb-1">Próximo cobro</p>
              <p className="font-semibold text-sm text-slate-900">
                {formatDate(subscription?.subscription_end)}
              </p>
            </div>
            <div className="text-center p-4 bg-slate-50 rounded-xl">
              <CreditCard className="mx-auto mb-2 text-slate-400" size={20} />
              <p className="text-xs text-slate-500 mb-1">Tipo</p>
              <p className="font-semibold text-sm text-slate-900 capitalize">
                {subscription?.subscription_type === 'mercadopago' ? 'Mercado Pago' : 'Manual'}
              </p>
            </div>
          </div>

          {/* Auto renewal notice */}
          {subscription?.subscription_type === 'mercadopago' && (
            <div className="flex items-start gap-4 p-4 bg-blue-50 rounded-xl border border-blue-100">
              <div className="bg-blue-100 rounded-full p-2">
                <Shield className="text-blue-600" size={20} />
              </div>
              <div>
                <h4 className="font-semibold text-blue-900 mb-1">Renovación automática activa</h4>
                <p className="text-sm text-blue-700">
                  Tu suscripción se renovará automáticamente el {formatDate(subscription?.subscription_end)}. 
                  Se cargará {planDetails.price} CLP a tu tarjeta.
                </p>
              </div>
            </div>
          )}

          {/* Manual access notice */}
          {subscription?.subscription_type === 'manual' && (
            <div className="flex items-start gap-4 p-4 bg-purple-50 rounded-xl border border-purple-100">
              <div className="bg-purple-100 rounded-full p-2">
                <Gift className="text-purple-600" size={20} />
              </div>
              <div>
                <h4 className="font-semibold text-purple-900 mb-1">Acceso cortesía</h4>
                <p className="text-sm text-purple-700">
                  Tu acceso fue otorgado por el administrador y expira el {formatDate(subscription?.subscription_end)}. 
                  No se realizarán cobros automáticos.
                </p>
              </div>
            </div>
          )}

          {/* Benefits */}
          <div>
            <h3 className="font-semibold text-slate-900 mb-4 flex items-center gap-2">
              <Zap className="text-cyan-500" size={18} />
              Incluido en tu plan
            </h3>
            <div className="grid grid-cols-2 gap-3">
              {[
                'Acceso a todos los cursos',
                'Simulacros ilimitados',
                'Seguimiento de progreso',
                'Soporte prioritario',
                ...(subscription?.subscription_plan === 'semestral' ? [
                  'Contenido exclusivo',
                  'Acceso anticipado'
                ] : [])
              ].map((benefit, idx) => (
                <div key={idx} className="flex items-center gap-2 text-sm text-slate-600">
                  <CheckCircle size={16} className="text-green-500 flex-shrink-0" />
                  {benefit}
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Cancel Section - Only for Mercado Pago */}
      {subscription?.subscription_type === 'mercadopago' && (
        <Card className="border-slate-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-slate-900">¿Necesitas cancelar?</h3>
                <p className="text-sm text-slate-500">
                  Mantendrás acceso hasta el {formatDate(subscription?.subscription_end)}
                </p>
              </div>
              <AlertDialog>
                <AlertDialogTrigger asChild>
                  <Button variant="outline" className="text-red-600 border-red-200 hover:bg-red-50">
                    Cancelar suscripción
                  </Button>
                </AlertDialogTrigger>
                <AlertDialogContent>
                  <AlertDialogHeader>
                    <AlertDialogTitle className="flex items-center gap-2">
                      <AlertTriangle className="text-yellow-500" size={24} />
                      ¿Cancelar tu suscripción?
                    </AlertDialogTitle>
                    <AlertDialogDescription className="space-y-3 text-left">
                      <p>Si cancelas:</p>
                      <ul className="list-disc list-inside space-y-1 text-sm">
                        <li>No se realizarán más cobros</li>
                        <li>Mantendrás acceso hasta el {formatDate(subscription?.subscription_end)}</li>
                        <li>Después perderás acceso al contenido</li>
                        <li>Puedes volver a suscribirte cuando quieras</li>
                      </ul>
                    </AlertDialogDescription>
                  </AlertDialogHeader>
                  <AlertDialogFooter>
                    <AlertDialogCancel>Mantener suscripción</AlertDialogCancel>
                    <AlertDialogAction
                      onClick={handleCancelSubscription}
                      disabled={cancelling}
                      className="bg-red-600 hover:bg-red-700"
                    >
                      {cancelling ? 'Cancelando...' : 'Sí, cancelar'}
                    </AlertDialogAction>
                  </AlertDialogFooter>
                </AlertDialogContent>
              </AlertDialog>
            </div>
          </CardContent>
        </Card>
      )}

      {/* FAQ */}
      <Card>
        <CardContent className="p-6">
          <h3 className="font-semibold text-slate-900 mb-4">Preguntas frecuentes</h3>
          <div className="space-y-4 text-sm">
            <div>
              <p className="font-medium text-slate-700">¿Cómo funciona la renovación?</p>
              <p className="text-slate-500">Se cobra automáticamente al final de cada período.</p>
            </div>
            <div>
              <p className="font-medium text-slate-700">¿Puedo cancelar?</p>
              <p className="text-slate-500">Sí, mantendrás acceso hasta el final del período pagado.</p>
            </div>
            <div>
              <p className="font-medium text-slate-700">¿Cómo cambio mi tarjeta?</p>
              <p className="text-slate-500">Cancela y vuelve a suscribirte con la nueva tarjeta.</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

// Missing icons
const ClipboardCheck = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}>
    <rect x="8" y="2" width="8" height="4" rx="1" ry="1"/>
    <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>
    <path d="m9 14 2 2 4-4"/>
  </svg>
);

const TrendingUp = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}>
    <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/>
    <polyline points="16 7 22 7 22 13"/>
  </svg>
);

export default MiSuscripcion;
