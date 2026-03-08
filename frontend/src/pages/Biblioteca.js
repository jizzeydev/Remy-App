import { useState, useEffect } from 'react';
import axios from 'axios';
import { BookOpen, Loader2, Play, FileText } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Biblioteca = () => {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [materials, setMaterials] = useState([]);

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/courses`);
      setCourses(response.data);
    } catch (error) {
      console.error('Error fetching courses:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchMaterials = async (courseId) => {
    try {
      const response = await axios.get(`${API}/materials/${courseId}`);
      setMaterials(response.data);
    } catch (error) {
      console.error('Error fetching materials:', error);
      setMaterials([]);
    }
  };

  const handleCourseClick = (course) => {
    setSelectedCourse(course);
    fetchMaterials(course.id);
  };

  const getLevelColor = (level) => {
    const colors = {
      'Básico': 'bg-green-100 text-green-800',
      'Intermedio': 'bg-blue-100 text-blue-800',
      'Avanzado': 'bg-purple-100 text-purple-800'
    };
    return colors[level] || 'bg-gray-100 text-gray-800';
  };

  if (selectedCourse) {
    return (
      <div className="space-y-6 pb-24 lg:pb-8" data-testid="course-detail-view">
        <Button
          variant="ghost"
          onClick={() => {
            setSelectedCourse(null);
            setMaterials([]);
          }}
          data-testid="back-to-courses-button"
        >
          ← Volver a cursos
        </Button>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <div className="aspect-video bg-gradient-to-br from-cyan-400 to-cyan-600 rounded-lg mb-4 flex items-center justify-center text-white text-4xl font-bold">
                  {selectedCourse.title.charAt(0)}
                </div>
                <CardTitle>{selectedCourse.title}</CardTitle>
                <CardDescription>{selectedCourse.description}</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-600">Nivel</span>
                  <Badge className={getLevelColor(selectedCourse.level)}>
                    {selectedCourse.level}
                  </Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-600">Módulos</span>
                  <span className="font-semibold">{selectedCourse.modules_count}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-600">Instructor</span>
                  <span className="font-semibold">{selectedCourse.instructor}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-600">Rating</span>
                  <span className="font-semibold">⭐ {selectedCourse.rating}</span>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle>Materiales del curso</CardTitle>
                <CardDescription>
                  {materials.length} materiales disponibles
                </CardDescription>
              </CardHeader>
              <CardContent>
                {materials.length === 0 ? (
                  <div className="text-center py-12">
                    <FileText className="mx-auto mb-4 text-slate-400" size={48} />
                    <p className="text-slate-500">No hay materiales disponibles aún</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {materials.map((material, index) => (
                      <div
                        key={material.id}
                        className="flex items-center justify-between p-4 border border-slate-100 rounded-lg hover:bg-secondary transition-colors"
                        data-testid={`material-item-${index}`}
                      >
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 bg-cyan-100 rounded-lg flex items-center justify-center">
                            {material.type === 'video' ? (
                              <Play className="text-cyan-600" size={20} />
                            ) : (
                              <FileText className="text-cyan-600" size={20} />
                            )}
                          </div>
                          <div>
                            <h4 className="font-semibold">{material.title}</h4>
                            <p className="text-sm text-slate-500">{material.type}</p>
                          </div>
                        </div>
                        <Button size="sm" variant="outline" data-testid={`view-material-${index}`}>
                          Ver
                        </Button>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    );
  }

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
                <BookOpen className="mx-auto mb-4 text-slate-400" size={48} />
                <h3 className="text-xl font-semibold mb-2">No hay cursos disponibles</h3>
                <p className="text-slate-500">Los cursos aparecerán aquí cuando estén disponibles</p>
              </CardContent>
            </Card>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {courses.map((course, index) => (
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
                      <span className="text-sm text-slate-500">
                        {course.modules_count} módulos
                      </span>
                    </div>
                    <CardTitle className="text-lg">{course.title}</CardTitle>
                    <CardDescription className="line-clamp-2">
                      {course.description}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="flex items-center justify-between text-sm mb-3">
                      <span className="text-slate-600">{course.instructor}</span>
                      <span className="font-semibold">⭐ {course.rating}</span>
                    </div>
                    <Button
                      className="w-full"
                      onClick={() => navigate(`/course/${course.id}`)}
                    >
                      Ver Curso
                    </Button>
                  </CardContent>
                </Card>
              ))}
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
