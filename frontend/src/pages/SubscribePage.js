/**
 * Subscription/Checkout Page
 * Allows users to subscribe to Remy using Mercado Pago
 */
import { useState, useEffect, useCallback } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { 
  Check, Crown, CreditCard, Lock, ArrowLeft, 
  Loader2, AlertCircle, CheckCircle2 
} from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

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
  const [cardForm, setCardForm] = useState(null);
  
  // Card form state
  const [cardNumber, setCardNumber] = useState('');
  const [cardExpiry, setCardExpiry] = useState('');
  const [cardCvv, setCardCvv] = useState('');
  const [cardHolder, setCardHolder] = useState('');
  const [docType, setDocType] = useState('RUT');
  const [docNumber, setDocNumber] = useState('');

  // Get plan from URL if specified
  const planFromUrl = searchParams.get('plan');

  // Fetch plans
  useEffect(() => {
    const fetchPlans = async () => {
      try {
        const response = await axios.get(`${API}/payments/plans`);
        setPlans(response.data.plans);
        setPublicKey(response.data.mercadopago_public_key);
        
        // Pre-select plan from URL or default to monthly
        const defaultPlan = planFromUrl || 'monthly';
        const plan = response.data.plans.find(p => p.id === defaultPlan);
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

  // Load Mercado Pago SDK
  useEffect(() => {
    if (!publicKey) return;
    
    // Check if SDK is already loaded
    if (window.MercadoPago) {
      setMpReady(true);
      return;
    }
    
    // Load SDK script
    const script = document.createElement('script');
    script.src = 'https://sdk.mercadopago.com/js/v2';
    script.async = true;
    script.onload = () => {
      setMpReady(true);
    };
    document.body.appendChild(script);
    
    return () => {
      // Cleanup if needed
    };
  }, [publicKey]);

  // Redirect if not authenticated
  useEffect(() => {
    if (!isAuthenticated && !loading) {
      navigate('/auth?redirect=/subscribe');
    }
  }, [isAuthenticated, loading, navigate]);

  // Check if user already has subscription
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
    if (v.length >= 2) {
      return v.substring(0, 2) + '/' + v.substring(2, 4);
    }
    return v;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedPlan || !mpReady || !publicKey) {
      toast.error('Por favor selecciona un plan');
      return;
    }
    
    // Validate fields
    if (!cardNumber || !cardExpiry || !cardCvv || !cardHolder || !docNumber) {
      toast.error('Por favor completa todos los campos');
      return;
    }
    
    setProcessing(true);
    
    try {
      // Initialize Mercado Pago
      const mp = new window.MercadoPago(publicKey, {
        locale: 'es-CL'
      });
      
      // Parse expiry
      const [expMonth, expYear] = cardExpiry.split('/');
      
      // Create card token
      const cardData = {
        cardNumber: cardNumber.replace(/\s/g, ''),
        cardholderName: cardHolder,
        cardExpirationMonth: expMonth,
        cardExpirationYear: '20' + expYear,
        securityCode: cardCvv,
        identificationType: docType,
        identificationNumber: docNumber
      };
      
      console.log('Creating card token with data:', { ...cardData, securityCode: '***' });
      
      let tokenResponse;
      try {
        tokenResponse = await mp.createCardToken(cardData);
        console.log('Token response:', tokenResponse);
      } catch (sdkError) {
        console.error('SDK createCardToken error:', sdkError);
        // Handle array of errors from MP SDK
        if (Array.isArray(sdkError)) {
          const errorMessages = sdkError.map(e => {
            if (e.message) return e.message;
            if (e.cause) return e.cause;
            return JSON.stringify(e);
          });
          throw new Error(errorMessages.join(', '));
        }
        throw new Error(sdkError.message || 'Error al procesar la tarjeta');
      }
      
      // Check if response is an array (error case)
      if (Array.isArray(tokenResponse)) {
        console.error('Token response is array (error):', tokenResponse);
        const errorMessages = tokenResponse.map(e => {
          if (e.message) return e.message;
          if (e.cause) return e.cause;
          if (e.description) return e.description;
          return JSON.stringify(e);
        });
        throw new Error(errorMessages.join(', ') || 'Error en los datos de la tarjeta');
      }
      
      if (tokenResponse.error) {
        console.error('Token error:', tokenResponse);
        throw new Error(tokenResponse.error.message || tokenResponse.error);
      }
      
      if (!tokenResponse.id) {
        console.error('No token ID in response:', tokenResponse);
        throw new Error('No se pudo generar el token de la tarjeta');
      }
      
      const cardToken = tokenResponse.id;
      console.log('Card token created:', cardToken);
      
      // Get session token from localStorage
      const sessionToken = localStorage.getItem('remy_session_token');
      
      console.log('Submitting payment with plan:', selectedPlan);
      console.log('Plan ID being sent:', selectedPlan.id);
      
      // Send to backend
      const response = await axios.post(
        `${API}/payments/subscribe`,
        {
          plan_id: selectedPlan.id,
          card_token: cardToken
        },
        { 
          headers: sessionToken ? { Authorization: `Bearer ${sessionToken}` } : {}
        }
      );
      
      console.log('Backend response:', response.data);
      
      if (response.data.success) {
        toast.success('¡Suscripción activada exitosamente!');
        await refreshUser();
        navigate('/biblioteca?subscription=success');
      } else if (response.data.init_point) {
        // Redirect to Mercado Pago if additional verification needed
        window.location.href = response.data.init_point;
      }
      
    } catch (error) {
      console.error('Payment error:', error);
      console.error('Error response:', error.response?.data);
      
      let message = 'Error al procesar el pago';
      
      if (error.response?.data?.detail) {
        message = error.response.data.detail;
      } else if (error.message) {
        const errMsg = error.message.toLowerCase();
        // Handle Mercado Pago SDK errors
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
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-cyan-900 flex items-center justify-center">
        <Loader2 className="w-8 h-8 text-cyan-500 animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-cyan-900 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <button 
            onClick={() => navigate(-1)}
            className="text-slate-400 hover:text-white flex items-center gap-2 mb-4 transition-colors"
          >
            <ArrowLeft size={20} />
            Volver
          </button>
          <h1 className="text-3xl font-bold text-white">Suscríbete a Remy</h1>
          <p className="text-slate-400 mt-2">Elige tu plan y comienza a aprender hoy</p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Plan Selection */}
          <div className="space-y-4">
            <h2 className="text-xl font-semibold text-white mb-4">Selecciona tu plan</h2>
            
            {plans.map((plan) => (
              <Card
                key={plan.id}
                className={`cursor-pointer transition-all text-slate-900 ${
                  selectedPlan?.id === plan.id
                    ? 'ring-2 ring-cyan-500 bg-white'
                    : 'bg-white/90 hover:bg-white'
                }`}
                onClick={() => setSelectedPlan(plan)}
                data-testid={`plan-card-${plan.id}`}
              >
                <CardContent className="p-6">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <h3 className="font-bold text-lg text-slate-900">{plan.name}</h3>
                        {plan.discount && (
                          <Badge className="bg-green-100 text-green-700">{plan.discount} OFF</Badge>
                        )}
                      </div>
                      <p className="text-slate-600 text-sm mt-1">{plan.description}</p>
                      
                      <div className="mt-4">
                        {plan.original_amount && (
                          <span className="text-slate-400 line-through text-sm mr-2">
                            ${plan.original_amount.toLocaleString('es-CL')}
                          </span>
                        )}
                        <span className="text-2xl font-bold text-slate-900">
                          ${plan.amount.toLocaleString('es-CL')}
                        </span>
                        <span className="text-slate-500 text-sm ml-1">
                          {plan.currency}/{plan.frequency}
                        </span>
                      </div>
                      
                      <ul className="mt-4 space-y-2">
                        {plan.features.slice(0, 3).map((feature, idx) => (
                          <li key={idx} className="flex items-center text-sm text-slate-600">
                            <Check size={16} className="text-green-500 mr-2 flex-shrink-0" />
                            {feature}
                          </li>
                        ))}
                      </ul>
                    </div>
                    
                    <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                      selectedPlan?.id === plan.id 
                        ? 'border-cyan-500 bg-cyan-500' 
                        : 'border-slate-300'
                    }`}>
                      {selectedPlan?.id === plan.id && (
                        <Check size={14} className="text-white" />
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Payment Form */}
          <div>
            <Card className="bg-white text-slate-900">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-slate-900">
                  <CreditCard size={20} />
                  Información de pago
                </CardTitle>
                <CardDescription className="text-slate-600">
                  Pago seguro con Mercado Pago
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="cardNumber" className="text-slate-700">Número de tarjeta</Label>
                    <Input
                      id="cardNumber"
                      placeholder="1234 5678 9012 3456"
                      value={cardNumber}
                      onChange={(e) => setCardNumber(formatCardNumber(e.target.value))}
                      maxLength={19}
                      data-testid="card-number-input"
                      className="bg-white text-slate-900 placeholder:text-slate-400 border-slate-300"
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="cardExpiry" className="text-slate-700">Vencimiento</Label>
                      <Input
                        id="cardExpiry"
                        placeholder="MM/AA"
                        value={cardExpiry}
                        onChange={(e) => setCardExpiry(formatExpiry(e.target.value))}
                        maxLength={5}
                        data-testid="card-expiry-input"
                        className="bg-white text-slate-900 placeholder:text-slate-400 border-slate-300"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="cardCvv" className="text-slate-700">CVV</Label>
                      <Input
                        id="cardCvv"
                        placeholder="123"
                        type="password"
                        value={cardCvv}
                        onChange={(e) => setCardCvv(e.target.value.replace(/\D/g, '').slice(0, 4))}
                        maxLength={4}
                        data-testid="card-cvv-input"
                        className="bg-white text-slate-900 placeholder:text-slate-400 border-slate-300"
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="cardHolder" className="text-slate-700">Nombre del titular</Label>
                    <Input
                      id="cardHolder"
                      placeholder="Como aparece en la tarjeta"
                      value={cardHolder}
                      onChange={(e) => setCardHolder(e.target.value.toUpperCase())}
                      data-testid="card-holder-input"
                      className="bg-white text-slate-900 placeholder:text-slate-400 border-slate-300"
                    />
                  </div>

                  <div className="grid grid-cols-3 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="docType" className="text-slate-700">Tipo Doc.</Label>
                      <select
                        id="docType"
                        value={docType}
                        onChange={(e) => setDocType(e.target.value)}
                        className="w-full h-10 px-3 rounded-md border border-slate-300 bg-white text-slate-900 text-sm"
                        data-testid="doc-type-select"
                      >
                        <option value="RUT">RUT</option>
                        <option value="DNI">DNI</option>
                        <option value="CI">CI</option>
                      </select>
                    </div>
                    <div className="col-span-2 space-y-2">
                      <Label htmlFor="docNumber" className="text-slate-700">Número de documento</Label>
                      <Input
                        id="docNumber"
                        placeholder="123456789"
                        value={docNumber}
                        onChange={(e) => setDocNumber(e.target.value.replace(/[.-]/g, ''))}
                        data-testid="doc-number-input"
                        className="bg-white text-slate-900 placeholder:text-slate-400 border-slate-300"
                      />
                      <p className="text-xs text-slate-500">Sin puntos ni guión (ej: 123456789)</p>
                    </div>
                  </div>
                  
                  {/* Summary */}
                  {selectedPlan && (
                    <div className="bg-slate-50 rounded-lg p-4 mt-6">
                      <div className="flex justify-between items-center">
                        <span className="text-slate-600">Total a pagar:</span>
                        <span className="text-2xl font-bold text-slate-900">
                          ${selectedPlan.amount.toLocaleString('es-CL')} {selectedPlan.currency}
                        </span>
                      </div>
                      <p className="text-xs text-slate-500 mt-1">
                        Se renovará automáticamente cada {selectedPlan.frequency === 'mensual' ? 'mes' : '6 meses'}
                      </p>
                    </div>
                  )}
                  
                  <Button
                    type="submit"
                    className="w-full h-12 bg-cyan-500 hover:bg-cyan-600 text-white text-lg mt-4"
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
                  
                  <div className="flex items-center justify-center gap-2 text-xs text-slate-500 mt-4">
                    <Lock size={12} />
                    <span>Pago seguro procesado por Mercado Pago</span>
                  </div>
                </form>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SubscribePage;
