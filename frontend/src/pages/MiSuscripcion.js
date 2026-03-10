/**
 * Mi Suscripción - User Subscription Management Page
 * Shows subscription status, days remaining, and allows cancellation
 */
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';
import { 
  Crown, Calendar, CreditCard, Clock, AlertTriangle,
  CheckCircle, XCircle, Loader2, ArrowLeft, RefreshCw,
  Shield, Zap
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
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

  // Calculate days remaining
  const calculateDaysRemaining = () => {
    if (!subscription?.subscription_end) return 0;
    const endDate = new Date(subscription.subscription_end);
    const now = new Date();
    const diffTime = endDate - now;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return Math.max(0, diffDays);
  };

  // Calculate progress percentage (days used / total days)
  const calculateProgress = () => {
    if (!subscription?.subscription_end || !user?.subscription_start) return 0;
    const startDate = new Date(user.subscription_start);
    const endDate = new Date(subscription.subscription_end);
    const now = new Date();
    
    const totalDays = (endDate - startDate) / (1000 * 60 * 60 * 24);
    const usedDays = (now - startDate) / (1000 * 60 * 60 * 24);
    
    return Math.min(100, Math.max(0, (usedDays / totalDays) * 100));
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return '-';
    return new Date(dateStr).toLocaleDateString('es-CL', {
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    });
  };

  const getPlanName = (plan) => {
    const plans = {
      'monthly': 'Plan Mensual',
      'semestral': 'Plan Semestral'
    };
    return plans[plan] || plan;
  };

  const getPlanPrice = (plan) => {
    const prices = {
      'monthly': '$9.990 CLP/mes',
      'semestral': '$29.990 CLP/6 meses'
    };
    return prices[plan] || '-';
  };

  const getStatusBadge = (status) => {
    const badges = {
      'active': { color: 'bg-green-100 text-green-700', icon: CheckCircle, text: 'Activa' },
      'cancelled': { color: 'bg-red-100 text-red-700', icon: XCircle, text: 'Cancelada' },
      'expired': { color: 'bg-orange-100 text-orange-700', icon: Clock, text: 'Expirada' },
      'pending': { color: 'bg-yellow-100 text-yellow-700', icon: Clock, text: 'Pendiente' },
      'inactive': { color: 'bg-slate-100 text-slate-700', icon: XCircle, text: 'Sin suscripción' }
    };
    const badge = badges[status] || badges['inactive'];
    const Icon = badge.icon;
    return (
      <Badge className={`${badge.color} flex items-center gap-1`}>
        <Icon size={14} />
        {badge.text}
      </Badge>
    );
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
  const progress = calculateProgress();

  return (
    <div className="space-y-6 pb-24 lg:pb-8" data-testid="mi-suscripcion-page">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Mi Suscripción</h1>
          <p className="text-slate-600 mt-1">Gestiona tu plan y método de pago</p>
        </div>
        <Button variant="outline" onClick={() => navigate('/biblioteca')}>
          <ArrowLeft size={18} className="mr-2" />
          Volver
        </Button>
      </div>

      {/* Subscription Status Card */}
      <Card className={`border-2 ${isActive ? 'border-green-200 bg-green-50/30' : 'border-slate-200'}`}>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className={`p-3 rounded-full ${isActive ? 'bg-green-100' : 'bg-slate-100'}`}>
                <Crown size={24} className={isActive ? 'text-green-600' : 'text-slate-400'} />
              </div>
              <div>
                <CardTitle className="text-xl">
                  {isActive ? getPlanName(subscription?.subscription_plan) : 'Sin Suscripción Activa'}
                </CardTitle>
                <CardDescription>
                  {isActive ? getPlanPrice(subscription?.subscription_plan) : 'Suscríbete para acceder a todo el contenido'}
                </CardDescription>
              </div>
            </div>
            {getStatusBadge(subscription?.subscription_status)}
          </div>
        </CardHeader>
        
        {isActive && (
          <CardContent className="space-y-6">
            {/* Days Remaining */}
            <div className="bg-white rounded-lg p-4 border">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-slate-600">Tiempo restante</span>
                <span className="font-bold text-lg text-slate-900">{daysRemaining} días</span>
              </div>
              <Progress value={100 - progress} className="h-2" />
              <p className="text-xs text-slate-500 mt-2">
                Tu suscripción se renovará automáticamente el {formatDate(subscription?.subscription_end)}
              </p>
            </div>

            {/* Subscription Details */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-white rounded-lg p-4 border">
                <div className="flex items-center gap-2 text-slate-500 mb-1">
                  <Calendar size={16} />
                  <span className="text-sm">Fecha de inicio</span>
                </div>
                <p className="font-semibold">
                  {formatDate(user?.subscription_start) || formatDate(subscription?.subscription_details?.start_date) || '-'}
                </p>
              </div>
              
              <div className="bg-white rounded-lg p-4 border">
                <div className="flex items-center gap-2 text-slate-500 mb-1">
                  <RefreshCw size={16} />
                  <span className="text-sm">Próxima renovación</span>
                </div>
                <p className="font-semibold">{formatDate(subscription?.subscription_end)}</p>
              </div>
              
              <div className="bg-white rounded-lg p-4 border">
                <div className="flex items-center gap-2 text-slate-500 mb-1">
                  <CreditCard size={16} />
                  <span className="text-sm">Tipo de suscripción</span>
                </div>
                <p className="font-semibold capitalize">
                  {subscription?.subscription_type === 'mercadopago' ? 'Mercado Pago' : 
                   subscription?.subscription_type === 'manual' ? 'Acceso Manual' : '-'}
                </p>
              </div>
            </div>

            {/* Auto-renewal notice */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-start gap-3">
                <Shield className="text-blue-600 flex-shrink-0 mt-0.5" size={20} />
                <div>
                  <h4 className="font-semibold text-blue-900">Renovación automática</h4>
                  <p className="text-sm text-blue-700 mt-1">
                    Tu suscripción se renueva automáticamente cada {subscription?.subscription_plan === 'monthly' ? 'mes' : '6 meses'}. 
                    Se cargará {getPlanPrice(subscription?.subscription_plan)} a tu método de pago el {formatDate(subscription?.subscription_end)}.
                  </p>
                </div>
              </div>
            </div>

            {/* Benefits */}
            <div className="bg-white rounded-lg p-4 border">
              <h4 className="font-semibold mb-3 flex items-center gap-2">
                <Zap size={18} className="text-cyan-500" />
                Beneficios de tu plan
              </h4>
              <ul className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {[
                  'Acceso a todos los cursos',
                  'Simulacros ilimitados',
                  'Seguimiento de progreso',
                  'Soporte prioritario',
                  ...(subscription?.subscription_plan === 'semestral' ? [
                    'Contenido exclusivo',
                    'Acceso anticipado a nuevos cursos'
                  ] : [])
                ].map((benefit, idx) => (
                  <li key={idx} className="flex items-center gap-2 text-sm text-slate-600">
                    <CheckCircle size={16} className="text-green-500 flex-shrink-0" />
                    {benefit}
                  </li>
                ))}
              </ul>
            </div>

            {/* Cancel Subscription - Only for Mercado Pago subscriptions */}
            {subscription?.subscription_type === 'mercadopago' && (
              <div className="border-t pt-6">
                <AlertDialog>
                  <AlertDialogTrigger asChild>
                    <Button variant="outline" className="text-red-600 border-red-200 hover:bg-red-50">
                      <XCircle size={18} className="mr-2" />
                      Cancelar suscripción
                    </Button>
                  </AlertDialogTrigger>
                  <AlertDialogContent>
                    <AlertDialogHeader>
                      <AlertDialogTitle className="flex items-center gap-2">
                        <AlertTriangle className="text-yellow-500" size={24} />
                        ¿Cancelar tu suscripción?
                      </AlertDialogTitle>
                      <AlertDialogDescription className="space-y-3">
                        <p>
                          Si cancelas tu suscripción:
                        </p>
                        <ul className="list-disc list-inside space-y-1 text-sm">
                          <li>No se realizarán más cobros automáticos</li>
                          <li>Mantendrás acceso hasta el {formatDate(subscription?.subscription_end)}</li>
                          <li>Después de esa fecha, perderás acceso al contenido premium</li>
                          <li>Puedes volver a suscribirte en cualquier momento</li>
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
                        {cancelling ? (
                          <>
                            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                            Cancelando...
                          </>
                        ) : (
                          'Sí, cancelar suscripción'
                        )}
                      </AlertDialogAction>
                    </AlertDialogFooter>
                  </AlertDialogContent>
                </AlertDialog>
                
                <p className="text-xs text-slate-500 mt-2">
                  Al cancelar, mantendrás acceso hasta el final de tu período pagado.
                </p>
              </div>
            )}

            {/* Manual subscription notice */}
            {subscription?.subscription_type === 'manual' && (
              <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                <div className="flex items-start gap-3">
                  <Crown className="text-purple-600 flex-shrink-0 mt-0.5" size={20} />
                  <div>
                    <h4 className="font-semibold text-purple-900">Acceso otorgado por el administrador</h4>
                    <p className="text-sm text-purple-700 mt-1">
                      Tu acceso fue otorgado manualmente y expira el {formatDate(subscription?.subscription_end)}. 
                      Contacta al administrador si necesitas extender tu acceso.
                    </p>
                  </div>
                </div>
              </div>
            )}
          </CardContent>
        )}

        {/* No subscription - Show CTA */}
        {!isActive && (
          <CardContent>
            <div className="text-center py-6">
              <p className="text-slate-600 mb-6">
                Obtén acceso ilimitado a todos los cursos, simulacros y más.
              </p>
              <Button 
                size="lg"
                className="bg-cyan-500 hover:bg-cyan-600"
                onClick={() => navigate('/subscribe')}
              >
                <Crown className="mr-2" size={20} />
                Suscribirme ahora
              </Button>
            </div>
          </CardContent>
        )}
      </Card>

      {/* FAQ Section */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Preguntas frecuentes</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <h4 className="font-medium text-slate-900">¿Cómo funciona la renovación automática?</h4>
            <p className="text-sm text-slate-600 mt-1">
              Tu suscripción se renueva automáticamente al final de cada período. Se cargará el monto correspondiente a tu método de pago registrado.
            </p>
          </div>
          <div>
            <h4 className="font-medium text-slate-900">¿Puedo cancelar en cualquier momento?</h4>
            <p className="text-sm text-slate-600 mt-1">
              Sí, puedes cancelar tu suscripción cuando quieras. Mantendrás acceso hasta el final del período que ya pagaste.
            </p>
          </div>
          <div>
            <h4 className="font-medium text-slate-900">¿Qué pasa si cancelo mi suscripción?</h4>
            <p className="text-sm text-slate-600 mt-1">
              No se realizarán más cobros automáticos. Tu acceso continuará hasta la fecha de vencimiento del período actual. Después, puedes volver a suscribirte cuando lo desees.
            </p>
          </div>
          <div>
            <h4 className="font-medium text-slate-900">¿Cómo cambio mi método de pago?</h4>
            <p className="text-sm text-slate-600 mt-1">
              Para cambiar tu método de pago, cancela tu suscripción actual y vuelve a suscribirte con el nuevo método de pago.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default MiSuscripcion;
