import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { toast } from 'sonner';
import { BookOpen, GraduationCap, Loader2, Clock, ArrowRight, X, Building2 } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import InlineMd from '@/components/course/InlineMd';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const MisCursos = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({ enrolled_count: 0, limit: null, can_enroll_more: true });

  useEffect(() => {
    fetchEnrolledCourses();
    fetchEnrollmentStats();
  }, []);

  const fetchEnrolledCourses = async () => {
    try {
      const token = localStorage.getItem('remy_session_token');
      const response = await axios.get(`${API}/enrollments`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setCourses(response.data);
    } catch (error) {
      console.error('Error fetching enrolled courses:', error);
      if (error.response?.status !== 401) {
        toast.error('Error al cargar tus cursos');
      }
    } finally {
      setLoading(false);
    }
  };

  const fetchEnrollmentStats = async () => {
    try {
      const token = localStorage.getItem('remy_session_token');
      const response = await axios.get(`${API}/enrollments/stats`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const handleUnenroll = async (courseId, courseTitle) => {
    if (!window.confirm(`¿Desinscribirse de "${courseTitle}"?`)) return;
    
    try {
      const token = localStorage.getItem('remy_session_token');
      await axios.delete(`${API}/enrollments/${courseId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      toast.success('Desinscrito del curso');
      fetchEnrolledCourses();
      fetchEnrollmentStats();
    } catch (error) {
      console.error('Error unenrolling:', error);
      toast.error('Error al desinscribirse');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <Loader2 className="animate-spin text-primary" size={40} />
      </div>
    );
  }

  return (
    <div className="space-y-6" data-testid="mis-cursos-page">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Mis Cursos</h1>
          <p className="text-slate-600 dark:text-slate-400">
            Cursos en los que estás inscrito
          </p>
        </div>
        <Button onClick={() => navigate('/biblioteca')} data-testid="go-to-biblioteca">
          <BookOpen className="mr-2" size={18} />
          Explorar Biblioteca
        </Button>
      </div>

      {/* Stats - only show for non-subscribers */}
      {stats.limit && !stats.has_subscription && (
        <div className="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg p-4">
          <p className="text-amber-800 dark:text-amber-200 text-sm">
            <strong>Periodo de prueba:</strong> Puedes inscribirte en {stats.limit} curso durante los 7 días de prueba. 
            {!stats.can_enroll_more && " Ya alcanzaste el límite."}
            {" "}
            <button 
              onClick={() => navigate('/subscribe')}
              className="underline font-medium"
            >
              Suscríbete para acceso ilimitado
            </button>
          </p>
        </div>
      )}

      {courses.length === 0 ? (
        <Card className="p-12 text-center">
          <GraduationCap className="mx-auto mb-4 text-slate-400" size={64} />
          <h3 className="text-xl font-semibold mb-2">No tienes cursos inscritos</h3>
          <p className="text-slate-500 mb-6">
            Explora la biblioteca y encuentra cursos que te interesen
          </p>
          <Button size="lg" onClick={() => navigate('/biblioteca')}>
            <BookOpen className="mr-2" size={20} />
            Ir a Biblioteca
          </Button>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses.map((course) => (
            <Card 
              key={course.id} 
              className="hover:shadow-lg transition-all group"
              data-testid={`enrolled-course-${course.id}`}
            >
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between gap-2">
                  <CardTitle className="text-lg leading-tight flex-1">
                    {course.title}
                  </CardTitle>
                  {course.university && (
                    <Badge 
                      variant="outline" 
                      className="text-xs shrink-0"
                    >
                      {course.university.short_name === 'GEN' ? (
                        <span className="flex items-center gap-1">
                          <Building2 size={12} />
                          General
                        </span>
                      ) : (
                        course.university.short_name
                      )}
                    </Badge>
                  )}
                </div>
                <div className="flex items-center gap-2 mt-2">
                  <Badge className="bg-primary/10 text-primary">
                    {course.level}
                  </Badge>
                  <Badge variant="secondary">
                    {course.category}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-slate-600 dark:text-slate-400 mb-4 line-clamp-2">
                  <InlineMd>{course.description}</InlineMd>
                </p>
                
                {course.enrolled_at && (
                  <div className="flex items-center gap-2 text-xs text-slate-500 mb-4">
                    <Clock size={14} />
                    <span>
                      Inscrito el {new Date(course.enrolled_at).toLocaleDateString('es-CL')}
                    </span>
                  </div>
                )}
                
                <div className="flex gap-2">
                  <Button
                    className="flex-1"
                    onClick={() => navigate(`/course/${course.id}`)}
                    data-testid={`continue-course-${course.id}`}
                  >
                    Continuar
                    <ArrowRight className="ml-2" size={16} />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => handleUnenroll(course.id, course.title)}
                    className="text-slate-400 hover:text-red-500"
                    title="Desinscribirse"
                    data-testid={`unenroll-${course.id}`}
                  >
                    <X size={18} />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default MisCursos;
