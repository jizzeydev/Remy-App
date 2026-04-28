import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { Toaster } from '@/components/ui/sonner';
import { useState, useEffect, lazy, Suspense } from 'react';
import { Loader2 } from 'lucide-react';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';
import { PricingProvider } from './hooks/usePricing';

// ----- Eagerly loaded (first paint / common nav) -----
import Layout from './components/Layout';
import AdminLayout from './components/AdminLayout';
import Landing from './pages/Landing';
import AuthPage from './pages/AuthPage';
import MiSuscripcion from './pages/MiSuscripcion';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Biblioteca from './pages/Biblioteca';
import MisCursos from './pages/MisCursos';
import CourseViewer from './pages/student/CourseViewer';
import AdminLogin from './pages/admin/AdminLogin';

// ----- Lazy chunks (heavy deps + rarely-visited routes) -----
// Charts (recharts) — Simulacros & Progreso each pull recharts ~140KB.
const Simulacros = lazy(() => import('./pages/Simulacros'));
const Progreso = lazy(() => import('./pages/Progreso'));
const Logros = lazy(() => import('./pages/Logros'));
// LessonViewer pulls katex + markdown + BlockRenderer (plotly/three.js for some
// lesson content) — biggest single page in the app.
const LessonViewer = lazy(() => import('./pages/student/LessonViewer'));
// Mercado Pago SDK only loads when the user actually enters checkout.
const SubscribePage = lazy(() => import('./pages/SubscribePage'));
// Admin: most users never visit any of these — keep them off the student
// bundle entirely. Each admin page becomes its own chunk.
const AdminDashboard = lazy(() => import('./pages/admin/AdminDashboard'));
const AdminCourses = lazy(() => import('./pages/admin/AdminCourses'));
const AdminQuestions = lazy(() => import('./pages/admin/AdminQuestions'));
const AdminUsers = lazy(() => import('./pages/admin/AdminUsers'));
const AdminPricing = lazy(() => import('./pages/admin/AdminPricing'));
const AdminLibraryUniversities = lazy(() => import('./pages/admin/AdminLibraryUniversities'));
const CourseContentEditor = lazy(() => import('./pages/admin/CourseContentEditor'));
const AdminTrash = lazy(() => import('./pages/admin/AdminTrash'));

import '@/App.css';

// Spinner shown while a lazy chunk is downloading. Match the auth/loading look.
function ChunkFallback() {
  return (
    <div className="flex items-center justify-center min-h-[60vh] bg-background" role="status" aria-live="polite">
      <Loader2 className="animate-spin text-primary" size={32} />
      <span className="sr-only">Cargando…</span>
    </div>
  );
}

// Protected Route for Admin
function AdminProtectedRoute({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('admin_token');
    setIsAuthenticated(!!token);
  }, []);

  if (isAuthenticated === null) {
    return <div className="flex items-center justify-center min-h-screen">Cargando...</div>;
  }

  return isAuthenticated ? children : <Navigate to="/admin/login" replace />;
}

// Protected Route for Students (requires authentication)
function StudentProtectedRoute({ children }) {
  const { user, loading, isAuthenticated } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-background">
        <div className="text-center">
          <div className="animate-spin w-8 h-8 border-4 border-primary border-t-transparent rounded-full mx-auto mb-4" />
          <p className="text-muted-foreground">Cargando...</p>
        </div>
      </div>
    );
  }

  // If coming from auth callback with user data, allow access
  if (location.state?.user) {
    return children;
  }

  if (!isAuthenticated) {
    return <Navigate to="/auth" state={{ from: location }} replace />;
  }

  return children;
}

// App Router
function AppRouter() {
  return (
    <Suspense fallback={<ChunkFallback />}>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<Landing />} />
        <Route path="/auth" element={<AuthPage />} />
        <Route path="/subscribe" element={<StudentProtectedRoute><SubscribePage /></StudentProtectedRoute>} />
        <Route path="/mi-suscripcion" element={<StudentProtectedRoute><MiSuscripcion /></StudentProtectedRoute>} />

        {/* Student App - Protected */}
        <Route element={<StudentProtectedRoute><Layout /></StudentProtectedRoute>}>
          <Route path="/inicio" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/mis-cursos" element={<MisCursos />} />
          <Route path="/simulacros" element={<Simulacros />} />
          <Route path="/biblioteca" element={<Biblioteca />} />
          <Route path="/course/:courseId" element={<CourseViewer />} />
          <Route path="/lesson/:lessonId" element={<LessonViewer />} />
          <Route path="/progreso" element={<Progreso />} />
          <Route path="/logros" element={<Logros />} />
        </Route>

        {/* Admin Routes */}
        <Route path="/admin/login" element={<AdminLogin />} />
        <Route element={<AdminProtectedRoute><AdminLayout /></AdminProtectedRoute>}>
          <Route path="/admin" element={<Navigate to="/admin/dashboard" replace />} />
          <Route path="/admin/dashboard" element={<AdminDashboard />} />
          <Route path="/admin/courses" element={<AdminCourses />} />
          <Route path="/admin/courses/:courseId/content" element={<CourseContentEditor />} />
          <Route path="/admin/questions" element={<AdminQuestions />} />
          <Route path="/admin/users" element={<AdminUsers />} />
          <Route path="/admin/pricing" element={<AdminPricing />} />
          <Route path="/admin/library-universities" element={<AdminLibraryUniversities />} />
          <Route path="/admin/papelera" element={<AdminTrash />} />
        </Route>
      </Routes>
    </Suspense>
  );
}

const GOOGLE_CLIENT_ID = process.env.REACT_APP_GOOGLE_CLIENT_ID || '';

function App() {
  return (
    <div className="App">
      <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
        <ThemeProvider>
          <AuthProvider>
            <PricingProvider>
              <BrowserRouter>
                <AppRouter />
              </BrowserRouter>
              <Toaster richColors position="top-right" />
            </PricingProvider>
          </AuthProvider>
        </ThemeProvider>
      </GoogleOAuthProvider>
    </div>
  );
}

export default App;
