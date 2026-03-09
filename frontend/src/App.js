import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from '@/components/ui/sonner';
import { useState, useEffect } from 'react';
import Layout from './components/Layout';
import AdminLayout from './components/AdminLayout';
import Landing from './pages/Landing';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Simulacros from './pages/Simulacros';
import Biblioteca from './pages/Biblioteca';
import Progreso from './pages/Progreso';
import CourseViewer from './pages/student/CourseViewer';
import LessonViewer from './pages/student/LessonViewer';
import AdminLogin from './pages/admin/AdminLogin';
import AdminDashboard from './pages/admin/AdminDashboard';
import AdminCourses from './pages/admin/AdminCourses';
import AdminQuestions from './pages/admin/AdminQuestions';
import CourseContentEditor from './pages/admin/CourseContentEditor';
import '@/App.css';

function ProtectedRoute({ children }) {
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

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          {/* Landing Page */}
          <Route path="/" element={<Landing />} />
          
          {/* Student App */}
          <Route element={<Layout />}>
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
          <Route element={<ProtectedRoute><AdminLayout /></ProtectedRoute>}>
            <Route path="/admin" element={<Navigate to="/admin/dashboard" replace />} />
            <Route path="/admin/dashboard" element={<AdminDashboard />} />
            <Route path="/admin/courses" element={<AdminCourses />} />
            <Route path="/admin/courses/:courseId/content" element={<CourseContentEditor />} />
            <Route path="/admin/questions" element={<AdminQuestions />} />
          </Route>
        </Routes>
      </BrowserRouter>
      <Toaster richColors position="top-right" />
    </div>
  );
}

export default App;
