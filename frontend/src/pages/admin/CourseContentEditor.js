import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { Checkbox } from '@/components/ui/checkbox';
import { toast } from 'sonner';
import InlineMd from '@/components/course/InlineMd';
import { Plus, Edit, Trash2, ArrowLeft, GripVertical, BookOpen, FileText, X, Link2, Unlink, Layers, AlertTriangle } from 'lucide-react';
import BlockEditor from '@/components/admin/BlockEditor';
import BlockRenderer from '@/components/course/BlockRenderer';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const ADMIN_API = `${BACKEND_URL}/api/admin`;

const CourseContentEditor = () => {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const [course, setCourse] = useState(null);
  const [chapters, setChapters] = useState([]);
  const [loading, setLoading] = useState(false);
  const [chapterDialogOpen, setChapterDialogOpen] = useState(false);
  const [lessonDialogOpen, setLessonDialogOpen] = useState(false);
  const [editingChapter, setEditingChapter] = useState(null);
  const [editingLesson, setEditingLesson] = useState(null);
  const [selectedChapter, setSelectedChapter] = useState(null);

  // Link chapters state
  const [linkDialogOpen, setLinkDialogOpen] = useState(false);
  const [templateChapters, setTemplateChapters] = useState([]);
  const [selectedTemplateChapters, setSelectedTemplateChapters] = useState([]);
  const [linking, setLinking] = useState(false);

  const [chapterForm, setChapterForm] = useState({
    title: '',
    description: '',
    order: 1
  });

  const [lessonForm, setLessonForm] = useState({
    title: '',
    blocks: [],
    order: 1,
    duration_minutes: 30
  });

  useEffect(() => {
    fetchCourse();
    fetchChapters();
  }, [courseId]);

  const fetchCourse = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/api/courses/${courseId}`);
      setCourse(response.data);
    } catch (error) {
      console.error('Error fetching course:', error);
      toast.error('Error al cargar curso');
    }
  };

  const fetchChapters = async () => {
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.get(`${ADMIN_API}/courses/${courseId}/chapters`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      // Fetch lessons for each chapter
      const chaptersWithLessons = await Promise.all(
        response.data.map(async (chapter) => {
          const lessonsResponse = await axios.get(`${ADMIN_API}/chapters/${chapter.id}/lessons`, {
            headers: { Authorization: `Bearer ${token}` }
          });
          return { ...chapter, lessons: lessonsResponse.data };
        })
      );
      
      setChapters(chaptersWithLessons);
    } catch (error) {
      console.error('Error fetching chapters:', error);
      toast.error('Error al cargar capítulos');
    }
  };

  const handleSaveChapter = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const token = localStorage.getItem('admin_token');
      const payload = {
        ...chapterForm,
        course_id: courseId,
        id: editingChapter?.id || undefined
      };

      if (editingChapter) {
        await axios.put(`${ADMIN_API}/chapters/${editingChapter.id}`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Capítulo actualizado');
      } else {
        await axios.post(`${ADMIN_API}/chapters`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Capítulo creado');
      }

      fetchChapters();
      setChapterDialogOpen(false);
      resetChapterForm();
    } catch (error) {
      console.error('Error saving chapter:', error);
      toast.error('Error al guardar capítulo');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteChapter = async (chapterId) => {
    if (!window.confirm('¿Eliminar este capítulo y todas sus lecciones?')) return;

    try {
      const token = localStorage.getItem('admin_token');
      await axios.delete(`${ADMIN_API}/chapters/${chapterId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      toast.success('Capítulo eliminado');
      fetchChapters();
    } catch (error) {
      console.error('Error deleting chapter:', error);
      toast.error('Error al eliminar capítulo');
    }
  };

  const handleSaveLesson = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const token = localStorage.getItem('admin_token');
      const payload = {
        ...lessonForm,
        chapter_id: selectedChapter.id,
        id: editingLesson?.id || undefined
      };

      if (editingLesson) {
        await axios.put(`${ADMIN_API}/lessons/${editingLesson.id}`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Lección actualizada');
      } else {
        await axios.post(`${ADMIN_API}/lessons`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Lección creada');
      }

      fetchChapters();
      setLessonDialogOpen(false);
      resetLessonForm();
    } catch (error) {
      console.error('Error saving lesson:', error);
      toast.error('Error al guardar lección');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteLesson = async (lessonId) => {
    if (!window.confirm('¿Eliminar esta lección?')) return;

    try {
      const token = localStorage.getItem('admin_token');
      await axios.delete(`${ADMIN_API}/lessons/${lessonId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      toast.success('Lección eliminada');
      fetchChapters();
    } catch (error) {
      console.error('Error deleting lesson:', error);
      toast.error('Error al eliminar lección');
    }
  };

  const openAddChapter = () => {
    resetChapterForm();
    setChapterDialogOpen(true);
  };

  const openEditChapter = (chapter) => {
    setEditingChapter(chapter);
    setChapterForm({
      title: chapter.title,
      description: chapter.description,
      order: chapter.order
    });
    setChapterDialogOpen(true);
  };

  const openAddLesson = (chapter) => {
    setSelectedChapter(chapter);
    resetLessonForm();
    setLessonDialogOpen(true);
  };

  const openEditLesson = (chapter, lesson) => {
    setSelectedChapter(chapter);
    setEditingLesson(lesson);
    setLessonForm({
      title: lesson.title,
      blocks: Array.isArray(lesson.blocks) ? lesson.blocks : [],
      order: lesson.order,
      duration_minutes: lesson.duration_minutes
    });
    setLessonDialogOpen(true);
  };

  const resetChapterForm = () => {
    setEditingChapter(null);
    setChapterForm({ title: '', description: '', order: chapters.length + 1 });
  };

  const resetLessonForm = () => {
    setEditingLesson(null);
    setLessonForm({ title: '', blocks: [], order: 1, duration_minutes: 30 });
  };

  if (!course) return <div>Cargando...</div>;

  // Check if this is a university course (can link chapters)
  const isUniversityCourse = course.university_id !== null && course.university_id !== undefined;

  // Fetch template chapters when link dialog opens
  const openLinkDialog = async () => {
    setLinkDialogOpen(true);
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.get(`${ADMIN_API}/template-chapters`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setTemplateChapters(response.data);
      setSelectedTemplateChapters([]);
    } catch (error) {
      console.error('Error fetching templates:', error);
      toast.error('Error al cargar plantillas');
    }
  };

  const handleLinkChapters = async () => {
    if (selectedTemplateChapters.length === 0) {
      toast.error('Selecciona al menos un capítulo');
      return;
    }
    
    setLinking(true);
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.post(
        `${ADMIN_API}/courses/${courseId}/link-chapters`,
        { template_chapter_ids: selectedTemplateChapters },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      if (response.data.errors?.length > 0) {
        toast.warning(`Vinculados ${response.data.linked_chapters.length} capítulos. Errores: ${response.data.errors.join(', ')}`);
      } else {
        toast.success(`Vinculados ${response.data.linked_chapters.length} capítulos`);
      }
      
      setLinkDialogOpen(false);
      fetchChapters();
    } catch (error) {
      console.error('Error linking chapters:', error);
      toast.error(error.response?.data?.detail || 'Error al vincular capítulos');
    } finally {
      setLinking(false);
    }
  };

  const handleUnlinkChapter = async (chapterId) => {
    if (!window.confirm('¿Desvincular este capítulo? Se copiará el contenido y será independiente.')) return;
    
    try {
      const token = localStorage.getItem('admin_token');
      await axios.post(
        `${ADMIN_API}/chapters/${chapterId}/unlink`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      toast.success('Capítulo desvinculado. Ahora es independiente.');
      fetchChapters();
    } catch (error) {
      console.error('Error unlinking chapter:', error);
      toast.error(error.response?.data?.detail || 'Error al desvincular');
    }
  };

  const toggleTemplateChapter = (chapterId) => {
    setSelectedTemplateChapters(prev => 
      prev.includes(chapterId)
        ? prev.filter(id => id !== chapterId)
        : [...prev, chapterId]
    );
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" onClick={() => navigate('/admin/courses')}>
          <ArrowLeft size={20} className="mr-2" />
          Volver
        </Button>
        <div className="flex-1">
          <h1 className="text-3xl font-bold">{course.title}</h1>
          <p className="text-slate-600 dark:text-slate-400">
            Editar contenido del curso
            {course.university && course.university.short_name !== 'GEN' && (
              <Badge variant="outline" className="ml-2">{course.university.short_name}</Badge>
            )}
          </p>
        </div>
        <div className="flex gap-2">
          {isUniversityCourse && (
            <Button variant="outline" onClick={openLinkDialog}>
              <Link2 size={20} className="mr-2" />
              Vincular Plantillas
            </Button>
          )}
          <Button onClick={openAddChapter}>
            <Plus size={20} className="mr-2" />
            Nuevo Capítulo
          </Button>
        </div>
      </div>

      {/* Info banner for university courses */}
      {isUniversityCourse && (
        <Card className="bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800">
          <CardContent className="py-3">
            <p className="text-sm text-blue-800 dark:text-blue-200 flex items-center gap-2">
              <Link2 size={16} />
              <span>
                <strong>Curso universitario:</strong> Puedes vincular capítulos de cursos Generales (plantillas). 
                Los cambios en las plantillas se reflejarán automáticamente aquí.
              </span>
            </p>
          </CardContent>
        </Card>
      )}

      <div className="space-y-4">
        {chapters.length === 0 ? (
          <Card>
            <CardContent className="text-center py-12">
              <BookOpen className="mx-auto mb-4 text-slate-400" size={48} />
              <h3 className="text-xl font-semibold mb-2">No hay capítulos</h3>
              <p className="text-slate-500 mb-4">
                {isUniversityCourse 
                  ? 'Vincula capítulos de plantillas o crea uno nuevo'
                  : 'Comienza agregando el primer capítulo'
                }
              </p>
              <div className="flex gap-2 justify-center">
                {isUniversityCourse && (
                  <Button variant="outline" onClick={openLinkDialog}>
                    <Link2 size={16} className="mr-2" />
                    Vincular Plantillas
                  </Button>
                )}
                <Button onClick={openAddChapter}>Crear Capítulo</Button>
              </div>
            </CardContent>
          </Card>
        ) : (
          chapters.map((chapter, chapterIndex) => (
            <Card key={chapter.id} className={chapter.is_linked ? 'border-blue-300 dark:border-blue-700' : ''}>
              <CardHeader className={chapter.is_linked ? 'bg-blue-50 dark:bg-blue-900/20' : 'bg-slate-50 dark:bg-slate-800/50'}>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <GripVertical className="text-slate-400" size={20} />
                    <div>
                      <div className="flex items-center gap-2">
                        <CardTitle className="text-lg">
                          Capítulo {chapter.order}: {chapter.title}
                        </CardTitle>
                        {chapter.is_linked && (
                          <Badge variant="secondary" className="bg-blue-100 text-blue-700 dark:bg-blue-800 dark:text-blue-200">
                            <Link2 size={12} className="mr-1" />
                            Vinculado
                          </Badge>
                        )}
                      </div>
                      <p className="text-sm text-slate-600 dark:text-slate-400 mt-1"><InlineMd>{chapter.description}</InlineMd></p>
                      {chapter.template_info && (
                        <p className="text-xs text-blue-600 dark:text-blue-400 mt-1">
                          Plantilla: {chapter.template_info.course_title}
                        </p>
                      )}
                    </div>
                  </div>
                  <div className="flex gap-2">
                    {!chapter.is_linked && (
                      <>
                        <Button size="sm" variant="outline" onClick={() => openAddLesson(chapter)}>
                          <Plus size={16} className="mr-1" />
                          Lección
                        </Button>
                        <Button size="sm" variant="outline" onClick={() => openEditChapter(chapter)}>
                          <Edit size={16} />
                        </Button>
                      </>
                    )}
                    {chapter.is_linked && (
                      <Button 
                        size="sm" 
                        variant="outline" 
                        onClick={() => handleUnlinkChapter(chapter.id)}
                        title="Desvincular y hacer independiente"
                      >
                        <Unlink size={16} className="mr-1" />
                        Desvincular
                      </Button>
                    )}
                    <Button size="sm" variant="destructive" onClick={() => handleDeleteChapter(chapter.id)}>
                      <Trash2 size={16} />
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="pt-4">
                {chapter.lessons?.length === 0 ? (
                  <div className="text-center py-8 text-slate-500">
                    <FileText className="mx-auto mb-2 text-slate-400" size={32} />
                    <p className="text-sm">No hay lecciones en este capítulo</p>
                  </div>
                ) : (
                  <div className="space-y-2">
                    {chapter.lessons?.map((lesson) => (
                      <div
                        key={lesson.id}
                        className="flex items-center justify-between p-3 border border-slate-200 rounded-lg hover:bg-slate-50"
                      >
                        <div className="flex items-center gap-3">
                          <GripVertical className="text-slate-400" size={16} />
                          <FileText className="text-primary" size={20} />
                          <div>
                            <p className="font-medium">{lesson.title}</p>
                            <p className="text-xs text-slate-500">{lesson.duration_minutes} min</p>
                          </div>
                        </div>
                        <div className="flex gap-2">
                          <Button size="sm" variant="ghost" onClick={() => openEditLesson(chapter, lesson)}>
                            <Edit size={14} />
                          </Button>
                          <Button size="sm" variant="ghost" onClick={() => handleDeleteLesson(lesson.id)}>
                            <Trash2 size={14} />
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          ))
        )}
      </div>

      {/* Chapter Dialog */}
      <Dialog open={chapterDialogOpen} onOpenChange={setChapterDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{editingChapter ? 'Editar Capítulo' : 'Nuevo Capítulo'}</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSaveChapter} className="space-y-4">
            <div>
              <Label>Título</Label>
              <Input
                value={chapterForm.title}
                onChange={(e) => setChapterForm({ ...chapterForm, title: e.target.value })}
                required
              />
            </div>
            <div>
              <Label>Descripción</Label>
              <Textarea
                value={chapterForm.description}
                onChange={(e) => setChapterForm({ ...chapterForm, description: e.target.value })}
                required
              />
            </div>
            <div>
              <Label>Orden</Label>
              <Input
                type="number"
                value={chapterForm.order}
                onChange={(e) => setChapterForm({ ...chapterForm, order: parseInt(e.target.value) })}
                min={1}
                required
              />
            </div>
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? 'Guardando...' : editingChapter ? 'Actualizar' : 'Crear'}
            </Button>
          </form>
        </DialogContent>
      </Dialog>

      {/* Lesson Dialog */}
      <Dialog open={lessonDialogOpen} onOpenChange={setLessonDialogOpen}>
        <DialogContent className="max-h-[90vh] overflow-y-auto max-w-5xl">
          <DialogHeader>
            <DialogTitle>
              {editingLesson ? 'Editar Lección' : 'Nueva Lección'} - {selectedChapter?.title}
            </DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSaveLesson} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label>Título de la Lección</Label>
                <Input
                  value={lessonForm.title}
                  onChange={(e) => setLessonForm({ ...lessonForm, title: e.target.value })}
                  required
                />
              </div>
              <div>
                <Label>Duración (minutos)</Label>
                <Input
                  type="number"
                  value={lessonForm.duration_minutes}
                  onChange={(e) => setLessonForm({ ...lessonForm, duration_minutes: parseInt(e.target.value) })}
                  min={1}
                  required
                />
              </div>
            </div>

            {/* Editor Layout - 2 cols (block editor + preview) */}
            <div className="grid gap-4 grid-cols-1 lg:grid-cols-2">
              {/* Block editor */}
              <div>
                <Label className="mb-2 block">Bloques de la lección</Label>
                <div className="border rounded-lg p-3 max-h-[600px] overflow-y-auto bg-secondary/20">
                  <BlockEditor
                    blocks={lessonForm.blocks}
                    onChange={(blocks) => setLessonForm({ ...lessonForm, blocks })}
                  />
                </div>
              </div>

              {/* Preview */}
              <div>
                <Label className="mb-2 block">Vista previa (alumno)</Label>
                <div className="border rounded-lg p-4 max-h-[600px] overflow-y-auto bg-background">
                  <BlockRenderer blocks={lessonForm.blocks} />
                </div>
              </div>
            </div>

            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? 'Guardando...' : editingLesson ? 'Actualizar Lección' : 'Crear Lección'}
            </Button>
          </form>
        </DialogContent>
      </Dialog>

      {/* Link Chapters Dialog */}
      <Dialog open={linkDialogOpen} onOpenChange={setLinkDialogOpen}>
        <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Link2 size={20} />
              Vincular Capítulos de Plantillas
            </DialogTitle>
            <DialogDescription>
              Selecciona capítulos de cursos Generales para vincularlos a este curso. 
              Los cambios en las plantillas se reflejarán automáticamente.
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-4 mt-4">
            {templateChapters.length === 0 ? (
              <div className="text-center py-8">
                <Layers className="mx-auto mb-4 text-slate-400" size={48} />
                <p className="text-slate-500">No hay capítulos en cursos Generales</p>
                <p className="text-sm text-slate-400">Crea capítulos en cursos sin universidad asignada</p>
              </div>
            ) : (
              templateChapters.map((courseGroup) => (
                <Card key={courseGroup.course.id}>
                  <CardHeader className="py-3">
                    <CardTitle className="text-base flex items-center gap-2">
                      <BookOpen size={16} />
                      {courseGroup.course.title}
                      <Badge variant="secondary" className="text-xs">General</Badge>
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="pt-0">
                    <div className="space-y-2">
                      {courseGroup.chapters.map((chapter) => {
                        const isSelected = selectedTemplateChapters.includes(chapter.id);
                        const isAlreadyLinked = chapters.some(c => c.template_chapter_id === chapter.id);
                        
                        return (
                          <div 
                            key={chapter.id}
                            className={`flex items-center gap-3 p-3 border rounded-lg transition-colors ${
                              isAlreadyLinked 
                                ? 'bg-slate-100 dark:bg-slate-800 opacity-60' 
                                : isSelected 
                                  ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' 
                                  : 'hover:bg-slate-50 dark:hover:bg-slate-800'
                            }`}
                          >
                            <Checkbox
                              id={chapter.id}
                              checked={isSelected}
                              onCheckedChange={() => !isAlreadyLinked && toggleTemplateChapter(chapter.id)}
                              disabled={isAlreadyLinked}
                            />
                            <label htmlFor={chapter.id} className="flex-1 cursor-pointer">
                              <div className="font-medium">{chapter.title}</div>
                              <div className="text-xs text-slate-500 flex gap-3 mt-1">
                                <span>{chapter.lesson_count || 0} lecciones</span>
                                <span>{chapter.question_count || 0} preguntas</span>
                              </div>
                            </label>
                            {isAlreadyLinked && (
                              <Badge variant="secondary" className="text-xs">Ya vinculado</Badge>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </div>
          
          <DialogFooter className="mt-4">
            <Button variant="outline" onClick={() => setLinkDialogOpen(false)}>
              Cancelar
            </Button>
            <Button 
              onClick={handleLinkChapters}
              disabled={selectedTemplateChapters.length === 0 || linking}
            >
              {linking ? 'Vinculando...' : `Vincular ${selectedTemplateChapters.length} capítulo(s)`}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default CourseContentEditor;
