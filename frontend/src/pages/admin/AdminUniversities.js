import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import {
  Building2, Plus, Edit, Trash2, ChevronRight,
  BookOpen, ClipboardList, GraduationCap, Search,
  Loader2
} from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/admin/universities`;

const AdminUniversities = () => {
  const navigate = useNavigate();
  const [universities, setUniversities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  
  // Dialog states
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [editingUniversity, setEditingUniversity] = useState(null);
  const [saving, setSaving] = useState(false);
  
  // Form state
  const [formData, setFormData] = useState({
    name: '',
    short_name: ''
  });

  useEffect(() => {
    fetchUniversities();
  }, []);

  const fetchUniversities = async () => {
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.get(API, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUniversities(response.data);
    } catch (error) {
      console.error('Error fetching universities:', error);
      toast.error('Error al cargar universidades');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    if (!formData.name.trim()) {
      toast.error('El nombre es requerido');
      return;
    }
    
    setSaving(true);
    try {
      const token = localStorage.getItem('admin_token');
      await axios.post(API, formData, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      toast.success('Universidad creada');
      setShowCreateDialog(false);
      resetForm();
      fetchUniversities();
    } catch (error) {
      toast.error('Error al crear universidad');
    } finally {
      setSaving(false);
    }
  };

  const handleUpdate = async () => {
    if (!formData.name.trim()) {
      toast.error('El nombre es requerido');
      return;
    }
    
    setSaving(true);
    try {
      const token = localStorage.getItem('admin_token');
      await axios.put(`${API}/${editingUniversity.id}`, formData, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      toast.success('Universidad actualizada');
      setEditingUniversity(null);
      resetForm();
      fetchUniversities();
    } catch (error) {
      toast.error('Error al actualizar universidad');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (university) => {
    if (!window.confirm(`¿Eliminar ${university.name}? Esto eliminará todos los cursos, evaluaciones y preguntas asociadas.`)) {
      return;
    }
    
    try {
      const token = localStorage.getItem('admin_token');
      await axios.delete(`${API}/${university.id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      toast.success('Universidad eliminada');
      fetchUniversities();
    } catch (error) {
      toast.error('Error al eliminar universidad');
    }
  };

  const openEditDialog = (university) => {
    setFormData({
      name: university.name,
      short_name: university.short_name || ''
    });
    setEditingUniversity(university);
  };

  const resetForm = () => {
    setFormData({
      name: '',
      short_name: ''
    });
  };

  const filteredUniversities = universities.filter(uni =>
    uni.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    (uni.short_name && uni.short_name.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="animate-spin text-cyan-500" size={32} />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3">
            <Building2 className="text-cyan-500" />
            Universidades
          </h1>
          <p className="text-slate-500 mt-1">
            Gestiona universidades, cursos y evaluaciones
          </p>
        </div>
        <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
          <DialogTrigger asChild>
            <Button className="bg-cyan-500 hover:bg-cyan-400">
              <Plus size={18} className="mr-2" />
              Nueva Universidad
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Crear Universidad</DialogTitle>
              <DialogDescription>
                Agrega una nueva universidad para crear evaluaciones específicas
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4 py-4">
              <div>
                <Label>Nombre *</Label>
                <Input
                  placeholder="Universidad de Chile"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                />
              </div>
              <div>
                <Label>Sigla</Label>
                <Input
                  placeholder="UCH"
                  value={formData.short_name}
                  onChange={(e) => setFormData({...formData, short_name: e.target.value})}
                />
              </div>
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setShowCreateDialog(false)}>
                Cancelar
              </Button>
              <Button onClick={handleCreate} disabled={saving}>
                {saving ? 'Creando...' : 'Crear Universidad'}
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>

      {/* Search */}
      <div className="relative max-w-md">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
        <Input
          className="pl-10"
          placeholder="Buscar universidad..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      {/* Universities Grid */}
      {filteredUniversities.length === 0 ? (
        <Card className="text-center py-12">
          <CardContent>
            <Building2 className="mx-auto mb-4 text-slate-400" size={48} />
            <h3 className="text-xl font-semibold mb-2">No hay universidades</h3>
            <p className="text-slate-500 mb-4">
              Crea tu primera universidad para comenzar a agregar evaluaciones
            </p>
            <Button onClick={() => setShowCreateDialog(true)}>
              <Plus size={18} className="mr-2" />
              Crear Universidad
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredUniversities.map((university) => (
            <Card 
              key={university.id} 
              className="hover:shadow-lg transition-all cursor-pointer group"
              onClick={() => navigate(`/admin/universities/${university.id}`)}
            >
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 bg-gradient-to-br from-cyan-400 to-blue-600 rounded-lg flex items-center justify-center text-white font-bold text-lg">
                      {university.short_name ? university.short_name.substring(0,2) : university.name.charAt(0)}
                    </div>
                    <div>
                      <CardTitle className="text-lg">{university.name}</CardTitle>
                      {university.short_name && (
                        <Badge variant="outline" className="mt-1">{university.short_name}</Badge>
                      )}
                    </div>
                  </div>
                  <ChevronRight className="text-slate-400 group-hover:text-cyan-500 transition-colors" size={20} />
                </div>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-4 text-sm text-slate-600">
                  <div className="flex items-center gap-1">
                    <BookOpen size={14} className="text-cyan-500" />
                    {university.courses_count || 0} cursos
                  </div>
                </div>
                
                <div className="flex gap-2 mt-4 pt-4 border-t" onClick={(e) => e.stopPropagation()}>
                  <Button 
                    variant="outline" 
                    size="sm"
                    onClick={(e) => {
                      e.stopPropagation();
                      openEditDialog(university);
                    }}
                  >
                    <Edit size={14} className="mr-1" />
                    Editar
                  </Button>
                  <Button 
                    variant="outline" 
                    size="sm"
                    className="text-red-600 hover:text-red-700 hover:bg-red-50"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDelete(university);
                    }}
                  >
                    <Trash2 size={14} className="mr-1" />
                    Eliminar
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Edit Dialog */}
      <Dialog open={!!editingUniversity} onOpenChange={() => setEditingUniversity(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Editar Universidad</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div>
              <Label>Nombre *</Label>
              <Input
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
              />
            </div>
            <div>
              <Label>Sigla</Label>
              <Input
                value={formData.short_name}
                onChange={(e) => setFormData({...formData, short_name: e.target.value})}
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setEditingUniversity(null)}>
              Cancelar
            </Button>
            <Button onClick={handleUpdate} disabled={saving}>
              {saving ? 'Guardando...' : 'Guardar Cambios'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default AdminUniversities;
