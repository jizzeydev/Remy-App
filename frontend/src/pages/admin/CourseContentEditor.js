import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { toast } from 'sonner';
import { Plus, Edit, Trash2, ArrowLeft, GripVertical, BookOpen, FileText, Sparkles, Send, MessageSquare, X, Image, Upload, Wand2, Check } from 'lucide-react';
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
  const [topicPrompt, setTopicPrompt] = useState(''); // NEW: topic prompt for generation
  const [generationMode, setGenerationMode] = useState('prompt'); // 'prompt' or 'document'
  
  // AI Chat state
  const [chatOpen, setChatOpen] = useState(false);
  const [chatMessage, setChatMessage] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const chatEndRef = useRef(null);
  
  // Image insertion state
  const [imageDialogOpen, setImageDialogOpen] = useState(false);
  const [imagePrompt, setImagePrompt] = useState('');
  const [imageStyle, setImageStyle] = useState('educativo');
  const [generatingImage, setGeneratingImage] = useState(false);
  const [uploadingImage, setUploadingImage] = useState(false);
  const fileInputRef = useRef(null);

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

      // Use full text for generation, not just preview
      setPdfText(response.data.text || response.data.text_preview);
      toast.success(`PDF procesado: ${response.data.text_length} caracteres extraídos`);
    } catch (error) {
      console.error('Error uploading PDF:', error);
      toast.error('Error al procesar PDF');
    }
  };

  const handleGenerateContent = async () => {
    if (!lessonForm.title) {
      toast.error('Especifica el título de la lección');
      return;
    }

    // Validate based on mode
    if (generationMode === 'document' && !pdfText) {
      toast.error('Procesa un PDF primero');
      return;
    }
    if (generationMode === 'prompt' && !topicPrompt.trim()) {
      toast.error('Escribe un tema o instrucciones para generar');
      return;
    }

    setGeneratingContent(true);
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.post(
        `${ADMIN_API}/generate-lesson-content`,
        {
          pdf_content: generationMode === 'document' ? pdfText : null,
          topic_prompt: generationMode === 'prompt' ? topicPrompt : null,
          lesson_title: lessonForm.title,
          chapter_title: selectedChapter?.title || '',
          course_title: course?.title || ''
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      setLessonForm({ ...lessonForm, content: response.data.content });
      toast.success('¡Contenido generado con GPT-5.2!');
    } catch (error) {
      console.error('Error generating content:', error);
      toast.error('Error al generar contenido');
    } finally {
      setGeneratingContent(false);
    }
  };

  // AI Chat functions
  const handleSendChatMessage = async () => {
    if (!chatMessage.trim() || !lessonForm.content) return;
    
    const userMsg = chatMessage.trim();
    setChatMessage('');
    setChatHistory(prev => [...prev, { role: 'user', content: userMsg }]);
    setChatLoading(true);
    
    try {
      const token = localStorage.getItem('admin_token');
      
      // Get chapter title for context
      const currentChapter = chapters.find(ch => ch.id === selectedChapter);
      const chapterTitle = currentChapter?.title || '';
      
      const response = await axios.post(
        `${ADMIN_API}/edit-lesson-content`,
        {
          current_content: lessonForm.content,
          user_instruction: userMsg,
          lesson_title: lessonForm.title,
          chapter_title: chapterTitle
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      setLessonForm({ ...lessonForm, content: response.data.content });
      setChatHistory(prev => [...prev, { 
        role: 'assistant', 
        content: '✅ ¡Listo! He actualizado el contenido. Revisa la vista previa para ver los cambios.' 
      }]);
      toast.success('Contenido actualizado');
    } catch (error) {
      console.error('Error editing content:', error);
      setChatHistory(prev => [...prev, { 
        role: 'assistant', 
        content: '❌ Hubo un error. Intenta ser más específico en tu instrucción.' 
      }]);
      toast.error('Error al editar contenido');
    } finally {
      setChatLoading(false);
      setTimeout(() => chatEndRef.current?.scrollIntoView({ behavior: 'smooth' }), 100);
    }
  };

  const openChatEditor = () => {
    setChatOpen(true);
    setChatHistory([{
      role: 'assistant',
      content: `¡Hola! Soy Remy 🎓

Estoy listo para mejorar la lección "${lessonForm.title}".

**Puedo ayudarte a:**
• Agregar ejemplos más claros
• Mejorar explicaciones confusas
• Añadir gráficos Desmos interactivos
• Quitar contenido innecesario
• Agregar tips para el examen

**Ejemplos de instrucciones:**
"Agrega un ejemplo paso a paso de cómo derivar x³"
"Mejora la explicación del límite, está confusa"
"Pon un Desmos donde se vea la tangente moviéndose"
"Quita el segundo ejemplo y pon uno más fácil"`
    }]);
  };

  // Image functions
  const handleGenerateImage = async () => {
    if (!imagePrompt.trim()) {
      toast.error('Escribe una descripción para la imagen');
      return;
    }
    
    setGeneratingImage(true);
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.post(
        `${ADMIN_API}/generate-image`,
        { prompt: imagePrompt, style: imageStyle },
        { headers: { Authorization: `Bearer ${token}` }, timeout: 120000 }
      );
      
      // The API returns a path like /api/uploads/xxx.png
      // We need to prepend the base URL for the markdown
      const imageUrl = response.data.image_url;
      const fullUrl = imageUrl.startsWith('/api') 
        ? `${process.env.REACT_APP_BACKEND_URL}${imageUrl}`
        : imageUrl;
      
      const imageMarkdown = `\n\n![${imagePrompt}](${fullUrl})\n\n`;
      setLessonForm({ ...lessonForm, content: lessonForm.content + imageMarkdown });
      
      toast.success('¡Imagen generada e insertada!');
      setImageDialogOpen(false);
      setImagePrompt('');
    } catch (error) {
      console.error('Error generating image:', error);
      toast.error('Error al generar imagen. Intenta con otra descripción.');
    } finally {
      setGeneratingImage(false);
    }
  };

  const handleUploadImage = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    
    if (!file.type.startsWith('image/')) {
      toast.error('Solo se permiten archivos de imagen');
      return;
    }
    
    setUploadingImage(true);
    try {
      const token = localStorage.getItem('admin_token');
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await axios.post(
        `${ADMIN_API}/upload-image`,
        formData,
        { 
          headers: { 
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          }
        }
      );
      
      // The API returns a path like /api/uploads/xxx.png
      const imageUrl = response.data.image_url;
      const fullUrl = imageUrl.startsWith('/api') 
        ? `${process.env.REACT_APP_BACKEND_URL}${imageUrl}`
        : imageUrl;
      
      const imageName = file.name.replace(/\.[^/.]+$/, '');
      const imageMarkdown = `\n\n![${imageName}](${fullUrl})\n\n`;
      setLessonForm({ ...lessonForm, content: lessonForm.content + imageMarkdown });
      
      toast.success('¡Imagen subida e insertada!');
      setImageDialogOpen(false);
    } catch (error) {
      console.error('Error uploading image:', error);
      toast.error('Error al subir imagen');
    } finally {
      setUploadingImage(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
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
    setTopicPrompt('');
    setGenerationMode('prompt');
    setLessonForm({ title: '', content: '', order: 1, duration_minutes: 30 });
    setChatOpen(false);
    setChatHistory([]);
    setChatMessage('');
  };

  if (!course) return <div>Cargando...</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" onClick={() => navigate('/admin/courses')}>
          <ArrowLeft size={20} className="mr-2" />
          Volver
        </Button>
        <div className="flex-1">
          <h1 className="text-3xl font-bold">{course.title}</h1>
          <p className="text-slate-600">Editar contenido del curso</p>
        </div>
        <Button onClick={openAddChapter}>
          <Plus size={20} className="mr-2" />
          Nuevo Capítulo
        </Button>
      </div>

      <div className="space-y-4">
        {chapters.length === 0 ? (
          <Card>
            <CardContent className="text-center py-12">
              <BookOpen className="mx-auto mb-4 text-slate-400" size={48} />
              <h3 className="text-xl font-semibold mb-2">No hay capítulos</h3>
              <p className="text-slate-500 mb-4">Comienza agregando el primer capítulo</p>
              <Button onClick={openAddChapter}>Crear Capítulo</Button>
            </CardContent>
          </Card>
        ) : (
          chapters.map((chapter, chapterIndex) => (
            <Card key={chapter.id}>
              <CardHeader className="bg-slate-50">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <GripVertical className="text-slate-400" size={20} />
                    <div>
                      <CardTitle className="text-lg">
                        Capítulo {chapter.order}: {chapter.title}
                      </CardTitle>
                      <p className="text-sm text-slate-600 mt-1">{chapter.description}</p>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Button size="sm" variant="outline" onClick={() => openAddLesson(chapter)}>
                      <Plus size={16} className="mr-1" />
                      Lección
                    </Button>
                    <Button size="sm" variant="outline" onClick={() => openEditChapter(chapter)}>
                      <Edit size={16} />
                    </Button>
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
        <DialogContent className="max-w-5xl max-h-[90vh] overflow-y-auto">
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

            <div className="border-t pt-4">
              <Label className="flex items-center gap-2 mb-3">
                <Sparkles size={16} className="text-primary" />
                Generar contenido con IA (GPT-5.2)
              </Label>
              
              {/* Generation Mode Tabs */}
              <div className="bg-slate-50 rounded-lg p-4">
                <div className="flex gap-2 mb-4">
                  <Button
                    type="button"
                    size="sm"
                    variant={generationMode === 'prompt' ? 'default' : 'outline'}
                    onClick={() => setGenerationMode('prompt')}
                    className="flex-1"
                  >
                    <MessageSquare size={14} className="mr-1" />
                    Desde Tema
                  </Button>
                  <Button
                    type="button"
                    size="sm"
                    variant={generationMode === 'document' ? 'default' : 'outline'}
                    onClick={() => setGenerationMode('document')}
                    className="flex-1"
                  >
                    <FileText size={14} className="mr-1" />
                    Desde Documento
                  </Button>
                </div>

                {generationMode === 'prompt' ? (
                  <div className="space-y-3">
                    <p className="text-xs text-slate-500">
                      Describe el tema y qué quieres que contenga la lección. Remy generará contenido completo con ejemplos, gráficos y ejercicios.
                    </p>
                    <Textarea
                      value={topicPrompt}
                      onChange={(e) => setTopicPrompt(e.target.value)}
                      placeholder="Ej: Explica la regla de la cadena para derivadas, incluye ejemplos con funciones trigonométricas compuestas y aplicaciones en física."
                      className="h-24 text-sm"
                    />
                    <Button
                      type="button"
                      onClick={handleGenerateContent}
                      disabled={!topicPrompt.trim() || !lessonForm.title || generatingContent}
                      className="w-full"
                    >
                      {generatingContent ? (
                        <>
                          <div className="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full mr-2"></div>
                          Generando con GPT-5.2...
                        </>
                      ) : (
                        <>
                          <Sparkles size={16} className="mr-2" />
                          Generar Lección
                        </>
                      )}
                    </Button>
                  </div>
                ) : (
                  <div className="space-y-3">
                    <p className="text-xs text-slate-500">
                      Sube un PDF con el material de referencia. Remy extraerá y adaptará el contenido de forma didáctica.
                    </p>
                    <Input
                      type="file"
                      accept=".pdf"
                      onChange={(e) => setPdfFile(e.target.files[0])}
                      className="text-sm"
                    />
                    <div className="flex gap-2">
                      <Button 
                        type="button" 
                        onClick={handlePdfUpload} 
                        size="sm" 
                        variant="outline" 
                        disabled={!pdfFile}
                        className="flex-1"
                      >
                        <FileText size={14} className="mr-1" />
                        Procesar PDF
                      </Button>
                      <Button
                        type="button"
                        onClick={handleGenerateContent}
                        size="sm"
                        disabled={!pdfText || !lessonForm.title || generatingContent}
                        className="flex-1"
                      >
                        {generatingContent ? 'Generando...' : 'Generar desde PDF'}
                      </Button>
                    </div>
                    {pdfText && (
                      <div className="space-y-2">
                        <p className="text-xs text-green-600 flex items-center gap-1">
                          <Check size={12} />
                          PDF procesado: {pdfText.length.toLocaleString()} caracteres extraídos
                        </p>
                        <div className="bg-slate-100 rounded p-2 max-h-24 overflow-y-auto">
                          <p className="text-xs text-slate-600 font-mono whitespace-pre-wrap">
                            {pdfText.substring(0, 500)}...
                          </p>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="relative">
                <div className="flex items-center justify-between mb-2">
                  <Label>Contenido (Markdown + LaTeX)</Label>
                  <div className="flex gap-2">
                    <Button 
                      type="button" 
                      size="sm" 
                      variant="outline"
                      onClick={() => setImageDialogOpen(true)}
                      className="gap-1"
                    >
                      <Image size={14} />
                      Insertar Imagen
                    </Button>
                    {lessonForm.content && (
                      <Button 
                        type="button" 
                        size="sm" 
                        variant={chatOpen ? "default" : "outline"}
                        onClick={() => chatOpen ? setChatOpen(false) : openChatEditor()}
                        className="gap-1"
                      >
                        <MessageSquare size={14} />
                        {chatOpen ? 'Cerrar Chat' : 'Editar con IA'}
                      </Button>
                    )}
                  </div>
                </div>
                <Textarea
                  value={lessonForm.content}
                  onChange={(e) => setLessonForm({ ...lessonForm, content: e.target.value })}
                  placeholder="# Título\n\n## Sección\n\nTexto con fórmulas $$x^2$$\n\n[DESMOS:y=x^2]"
                  className="font-mono text-sm"
                  rows={20}
                  required
                />
                
                {/* AI Chat Panel */}
                {chatOpen && (
                  <div className="absolute top-10 right-0 w-96 bg-white border rounded-lg shadow-2xl z-10">
                    <div className="p-3 bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-t-lg flex items-center justify-between">
                      <span className="font-medium flex items-center gap-2">
                        <Sparkles size={16} />
                        Chat con Remy - Editar Lección
                      </span>
                      <button onClick={() => setChatOpen(false)} className="hover:bg-white/20 rounded p-1">
                        <X size={16} />
                      </button>
                    </div>
                    <div className="h-80 overflow-y-auto p-3 space-y-3 bg-slate-50">
                      {chatHistory.map((msg, i) => (
                        <div 
                          key={i} 
                          className={`p-3 rounded-lg text-sm ${
                            msg.role === 'user' 
                              ? 'bg-cyan-500 text-white ml-8' 
                              : 'bg-white border shadow-sm mr-4 text-slate-700'
                          }`}
                        >
                          <div className="whitespace-pre-wrap leading-relaxed">{msg.content}</div>
                        </div>
                      ))}
                      {chatLoading && (
                        <div className="bg-white border shadow-sm mr-4 p-3 rounded-lg text-sm flex items-center gap-2">
                          <div className="animate-spin w-4 h-4 border-2 border-cyan-500 border-t-transparent rounded-full"></div>
                          <span className="text-slate-500">Remy está trabajando...</span>
                        </div>
                      )}
                      <div ref={chatEndRef} />
                    </div>
                    <div className="p-3 border-t bg-white rounded-b-lg">
                      <div className="flex gap-2">
                        <Input
                          value={chatMessage}
                          onChange={(e) => setChatMessage(e.target.value)}
                          placeholder="Ej: Agrega un ejemplo de derivada de x³..."
                          onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleSendChatMessage()}
                          disabled={chatLoading}
                          className="text-sm"
                        />
                        <Button 
                          type="button" 
                          size="sm" 
                          onClick={handleSendChatMessage}
                          disabled={chatLoading || !chatMessage.trim()}
                          className="bg-cyan-500 hover:bg-cyan-600"
                        >
                          <Send size={14} />
                        </Button>
                      </div>
                      <p className="text-xs text-slate-400 mt-2">
                        Tip: Sé específico. "Agrega un Desmos interactivo que muestre cómo la pendiente cambia"
                      </p>
                    </div>
                  </div>
                )}
              </div>
              <div>
                <Label>Vista Previa</Label>
                <div className="border rounded-lg p-4 h-[500px] overflow-y-auto bg-white">
                  <MarkdownRenderer content={lessonForm.content} />
                </div>
              </div>
            </div>

            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? 'Guardando...' : editingLesson ? 'Actualizar Lección' : 'Crear Lección'}
            </Button>
          </form>
        </DialogContent>
      </Dialog>

      {/* Image Insertion Dialog */}
      <Dialog open={imageDialogOpen} onOpenChange={setImageDialogOpen}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Image size={20} />
              Insertar Imagen
            </DialogTitle>
          </DialogHeader>
          
          <Tabs defaultValue="generate" className="w-full">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="generate" className="gap-2">
                <Wand2 size={14} />
                Generar con IA
              </TabsTrigger>
              <TabsTrigger value="upload" className="gap-2">
                <Upload size={14} />
                Subir Archivo
              </TabsTrigger>
            </TabsList>
            
            <TabsContent value="generate" className="space-y-4 mt-4">
              <div className="space-y-2">
                <Label>Describe la imagen que necesitas</Label>
                <Textarea
                  value={imagePrompt}
                  onChange={(e) => setImagePrompt(e.target.value)}
                  placeholder="Ej: Diagrama que muestre la relación entre una función y su derivada, con flechas indicando la pendiente en diferentes puntos"
                  rows={3}
                />
              </div>
              
              <div className="space-y-2">
                <Label>Estilo</Label>
                <select
                  value={imageStyle}
                  onChange={(e) => setImageStyle(e.target.value)}
                  className="w-full border rounded-md p-2 text-sm"
                >
                  <option value="educativo">Educativo (limpio, profesional)</option>
                  <option value="diagrama">Diagrama técnico</option>
                  <option value="ilustracion">Ilustración colorida</option>
                  <option value="minimalista">Minimalista</option>
                </select>
              </div>
              
              <Button 
                onClick={handleGenerateImage} 
                disabled={generatingImage || !imagePrompt.trim()}
                className="w-full gap-2"
              >
                {generatingImage ? (
                  <>
                    <div className="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full"></div>
                    Generando imagen... (puede tomar ~30s)
                  </>
                ) : (
                  <>
                    <Wand2 size={16} />
                    Generar Imagen con IA
                  </>
                )}
              </Button>
              
              <p className="text-xs text-slate-500 text-center">
                La imagen se generará con GPT Image y se insertará al final del contenido
              </p>
            </TabsContent>
            
            <TabsContent value="upload" className="space-y-4 mt-4">
              <div className="border-2 border-dashed border-slate-200 rounded-lg p-8 text-center hover:border-cyan-400 transition-colors">
                <Upload className="mx-auto mb-4 text-slate-400" size={40} />
                <p className="text-slate-600 mb-2">Arrastra una imagen o haz clic para seleccionar</p>
                <p className="text-xs text-slate-400 mb-4">PNG, JPG, GIF hasta 10MB</p>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleUploadImage}
                  className="hidden"
                  id="image-upload"
                />
                <Button 
                  type="button" 
                  variant="outline"
                  onClick={() => fileInputRef.current?.click()}
                  disabled={uploadingImage}
                >
                  {uploadingImage ? 'Subiendo...' : 'Seleccionar Archivo'}
                </Button>
              </div>
              
              <p className="text-xs text-slate-500 text-center">
                La imagen se convertirá a base64 y se insertará al final del contenido
              </p>
            </TabsContent>
          </Tabs>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default CourseContentEditor;
