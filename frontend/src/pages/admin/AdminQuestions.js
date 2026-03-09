import { useState, useEffect, useRef, useCallback } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { toast } from 'sonner';
import { Plus, Edit, Trash2, Sparkles, FileText, Filter, Image, Upload, Wand2, Eye, EyeOff, MessageSquare } from 'lucide-react';
import { QuestionContent, QuestionOption, ExplanationBlock } from '@/components/course/QuestionRenderer';
import RemyChat from '@/components/RemyChat';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const ADMIN_API = `${BACKEND_URL}/api/admin`;

const AdminQuestions = () => {
  const [questions, setQuestions] = useState([]);
  const [courses, setCourses] = useState([]);
  const [chapters, setChapters] = useState([]);
  const [lessons, setLessons] = useState([]);
  const [loading, setLoading] = useState(false);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [pdfDialogOpen, setPdfDialogOpen] = useState(false);
  const [editingQuestion, setEditingQuestion] = useState(null);
  const [pdfFile, setPdfFile] = useState(null);
  const [pdfText, setPdfText] = useState('');
  const [generatingQuestions, setGeneratingQuestions] = useState(false);
  const [generatedQuestions, setGeneratedQuestions] = useState([]);
  const [showPreview, setShowPreview] = useState(true);
  
  // Filters
  const [filterCourse, setFilterCourse] = useState('');
  const [filterChapter, setFilterChapter] = useState('');
  const [filterTopic, setFilterTopic] = useState('');
  
  // Image dialog state
  const [imageDialogOpen, setImageDialogOpen] = useState(false);
  const [imagePrompt, setImagePrompt] = useState('');
  const [generatingImage, setGeneratingImage] = useState(false);
  const [uploadingImage, setUploadingImage] = useState(false);
  const [imageTarget, setImageTarget] = useState('question'); // 'question', 'option', 'explanation'
  const fileInputRef = useRef(null);
  const questionTextareaRef = useRef(null);
  const explanationTextareaRef = useRef(null);
  const [cursorPosition, setCursorPosition] = useState(null);

  // Chat with Remy state
  const [chatOpen, setChatOpen] = useState(false);

  const [formData, setFormData] = useState({
    course_id: '',
    chapter_id: '',
    lesson_id: '',
    topic: '',
    subtopic: '',
    difficulty: 'medio',
    question_text: '',
    options: ['A) ', 'B) ', 'C) ', 'D) '],
    correct_answer: 'A',
    explanation: '',
    image_placeholder: ''
  });

  const [generatorData, setGeneratorData] = useState({
    course_id: '',
    chapter_id: '',
    topic: '',
    num_questions: 5
  });

  useEffect(() => {
    fetchQuestions();
    fetchCourses();
  }, []);

  useEffect(() => {
    if (formData.course_id) {
      fetchChaptersForCourse(formData.course_id);
    } else {
      setChapters([]);
      setLessons([]);
    }
  }, [formData.course_id]);

  useEffect(() => {
    if (formData.chapter_id) {
      fetchLessonsForChapter(formData.chapter_id);
    } else {
      setLessons([]);
    }
  }, [formData.chapter_id]);

  const fetchQuestions = async () => {
    try {
      const token = localStorage.getItem('admin_token');
      const params = new URLSearchParams();
      if (filterCourse) params.append('course_id', filterCourse);
      if (filterChapter) params.append('chapter_id', filterChapter);
      if (filterTopic) params.append('topic', filterTopic);

      const response = await axios.get(`${ADMIN_API}/questions?${params.toString()}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setQuestions(response.data);
    } catch (error) {
      console.error('Error fetching questions:', error);
      toast.error('Error al cargar preguntas');
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

  const fetchChaptersForCourse = async (courseId) => {
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.get(`${ADMIN_API}/courses/${courseId}/chapters`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setChapters(response.data);
    } catch (error) {
      console.error('Error fetching chapters:', error);
      setChapters([]);
    }
  };

  const fetchLessonsForChapter = async (chapterId) => {
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.get(`${ADMIN_API}/chapters/${chapterId}/lessons`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setLessons(response.data);
    } catch (error) {
      console.error('Error fetching lessons:', error);
      setLessons([]);
    }
  };

  // Callback for RemyChat to update question content
  const handleQuestionContentUpdate = useCallback((newContent) => {
    // The AI returns the complete question data as JSON
    try {
      const updatedData = JSON.parse(newContent);
      setFormData(prev => ({
        ...prev,
        question_text: updatedData.question_text || prev.question_text,
        options: updatedData.options || prev.options,
        explanation: updatedData.explanation || prev.explanation,
        correct_answer: updatedData.correct_answer || prev.correct_answer
      }));
    } catch {
      // If not JSON, it might be just the explanation or question text
      // Try to detect which field was updated based on content
      if (newContent.includes('A)') && newContent.includes('B)')) {
        // Looks like it's a full question, try to parse manually
        toast.info('Contenido actualizado - revisa los cambios');
      }
    }
  }, []);

  // Get combined content for the chat context
  const getQuestionContentForChat = useCallback(() => {
    return JSON.stringify({
      question_text: formData.question_text,
      options: formData.options,
      correct_answer: formData.correct_answer,
      explanation: formData.explanation
    }, null, 2);
  }, [formData.question_text, formData.options, formData.correct_answer, formData.explanation]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const token = localStorage.getItem('admin_token');
      const payload = {
        ...formData,
        id: editingQuestion?.id || undefined,
        options: formData.options.filter(opt => opt.trim() !== '' && opt.trim() !== 'A)' && opt.trim() !== 'B)' && opt.trim() !== 'C)' && opt.trim() !== 'D)')
      };

      if (editingQuestion) {
        await axios.put(`${ADMIN_API}/questions/${editingQuestion.id}`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Pregunta actualizada exitosamente');
      } else {
        await axios.post(`${ADMIN_API}/questions`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Pregunta creada exitosamente');
      }

      fetchQuestions();
      setDialogOpen(false);
      resetForm();
    } catch (error) {
      console.error('Error saving question:', error);
      toast.error('Error al guardar pregunta');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (questionId) => {
    if (!window.confirm('¿Estás seguro de eliminar esta pregunta?')) return;

    try {
      const token = localStorage.getItem('admin_token');
      await axios.delete(`${ADMIN_API}/questions/${questionId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      toast.success('Pregunta eliminada exitosamente');
      fetchQuestions();
    } catch (error) {
      console.error('Error deleting question:', error);
      toast.error('Error al eliminar pregunta');
    }
  };

  const handleEdit = (question) => {
    setEditingQuestion(question);
    // Ensure options have proper format
    const options = question.options || ['A) ', 'B) ', 'C) ', 'D) '];
    while (options.length < 4) {
      options.push(`${String.fromCharCode(65 + options.length)}) `);
    }
    
    setFormData({
      course_id: question.course_id || '',
      chapter_id: question.chapter_id || '',
      lesson_id: question.lesson_id || '',
      topic: question.topic || '',
      subtopic: question.subtopic || '',
      difficulty: question.difficulty || 'medio',
      question_text: question.question_text || '',
      options: options,
      correct_answer: question.correct_answer || 'A',
      explanation: question.explanation || '',
      image_placeholder: question.image_placeholder || ''
    });
    setDialogOpen(true);
  };

  const resetForm = () => {
    setEditingQuestion(null);
    setFormData({
      course_id: '',
      chapter_id: '',
      lesson_id: '',
      topic: '',
      subtopic: '',
      difficulty: 'medio',
      question_text: '',
      options: ['A) ', 'B) ', 'C) ', 'D) '],
      correct_answer: 'A',
      explanation: '',
      image_placeholder: ''
    });
    setChapters([]);
    setLessons([]);
    setChatOpen(false);
  };

  const handlePdfUpload = async () => {
    if (!pdfFile) {
      toast.error('Por favor selecciona un archivo PDF');
      return;
    }

    try {
      const token = localStorage.getItem('admin_token');
      const formDataPdf = new FormData();
      formDataPdf.append('file', pdfFile);

      const response = await axios.post(`${ADMIN_API}/upload-pdf`, formDataPdf, {
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

  const handleGenerateQuestions = async () => {
    if (!pdfText || !generatorData.course_id || !generatorData.topic) {
      toast.error('Debes subir un PDF, seleccionar curso y especificar tema');
      return;
    }

    setGeneratingQuestions(true);
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.post(
        `${ADMIN_API}/generate-questions`,
        {
          pdf_content: pdfText,
          course_id: generatorData.course_id,
          topic: generatorData.topic,
          num_questions: generatorData.num_questions
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      setGeneratedQuestions(response.data.questions);
      toast.success(`${response.data.questions.length} preguntas generadas con GPT-5.2`);
    } catch (error) {
      console.error('Error generating questions:', error);
      toast.error('Error al generar preguntas con IA');
    } finally {
      setGeneratingQuestions(false);
    }
  };

  const handleSaveGeneratedQuestion = async (question) => {
    try {
      const token = localStorage.getItem('admin_token');
      await axios.post(
        `${ADMIN_API}/questions`,
        {
          course_id: generatorData.course_id,
          chapter_id: generatorData.chapter_id || null,
          topic: generatorData.topic,
          subtopic: '',
          difficulty: question.difficulty || 'medio',
          question_text: question.question_text,
          options: question.options,
          correct_answer: question.correct_answer,
          explanation: question.explanation,
          image_placeholder: question.image_placeholder || null
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      toast.success('Pregunta guardada en el banco');
      fetchQuestions();
      // Remove from generated list
      setGeneratedQuestions(prev => prev.filter(q => q !== question));
    } catch (error) {
      console.error('Error saving generated question:', error);
      toast.error('Error al guardar pregunta');
    }
  };

  // Image handling
  const handleGenerateImage = async () => {
    if (!imagePrompt.trim()) {
      toast.error('Describe la imagen que necesitas');
      return;
    }
    
    setGeneratingImage(true);
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.post(
        `${ADMIN_API}/generate-image`,
        {
          prompt: `Imagen educativa para pregunta de examen: ${imagePrompt}`,
          style: 'educativo'
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      const imageUrl = response.data.image_url;
      const imageMarkdown = `![${imagePrompt}](${imageUrl})`;
      
      insertImageIntoField(imageMarkdown);
      setImageDialogOpen(false);
      setImagePrompt('');
      toast.success('Imagen generada e insertada');
    } catch (error) {
      console.error('Error generating image:', error);
      toast.error('Error al generar imagen');
    } finally {
      setGeneratingImage(false);
    }
  };

  const handleUploadImage = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    setUploadingImage(true);
    try {
      const token = localStorage.getItem('admin_token');
      const uploadData = new FormData();
      uploadData.append('file', file);
      
      const response = await axios.post(`${ADMIN_API}/upload-image`, uploadData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      });
      
      const imageUrl = response.data.image_url;
      const imageMarkdown = `![Imagen](${imageUrl})`;
      
      insertImageIntoField(imageMarkdown);
      setImageDialogOpen(false);
      toast.success('Imagen subida e insertada');
    } catch (error) {
      console.error('Error uploading image:', error);
      toast.error('Error al subir imagen');
    } finally {
      setUploadingImage(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const insertImageIntoField = (imageMarkdown) => {
    const insertAtPosition = (text, position, insertion) => {
      if (position !== null && position !== undefined) {
        const before = text.substring(0, position);
        const after = text.substring(position);
        return before + '\n\n' + insertion + '\n\n' + after;
      }
      return text + '\n\n' + insertion;
    };

    if (imageTarget === 'question') {
      setFormData(prev => ({
        ...prev,
        question_text: insertAtPosition(prev.question_text, cursorPosition, imageMarkdown)
      }));
    } else if (imageTarget === 'explanation') {
      setFormData(prev => ({
        ...prev,
        explanation: insertAtPosition(prev.explanation, cursorPosition, imageMarkdown)
      }));
    }
    setCursorPosition(null);
  };

  const openImageDialog = (target) => {
    // Save cursor position before opening dialog
    if (target === 'question' && questionTextareaRef.current) {
      setCursorPosition(questionTextareaRef.current.selectionStart);
    } else if (target === 'explanation' && explanationTextareaRef.current) {
      setCursorPosition(explanationTextareaRef.current.selectionStart);
    }
    setImageTarget(target);
    setImageDialogOpen(true);
  };

  // Get course/chapter names for display
  const getCourseName = (courseId) => courses.find(c => c.id === courseId)?.title || courseId;
  const getChapterName = (chapterId) => chapters.find(c => c.id === chapterId)?.title || chapterId;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Banco de Preguntas</h1>
          <p className="text-slate-600">Administra las preguntas para simulacros</p>
        </div>
        <div className="flex gap-2">
          <Dialog open={pdfDialogOpen} onOpenChange={setPdfDialogOpen}>
            <DialogTrigger asChild>
              <Button variant="outline">
                <Sparkles className="mr-2" size={20} />
                Generar con IA
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-5xl max-h-[90vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle>Generar Preguntas con GPT-5.2</DialogTitle>
              </DialogHeader>
              <Tabs defaultValue="upload">
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="upload">1. Subir Documento</TabsTrigger>
                  <TabsTrigger value="generate">2. Generar y Revisar</TabsTrigger>
                </TabsList>
                <TabsContent value="upload" className="space-y-4">
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-sm text-blue-800">
                    <p className="font-medium mb-1">💡 Cómo funciona:</p>
                    <ul className="list-disc ml-4 space-y-1">
                      <li>Sube un PDF con ejercicios de práctica o exámenes anteriores</li>
                      <li>La IA extraerá los ejercicios y los convertirá en preguntas de opción múltiple</li>
                      <li>También creará variantes cambiando valores numéricos</li>
                      <li>Las respuestas correctas variarán (no siempre será A)</li>
                    </ul>
                  </div>
                  <div>
                    <Label htmlFor="pdf-upload">Subir PDF de Ejercicios</Label>
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
                      <Textarea value={pdfText} readOnly className="h-40 text-xs font-mono" />
                    </div>
                  )}
                </TabsContent>
                <TabsContent value="generate" className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label>Curso</Label>
                      <Select
                        value={generatorData.course_id}
                        onValueChange={(value) => setGeneratorData({ ...generatorData, course_id: value })}
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
                      <Label>Tema</Label>
                      <Input
                        value={generatorData.topic}
                        onChange={(e) => setGeneratorData({ ...generatorData, topic: e.target.value })}
                        placeholder="Ej: Derivadas, Integrales, Límites"
                      />
                    </div>
                  </div>
                  <div>
                    <Label>Cantidad de preguntas a generar</Label>
                    <Input
                      type="number"
                      value={generatorData.num_questions}
                      onChange={(e) => setGeneratorData({ ...generatorData, num_questions: parseInt(e.target.value) })}
                      min={1}
                      max={20}
                    />
                  </div>
                  <Button
                    onClick={handleGenerateQuestions}
                    disabled={!pdfText || generatingQuestions}
                    className="w-full"
                  >
                    {generatingQuestions ? (
                      <>
                        <div className="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full mr-2"></div>
                        Generando con GPT-5.2...
                      </>
                    ) : 'Generar Preguntas'}
                  </Button>
                  
                  {generatedQuestions.length > 0 && (
                    <div className="space-y-4 mt-4">
                      <div className="flex items-center justify-between">
                        <h3 className="font-semibold">Preguntas Generadas ({generatedQuestions.length})</h3>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => setShowPreview(!showPreview)}
                        >
                          {showPreview ? <EyeOff size={16} className="mr-1" /> : <Eye size={16} className="mr-1" />}
                          {showPreview ? 'Ocultar Vista Previa' : 'Mostrar Vista Previa'}
                        </Button>
                      </div>
                      
                      {generatedQuestions.map((q, idx) => (
                        <Card key={idx} className="border-2 border-dashed border-slate-300">
                          <CardHeader className="pb-2">
                            <div className="flex items-center justify-between">
                              <div className="flex items-center gap-2">
                                <span className="bg-cyan-100 text-cyan-700 px-2 py-1 rounded text-xs font-medium">
                                  Respuesta: {q.correct_answer}
                                </span>
                                <span className={`text-xs px-2 py-1 rounded ${
                                  q.difficulty === 'fácil' ? 'bg-green-100 text-green-700' :
                                  q.difficulty === 'medio' ? 'bg-yellow-100 text-yellow-700' :
                                  'bg-red-100 text-red-700'
                                }`}>
                                  {q.difficulty}
                                </span>
                              </div>
                              <Button size="sm" onClick={() => handleSaveGeneratedQuestion(q)}>
                                Guardar en banco
                              </Button>
                            </div>
                          </CardHeader>
                          <CardContent>
                            {showPreview ? (
                              <div className="space-y-3">
                                <div className="font-medium">
                                  <QuestionContent content={`${idx + 1}. ${q.question_text}`} />
                                </div>
                                <div className="space-y-2">
                                  {q.options?.map((opt, i) => {
                                    const letter = opt.charAt(0);
                                    const isCorrect = letter === q.correct_answer;
                                    return (
                                      <div 
                                        key={i} 
                                        className={`p-2 rounded border ${isCorrect ? 'border-green-500 bg-green-50' : 'border-slate-200'}`}
                                      >
                                        <QuestionContent content={opt} />
                                        {isCorrect && <span className="text-green-600 text-sm ml-2">✓ Correcta</span>}
                                      </div>
                                    );
                                  })}
                                </div>
                                <ExplanationBlock explanation={q.explanation} />
                                {q.image_placeholder && (
                                  <div className="bg-amber-50 border border-amber-200 rounded p-3 text-sm">
                                    <span className="font-medium text-amber-700">📷 Imagen sugerida: </span>
                                    <span className="text-amber-600">{q.image_placeholder}</span>
                                  </div>
                                )}
                              </div>
                            ) : (
                              <div className="text-sm text-slate-600 space-y-1">
                                <p><strong>Pregunta:</strong> {q.question_text.substring(0, 100)}...</p>
                                <p><strong>Respuesta:</strong> {q.correct_answer}</p>
                              </div>
                            )}
                          </CardContent>
                        </Card>
                      ))}
                    </div>
                  )}
                </TabsContent>
              </Tabs>
            </DialogContent>
          </Dialog>
          
          <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
            <DialogTrigger asChild>
              <Button onClick={resetForm}>
                <Plus className="mr-2" size={20} />
                Nueva Pregunta
              </Button>
            </DialogTrigger>
            <DialogContent className={`max-h-[90vh] overflow-y-auto ${chatOpen ? 'max-w-7xl' : 'max-w-5xl'}`}>
              <DialogHeader>
                <DialogTitle>{editingQuestion ? 'Editar Pregunta' : 'Nueva Pregunta'}</DialogTitle>
              </DialogHeader>
              <form onSubmit={handleSubmit} className="space-y-4">
                {/* Classification Section */}
                <div className="bg-slate-50 rounded-lg p-4 space-y-3">
                  <h3 className="font-medium text-sm text-slate-700">Clasificación</h3>
                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <Label>Curso *</Label>
                      <Select
                        value={formData.course_id}
                        onValueChange={(value) => setFormData({ ...formData, course_id: value, chapter_id: '', lesson_id: '' })}
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
                    <div>
                      <Label>Capítulo (opcional)</Label>
                      <Select
                        value={formData.chapter_id || "none"}
                        onValueChange={(value) => setFormData({ ...formData, chapter_id: value === "none" ? '' : value, lesson_id: '' })}
                        disabled={!formData.course_id}
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Selecciona capítulo" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="none">Sin capítulo específico</SelectItem>
                          {chapters.map((chapter) => (
                            <SelectItem key={chapter.id} value={chapter.id}>
                              {chapter.title}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    <div>
                      <Label>Lección (opcional)</Label>
                      <Select
                        value={formData.lesson_id || "none"}
                        onValueChange={(value) => setFormData({ ...formData, lesson_id: value === "none" ? '' : value })}
                        disabled={!formData.chapter_id}
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Selecciona lección" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="none">Sin lección específica</SelectItem>
                          {lessons.map((lesson) => (
                            <SelectItem key={lesson.id} value={lesson.id}>
                              {lesson.title}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <Label>Tema *</Label>
                      <Input
                        value={formData.topic}
                        onChange={(e) => setFormData({ ...formData, topic: e.target.value })}
                        placeholder="Ej: Derivadas"
                        required
                      />
                    </div>
                    <div>
                      <Label>Subtema (opcional)</Label>
                      <Input
                        value={formData.subtopic}
                        onChange={(e) => setFormData({ ...formData, subtopic: e.target.value })}
                        placeholder="Ej: Regla de la cadena"
                      />
                    </div>
                    <div>
                      <Label>Dificultad</Label>
                      <Select
                        value={formData.difficulty}
                        onValueChange={(value) => setFormData({ ...formData, difficulty: value })}
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="fácil">Fácil</SelectItem>
                          <SelectItem value="medio">Medio</SelectItem>
                          <SelectItem value="difícil">Difícil</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                </div>

                {/* Question Editor - Dynamic columns */}
                <div className={`grid gap-4 ${chatOpen ? 'grid-cols-3' : 'grid-cols-2'}`}>
                  {/* Left: Editor */}
                  <div className="space-y-4">
                    <div>
                      <div className="flex items-center justify-between mb-1">
                        <Label>Enunciado de la pregunta (Markdown + LaTeX)</Label>
                        <div className="flex gap-1">
                          <Button type="button" variant="ghost" size="sm" onClick={() => openImageDialog('question')}>
                            <Image size={14} className="mr-1" />
                            Imagen
                          </Button>
                          {formData.question_text && (
                            <Button 
                              type="button" 
                              size="sm" 
                              variant={chatOpen ? "default" : "outline"}
                              onClick={(e) => {
                                e.stopPropagation();
                                setChatOpen(!chatOpen);
                              }}
                              className="gap-1"
                              data-testid="toggle-remy-chat-questions"
                            >
                              <MessageSquare size={14} />
                              {chatOpen ? 'Cerrar' : 'Remy'}
                            </Button>
                          )}
                        </div>
                      </div>
                      <Textarea
                        ref={questionTextareaRef}
                        value={formData.question_text}
                        onChange={(e) => setFormData({ ...formData, question_text: e.target.value })}
                        placeholder="Usa $formula$ para LaTeX inline, $$formula$$ para bloque"
                        className="h-24 font-mono text-sm"
                        required
                      />
                    </div>
                    
                    <div>
                      <Label>Opciones (A, B, C, D)</Label>
                      <div className="space-y-2 mt-1">
                        {formData.options.map((opt, idx) => (
                          <div key={idx} className="flex items-center gap-2">
                            <span className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                              formData.correct_answer === String.fromCharCode(65 + idx) 
                                ? 'bg-green-500 text-white' 
                                : 'bg-slate-200 text-slate-700'
                            }`}>
                              {String.fromCharCode(65 + idx)}
                            </span>
                            <Input
                              value={opt.startsWith(`${String.fromCharCode(65 + idx)}) `) ? opt.substring(3) : opt}
                              onChange={(e) => {
                                const newOpts = [...formData.options];
                                newOpts[idx] = `${String.fromCharCode(65 + idx)}) ${e.target.value}`;
                                setFormData({ ...formData, options: newOpts });
                              }}
                              placeholder={`Opción ${String.fromCharCode(65 + idx)} - usa $formula$ para LaTeX`}
                              className="flex-1 font-mono text-sm"
                            />
                            <Button
                              type="button"
                              variant={formData.correct_answer === String.fromCharCode(65 + idx) ? "default" : "outline"}
                              size="sm"
                              onClick={() => setFormData({ ...formData, correct_answer: String.fromCharCode(65 + idx) })}
                            >
                              ✓
                            </Button>
                          </div>
                        ))}
                      </div>
                      <p className="text-xs text-slate-500 mt-1">
                        Haz clic en ✓ para marcar la respuesta correcta
                      </p>
                    </div>
                    
                    <div>
                      <div className="flex items-center justify-between mb-1">
                        <Label>Explicación / Solución</Label>
                        <Button type="button" variant="ghost" size="sm" onClick={() => openImageDialog('explanation')}>
                          <Image size={14} className="mr-1" />
                          Imagen
                        </Button>
                      </div>
                      <Textarea
                        ref={explanationTextareaRef}
                        value={formData.explanation}
                        onChange={(e) => setFormData({ ...formData, explanation: e.target.value })}
                        placeholder="Explica paso a paso la solución usando $formulas$ de LaTeX"
                        className="h-32 font-mono text-sm"
                        required
                      />
                    </div>
                    
                    <div>
                      <Label>Descripción de imagen para GPAI (opcional)</Label>
                      <Input
                        value={formData.image_placeholder}
                        onChange={(e) => setFormData({ ...formData, image_placeholder: e.target.value })}
                        placeholder="Ej: Gráfica de f(x)=x² con tangente en x=2"
                      />
                      <p className="text-xs text-slate-500 mt-1">
                        Describe la imagen que necesitas para generarla con IA externa
                      </p>
                    </div>
                  </div>

                  {/* Middle: Preview */}
                  <div className="border rounded-lg p-4 bg-white overflow-y-auto max-h-[500px]">
                    <h3 className="text-sm font-medium text-slate-500 mb-3">Vista Previa</h3>
                    <div className="space-y-4">
                      <div>
                        <QuestionContent content={formData.question_text || '*Escribe el enunciado...*'} />
                      </div>
                      <div className="space-y-2">
                        {formData.options.map((opt, idx) => {
                          const letter = String.fromCharCode(65 + idx);
                          const content = opt.startsWith(`${letter}) `) ? opt.substring(3) : opt;
                          if (!content.trim()) return null;
                          return (
                            <QuestionOption
                              key={idx}
                              option={opt}
                              isSelected={false}
                              isCorrect={formData.correct_answer === letter}
                              showResult={true}
                              disabled={true}
                            />
                          );
                        })}
                      </div>
                      {formData.explanation && (
                        <ExplanationBlock explanation={formData.explanation} />
                      )}
                      {formData.image_placeholder && (
                        <div className="bg-amber-50 border border-amber-200 rounded-lg p-3 text-sm">
                          <span className="font-medium text-amber-700">📷 Imagen pendiente: </span>
                          <span className="text-amber-600">{formData.image_placeholder}</span>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Right: Chat with Remy - Only visible when chat is open */}
                  {chatOpen && (
                    <div className="h-[500px]">
                      <RemyChat
                        isOpen={chatOpen}
                        onClose={() => setChatOpen(false)}
                        currentContent={getQuestionContentForChat()}
                        onContentUpdate={handleQuestionContentUpdate}
                        context={{
                          type: 'question',
                          topic: formData.topic,
                          courseTitle: courses.find(c => c.id === formData.course_id)?.title || '',
                          questionData: {
                            question_text: formData.question_text,
                            options: formData.options,
                            correct_answer: formData.correct_answer,
                            explanation: formData.explanation
                          }
                        }}
                      />
                    </div>
                  )}
                </div>

                <Button type="submit" className="w-full" disabled={loading}>
                  {loading ? 'Guardando...' : editingQuestion ? 'Actualizar Pregunta' : 'Crear Pregunta'}
                </Button>
              </form>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {/* Filters */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="flex items-center gap-2 text-lg">
            <Filter size={18} />
            Filtros
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <Label>Curso</Label>
              <Select value={filterCourse || "all"} onValueChange={(v) => setFilterCourse(v === "all" ? "" : v)}>
                <SelectTrigger>
                  <SelectValue placeholder="Todos los cursos" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Todos</SelectItem>
                  {courses.map((course) => (
                    <SelectItem key={course.id} value={course.id}>
                      {course.title}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Capítulo</Label>
              <Select 
                value={filterChapter || "all"} 
                onValueChange={(v) => setFilterChapter(v === "all" ? "" : v)}
                disabled={!filterCourse}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Todos los capítulos" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Todos</SelectItem>
                  {chapters.map((chapter) => (
                    <SelectItem key={chapter.id} value={chapter.id}>
                      {chapter.title}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Tema</Label>
              <Input
                value={filterTopic}
                onChange={(e) => setFilterTopic(e.target.value)}
                placeholder="Ej: Derivadas"
              />
            </div>
            <div className="flex items-end">
              <Button onClick={fetchQuestions} className="w-full">
                Aplicar Filtros
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Questions List */}
      <div className="space-y-4">
        <p className="text-sm text-slate-600">Total: {questions.length} preguntas en el banco</p>
        {questions.map((question, idx) => (
          <Card key={question.id} className="overflow-hidden">
            <CardHeader className="bg-slate-50 pb-3">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2 flex-wrap">
                    <span className="text-xs bg-primary/10 text-primary px-2 py-1 rounded font-medium">
                      {question.topic}
                    </span>
                    {question.subtopic && (
                      <span className="text-xs bg-slate-200 text-slate-600 px-2 py-1 rounded">
                        {question.subtopic}
                      </span>
                    )}
                    <span className={`text-xs px-2 py-1 rounded font-medium ${
                      question.difficulty === 'fácil' ? 'bg-green-100 text-green-700' :
                      question.difficulty === 'medio' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-red-100 text-red-700'
                    }`}>
                      {question.difficulty}
                    </span>
                    <span className="text-xs bg-cyan-100 text-cyan-700 px-2 py-1 rounded font-medium">
                      Respuesta: {question.correct_answer}
                    </span>
                  </div>
                </div>
                <div className="flex gap-2">
                  <Button size="sm" variant="outline" onClick={() => handleEdit(question)}>
                    <Edit size={14} className="mr-1" />
                    Editar
                  </Button>
                  <Button size="sm" variant="destructive" onClick={() => handleDelete(question.id)}>
                    <Trash2 size={14} />
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent className="pt-4">
              <div className="space-y-4">
                <div className="font-medium">
                  <QuestionContent content={`${idx + 1}. ${question.question_text}`} />
                </div>
                <div className="space-y-2">
                  {question.options?.map((opt, i) => {
                    const letter = opt.charAt(0);
                    const isCorrect = letter === question.correct_answer;
                    return (
                      <div key={i} className={`p-3 rounded-lg border ${isCorrect ? 'border-green-500 bg-green-50' : 'border-slate-200'}`}>
                        <QuestionContent content={opt} />
                        {isCorrect && <span className="text-green-600 text-sm font-medium ml-2">✓ Correcta</span>}
                      </div>
                    );
                  })}
                </div>
                <ExplanationBlock explanation={question.explanation} />
                {question.image_placeholder && (
                  <div className="bg-amber-50 border border-amber-200 rounded-lg p-3 text-sm">
                    <span className="font-medium text-amber-700">📷 Imagen pendiente: </span>
                    <span className="text-amber-600">{question.image_placeholder}</span>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Image Dialog */}
      <Dialog open={imageDialogOpen} onOpenChange={setImageDialogOpen}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Image size={20} />
              Insertar Imagen en {imageTarget === 'question' ? 'Enunciado' : 'Explicación'}
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
                  placeholder="Ej: Gráfica de la función f(x)=x² mostrando el vértice y los ejes"
                  rows={3}
                />
              </div>
              
              <Button 
                onClick={handleGenerateImage} 
                disabled={generatingImage || !imagePrompt.trim()}
                className="w-full gap-2"
              >
                {generatingImage ? (
                  <>
                    <div className="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full"></div>
                    Generando...
                  </>
                ) : (
                  <>
                    <Wand2 size={16} />
                    Generar Imagen
                  </>
                )}
              </Button>
            </TabsContent>
            
            <TabsContent value="upload" className="space-y-4 mt-4">
              <div className="border-2 border-dashed border-slate-200 rounded-lg p-8 text-center hover:border-cyan-400 transition-colors">
                <Upload className="mx-auto mb-4 text-slate-400" size={40} />
                <p className="text-slate-600 mb-2">Arrastra o selecciona una imagen</p>
                <p className="text-xs text-slate-400 mb-4">PNG, JPG, GIF hasta 10MB</p>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleUploadImage}
                  className="hidden"
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
            </TabsContent>
          </Tabs>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default AdminQuestions;
