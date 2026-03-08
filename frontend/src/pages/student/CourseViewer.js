import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ArrowLeft, BookOpen, Play, Clock } from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const CourseViewer = () => {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const [course, setCourse] = useState(null);
  const [chapters, setChapters] = useState([]);
  const [loading, setLoading] = useState(true);

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
    } catch (error) {
      console.error('Error fetching course:', error);
      toast.error('Error al cargar el curso');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="text-center py-12">Cargando...</div>;
  if (!course) return <div className="text-center py-12">Curso no encontrado</div>;

  return (
    <div className="space-y-6 pb-24 lg:pb-8">
      <Button variant="ghost" onClick={() => navigate('/biblioteca')}>
        <ArrowLeft size={20} className="mr-2" />
        Volver a biblioteca
      </Button>

      <div className="bg-gradient-to-r from-cyan-500 to-blue-600 rounded-xl p-8 text-white">
        {course.cover_image_url && (
          <img
            src={course.cover_image_url}
            alt={course.title}
            className="w-full h-64 object-cover rounded-lg mb-6"
          />
        )}
        <h1 className="text-4xl font-bold mb-2">{course.title}</h1>
        <p className="text-xl text-cyan-50 mb-4">{course.description}</p>
        <div className="flex items-center gap-4 text-sm">
          <span className="bg-white/20 px-3 py-1 rounded-full">{course.level}</span>
          <span className="bg-white/20 px-3 py-1 rounded-full">
            {chapters.length} capítulos
          </span>
          <span className="bg-white/20 px-3 py-1 rounded-full">
            ⭐ {course.rating}
          </span>
        </div>
      </div>

      {course.summary && (
        <Card>
          <CardHeader>
            <CardTitle>Resumen del Curso</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-slate-700 leading-relaxed">{course.summary}</p>
          </CardContent>
        </Card>
      )}

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
          chapters.map((chapter, index) => (
            <Card key={chapter.id}>
              <CardHeader className="bg-slate-50">
                <CardTitle className="flex items-center gap-3">
                  <span className="flex items-center justify-center w-10 h-10 rounded-full bg-primary text-white font-bold">
                    {index + 1}
                  </span>
                  {chapter.title}
                </CardTitle>
                <p className="text-sm text-slate-600 ml-13">{chapter.description}</p>
              </CardHeader>
              <CardContent className="pt-4">
                {chapter.lessons?.length === 0 ? (
                  <p className="text-sm text-slate-500 italic">No hay lecciones disponibles</p>
                ) : (
                  <div className="space-y-2">
                    {chapter.lessons?.map((lesson, lessonIndex) => (
                      <button
                        key={lesson.id}
                        onClick={() => navigate(`/lesson/${lesson.id}`)}
                        className="w-full flex items-center justify-between p-4 border border-slate-200 rounded-lg hover:bg-cyan-50 hover:border-primary transition-all group"
                      >
                        <div className="flex items-center gap-3">
                          <div className="w-8 h-8 rounded-full bg-slate-100 group-hover:bg-primary group-hover:text-white flex items-center justify-center transition-colors">
                            <Play size={16} />
                          </div>
                          <div className="text-left">
                            <p className="font-medium group-hover:text-primary transition-colors">
                              {lessonIndex + 1}. {lesson.title}
                            </p>
                            <div className="flex items-center gap-2 text-xs text-slate-500 mt-1">
                              <Clock size={12} />
                              {lesson.duration_minutes} min
                            </div>
                          </div>
                        </div>
                        <ArrowLeft size={20} className="rotate-180 text-slate-400 group-hover:text-primary transition-colors" />
                      </button>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
};

export default CourseViewer;
