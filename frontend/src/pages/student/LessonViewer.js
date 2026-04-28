import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import axios from 'axios';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { ArrowLeft, ArrowRight, Clock, BookOpen, CheckCircle, Lock, Loader2 } from 'lucide-react';
import { toast } from 'sonner';
import BlockRenderer from '@/components/course/BlockRenderer';
import InlineMd from '@/components/course/InlineMd';

const fadeUp = (i = 0) => ({
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.4, delay: i * 0.05, ease: [0.22, 1, 0.36, 1] }
});

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const LessonViewer = () => {
  const { lessonId } = useParams();
  const navigate = useNavigate();
  const [lesson, setLesson] = useState(null);
  const [chapter, setChapter] = useState(null);
  const [course, setCourse] = useState(null);
  const [allLessons, setAllLessons] = useState([]); // All lessons in order
  const [currentIndex, setCurrentIndex] = useState(-1);
  const [loading, setLoading] = useState(true);
  const [markingComplete, setMarkingComplete] = useState(false);
  const [isEnrolled, setIsEnrolled] = useState(false);
  const [checkingEnrollment, setCheckingEnrollment] = useState(true);

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
    fetchLessonData();
  }, [lessonId]);

  const fetchLessonData = async () => {
    setLoading(true);
    setCheckingEnrollment(true);
    try {
      // Fetch the lesson
      const lessonRes = await axios.get(`${API}/lessons/${lessonId}`);
      const lessonData = lessonRes.data;
      setLesson(lessonData);

      // Fetch the chapter
      const chapterId = lessonData.chapter_id;
      if (chapterId) {
        // We need to find the course by iterating through courses
        const coursesRes = await axios.get(`${API}/courses`);
        
        for (const c of coursesRes.data) {
          const chaptersRes = await axios.get(`${API}/courses/${c.id}/chapters`);
          const foundChapter = chaptersRes.data.find(ch => ch.id === chapterId);
          
          if (foundChapter) {
            setChapter(foundChapter);
            setCourse(c);
            
            // Check enrollment for this course
            const token = localStorage.getItem('remy_session_token');
            if (token) {
              try {
                const enrollmentRes = await axios.get(`${API}/enrollments/check/${c.id}`, {
                  headers: { Authorization: `Bearer ${token}` }
                });
                setIsEnrolled(enrollmentRes.data.enrolled);
              } catch (e) {
                setIsEnrolled(false);
              }
            } else {
              setIsEnrolled(false);
            }
            
            // Build ordered list of all lessons in this course
            const orderedLessons = [];
            for (const ch of chaptersRes.data) {
              const lessonsRes = await axios.get(`${API}/chapters/${ch.id}/lessons`);
              lessonsRes.data.forEach(l => {
                orderedLessons.push({
                  ...l,
                  chapterId: ch.id,
                  chapterTitle: ch.title
                });
              });
            }
            
            setAllLessons(orderedLessons);
            const idx = orderedLessons.findIndex(l => l.id === lessonId);
            setCurrentIndex(idx);
            break;
          }
        }
      }
    } catch (error) {
      console.error('Error fetching lesson:', error);
      toast.error('Error al cargar la lección');
    } finally {
      setLoading(false);
      setCheckingEnrollment(false);
    }
  };

  const handleNextLesson = async () => {
    if (currentIndex < 0 || !course) return;

    setMarkingComplete(true);
    
    try {
      const studentId = getStudentId();
      
      // Mark current lesson as complete
      await axios.post(`${API}/progress/complete-lesson`, {
        student_id: studentId,
        course_id: course.id,
        lesson_id: lessonId
      });
      
      toast.success('¡Lección completada!');
      
      // Navigate to next lesson if available
      if (currentIndex < allLessons.length - 1) {
        const nextLesson = allLessons[currentIndex + 1];
        navigate(`/lesson/${nextLesson.id}`);
      } else {
        // Course completed!
        toast.success('¡Felicidades! Has completado el curso');
        navigate(`/course/${course.id}`);
      }
    } catch (error) {
      console.error('Error marking lesson complete:', error);
      // Still navigate even if progress fails
      if (currentIndex < allLessons.length - 1) {
        navigate(`/lesson/${allLessons[currentIndex + 1].id}`);
      } else {
        navigate(`/course/${course.id}`);
      }
    } finally {
      setMarkingComplete(false);
    }
  };

  const handlePreviousLesson = () => {
    if (currentIndex > 0) {
      navigate(`/lesson/${allLessons[currentIndex - 1].id}`);
    }
  };

  if (loading || checkingEnrollment) {
    return (
      <div className="flex items-center justify-center py-12" role="status" aria-live="polite">
        <Loader2 className="animate-spin text-primary" size={32} />
        <span className="sr-only">Cargando lección</span>
      </div>
    );
  }
  if (!lesson) return <div className="text-center py-12 text-muted-foreground">Lección no encontrada</div>;

  // If not enrolled, redirect to course page
  if (!isEnrolled && course) {
    return (
      <div className="max-w-2xl mx-auto text-center py-12">
        <motion.div {...fadeUp(0)}>
          <Card className="p-8 border-border bg-card">
            <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-primary/15 ring-1 ring-primary/30 flex items-center justify-center">
              <Lock className="text-primary" size={28} aria-hidden="true" />
            </div>
            <h2 className="text-2xl font-bold mb-2 text-foreground tracking-tight">Acceso restringido</h2>
            <p className="text-muted-foreground mb-6">
              Debes estar inscrito en el curso para acceder a esta lección.
            </p>
            <Button onClick={() => navigate(`/course/${course.id}`)} className="bg-primary hover:bg-primary/90">
              Ver curso e inscribirme
            </Button>
          </Card>
        </motion.div>
      </div>
    );
  }

  const isLastLesson = currentIndex === allLessons.length - 1;
  const isFirstLesson = currentIndex === 0;
  const lessonProgress = allLessons.length > 0 ? ((currentIndex + 1) / allLessons.length) * 100 : 0;

  return (
    <div className="max-w-4xl mx-auto space-y-5 pb-24 lg:pb-8">
      {/* Navigation header + progress */}
      <motion.div {...fadeUp(0)} className="space-y-3">
        <div className="flex items-center justify-between gap-3 flex-wrap">
          <Button
            variant="ghost"
            onClick={() => course ? navigate(`/course/${course.id}`) : navigate(-1)}
            className="text-muted-foreground hover:text-foreground -ml-2"
          >
            <ArrowLeft size={20} className="mr-2" />
            Volver al curso
          </Button>

          {allLessons.length > 0 && (
            <span className="text-sm text-muted-foreground tabular-nums">
              Lección {currentIndex + 1} de {allLessons.length}
            </span>
          )}
        </div>

        {allLessons.length > 0 && (
          <Progress
            value={lessonProgress}
            className="h-1"
            aria-label={`Progreso del curso: lección ${currentIndex + 1} de ${allLessons.length}`}
          />
        )}
      </motion.div>

      {/* Lesson content */}
      <motion.div {...fadeUp(1)}>
        <Card className="border-border bg-card">
          <CardContent className="pt-6 md:pt-8 px-5 md:px-8 pb-8">
            <div className="mb-6 pb-6 border-b border-border">
              {chapter && (
                <div className="flex items-center gap-2 text-sm text-primary mb-2 font-medium">
                  <BookOpen size={16} aria-hidden="true" />
                  <span>{chapter.title}</span>
                </div>
              )}
              <h1 className="text-2xl md:text-3xl font-bold mb-3 text-foreground tracking-tight leading-tight">
                <InlineMd>{lesson.title}</InlineMd>
              </h1>
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Clock size={16} aria-hidden="true" />
                <span className="tabular-nums">{lesson.duration_minutes} minutos</span>
              </div>
            </div>

            <BlockRenderer blocks={lesson.blocks || []} />
          </CardContent>
        </Card>
      </motion.div>

      {/* Navigation footer */}
      <motion.div {...fadeUp(2)}>
        <Card className="bg-secondary/40 border-border">
          <CardContent className="py-4 px-4 md:px-6">
            <div className="flex items-center justify-between gap-3">
              <Button
                variant="outline"
                onClick={handlePreviousLesson}
                disabled={isFirstLesson}
                className="gap-2"
              >
                <ArrowLeft size={18} />
                <span className="hidden sm:inline">Anterior</span>
              </Button>

              <Button
                onClick={handleNextLesson}
                disabled={markingComplete}
                className="gap-2 bg-primary hover:bg-primary/90 shadow-md shadow-primary/20"
                size="lg"
              >
                {markingComplete ? (
                  <>
                    <Loader2 size={18} className="animate-spin" />
                    Guardando...
                  </>
                ) : isLastLesson ? (
                  <>
                    <CheckCircle size={18} />
                    Finalizar Curso
                  </>
                ) : (
                  <>
                    Siguiente Lección
                    <ArrowRight size={18} />
                  </>
                )}
              </Button>
            </div>

            <p className="text-center text-xs text-muted-foreground mt-3 truncate">
              {isLastLesson
                ? 'Esta es la última lección del curso'
                : <>Siguiente: <span className="text-foreground font-medium">{allLessons[currentIndex + 1]?.title || ''}</span></>
              }
            </p>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
};

export default LessonViewer;
