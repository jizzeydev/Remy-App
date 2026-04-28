/**
 * Mi Suscripción - User Subscription Management Page
 * Theme-token-driven so it adapts to dark / light mode automatically.
 */
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import axios from 'axios';
import {
  Crown, Calendar, CreditCard, AlertTriangle,
  CheckCircle, Loader2, ArrowLeft, RefreshCw,
  Shield, Zap, Sparkles, Star, Gift, ChevronRight,
  ClipboardCheck, TrendingUp, MessageCircle
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { usePricing } from '../hooks/usePricing';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  Accordion, AccordionContent, AccordionItem, AccordionTrigger
} from '@/components/ui/accordion';
import {
  AlertDialog, AlertDialogAction, AlertDialogCancel,
  AlertDialogContent, AlertDialogDescription, AlertDialogFooter,
  AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger
} from '@/components/ui/alert-dialog';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const fadeUp = {
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.4, ease: [0.22, 1, 0.36, 1] }
};

const stagger = (i = 0) => ({
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.4, delay: i * 0.05, ease: [0.22, 1, 0.36, 1] }
});

// Plan visual identity (gradients work on white text in any theme)
const PLAN_VISUALS = {
  monthly: {
    gradient: 'from-cyan-500 via-cyan-600 to-blue-700',
    glow: 'shadow-cyan-500/30'
  },
  semestral: {
    gradient: 'from-violet-500 via-fuchsia-600 to-pink-600',
    glow: 'shadow-fuchsia-500/30'
  },
  fallback: {
    gradient: 'from-slate-600 to-slate-800',
    glow: 'shadow-slate-500/20'
  }
};

