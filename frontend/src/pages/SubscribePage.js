/**
 * Subscription / Checkout Page
 * Theme-token-driven; preserves Mercado Pago SDK integration verbatim.
 */
import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import axios from 'axios';
import {
  Check, CreditCard, Lock, ArrowLeft, Loader2, ShieldCheck, Sparkles
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const fadeUp = {
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.4, ease: [0.22, 1, 0.36, 1] }
};

const formatCLP = (amount) => '$' + new Intl.NumberFormat('es-CL').format(amount);

const SubscribePage = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { user, isAuthenticated, refreshUser } = useAuth();

  const [plans, setPlans] = useState([]);
  const [selectedPlan, setSelectedPlan] = useState(null);
  const [publicKey, setPublicKey] = useState('');
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [mpReady, setMpReady] = useState(false);

  const [cardNumber, setCardNumber] = useState('');
  const [cardExpiry, setCardExpiry] = useState('');
  const [cardCvv, setCardCvv] = useState('');
  const [cardHolder, setCardHolder] = useState('');
  const [docType, setDocType] = useState('RUT');
  const [docNumber, setDocNumber] = useState('');

  const planFromUrl = searchParams.get('plan');

  useEffect(() => {
    const fetchPlans = async () => {
      try {
        const response = await axios.get(`${API}/payments/plans`);
        setPlans(response.data.plans);
        setPublicKey(response.data.mercadopago_public_key);
        const defaultPlan = planFromUrl || 'monthly';
        const plan = response.data.plans.find((p) => p.id === defaultPlan);
        if (plan) setSelectedPlan(plan);
      } catch (error) {
        console.error('Error fetching plans:', error);
        toast.error('Error al cargar los planes');
      } finally {
        setLoading(false);
      }
    };
    fetchPlans();
  }, [planFromUrl]);

  useEffect(() => {
    if (!publicKey) return;
    if (window.MercadoPago) {
      setMpReady(true);
      return;
    }
    const script = document.createElement('script');
    script.src = 'https://sdk.mercadopago.com/js/v2';
    script.async = true;
    script.onload = () => setMpReady(true);
    document.body.appendChild(script);
  }, [publicKey]);

  useEffect(() => {
    if (!isAuthenticated && !loading) {
      navigate('/auth?redirect=/subscribe');
    }
  }, [isAuthenticated, loading, navigate]);

  useEffect(() => {
    if (user?.subscription_status === 'active') {
      toast.info('Ya tienes una suscripción activa');
      navigate('/biblioteca');
    }
  }, [user, navigate]);

  const formatCardNumber = (value) => {
    const v = value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
    const matches = v.match(/\d{4,16}/g);
    const match = (matches && matches[0]) || '';
    const parts = [];
    for (let i = 0, len = match.length; i < len; i += 4) {
      parts.push(match.substring(i, i + 4));
    }
    return parts.length ? parts.join(' ') : value;
  };

  const formatExpiry = (value) => {
    const v = value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
    if (v.length >= 2) return v.substring(0, 2) + '/' + v.substring(2, 4);
    return v;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedPlan || !mpReady || !publicKey) {
      toast.error('Por favor selecciona un plan');
      return;
    }
    if (!cardNumber || !cardExpiry || !cardCvv || !cardHolder || !docNumber) {
      toast.error('Por favor completa todos los campos');
      return;
    }
    setProcessing(true);
    try {
      const mp = new window.MercadoPago(publicKey, { locale: 'es-CL' });
      const [expMonth, expYear] = cardExpiry.split('/');
      const cardData = {
        cardNumber: cardNumber.replace(/\s/g, ''),
        cardholderName: cardHolder,
        cardExpirationMonth: expMonth,
        cardExpirationYear: '20' + expYear,
        securityCode: cardCvv,
        identificationType: docType,
        identificationNumber: docNumber
      };

      let tokenResponse;
      try {
        tokenResponse = await mp.createCardToken(cardData);
      } catch (sdkError) {
        if (Array.isArray(sdkError)) {
          const errorMessages = sdkError.map((err) => err.message || err.cause || JSON.stringify(err));
          throw new Error(errorMessages.join(', '));
        }
        throw new Error(sdkError.message || 'Error al procesar la tarjeta');
      }

      if (Array.isArray(tokenResponse)) {
        const errorMessages = tokenResponse.map((err) => err.message || err.cause || err.description || JSON.stringify(err));
        throw new Error(errorMessages.join(', ') || 'Error en los datos de la tarjeta');
      }
      if (tokenResponse.error) {
        throw new Error(tokenResponse.error.message || tokenResponse.error);
      }
      if (!tokenResponse.id) {
        throw new Error('No se pudo generar el token de la tarjeta');
      }

      const cardToken = tokenResponse.id;
      const sessionToken = localStorage.getItem('remy_session_token');

      const response = await axios.post(
        `${API}/payments/subscribe`,
        { plan_id: selectedPlan.id, card_token: cardToken },
        { headers: sessionToken ? { Authorization: `Bearer ${sessionToken}` } : {} }
      );

      if (response.data.success) {
        toast.success('¡Suscripción activada exitosamente!');
        await refreshUser();
        navigate('/biblioteca?subscription=success');
      } else if (response.data.init_point) {
        window.location.href = response.data.init_point;
      }
    } catch (error) {
      console.error('Payment error:', error);
      let message = 'Error al procesar el pago';
      if (error.response?.data?.detail) {
        message = error.response.data.detail;
      } else if (error.message) {
        const errMsg = error.message.toLowerCase();
        if (errMsg.includes('cardnumber') || errMsg.includes('card number') || errMsg.includes('invalid card')) {
          message = 'Número de tarjeta inválido. Verifica los 16 dígitos.';
        } else if (errMsg.includes('securitycode') || errMsg.includes('cvv') || errMsg.includes('security code')) {
          message = 'CVV inválido. Son los 3 dígitos del reverso.';
        } else if (errMsg.includes('expiration') || errMsg.includes('expire') || errMsg.includes('date')) {
          message = 'Fecha de vencimiento inválida o tarjeta expirada.';
        } else if (errMsg.includes('identification') || errMsg.includes('document')) {
          message = 'RUT inválido. Ingresa sin puntos ni guión.';
        } else if (errMsg.includes('cardholder') || errMsg.includes('name')) {
          message = 'Nombre del titular inválido.';
        } else if (errMsg.includes('parameter') || errMsg.includes('required')) {
          message = 'Completa todos los campos correctamente.';
        } else {
          message = error.message;
        }
      }
      toast.error(message);
    } finally {
      setProcessing(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center" role="status" aria-live="polite">
        <Loader2 className="w-8 h-8 text-primary animate-spin" />
        <span className="sr-only">Cargando planes</span>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background py-10 md:py-14 px-4 relative overflow-hidden">
      {/* Ambient decoration (visible mainly in dark mode) */}
      <div className="absolute inset-0 pointer-events-none opacity-60 dark:opacity-100" aria-hidden="true">
        <div className="absolute top-0 -left-32 w-[500px] h-[500px] bg-primary/10 dark:bg-primary/15 rounded-full blur-[140px]" />
        <div className="absolute top-1/3 -right-32 w-[400px] h-[400px] bg-blue-500/10 dark:bg-blue-500/15 rounded-full blur-[140px]" />
      </div>

      <div className="max-w-5xl mx-auto relative z-10">
        {/* Header */}
        <motion.div {...fadeUp} className="mb-8">
          <button
            onClick={() => navigate(-1)}
            className="text-muted-foreground hover:text-foreground inline-flex items-center gap-2 mb-4 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary rounded-md px-1 py-0.5"
          >
            <ArrowLeft size={20} aria-hidden="true" />
            Volver
          </button>
          <h1 className="text-3xl md:text-4xl font-bold text-foreground tracking-tight">Suscríbete a Remy</h1>
          <p className="text-muted-foreground mt-2 text-base md:text-lg">
            Elige tu plan y comienza a aprender hoy.
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-5 gap-6 lg:gap-8">
          {/* Plan Selection */}
          <motion.div {...fadeUp} className="lg:col-span-2 space-y-3">
            <h2 className="text-lg font-semibold text-foreground mb-2">Selecciona tu plan</h2>

            {plans.map((plan) => {
              const isSelected = selectedPlan?.id === plan.id;
              const monthlyEquivalent = plan.id === 'semestral' ? Math.round(plan.amount / 6) : null;

              return (
                <button
                  key={plan.id}
                  type="button"
                  onClick={() => setSelectedPlan(plan)}
                  data-testid={`plan-card-${plan.id}`}
                  className={`w-full text-left rounded-2xl border-2 p-5 transition-all focus:outline-none focus-visible:ring-2 focus-visible:ring-primary ${
                    isSelected
                      ? 'border-primary bg-primary/5 shadow-lg shadow-primary/10'
                      : 'border-border bg-card hover:border-primary/50'
                  }`}
                >
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 flex-wrap">
                        <h3 className="font-bold text-base md:text-lg text-foreground">{plan.name}</h3>
                        {plan.discount && (
                          <Badge className="bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 hover:bg-emerald-500/15 border border-emerald-500/30 text-xs">
                            {plan.discount} OFF
                          </Badge>
                        )}
                        {plan.is_popular && (
                          <Badge className="bg-primary/15 text-primary hover:bg-primary/15 border border-primary/30 text-xs">
                            <Sparkles size={10} className="mr-1" aria-hidden="true" />
                            POPULAR
                          </Badge>
                        )}
                      </div>
                      <p className="text-muted-foreground text-sm mt-1">{plan.description}</p>

                      <div className="mt-3 flex items-baseline gap-2 flex-wrap">
                        {plan.original_amount && (
                          <span className="text-muted-foreground line-through text-sm">
                            {formatCLP(plan.original_amount)}
                          </span>
                        )}
                        <span className="text-2xl md:text-3xl font-bold text-foreground tracking-tight">
                          {formatCLP(plan.amount)}
                        </span>
                        <span className="text-muted-foreground text-sm">
                          {plan.currency}/{plan.frequency}
                        </span>
                      </div>

                      {monthlyEquivalent && (
                        <p className="text-xs text-primary font-medium mt-1">
                          Equivale a {formatCLP(monthlyEquivalent)} CLP/mes
                        </p>
                      )}

                      <ul className="mt-3 space-y-1.5">
                        {plan.features.slice(0, 3).map((feature, idx) => (
                          <li key={idx} className="flex items-start text-sm text-foreground">
                            <Check
                              size={15}
                              className="text-emerald-500 dark:text-emerald-400 mr-2 mt-0.5 flex-shrink-0"
                              aria-hidden="true"
                            />
                            <span>{feature}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div
                      className={`w-6 h-6 rounded-full border-2 flex items-center justify-center flex-shrink-0 transition-colors ${
                        isSelected ? 'border-primary bg-primary' : 'border-border'
                      }`}
                      aria-hidden="true"
                    >
                      {isSelected && <Check size={14} className="text-primary-foreground" />}
                    </div>
                  </div>
                </button>
              );
            })}

            {/* Trust strip */}
            <div className="flex items-center gap-2 text-xs text-muted-foreground mt-2 pt-3">
              <ShieldCheck size={14} className="text-emerald-500 dark:text-emerald-400" aria-hidden="true" />
              <span>Cancela cuando quieras desde tu cuenta</span>
            </div>
          </motion.div>

          {/* Payment Form */}
          <motion.div {...fadeUp} className="lg:col-span-3">
            <Card className="bg-card border-border shadow-xl">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-foreground">
                  <CreditCard size={20} aria-hidden="true" />
                  Información de pago
                </CardTitle>
                <CardDescription className="text-muted-foreground">
                  Pago seguro procesado por Mercado Pago
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-4" noValidate>
                  <div className="space-y-2">
                    <Label htmlFor="cardNumber">Número de tarjeta</Label>
                    <Input
                      id="cardNumber"
                      inputMode="numeric"
                      autoComplete="cc-number"
                      placeholder="1234 5678 9012 3456"
                      value={cardNumber}
                      onChange={(e) => setCardNumber(formatCardNumber(e.target.value))}
                      maxLength={19}
                      data-testid="card-number-input"
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="cardExpiry">Vencimiento</Label>
                      <Input
                        id="cardExpiry"
                        inputMode="numeric"
                        autoComplete="cc-exp"
                        placeholder="MM/AA"
                        value={cardExpiry}
                        onChange={(e) => setCardExpiry(formatExpiry(e.target.value))}
                        maxLength={5}
                        data-testid="card-expiry-input"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="cardCvv">CVV</Label>
                      <Input
                        id="cardCvv"
                        inputMode="numeric"
                        autoComplete="cc-csc"
                        placeholder="123"
                        type="password"
                        value={cardCvv}
                        onChange={(e) => setCardCvv(e.target.value.replace(/\D/g, '').slice(0, 4))}
                        maxLength={4}
                        data-testid="card-cvv-input"
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="cardHolder">Nombre del titular</Label>
                    <Input
                      id="cardHolder"
                      autoComplete="cc-name"
                      placeholder="Como aparece en la tarjeta"
                      value={cardHolder}
                      onChange={(e) => setCardHolder(e.target.value.toUpperCase())}
                      data-testid="card-holder-input"
                    />
                  </div>

                  <div className="grid grid-cols-3 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="docType">Tipo Doc.</Label>
                      <select
                        id="docType"
                        value={docType}
                        onChange={(e) => setDocType(e.target.value)}
                        className="w-full h-10 px-3 rounded-md border border-input bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-ring"
                        data-testid="doc-type-select"
                      >
                        <option value="RUT">RUT</option>
                        <option value="DNI">DNI</option>
                        <option value="CI">CI</option>
                      </select>
                    </div>
                    <div className="col-span-2 space-y-2">
                      <Label htmlFor="docNumber">Número de documento</Label>
                      <Input
                        id="docNumber"
                        inputMode="numeric"
                        placeholder="123456789"
                        value={docNumber}
                        onChange={(e) => setDocNumber(e.target.value.replace(/[.-]/g, ''))}
                        data-testid="doc-number-input"
                        aria-describedby="docNumber-help"
                      />
                      <p id="docNumber-help" className="text-xs text-muted-foreground">
                        Sin puntos ni guión (ej: 123456789)
                      </p>
                    </div>
                  </div>

                  {/* Summary */}
                  {selectedPlan && (
                    <div className="bg-muted border border-border rounded-lg p-4 mt-6">
                      <div className="flex justify-between items-baseline gap-2 flex-wrap">
                        <span className="text-muted-foreground text-sm">Total a pagar:</span>
                        <span className="text-2xl font-bold text-foreground tracking-tight">
                          {formatCLP(selectedPlan.amount)}{' '}
                          <span className="text-sm font-medium text-muted-foreground">
                            {selectedPlan.currency}
                          </span>
                        </span>
                      </div>
                      <p className="text-xs text-muted-foreground mt-2">
                        Se renovará automáticamente cada{' '}
                        {selectedPlan.frequency === 'mensual' ? 'mes' : '6 meses'}.
                      </p>
                    </div>
                  )}

                  <Button
                    type="submit"
                    className="w-full h-12 bg-primary hover:bg-primary/90 text-primary-foreground text-base md:text-lg mt-2 shadow-lg shadow-primary/20 font-semibold"
                    disabled={processing || !mpReady || !selectedPlan}
                    data-testid="subscribe-submit-btn"
                  >
                    {processing ? (
                      <>
                        <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                        Procesando...
                      </>
                    ) : (
                      <>
                        <Lock className="mr-2 h-5 w-5" />
                        Suscribirme ahora
                      </>
                    )}
                  </Button>

                  <div className="flex items-center justify-center gap-2 text-xs text-muted-foreground mt-3">
                    <Lock size={12} aria-hidden="true" />
                    <span>Pago seguro procesado por Mercado Pago</span>
                  </div>
                </form>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default SubscribePage;
