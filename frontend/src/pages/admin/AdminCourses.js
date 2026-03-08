import { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { toast } from 'sonner';
import { Plus, Edit, Trash2, FileText, Sparkles } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const ADMIN_API = `${BACKEND_URL}/api/admin`;

const AdminCourses = () => {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [pdfDialogOpen, setPdfDialogOpen] = useState(false);
  const [editingCourse, setEditingCourse] = useState(null);
  const [pdfFile, setPdfFile] = useState(null);
  const [pdfText, setPdfText] = useState('');
  const [generatingSummary, setGeneratingSummary] = useState(false);
  const [selectedCourseForSummary, setSelectedCourseForSummary] = useState(null);

  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: 'Matemáticas',
    level: 'Intermedio',
    modules_count: 0,
    instructor: 'Jesus Bravo',
    rating: 4.8,
    summary: ''
  });

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    try {
      const response = await axios.get(`${API}/courses`);
      setCourses(response.data);
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
      const payload = { ...formData, id: editingCourse?.id || undefined };

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
    if (!window.confirm('¿Estás seguro de eliminar este curso?')) return;

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
      category: course.category,
      level: course.level,
      modules_count: course.modules_count,
      instructor: course.instructor,
      rating: course.rating,
      summary: course.summary || ''
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
      modules_count: 0,
      instructor: 'Jesus Bravo',
      rating: 4.8,
      summary: ''
    });
  };

  const handlePdfUpload = async () => {
    if (!pdfFile) {
      toast.error('Por favor selecciona un archivo PDF');
      return;
    }

    try {
      const token = localStorage.getItem('admin_token');
      const formData = new FormData();
      formData.append('file', pdfFile);

      const response = await axios.post(`${ADMIN_API}/upload-pdf`, formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      });

      setPdfText(response.data.text_preview);
      toast.success('PDF procesado exitosamente');
    } catch (error) {
      console.error('Error uploading PDF:', error);
      toast.error('Error al procesar PDF');
    }
  };

  const handleGenerateSummary = async () => {
    if (!pdfText || !selectedCourseForSummary) {
      toast.error('Debes subir un PDF y seleccionar un curso');
      return;
    }

    setGeneratingSummary(true);
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.post(
        `${ADMIN_API}/generate-summary`,
        {
          pdf_content: pdfText,
          course_title: selectedCourseForSummary.title
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      // Actualizar el curso con el resumen generado
      await axios.put(
        `${ADMIN_API}/courses/${selectedCourseForSummary.id}`,
        {
          ...selectedCourseForSummary,
          summary: response.data.summary
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      toast.success('Resumen generado y guardado exitosamente');
      fetchCourses();
      setPdfDialogOpen(false);
      setPdfFile(null);
      setPdfText('');
      setSelectedCourseForSummary(null);
    } catch (error) {
      console.error('Error generating summary:', error);
      toast.error('Error al generar resumen con Gemini');
    } finally {
      setGeneratingSummary(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Gestión de Cursos</h1>
          <p className="text-slate-600">Administra los cursos disponibles en la plataforma</p>
        </div>
        <div className="flex gap-2">
          <Dialog open={pdfDialogOpen} onOpenChange={setPdfDialogOpen}>
            <DialogTrigger asChild>
              <Button variant="outline">
                <Sparkles className="mr-2" size={20} />
                Generar Resumen con IA
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-2xl">
              <DialogHeader>
                <DialogTitle>Generar Resumen con Gemini</DialogTitle>
              </DialogHeader>
              <div className="space-y-4">
                <div>
                  <Label>Seleccionar Curso</Label>
                  <Select
                    value={selectedCourseForSummary?.id}
                    onValueChange={(value) => {
                      const course = courses.find(c => c.id === value);
                      setSelectedCourseForSummary(course);
                    }}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Selecciona un curso" />
                    </SelectTrigger>
                    <SelectContent>
                      {courses.map((course) => (
                        <SelectItem key={course.id} value={course.id}>
                          {course.title}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="pdf-upload">Subir PDF Teórico</Label>
                  <Input
                    id="pdf-upload"
                    type="file"
                    accept=".pdf"
                    onChange={(e) => setPdfFile(e.target.files[0])}
                  />
                  <Button onClick={handlePdfUpload} className="mt-2" size="sm">
                    <FileText className="mr-2" size={16} />
                    Procesar PDF
                  </Button>
                </div>
                {pdfText && (
                  <div>
                    <Label>Vista previa del texto extraído</Label>
                    <Textarea
                      value={pdfText}
                      readOnly
                      className="h-32 text-xs"
                    />
                  </div>
                )}
                <Button
                  onClick={handleGenerateSummary}
                  disabled={!pdfText || !selectedCourseForSummary || generatingSummary}
                  className="w-full"
                >
                  {generatingSummary ? 'Generando con Gemini...' : 'Generar Resumen'}
                </Button>
              </div>
            </DialogContent>
          </Dialog>
          <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
            <DialogTrigger asChild>
              <Button onClick={resetForm}>
                <Plus className="mr-2" size={20} />
                Nuevo Curso
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle>
                  {editingCourse ? 'Editar Curso' : 'Nuevo Curso'}
                </DialogTitle>
              </DialogHeader>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <Label htmlFor="title">Título</Label>
                  <Input
                    id="title"
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="description">Descripción</Label>
                  <Textarea
                    id="description"
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    required
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="category">Categoría</Label>
                    <Input
                      id="category"
                      value={formData.category}
                      onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                    />
                  </div>
                  <div>
                    <Label htmlFor="level">Nivel</Label>
                    <Select
                      value={formData.level}
                      onValueChange={(value) => setFormData({ ...formData, level: value })}
                    >
                      <SelectTrigger>
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
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="modules_count">Número de Módulos</Label>
                    <Input
                      id="modules_count"
                      type="number"
                      value={formData.modules_count}
                      onChange={(e) => setFormData({ ...formData, modules_count: parseInt(e.target.value) })}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="instructor">Instructor</Label>
                    <Input
                      id="instructor"
                      value={formData.instructor}
                      onChange={(e) => setFormData({ ...formData, instructor: e.target.value })}
                    />
                  </div>
                </div>
                <div>
                  <Label htmlFor="summary">Resumen (opcional)</Label>
                  <Textarea
                    id="summary"
                    value={formData.summary}
                    onChange={(e) => setFormData({ ...formData, summary: e.target.value })}
                    placeholder="Puedes agregar un resumen manualmente o generarlo con IA"
                    rows={4}
                  />
                </div>
                <Button type="submit" className="w-full" disabled={loading}>
                  {loading ? 'Guardando...' : editingCourse ? 'Actualizar' : 'Crear'}
                </Button>
              </form>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {courses.map((course) => (
          <Card key={course.id}>
            <CardHeader>
              <CardTitle className="text-lg">{course.title}</CardTitle>
              <div className="flex items-center gap-2 text-sm text-slate-600">
                <span className="px-2 py-1 bg-primary/10 text-primary rounded">
                  {course.level}
                </span>
                <span>{course.modules_count} módulos</span>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-slate-600 mb-4 line-clamp-2">
                {course.description}
              </p>
              {course.summary && (
                <p className="text-xs text-emerald-600 mb-4">
                  ✓ Resumen generado con IA
                </p>
              )}
              <div className="flex gap-2">
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => handleEdit(course)}
                  className="flex-1"
                >
                  <Edit size={16} className="mr-1" />
                  Editar
                </Button>
                <Button
                  size="sm"
                  variant="destructive"
                  onClick={() => handleDelete(course.id)}
                >
                  <Trash2 size={16} />
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default AdminCourses;