const MiSuscripcion = () => {
  const navigate = useNavigate();
  const { user, refreshUser } = useAuth();
  const { monthly, semestral, formatPrice, loading: pricingLoading } = usePricing();
  const [subscription, setSubscription] = useState(null);
  const [loading, setLoading] = useState(true);
  const [cancelling, setCancelling] = useState(false);

  useEffect(() => {
    fetchSubscription();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchSubscription = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('remy_session_token');
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      const response = await axios.get(`${API}/payments/subscription`, { headers });
      setSubscription(response.data);
    } catch (error) {
      console.error('Error fetching subscription:', error);
      if (error.response?.status === 401) navigate('/auth');
    } finally {
      setLoading(false);
    }
  };

  const handleCancelSubscription = async () => {
    setCancelling(true);
    try {
      const token = localStorage.getItem('remy_session_token');
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      const response = await axios.post(`${API}/payments/cancel`, {}, { headers });
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
    const diffDays = Math.ceil((endDate - now) / (1000 * 60 * 60 * 24));
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
    if (plan === 'monthly') return { name: monthly.name, price: formatPrice(monthly.amount), period: monthly.period, visuals: PLAN_VISUALS.monthly };
    if (plan === 'semestral') return { name: semestral.name, price: formatPrice(semestral.amount), period: semestral.period, visuals: PLAN_VISUALS.semestral };
    return { name: 'Plan', price: '-', period: '', visuals: PLAN_VISUALS.fallback };
  };

  if (loading || pricingLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center" role="status" aria-live="polite">
        <Loader2 className="animate-spin text-primary" size={32} />
        <span className="sr-only">Cargando tu suscripción</span>
      </div>
    );
  }

  const isActive = subscription?.subscription_status === 'active';
  const daysRemaining = calculateDaysRemaining();
  const planDetails = getPlanDetails(subscription?.subscription_plan);
  const totalDays = subscription?.subscription_plan === 'monthly' ? 30 : 180;
  const progressPct = Math.max(5, Math.min(100, (daysRemaining / totalDays) * 100));

  // ==================== HEADER (shared) ====================
  const Header = () => (
    <motion.div {...fadeUp} className="flex items-center justify-between gap-4">
      <div>
        <h1 className="text-2xl md:text-3xl font-bold text-foreground tracking-tight">Mi Suscripción</h1>
        <p className="text-sm md:text-base text-muted-foreground mt-1">Gestiona tu plan de Remy</p>
      </div>
      <Button
        variant="ghost"
        onClick={() => navigate('/dashboard')}
        className="text-muted-foreground hover:text-foreground"
      >
        <ArrowLeft size={18} className="mr-2" />
        Volver
      </Button>
    </motion.div>
  );

  // ==================== NO SUBSCRIPTION VIEW ====================
  if (!isActive) {
    const benefits = [
      { icon: Sparkles, label: 'Cursos ilimitados', tone: 'text-cyan-500 dark:text-cyan-400' },
      { icon: ClipboardCheck, label: 'Simulacros', tone: 'text-violet-500 dark:text-violet-400' },
      { icon: TrendingUp, label: 'Progreso', tone: 'text-emerald-500 dark:text-emerald-400' },
      { icon: Zap, label: 'Correcciones', tone: 'text-amber-500 dark:text-amber-400' }
    ];

    return (
      <div className="min-h-screen bg-background py-8 md:py-12 px-4 relative overflow-hidden" data-testid="mi-suscripcion-page">
        {/* Ambient decoration (visible mainly in dark mode) */}
        <div className="absolute inset-0 pointer-events-none opacity-50 dark:opacity-100" aria-hidden="true">
          <div className="absolute top-0 -left-32 w-[500px] h-[500px] bg-primary/8 dark:bg-primary/12 rounded-full blur-[140px]" />
          <div className="absolute bottom-0 -right-32 w-[400px] h-[400px] bg-blue-500/8 dark:bg-blue-500/12 rounded-full blur-[140px]" />
        </div>

        <div className="max-w-4xl mx-auto space-y-6 md:space-y-8 relative z-10">
          <Header />

          {/* Hero card — no subscription */}
        <motion.div {...stagger(1)}>
          <Card className="overflow-hidden border-border bg-card">
            {/* Top accent strip */}
            <div className="relative bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 dark:from-slate-950 dark:via-slate-900 dark:to-slate-950 p-8 md:p-10 text-white text-center overflow-hidden">
              <div className="absolute inset-0 pointer-events-none" aria-hidden="true">
                <div className="absolute -top-20 -right-20 w-64 h-64 bg-cyan-500/20 rounded-full blur-3xl" />
                <div className="absolute -bottom-20 -left-20 w-64 h-64 bg-blue-500/15 rounded-full blur-3xl" />
              </div>
              <div className="relative">
                <div className="w-20 h-20 bg-white/10 ring-1 ring-white/20 rounded-full mx-auto mb-5 flex items-center justify-center backdrop-blur-sm">
                  <Crown size={40} className="text-cyan-300" aria-hidden="true" />
                </div>
                <h2 className="text-2xl md:text-3xl font-bold mb-2 tracking-tight">Sin suscripción activa</h2>
                <p className="text-slate-300 max-w-md mx-auto text-sm md:text-base">
                  Desbloquea todo el potencial de Remy con una suscripción premium.
                </p>
              </div>
            </div>

            <CardContent className="p-6 md:p-8 space-y-8">
              {/* Benefits */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-4">
                {benefits.map((b, idx) => {
                  const Icon = b.icon;
                  return (
                    <motion.div
                      key={idx}
                      {...stagger(idx + 2)}
                      className="text-center p-4 rounded-xl bg-muted border border-border"
                    >
                      <Icon className={`mx-auto mb-2 ${b.tone}`} size={24} aria-hidden="true" />
                      <p className="text-sm font-medium text-foreground">{b.label}</p>
                    </motion.div>
                  );
                })}
              </div>

              {/* Plans */}
              <div className="grid md:grid-cols-2 gap-4">
                {[monthly, semestral].filter(Boolean).map((plan, idx) => {
                  const isPopular = plan.is_popular;
                  const hasDiscount = plan.discount_active && plan.discount_percentage > 0;
                  const monthlyEquivalent = plan.id === 'semestral' ? Math.round(plan.amount / 6) : null;

                  return (
                    <motion.button
                      key={plan.id}
                      type="button"
                      {...stagger(idx + 6)}
                      onClick={() => navigate(`/subscribe?plan=${plan.id}`)}
                      data-testid={`plan-card-${plan.id}`}
                      className={`group relative text-left p-5 md:p-6 rounded-2xl border-2 transition-all hover:shadow-lg focus:outline-none focus-visible:ring-2 focus-visible:ring-primary ${
                        isPopular
                          ? 'border-primary bg-primary/5 hover:bg-primary/10 hover:shadow-primary/20'
                          : 'border-border bg-background hover:border-primary/50'
                      }`}
                    >
                      {hasDiscount && (
                        <div className="absolute -top-3 right-4">
                          <Badge className={`${isPopular ? 'bg-primary text-primary-foreground' : 'bg-red-500 text-white hover:bg-red-500'} border-0 text-xs px-3 py-1 font-bold`}>
                            {isPopular ? `AHORRA ${plan.discount_percentage}%` : `-${plan.discount_percentage}%`}
                          </Badge>
                        </div>
                      )}

                      <h3 className="font-bold text-lg text-foreground mb-2">{plan.name}</h3>

                      <div className="flex items-baseline gap-2 flex-wrap mb-2">
                        {hasDiscount && plan.original_amount && (
                          <span className="text-sm text-muted-foreground line-through">
                            {formatPrice(plan.original_amount)}
                          </span>
                        )}
                        <span className="text-3xl md:text-4xl font-bold text-foreground tracking-tight">
                          {formatPrice(plan.amount)}
                        </span>
                        <span className="text-sm text-muted-foreground">CLP/{plan.period}</span>
                      </div>

                      {monthlyEquivalent && (
                        <p className="text-xs text-primary font-medium mb-2">
                          Equivale a {formatPrice(monthlyEquivalent)} CLP/mes
                        </p>
                      )}

                      <p className="text-sm text-muted-foreground pr-6">
                        {plan.id === 'monthly'
                          ? 'Flexibilidad total, cancela cuando quieras'
                          : 'El mejor valor para tu aprendizaje'}
                      </p>

                      <ChevronRight
                        className="absolute right-4 top-1/2 -translate-y-1/2 text-muted-foreground group-hover:text-primary group-hover:translate-x-0.5 transition-all"
                        size={22}
                        aria-hidden="true"
                      />
                    </motion.button>
                  );
                })}
              </div>

              {/* Primary CTA */}
              <Button
                size="lg"
                className="w-full bg-primary hover:bg-primary/90 text-primary-foreground py-6 text-base md:text-lg rounded-xl shadow-lg shadow-primary/20 font-semibold"
                onClick={() => navigate('/subscribe')}
                data-testid="subscribe-cta"
              >
                <Crown className="mr-2" size={20} />
                Comenzar mi suscripción
              </Button>
            </CardContent>
          </Card>
        </motion.div>
        </div>
      </div>
    );
  }

  // ==================== ACTIVE SUBSCRIPTION VIEW ====================
  return (
    <div className="min-h-screen bg-background py-8 md:py-12 px-4 relative overflow-hidden" data-testid="mi-suscripcion-page">
      {/* Ambient decoration */}
      <div className="absolute inset-0 pointer-events-none opacity-50 dark:opacity-100" aria-hidden="true">
        <div className="absolute top-0 -left-32 w-[500px] h-[500px] bg-primary/8 dark:bg-primary/12 rounded-full blur-[140px]" />
        <div className="absolute bottom-0 -right-32 w-[400px] h-[400px] bg-blue-500/8 dark:bg-blue-500/12 rounded-full blur-[140px]" />
      </div>

      <div className="max-w-4xl mx-auto space-y-6 relative z-10">
        <Header />

      {/* Status hero */}
      <motion.div {...stagger(1)}>
        <Card className={`overflow-hidden border-0 shadow-xl ${planDetails.visuals.glow}`}>
          <div className={`bg-gradient-to-br ${planDetails.visuals.gradient} p-6 md:p-8 text-white relative overflow-hidden`}>
            <div className="absolute inset-0 pointer-events-none" aria-hidden="true">
              <div className="absolute -top-20 -right-20 w-64 h-64 bg-white/10 rounded-full blur-2xl" />
              <div className="absolute -bottom-20 -left-20 w-32 h-32 bg-white/10 rounded-full blur-2xl" />
            </div>

            <div className="relative z-10">
              <div className="flex items-start justify-between gap-4 mb-6 flex-wrap">
                <div className="min-w-0">
                  <Badge className="bg-white/20 text-white hover:bg-white/20 mb-3 px-3 py-1 border-0 backdrop-blur-sm">
                    <Star size={12} className="mr-1" fill="currentColor" aria-hidden="true" />
                    PREMIUM ACTIVO
                  </Badge>
                  <h2 className="text-2xl md:text-3xl font-bold mb-1 tracking-tight">{planDetails.name}</h2>
                  <p className="text-white/80 text-sm md:text-base">
                    {planDetails.price} CLP / {planDetails.period}
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-4xl md:text-5xl font-bold tabular-nums leading-none">{daysRemaining}</div>
                  <div className="text-white/80 text-xs md:text-sm mt-1">días restantes</div>
                </div>
              </div>

              <div
                className="bg-white/20 rounded-full h-2 overflow-hidden"
                role="progressbar"
                aria-label="Tiempo restante de tu suscripción"
                aria-valuenow={daysRemaining}
                aria-valuemin={0}
                aria-valuemax={totalDays}
              >
                <div
                  className="bg-white h-full rounded-full transition-all duration-500"
                  style={{ width: `${progressPct}%` }}
                />
              </div>
              <p className="text-white/80 text-xs md:text-sm mt-3">
                Se renueva el {formatDate(subscription?.subscription_end)}
              </p>
            </div>
          </div>

          <CardContent className="p-6 space-y-6">
            {/* Info grid */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {[
                { icon: Calendar, label: 'Inicio', value: formatDate(user?.subscription_start || subscription?.subscription_details?.start_date) },
                { icon: RefreshCw, label: 'Próximo cobro', value: formatDate(subscription?.subscription_end) },
                { icon: CreditCard, label: 'Tipo', value: subscription?.subscription_type === 'mercadopago' ? 'Mercado Pago' : 'Manual' }
              ].map((item, idx) => {
                const Icon = item.icon;
                return (
                  <motion.div
                    key={idx}
                    {...stagger(idx + 2)}
                    className="text-center p-4 bg-muted border border-border rounded-xl"
                  >
                    <Icon className="mx-auto mb-2 text-muted-foreground" size={20} aria-hidden="true" />
                    <p className="text-xs text-muted-foreground mb-1">{item.label}</p>
                    <p className="font-semibold text-sm text-foreground">{item.value}</p>
                  </motion.div>
                );
              })}
            </div>

            {/* Auto-renewal notice */}
            {subscription?.subscription_type === 'mercadopago' && (
              <motion.div
                {...fadeUp}
                className="flex items-start gap-4 p-4 bg-primary/10 rounded-xl border border-primary/20"
              >
                <div className="bg-primary/20 rounded-full p-2 flex-shrink-0">
                  <Shield className="text-primary" size={20} aria-hidden="true" />
                </div>
                <div className="min-w-0">
                  <h4 className="font-semibold text-foreground mb-1">Renovación automática activa</h4>
                  <p className="text-sm text-muted-foreground">
                    Tu suscripción se renovará automáticamente el {formatDate(subscription?.subscription_end)}.
                    Se cargará {planDetails.price} CLP a tu tarjeta.
                  </p>
                </div>
              </motion.div>
            )}

            {/* Manual access notice */}
            {subscription?.subscription_type === 'manual' && (
              <motion.div
                {...fadeUp}
                className="flex items-start gap-4 p-4 bg-violet-500/10 rounded-xl border border-violet-500/20"
              >
                <div className="bg-violet-500/20 rounded-full p-2 flex-shrink-0">
                  <Gift className="text-violet-500 dark:text-violet-400" size={20} aria-hidden="true" />
                </div>
                <div className="min-w-0">
                  <h4 className="font-semibold text-foreground mb-1">Acceso cortesía</h4>
                  <p className="text-sm text-muted-foreground">
                    Tu acceso fue otorgado por el administrador y expira el {formatDate(subscription?.subscription_end)}.
                    No se realizarán cobros automáticos.
                  </p>
                </div>
              </motion.div>
            )}

            {/* Features */}
            <div>
              <h3 className="font-semibold text-foreground mb-4 flex items-center gap-2">
                <Zap className="text-primary" size={18} aria-hidden="true" />
                Incluido en tu plan
              </h3>
              <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                {(subscription?.subscription_plan === 'semestral' ? semestral.features : monthly.features).map((benefit, idx) => (
                  <li key={idx} className="flex items-start gap-2 text-sm text-foreground">
                    <CheckCircle size={16} className="text-emerald-500 dark:text-emerald-400 flex-shrink-0 mt-0.5" aria-hidden="true" />
                    <span>{benefit}</span>
                  </li>
                ))}
              </ul>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Cancel section — only Mercado Pago */}
      {subscription?.subscription_type === 'mercadopago' && (
        <motion.div {...stagger(2)}>
          <Card className="border-border bg-card">
            <CardContent className="p-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="min-w-0">
                  <h3 className="font-semibold text-foreground">¿Necesitas cancelar?</h3>
                  <p className="text-sm text-muted-foreground mt-0.5">
                    Mantendrás acceso hasta el {formatDate(subscription?.subscription_end)}
                  </p>
                </div>
                <AlertDialog>
                  <AlertDialogTrigger asChild>
                    <Button
                      variant="outline"
                      className="text-destructive border-destructive/30 hover:bg-destructive/10 hover:text-destructive"
                      data-testid="cancel-subscription-btn"
                    >
                      Cancelar suscripción
                    </Button>
                  </AlertDialogTrigger>
                  <AlertDialogContent>
                    <AlertDialogHeader>
                      <AlertDialogTitle className="flex items-center gap-2">
                        <AlertTriangle className="text-amber-500" size={24} aria-hidden="true" />
                        ¿Cancelar tu suscripción?
                      </AlertDialogTitle>
                      <AlertDialogDescription asChild>
                        <div className="space-y-3 text-left">
                          <p>Si cancelas:</p>
                          <ul className="list-disc list-inside space-y-1 text-sm">
                            <li>No se realizarán más cobros</li>
                            <li>Mantendrás acceso hasta el {formatDate(subscription?.subscription_end)}</li>
                            <li>Después perderás acceso al contenido</li>
                            <li>Puedes volver a suscribirte cuando quieras</li>
                          </ul>
                        </div>
                      </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                      <AlertDialogCancel>Mantener suscripción</AlertDialogCancel>
                      <AlertDialogAction
                        onClick={handleCancelSubscription}
                        disabled={cancelling}
                        className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
                      >
                        {cancelling ? (
                          <>
                            <Loader2 size={16} className="mr-2 animate-spin" />
                            Cancelando...
                          </>
                        ) : (
                          'Sí, cancelar'
                        )}
                      </AlertDialogAction>
                    </AlertDialogFooter>
                  </AlertDialogContent>
                </AlertDialog>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}

      {/* FAQ */}
      <motion.div {...stagger(3)}>
        <Card className="border-border bg-card">
          <CardContent className="p-6">
            <h3 className="font-semibold text-foreground mb-4">Preguntas frecuentes</h3>
            <Accordion type="single" collapsible className="w-full">
              {[
                { q: '¿Cómo funciona la renovación?', a: 'Se cobra automáticamente al final de cada período usando la misma tarjeta con la que te suscribiste.' },
                { q: '¿Puedo cancelar?', a: 'Sí. Cancelas con un click y mantendrás acceso hasta el final del período ya pagado. Sin letra chica.' },
                { q: '¿Cómo cambio mi tarjeta?', a: 'Por ahora, cancela tu suscripción actual y vuelve a suscribirte con la nueva tarjeta. Próximamente podrás actualizarla directo desde la cuenta.' },
                { q: '¿Tienen reembolsos?', a: 'Si tuviste un problema dentro de los primeros 7 días, contáctanos por WhatsApp y revisamos tu caso.' }
              ].map((item, idx) => (
                <AccordionItem
                  key={idx}
                  value={`faq-${idx}`}
                  className="border-border last:border-b-0"
                >
                  <AccordionTrigger className="text-left text-sm md:text-base font-medium text-foreground hover:no-underline">
                    {item.q}
                  </AccordionTrigger>
                  <AccordionContent className="text-sm text-muted-foreground leading-relaxed">
                    {item.a}
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </CardContent>
        </Card>
      </motion.div>

      {/* Support card */}
      <motion.div {...stagger(4)}>
        <Card className="border-emerald-500/20 bg-emerald-500/5">
          <CardContent className="p-6">
            <div className="flex flex-col sm:flex-row sm:items-center gap-4">
              <div className="bg-emerald-500 p-3 rounded-full flex-shrink-0">
                <MessageCircle className="text-white" size={24} aria-hidden="true" />
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="font-semibold text-foreground">¿Necesitas ayuda?</h3>
                <p className="text-sm text-muted-foreground">
                  Contacta a soporte por WhatsApp para reembolsos u otras consultas.
                </p>
              </div>
              <a
                href="https://wa.me/56953047119?text=Hola,%20necesito%20ayuda%20con%20mi%20suscripci%C3%B3n%20de%20Remy"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center justify-center gap-2 bg-emerald-500 hover:bg-emerald-600 text-white px-4 py-2.5 rounded-lg font-medium transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400 focus-visible:ring-offset-2 focus-visible:ring-offset-background"
                data-testid="whatsapp-support-link"
              >
                Contactar
              </a>
            </div>
          </CardContent>
        </Card>
      </motion.div>
      </div>
    </div>
  );
};

export default MiSuscripcion;
