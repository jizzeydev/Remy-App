import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { ArrowLeft, BookOpen, Play, Clock, CheckCircle } from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const CourseViewer = () => {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const [course, setCourse] = useState(null);
  const [chapters, setChapters] = useState([]);
  const [completedLessons, setCompletedLessons] = useState([]);
  const [loading, setLoading] = useState(true);

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
    fetchCourseData();
  }, [courseId]);

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

  if (loading) return <div className="text-center py-12">Cargando...</div>;
  if (!course) return <div className="text-center py-12">Curso no encontrado</div>;

  const nextLesson = findNextLesson();

  return (
    <div className="space-y-6 pb-24 lg:pb-8">
      <Button variant="ghost" onClick={() => navigate('/biblioteca')}>
        <ArrowLeft size={20} className="mr-2" />
        Volver a biblioteca
      </Button>

      {/* Course header */}
      <div className="bg-gradient-to-r from-cyan-500 to-blue-600 rounded-xl p-8 text-white">
        <h1 className="text-4xl font-bold mb-2">{course.title}</h1>
        <p className="text-xl text-cyan-50 mb-4">{course.description}</p>
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
              className="mt-4 bg-white text-cyan-600 hover:bg-cyan-50"
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
        <h2 className="text-2xl font-bold">Contenido del Curso</h2>
        {chapters.length === 0 ? (
          <Card>
            <CardContent className="text-center py-12">
              <BookOpen className="mx-auto mb-4 text-slate-400" size={48} />
              <p className="text-slate-500">Este curso aún no tiene contenido disponible</p>
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
                <CardHeader className="bg-slate-50">
                  <div className="flex items-center justify-between">
                    <CardTitle className="flex items-center gap-3">
                      <span className={`flex items-center justify-center w-10 h-10 rounded-full font-bold ${
                        chapterProgress === 100 
                          ? 'bg-green-500 text-white' 
                          : 'bg-primary text-white'
                      }`}>
                        {chapterProgress === 100 ? <CheckCircle size={20} /> : index + 1}
                      </span>
                      {chapter.title}
                    </CardTitle>
                    <span className="text-sm text-slate-500">
                      {chapterCompleted}/{chapterLessons.length} completadas
                    </span>
                  </div>
                  <p className="text-sm text-slate-600 ml-13">{chapter.description}</p>
                </CardHeader>
                <CardContent className="pt-4">
                  {chapterLessons.length === 0 ? (
                    <p className="text-sm text-slate-500 italic">No hay lecciones disponibles</p>
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
                                ? 'border-green-200 bg-green-50 hover:bg-green-100' 
                                : 'border-slate-200 hover:bg-cyan-50 hover:border-primary'
                            }`}
                          >
                            <div className="flex items-center gap-3">
                              <div className={`w-8 h-8 rounded-full flex items-center justify-center transition-colors ${
                                isCompleted 
                                  ? 'bg-green-500 text-white' 
                                  : 'bg-slate-100 group-hover:bg-primary group-hover:text-white'
                              }`}>
                                {isCompleted ? <CheckCircle size={16} /> : <Play size={16} />}
                              </div>
                              <div className="text-left">
                                <p className={`font-medium transition-colors ${
                                  isCompleted ? 'text-green-700' : 'group-hover:text-primary'
                                }`}>
                                  {lessonIndex + 1}. {lesson.title}
                                </p>
                                <div className="flex items-center gap-2 text-xs text-slate-500 mt-1">
                                  <Clock size={12} />
                                  {lesson.duration_minutes} min
                                  {isCompleted && (
                                    <span className="text-green-600 font-medium ml-2">✓ Completada</span>
                                  )}
                                </div>
                              </div>
                            </div>
                            <ArrowLeft size={20} className={`rotate-180 transition-colors ${
                              isCompleted ? 'text-green-400' : 'text-slate-400 group-hover:text-primary'
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
