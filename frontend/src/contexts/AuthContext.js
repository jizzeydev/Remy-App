/**
 * Authentication Context for Remy Platform
 * Handles Google OAuth + Email/Password authentication
 * Uses both cookies and localStorage for session persistence
 */
import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const SESSION_TOKEN_KEY = 'remy_session_token';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Helper to get session token from localStorage
const getStoredToken = () => localStorage.getItem(SESSION_TOKEN_KEY);
const storeToken = (token) => localStorage.setItem(SESSION_TOKEN_KEY, token);
const removeToken = () => localStorage.removeItem(SESSION_TOKEN_KEY);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Check authentication status
  const checkAuth = useCallback(async () => {
    // CRITICAL: If returning from OAuth callback, skip the /me check.
    // AuthCallback will exchange the session_id and establish the session first.
    // Also skip for admin routes - they handle their own auth
    if (window.location.hash?.includes('session_id=') || window.location.pathname.startsWith('/admin')) {
      setLoading(false);
      return;
    }

    try {
      // Get stored token for Authorization header
      const storedToken = getStoredToken();
      const headers = storedToken ? { Authorization: `Bearer ${storedToken}` } : {};
      
      const response = await axios.get(`${API}/auth/me`, {
        headers
      });
      setUser(response.data);
    } catch (err) {
      // Not authenticated - clear any stale token
      removeToken();
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  // Google OAuth - Redirect to Emergent Auth
  const loginWithGoogle = () => {
    // REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
    const redirectUrl = window.location.origin + '/auth/callback';
    window.location.href = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(redirectUrl)}`;
  };

  // Process Google OAuth callback
  const processGoogleCallback = async (sessionId) => {
    try {
      setError(null);
      console.log('Sending session_id to backend...');
      
      const response = await axios.post(`${API}/auth/google/session`, {
        session_id: sessionId
      }, {
        timeout: 15000 // 15 second timeout for slow mobile connections
      });
      
      console.log('Backend response received');
      
      // Store session token for persistence
      if (response.data.session_token) {
        storeToken(response.data.session_token);
        console.log('Session token stored');
      }
      
      setUser(response.data.user);
      return { success: true, user: response.data.user };
    } catch (err) {
      console.error('Google callback error:', err);
      
      let message = 'Error de autenticación con Google';
      
      if (err.code === 'ECONNABORTED' || err.message?.includes('timeout')) {
        message = 'Conexión lenta. Intenta de nuevo.';
      } else if (err.response?.data?.detail) {
        const detail = err.response.data.detail;
        if (detail.includes('expired') || detail.includes('not found')) {
          message = 'La sesión expiró. Intenta de nuevo.';
        } else {
          message = detail;
        }
      } else if (!navigator.onLine) {
        message = 'Sin conexión a internet';
      }
      
      setError(message);
      return { success: false, error: message };
    }
  };

  // Logout
  const logout = async () => {
    try {
      const storedToken = getStoredToken();
      const headers = storedToken ? { Authorization: `Bearer ${storedToken}` } : {};
      
      await axios.post(`${API}/auth/logout`, {}, {
        headers
      });
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      removeToken();
      setUser(null);
    }
  };

  // Check if user has active subscription (including cancelled but still in paid period)
  const hasActiveSubscription = () => {
    if (!user) return false;
    
    // Active subscription
    if (user.subscription_status === 'active') return true;
    
    // Cancelled but still has access until end date
    if (user.subscription_status === 'cancelled' && user.subscription_end) {
      try {
        const endDate = new Date(user.subscription_end);
        const now = new Date();
        if (endDate > now) {
          return true; // Still within paid period
        }
      } catch (e) {
        console.error('Error parsing subscription_end:', e);
      }
    }
    
    return false;
  };

  // Check if user has active trial
  const hasActiveTrial = () => {
    if (!user) return false;
    if (hasActiveSubscription()) return false; // Subscription takes priority
    
    if (!user.trial_active) return false;
    
    // Check if trial hasn't expired
    if (user.trial_end_date) {
      try {
        const trialEnd = new Date(user.trial_end_date);
        const now = new Date();
        if (trialEnd > now) {
          return true;
        }
      } catch (e) {
        console.error('Error parsing trial_end_date:', e);
      }
    }
    
    return false;
  };

  // Get trial days remaining
  const getTrialDaysRemaining = () => {
    if (!user || !user.trial_end_date) return 0;
    
    try {
      const trialEnd = new Date(user.trial_end_date);
      const now = new Date();
      const diffTime = trialEnd - now;
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      return Math.max(0, diffDays);
    } catch (e) {
      return 0;
    }
  };

  // Get trial simulations remaining
  const getTrialSimulationsRemaining = () => {
    if (!user) return 0;
    const used = user.trial_simulations_used || 0;
    const limit = user.trial_simulations_limit || 10;
    return Math.max(0, limit - used);
  };

  // Check if user can access content (subscription OR active trial)
  const canAccessContent = () => {
    return hasActiveSubscription() || hasActiveTrial();
  };

  const value = {
    user,
    loading,
    error,
    isAuthenticated: !!user,
    hasActiveSubscription,
    hasActiveTrial,
    getTrialDaysRemaining,
    getTrialSimulationsRemaining,
    canAccessContent,
    loginWithGoogle,
    processGoogleCallback,
    logout,
    refreshUser: checkAuth,
    setUser
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
