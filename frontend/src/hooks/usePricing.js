/**
 * usePricing Hook - Centralized pricing data from backend
 * All pricing across the app MUST use this hook
 */
import { useState, useEffect, createContext, useContext } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Context for pricing data
const PricingContext = createContext(null);

// Default pricing (fallback only - should rarely be needed)
// Launch prices: $4.990 mensual / $19.990 semestral (33% off vs paying month-by-month)
const DEFAULT_PRICING = {
  monthly: {
    id: 'monthly',
    name: 'Plan Mensual',
    description: 'Acceso completo por 1 mes',
    amount: 4990,
    original_amount: null,
    discount_percentage: 0,
    discount_active: false,
    currency: 'CLP',
    frequency: 'mensual',
    period: 'mes',
    features: [
      'Acceso a todos los cursos',
      'Simulacros ilimitados',
      'Seguimiento de progreso',
      'Correcciones detalladas'
    ]
  },
  semestral: {
    id: 'semestral',
    name: 'Plan Semestral',
    description: 'El más popular - 6 meses de acceso',
    amount: 19990,
    original_amount: 29940,
    discount_percentage: 33,
    discount_active: true,
    currency: 'CLP',
    frequency: 'semestral',
    period: '6 meses',
    is_popular: true,
    features: [
      'Acceso a todos los cursos',
      'Simulacros ilimitados',
      'Seguimiento de progreso',
      'Correcciones detalladas',
      'Acceso anticipado a nuevos cursos'
    ]
  }
};

/**
 * Pricing Provider Component
 * Wrap your app with this to provide pricing data
 */
export const PricingProvider = ({ children }) => {
  const [pricing, setPricing] = useState(DEFAULT_PRICING);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchPricing();
  }, []);

  const fetchPricing = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API}/payments/plans`);
      const plans = response.data.plans || [];
      
      const pricingData = { ...DEFAULT_PRICING };
      
      plans.forEach(plan => {
        if (plan.id === 'monthly' || plan.id === 'semestral') {
          const discountActive = plan.original_amount && plan.original_amount > plan.amount;
          const discountPct = discountActive 
            ? Math.round((1 - plan.amount / plan.original_amount) * 100)
            : (plan.discount ? parseInt(plan.discount) : 0);
          
          pricingData[plan.id] = {
            id: plan.id,
            name: plan.name,
            description: plan.description,
            amount: plan.amount,
            original_amount: plan.original_amount || null,
            discount_percentage: discountPct,
            discount_active: discountActive || !!plan.discount,
            currency: plan.currency || 'CLP',
            frequency: plan.frequency,
            period: plan.id === 'monthly' ? 'mes' : '6 meses',
            is_popular: plan.is_popular || plan.id === 'semestral',
            features: plan.features || DEFAULT_PRICING[plan.id].features
          };
        }
      });
      
      setPricing(pricingData);
      setError(null);
    } catch (err) {
      console.error('Error fetching pricing:', err);
      setError(err);
      // Keep default pricing on error
    } finally {
      setLoading(false);
    }
  };

  const value = {
    pricing,
    loading,
    error,
    refetch: fetchPricing
  };

  return (
    <PricingContext.Provider value={value}>
      {children}
    </PricingContext.Provider>
  );
};

/**
 * usePricing Hook
 * Use this hook to get pricing data anywhere in the app
 * 
 * @returns {Object} pricing data and utilities
 * 
 * @example
 * const { monthly, semestral, formatPrice, loading } = usePricing();
 * console.log(monthly.amount); // 4990
 * console.log(formatPrice(monthly.amount)); // "$9.990"
 */
export const usePricing = () => {
  const context = useContext(PricingContext);
  
  // If not inside provider, fetch directly (standalone usage)
  const [standaloneData, setStandaloneData] = useState(null);
  const [standaloneLoading, setStandaloneLoading] = useState(!context);
  
  useEffect(() => {
    if (!context) {
      // Standalone mode - fetch pricing directly
      const fetchStandalone = async () => {
        try {
          const response = await axios.get(`${API}/payments/plans`);
          const plans = response.data.plans || [];
          
          const pricingData = { ...DEFAULT_PRICING };
          
          plans.forEach(plan => {
            if (plan.id === 'monthly' || plan.id === 'semestral') {
              const discountActive = plan.original_amount && plan.original_amount > plan.amount;
              const discountPct = discountActive 
                ? Math.round((1 - plan.amount / plan.original_amount) * 100)
                : (plan.discount ? parseInt(plan.discount) : 0);
              
              pricingData[plan.id] = {
                id: plan.id,
                name: plan.name,
                description: plan.description,
                amount: plan.amount,
                original_amount: plan.original_amount || null,
                discount_percentage: discountPct,
                discount_active: discountActive || !!plan.discount,
                currency: plan.currency || 'CLP',
                frequency: plan.frequency,
                period: plan.id === 'monthly' ? 'mes' : '6 meses',
                is_popular: plan.is_popular || plan.id === 'semestral',
                features: plan.features || DEFAULT_PRICING[plan.id].features
              };
            }
          });
          
          setStandaloneData(pricingData);
        } catch (err) {
          console.error('Error fetching standalone pricing:', err);
          setStandaloneData(DEFAULT_PRICING);
        } finally {
          setStandaloneLoading(false);
        }
      };
      
      fetchStandalone();
    }
  }, [context]);
  
  const pricing = context?.pricing || standaloneData || DEFAULT_PRICING;
  const loading = context?.loading ?? standaloneLoading;
  
  // Utility function to format price
  const formatPrice = (amount) => {
    return '$' + new Intl.NumberFormat('es-CL').format(amount);
  };
  
  // Get lowest price for marketing
  const getLowestPrice = () => {
    return Math.min(pricing.monthly.amount, pricing.semestral.amount);
  };
  
  // Get monthly equivalent for semestral
  const getSemestralMonthlyEquivalent = () => {
    return Math.round(pricing.semestral.amount / 6);
  };
  
  return {
    // Plan data
    monthly: pricing.monthly,
    semestral: pricing.semestral,
    plans: [pricing.monthly, pricing.semestral],
    
    // State
    loading,
    error: context?.error || null,
    
    // Utilities
    formatPrice,
    getLowestPrice,
    getSemestralMonthlyEquivalent,
    
    // Refetch function
    refetch: context?.refetch || (() => {}),
    
    // Raw pricing object
    pricing
  };
};

export default usePricing;
