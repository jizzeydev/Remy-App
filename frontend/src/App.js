import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { Toaster } from '@/components/ui/sonner';
import { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';
import { PricingProvider } from './hooks/usePricing';
import Layout from './components/Layout';
import AdminLayout from './components/AdminLayout';
import Landing from './pages/Landing';
import AuthPage from './pages/AuthPage';
import SubscribePage from './pages/SubscribePage';
import MiSuscripcion from './pages/MiSuscripcion';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Simulacros from './pages/Simulacros';
import Biblioteca from './pages/Biblioteca';
import MisCursos from './pages/MisCursos';
import Progreso from './pages/Progreso';
import Logros from './pages/Logros';
import CourseViewer from './pages/student/CourseViewer';
import LessonViewer from './pages/student/LessonViewer';
import AdminLogin from './pages/admin/AdminLogin';
import AdminDashboard from './pages/admin/AdminDashboard';
import AdminCourses from './pages/admin/AdminCourses';
import AdminQuestions from './pages/admin/AdminQuestions';
import AdminUsers from './pages/admin/AdminUsers';
import AdminPricing from './pages/admin/AdminPricing';
import AdminLibraryUniversities from './pages/admin/AdminLibraryUniversities';
import CourseContentEditor from './pages/admin/CourseContentEditor';
import AdminTrash from './pages/admin/AdminTrash';
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
