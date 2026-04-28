import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { ArrowLeft, BookOpen, Play, Clock, CheckCircle, Lock, Plus, Loader2 } from 'lucide-react';
import { toast } from 'sonner';
import { useAuth } from '@/contexts/AuthContext';
import InlineMd from '@/components/course/InlineMd';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const CourseViewer = () => {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const { canAccessContent } = useAuth();
  const [course, setCourse] = useState(null);
  const [chapters, setChapters] = useState([]);
  const [completedLessons, setCompletedLessons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isEnrolled, setIsEnrolled] = useState(false);
  const [checkingEnrollment, setCheckingEnrollment] = useState(true);
  const [enrolling, setEnrolling] = useState(false);

  // Get student ID from localStorage
  const getStudentId = () => {
    let studentId = localStorage.getItem('student_id');
    if (!studentId) {
      studentId = 'student_' + Date.now();
      localStorage.setItem('student_id', studentId);
    }
    return studentId;
  };

  useEffect(() => {
    checkEnrollment();
    fetchCourseData();
  }, [courseId]);

  const checkEnrollment = async () => {
    try {
      const token = localStorage.getItem('remy_session_token');
      if (!token) {
        setIsEnrolled(false);
        setCheckingEnrollment(false);
        return;
      }
      
      const response = await axios.get(`${API}/enrollments/check/${courseId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setIsEnrolled(response.data.enrolled);
    } catch (error) {
      console.error('Error checking enrollment:', error);
      setIsEnrolled(false);
    } finally {
      setCheckingEnrollment(false);
    }
  };

  const handleEnroll = async () => {
    const token = localStorage.getItem('remy_session_token');
    if (!token) {
      navigate('/auth');
      return;
    }
    
    setEnrolling(true);
    try {
      await axios.post(
        `${API}/enrollments`,
        { course_id: courseId },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      toast.success('¡Inscrito exitosamente!');
      setIsEnrolled(true);
    } catch (error) {
      console.error('Error enrolling:', error);
      const msg = error.response?.data?.detail || 'Error al inscribirse';
      toast.error(msg);
      
      if (error.response?.status === 403) {
        navigate('/subscribe');
      }
    } finally {
      setEnrolling(false);
    }
  };

  const fetchCourseData = async () => {
    try {
      const [courseRes, chaptersRes] = await Promise.all([
        axios.get(`${API}/courses/${courseId}`),
        axios.get(`${API}/courses/${courseId}/chapters`)
      ]);

      setCourse(courseRes.data);

      const chaptersWithLessons = await Promise.all(
        chaptersRes.data.map(async (chapter) => {
          const lessonsRes = await axios.get(`${API}/chapters/${chapter.id}/lessons`);
          return { ...chapter, lessons: lessonsRes.data };
        })
      );

      setChapters(chaptersWithLessons);

      // Fetch progress
      try {
        const studentId = getStudentId();
        const progressRes = await axios.get(`${API}/progress/${studentId}/${courseId}`);
        setCompletedLessons(progressRes.data.completed_lessons || []);
      } catch (e) {
        // No progress yet
      }
    } catch (error) {
      console.error('Error fetching course:', error);
      toast.error('Error al cargar el curso');
    } finally {
      setLoading(false);
    }
  };

  // Calculate total lessons and progress
  const totalLessons = chapters.reduce((sum, ch) => sum + (ch.lessons?.length || 0), 0);
  const progressPercent = totalLessons > 0 ? Math.round((completedLessons.length / totalLessons) * 100) : 0;

  // Find next lesson to continue
  const findNextLesson = () => {
    for (const chapter of chapters) {
      for (const lesson of chapter.lessons || []) {
        if (!completedLessons.includes(lesson.id)) {
          return lesson;
        }
      }
    }
    // All completed, return first lesson
    return chapters[0]?.lessons?.[0];
  };

  if (loading || checkingEnrollment) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="animate-spin text-primary" size={32} />
      </div>
    );
  }
  
  if (!course) return <div className="text-center py-12 text-foreground">Curso no encontrado</div>;

  const nextLesson = findNextLesson();
  const hasAccess = canAccessContent();

  // If not enrolled, show enrollment prompt
  if (!isEnrolled) {
    return (
      <div className="space-y-6 pb-24 lg:pb-8">
        <Button variant="ghost" onClick={() => navigate('/biblioteca')}>
          <ArrowLeft size={20} className="mr-2" />
          Volver a biblioteca
        </Button>

        {/* Course header - Preview mode */}
        <div className="bg-gradient-to-r from-slate-600 to-slate-700 rounded-xl p-8 text-white relative overflow-hidden">
          <div className="absolute inset-0 bg-black/20 flex items-center justify-center">
            <Lock size={64} className="text-white/30" />
          </div>
          <div className="relative z-10">
            <h1 className="text-4xl font-bold mb-2">{course.title}</h1>
            <p className="text-xl text-white/80 mb-4"><InlineMd>{course.description}</InlineMd></p>
            <div className="flex items-center gap-4 text-sm mb-6">
              <span className="bg-white/20 px-3 py-1 rounded-full">{course.level}</span>
              <span className="bg-white/20 px-3 py-1 rounded-full">
                {chapters.length} capítulos
              </span>
              <span className="bg-white/20 px-3 py-1 rounded-full">
                {totalLessons} lecciones
              </span>
            </div>
          </div>
        </div>

        {/* Enrollment CTA */}
        <Card className="border-primary bg-primary/5">
          <CardContent className="text-center py-8">
            <Lock className="mx-auto mb-4 text-primary" size={48} />
            <h2 className="text-2xl font-bold mb-2 text-foreground">
              Inscríbete para acceder al contenido
            </h2>
            <p className="text-muted-foreground mb-6 max-w-md mx-auto">
              Para ver las lecciones, realizar ejercicios y hacer un seguimiento de tu progreso, 
              primero debes inscribirte en este curso.
            </p>
            
            {hasAccess ? (
              <Button 
                size="lg" 
                onClick={handleEnroll}
                disabled={enrolling}
                className="px-8"
              >
                {enrolling ? (
                  <>
                    <Loader2 className="animate-spin mr-2" size={20} />
                    Inscribiendo...
                  </>
                ) : (
                  <>
                    <Plus className="mr-2" size={20} />
                    Inscribirme en este curso
                  </>
                )}
              </Button>
            ) : (
              <div className="space-y-3">
                <p className="text-sm text-amber-600 dark:text-amber-400">
                  Necesitas una cuenta para inscribirte
                </p>
                <Button size="lg" onClick={() => navigate('/auth')}>
                  Crear cuenta gratis
                </Button>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Course preview - locked chapters */}
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-foreground">Vista previa del contenido</h2>
          {chapters.map((chapter, index) => (
            <Card key={chapter.id} className="opacity-75">
              <CardHeader className="bg-secondary/50">
                <div className="flex items-center justify-between">
                  <CardTitle className="flex items-center gap-3">
                    <span className="flex items-center justify-center w-10 h-10 rounded-full font-bold bg-slate-400 text-white">
                      <Lock size={16} />
                    </span>
                    <span className="text-foreground">{chapter.title}</span>
                  </CardTitle>
                  <span className="text-sm text-muted-foreground">
                    {chapter.lessons?.length || 0} lecciones
                  </span>
                </div>
                <p className="text-sm text-muted-foreground ml-13"><InlineMd>{chapter.description}</InlineMd></p>
              </CardHeader>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  // User is enrolled - show full content
  return (
    <div className="space-y-6 pb-24 lg:pb-8">
      <Button variant="ghost" onClick={() => navigate('/mis-cursos')}>
        <ArrowLeft size={20} className="mr-2" />
        Volver a Mis Cursos
      </Button>

      {/* Course header */}
      <div className="bg-gradient-to-r from-primary to-blue-600 rounded-xl p-8 text-white">
        <h1 className="text-4xl font-bold mb-2">{course.title}</h1>
        <p className="text-xl text-primary-foreground/80 mb-4"><InlineMd>{course.description}</InlineMd></p>
        <div className="flex items-center gap-4 text-sm mb-6">
          <span className="bg-white/20 px-3 py-1 rounded-full">{course.level}</span>
          <span className="bg-white/20 px-3 py-1 rounded-full">
            {chapters.length} capítulos
          </span>
          <span className="bg-white/20 px-3 py-1 rounded-full">
            {totalLessons} lecciones
          </span>
        </div>
        
        {/* Progress section */}
        <div className="bg-white/10 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="font-medium">Tu progreso</span>
            <span>{completedLessons.length}/{totalLessons} lecciones completadas</span>
          </div>
          <Progress value={progressPercent} className="h-3 bg-white/20" />
          
          {nextLesson && (
            <Button 
              className="mt-4 bg-white text-primary hover:bg-white/90"
              onClick={() => navigate(`/lesson/${nextLesson.id}`)}
            >
              {completedLessons.length === 0 ? 'Comenzar curso' : 
               progressPercent === 100 ? 'Repasar curso' : 'Continuar'}
            </Button>
          )}
        </div>
      </div>

      {/* Course content */}
      <div className="space-y-4">
        <h2 className="text-2xl font-bold text-foreground">Contenido del Curso</h2>
        {chapters.length === 0 ? (
          <Card>
            <CardContent className="text-center py-12">
              <BookOpen className="mx-auto mb-4 text-muted-foreground" size={48} />
              <p className="text-muted-foreground">Este curso aún no tiene contenido disponible</p>
            </CardContent>
          </Card>
        ) : (
          chapters.map((chapter, index) => {
            const chapterLessons = chapter.lessons || [];
            const chapterCompleted = chapterLessons.filter(l => completedLessons.includes(l.id)).length;
            const chapterProgress = chapterLessons.length > 0 
              ? Math.round((chapterCompleted / chapterLessons.length) * 100) 
              : 0;

            return (
              <Card key={chapter.id}>
                <CardHeader className="bg-secondary/50">
                  <div className="flex items-center justify-between">
                    <CardTitle className="flex items-center gap-3">
                      <span className={`flex items-center justify-center w-10 h-10 rounded-full font-bold ${
                        chapterProgress === 100 
                          ? 'bg-green-500 text-white' 
                          : 'bg-primary text-primary-foreground'
                      }`}>
                        {chapterProgress === 100 ? <CheckCircle size={20} /> : index + 1}
                      </span>
                      <span className="text-foreground">{chapter.title}</span>
                    </CardTitle>
                    <span className="text-sm text-muted-foreground">
                      {chapterCompleted}/{chapterLessons.length} completadas
                    </span>
                  </div>
                  <p className="text-sm text-muted-foreground ml-13"><InlineMd>{chapter.description}</InlineMd></p>
                </CardHeader>
                <CardContent className="pt-4">
                  {chapterLessons.length === 0 ? (
                    <p className="text-sm text-muted-foreground italic">No hay lecciones disponibles</p>
                  ) : (
                    <div className="space-y-2">
                      {chapterLessons.map((lesson, lessonIndex) => {
                        const isCompleted = completedLessons.includes(lesson.id);
                        return (
                          <button
                            key={lesson.id}
                            onClick={() => navigate(`/lesson/${lesson.id}`)}
                            className={`w-full flex items-center justify-between p-4 border rounded-lg transition-all group ${
                              isCompleted 
                                ? 'border-green-500/30 bg-green-500/10 hover:bg-green-500/20' 
                                : 'border-border hover:bg-primary/10 hover:border-primary'
                            }`}
                          >
                            <div className="flex items-center gap-3">
                              <div className={`w-8 h-8 rounded-full flex items-center justify-center transition-colors ${
                                isCompleted 
                                  ? 'bg-green-500 text-white' 
                                  : 'bg-secondary group-hover:bg-primary group-hover:text-primary-foreground'
                              }`}>
                                {isCompleted ? <CheckCircle size={16} /> : <Play size={16} />}
                              </div>
                              <div className="text-left">
                                <p className={`font-medium transition-colors ${
                                  isCompleted ? 'text-green-600 dark:text-green-400' : 'text-foreground group-hover:text-primary'
                                }`}>
                                  {lessonIndex + 1}. {lesson.title}
                                </p>
                                <div className="flex items-center gap-2 text-xs text-muted-foreground mt-1">
                                  <Clock size={12} />
                                  {lesson.duration_minutes} min
                                  {isCompleted && (
                                    <span className="text-green-600 dark:text-green-400 font-medium ml-2">✓ Completada</span>
                                  )}
                                </div>
                              </div>
                            </div>
                            <ArrowLeft size={20} className={`rotate-180 transition-colors ${
                              isCompleted ? 'text-green-500' : 'text-muted-foreground group-hover:text-primary'
                            }`} />
                          </button>
                        );
                      })}
                    </div>
                  )}
                </CardContent>
              </Card>
            );
          })
        )}
      </div>
    </div>
  );
};

export default CourseViewer;
