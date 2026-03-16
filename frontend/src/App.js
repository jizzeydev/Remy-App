import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { Toaster } from '@/components/ui/sonner';
import { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { PricingProvider } from './hooks/usePricing';
import Layout from './components/Layout';
import AdminLayout from './components/AdminLayout';
import Landing from './pages/Landing';
import AuthPage from './pages/AuthPage';
import AuthCallback from './pages/AuthCallback';
import SubscribePage from './pages/SubscribePage';
import MiSuscripcion from './pages/MiSuscripcion';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Simulacros from './pages/Simulacros';
import Biblioteca from './pages/Biblioteca';
import Progreso from './pages/Progreso';
import CourseViewer from './pages/student/CourseViewer';
import LessonViewer from './pages/student/LessonViewer';
import AdminLogin from './pages/admin/AdminLogin';
import AdminAuthCallback from './pages/admin/AdminAuthCallback';
import AdminDashboard from './pages/admin/AdminDashboard';
import AdminCourses from './pages/admin/AdminCourses';
import AdminQuestions from './pages/admin/AdminQuestions';
import AdminUsers from './pages/admin/AdminUsers';
import AdminPricing from './pages/admin/AdminPricing';
import AdminUniversities from './pages/admin/AdminUniversities';
import UniversityDetail from './pages/admin/UniversityDetail';
import CourseContentEditor from './pages/admin/CourseContentEditor';
import '@/App.css';

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
      <div className="flex items-center justify-center min-h-screen bg-slate-50">
        <div className="text-center">
          <div className="animate-spin w-8 h-8 border-4 border-cyan-500 border-t-transparent rounded-full mx-auto mb-4" />
          <p className="text-slate-600">Cargando...</p>
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

// App Router with session_id detection
function AppRouter() {
  const location = useLocation();
  
  // Check URL fragment for session_id synchronously during render
  // This prevents race conditions by processing new session_id FIRST
  // BUT: Don't intercept admin routes - they have their own callback handler
  if (location.hash?.includes('session_id=') && !location.pathname.startsWith('/admin')) {
    return <AuthCallback />;
  }
  
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/" element={<Landing />} />
      <Route path="/auth" element={<AuthPage />} />
      <Route path="/auth/callback" element={<AuthCallback />} />
      <Route path="/subscribe" element={<StudentProtectedRoute><SubscribePage /></StudentProtectedRoute>} />
      <Route path="/mi-suscripcion" element={<StudentProtectedRoute><MiSuscripcion /></StudentProtectedRoute>} />
      
      {/* Student App - Protected */}
      <Route element={<StudentProtectedRoute><Layout /></StudentProtectedRoute>}>
        <Route path="/inicio" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/simulacros" element={<Simulacros />} />
        <Route path="/biblioteca" element={<Biblioteca />} />
        <Route path="/course/:courseId" element={<CourseViewer />} />
        <Route path="/lesson/:lessonId" element={<LessonViewer />} />
        <Route path="/progreso" element={<Progreso />} />
      </Route>
      
      {/* Admin Routes */}
      <Route path="/admin/login" element={<AdminLogin />} />
      <Route path="/admin/auth/callback" element={<AdminAuthCallback />} />
      <Route element={<AdminProtectedRoute><AdminLayout /></AdminProtectedRoute>}>
        <Route path="/admin" element={<Navigate to="/admin/dashboard" replace />} />
        <Route path="/admin/dashboard" element={<AdminDashboard />} />
        <Route path="/admin/courses" element={<AdminCourses />} />
        <Route path="/admin/courses/:courseId/content" element={<CourseContentEditor />} />
        <Route path="/admin/questions" element={<AdminQuestions />} />
        <Route path="/admin/users" element={<AdminUsers />} />
        <Route path="/admin/pricing" element={<AdminPricing />} />
        <Route path="/admin/universities" element={<AdminUniversities />} />
        <Route path="/admin/universities/:universityId" element={<UniversityDetail />} />
      </Route>
    </Routes>
  );
}

function App() {
  return (
    <div className="App">
      <AuthProvider>
        <PricingProvider>
          <BrowserRouter>
            <AppRouter />
          </BrowserRouter>
          <Toaster richColors position="top-right" />
        </PricingProvider>
      </AuthProvider>
    </div>
  );
}

export default App;
