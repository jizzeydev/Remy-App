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
import { Plus, Edit, Trash2 } from 'lucide-react';
import { InlineMath } from 'react-katex';
import 'katex/dist/katex.min.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const ADMIN_API = `${BACKEND_URL}/api/admin`;

const AdminFormulas = () => {
  const [formulas, setFormulas] = useState([]);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingFormula, setEditingFormula] = useState(null);

  const [formData, setFormData] = useState({
    course_id: '',
    topic: '',
    name: '',
    latex: '',
    description: '',
    example: ''
  });

  useEffect(() => {
    fetchFormulas();
    fetchCourses();
  }, []);

  const fetchFormulas = async () => {
    try {
      const response = await axios.post(`${API}/formulas/search`, {
        query: '',
        course_id: null
      });
      setFormulas(response.data);
    } catch (error) {
      console.error('Error fetching formulas:', error);
      toast.error('Error al cargar fórmulas');
    }
  };

  const fetchCourses = async () => {
    try {
      const response = await axios.get(`${API}/courses`);
      setCourses(response.data);
    } catch (error) {
      console.error('Error fetching courses:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const token = localStorage.getItem('admin_token');
      const payload = { ...formData, id: editingFormula?.id || undefined };

      if (editingFormula) {
        await axios.put(`${ADMIN_API}/formulas/${editingFormula.id}`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Fórmula actualizada exitosamente');
      } else {
        await axios.post(`${ADMIN_API}/formulas`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Fórmula creada exitosamente');
      }

      fetchFormulas();
      setDialogOpen(false);
      resetForm();
    } catch (error) {
      console.error('Error saving formula:', error);
      toast.error('Error al guardar fórmula');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (formulaId) => {
    if (!window.confirm('¿Estás seguro de eliminar esta fórmula?')) return;

    try {
      const token = localStorage.getItem('admin_token');
      await axios.delete(`${ADMIN_API}/formulas/${formulaId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      toast.success('Fórmula eliminada exitosamente');
      fetchFormulas();
    } catch (error) {
      console.error('Error deleting formula:', error);
      toast.error('Error al eliminar fórmula');
    }
  };

  const handleEdit = (formula) => {
    setEditingFormula(formula);
    setFormData({
      course_id: formula.course_id,
      topic: formula.topic,
      name: formula.name,
      latex: formula.latex,
      description: formula.description,
      example: formula.example || ''
    });
    setDialogOpen(true);
  };

  const resetForm = () => {
    setEditingFormula(null);
    setFormData({
      course_id: '',
      topic: '',
      name: '',
      latex: '',
      description: '',
      example: ''
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Gestión de Fórmulas</h1>
          <p className="text-slate-600">Administra las fórmulas matemáticas con LaTeX</p>
        </div>
        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogTrigger asChild>
            <Button onClick={resetForm}>
              <Plus className="mr-2" size={20} />
              Nueva Fórmula
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>
                {editingFormula ? 'Editar Fórmula' : 'Nueva Fórmula'}
              </DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label htmlFor="course_id">Curso</Label>
                <Select
                  value={formData.course_id}
                  onValueChange={(value) => setFormData({ ...formData, course_id: value })}
                  required
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
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="topic">Tema</Label>
                  <Input
                    id="topic"
                    value={formData.topic}
                    onChange={(e) => setFormData({ ...formData, topic: e.target.value })}
                    placeholder="Ej: Derivadas"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="name">Nombre</Label>
                  <Input
                    id="name"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    placeholder="Ej: Regla de la potencia"
                    required
                  />
                </div>
              </div>
              <div>
                <Label htmlFor="latex">Fórmula (LaTeX)</Label>
                <Input
                  id="latex"
                  value={formData.latex}
                  onChange={(e) => setFormData({ ...formData, latex: e.target.value })}
                  placeholder="Ej: d/dx(x^n) = n·x^(n-1)"
                  required
                />
                {formData.latex && (
                  <div className="mt-2 p-3 bg-slate-50 rounded border border-slate-200">
                    <p className="text-xs text-slate-600 mb-1">Vista previa:</p>
                    <div className="text-lg">
                      <InlineMath math={formData.latex} />
                    </div>
                  </div>
                )}
              </div>
              <div>
                <Label htmlFor="description">Descripción</Label>
                <Textarea
                  id="description"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  placeholder="Explicación de la fórmula"
                  required
                />
              </div>
              <div>
                <Label htmlFor="example">Ejemplo (opcional)</Label>
                <Textarea
                  id="example"
                  value={formData.example}
                  onChange={(e) => setFormData({ ...formData, example: e.target.value })}
                  placeholder="Ej: d/dx(x³) = 3x²"
                />
              </div>
              <Button type="submit" className="w-full" disabled={loading}>
                {loading ? 'Guardando...' : editingFormula ? 'Actualizar' : 'Crear'}
              </Button>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {formulas.map((formula) => (
          <Card key={formula.id}>
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <CardTitle className="text-lg">{formula.name}</CardTitle>
                  <p className="text-sm text-slate-600 mt-1">{formula.topic}</p>
                </div>
                <span className="text-xs bg-primary/10 text-primary px-2 py-1 rounded">
                  {courses.find(c => c.id === formula.course_id)?.title.split(' ')[0] || 'General'}
                </span>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="bg-slate-50 border border-slate-200 rounded-lg p-3 text-center">
                  <InlineMath math={formula.latex} />
                </div>
                <p className="text-sm text-slate-600">{formula.description}</p>
                {formula.example && (
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                    <p className="text-xs font-semibold text-blue-900 mb-1">Ejemplo:</p>
                    <p className="text-sm text-blue-800">{formula.example}</p>
                  </div>
                )}
                <div className="flex gap-2 pt-2">
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => handleEdit(formula)}
                    className="flex-1"
                  >
                    <Edit size={16} className="mr-1" />
                    Editar
                  </Button>
                  <Button
                    size="sm"
                    variant="destructive"
                    onClick={() => handleDelete(formula.id)}
                  >
                    <Trash2 size={16} />
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default AdminFormulas;
