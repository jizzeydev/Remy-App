import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Switch } from '@/components/ui/switch';
import { Badge } from '@/components/ui/badge';
import { toast } from 'sonner';
import { Plus, Edit, Trash2, Building2, Upload, Loader2, BookOpen } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AdminLibraryUniversities = () => {
  const [universities, setUniversities] = useState([]);
  const [courseCounts, setCourseCounts] = useState({});
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingUniversity, setEditingUniversity] = useState(null);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef(null);

  const [formData, setFormData] = useState({
    name: '',
    short_name: '',
    logo_url: ''
  });

  useEffect(() => {
    fetchUniversities();
  }, []);

  const fetchUniversities = async () => {
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.get(`${API}/admin/library-universities`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUniversities(response.data);
      
      // Fetch course counts
      const coursesRes = await axios.get(`${API}/admin/courses`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      const counts = {};
      for (const course of coursesRes.data) {
        const uniId = course.university_id || 'general';
        counts[uniId] = (counts[uniId] || 0) + 1;
      }
      setCourseCounts(counts);
    } catch (error) {
      console.error('Error fetching universities:', error);
      toast.error('Error al cargar universidades');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.name || !formData.short_name) {
      toast.error('Nombre y sigla son requeridos');
      return;
    }

    try {
      const token = localStorage.getItem('admin_token');
      
      if (editingUniversity) {
        await axios.put(
          `${API}/admin/library-universities/${editingUniversity.id}`,
          formData,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        toast.success('Universidad actualizada');
      } else {
        await axios.post(
          `${API}/admin/library-universities`,
          formData,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        toast.success('Universidad creada');
      }

      fetchUniversities();
      setDialogOpen(false);
      resetForm();
    } catch (error) {
      console.error('Error saving university:', error);
      toast.error(error.response?.data?.detail || 'Error al guardar universidad');
    }
  };

  const handleDelete = async (university) => {
    const courseCount = courseCounts[university.id] || 0;
    
    if (courseCount > 0) {
      toast.error(`No se puede eliminar: ${courseCount} curso(s) usan esta universidad`);
      return;
    }
    
    if (!window.confirm(`¿Eliminar "${university.name}"?`)) return;

    try {
      const token = localStorage.getItem('admin_token');
      await axios.delete(`${API}/admin/library-universities/${university.id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      toast.success('Universidad eliminada');
      fetchUniversities();
    } catch (error) {
      console.error('Error deleting university:', error);
      toast.error(error.response?.data?.detail || 'Error al eliminar universidad');
    }
  };

  const handleEdit = (university) => {
    setEditingUniversity(university);
    setFormData({
      name: university.name,
      short_name: university.short_name,
      logo_url: university.logo_url || ''
    });
    setDialogOpen(true);
  };

  const resetForm = () => {
    setEditingUniversity(null);
    setFormData({
      name: '',
      short_name: '',
      logo_url: ''
    });
  };

  const handleLogoUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
      toast.error('Solo se permiten imágenes');
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      toast.error('La imagen no debe superar 5MB');
      return;
    }

    setUploading(true);
    try {
      const token = localStorage.getItem('admin_token');
      const uploadFormData = new FormData();
      uploadFormData.append('image', file);
      uploadFormData.append('folder', 'universities');

      const response = await axios.post(
        `${API}/images/upload`,
        uploadFormData,
        { 
          headers: { 
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          } 
        }
      );

      setFormData(prev => ({ ...prev, logo_url: response.data.url }));
      toast.success('Logo subido');
    } catch (error) {
      console.error('Error uploading logo:', error);
      toast.error('Error al subir logo');
    } finally {
      setUploading(false);
    }
  };

  const toggleActive = async (university) => {
    try {
      const token = localStorage.getItem('admin_token');
      await axios.put(
        `${API}/admin/library-universities/${university.id}`,
        { is_active: !university.is_active },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      toast.success(university.is_active ? 'Universidad desactivada' : 'Universidad activada');
      fetchUniversities();
    } catch (error) {
      console.error('Error toggling university:', error);
      toast.error('Error al cambiar estado');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="animate-spin" size={32} />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Universidades</h1>
          <p className="text-slate-600 dark:text-slate-400">
            Gestiona las universidades para categorizar cursos
          </p>
        </div>
        <Button onClick={() => { resetForm(); setDialogOpen(true); }} data-testid="new-university-btn">
          <Plus className="mr-2" size={20} />
          Nueva Universidad
        </Button>
      </div>

      {/* Stats Card */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-4">
            <div className="p-3 bg-primary/10 rounded-lg">
              <Building2 className="text-primary" size={24} />
            </div>
            <div>
              <div className="text-2xl font-bold">{universities.length}</div>
              <div className="text-sm text-slate-500">Universidades</div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-4">
            <div className="p-3 bg-green-100 dark:bg-green-900/30 rounded-lg">
              <Building2 className="text-green-600" size={24} />
            </div>
            <div>
              <div className="text-2xl font-bold">
                {universities.filter(u => u.is_active).length}
              </div>
              <div className="text-sm text-slate-500">Activas</div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-4">
            <div className="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
              <BookOpen className="text-blue-600" size={24} />
            </div>
            <div>
              <div className="text-2xl font-bold">{courseCounts['general'] || 0}</div>
              <div className="text-sm text-slate-500">Cursos Generales</div>
            </div>
          </CardContent>
        </Card>
      </div>

      {universities.length === 0 ? (
        <Card className="p-12 text-center">
          <Building2 className="mx-auto mb-4 text-slate-400" size={48} />
          <h3 className="text-lg font-medium mb-2">No hay universidades</h3>
          <p className="text-slate-500 mb-4">Crea universidades para categorizar tus cursos</p>
          <Button onClick={() => setDialogOpen(true)}>
            <Plus className="mr-2" size={16} />
            Crear Universidad
          </Button>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {universities.map((university) => {
            const courseCount = courseCounts[university.id] || 0;
            return (
              <Card 
                key={university.id} 
                className={`transition-all ${!university.is_active ? 'opacity-60' : ''}`}
                data-testid={`university-card-${university.id}`}
              >
                <CardHeader className="pb-3">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-3">
                      {university.logo_url ? (
                        <img 
                          src={university.logo_url} 
                          alt={university.name}
                          className="w-12 h-12 rounded-lg object-cover border"
                        />
                      ) : (
                        <div className="w-12 h-12 rounded-lg bg-slate-100 dark:bg-slate-700 flex items-center justify-center">
                          <Building2 className="text-slate-400" size={24} />
                        </div>
                      )}
                      <div>
                        <CardTitle className="text-lg">{university.name}</CardTitle>
                        <Badge variant="outline" className="mt-1">{university.short_name}</Badge>
                      </div>
                    </div>
                    <Switch
                      checked={university.is_active}
                      onCheckedChange={() => toggleActive(university)}
                      data-testid={`toggle-active-${university.id}`}
                    />
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center gap-2 text-sm text-slate-500 mb-4">
                    <BookOpen size={16} />
                    <span>{courseCount} curso(s)</span>
                  </div>
                  
                  <div className="flex gap-2">
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleEdit(university)}
                      className="flex-1"
                      data-testid={`edit-university-${university.id}`}
                    >
                      <Edit size={14} className="mr-1" />
                      Editar
                    </Button>
                    <Button
                      size="sm"
                      variant="destructive"
                      onClick={() => handleDelete(university)}
                      disabled={courseCount > 0}
                      title={courseCount > 0 ? 'No se puede eliminar: tiene cursos asociados' : 'Eliminar'}
                      data-testid={`delete-university-${university.id}`}
                    >
                      <Trash2 size={14} />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}

      {/* Create/Edit Dialog */}
      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle>
              {editingUniversity ? 'Editar Universidad' : 'Nueva Universidad'}
            </DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Label htmlFor="name">Nombre *</Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder="Ej: Pontificia Universidad Católica de Chile"
                required
                data-testid="university-name-input"
              />
            </div>
            <div>
              <Label htmlFor="short_name">Sigla *</Label>
              <Input
                id="short_name"
                value={formData.short_name}
                onChange={(e) => setFormData({ ...formData, short_name: e.target.value.toUpperCase() })}
                placeholder="Ej: PUC"
                maxLength={10}
                required
                data-testid="university-shortname-input"
              />
              <p className="text-xs text-slate-500 mt-1">Máximo 10 caracteres</p>
            </div>
            <div>
              <Label>Logo</Label>
              <div className="flex items-center gap-4 mt-2">
                {formData.logo_url ? (
                  <img 
                    src={formData.logo_url} 
                    alt="Preview"
                    className="w-16 h-16 rounded-lg object-cover border"
                  />
                ) : (
                  <div className="w-16 h-16 rounded-lg bg-slate-100 dark:bg-slate-700 flex items-center justify-center">
                    <Building2 className="text-slate-400" size={24} />
                  </div>
                )}
                <div className="flex-1">
                  <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleLogoUpload}
                    accept="image/*"
                    className="hidden"
                  />
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    onClick={() => fileInputRef.current?.click()}
                    disabled={uploading}
                    className="w-full"
                  >
                    {uploading ? (
                      <>
                        <Loader2 className="animate-spin mr-2" size={14} />
                        Subiendo...
                      </>
                    ) : (
                      <>
                        <Upload size={14} className="mr-2" />
                        Subir Logo
                      </>
                    )}
                  </Button>
                  {formData.logo_url && (
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      onClick={() => setFormData({ ...formData, logo_url: '' })}
                      className="w-full mt-1 text-red-600"
                    >
                      Quitar logo
                    </Button>
                  )}
                </div>
              </div>
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setDialogOpen(false)}>
                Cancelar
              </Button>
              <Button type="submit" data-testid="save-university-btn">
                {editingUniversity ? 'Actualizar' : 'Crear'}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default AdminLibraryUniversities;
