/**
 * Progreso Page - Real data from backend
 * Shows: lessons completed, quizzes taken, average grade
 */
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { BookOpen, ClipboardCheck, TrendingUp, Award, Loader2, ChevronRight } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Button } from '@/components/ui/button';
import { useAuth } from '../contexts/AuthContext';
import SubscriptionRequired from '../components/SubscriptionRequired';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Progreso = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [courses, setCourses] = useState([]);
  const [courseProgress, setCourseProgress] = useState({});
  const [quizStats, setQuizStats] = useState({ total: 0, average: 0, grades: [] });

  const getStudentId = () => {
    if (user?.user_id) return user.user_id;
    return localStorage.getItem('student_id') || 'anonymous';
  };

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    setLoading(true);
    const studentId = getStudentId();
    
    try {
      // Fetch courses
      const coursesRes = await axios.get(`${API}/courses`);
      const coursesData = coursesRes.data;
      setCourses(coursesData);

      // Fetch progress for each course
      const progressMap = {};
      let totalLessons = 0;
      let completedLessons = 0;

      for (const course of coursesData) {
        try {
          // Get chapters and lessons count
          const chaptersRes = await axios.get(`${API}/courses/${course.id}/chapters`);
          const chapters = chaptersRes.data;
          
          let courseLessons = 0;
          for (const chapter of chapters) {
            const lessonsRes = await axios.get(`${API}/chapters/${chapter.id}/lessons`);
            courseLessons += lessonsRes.data.length;
          }
          
          // Get progress
          let courseCompleted = 0;
          try {
            const progressRes = await axios.get(`${API}/progress/${studentId}/${course.id}`);
            courseCompleted = progressRes.data.completed_lessons?.length || 0;
          } catch (e) {
            // No progress yet
          }

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
      try {
        const quizzesRes = await axios.get(`${API}/quiz/history/${studentId}`);
        const quizzes = quizzesRes.data || [];
        
        const grades = quizzes.map(q => q.grade || 0).filter(g => g > 0);
        const average = grades.length > 0 
          ? (grades.reduce((a, b) => a + b, 0) / grades.length).toFixed(1)
          : 0;

        setQuizStats({
          total: quizzes.length,
          average: parseFloat(average),
          grades: grades.slice(0, 10) // Last 10 grades
        });
      } catch (e) {
        console.error('Error fetching quizzes:', e);
      }

    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Calculate totals
  const totalLessons = Object.values(courseProgress).reduce((sum, p) => sum + p.total, 0);
  const completedLessons = Object.values(courseProgress).reduce((sum, p) => sum + p.completed, 0);
  const overallProgress = totalLessons > 0 ? Math.round((completedLessons / totalLessons) * 100) : 0;

  // Get grade color
  const getGradeColor = (grade) => {
    if (grade >= 6) return 'text-green-600 dark:text-green-400';
    if (grade >= 5) return 'text-primary';
    if (grade >= 4) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="animate-spin text-primary" size={32} />
      </div>
    );
  }

  return (
    <div className="space-y-6 pb-24 lg:pb-8" data-testid="progreso-page">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Mi Progreso</h1>
        <p className="text-muted-foreground mt-1">Tu avance de aprendizaje en Remy</p>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Lessons Completed */}
        <Card className="border-0 shadow-md bg-gradient-to-br from-primary/10 to-transparent">
          <CardContent className="pt-6">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm text-muted-foreground mb-1">Lecciones completadas</p>
                <p className="text-4xl font-bold text-foreground">{completedLessons}</p>
                <p className="text-sm text-muted-foreground mt-1">de {totalLessons} totales</p>
              </div>
              <div className="bg-primary/20 p-3 rounded-xl">
                <BookOpen className="text-primary" size={24} />
              </div>
            </div>
            <Progress value={overallProgress} className="mt-4 h-2" />
            <p className="text-xs text-muted-foreground mt-2">{overallProgress}% completado</p>
          </CardContent>
        </Card>

        {/* Quizzes Taken */}
        <Card className="border-0 shadow-md bg-gradient-to-br from-purple-500/10 to-transparent">
          <CardContent className="pt-6">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm text-muted-foreground mb-1">Simulacros realizados</p>
                <p className="text-4xl font-bold text-foreground">{quizStats.total}</p>
                <p className="text-sm text-muted-foreground mt-1">simulacros de práctica</p>
              </div>
              <div className="bg-purple-500/20 p-3 rounded-xl">
                <ClipboardCheck className="text-purple-600 dark:text-purple-400" size={24} />
              </div>
            </div>
            {quizStats.total > 0 && (
              <Button 
                variant="link" 
                className="p-0 h-auto mt-4 text-purple-600 dark:text-purple-400"
                onClick={() => navigate('/simulacros')}
              >
                Ver historial <ChevronRight size={16} />
              </Button>
            )}
          </CardContent>
        </Card>

        {/* Average Grade */}
        <Card className="border-0 shadow-md bg-gradient-to-br from-green-500/10 to-transparent">
          <CardContent className="pt-6">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm text-muted-foreground mb-1">Nota promedio</p>
                {quizStats.total > 0 ? (
                  <>
                    <p className={`text-4xl font-bold ${getGradeColor(quizStats.average)}`}>
                      {quizStats.average}
                    </p>
                    <p className="text-sm text-muted-foreground mt-1">escala 1.0 - 7.0</p>
                  </>
                ) : (
                  <>
                    <p className="text-4xl font-bold text-muted-foreground">-</p>
                    <p className="text-sm text-muted-foreground mt-1">Sin simulacros aún</p>
                  </>
                )}
              </div>
              <div className="bg-green-500/20 p-3 rounded-xl">
                <Award className="text-green-600 dark:text-green-400" size={24} />
              </div>
            </div>
            {quizStats.average >= 4 && quizStats.total > 0 && (
              <div className="mt-4 text-sm text-green-600 dark:text-green-400 flex items-center gap-1">
                <TrendingUp size={14} />
                {quizStats.average >= 6 ? '¡Excelente trabajo!' : 
                 quizStats.average >= 5 ? '¡Vas muy bien!' : 'Sigue practicando'}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Course Progress */}
      <Card>
        <CardHeader>
          <CardTitle>Progreso por curso</CardTitle>
          <CardDescription>Tu avance en cada curso disponible</CardDescription>
        </CardHeader>
        <CardContent>
          {courses.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              No hay cursos disponibles aún
            </div>
          ) : (
            <div className="space-y-6">
              {courses.map((course) => {
                const progress = courseProgress[course.id] || { total: 0, completed: 0, percentage: 0 };
                return (
                  <div 
                    key={course.id} 
                    className="p-4 rounded-xl bg-secondary/50 hover:bg-secondary transition-colors cursor-pointer"
                    onClick={() => navigate(`/course/${course.id}`)}
                  >
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <h4 className="font-semibold text-foreground">{course.title}</h4>
                        <p className="text-sm text-muted-foreground">{course.category}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-lg font-bold text-primary">{progress.percentage}%</p>
                        <p className="text-xs text-muted-foreground">
                          {progress.completed}/{progress.total} lecciones
                        </p>
                      </div>
                    </div>
                    <Progress value={progress.percentage} className="h-2" />
                  </div>
                );
              })}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Recent Quizzes */}
      {quizStats.grades.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Últimas notas en simulacros</CardTitle>
            <CardDescription>Tus {quizStats.grades.length} simulacros más recientes</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex gap-3 flex-wrap">
              {quizStats.grades.map((grade, idx) => (
                <div 
                  key={idx}
                  className={`w-12 h-12 rounded-xl flex items-center justify-center font-bold text-lg ${
                    grade >= 6 ? 'bg-green-500/20 text-green-600 dark:text-green-400' :
                    grade >= 5 ? 'bg-primary/20 text-primary' :
                    grade >= 4 ? 'bg-yellow-500/20 text-yellow-600 dark:text-yellow-400' :
                    'bg-red-500/20 text-red-600 dark:text-red-400'
                  }`}
                >
                  {grade.toFixed(1)}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Empty state for new users */}
      {completedLessons === 0 && quizStats.total === 0 && (
        <Card className="border-dashed">
          <CardContent className="py-12 text-center">
            <div className="w-16 h-16 bg-primary/20 rounded-full mx-auto mb-4 flex items-center justify-center">
              <TrendingUp className="text-primary" size={32} />
            </div>
            <h3 className="text-xl font-semibold text-foreground mb-2">
              ¡Comienza tu aventura de aprendizaje!
            </h3>
            <p className="text-muted-foreground mb-6 max-w-md mx-auto">
              Completa lecciones y realiza simulacros para ver tu progreso aquí.
            </p>
            <Button onClick={() => navigate('/biblioteca')} className="bg-primary hover:bg-primary/90">
              Explorar cursos
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

// Wrap with subscription guard
export default function ProgresoPage() {
  return (
    <SubscriptionRequired feature="tu página de progreso">
      <Progreso />
    </SubscriptionRequired>
  );
}
