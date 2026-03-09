import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { BookOpen, Loader2, Layers, GraduationCap } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Biblioteca = () => {
  const navigate = useNavigate();
  const [courses, setCourses] = useState([]);
  const [coursesStats, setCoursesStats] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/courses`);
      setCourses(response.data);
      
      // Fetch stats for each course (chapters and lessons count)
      const stats = {};
      for (const course of response.data) {
        try {
          const chaptersRes = await axios.get(`${API}/courses/${course.id}/chapters`);
          const chapters = chaptersRes.data;
          let totalLessons = 0;
          
          for (const chapter of chapters) {
            try {
              const lessonsRes = await axios.get(`${API}/chapters/${chapter.id}/lessons`);
              totalLessons += lessonsRes.data.length;
            } catch (e) {
              console.error('Error fetching lessons:', e);
            }
          }
          
          stats[course.id] = {
            chapters: chapters.length,
            lessons: totalLessons
          };
        } catch (e) {
          stats[course.id] = { chapters: 0, lessons: 0 };
        }
      }
      setCoursesStats(stats);
    } catch (error) {
      console.error('Error fetching courses:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCourseClick = (course) => {
    navigate(`/course/${course.id}`);
  };

  const getLevelColor = (level) => {
    const colors = {
      'Básico': 'bg-green-100 text-green-800',
      'Intermedio': 'bg-blue-100 text-blue-800',
      'Avanzado': 'bg-purple-100 text-purple-800'
    };
    return colors[level] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="space-y-6 pb-24 lg:pb-8" data-testid="biblioteca-page">
      <div>
        <h1 className="text-3xl font-bold">Biblioteca de Cursos</h1>
        <p className="text-slate-600 mt-1">Explora y accede a todos tus cursos</p>
      </div>

      <Tabs defaultValue="all" className="w-full">
        <TabsList className="grid w-full grid-cols-4 max-w-md" data-testid="course-tabs">
          <TabsTrigger value="all">Todos</TabsTrigger>
          <TabsTrigger value="enrolled">Inscritos</TabsTrigger>
          <TabsTrigger value="progress">En progreso</TabsTrigger>
          <TabsTrigger value="completed">Completados</TabsTrigger>
        </TabsList>

        <TabsContent value="all" className="mt-6">
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="animate-spin text-primary" size={32} />
            </div>
          ) : courses.length === 0 ? (
            <Card className="text-center py-12">
              <CardContent>
                <GraduationCap className="mx-auto mb-4 text-slate-400" size={48} />
                <h3 className="text-xl font-semibold mb-2">No hay cursos disponibles</h3>
                <p className="text-slate-500">Los cursos aparecerán aquí cuando estén disponibles</p>
              </CardContent>
            </Card>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {courses.map((course, index) => {
                const stats = coursesStats[course.id] || { chapters: 0, lessons: 0 };
                return (
                  <Card
                    key={course.id}
                    className="cursor-pointer hover:shadow-lg transition-all course-card"
                    onClick={() => handleCourseClick(course)}
                    data-testid={`course-card-${index}`}
                  >
                    <CardHeader>
                      <div className="aspect-video bg-gradient-to-br from-cyan-400 to-cyan-600 rounded-lg mb-4 flex items-center justify-center text-white text-3xl font-bold">
                        {course.title.charAt(0)}
                      </div>
                      <div className="flex items-center justify-between mb-2">
                        <Badge className={getLevelColor(course.level)}>
                          {course.level}
                        </Badge>
                        <div className="flex items-center gap-3 text-sm text-slate-500">
                          <span className="flex items-center gap-1">
                            <Layers size={14} />
                            {stats.chapters}
                          </span>
                          <span className="flex items-center gap-1">
                            <BookOpen size={14} />
                            {stats.lessons}
                          </span>
                        </div>
                      </div>
                      <CardTitle className="text-lg">{course.title}</CardTitle>
                      <CardDescription className="line-clamp-2">
                        {course.description}
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="flex items-center justify-between text-sm mb-3">
                        <span className="text-slate-600">{course.instructor || 'Se Remonta'}</span>
                        <span className="text-xs bg-slate-100 px-2 py-1 rounded">{course.category}</span>
                      </div>
                      <Button
                        className="w-full"
                        onClick={(e) => {
                          e.stopPropagation();
                          navigate(`/course/${course.id}`);
                        }}
                      >
                        Ver Curso
                      </Button>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          )}
        </TabsContent>

        <TabsContent value="enrolled" className="mt-6">
          <Card className="text-center py-12">
            <CardContent>
              <p className="text-slate-500">No hay cursos inscritos aún</p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="progress" className="mt-6">
          <Card className="text-center py-12">
            <CardContent>
              <p className="text-slate-500">No hay cursos en progreso</p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="completed" className="mt-6">
          <Card className="text-center py-12">
            <CardContent>
              <p className="text-slate-500">No hay cursos completados aún</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Biblioteca;
