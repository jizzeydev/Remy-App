/**
 * Dashboard - Main student dashboard with real data
 */
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import axios from 'axios';
import { ClipboardCheck, BookOpen, TrendingUp, Sparkles, Loader2, ChevronRight } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { useAuth } from '../contexts/AuthContext';
import SubscriptionRequired from '../components/SubscriptionRequired';
import TrialBanner from '../components/TrialBanner';

const fadeUp = (i = 0) => ({
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.4, delay: i * 0.05, ease: [0.22, 1, 0.36, 1] }
});

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Dashboard = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [courses, setCourses] = useState([]);
  const [courseProgress, setCourseProgress] = useState({});
  const [stats, setStats] = useState({ lessons: 0, totalLessons: 0, quizzes: 0, average: 0 });
  const [loading, setLoading] = useState(true);

  const getStudentId = () => {
    if (user?.user_id) return user.user_id;
    return localStorage.getItem('student_id') || 'anonymous';
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    setLoading(true);
    const studentId = getStudentId();
    
    try {
      // Fetch ENROLLED courses only
      const token = localStorage.getItem('remy_session_token');
      let coursesData = [];
      
      if (token) {
        try {
          const enrolledRes = await axios.get(`${API}/enrollments`, {
            headers: { Authorization: `Bearer ${token}` }
          });
          coursesData = enrolledRes.data.slice(0, 3);
        } catch (e) {
          // Fallback to empty if not logged in
          coursesData = [];
        }
      }
      
      setCourses(coursesData);

      // Calculate progress for each course
      const progressMap = {};
      let totalLessons = 0;
      let completedLessons = 0;

      for (const course of coursesData) {
        try {
          const chaptersRes = await axios.get(`${API}/courses/${course.id}/chapters`);
          let courseLessons = 0;
          
          for (const chapter of chaptersRes.data) {
            const lessonsRes = await axios.get(`${API}/chapters/${chapter.id}/lessons`);
            courseLessons += lessonsRes.data.length;
          }

          let courseCompleted = 0;
          try {
            const progressRes = await axios.get(`${API}/progress/${studentId}/${course.id}`);
            courseCompleted = progressRes.data.completed_lessons?.length || 0;
          } catch (e) {}

          progressMap[course.id] = {
            total: courseLessons,
            completed: courseCompleted,
            percentage: courseLessons > 0 ? Math.round((courseCompleted / courseLessons) * 100) : 0
          };

          totalLessons += courseLessons;
          completedLessons += courseCompleted;
        } catch (e) {
          progressMap[course.id] = { total: 0, completed: 0, percentage: 0 };
        }
      }

      setCourseProgress(progressMap);

      // Fetch quiz stats
      let quizCount = 0;
      let quizAverage = 0;
      try {
        const quizzesRes = await axios.get(`${API}/quiz/history/${studentId}`);
        const quizzes = quizzesRes.data || [];
        quizCount = quizzes.length;
        
        const grades = quizzes.map(q => q.grade || 0).filter(g => g > 0);
        if (grades.length > 0) {
          quizAverage = (grades.reduce((a, b) => a + b, 0) / grades.length).toFixed(1);
        }
      } catch (e) {}

      setStats({
        lessons: completedLessons,
        totalLessons: totalLessons,
        quizzes: quizCount,
        average: parseFloat(quizAverage)
      });

    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const quickActions = [
    { icon: ClipboardCheck, label: 'Crear Simulacro', path: '/simulacros', color: 'bg-purple-500', testId: 'quick-action-quiz' },
    { icon: BookOpen, label: 'Mis Cursos', path: '/biblioteca', color: 'bg-cyan-500', testId: 'quick-action-courses' },
    { icon: TrendingUp, label: 'Ver Progreso', path: '/progreso', color: 'bg-green-500', testId: 'quick-action-progress' },
  ];

  const userName = user?.name?.split(' ')[0] || 'Estudiante';

  return (
    <div className="space-y-8 pb-24 lg:pb-8">
      {/* Trial Banner - Shows trial status or subscription prompt */}
      <TrialBanner />
      
      {/* Welcome Section */}
      <motion.div data-testid="welcome-section" {...fadeUp(0)}>
        <div className="flex items-center gap-3 mb-2">
          <Sparkles className="text-primary" size={28} aria-hidden="true" />
          <h1 className="text-3xl md:text-4xl font-bold text-foreground tracking-tight">
            Hola, {userName} 👋
          </h1>
        </div>
        <p className="text-muted-foreground text-lg">¿Listo para aprender hoy?</p>
      </motion.div>

      {/* Quick Actions */}
      <div className="grid grid-cols-3 gap-3 md:gap-4">
        {quickActions.map((action, index) => {
          const Icon = action.icon;
          return (
            <motion.div key={index} {...fadeUp(index + 1)}>
              <Card
                className="cursor-pointer hover:shadow-lg transition-all hover:-translate-y-0.5 border-border bg-card h-full"
                onClick={() => navigate(action.path)}
                data-testid={action.testId}
              >
                <CardContent className="p-4 md:p-6 flex flex-col items-center text-center gap-3">
                  <div className={`${action.color} p-3 md:p-4 rounded-xl`} aria-hidden="true">
                    <Icon className="text-white" size={24} />
                  </div>
                  <span className="font-semibold text-xs md:text-sm text-foreground">{action.label}</span>
                </CardContent>
              </Card>
            </motion.div>
          );
        })}
      </div>

      {/* Main Content Grid */}
      <motion.div {...fadeUp(4)} className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column - Courses */}
        <div className="lg:col-span-8 space-y-6">
          {/* Recent Courses */}
          <Card className="border-border bg-card shadow-sm" data-testid="recent-courses-card">
            <CardHeader>
              <CardTitle>Continúa estudiando</CardTitle>
              <CardDescription>Tus cursos disponibles</CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="flex items-center justify-center py-8" role="status" aria-live="polite">
                  <Loader2 className="animate-spin text-primary" size={32} />
                  <span className="sr-only">Cargando cursos</span>
                </div>
              ) : courses.length > 0 ? (
                <div className="space-y-4">
                  {courses.map((course, index) => {
                    const progress = courseProgress[course.id] || { total: 0, completed: 0, percentage: 0 };
                    return (
                      <div
                        key={course.id}
                        className="flex items-center gap-4 p-4 rounded-xl bg-secondary/50 hover:bg-secondary transition-colors cursor-pointer"
                        data-testid={`course-item-${index}`}
                        onClick={() => navigate(`/course/${course.id}`)}
                      >
                        <div className="flex-shrink-0 w-16 h-16 bg-gradient-to-br from-primary to-primary/70 rounded-xl flex items-center justify-center text-primary-foreground font-bold text-xl">
                          {course.title.charAt(0)}
                        </div>
                        <div className="flex-1 min-w-0">
                          <h4 className="font-semibold truncate text-foreground">{course.title}</h4>
                          <p className="text-sm text-muted-foreground">
                            {progress.completed}/{progress.total} lecciones completadas
                          </p>
                          <Progress value={progress.percentage} className="mt-2 h-2" />
                        </div>
                        <ChevronRight className="text-muted-foreground" size={20} />
                      </div>
                    );
                  })}
                </div>
              ) : (
                <div className="text-center py-8">
                  <BookOpen className="mx-auto mb-4 text-muted-foreground" size={48} />
                  <p className="text-muted-foreground mb-4">No tienes cursos inscritos</p>
                  <Button onClick={() => navigate('/biblioteca')} data-testid="browse-courses-button">
                    Explorar Biblioteca
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Right Column - Stats */}
        <div className="lg:col-span-4 space-y-6">
          {/* Progress Summary */}
          <Card className="border-border bg-card shadow-sm" data-testid="progress-summary-card">
            <CardHeader>
              <CardTitle className="text-lg">Tu progreso</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-sm font-medium text-muted-foreground">Lecciones completadas</span>
                  <span className="text-sm font-bold text-primary">
                    {stats.lessons}/{stats.totalLessons}
                  </span>
                </div>
                <Progress 
                  value={stats.totalLessons > 0 ? (stats.lessons / stats.totalLessons) * 100 : 0} 
                  className="h-2" 
                />
              </div>
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-sm font-medium text-muted-foreground">Simulacros realizados</span>
                  <span className="text-sm font-bold text-purple-600 dark:text-purple-400">{stats.quizzes}</span>
                </div>
              </div>
              {stats.quizzes > 0 && (
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-muted-foreground">Nota promedio</span>
                    <span className={`text-sm font-bold ${
                      stats.average >= 6 ? 'text-green-600 dark:text-green-400' :
                      stats.average >= 5 ? 'text-primary' :
                      stats.average >= 4 ? 'text-yellow-600 dark:text-yellow-400' : 'text-red-600 dark:text-red-400'
                    }`}>
                      {stats.average}
                    </span>
                  </div>
                </div>
              )}
              <Button
                className="w-full mt-4 rounded-full bg-primary hover:bg-primary/90"
                onClick={() => navigate('/progreso')}
                data-testid="view-progress-button"
              >
                <TrendingUp size={16} className="mr-2" />
                Ver detalles
              </Button>
            </CardContent>
          </Card>

          {/* Study Tip */}
          <Card className="bg-gradient-to-br from-amber-500/10 to-orange-500/10 border-amber-500/20" data-testid="study-tip-card">
            <CardHeader>
              <CardTitle className="text-lg text-amber-600 dark:text-amber-400">Consejo del día</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-foreground leading-relaxed text-sm">
                Estudia en bloques de 25 minutos seguidos de 5 minutos de descanso. Esta técnica mejora la concentración y retención.
              </p>
            </CardContent>
          </Card>
        </div>
      </motion.div>
    </div>
  );
};

// Wrap with subscription guard
export default function DashboardPage() {
  return (
    <SubscriptionRequired feature="el dashboard">
      <Dashboard />
    </SubscriptionRequired>
  );
}
