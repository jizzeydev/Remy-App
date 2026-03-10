/**
 * Authentication Context for Remy Platform
 * Handles Google OAuth + Email/Password authentication
 */
import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

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
      const response = await axios.get(`${API}/auth/me`, {
        withCredentials: true
      });
      setUser(response.data);
    } catch (err) {
      // Not authenticated - that's ok
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  // Email/Password Registration
  const register = async (email, password, name) => {
    try {
      setError(null);
      const response = await axios.post(`${API}/auth/register`, {
        email,
        password,
        name
      }, {
        withCredentials: true
      });
      
      setUser(response.data.user);
      return { success: true, user: response.data.user };
    } catch (err) {
      const message = err.response?.data?.detail || 'Error al registrarse';
      setError(message);
      return { success: false, error: message };
    }
  };

  // Email/Password Login
  const login = async (email, password) => {
    try {
      setError(null);
      const response = await axios.post(`${API}/auth/login`, {
        email,
        password
      }, {
        withCredentials: true
      });
      
      setUser(response.data.user);
      return { success: true, user: response.data.user };
    } catch (err) {
      const message = err.response?.data?.detail || 'Credenciales incorrectas';
      setError(message);
      return { success: false, error: message };
    }
  };

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
      const response = await axios.post(`${API}/auth/google/session`, {
        session_id: sessionId
      }, {
        withCredentials: true
      });
      
      setUser(response.data.user);
      return { success: true, user: response.data.user };
    } catch (err) {
      const message = err.response?.data?.detail || 'Error de autenticación con Google';
      setError(message);
      return { success: false, error: message };
    }
  };

  // Logout
  const logout = async () => {
    try {
      await axios.post(`${API}/auth/logout`, {}, {
        withCredentials: true
      });
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      setUser(null);
    }
  };

  // Check if user has active subscription
  const hasActiveSubscription = () => {
    return user?.subscription_status === 'active';
  };

  const value = {
    user,
    loading,
    error,
    isAuthenticated: !!user,
    hasActiveSubscription,
    register,
    login,
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
