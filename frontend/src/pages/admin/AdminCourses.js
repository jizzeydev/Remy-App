import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { toast } from 'sonner';
import { Plus, Edit, Trash2, BookOpen, GraduationCap, Layers } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const ADMIN_API = `${BACKEND_URL}/api/admin`;

const AdminCourses = () => {
  const navigate = useNavigate();
  const [courses, setCourses] = useState([]);
  const [coursesStats, setCoursesStats] = useState({}); // {courseId: {chapters, lessons}}
  const [loading, setLoading] = useState(false);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingCourse, setEditingCourse] = useState(null);

  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: 'Matemáticas',
    level: 'Intermedio',
    instructor: 'Jesus Bravo'
  });

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    try {
      const response = await axios.get(`${API}/courses`);
      setCourses(response.data);
      
      // Fetch stats for each course
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
      toast.error('Error al cargar cursos');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const token = localStorage.getItem('admin_token');
      const payload = { 
        ...formData, 
        id: editingCourse?.id || undefined,
        // Keep these fields for backwards compatibility but with defaults
        modules_count: 0,
        rating: 4.8
      };

      if (editingCourse) {
        await axios.put(`${ADMIN_API}/courses/${editingCourse.id}`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Curso actualizado exitosamente');
      } else {
        await axios.post(`${ADMIN_API}/courses`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Curso creado exitosamente');
      }

      fetchCourses();
      setDialogOpen(false);
      resetForm();
    } catch (error) {
      console.error('Error saving course:', error);
      toast.error('Error al guardar curso');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (courseId) => {
    if (!window.confirm('¿Estás seguro de eliminar este curso? Se eliminarán todos sus capítulos y lecciones.')) return;

    try {
      const token = localStorage.getItem('admin_token');
      await axios.delete(`${ADMIN_API}/courses/${courseId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      toast.success('Curso eliminado exitosamente');
      fetchCourses();
    } catch (error) {
      console.error('Error deleting course:', error);
      toast.error('Error al eliminar curso');
    }
  };

  const handleEdit = (course) => {
    setEditingCourse(course);
    setFormData({
      title: course.title,
      description: course.description,
      category: course.category || 'Matemáticas',
      level: course.level || 'Intermedio',
      instructor: course.instructor || 'Jesus Bravo'
    });
    setDialogOpen(true);
  };

  const resetForm = () => {
    setEditingCourse(null);
    setFormData({
      title: '',
      description: '',
      category: 'Matemáticas',
      level: 'Intermedio',
      instructor: 'Jesus Bravo'
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Gestión de Cursos</h1>
          <p className="text-slate-600">Administra los cursos disponibles en la plataforma</p>
        </div>
        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogTrigger asChild>
            <Button onClick={resetForm} data-testid="new-course-btn">
              <Plus className="mr-2" size={20} />
              Nuevo Curso
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-lg">
            <DialogHeader>
              <DialogTitle>
                {editingCourse ? 'Editar Curso' : 'Nuevo Curso'}
              </DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label htmlFor="title">Título del Curso *</Label>
                <Input
                  id="title"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  placeholder="Ej: Cálculo Diferencial"
                  required
                  data-testid="course-title-input"
                />
              </div>
              <div>
                <Label htmlFor="description">Descripción *</Label>
                <Textarea
                  id="description"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  placeholder="Breve descripción del contenido del curso"
                  rows={3}
                  required
                  data-testid="course-description-input"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="category">Categoría</Label>
                  <Input
                    id="category"
                    value={formData.category}
                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                    placeholder="Ej: Matemáticas"
                    data-testid="course-category-input"
                  />
                </div>
                <div>
                  <Label htmlFor="level">Nivel</Label>
                  <Select
                    value={formData.level}
                    onValueChange={(value) => setFormData({ ...formData, level: value })}
                  >
                    <SelectTrigger data-testid="course-level-select">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Básico">Básico</SelectItem>
                      <SelectItem value="Intermedio">Intermedio</SelectItem>
                      <SelectItem value="Avanzado">Avanzado</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <div>
                <Label htmlFor="instructor">Instructor</Label>
                <Input
                  id="instructor"
                  value={formData.instructor}
                  onChange={(e) => setFormData({ ...formData, instructor: e.target.value })}
                  placeholder="Nombre del instructor"
                  data-testid="course-instructor-input"
                />
              </div>
              <Button type="submit" className="w-full" disabled={loading} data-testid="save-course-btn">
                {loading ? 'Guardando...' : editingCourse ? 'Actualizar Curso' : 'Crear Curso'}
              </Button>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {courses.length === 0 ? (
        <Card className="p-12 text-center">
          <GraduationCap className="mx-auto mb-4 text-slate-400" size={48} />
          <h3 className="text-lg font-medium text-slate-700 mb-2">No hay cursos creados</h3>
          <p className="text-slate-500 mb-4">Crea tu primer curso para comenzar a agregar contenido</p>
          <Button onClick={() => setDialogOpen(true)}>
            <Plus className="mr-2" size={16} />
            Crear Curso
          </Button>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses.map((course) => {
            const stats = coursesStats[course.id] || { chapters: 0, lessons: 0 };
            return (
              <Card key={course.id} className="hover:shadow-lg transition-shadow" data-testid={`course-card-${course.id}`}>
                <CardHeader className="pb-3">
                  <CardTitle className="text-lg leading-tight">{course.title}</CardTitle>
                  <div className="flex items-center gap-2 mt-2">
                    <span className="px-2 py-1 bg-primary/10 text-primary rounded text-xs font-medium">
                      {course.level}
                    </span>
                    <span className="px-2 py-1 bg-slate-100 text-slate-600 rounded text-xs">
                      {course.category}
                    </span>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-slate-600 mb-4 line-clamp-2">
                    {course.description}
                  </p>
                  
                  {/* Stats */}
                  <div className="flex items-center gap-4 mb-4 text-sm text-slate-500">
                    <div className="flex items-center gap-1">
                      <Layers size={14} />
                      <span>{stats.chapters} capítulos</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <BookOpen size={14} />
                      <span>{stats.lessons} lecciones</span>
                    </div>
                  </div>
                  
                  <div className="flex flex-col gap-2">
                    <Button
                      size="sm"
                      onClick={() => navigate(`/admin/courses/${course.id}/content`)}
                      className="w-full"
                      data-testid={`edit-content-${course.id}`}
                    >
                      <BookOpen size={16} className="mr-2" />
                      Editar Contenido
                    </Button>
                    <div className="flex gap-2">
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => handleEdit(course)}
                        className="flex-1"
                        data-testid={`edit-course-${course.id}`}
                      >
                        <Edit size={14} className="mr-1" />
                        Editar
                      </Button>
                      <Button
                        size="sm"
                        variant="destructive"
                        onClick={() => handleDelete(course.id)}
                        data-testid={`delete-course-${course.id}`}
                      >
                        <Trash2 size={14} />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default AdminCourses;
