import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ArrowLeft, ArrowRight, Clock, BookOpen, CheckCircle } from 'lucide-react';
import { toast } from 'sonner';
import MarkdownRenderer from '@/components/course/MarkdownRenderer';

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
        toast.success('🎉 ¡Felicidades! Has completado el curso');
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

  if (loading) return <div className="text-center py-12">Cargando...</div>;
  if (!lesson) return <div className="text-center py-12">Lección no encontrada</div>;

  const isLastLesson = currentIndex === allLessons.length - 1;
  const isFirstLesson = currentIndex === 0;

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-24 lg:pb-8">
      {/* Navigation header */}
      <div className="flex items-center justify-between">
        <Button variant="ghost" onClick={() => course ? navigate(`/course/${course.id}`) : navigate(-1)}>
          <ArrowLeft size={20} className="mr-2" />
          Volver al curso
        </Button>
        
        {allLessons.length > 0 && (
          <span className="text-sm text-slate-500">
            Lección {currentIndex + 1} de {allLessons.length}
          </span>
        )}
      </div>

      {/* Lesson content */}
      <Card>
        <CardContent className="pt-6">
          <div className="mb-6">
            {chapter && (
              <div className="flex items-center gap-2 text-sm text-cyan-600 mb-2">
                <BookOpen size={16} />
                <span>{chapter.title}</span>
              </div>
            )}
            <h1 className="text-3xl font-bold mb-3">{lesson.title}</h1>
            <div className="flex items-center gap-2 text-sm text-slate-600">
              <Clock size={16} />
              <span>{lesson.duration_minutes} minutos</span>
            </div>
          </div>

          <div className="prose prose-slate max-w-none">
            <MarkdownRenderer content={lesson.content} />
          </div>
        </CardContent>
      </Card>

      {/* Navigation footer */}
      <Card className="bg-slate-50">
        <CardContent className="py-4">
          <div className="flex items-center justify-between">
            <Button
              variant="outline"
              onClick={handlePreviousLesson}
              disabled={isFirstLesson}
              className="gap-2"
            >
              <ArrowLeft size={18} />
              Anterior
            </Button>

            <Button
              onClick={handleNextLesson}
              disabled={markingComplete}
              className="gap-2 bg-cyan-500 hover:bg-cyan-600"
              size="lg"
            >
              {markingComplete ? (
                <>
                  <div className="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full" />
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
          
          {/* Progress hint */}
          <p className="text-center text-xs text-slate-500 mt-3">
            {isLastLesson 
              ? 'Esta es la última lección del curso' 
              : `Siguiente: ${allLessons[currentIndex + 1]?.title || ''}`
            }
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

export default LessonViewer;
