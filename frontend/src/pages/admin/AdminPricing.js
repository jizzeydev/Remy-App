import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Switch } from '@/components/ui/switch';
import { Badge } from '@/components/ui/badge';
import { toast } from 'sonner';
import { 
  DollarSign, Percent, Calendar, Save, RotateCcw, 
  CheckCircle, Star, ArrowLeft, Eye 
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const ADMIN_API = `${BACKEND_URL}/api/payments/admin`;

const AdminPricing = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [previewMode, setPreviewMode] = useState(false);
  
  // Pricing state — defaults match launch pricing ($4.990 / $19.990)
  const [monthly, setMonthly] = useState({
    name: 'Plan Mensual',
    description: 'Acceso completo por 1 mes',
    base_price: 4990,
    features: ['Acceso a todos los cursos', 'Simulacros ilimitados', 'Seguimiento de progreso', 'Correcciones detalladas'],
    discount_enabled: false,
    discount_percentage: 0,
    promotion_start: '',
    promotion_end: '',
    is_popular: false
  });

  const [semestral, setSemestral] = useState({
    name: 'Plan Semestral',
    description: 'El más popular - 6 meses de acceso',
    base_price: 29940,
    final_price: 19990,
    features: ['Acceso a todos los cursos', 'Simulacros ilimitados', 'Seguimiento de progreso', 'Correcciones detalladas', 'Acceso anticipado a nuevos cursos'],
    discount_enabled: true,
    discount_percentage: 33,
    promotion_start: '',
    promotion_end: '',
    is_popular: true
  });

  useEffect(() => {
    fetchPricingConfig();
  }, []);

  const fetchPricingConfig = async () => {
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.get(`${ADMIN_API}/pricing`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      if (response.data.plans) {
        const plans = response.data.plans;
        
        if (plans.monthly) {
          setMonthly({
            name: plans.monthly.name || 'Plan Mensual',
            description: plans.monthly.description || '',
            base_price: plans.monthly.base_price || 4990,
            features: plans.monthly.features || [],
            discount_enabled: plans.monthly.discount_enabled || false,
            discount_percentage: plans.monthly.discount_percentage || 0,
            promotion_start: plans.monthly.promotion_start || '',
            promotion_end: plans.monthly.promotion_end || '',
            is_popular: plans.monthly.is_popular || false
          });
        }
        
        if (plans.semestral) {
          setSemestral({
            name: plans.semestral.name || 'Plan Semestral',
            description: plans.semestral.description || '',
            base_price: plans.semestral.base_price || 29940,
            final_price: plans.semestral.final_price || 19990,
            features: plans.semestral.features || [],
            discount_enabled: plans.semestral.discount_enabled || true,
            discount_percentage: plans.semestral.discount_percentage || 33,
            promotion_start: plans.semestral.promotion_start || '',
            promotion_end: plans.semestral.promotion_end || '',
            is_popular: plans.semestral.is_popular || true
          });
        }
      }
    } catch (error) {
      console.error('Error fetching pricing:', error);
      toast.error('Error al cargar configuración de precios');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      const token = localStorage.getItem('admin_token');
      
      await axios.put(`${ADMIN_API}/pricing`, {
        monthly: {
          ...monthly,
          promotion_start: monthly.promotion_start || null,
          promotion_end: monthly.promotion_end || null
        },
        semestral: {
          ...semestral,
          promotion_start: semestral.promotion_start || null,
          promotion_end: semestral.promotion_end || null
        }
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      toast.success('Precios actualizados correctamente');
    } catch (error) {
      console.error('Error saving pricing:', error);
      toast.error('Error al guardar precios');
    } finally {
      setSaving(false);
    }
  };

  const handleReset = async () => {
    if (!window.confirm('¿Restaurar precios a valores por defecto?')) return;
    
    try {
      const token = localStorage.getItem('admin_token');
      await axios.post(`${ADMIN_API}/pricing/reset`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      toast.success('Precios restaurados');
      fetchPricingConfig();
    } catch (error) {
      console.error('Error resetting pricing:', error);
      toast.error('Error al restaurar precios');
    }
  };

  const formatPrice = (amount) => {
    return new Intl.NumberFormat('es-CL').format(amount);
  };

  const calculateDiscountedPrice = (basePrice, discountPct) => {
    return Math.round(basePrice * (100 - discountPct) / 100);
  };

  const handleFeatureChange = (planSetter, features, index, value) => {
    const newFeatures = [...features];
    newFeatures[index] = value;
    planSetter(prev => ({ ...prev, features: newFeatures }));
  };

  const addFeature = (planSetter, features) => {
    planSetter(prev => ({ ...prev, features: [...features, ''] }));
  };

  const removeFeature = (planSetter, features, index) => {
    const newFeatures = features.filter((_, i) => i !== index);
    planSetter(prev => ({ ...prev, features: newFeatures }));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin w-8 h-8 border-4 border-cyan-500 border-t-transparent rounded-full" />
      </div>
    );
  }

  // Preview Card Component
  const PricingPreviewCard = ({ plan, isPopular }) => {
    const hasDiscount = plan.discount_enabled && plan.discount_percentage > 0;
    const finalPrice = plan.final_price || calculateDiscountedPrice(plan.base_price, plan.discount_percentage);
    
    return (
      <Card className={`relative ${isPopular ? 'border-2 border-cyan-500 shadow-lg' : 'border-slate-200'}`}>
        {isPopular && (
          <div className="absolute top-0 left-0 right-0 bg-cyan-500 text-white text-center py-1 text-sm font-semibold">
            MÁS POPULAR
          </div>
        )}
        {hasDiscount && (
          <div className="absolute top-4 right-4">
            <Badge className="bg-red-500 text-white">{plan.discount_percentage}% DCTO</Badge>
          </div>
        )}
        <CardHeader className={isPopular ? 'pt-10' : ''}>
          <CardTitle>{plan.name}</CardTitle>
          <CardDescription>{plan.description}</CardDescription>
          <div className="mt-4">
            {hasDiscount && (
              <span className="text-slate-400 line-through text-lg mr-2">
                ${formatPrice(plan.base_price)}
              </span>
            )}
            <span className="text-4xl font-bold">
              ${formatPrice(hasDiscount ? finalPrice : plan.base_price)}
            </span>
          </div>
        </CardHeader>
        <CardContent>
          <ul className="space-y-2">
            {plan.features.filter(f => f.trim()).map((feature, i) => (
              <li key={i} className="flex items-center gap-2 text-sm">
                <CheckCircle className="text-cyan-500" size={16} />
                {feature}
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" onClick={() => navigate('/admin')}>
            <ArrowLeft size={20} className="mr-2" />
            Volver
          </Button>
          <div>
            <h1 className="text-3xl font-bold">Gestión de Precios</h1>
            <p className="text-slate-600">Configura los planes de suscripción</p>
          </div>
        </div>
        <div className="flex gap-2">
          <Button 
            variant="outline" 
            onClick={() => setPreviewMode(!previewMode)}
            className="gap-2"
          >
            <Eye size={18} />
            {previewMode ? 'Editar' : 'Vista Previa'}
          </Button>
          <Button 
            variant="outline" 
            onClick={handleReset}
            className="gap-2"
          >
            <RotateCcw size={18} />
            Restaurar
          </Button>
          <Button 
            onClick={handleSave} 
            disabled={saving}
            className="bg-cyan-500 hover:bg-cyan-400 gap-2"
          >
            <Save size={18} />
            {saving ? 'Guardando...' : 'Guardar Cambios'}
          </Button>
        </div>
      </div>

      {previewMode ? (
        // Preview Mode
        <div className="space-y-6">
          <Card className="bg-cyan-50 border-cyan-200">
            <CardContent className="py-4">
              <p className="text-cyan-700 text-center">
                Vista previa de cómo se verán los precios en la landing page
              </p>
            </CardContent>
          </Card>
          
          <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
            <PricingPreviewCard plan={monthly} isPopular={monthly.is_popular} />
            <PricingPreviewCard plan={semestral} isPopular={semestral.is_popular} />
          </div>
        </div>
      ) : (
        // Edit Mode
        <div className="grid lg:grid-cols-2 gap-6">
          {/* Monthly Plan */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2">
                  <DollarSign className="text-cyan-500" size={24} />
                  Plan Mensual
                </CardTitle>
                <div className="flex items-center gap-2">
                  <Label htmlFor="monthly-popular" className="text-sm">Popular</Label>
                  <Switch
                    id="monthly-popular"
                    checked={monthly.is_popular}
                    onCheckedChange={(checked) => setMonthly({...monthly, is_popular: checked})}
                  />
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>Nombre del Plan</Label>
                  <Input
                    value={monthly.name}
                    onChange={(e) => setMonthly({...monthly, name: e.target.value})}
                  />
                </div>
                <div>
                  <Label>Precio Base (CLP)</Label>
                  <Input
                    type="number"
                    value={monthly.base_price}
                    onChange={(e) => setMonthly({...monthly, base_price: parseInt(e.target.value) || 0})}
                  />
                </div>
              </div>
              
              <div>
                <Label>Descripción</Label>
                <Input
                  value={monthly.description}
                  onChange={(e) => setMonthly({...monthly, description: e.target.value})}
                />
              </div>

              {/* Discount Section */}
              <div className="border rounded-lg p-4 space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Percent className="text-green-500" size={20} />
                    <Label>Descuento Activo</Label>
                  </div>
                  <Switch
                    checked={monthly.discount_enabled}
                    onCheckedChange={(checked) => setMonthly({...monthly, discount_enabled: checked})}
                  />
                </div>
                
                {monthly.discount_enabled && (
                  <>
                    <div>
                      <Label>Porcentaje de Descuento (%)</Label>
                      <Input
                        type="number"
                        min="0"
                        max="100"
                        value={monthly.discount_percentage}
                        onChange={(e) => setMonthly({...monthly, discount_percentage: parseInt(e.target.value) || 0})}
                      />
                      <p className="text-sm text-slate-500 mt-1">
                        Precio final: ${formatPrice(calculateDiscountedPrice(monthly.base_price, monthly.discount_percentage))}
                      </p>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <Label className="flex items-center gap-1">
                          <Calendar size={14} />
                          Inicio Promoción
                        </Label>
                        <Input
                          type="datetime-local"
                          value={monthly.promotion_start}
                          onChange={(e) => setMonthly({...monthly, promotion_start: e.target.value})}
                        />
                      </div>
                      <div>
                        <Label className="flex items-center gap-1">
                          <Calendar size={14} />
                          Fin Promoción
                        </Label>
                        <Input
                          type="datetime-local"
                          value={monthly.promotion_end}
                          onChange={(e) => setMonthly({...monthly, promotion_end: e.target.value})}
                        />
                      </div>
                    </div>
                    <p className="text-xs text-slate-400">
                      Deja vacío para descuento permanente
                    </p>
                  </>
                )}
              </div>

              {/* Features */}
              <div>
                <Label>Características</Label>
                <div className="space-y-2 mt-2">
                  {monthly.features.map((feature, index) => (
                    <div key={index} className="flex gap-2">
                      <Input
                        value={feature}
                        onChange={(e) => handleFeatureChange(setMonthly, monthly.features, index, e.target.value)}
                        placeholder="Característica..."
                      />
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        onClick={() => removeFeature(setMonthly, monthly.features, index)}
                      >
                        ×
                      </Button>
                    </div>
                  ))}
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    onClick={() => addFeature(setMonthly, monthly.features)}
                  >
                    + Agregar característica
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Semestral Plan */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2">
                  <Star className="text-yellow-500" size={24} />
                  Plan Semestral
                </CardTitle>
                <div className="flex items-center gap-2">
                  <Label htmlFor="semestral-popular" className="text-sm">Popular</Label>
                  <Switch
                    id="semestral-popular"
                    checked={semestral.is_popular}
                    onCheckedChange={(checked) => setSemestral({...semestral, is_popular: checked})}
                  />
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>Nombre del Plan</Label>
                  <Input
                    value={semestral.name}
                    onChange={(e) => setSemestral({...semestral, name: e.target.value})}
                  />
                </div>
                <div>
                  <Label>Precio Original (CLP)</Label>
                  <Input
                    type="number"
                    value={semestral.base_price}
                    onChange={(e) => setSemestral({...semestral, base_price: parseInt(e.target.value) || 0})}
                  />
                </div>
              </div>
              
              <div>
                <Label>Descripción</Label>
                <Input
                  value={semestral.description}
                  onChange={(e) => setSemestral({...semestral, description: e.target.value})}
                />
              </div>

              {/* Discount Section */}
              <div className="border rounded-lg p-4 space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Percent className="text-green-500" size={20} />
                    <Label>Descuento Activo</Label>
                  </div>
                  <Switch
                    checked={semestral.discount_enabled}
                    onCheckedChange={(checked) => setSemestral({...semestral, discount_enabled: checked})}
                  />
                </div>
                
                {semestral.discount_enabled && (
                  <>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <Label>Porcentaje (%)</Label>
                        <Input
                          type="number"
                          min="0"
                          max="100"
                          value={semestral.discount_percentage}
                          onChange={(e) => setSemestral({...semestral, discount_percentage: parseInt(e.target.value) || 0})}
                        />
                      </div>
                      <div>
                        <Label>Precio Final (CLP)</Label>
                        <Input
                          type="number"
                          value={semestral.final_price}
                          onChange={(e) => setSemestral({...semestral, final_price: parseInt(e.target.value) || 0})}
                        />
                      </div>
                    </div>
                    <p className="text-sm text-slate-500">
                      {semestral.base_price > 0 && semestral.final_price > 0 && (
                        <>Descuento real: {Math.round((1 - semestral.final_price / semestral.base_price) * 100)}%</>
                      )}
                    </p>
                    
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <Label className="flex items-center gap-1">
                          <Calendar size={14} />
                          Inicio Promoción
                        </Label>
                        <Input
                          type="datetime-local"
                          value={semestral.promotion_start}
                          onChange={(e) => setSemestral({...semestral, promotion_start: e.target.value})}
                        />
                      </div>
                      <div>
                        <Label className="flex items-center gap-1">
                          <Calendar size={14} />
                          Fin Promoción
                        </Label>
                        <Input
                          type="datetime-local"
                          value={semestral.promotion_end}
                          onChange={(e) => setSemestral({...semestral, promotion_end: e.target.value})}
                        />
                      </div>
                    </div>
                    <p className="text-xs text-slate-400">
                      Deja vacío para descuento permanente
                    </p>
                  </>
                )}
              </div>

              {/* Features */}
              <div>
                <Label>Características</Label>
                <div className="space-y-2 mt-2">
                  {semestral.features.map((feature, index) => (
                    <div key={index} className="flex gap-2">
                      <Input
                        value={feature}
                        onChange={(e) => handleFeatureChange(setSemestral, semestral.features, index, e.target.value)}
                        placeholder="Característica..."
                      />
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        onClick={() => removeFeature(setSemestral, semestral.features, index)}
                      >
                        ×
                      </Button>
                    </div>
                  ))}
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    onClick={() => addFeature(setSemestral, semestral.features)}
                  >
                    + Agregar característica
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Info Card */}
      <Card className="bg-slate-50">
        <CardContent className="py-4">
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 bg-cyan-100 rounded-full flex items-center justify-center flex-shrink-0">
              <DollarSign className="text-cyan-600" size={18} />
            </div>
            <div>
              <h4 className="font-semibold">Cómo funcionan los precios</h4>
              <ul className="text-sm text-slate-600 mt-2 space-y-1">
                <li>• Los cambios se aplican inmediatamente en la landing page</li>
                <li>• Puedes configurar promociones temporales con fechas de inicio y fin</li>
                <li>• Si no defines fechas, el descuento estará activo permanentemente</li>
                <li>• El plan marcado como "Popular" se destacará visualmente</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default AdminPricing;
