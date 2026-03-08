import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { MessageSquare, ClipboardCheck, BookOpen, Calculator, TrendingUp, Sparkles } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { motion } from 'framer-motion';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Dashboard = () => {
  const navigate = useNavigate();
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const userId = 'demo-user-001';

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    try {
      const response = await axios.get(`${API}/courses`);
      setCourses(response.data.slice(0, 3));
    } catch (error) {
      console.error('Error fetching courses:', error);
    } finally {
      setLoading(false);
    }
  };

  const quickActions = [
    { icon: MessageSquare, label: 'Pregunta a Remy', path: '/chat', color: 'bg-cyan-500', testId: 'quick-action-chat' },
    { icon: ClipboardCheck, label: 'Crear Simulacro', path: '/simulacros', color: 'bg-blue-500', testId: 'quick-action-quiz' },
    { icon: Calculator, label: 'Buscar Fórmula', path: '/formulas', color: 'bg-emerald-500', testId: 'quick-action-formula' },
    { icon: BookOpen, label: 'Mis Cursos', path: '/biblioteca', color: 'bg-purple-500', testId: 'quick-action-courses' },
  ];

  return (
    <div className="space-y-8 pb-24 lg:pb-8">
      {/* Welcome Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        data-testid="welcome-section"
      >
        <div className="flex items-center gap-3 mb-2">
          <Sparkles className="text-primary" size={28} />
          <h1 className="text-3xl md:text-4xl font-bold">Hola, Estudiante 👋</h1>
        </div>
        <p className="text-slate-600 text-lg">¿Listo para aprender hoy?</p>
      </motion.div>

      {/* Quick Actions */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {quickActions.map((action, index) => {
          const Icon = action.icon;
          return (
            <motion.div
              key={index}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
            >
              <Card
                className="cursor-pointer hover:shadow-[0_8px_24px_rgba(0,188,212,0.15)] transition-all hover:-translate-y-1"
                onClick={() => navigate(action.path)}
                data-testid={action.testId}
              >
                <CardContent className="p-6 flex flex-col items-center text-center gap-3">
                  <div className={`${action.color} p-4 rounded-xl`}>
                    <Icon className="text-white" size={24} />
                  </div>
                  <span className="font-semibold text-sm">{action.label}</span>
                </CardContent>
              </Card>
            </motion.div>
          );
        })}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column - Stats & Progress */}
        <div className="lg:col-span-8 space-y-6">
          {/* Daily Challenge */}
          <Card className="bg-gradient-to-r from-cyan-500 to-blue-500 text-white border-0">
            <CardHeader>
              <CardTitle className="text-white">Reto diario</CardTitle>
              <CardDescription className="text-cyan-50">Completa el reto de hoy y gana +50 XP</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <p className="text-lg">¿Cuál es la derivada de x²?</p>
                <div className="flex gap-3">
                  <Button
                    variant="secondary"
                    data-testid="challenge-option-1"
                    className="bg-white/20 hover:bg-white/30 text-white border-white/30"
                  >
                    2x
                  </Button>
                  <Button
                    variant="secondary"
                    data-testid="challenge-option-2"
                    className="bg-white/20 hover:bg-white/30 text-white border-white/30"
                  >
                    x
                  </Button>
                  <Button
                    variant="secondary"
                    data-testid="challenge-option-3"
                    className="bg-white/20 hover:bg-white/30 text-white border-white/30"
                  >
                    2x²
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Recent Courses */}
          <Card data-testid="recent-courses-card">
            <CardHeader>
              <CardTitle>Continúa estudiando</CardTitle>
              <CardDescription>Tus cursos recientes</CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="text-center py-8 text-slate-500">Cargando cursos...</div>
              ) : courses.length > 0 ? (
                <div className="space-y-4">
                  {courses.map((course, index) => (
                    <div
                      key={course.id}
                      className="flex items-center gap-4 p-4 rounded-xl border border-slate-100 hover:bg-secondary transition-colors cursor-pointer"
                      data-testid={`course-item-${index}`}
                      onClick={() => navigate('/biblioteca')}
                    >
                      <div className="flex-shrink-0 w-16 h-16 bg-gradient-to-br from-cyan-400 to-cyan-600 rounded-lg flex items-center justify-center text-white font-bold text-xl">
                        {course.title.charAt(0)}
                      </div>
                      <div className="flex-1 min-w-0">
                        <h4 className="font-semibold truncate">{course.title}</h4>
                        <p className="text-sm text-slate-500">{course.modules_count} módulos</p>
                        <Progress value={Math.random() * 100} className="mt-2" />
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8">
                  <p className="text-slate-500 mb-4">No hay cursos disponibles aún</p>
                  <Button onClick={() => navigate('/biblioteca')} data-testid="browse-courses-button">
                    Explorar cursos
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Right Column - Activity & Tips */}
        <div className="lg:col-span-4 space-y-6">
          {/* Progress Summary */}
          <Card data-testid="progress-summary-card">
            <CardHeader>
              <CardTitle className="text-lg">Tu progreso</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-sm font-medium">Lecciones completadas</span>
                  <span className="text-sm font-bold text-primary">12/20</span>
                </div>
                <Progress value={60} className="h-2" />
              </div>
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-sm font-medium">Simulacros realizados</span>
                  <span className="text-sm font-bold text-primary">5</span>
                </div>
                <Progress value={40} className="h-2" />
              </div>
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-sm font-medium">Promedio</span>
                  <span className="text-sm font-bold text-primary">85%</span>
                </div>
                <Progress value={85} className="h-2" />
              </div>
              <Button
                className="w-full mt-4 rounded-full"
                onClick={() => navigate('/progreso')}
                data-testid="view-progress-button"
              >
                <TrendingUp size={16} className="mr-2" />
                Ver detalles
              </Button>
            </CardContent>
          </Card>

          {/* Study Tip */}
          <Card className="bg-gradient-to-br from-amber-50 to-orange-50 border-amber-200" data-testid="study-tip-card">
            <CardHeader>
              <CardTitle className="text-lg text-amber-900">Consejo del día</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-amber-800 leading-relaxed">
                💡 Estudia en bloques de 25 minutos seguidos de 5 minutos de descanso. Esta técnica mejora la concentración y retención.
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
