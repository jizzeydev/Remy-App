import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { ArrowLeft, ChevronRight, BookOpen, Play, Clock, CheckCircle, Lock, Plus, Loader2 } from 'lucide-react';
import { toast } from 'sonner';
import { useAuth } from '@/contexts/AuthContext';
import InlineMd from '@/components/course/InlineMd';

const fadeUp = (i = 0) => ({
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.4, delay: i * 0.05, ease: [0.22, 1, 0.36, 1] }
});

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
      <div className="flex items-center justify-center py-12" role="status" aria-live="polite">
        <Loader2 className="animate-spin text-primary" size={32} />
        <span className="sr-only">Cargando curso</span>
      </div>
    );
  }

  if (!course) return <div className="text-center py-12 text-muted-foreground">Curso no encontrado</div>;

  const nextLesson = findNextLesson();
  const hasAccess = canAccessContent();

  // If not enrolled, show enrollment prompt
  if (!isEnrolled) {
    return (
      <div className="space-y-6 pb-24 lg:pb-8">
        <motion.div {...fadeUp(0)}>
          <Button variant="ghost" onClick={() => navigate('/biblioteca')} className="text-muted-foreground hover:text-foreground">
            <ArrowLeft size={20} className="mr-2" />
            Volver a biblioteca
          </Button>
        </motion.div>

        {/* Course header — preview (locked) */}
        <motion.div
          {...fadeUp(1)}
          className="bg-gradient-to-br from-slate-700 via-slate-800 to-slate-900 dark:from-slate-800 dark:via-slate-900 dark:to-slate-950 rounded-xl p-6 md:p-8 text-white relative overflow-hidden"
        >
          <div className="absolute inset-0 pointer-events-none" aria-hidden="true">
            <div className="absolute -top-20 -right-20 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl" />
          </div>
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none" aria-hidden="true">
            <Lock size={96} className="text-white/[0.07]" />
          </div>
          <div className="relative z-10">
            <h1 className="text-3xl md:text-4xl font-bold mb-2 tracking-tight">{course.title}</h1>
            <p className="text-base md:text-lg text-white/80 mb-4"><InlineMd>{course.description}</InlineMd></p>
            <div className="flex items-center gap-2 text-sm flex-wrap">
              <span className="bg-white/15 backdrop-blur-sm px-3 py-1 rounded-full">{course.level}</span>
              <span className="bg-white/15 backdrop-blur-sm px-3 py-1 rounded-full tabular-nums">
                {chapters.length} capítulos
              </span>
              <span className="bg-white/15 backdrop-blur-sm px-3 py-1 rounded-full tabular-nums">
                {totalLessons} lecciones
              </span>
            </div>
          </div>
        </motion.div>

        {/* Enrollment CTA */}
        <motion.div {...fadeUp(2)}>
          <Card className="border-primary/30 bg-primary/5">
            <CardContent className="text-center py-8 md:py-10">
              <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-primary/15 ring-1 ring-primary/30 flex items-center justify-center">
                <Lock className="text-primary" size={28} aria-hidden="true" />
              </div>
              <h2 className="text-xl md:text-2xl font-bold mb-2 text-foreground tracking-tight">
                Inscríbete para acceder al contenido
              </h2>
              <p className="text-muted-foreground mb-6 max-w-md mx-auto text-sm md:text-base">
                Para ver las lecciones, realizar ejercicios y hacer seguimiento de tu progreso,
                primero debes inscribirte en este curso.
              </p>

              {hasAccess ? (
                <Button
                  size="lg"
                  onClick={handleEnroll}
                  disabled={enrolling}
                  className="px-8 bg-primary hover:bg-primary/90 shadow-lg shadow-primary/20"
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
        </motion.div>

        {/* Course preview — locked chapters */}
        <motion.div {...fadeUp(3)} className="space-y-3">
          <h2 className="text-xl md:text-2xl font-bold text-foreground tracking-tight">Vista previa del contenido</h2>
          {chapters.map((chapter, index) => (
            <motion.div key={chapter.id} {...fadeUp(index + 4)}>
              <Card className="opacity-80 border-border bg-card">
                <CardHeader className="bg-secondary/40">
                  <div className="flex items-center justify-between gap-3">
                    <CardTitle className="flex items-center gap-3 min-w-0">
                      <span className="flex items-center justify-center w-10 h-10 rounded-full bg-muted text-muted-foreground border border-border flex-shrink-0" aria-hidden="true">
                        <Lock size={16} />
                      </span>
                      <span className="text-foreground truncate">{chapter.title}</span>
                    </CardTitle>
                    <span className="text-sm text-muted-foreground flex-shrink-0 tabular-nums">
                      {chapter.lessons?.length || 0} lecciones
                    </span>
                  </div>
                  {chapter.description && (
                    <p className="text-sm text-muted-foreground pl-13 mt-1"><InlineMd>{chapter.description}</InlineMd></p>
                  )}
                </CardHeader>
              </Card>
            </motion.div>
          ))}
        </motion.div>
      </div>
    );
  }

  // User is enrolled - show full content
  return (
    <div className="space-y-6 pb-24 lg:pb-8">
      <motion.div {...fadeUp(0)}>
        <Button variant="ghost" onClick={() => navigate('/mis-cursos')} className="text-muted-foreground hover:text-foreground">
          <ArrowLeft size={20} className="mr-2" />
          Volver a Mis Cursos
        </Button>
      </motion.div>

      {/* Course header */}
      <motion.div
        {...fadeUp(1)}
        className="bg-gradient-to-br from-cyan-500 via-cyan-600 to-blue-700 rounded-xl p-6 md:p-8 text-white relative overflow-hidden shadow-xl shadow-cyan-500/20"
      >
        <div className="absolute inset-0 pointer-events-none" aria-hidden="true">
          <div className="absolute -top-20 -right-20 w-64 h-64 bg-white/10 rounded-full blur-3xl" />
          <div className="absolute -bottom-20 -left-20 w-48 h-48 bg-white/5 rounded-full blur-3xl" />
        </div>
        <div className="relative z-10">
          <h1 className="text-3xl md:text-4xl font-bold mb-2 tracking-tight">{course.title}</h1>
          <p className="text-base md:text-lg text-white/85 mb-4"><InlineMd>{course.description}</InlineMd></p>
          <div className="flex items-center gap-2 text-sm flex-wrap mb-6">
            <span className="bg-white/15 backdrop-blur-sm px-3 py-1 rounded-full">{course.level}</span>
            <span className="bg-white/15 backdrop-blur-sm px-3 py-1 rounded-full tabular-nums">
              {chapters.length} capítulos
            </span>
            <span className="bg-white/15 backdrop-blur-sm px-3 py-1 rounded-full tabular-nums">
              {totalLessons} lecciones
            </span>
          </div>

          {/* Progress section */}
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/10">
            <div className="flex items-center justify-between mb-2 gap-2 flex-wrap">
              <span className="font-medium">Tu progreso</span>
              <span className="text-sm text-white/85 tabular-nums">{completedLessons.length}/{totalLessons} lecciones completadas</span>
            </div>
            <Progress
              value={progressPercent}
              className="h-3 bg-white/20"
              aria-label={`${progressPercent}% completado`}
            />

            {nextLesson && (
              <Button
                className="mt-4 bg-white text-cyan-700 hover:bg-cyan-50 font-semibold"
                onClick={() => navigate(`/lesson/${nextLesson.id}`)}
              >
                {completedLessons.length === 0 ? 'Comenzar curso' :
                 progressPercent === 100 ? 'Repasar curso' : 'Continuar'}
                <ChevronRight size={18} className="ml-1" />
              </Button>
            )}
          </div>
        </div>
      </motion.div>

      {/* Course content */}
      <motion.div {...fadeUp(2)} className="space-y-4">
        <h2 className="text-xl md:text-2xl font-bold text-foreground tracking-tight">Contenido del Curso</h2>
        {chapters.length === 0 ? (
          <Card className="border-border bg-card">
            <CardContent className="text-center py-12">
              <BookOpen className="mx-auto mb-4 text-muted-foreground" size={48} aria-hidden="true" />
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
              <motion.div key={chapter.id} {...fadeUp(index + 3)}>
                <Card className="border-border bg-card overflow-hidden">
                  <CardHeader className="bg-secondary/40">
                    <div className="flex items-center justify-between gap-3">
                      <CardTitle className="flex items-center gap-3 min-w-0">
                        <span className={`flex items-center justify-center w-10 h-10 rounded-full font-bold flex-shrink-0 transition-colors ${
                          chapterProgress === 100
                            ? 'bg-emerald-500 text-white'
                            : 'bg-primary text-primary-foreground'
                        }`} aria-hidden="true">
                          {chapterProgress === 100 ? <CheckCircle size={20} /> : index + 1}
                        </span>
                        <span className="text-foreground truncate">{chapter.title}</span>
                      </CardTitle>
                      <span className="text-sm text-muted-foreground flex-shrink-0 tabular-nums">
                        {chapterCompleted}/{chapterLessons.length}
                      </span>
                    </div>
                    {chapter.description && (
                      <p className="text-sm text-muted-foreground pl-13 mt-1"><InlineMd>{chapter.description}</InlineMd></p>
                    )}
                  </CardHeader>
                  <CardContent className="pt-4">
                    {chapterLessons.length === 0 ? (
                      <p className="text-sm text-muted-foreground italic">No hay lecciones disponibles</p>
                    ) : (
                      <ul className="space-y-2">
                        {chapterLessons.map((lesson, lessonIndex) => {
                          const isCompleted = completedLessons.includes(lesson.id);
                          return (
                            <li key={lesson.id}>
                              <button
                                type="button"
                                onClick={() => navigate(`/lesson/${lesson.id}`)}
                                className={`w-full flex items-center justify-between p-3 md:p-4 border rounded-lg transition-all group focus:outline-none focus-visible:ring-2 focus-visible:ring-primary ${
                                  isCompleted
                                    ? 'border-emerald-500/30 bg-emerald-500/10 hover:bg-emerald-500/15'
                                    : 'border-border hover:bg-primary/5 hover:border-primary/40'
                                }`}
                                aria-label={`${isCompleted ? 'Revisar' : 'Comenzar'} lección ${lessonIndex + 1}: ${lesson.title}`}
                              >
                                <div className="flex items-center gap-3 min-w-0">
                                  <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 transition-colors ${
                                    isCompleted
                                      ? 'bg-emerald-500 text-white'
                                      : 'bg-muted text-muted-foreground group-hover:bg-primary group-hover:text-primary-foreground'
                                  }`} aria-hidden="true">
                                    {isCompleted ? <CheckCircle size={16} /> : <Play size={16} />}
                                  </div>
                                  <div className="text-left min-w-0">
                                    <p className={`font-medium truncate transition-colors ${
                                      isCompleted ? 'text-emerald-600 dark:text-emerald-400' : 'text-foreground group-hover:text-primary'
                                    }`}>
                                      {lessonIndex + 1}. {lesson.title}
                                    </p>
                                    <div className="flex items-center gap-2 text-xs text-muted-foreground mt-0.5">
                                      <Clock size={12} aria-hidden="true" />
                                      <span className="tabular-nums">{lesson.duration_minutes} min</span>
                                      {isCompleted && (
                                        <span className="text-emerald-600 dark:text-emerald-400 font-medium ml-1">· Completada</span>
                                      )}
                                    </div>
                                  </div>
                                </div>
                                <ChevronRight size={20} className={`flex-shrink-0 transition-all group-hover:translate-x-0.5 ${
                                  isCompleted ? 'text-emerald-500' : 'text-muted-foreground group-hover:text-primary'
                                }`} aria-hidden="true" />
                              </button>
                            </li>
                          );
                        })}
                      </ul>
                    )}
                  </CardContent>
                </Card>
              </motion.div>
            );
          })
        )}
      </motion.div>
    </div>
  );
};

export default CourseViewer;
