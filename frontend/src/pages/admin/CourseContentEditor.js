import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { toast } from 'sonner';
import { Plus, Edit, Trash2, ArrowLeft, GripVertical, BookOpen, FileText, Sparkles } from 'lucide-react';
import MarkdownRenderer from '@/components/course/MarkdownRenderer';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
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
  const [pdfFile, setPdfFile] = useState(null);
  const [pdfText, setPdfText] = useState('');
  const [generatingContent, setGeneratingContent] = useState(false);

  const [chapterForm, setChapterForm] = useState({
    title: '',
    description: '',
    order: 1
  });

  const [lessonForm, setLessonForm] = useState({
    title: '',
    content: '',
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

  const handlePdfUpload = async () => {
    if (!pdfFile) {
      toast.error('Selecciona un PDF');
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
      toast.success('PDF procesado');
    } catch (error) {
      console.error('Error uploading PDF:', error);
      toast.error('Error al procesar PDF');
    }
  };

  const handleGenerateContent = async () => {
    if (!pdfText || !lessonForm.title) {
      toast.error('Debes subir un PDF y especificar título de lección');
      return;
    }

    setGeneratingContent(true);
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.post(
        `${ADMIN_API}/generate-lesson-content`,
        {
          pdf_content: pdfText,
          lesson_title: lessonForm.title,
          chapter_title: selectedChapter.title
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      setLessonForm({ ...lessonForm, content: response.data.content });
      toast.success('Contenido generado con Gemini');
    } catch (error) {
      console.error('Error generating content:', error);
      toast.error('Error al generar contenido');
    } finally {
      setGeneratingContent(false);
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
      content: lesson.content,
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
    setPdfFile(null);
    setPdfText('');
    setLessonForm({ title: '', content: '', order: 1, duration_minutes: 30 });
  };

  if (!course) return <div>Cargando...</div>;

  return (
    <div className=\"space-y-6\">
      <div className=\"flex items-center gap-4\">
        <Button variant=\"ghost\" onClick={() => navigate('/admin/courses')}>
          <ArrowLeft size={20} className=\"mr-2\" />
          Volver
        </Button>
        <div className=\"flex-1\">
          <h1 className=\"text-3xl font-bold\">{course.title}</h1>
          <p className=\"text-slate-600\">Editar contenido del curso</p>
        </div>
        <Button onClick={openAddChapter}>
          <Plus size={20} className=\"mr-2\" />
          Nuevo Capítulo
        </Button>
      </div>

      <div className=\"space-y-4\">
        {chapters.length === 0 ? (
          <Card>
            <CardContent className=\"text-center py-12\">
              <BookOpen className=\"mx-auto mb-4 text-slate-400\" size={48} />
              <h3 className=\"text-xl font-semibold mb-2\">No hay capítulos</h3>
              <p className=\"text-slate-500 mb-4\">Comienza agregando el primer capítulo</p>
              <Button onClick={openAddChapter}>Crear Capítulo</Button>
            </CardContent>
          </Card>
        ) : (
          chapters.map((chapter, chapterIndex) => (
            <Card key={chapter.id}>
              <CardHeader className=\"bg-slate-50\">
                <div className=\"flex items-center justify-between\">
                  <div className=\"flex items-center gap-3\">
                    <GripVertical className=\"text-slate-400\" size={20} />
                    <div>
                      <CardTitle className=\"text-lg\">
                        Capítulo {chapter.order}: {chapter.title}
                      </CardTitle>
                      <p className=\"text-sm text-slate-600 mt-1\">{chapter.description}</p>
                    </div>
                  </div>
                  <div className=\"flex gap-2\">
                    <Button size=\"sm\" variant=\"outline\" onClick={() => openAddLesson(chapter)}>
                      <Plus size={16} className=\"mr-1\" />
                      Lección
                    </Button>
                    <Button size=\"sm\" variant=\"outline\" onClick={() => openEditChapter(chapter)}>
                      <Edit size={16} />
                    </Button>
                    <Button size=\"sm\" variant=\"destructive\" onClick={() => handleDeleteChapter(chapter.id)}>
                      <Trash2 size={16} />
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent className=\"pt-4\">
                {chapter.lessons?.length === 0 ? (
                  <div className=\"text-center py-8 text-slate-500\">
                    <FileText className=\"mx-auto mb-2 text-slate-400\" size={32} />
                    <p className=\"text-sm\">No hay lecciones en este capítulo</p>
                  </div>
                ) : (
                  <div className=\"space-y-2\">
                    {chapter.lessons?.map((lesson) => (
                      <div
                        key={lesson.id}
                        className=\"flex items-center justify-between p-3 border border-slate-200 rounded-lg hover:bg-slate-50\"
                      >
                        <div className=\"flex items-center gap-3\">
                          <GripVertical className=\"text-slate-400\" size={16} />
                          <FileText className=\"text-primary\" size={20} />
                          <div>
                            <p className=\"font-medium\">{lesson.title}</p>
                            <p className=\"text-xs text-slate-500\">{lesson.duration_minutes} min</p>
                          </div>
                        </div>
                        <div className=\"flex gap-2\">
                          <Button size=\"sm\" variant=\"ghost\" onClick={() => openEditLesson(chapter, lesson)}>
                            <Edit size={14} />
                          </Button>
                          <Button size=\"sm\" variant=\"ghost\" onClick={() => handleDeleteLesson(lesson.id)}>
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
          <form onSubmit={handleSaveChapter} className=\"space-y-4\">
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
                type=\"number\"
                value={chapterForm.order}
                onChange={(e) => setChapterForm({ ...chapterForm, order: parseInt(e.target.value) })}
                min={1}
                required
              />
            </div>
            <Button type=\"submit\" className=\"w-full\" disabled={loading}>
              {loading ? 'Guardando...' : editingChapter ? 'Actualizar' : 'Crear'}
            </Button>
          </form>
        </DialogContent>
      </Dialog>

      {/* Lesson Dialog */}
      <Dialog open={lessonDialogOpen} onOpenChange={setLessonDialogOpen}>
        <DialogContent className=\"max-w-5xl max-h-[90vh] overflow-y-auto\">
          <DialogHeader>
            <DialogTitle>
              {editingLesson ? 'Editar Lección' : 'Nueva Lección'} - {selectedChapter?.title}
            </DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSaveLesson} className=\"space-y-4\">
            <div className=\"grid grid-cols-2 gap-4\">
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
                  type=\"number\"
                  value={lessonForm.duration_minutes}
                  onChange={(e) => setLessonForm({ ...lessonForm, duration_minutes: parseInt(e.target.value) })}
                  min={1}
                  required
                />
              </div>
            </div>

            <div className=\"border-t pt-4\">
              <Label className=\"flex items-center gap-2 mb-2\">
                <Sparkles size={16} className=\"text-primary\" />
                Generar contenido con IA (opcional)
              </Label>
              <div className=\"space-y-2\">
                <Input
                  type=\"file\"
                  accept=\".pdf\"
                  onChange={(e) => setPdfFile(e.target.files[0])}
                />
                <div className=\"flex gap-2\">
                  <Button type=\"button\" onClick={handlePdfUpload} size=\"sm\" variant=\"outline\" disabled={!pdfFile}>
                    Procesar PDF
                  </Button>
                  <Button
                    type=\"button\"
                    onClick={handleGenerateContent}
                    size=\"sm\"
                    disabled={!pdfText || generatingContent}
                  >
                    {generatingContent ? 'Generando...' : 'Generar con Gemini'}
                  </Button>
                </div>
              </div>
            </div>

            <div className=\"grid grid-cols-2 gap-4\">
              <div>
                <Label>Contenido (Markdown + LaTeX)</Label>
                <Textarea
                  value={lessonForm.content}
                  onChange={(e) => setLessonForm({ ...lessonForm, content: e.target.value })}
                  placeholder=\"# Título\n\n## Sección\n\nTexto con fórmulas $$x^2$$\n\n[DESMOS:y=x^2]\"
                  className=\"font-mono text-sm\"
                  rows={20}
                  required
                />
              </div>
              <div>
                <Label>Vista Previa</Label>
                <div className=\"border rounded-lg p-4 h-[500px] overflow-y-auto bg-white\">
                  <MarkdownRenderer content={lessonForm.content} />
                </div>
              </div>
            </div>

            <Button type=\"submit\" className=\"w-full\" disabled={loading}>
              {loading ? 'Guardando...' : editingLesson ? 'Actualizar Lección' : 'Crear Lección'}
            </Button>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default CourseContentEditor;
