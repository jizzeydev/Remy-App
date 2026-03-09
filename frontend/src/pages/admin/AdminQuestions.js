import { useState, useEffect, useRef, useCallback } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { toast } from 'sonner';
import { 
  Plus, Edit, Trash2, Sparkles, FileText, Image, Upload, 
  MessageSquare, ArrowLeft, BookOpen, Layers, HelpCircle,
  CheckCircle, Wand2, FileUp, ChevronDown, ChevronRight
} from 'lucide-react';
import { QuestionContent, QuestionOption, ExplanationBlock } from '@/components/course/QuestionRenderer';
import RemyChat from '@/components/RemyChat';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const ADMIN_API = `${BACKEND_URL}/api/admin`;

// ==================== COURSE SELECTOR VIEW ====================
const CourseSelector = ({ courses, onSelectCourse }) => {
  return (
    <div className="space-y-6" data-testid="questions-course-selector">
      <div>
        <h1 className="text-3xl font-bold">Banco de Preguntas</h1>
        <p className="text-slate-600 mt-1">Selecciona un curso para gestionar sus preguntas</p>
      </div>

      {courses.length === 0 ? (
        <Card className="text-center py-12">
          <CardContent>
            <BookOpen className="mx-auto mb-4 text-slate-400" size={48} />
            <h3 className="text-xl font-semibold mb-2">No hay cursos disponibles</h3>
            <p className="text-slate-500">Primero crea un curso en la sección de Cursos</p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses.map((course) => (
            <Card
              key={course.id}
              className="cursor-pointer hover:shadow-lg hover:border-primary transition-all"
              onClick={() => onSelectCourse(course)}
              data-testid={`course-card-${course.id}`}
            >
              <CardHeader>
                <div className="flex items-center justify-between mb-2">
                  <Badge variant="outline">{course.level}</Badge>
                  <span className="text-sm text-slate-500 flex items-center gap-1">
                    <HelpCircle size={14} />
                    {course.questionCount || 0} preguntas
                  </span>
                </div>
                <CardTitle>{course.title}</CardTitle>
                <CardDescription className="line-clamp-2">
                  {course.description}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full">
                  <Layers className="mr-2" size={18} />
                  Gestionar Preguntas
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

// ==================== QUESTION MANAGER VIEW ====================
const QuestionManager = ({ course, onBack }) => {
  const [questions, setQuestions] = useState([]);
  const [chapters, setChapters] = useState([]);
  const [lessons, setLessons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedChapters, setExpandedChapters] = useState({});
  
  // Dialog states
  const [editorOpen, setEditorOpen] = useState(false);
  const [generatorOpen, setGeneratorOpen] = useState(false);
  const [editingQuestion, setEditingQuestion] = useState(null);
  const [chatOpen, setChatOpen] = useState(false);
  
  // Form data for manual question creation/editing
  const [formData, setFormData] = useState({
    chapter_id: '',
    lesson_id: '',
    difficulty: 'medio',
    question_text: '',
    options: ['A) ', 'B) ', 'C) ', 'D) '],
    correct_answer: 'A',
    explanation: ''
  });

  // Generator state
  const [generatorTab, setGeneratorTab] = useState('prompt');
  const [generatorData, setGeneratorData] = useState({
    chapter_id: '',
    lesson_id: '',
    difficulty: 'medio',
    topic: '',
    num_questions: 3
  });
  const [pdfFile, setPdfFile] = useState(null);
  const [pdfText, setPdfText] = useState('');
  const [generatingQuestions, setGeneratingQuestions] = useState(false);
  const [generatedQuestions, setGeneratedQuestions] = useState([]);
  const [generatorChapters, setGeneratorChapters] = useState([]);
  const [generatorLessons, setGeneratorLessons] = useState([]);

  // Refs for cursor position
  const questionTextareaRef = useRef(null);
  const explanationTextareaRef = useRef(null);
  const [cursorPosition, setCursorPosition] = useState(null);
  const [imageTarget, setImageTarget] = useState('question');
  const [imageDialogOpen, setImageDialogOpen] = useState(false);
  const [imagePrompt, setImagePrompt] = useState('');
  const [generatingImage, setGeneratingImage] = useState(false);
  const fileInputRef = useRef(null);

  useEffect(() => {
    fetchData();
  }, [course.id]);

  useEffect(() => {
    if (generatorData.chapter_id) {
      fetchLessonsForGenerator(generatorData.chapter_id);
    } else {
      setGeneratorLessons([]);
    }
  }, [generatorData.chapter_id]);

  useEffect(() => {
    if (formData.chapter_id) {
      fetchLessonsForForm(formData.chapter_id);
    } else {
      setLessons([]);
    }
  }, [formData.chapter_id]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('admin_token');
      
      // Fetch chapters for this course
      const chaptersRes = await axios.get(`${API}/courses/${course.id}/chapters`);
      setChapters(chaptersRes.data);
      setGeneratorChapters(chaptersRes.data);
      
      // Initialize expanded state
      const expanded = {};
      chaptersRes.data.forEach(ch => { expanded[ch.id] = true; });
      setExpandedChapters(expanded);
      
      // Fetch questions for this course
      const questionsRes = await axios.get(`${ADMIN_API}/questions?course_id=${course.id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setQuestions(questionsRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
      toast.error('Error al cargar datos');
    } finally {
      setLoading(false);
    }
  };

  const fetchLessonsForGenerator = async (chapterId) => {
    try {
      const res = await axios.get(`${API}/chapters/${chapterId}/lessons`);
      setGeneratorLessons(res.data);
    } catch (error) {
      console.error('Error fetching lessons:', error);
    }
  };

  const fetchLessonsForForm = async (chapterId) => {
    try {
      const res = await axios.get(`${API}/chapters/${chapterId}/lessons`);
      setLessons(res.data);
    } catch (error) {
      console.error('Error fetching lessons:', error);
    }
  };

  const toggleChapter = (chapterId) => {
    setExpandedChapters(prev => ({
      ...prev,
      [chapterId]: !prev[chapterId]
    }));
  };

  const getQuestionsForChapter = (chapterId) => {
    return questions.filter(q => q.chapter_id === chapterId);
  };

  const getDifficultyBadge = (difficulty) => {
    const styles = {
      'fácil': 'bg-green-100 text-green-800',
      'medio': 'bg-yellow-100 text-yellow-800',
      'difícil': 'bg-red-100 text-red-800'
    };
    return styles[difficulty] || styles['medio'];
  };

  // ==================== QUESTION CRUD ====================
  const openNewQuestion = (chapterId = '') => {
    setEditingQuestion(null);
    setFormData({
      chapter_id: chapterId,
      lesson_id: '',
      difficulty: 'medio',
      question_text: '',
      options: ['A) ', 'B) ', 'C) ', 'D) '],
      correct_answer: 'A',
      explanation: ''
    });
    setChatOpen(false);
    setEditorOpen(true);
  };

  const openEditQuestion = (question) => {
    setEditingQuestion(question);
    setFormData({
      chapter_id: question.chapter_id || '',
      lesson_id: question.lesson_id || '',
      difficulty: question.difficulty || 'medio',
      question_text: question.question_text || '',
      options: question.options || ['A) ', 'B) ', 'C) ', 'D) '],
      correct_answer: question.correct_answer || 'A',
      explanation: question.explanation || ''
    });
    setChatOpen(false);
    setEditorOpen(true);
  };

  const handleSaveQuestion = async () => {
    if (!formData.chapter_id) {
      toast.error('Selecciona un capítulo');
      return;
    }
    if (!formData.question_text.trim()) {
      toast.error('Escribe el enunciado de la pregunta');
      return;
    }

    try {
      const token = localStorage.getItem('admin_token');
      const payload = {
        course_id: course.id,
        chapter_id: formData.chapter_id,
        lesson_id: formData.lesson_id || null,
        difficulty: formData.difficulty,
        question_text: formData.question_text,
        options: formData.options,
        correct_answer: formData.correct_answer,
        explanation: formData.explanation
      };

      if (editingQuestion) {
        await axios.put(`${ADMIN_API}/questions/${editingQuestion.id}`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Pregunta actualizada');
      } else {
        await axios.post(`${ADMIN_API}/questions`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Pregunta creada');
      }

      setEditorOpen(false);
      fetchData();
    } catch (error) {
      console.error('Error saving question:', error);
      toast.error('Error al guardar pregunta');
    }
  };

  const handleDeleteQuestion = async (questionId) => {
    if (!window.confirm('¿Eliminar esta pregunta?')) return;
    
    try {
      const token = localStorage.getItem('admin_token');
      await axios.delete(`${ADMIN_API}/questions/${questionId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      toast.success('Pregunta eliminada');
      fetchData();
    } catch (error) {
      console.error('Error deleting question:', error);
      toast.error('Error al eliminar pregunta');
    }
  };

  // ==================== QUESTION GENERATION ====================
  const handleUploadPdf = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    setPdfFile(file);
    
    try {
      const token = localStorage.getItem('admin_token');
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await axios.post(`${ADMIN_API}/upload-pdf`, formData, {
        headers: { 
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      });
      
      setPdfText(response.data.text);
      toast.success('PDF procesado correctamente');
    } catch (error) {
      console.error('Error uploading PDF:', error);
      toast.error('Error al procesar el PDF');
      setPdfFile(null);
    }
  };

  const handleGenerateQuestions = async () => {
    if (!generatorData.chapter_id) {
      toast.error('Selecciona un capítulo');
      return;
    }

    if (generatorTab === 'prompt' && !generatorData.topic.trim()) {
      toast.error('Escribe un tema o instrucción para generar preguntas');
      return;
    }

    if (generatorTab === 'pdf' && !pdfText) {
      toast.error('Primero sube un documento PDF');
      return;
    }

    setGeneratingQuestions(true);
    setGeneratedQuestions([]);

    try {
      const token = localStorage.getItem('admin_token');
      
      const payload = {
        course_id: course.id,
        chapter_id: generatorData.chapter_id,
        lesson_id: generatorData.lesson_id || null,
        difficulty: generatorData.difficulty,
        num_questions: generatorData.num_questions,
        generation_type: generatorTab,
        topic: generatorTab === 'prompt' ? generatorData.topic : null,
        pdf_content: generatorTab === 'pdf' ? pdfText : null
      };

      const response = await axios.post(`${ADMIN_API}/generate-questions`, payload, {
        headers: { Authorization: `Bearer ${token}` },
        timeout: 120000
      });

      setGeneratedQuestions(response.data.questions || []);
      toast.success(`${response.data.questions?.length || 0} preguntas generadas`);
    } catch (error) {
      console.error('Error generating questions:', error);
      toast.error('Error al generar preguntas');
    } finally {
      setGeneratingQuestions(false);
    }
  };

  const handleAddGeneratedQuestion = async (question, index) => {
    try {
      const token = localStorage.getItem('admin_token');
      
      const payload = {
        course_id: course.id,
        chapter_id: generatorData.chapter_id,
        lesson_id: generatorData.lesson_id || null,
        difficulty: generatorData.difficulty,
        question_text: question.question_text,
        options: question.options,
        correct_answer: question.correct_answer,
        explanation: question.explanation
      };

      await axios.post(`${ADMIN_API}/questions`, payload, {
        headers: { Authorization: `Bearer ${token}` }
      });

      // Remove from generated list
      setGeneratedQuestions(prev => prev.filter((_, i) => i !== index));
      toast.success('Pregunta añadida al banco');
      fetchData();
    } catch (error) {
      console.error('Error adding question:', error);
      toast.error('Error al añadir pregunta');
    }
  };

  const handleEditGeneratedQuestion = (question, index) => {
    // Open the editor with this question's data for modifications
    setEditingQuestion(null);
    setFormData({
      chapter_id: generatorData.chapter_id,
      lesson_id: generatorData.lesson_id || '',
      difficulty: generatorData.difficulty,
      question_text: question.question_text,
      options: question.options,
      correct_answer: question.correct_answer,
      explanation: question.explanation
    });
    // Remove from generated list
    setGeneratedQuestions(prev => prev.filter((_, i) => i !== index));
    setGeneratorOpen(false);
    setEditorOpen(true);
  };

  // ==================== IMAGE HANDLING ====================
  const insertAtCursor = (textToInsert, field) => {
    const content = field === 'question' ? formData.question_text : formData.explanation;
    if (cursorPosition !== null) {
      const before = content.substring(0, cursorPosition);
      const after = content.substring(cursorPosition);
      return before + textToInsert + after;
    }
    return content + textToInsert;
  };

  const openImageDialog = (target) => {
    if (target === 'question' && questionTextareaRef.current) {
      setCursorPosition(questionTextareaRef.current.selectionStart);
    } else if (target === 'explanation' && explanationTextareaRef.current) {
      setCursorPosition(explanationTextareaRef.current.selectionStart);
    }
    setImageTarget(target);
    setImageDialogOpen(true);
  };

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
        { prompt: imagePrompt, style: 'educativo' },
        { headers: { Authorization: `Bearer ${token}` }, timeout: 120000 }
      );
      
      const imageUrl = response.data.image_url;
      const fullUrl = imageUrl.startsWith('/api') 
        ? `${BACKEND_URL}${imageUrl}`
        : imageUrl;
      
      const imageMarkdown = `\n\n![${imagePrompt}](${fullUrl})\n\n`;
      const newContent = insertAtCursor(imageMarkdown, imageTarget);
      
      if (imageTarget === 'question') {
        setFormData(prev => ({ ...prev, question_text: newContent }));
      } else {
        setFormData(prev => ({ ...prev, explanation: newContent }));
      }
      
      toast.success('Imagen generada e insertada');
      setImageDialogOpen(false);
      setImagePrompt('');
    } catch (error) {
      console.error('Error generating image:', error);
      toast.error('Error al generar imagen');
    } finally {
      setGeneratingImage(false);
    }
  };

  // ==================== REMY CHAT INTEGRATION ====================
  const handleQuestionContentUpdate = useCallback((newContent) => {
    try {
      const updatedData = JSON.parse(newContent);
      setFormData(prev => ({
        ...prev,
        question_text: updatedData.question_text || prev.question_text,
        options: updatedData.options || prev.options,
        explanation: updatedData.explanation || prev.explanation,
        correct_answer: updatedData.correct_answer || prev.correct_answer
      }));
      toast.success('Contenido actualizado por Remy');
    } catch {
      // If not JSON, might be partial update
      toast.info('Revisa los cambios sugeridos');
    }
  }, []);

  const getQuestionContentForChat = useCallback(() => {
    return JSON.stringify({
      question_text: formData.question_text,
      options: formData.options,
      correct_answer: formData.correct_answer,
      explanation: formData.explanation
    }, null, 2);
  }, [formData.question_text, formData.options, formData.correct_answer, formData.explanation]);

  if (loading) {
    return <div className="text-center py-12">Cargando...</div>;
  }

  return (
    <div className="space-y-6" data-testid="question-manager">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" onClick={onBack}>
            <ArrowLeft size={20} className="mr-2" />
            Volver
          </Button>
          <div>
            <h1 className="text-2xl font-bold">{course.title}</h1>
            <p className="text-slate-600">Gestión de preguntas del curso</p>
          </div>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => setGeneratorOpen(true)}>
            <Sparkles size={18} className="mr-2" />
            Generar con IA
          </Button>
          <Button onClick={() => openNewQuestion()}>
            <Plus size={18} className="mr-2" />
            Nueva Pregunta
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 text-center">
            <div className="text-3xl font-bold text-primary">{questions.length}</div>
            <div className="text-sm text-slate-600">Total Preguntas</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 text-center">
            <div className="text-3xl font-bold text-green-600">
              {questions.filter(q => q.difficulty === 'fácil').length}
            </div>
            <div className="text-sm text-slate-600">Fáciles</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 text-center">
            <div className="text-3xl font-bold text-yellow-600">
              {questions.filter(q => q.difficulty === 'medio').length}
            </div>
            <div className="text-sm text-slate-600">Medias</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 text-center">
            <div className="text-3xl font-bold text-red-600">
              {questions.filter(q => q.difficulty === 'difícil').length}
            </div>
            <div className="text-sm text-slate-600">Difíciles</div>
          </CardContent>
        </Card>
      </div>

      {/* Questions by Chapter */}
      <div className="space-y-4">
        {chapters.length === 0 ? (
          <Card className="text-center py-8">
            <CardContent>
              <Layers className="mx-auto mb-4 text-slate-400" size={40} />
              <p className="text-slate-500">Este curso no tiene capítulos. Crea capítulos primero.</p>
            </CardContent>
          </Card>
        ) : (
          chapters.map(chapter => {
            const chapterQuestions = getQuestionsForChapter(chapter.id);
            const isExpanded = expandedChapters[chapter.id];
            
            return (
              <Card key={chapter.id}>
                <CardHeader 
                  className="cursor-pointer hover:bg-slate-50"
                  onClick={() => toggleChapter(chapter.id)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      {isExpanded ? <ChevronDown size={20} /> : <ChevronRight size={20} />}
                      <CardTitle className="text-lg">{chapter.title}</CardTitle>
                      <Badge variant="secondary">{chapterQuestions.length} preguntas</Badge>
                    </div>
                    <Button 
                      size="sm" 
                      variant="outline"
                      onClick={(e) => {
                        e.stopPropagation();
                        openNewQuestion(chapter.id);
                      }}
                    >
                      <Plus size={16} className="mr-1" />
                      Añadir
                    </Button>
                  </div>
                </CardHeader>
                
                {isExpanded && (
                  <CardContent className="pt-0">
                    {chapterQuestions.length === 0 ? (
                      <p className="text-sm text-slate-500 italic py-4 text-center">
                        No hay preguntas en este capítulo
                      </p>
                    ) : (
                      <div className="space-y-3">
                        {chapterQuestions.map((question, idx) => (
                          <div 
                            key={question.id}
                            className="border rounded-lg p-4 hover:bg-slate-50 transition-colors"
                          >
                            <div className="flex items-start justify-between gap-4">
                              <div className="flex-1">
                                <div className="flex items-center gap-2 mb-2">
                                  <Badge className={getDifficultyBadge(question.difficulty)}>
                                    {question.difficulty}
                                  </Badge>
                                  {question.lesson_id && (
                                    <Badge variant="outline" className="text-xs">
                                      {lessons.find(l => l.id === question.lesson_id)?.title || 'Lección'}
                                    </Badge>
                                  )}
                                  <span className="text-xs text-slate-400">
                                    Respuesta: {question.correct_answer}
                                  </span>
                                </div>
                                <div className="text-sm">
                                  <QuestionContent content={question.question_text} />
                                </div>
                              </div>
                              <div className="flex gap-2">
                                <Button 
                                  size="sm" 
                                  variant="ghost"
                                  onClick={() => openEditQuestion(question)}
                                >
                                  <Edit size={16} />
                                </Button>
                                <Button 
                                  size="sm" 
                                  variant="ghost"
                                  className="text-red-600 hover:text-red-700"
                                  onClick={() => handleDeleteQuestion(question.id)}
                                >
                                  <Trash2 size={16} />
                                </Button>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </CardContent>
                )}
              </Card>
            );
          })
        )}
      </div>

      {/* ==================== QUESTION EDITOR DIALOG ==================== */}
      <Dialog open={editorOpen} onOpenChange={setEditorOpen}>
        <DialogContent className={`max-h-[90vh] overflow-y-auto ${chatOpen ? 'max-w-7xl' : 'max-w-5xl'}`}>
          <DialogHeader>
            <DialogTitle>
              {editingQuestion ? 'Editar Pregunta' : 'Nueva Pregunta'}
            </DialogTitle>
          </DialogHeader>

          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <Label>Capítulo *</Label>
              <Select
                value={formData.chapter_id}
                onValueChange={(v) => setFormData(prev => ({ ...prev, chapter_id: v, lesson_id: '' }))}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecciona capítulo" />
                </SelectTrigger>
                <SelectContent>
                  {chapters.map(ch => (
                    <SelectItem key={ch.id} value={ch.id}>{ch.title}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Lección (opcional)</Label>
              <Select
                value={formData.lesson_id || "none"}
                onValueChange={(v) => setFormData(prev => ({ ...prev, lesson_id: v === "none" ? "" : v }))}
                disabled={!formData.chapter_id}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecciona lección" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="none">Ninguna</SelectItem>
                  {lessons.map(l => (
                    <SelectItem key={l.id} value={l.id}>{l.title}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="mb-4">
            <Label>Dificultad</Label>
            <Select
              value={formData.difficulty}
              onValueChange={(v) => setFormData(prev => ({ ...prev, difficulty: v }))}
            >
              <SelectTrigger className="w-48">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="fácil">Fácil</SelectItem>
                <SelectItem value="medio">Medio</SelectItem>
                <SelectItem value="difícil">Difícil</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Editor Grid */}
          <div className={`grid gap-4 ${chatOpen ? 'grid-cols-3' : 'grid-cols-2'}`}>
            {/* Left: Editor */}
            <div className="space-y-4">
              <div>
                <div className="flex items-center justify-between mb-1">
                  <Label>Enunciado (Markdown + LaTeX)</Label>
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
                        onClick={() => setChatOpen(!chatOpen)}
                        data-testid="toggle-remy-chat"
                      >
                        <MessageSquare size={14} className="mr-1" />
                        {chatOpen ? 'Cerrar' : 'Remy'}
                      </Button>
                    )}
                  </div>
                </div>
                <Textarea
                  ref={questionTextareaRef}
                  value={formData.question_text}
                  onChange={(e) => setFormData(prev => ({ ...prev, question_text: e.target.value }))}
                  placeholder="Usa $fórmula$ para LaTeX..."
                  className="h-24 font-mono text-sm"
                />
              </div>
              
              <div>
                <Label>Opciones (A, B, C, D)</Label>
                <div className="space-y-2 mt-1">
                  {formData.options.map((opt, idx) => {
                    const letter = String.fromCharCode(65 + idx);
                    return (
                      <div key={idx} className="flex items-center gap-2">
                        <span className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                          formData.correct_answer === letter 
                            ? 'bg-green-500 text-white' 
                            : 'bg-slate-200 text-slate-700'
                        }`}>
                          {letter}
                        </span>
                        <Input
                          value={opt.startsWith(`${letter}) `) ? opt.substring(3) : opt}
                          onChange={(e) => {
                            const newOpts = [...formData.options];
                            newOpts[idx] = `${letter}) ${e.target.value}`;
                            setFormData(prev => ({ ...prev, options: newOpts }));
                          }}
                          placeholder={`Opción ${letter}`}
                          className="flex-1 font-mono text-sm"
                        />
                        <Button
                          type="button"
                          variant={formData.correct_answer === letter ? "default" : "outline"}
                          size="sm"
                          onClick={() => setFormData(prev => ({ ...prev, correct_answer: letter }))}
                        >
                          ✓
                        </Button>
                      </div>
                    );
                  })}
                </div>
              </div>
              
              <div>
                <div className="flex items-center justify-between mb-1">
                  <Label>Explicación</Label>
                  <Button type="button" variant="ghost" size="sm" onClick={() => openImageDialog('explanation')}>
                    <Image size={14} className="mr-1" />
                    Imagen
                  </Button>
                </div>
                <Textarea
                  ref={explanationTextareaRef}
                  value={formData.explanation}
                  onChange={(e) => setFormData(prev => ({ ...prev, explanation: e.target.value }))}
                  placeholder="Explica la solución..."
                  className="h-24 font-mono text-sm"
                />
              </div>
            </div>

            {/* Middle: Preview */}
            <div className="border rounded-lg p-4 bg-white overflow-y-auto max-h-[450px]">
              <h3 className="text-sm font-medium text-slate-500 mb-3">Vista Previa</h3>
              <div className="space-y-4">
                <QuestionContent content={formData.question_text || '*Escribe el enunciado...*'} />
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
              </div>
            </div>

            {/* Right: Chat with Remy */}
            {chatOpen && (
              <div className="h-[450px]">
                <RemyChat
                  isOpen={chatOpen}
                  onClose={() => setChatOpen(false)}
                  currentContent={getQuestionContentForChat()}
                  onContentUpdate={handleQuestionContentUpdate}
                  context={{
                    type: 'question',
                    courseTitle: course.title,
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

          <div className="flex justify-end gap-2 mt-4">
            <Button variant="outline" onClick={() => setEditorOpen(false)}>
              Cancelar
            </Button>
            <Button onClick={handleSaveQuestion}>
              {editingQuestion ? 'Guardar Cambios' : 'Crear Pregunta'}
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      {/* ==================== GENERATOR DIALOG ==================== */}
      <Dialog open={generatorOpen} onOpenChange={setGeneratorOpen}>
        <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Sparkles className="text-primary" />
              Generar Preguntas con IA
            </DialogTitle>
          </DialogHeader>

          <Tabs value={generatorTab} onValueChange={setGeneratorTab}>
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="prompt" className="flex items-center gap-2">
                <Wand2 size={16} />
                Desde Tema/Prompt
              </TabsTrigger>
              <TabsTrigger value="pdf" className="flex items-center gap-2">
                <FileUp size={16} />
                Desde Documento PDF
              </TabsTrigger>
            </TabsList>

            {/* Common Settings */}
            <div className="grid grid-cols-3 gap-4 my-4">
              <div>
                <Label>Capítulo *</Label>
                <Select
                  value={generatorData.chapter_id}
                  onValueChange={(v) => setGeneratorData(prev => ({ ...prev, chapter_id: v, lesson_id: '' }))}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Selecciona capítulo" />
                  </SelectTrigger>
                  <SelectContent>
                    {generatorChapters.map(ch => (
                      <SelectItem key={ch.id} value={ch.id}>{ch.title}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label>Lección (opcional)</Label>
                <Select
                  value={generatorData.lesson_id || "none"}
                  onValueChange={(v) => setGeneratorData(prev => ({ ...prev, lesson_id: v === "none" ? "" : v }))}
                  disabled={!generatorData.chapter_id}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Todas" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="none">Ninguna</SelectItem>
                    {generatorLessons.map(l => (
                      <SelectItem key={l.id} value={l.id}>{l.title}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label>Dificultad</Label>
                <Select
                  value={generatorData.difficulty}
                  onValueChange={(v) => setGeneratorData(prev => ({ ...prev, difficulty: v }))}
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

            <TabsContent value="prompt" className="space-y-4">
              <div>
                <Label>Tema o Instrucciones para generar preguntas</Label>
                <Textarea
                  value={generatorData.topic}
                  onChange={(e) => setGeneratorData(prev => ({ ...prev, topic: e.target.value }))}
                  placeholder="Ej: Genera 3 preguntas sobre derivadas de funciones trigonométricas, incluyendo una sobre la derivada de sin(x) y otra sobre la regla de la cadena."
                  className="h-24"
                />
              </div>
              <div>
                <Label>Número de preguntas</Label>
                <Select
                  value={String(generatorData.num_questions)}
                  onValueChange={(v) => setGeneratorData(prev => ({ ...prev, num_questions: parseInt(v) }))}
                >
                  <SelectTrigger className="w-32">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(n => (
                      <SelectItem key={n} value={String(n)}>{n}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </TabsContent>

            <TabsContent value="pdf" className="space-y-4">
              <div>
                <Label>Documento PDF</Label>
                <div className="mt-2">
                  <input
                    type="file"
                    accept=".pdf"
                    onChange={handleUploadPdf}
                    className="hidden"
                    id="pdf-upload"
                  />
                  <label
                    htmlFor="pdf-upload"
                    className="flex items-center justify-center gap-2 p-4 border-2 border-dashed rounded-lg cursor-pointer hover:border-primary hover:bg-slate-50"
                  >
                    <Upload size={20} />
                    {pdfFile ? pdfFile.name : 'Arrastra o haz clic para subir PDF'}
                  </label>
                </div>
                {pdfText && (
                  <div className="mt-2 p-3 bg-green-50 text-green-700 rounded-lg text-sm">
                    ✓ PDF procesado ({pdfText.length} caracteres extraídos)
                  </div>
                )}
              </div>
              <div>
                <Label>Número de preguntas a generar</Label>
                <Select
                  value={String(generatorData.num_questions)}
                  onValueChange={(v) => setGeneratorData(prev => ({ ...prev, num_questions: parseInt(v) }))}
                >
                  <SelectTrigger className="w-32">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(n => (
                      <SelectItem key={n} value={String(n)}>{n}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </TabsContent>
          </Tabs>

          <Button 
            onClick={handleGenerateQuestions} 
            disabled={generatingQuestions}
            className="w-full"
          >
            {generatingQuestions ? (
              <>
                <div className="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full mr-2" />
                Generando preguntas...
              </>
            ) : (
              <>
                <Sparkles className="mr-2" size={18} />
                Generar Preguntas
              </>
            )}
          </Button>

          {/* Generated Questions Preview */}
          {generatedQuestions.length > 0 && (
            <div className="mt-6 space-y-4">
              <h3 className="font-semibold flex items-center gap-2">
                <CheckCircle className="text-green-500" size={20} />
                Preguntas Generadas ({generatedQuestions.length})
              </h3>
              <p className="text-sm text-slate-600">
                Revisa las preguntas y añádelas al banco o edítalas antes de guardar.
              </p>
              
              {generatedQuestions.map((q, idx) => (
                <Card key={idx} className="border-2 border-dashed">
                  <CardContent className="pt-4">
                    <div className="flex items-center justify-between mb-3">
                      <Badge className={getDifficultyBadge(generatorData.difficulty)}>
                        {generatorData.difficulty}
                      </Badge>
                      <span className="text-sm text-slate-500">
                        Respuesta correcta: {q.correct_answer}
                      </span>
                    </div>
                    
                    <div className="mb-3">
                      <QuestionContent content={q.question_text} />
                    </div>
                    
                    <div className="space-y-2 mb-3">
                      {q.options?.map((opt, optIdx) => (
                        <QuestionOption
                          key={optIdx}
                          option={opt}
                          isSelected={false}
                          isCorrect={q.correct_answer === String.fromCharCode(65 + optIdx)}
                          showResult={true}
                          disabled={true}
                        />
                      ))}
                    </div>
                    
                    {q.explanation && (
                      <ExplanationBlock explanation={q.explanation} />
                    )}
                    
                    <div className="flex gap-2 mt-4 pt-4 border-t">
                      <Button 
                        onClick={() => handleAddGeneratedQuestion(q, idx)}
                        className="flex-1"
                      >
                        <Plus size={16} className="mr-1" />
                        Añadir al Banco
                      </Button>
                      <Button 
                        variant="outline"
                        onClick={() => handleEditGeneratedQuestion(q, idx)}
                        className="flex-1"
                      >
                        <Edit size={16} className="mr-1" />
                        Editar con Remy
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </DialogContent>
      </Dialog>

      {/* ==================== IMAGE DIALOG ==================== */}
      <Dialog open={imageDialogOpen} onOpenChange={setImageDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Insertar Imagen</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label>Descripción de la imagen a generar</Label>
              <Textarea
                value={imagePrompt}
                onChange={(e) => setImagePrompt(e.target.value)}
                placeholder="Ej: Gráfico de la función f(x) = x² con su derivada"
                className="h-24"
              />
            </div>
            <Button 
              onClick={handleGenerateImage} 
              disabled={generatingImage}
              className="w-full"
            >
              {generatingImage ? 'Generando...' : 'Generar Imagen con IA'}
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

// ==================== MAIN COMPONENT ====================
const AdminQuestions = () => {
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    try {
      const token = localStorage.getItem('admin_token');
      const coursesRes = await axios.get(`${API}/courses`);
      
      // Get question count for each course
      const coursesWithCounts = await Promise.all(
        coursesRes.data.map(async (course) => {
          try {
            const questionsRes = await axios.get(`${ADMIN_API}/questions?course_id=${course.id}`, {
              headers: { Authorization: `Bearer ${token}` }
            });
            return { ...course, questionCount: questionsRes.data.length };
          } catch {
            return { ...course, questionCount: 0 };
          }
        })
      );
      
      setCourses(coursesWithCounts);
    } catch (error) {
      console.error('Error fetching courses:', error);
      toast.error('Error al cargar cursos');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-12">Cargando...</div>;
  }

  if (selectedCourse) {
    return (
      <QuestionManager 
        course={selectedCourse} 
        onBack={() => {
          setSelectedCourse(null);
          fetchCourses(); // Refresh counts
        }} 
      />
    );
  }

  return (
    <CourseSelector 
      courses={courses} 
      onSelectCourse={setSelectedCourse} 
    />
  );
};

export default AdminQuestions;
