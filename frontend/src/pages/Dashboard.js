/**
 * Dashboard - Main student dashboard with real data
 */
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { ClipboardCheck, BookOpen, TrendingUp, Sparkles, Loader2, ChevronRight } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { useAuth } from '../contexts/AuthContext';
import SubscriptionRequired from '../components/SubscriptionRequired';

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
      // Fetch courses
      const coursesRes = await axios.get(`${API}/courses`);
      const coursesData = coursesRes.data.slice(0, 3);
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
      {/* Welcome Section */}
      <div data-testid="welcome-section">
        <div className="flex items-center gap-3 mb-2">
          <Sparkles className="text-cyan-500" size={28} />
          <h1 className="text-3xl md:text-4xl font-bold text-slate-900">
            Hola, {userName} 👋
          </h1>
        </div>
        <p className="text-slate-600 text-lg">¿Listo para aprender hoy?</p>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-3 gap-4">
        {quickActions.map((action, index) => {
          const Icon = action.icon;
          return (
            <Card
              key={index}
              className="cursor-pointer hover:shadow-lg transition-all hover:-translate-y-1 border-0 shadow-md"
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
          );
        })}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column - Courses */}
        <div className="lg:col-span-8 space-y-6">
          {/* Recent Courses */}
          <Card className="border-0 shadow-md" data-testid="recent-courses-card">
            <CardHeader>
              <CardTitle>Continúa estudiando</CardTitle>
              <CardDescription>Tus cursos disponibles</CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="animate-spin text-cyan-500" size={32} />
                </div>
              ) : courses.length > 0 ? (
                <div className="space-y-4">
                  {courses.map((course, index) => {
                    const progress = courseProgress[course.id] || { total: 0, completed: 0, percentage: 0 };
                    return (
                      <div
                        key={course.id}
                        className="flex items-center gap-4 p-4 rounded-xl bg-slate-50 hover:bg-slate-100 transition-colors cursor-pointer"
                        data-testid={`course-item-${index}`}
                        onClick={() => navigate(`/course/${course.id}`)}
                      >
                        <div className="flex-shrink-0 w-16 h-16 bg-gradient-to-br from-cyan-400 to-cyan-600 rounded-xl flex items-center justify-center text-white font-bold text-xl">
                          {course.title.charAt(0)}
                        </div>
                        <div className="flex-1 min-w-0">
                          <h4 className="font-semibold truncate text-slate-900">{course.title}</h4>
                          <p className="text-sm text-slate-500">
                            {progress.completed}/{progress.total} lecciones completadas
                          </p>
                          <Progress value={progress.percentage} className="mt-2 h-2" />
                        </div>
                        <ChevronRight className="text-slate-400" size={20} />
                      </div>
                    );
                  })}
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

        {/* Right Column - Stats */}
        <div className="lg:col-span-4 space-y-6">
          {/* Progress Summary */}
          <Card className="border-0 shadow-md" data-testid="progress-summary-card">
            <CardHeader>
              <CardTitle className="text-lg">Tu progreso</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-sm font-medium text-slate-600">Lecciones completadas</span>
                  <span className="text-sm font-bold text-cyan-600">
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
                  <span className="text-sm font-medium text-slate-600">Simulacros realizados</span>
                  <span className="text-sm font-bold text-purple-600">{stats.quizzes}</span>
                </div>
              </div>
              {stats.quizzes > 0 && (
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-slate-600">Nota promedio</span>
                    <span className={`text-sm font-bold ${
                      stats.average >= 6 ? 'text-green-600' :
                      stats.average >= 5 ? 'text-cyan-600' :
                      stats.average >= 4 ? 'text-yellow-600' : 'text-red-600'
                    }`}>
                      {stats.average}
                    </span>
                  </div>
                </div>
              )}
              <Button
                className="w-full mt-4 rounded-full bg-cyan-500 hover:bg-cyan-600"
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
              <p className="text-amber-800 leading-relaxed text-sm">
                💡 Estudia en bloques de 25 minutos seguidos de 5 minutos de descanso. Esta técnica mejora la concentración y retención.
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
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
