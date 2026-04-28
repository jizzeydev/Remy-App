import { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import {
  AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent,
  AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog';
import { toast } from 'sonner';
import { Trash2, RotateCcw, BookOpen, Layers, FileText, ClipboardList, RefreshCw, AlertTriangle } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const ADMIN_API = `${BACKEND_URL}/api/admin`;

const TYPE_META = {
  course: { label: 'Curso', icon: BookOpen, color: 'bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-200' },
  chapter: { label: 'Capítulo', icon: Layers, color: 'bg-purple-100 text-purple-700 dark:bg-purple-900/40 dark:text-purple-200' },
  lesson: { label: 'Lección', icon: FileText, color: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-200' },
  question: { label: 'Pregunta', icon: ClipboardList, color: 'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-200' },
};

const formatDate = (iso) => {
  if (!iso) return '';
  try {
    const d = new Date(iso);
    return d.toLocaleString('es-CL', { dateStyle: 'medium', timeStyle: 'short' });
  } catch {
    return iso;
  }
};

const childrenSummary = (item) => {
  const c = item.children_summary;
  if (!c) return null;
  if (item.type === 'course') {
    return `${c.chapters || 0} capítulo(s) · ${c.lessons || 0} lección(es)`;
  }
  if (item.type === 'chapter') {
    return `${c.lessons || 0} lección(es)`;
  }
  return null;
};

const AdminTrash = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filterType, setFilterType] = useState('all');

  const authHeader = () => ({ headers: { Authorization: `Bearer ${localStorage.getItem('admin_token')}` } });

  const fetchItems = async () => {
    setLoading(true);
    try {
      const params = filterType !== 'all' ? { type: filterType } : {};
      const res = await axios.get(`${ADMIN_API}/trash`, { ...authHeader(), params });
      setItems(res.data || []);
    } catch (err) {
      toast.error('Error al cargar la papelera');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchItems(); /* eslint-disable-next-line */ }, [filterType]);

  const handleRestore = async (item) => {
    try {
      await axios.post(`${ADMIN_API}/trash/${item.id}/restore`, {}, authHeader());
      toast.success(`${TYPE_META[item.type]?.label || 'Elemento'} restaurado`);
      fetchItems();
    } catch (err) {
      const msg = err?.response?.data?.detail || 'Error al restaurar';
      toast.error(msg);
    }
  };

  const handleDeleteForever = async (item) => {
    try {
      await axios.delete(`${ADMIN_API}/trash/${item.id}`, authHeader());
      toast.success('Elemento eliminado definitivamente');
      fetchItems();
    } catch (err) {
      toast.error(err?.response?.data?.detail || 'Error al eliminar');
    }
  };

  const handleEmpty = async () => {
    try {
      const res = await axios.delete(`${ADMIN_API}/trash`, authHeader());
      toast.success(`Papelera vaciada (${res.data?.deleted || 0} elemento(s))`);
      fetchItems();
    } catch (err) {
      toast.error('Error al vaciar la papelera');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-2">
            <Trash2 className="text-destructive" /> Papelera
          </h1>
          <p className="text-muted-foreground mt-1">
            Cursos, capítulos, lecciones y preguntas eliminados. Restaura o elimina definitivamente.
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={fetchItems} disabled={loading}>
            <RefreshCw size={16} className={`mr-2 ${loading ? 'animate-spin' : ''}`} />
            Refrescar
          </Button>
          <AlertDialog>
            <AlertDialogTrigger asChild>
              <Button variant="destructive" disabled={items.length === 0}>
                <Trash2 size={16} className="mr-2" /> Vaciar papelera
              </Button>
            </AlertDialogTrigger>
            <AlertDialogContent>
              <AlertDialogHeader>
                <AlertDialogTitle className="flex items-center gap-2">
                  <AlertTriangle className="text-destructive" /> Vaciar la papelera
                </AlertDialogTitle>
                <AlertDialogDescription>
                  Se eliminarán <strong>todos</strong> los {items.length} elementos definitivamente. Esta acción no se puede deshacer.
                </AlertDialogDescription>
              </AlertDialogHeader>
              <AlertDialogFooter>
                <AlertDialogCancel>Cancelar</AlertDialogCancel>
                <AlertDialogAction onClick={handleEmpty} className="bg-destructive text-white hover:bg-destructive/90">
                  Sí, vaciar
                </AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <Select value={filterType} onValueChange={setFilterType}>
          <SelectTrigger className="w-56">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Todos los tipos</SelectItem>
            <SelectItem value="course">Cursos</SelectItem>
            <SelectItem value="chapter">Capítulos</SelectItem>
            <SelectItem value="lesson">Lecciones</SelectItem>
            <SelectItem value="question">Preguntas</SelectItem>
          </SelectContent>
        </Select>
        <span className="text-sm text-muted-foreground">{items.length} elemento(s)</span>
      </div>

      {items.length === 0 && !loading && (
        <Card>
          <CardContent className="py-16 text-center text-muted-foreground">
            <Trash2 size={48} className="mx-auto mb-4 opacity-30" />
            <p>La papelera está vacía.</p>
          </CardContent>
        </Card>
      )}

      <div className="space-y-3">
        {items.map((item) => {
          const meta = TYPE_META[item.type] || { label: item.type, icon: FileText, color: '' };
          const Icon = meta.icon;
          const summary = childrenSummary(item);
          return (
            <Card key={item.id}>
              <CardContent className="py-4 flex items-start justify-between gap-4">
                <div className="flex items-start gap-3 flex-1 min-w-0">
                  <div className={`p-2 rounded-md ${meta.color}`}>
                    <Icon size={20} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <Badge variant="outline" className={meta.color}>{meta.label}</Badge>
                      <span className="font-semibold truncate">{item.title || '(sin título)'}</span>
                    </div>
                    <div className="text-xs text-muted-foreground mt-1">
                      Eliminado el {formatDate(item.deleted_at)}
                      {item.deleted_by ? ` por ${item.deleted_by}` : ''}
                    </div>
                    {summary && (
                      <div className="text-xs text-muted-foreground mt-1">Contiene: {summary}</div>
                    )}
                  </div>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  <Button size="sm" variant="outline" onClick={() => handleRestore(item)}>
                    <RotateCcw size={14} className="mr-1" /> Restaurar
                  </Button>
                  <AlertDialog>
                    <AlertDialogTrigger asChild>
                      <Button size="sm" variant="destructive">
                        <Trash2 size={14} className="mr-1" /> Eliminar
                      </Button>
                    </AlertDialogTrigger>
                    <AlertDialogContent>
                      <AlertDialogHeader>
                        <AlertDialogTitle>Eliminar definitivamente</AlertDialogTitle>
                        <AlertDialogDescription>
                          Esto borrará "{item.title}" para siempre. No se podrá restaurar.
                        </AlertDialogDescription>
                      </AlertDialogHeader>
                      <AlertDialogFooter>
                        <AlertDialogCancel>Cancelar</AlertDialogCancel>
                        <AlertDialogAction onClick={() => handleDeleteForever(item)} className="bg-destructive text-white hover:bg-destructive/90">
                          Eliminar
                        </AlertDialogAction>
                      </AlertDialogFooter>
                    </AlertDialogContent>
                  </AlertDialog>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
};

export default AdminTrash;
