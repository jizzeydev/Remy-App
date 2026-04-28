import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter, DialogDescription } from '@/components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import { Badge } from '@/components/ui/badge';
import { toast } from 'sonner';
import { Plus, Edit, Trash2, BookOpen, GraduationCap, Layers, Search, Building2, Copy, Filter } from 'lucide-react';
import InlineMd from '@/components/course/InlineMd';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const ADMIN_API = `${BACKEND_URL}/api/admin`;

const AdminCourses = () => {
  const navigate = useNavigate();
  const [courses, setCourses] = useState([]);
  const [filteredCourses, setFilteredCourses] = useState([]);
  const [coursesStats, setCoursesStats] = useState({});
  const [universities, setUniversities] = useState([]);
  const [loading, setLoading] = useState(false);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingCourse, setEditingCourse] = useState(null);
  
  // Filters
  const [searchTerm, setSearchTerm] = useState('');
  const [filterUniversity, setFilterUniversity] = useState('all');
  
  // Import chapters dialog
  const [importDialogOpen, setImportDialogOpen] = useState(false);
  const [importTargetCourse, setImportTargetCourse] = useState(null);
  const [importSourceCourse, setImportSourceCourse] = useState('');
  const [sourceChapters, setSourceChapters] = useState([]);
  const [selectedChapters, setSelectedChapters] = useState([]);
  const [importing, setImporting] = useState(false);

  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: 'Matemáticas',
    level: 'Intermedio',
    university_id: ''
  });

  useEffect(() => {
    fetchCourses();
    fetchUniversities();
  }, []);

  useEffect(() => {
    // Apply filters
    let filtered = [...courses];
    
    if (searchTerm) {
      filtered = filtered.filter(c => 
        c.title.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    
    if (filterUniversity && filterUniversity !== 'all') {
      if (filterUniversity === 'general') {
        filtered = filtered.filter(c => !c.university_id);
      } else {
        filtered = filtered.filter(c => c.university_id === filterUniversity);
      }
    }
    
    setFilteredCourses(filtered);
  }, [courses, searchTerm, filterUniversity]);

  const fetchUniversities = async () => {
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.get(`${API}/admin/library-universities`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUniversities(response.data);
    } catch (error) {
      console.error('Error fetching universities:', error);
    }
  };

  const fetchCourses = async () => {
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.get(`${ADMIN_API}/courses`, {
        headers: { Authorization: `Bearer ${token}` }
      });
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
        university_id: formData.university_id || null,
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
      university_id: course.university_id || ''
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
      university_id: ''
    });
  };

  // Import chapters functionality
  const openImportDialog = (course) => {
    setImportTargetCourse(course);
    setImportSourceCourse('');
    setSourceChapters([]);
    setSelectedChapters([]);
    setImportDialogOpen(true);
  };

  const handleSourceCourseChange = async (courseId) => {
    setImportSourceCourse(courseId);
    setSelectedChapters([]);
    
    if (!courseId) {
      setSourceChapters([]);
      return;
    }
    
    try {
      const response = await axios.get(`${API}/courses/${courseId}/chapters`);
      setSourceChapters(response.data);
    } catch (error) {
      console.error('Error fetching chapters:', error);
      toast.error('Error al cargar capítulos');
    }
  };

  const toggleChapterSelection = (chapterId) => {
    setSelectedChapters(prev => 
      prev.includes(chapterId) 
        ? prev.filter(id => id !== chapterId)
        : [...prev, chapterId]
    );
  };

  const handleImportChapters = async () => {
    if (selectedChapters.length === 0) {
      toast.error('Selecciona al menos un capítulo');
      return;
    }
    
    setImporting(true);
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.post(
        `${ADMIN_API}/courses/${importTargetCourse.id}/import-chapters`,
        {
          source_course_id: importSourceCourse,
          chapter_ids: selectedChapters,
          include_lessons: true,
          include_questions: true
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      toast.success(`Importados ${response.data.imported.chapters} capítulos, ${response.data.imported.lessons} lecciones y ${response.data.imported.questions} preguntas`);
      setImportDialogOpen(false);
      fetchCourses();
    } catch (error) {
      console.error('Error importing chapters:', error);
      toast.error(error.response?.data?.detail || 'Error al importar capítulos');
    } finally {
      setImporting(false);
    }
  };

  const getUniversityBadge = (course) => {
    if (course.university) {
      if (course.university.short_name === 'GEN') {
        return <Badge variant="secondary" className="text-xs">General</Badge>;
      }
      return (
        <Badge variant="outline" className="text-xs bg-blue-50 text-blue-700 border-blue-200">
          {course.university.short_name}
        </Badge>
      );
    }
    return <Badge variant="secondary" className="text-xs">General</Badge>;
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Gestión de Cursos</h1>
          <p className="text-slate-600 dark:text-slate-400">Administra los cursos disponibles en la plataforma</p>
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
                <Label htmlFor="university">Universidad</Label>
                <Select
                  value={formData.university_id || "general"}
                  onValueChange={(value) => setFormData({ ...formData, university_id: value === "general" ? "" : value })}
                >
                  <SelectTrigger data-testid="course-university-select">
                    <SelectValue placeholder="Seleccionar universidad" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="general">
                      <span className="flex items-center gap-2">
                        <Building2 size={14} />
                        General (Todas las universidades)
                      </span>
                    </SelectItem>
                    {universities.map((uni) => (
                      <SelectItem key={uni.id} value={uni.id}>
                        <span className="flex items-center gap-2">
                          {uni.logo_url && (
                            <img src={uni.logo_url} alt="" className="w-4 h-4 rounded object-cover" />
                          )}
                          {uni.name} ({uni.short_name})
                        </span>
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <p className="text-xs text-slate-500 mt-1">
                  Cursos "General" son plantillas base. Cursos específicos son para una universidad.
                </p>
              </div>
              <Button type="submit" className="w-full" disabled={loading} data-testid="save-course-btn">
                {loading ? 'Guardando...' : editingCourse ? 'Actualizar Curso' : 'Crear Curso'}
              </Button>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-4 items-center">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
          <Input
            placeholder="Buscar cursos..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
            data-testid="course-search-input"
          />
        </div>
        <div className="flex items-center gap-2">
          <Filter size={18} className="text-slate-500" />
          <Select value={filterUniversity} onValueChange={setFilterUniversity}>
            <SelectTrigger className="w-[200px]" data-testid="course-filter-university">
              <SelectValue placeholder="Filtrar por universidad" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todas las universidades</SelectItem>
              <SelectItem value="general">General</SelectItem>
              {universities.map((uni) => (
                <SelectItem key={uni.id} value={uni.id}>
                  {uni.short_name} - {uni.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <div className="text-sm text-slate-500">
          {filteredCourses.length} de {courses.length} cursos
        </div>
      </div>

      {filteredCourses.length === 0 ? (
        <Card className="p-12 text-center">
          <GraduationCap className="mx-auto mb-4 text-slate-400" size={48} />
          <h3 className="text-lg font-medium text-slate-700 dark:text-slate-300 mb-2">
            {courses.length === 0 ? 'No hay cursos creados' : 'No hay cursos que coincidan'}
          </h3>
          <p className="text-slate-500 mb-4">
            {courses.length === 0 
              ? 'Crea tu primer curso para comenzar a agregar contenido'
              : 'Prueba con otros filtros de búsqueda'
            }
          </p>
          {courses.length === 0 && (
            <Button onClick={() => setDialogOpen(true)}>
              <Plus className="mr-2" size={16} />
              Crear Curso
            </Button>
          )}
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredCourses.map((course) => {
            const stats = coursesStats[course.id] || { chapters: 0, lessons: 0 };
            return (
              <Card key={course.id} className="hover:shadow-lg transition-shadow" data-testid={`course-card-${course.id}`}>
                <CardHeader className="pb-3">
                  <div className="flex items-start justify-between gap-2">
                    <CardTitle className="text-lg leading-tight flex-1">{course.title}</CardTitle>
                    {getUniversityBadge(course)}
                  </div>
                  <div className="flex items-center gap-2 mt-2">
                    <span className="px-2 py-1 bg-primary/10 text-primary rounded text-xs font-medium">
                      {course.level}
                    </span>
                    <span className="px-2 py-1 bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 rounded text-xs">
                      {course.category}
                    </span>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-slate-600 dark:text-slate-400 mb-4 line-clamp-2">
                    <InlineMd>{course.description}</InlineMd>
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
                        onClick={() => openImportDialog(course)}
                        className="flex-1"
                        title="Importar capítulos de otro curso"
                        data-testid={`import-chapters-${course.id}`}
                      >
                        <Copy size={14} className="mr-1" />
                        Importar
                      </Button>
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

      {/* Import Chapters Dialog */}
      <Dialog open={importDialogOpen} onOpenChange={setImportDialogOpen}>
        <DialogContent className="max-w-xl">
          <DialogHeader>
            <DialogTitle>Importar Capítulos</DialogTitle>
            <DialogDescription>
              Importa capítulos (con lecciones y preguntas) de otro curso a "{importTargetCourse?.title}"
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-4">
            <div>
              <Label>Curso origen</Label>
              <Select value={importSourceCourse} onValueChange={handleSourceCourseChange}>
                <SelectTrigger>
                  <SelectValue placeholder="Seleccionar curso origen" />
                </SelectTrigger>
                <SelectContent>
                  {courses
                    .filter(c => c.id !== importTargetCourse?.id)
                    .map((course) => (
                      <SelectItem key={course.id} value={course.id}>
                        {course.title} {course.university?.short_name && `(${course.university.short_name})`}
                      </SelectItem>
                    ))
                  }
                </SelectContent>
              </Select>
            </div>
            
            {sourceChapters.length > 0 && (
              <div>
                <Label className="mb-2 block">Capítulos a importar</Label>
                <div className="border rounded-lg max-h-60 overflow-y-auto">
                  {sourceChapters.map((chapter) => (
                    <div 
                      key={chapter.id}
                      className="flex items-center gap-3 p-3 hover:bg-slate-50 dark:hover:bg-slate-800 border-b last:border-0"
                    >
                      <Checkbox
                        id={chapter.id}
                        checked={selectedChapters.includes(chapter.id)}
                        onCheckedChange={() => toggleChapterSelection(chapter.id)}
                      />
                      <label htmlFor={chapter.id} className="flex-1 cursor-pointer">
                        <div className="font-medium">{chapter.title}</div>
                        {chapter.description && (
                          <div className="text-xs text-slate-500 line-clamp-1"><InlineMd>{chapter.description}</InlineMd></div>
                        )}
                      </label>
                    </div>
                  ))}
                </div>
                <p className="text-xs text-slate-500 mt-2">
                  {selectedChapters.length} capítulo(s) seleccionado(s). Se copiarán las lecciones y preguntas asociadas.
                </p>
              </div>
            )}
          </div>
          
          <DialogFooter>
            <Button variant="outline" onClick={() => setImportDialogOpen(false)}>
              Cancelar
            </Button>
            <Button 
              onClick={handleImportChapters} 
              disabled={selectedChapters.length === 0 || importing}
            >
              {importing ? 'Importando...' : `Importar ${selectedChapters.length} capítulo(s)`}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default AdminCourses;
