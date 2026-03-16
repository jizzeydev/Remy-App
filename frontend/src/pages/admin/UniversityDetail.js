import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
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
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion';
import {
  Building2, Plus, Edit, Trash2, ChevronLeft,
  BookOpen, ClipboardList, FileText, Sparkles,
  Loader2, Upload, Target
} from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/admin/universities`;

const UniversityDetail = () => {
  const { universityId } = useParams();
  const navigate = useNavigate();
  
  const [university, setUniversity] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [selectedEvaluation, setSelectedEvaluation] = useState(null);
  
  // Dialog states
  const [showCourseDialog, setShowCourseDialog] = useState(false);
  const [showEvaluationDialog, setShowEvaluationDialog] = useState(false);
  const [showQuestionDialog, setShowQuestionDialog] = useState(false);
  const [showAIGenerateDialog, setShowAIGenerateDialog] = useState(false);
  const [saving, setSaving] = useState(false);
  
  // Form states
  const [courseForm, setCourseForm] = useState({ name: '', code: '', description: '', department: '' });
  const [evaluationForm, setEvaluationForm] = useState({ name: '', description: '', year: '', semester: '' });
  const [questionForm, setQuestionForm] = useState({
    question_content: '',
    question_type: 'multiple_choice',
    options: ['', '', '', ''],
    correct_answer: '',
    solution_content: '',
    difficulty: 'medio',
    topic: '',
    tags: []
  });
  const [aiPrompt, setAiPrompt] = useState('');
  const [aiNumQuestions, setAiNumQuestions] = useState(5);
  const [generating, setGenerating] = useState(false);
  const [pdfFile, setPdfFile] = useState(null);
  const [uploadingPdf, setUploadingPdf] = useState(false);
  const [pdfText, setPdfText] = useState('');
  
  // Questions list
  const [questions, setQuestions] = useState([]);

  useEffect(() => {
    fetchUniversity();
  }, [universityId]);

  useEffect(() => {
    if (selectedEvaluation) {
      fetchQuestions(selectedEvaluation.id);
    }
  }, [selectedEvaluation]);

  const fetchUniversity = async () => {
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.get(`${API}/${universityId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUniversity(response.data);
    } catch (error) {
      console.error('Error fetching university:', error);
      toast.error('Error al cargar universidad');
      navigate('/admin/universities');
    } finally {
      setLoading(false);
    }
  };

  const fetchCourseDetails = async (courseId) => {
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.get(`${API}/${universityId}/courses/${courseId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setSelectedCourse(response.data);
    } catch (error) {
      console.error('Error fetching course:', error);
    }
  };

  const fetchQuestions = async (evaluationId) => {
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.get(
        `${API}/${universityId}/courses/${selectedCourse.id}/evaluations/${evaluationId}/questions`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setQuestions(response.data);
    } catch (error) {
      console.error('Error fetching questions:', error);
    }
  };

  // Course CRUD
  const handleCreateCourse = async () => {
    if (!courseForm.name.trim()) {
      toast.error('El nombre del curso es requerido');
      return;
    }
    
    setSaving(true);
    try {
      const token = localStorage.getItem('admin_token');
      await axios.post(`${API}/${universityId}/courses`, courseForm, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      toast.success('Curso creado');
      setShowCourseDialog(false);
      setCourseForm({ name: '', code: '', description: '', department: '' });
      fetchUniversity();
    } catch (error) {
      toast.error('Error al crear curso');
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteCourse = async (courseId) => {
    if (!window.confirm('¿Eliminar este curso y todas sus evaluaciones?')) return;
    
    try {
      const token = localStorage.getItem('admin_token');
      await axios.delete(`${API}/${universityId}/courses/${courseId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      toast.success('Curso eliminado');
      setSelectedCourse(null);
      fetchUniversity();
    } catch (error) {
      toast.error('Error al eliminar curso');
    }
  };

  // Evaluation CRUD
  const handleCreateEvaluation = async () => {
    if (!evaluationForm.name.trim()) {
      toast.error('El nombre de la evaluación es requerido');
      return;
    }
    
    setSaving(true);
    try {
      const token = localStorage.getItem('admin_token');
      await axios.post(
        `${API}/${universityId}/courses/${selectedCourse.id}/evaluations`,
        {
          ...evaluationForm,
          year: evaluationForm.year ? parseInt(evaluationForm.year) : null,
          semester: evaluationForm.semester ? parseInt(evaluationForm.semester) : null
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      toast.success('Evaluación creada');
      setShowEvaluationDialog(false);
      setEvaluationForm({ name: '', description: '', year: '', semester: '' });
      fetchCourseDetails(selectedCourse.id);
    } catch (error) {
      toast.error('Error al crear evaluación');
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteEvaluation = async (evaluationId) => {
    if (!window.confirm('¿Eliminar esta evaluación y todas sus preguntas?')) return;
    
    try {
      const token = localStorage.getItem('admin_token');
      await axios.delete(
        `${API}/${universityId}/courses/${selectedCourse.id}/evaluations/${evaluationId}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      toast.success('Evaluación eliminada');
      setSelectedEvaluation(null);
      fetchCourseDetails(selectedCourse.id);
    } catch (error) {
      toast.error('Error al eliminar evaluación');
    }
  };

  // Question CRUD
  const handleCreateQuestion = async () => {
    if (!questionForm.question_content.trim()) {
      toast.error('El texto de la pregunta es requerido');
      return;
    }
    
    setSaving(true);
    try {
      const token = localStorage.getItem('admin_token');
      await axios.post(
        `${API}/${universityId}/courses/${selectedCourse.id}/evaluations/${selectedEvaluation.id}/questions`,
        {
          ...questionForm,
          options: questionForm.options.filter(o => o.trim()),
          source: 'manual'
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      toast.success('Pregunta creada');
      setShowQuestionDialog(false);
      resetQuestionForm();
      fetchQuestions(selectedEvaluation.id);
    } catch (error) {
      toast.error('Error al crear pregunta');
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteQuestion = async (questionId) => {
    if (!window.confirm('¿Eliminar esta pregunta?')) return;
    
    try {
      const token = localStorage.getItem('admin_token');
      await axios.delete(
        `${API}/${universityId}/courses/${selectedCourse.id}/evaluations/${selectedEvaluation.id}/questions/${questionId}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      toast.success('Pregunta eliminada');
      fetchQuestions(selectedEvaluation.id);
    } catch (error) {
      toast.error('Error al eliminar pregunta');
    }
  };

  // Handle PDF upload
  const handlePdfUpload = async (file) => {
    if (!file) return;
    
    if (file.type !== 'application/pdf') {
      toast.error('Solo se permiten archivos PDF');
      return;
    }
    
    setUploadingPdf(true);
    setPdfFile(file);
    
    try {
      const token = localStorage.getItem('admin_token');
      const formData = new FormData();
      formData.append('pdf_file', file);
      
      const response = await axios.post(
        `${API}/${universityId}/courses/${selectedCourse.id}/evaluations/${selectedEvaluation.id}/upload-pdf`,
        formData,
        {
          headers: { 
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          }
        }
      );
      
      if (response.data.success) {
        setPdfText(response.data.extracted_text);
        toast.success(`PDF procesado: ${response.data.text_length} caracteres extraídos`);
      }
    } catch (error) {
      console.error('Error uploading PDF:', error);
      toast.error(error.response?.data?.detail || 'Error al procesar el PDF');
      setPdfFile(null);
    } finally {
      setUploadingPdf(false);
    }
  };

  // AI Generation - Uses the university-specific endpoint
  const handleAIGenerate = async () => {
    // Check if we have either a prompt or PDF content
    if (!aiPrompt.trim() && !pdfText) {
      toast.error('Describe el tema o sube un PDF de examen anterior');
      return;
    }
    
    setGenerating(true);
    try {
      const token = localStorage.getItem('admin_token');
      
      // Determine generation type based on available content
      const generationType = pdfText ? 'pdf' : 'prompt';
      const content = pdfText || aiPrompt;
      
      // Use the university-specific generation endpoint
      const response = await axios.post(
        `${API}/${universityId}/courses/${selectedCourse.id}/evaluations/${selectedEvaluation.id}/generate`,
        {
          generation_type: generationType,
          prompt: generationType === 'prompt' ? content : null,
          pdf_content: generationType === 'pdf' ? content : null,
          num_questions: aiNumQuestions,
          difficulty: 'medio'
        },
        {
          headers: { Authorization: `Bearer ${token}` },
          timeout: 120000
        }
      );
      
      if (response.data.success && response.data.created_count > 0) {
        toast.success(`${response.data.created_count} preguntas generadas y guardadas`);
        setShowAIGenerateDialog(false);
        setAiPrompt('');
        setPdfFile(null);
        setPdfText('');
        fetchQuestions(selectedEvaluation.id);
      } else {
        toast.error('No se pudieron generar preguntas');
      }
    } catch (error) {
      console.error('Error generating questions:', error);
      toast.error(error.response?.data?.detail || 'Error al generar preguntas');
    } finally {
      setGenerating(false);
    }
  };

  const resetQuestionForm = () => {
    setQuestionForm({
      question_content: '',
      question_type: 'multiple_choice',
      options: ['', '', '', ''],
      correct_answer: '',
      solution_content: '',
      difficulty: 'medio',
      topic: '',
      tags: []
    });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="animate-spin text-cyan-500" size={32} />
      </div>
    );
  }

  if (!university) {
    return null;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Button variant="ghost" onClick={() => navigate('/admin/universities')} data-testid="back-btn">
          <ChevronLeft size={20} className="mr-1" />
          Volver
        </Button>
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 bg-gradient-to-br from-cyan-400 to-blue-600 rounded-lg flex items-center justify-center text-white font-bold text-xl">
            {university.short_name ? university.short_name.substring(0, 2) : university.name.charAt(0)}
          </div>
          <div>
            <h1 className="text-2xl font-bold">{university.name}</h1>
            {university.short_name && <Badge variant="outline">{university.short_name}</Badge>}
          </div>
        </div>
      </div>

      {/* Main Content - 3 Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Column 1: Courses */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center gap-2">
                <BookOpen size={20} className="text-cyan-500" />
                Cursos
              </CardTitle>
              <Button size="sm" onClick={() => setShowCourseDialog(true)} data-testid="add-course-btn">
                <Plus size={16} />
              </Button>
            </div>
          </CardHeader>
          <CardContent className="space-y-2">
            {university.courses?.length === 0 ? (
              <p className="text-slate-500 text-sm text-center py-4">No hay cursos</p>
            ) : (
              university.courses?.map((course) => (
                <div
                  key={course.id}
                  className={`p-3 rounded-lg cursor-pointer transition-all ${
                    selectedCourse?.id === course.id 
                      ? 'bg-cyan-50 border-2 border-cyan-500' 
                      : 'bg-slate-50 hover:bg-slate-100'
                  }`}
                  onClick={() => {
                    fetchCourseDetails(course.id);
                    setSelectedEvaluation(null);
                  }}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium">{course.name}</p>
                      {course.code && <p className="text-xs text-slate-500">{course.code}</p>}
                    </div>
                    <Badge variant="secondary">{course.evaluations_count || 0}</Badge>
                  </div>
                </div>
              ))
            )}
          </CardContent>
        </Card>

        {/* Column 2: Evaluations */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center gap-2">
                <ClipboardList size={20} className="text-purple-500" />
                Evaluaciones
              </CardTitle>
              {selectedCourse && (
                <Button size="sm" onClick={() => setShowEvaluationDialog(true)} data-testid="add-evaluation-btn">
                  <Plus size={16} />
                </Button>
              )}
            </div>
            {selectedCourse && (
              <CardDescription>
                {selectedCourse.name}
                <Button 
                  variant="ghost" 
                  size="sm" 
                  className="ml-2 text-red-500 hover:text-red-600"
                  onClick={() => handleDeleteCourse(selectedCourse.id)}
                >
                  <Trash2 size={14} />
                </Button>
              </CardDescription>
            )}
          </CardHeader>
          <CardContent className="space-y-2">
            {!selectedCourse ? (
              <p className="text-slate-500 text-sm text-center py-4">Selecciona un curso</p>
            ) : selectedCourse.evaluations?.length === 0 ? (
              <p className="text-slate-500 text-sm text-center py-4">No hay evaluaciones</p>
            ) : (
              selectedCourse.evaluations?.map((evaluation) => (
                <div
                  key={evaluation.id}
                  className={`p-3 rounded-lg cursor-pointer transition-all ${
                    selectedEvaluation?.id === evaluation.id 
                      ? 'bg-purple-50 border-2 border-purple-500' 
                      : 'bg-slate-50 hover:bg-slate-100'
                  }`}
                  onClick={() => setSelectedEvaluation(evaluation)}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium">{evaluation.name}</p>
                      {evaluation.year && (
                        <p className="text-xs text-slate-500">
                          {evaluation.year} {evaluation.semester && `- S${evaluation.semester}`}
                        </p>
                      )}
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge variant="secondary">{evaluation.questions_count || 0}</Badge>
                      <Button 
                        variant="ghost" 
                        size="sm" 
                        className="text-red-500 hover:text-red-600 p-1"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDeleteEvaluation(evaluation.id);
                        }}
                      >
                        <Trash2 size={14} />
                      </Button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </CardContent>
        </Card>

        {/* Column 3: Questions */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center gap-2">
                <Target size={20} className="text-orange-500" />
                Preguntas
              </CardTitle>
              {selectedEvaluation && (
                <div className="flex gap-2">
                  <Button size="sm" variant="outline" onClick={() => setShowAIGenerateDialog(true)} data-testid="ai-generate-btn">
                    <Sparkles size={16} className="mr-1" />
                    IA
                  </Button>
                  <Button size="sm" onClick={() => setShowQuestionDialog(true)} data-testid="add-question-btn">
                    <Plus size={16} />
                  </Button>
                </div>
              )}
            </div>
            {selectedEvaluation && (
              <CardDescription>{selectedEvaluation.name}</CardDescription>
            )}
          </CardHeader>
          <CardContent>
            {!selectedEvaluation ? (
              <p className="text-slate-500 text-sm text-center py-4">Selecciona una evaluación</p>
            ) : questions.length === 0 ? (
              <div className="text-center py-8">
                <Target className="mx-auto mb-3 text-slate-400" size={32} />
                <p className="text-slate-500 mb-4">No hay preguntas</p>
                <Button variant="outline" onClick={() => setShowAIGenerateDialog(true)}>
                  <Sparkles size={16} className="mr-2" />
                  Generar con IA
                </Button>
              </div>
            ) : (
              <div className="space-y-2 max-h-[400px] overflow-y-auto">
                {questions.map((q, index) => (
                  <div key={q.id} className="p-3 bg-slate-50 rounded-lg">
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium line-clamp-2">
                          {index + 1}. {q.question_content}
                        </p>
                        <div className="flex items-center gap-2 mt-2">
                          <Badge variant="outline" className="text-xs">
                            {q.difficulty}
                          </Badge>
                          {q.source?.includes('ai_generated') && (
                            <Badge variant="secondary" className="text-xs">
                              <Sparkles size={10} className="mr-1" />
                              IA
                            </Badge>
                          )}
                        </div>
                      </div>
                      <Button 
                        variant="ghost" 
                        size="sm"
                        className="text-red-500 hover:text-red-600"
                        onClick={() => handleDeleteQuestion(q.id)}
                      >
                        <Trash2 size={14} />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Create Course Dialog */}
      <Dialog open={showCourseDialog} onOpenChange={setShowCourseDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Nuevo Curso</DialogTitle>
            <DialogDescription>Agrega un curso a {university.name}</DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div>
              <Label>Nombre del Curso *</Label>
              <Input
                placeholder="Cálculo I"
                value={courseForm.name}
                onChange={(e) => setCourseForm({...courseForm, name: e.target.value})}
              />
            </div>
            <div>
              <Label>Código</Label>
              <Input
                placeholder="MAT1610"
                value={courseForm.code}
                onChange={(e) => setCourseForm({...courseForm, code: e.target.value})}
              />
            </div>
            <div>
              <Label>Departamento</Label>
              <Input
                placeholder="Matemáticas"
                value={courseForm.department}
                onChange={(e) => setCourseForm({...courseForm, department: e.target.value})}
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowCourseDialog(false)}>Cancelar</Button>
            <Button onClick={handleCreateCourse} disabled={saving}>
              {saving ? 'Creando...' : 'Crear Curso'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Create Evaluation Dialog */}
      <Dialog open={showEvaluationDialog} onOpenChange={setShowEvaluationDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Nueva Evaluación</DialogTitle>
            <DialogDescription>Agrega una evaluación a {selectedCourse?.name}</DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div>
              <Label>Nombre *</Label>
              <Input
                placeholder="I1, I2, Midterm, Exam..."
                value={evaluationForm.name}
                onChange={(e) => setEvaluationForm({...evaluationForm, name: e.target.value})}
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label>Año</Label>
                <Input
                  type="number"
                  placeholder="2024"
                  value={evaluationForm.year}
                  onChange={(e) => setEvaluationForm({...evaluationForm, year: e.target.value})}
                />
              </div>
              <div>
                <Label>Semestre</Label>
                <Input
                  type="number"
                  placeholder="1 o 2"
                  min="1"
                  max="2"
                  value={evaluationForm.semester}
                  onChange={(e) => setEvaluationForm({...evaluationForm, semester: e.target.value})}
                />
              </div>
            </div>
            <div>
              <Label>Descripción</Label>
              <Textarea
                placeholder="Contenido de la evaluación..."
                value={evaluationForm.description}
                onChange={(e) => setEvaluationForm({...evaluationForm, description: e.target.value})}
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowEvaluationDialog(false)}>Cancelar</Button>
            <Button onClick={handleCreateEvaluation} disabled={saving}>
              {saving ? 'Creando...' : 'Crear Evaluación'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Create Question Dialog */}
      <Dialog open={showQuestionDialog} onOpenChange={setShowQuestionDialog}>
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Nueva Pregunta</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div>
              <Label>Pregunta * (soporta LaTeX: $formula$)</Label>
              <Textarea
                placeholder="Escribe la pregunta... Usa $x^2$ para fórmulas LaTeX"
                value={questionForm.question_content}
                onChange={(e) => setQuestionForm({...questionForm, question_content: e.target.value})}
                rows={3}
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              {questionForm.options.map((opt, idx) => (
                <div key={idx}>
                  <Label>Opción {String.fromCharCode(65 + idx)}</Label>
                  <Input
                    value={opt}
                    onChange={(e) => {
                      const newOptions = [...questionForm.options];
                      newOptions[idx] = e.target.value;
                      setQuestionForm({...questionForm, options: newOptions});
                    }}
                  />
                </div>
              ))}
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label>Respuesta Correcta</Label>
                <Input
                  placeholder="A, B, C o D"
                  value={questionForm.correct_answer}
                  onChange={(e) => setQuestionForm({...questionForm, correct_answer: e.target.value.toUpperCase()})}
                />
              </div>
              <div>
                <Label>Dificultad</Label>
                <select
                  className="w-full h-10 rounded-md border border-input bg-background px-3"
                  value={questionForm.difficulty}
                  onChange={(e) => setQuestionForm({...questionForm, difficulty: e.target.value})}
                >
                  <option value="facil">Fácil</option>
                  <option value="medio">Medio</option>
                  <option value="dificil">Difícil</option>
                </select>
              </div>
            </div>
            <div>
              <Label>Solución/Explicación (soporta LaTeX)</Label>
              <Textarea
                placeholder="Explicación paso a paso..."
                value={questionForm.solution_content}
                onChange={(e) => setQuestionForm({...questionForm, solution_content: e.target.value})}
                rows={4}
              />
            </div>
            <div>
              <Label>Tema</Label>
              <Input
                placeholder="Derivadas, Integrales..."
                value={questionForm.topic}
                onChange={(e) => setQuestionForm({...questionForm, topic: e.target.value})}
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowQuestionDialog(false)}>Cancelar</Button>
            <Button onClick={handleCreateQuestion} disabled={saving}>
              {saving ? 'Guardando...' : 'Crear Pregunta'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* AI Generate Dialog */}
      <Dialog open={showAIGenerateDialog} onOpenChange={setShowAIGenerateDialog}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Sparkles className="text-cyan-500" />
              Generar Preguntas con IA
            </DialogTitle>
            <DialogDescription>
              Describe el tema o pega contenido de un examen anterior para generar preguntas similares
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div>
              <Label>Número de preguntas</Label>
              <Input
                type="number"
                min="1"
                max="20"
                value={aiNumQuestions}
                onChange={(e) => setAiNumQuestions(parseInt(e.target.value) || 5)}
              />
            </div>
            
            {/* PDF Upload Section */}
            <div className="border-2 border-dashed border-slate-300 rounded-lg p-4 bg-slate-50">
              <Label className="flex items-center gap-2 mb-2">
                <Upload size={16} />
                Subir PDF de examen anterior
              </Label>
              <input
                type="file"
                accept=".pdf"
                onChange={(e) => handlePdfUpload(e.target.files[0])}
                className="w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-cyan-50 file:text-cyan-700 hover:file:bg-cyan-100"
                disabled={uploadingPdf}
              />
              {uploadingPdf && (
                <div className="flex items-center gap-2 mt-2 text-sm text-slate-500">
                  <Loader2 className="animate-spin" size={14} />
                  Extrayendo texto del PDF...
                </div>
              )}
              {pdfFile && pdfText && (
                <div className="mt-2 p-2 bg-green-50 border border-green-200 rounded text-sm">
                  <p className="text-green-700 font-medium flex items-center gap-1">
                    <FileText size={14} />
                    {pdfFile.name}
                  </p>
                  <p className="text-green-600 text-xs mt-1">
                    {pdfText.length} caracteres extraídos - Listo para generar preguntas
                  </p>
                </div>
              )}
            </div>
            
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-white px-2 text-slate-500">O escribe manualmente</span>
              </div>
            </div>
            
            <div>
              <Label>Tema o contenido del examen</Label>
              <Textarea
                placeholder="Ej: Genera preguntas sobre derivadas e integrales, incluyendo aplicaciones a problemas de optimización..."
                value={aiPrompt}
                onChange={(e) => setAiPrompt(e.target.value)}
                rows={6}
                disabled={!!pdfText}
              />
              {pdfText && (
                <p className="text-xs text-amber-600 mt-1">
                  Campo deshabilitado porque ya subiste un PDF. Elimina el PDF para escribir manualmente.
                </p>
              )}
            </div>
            
            {pdfFile && (
              <Button 
                variant="outline" 
                size="sm"
                className="text-red-600"
                onClick={() => {
                  setPdfFile(null);
                  setPdfText('');
                }}
              >
                <Trash2 size={14} className="mr-1" />
                Eliminar PDF
              </Button>
            )}
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => {
              setShowAIGenerateDialog(false);
              setPdfFile(null);
              setPdfText('');
              setAiPrompt('');
            }}>Cancelar</Button>
            <Button onClick={handleAIGenerate} disabled={generating || uploadingPdf || (!aiPrompt.trim() && !pdfText)}>
              {generating ? (
                <>
                  <Loader2 className="animate-spin mr-2" size={16} />
                  Generando...
                </>
              ) : (
                <>
                  <Sparkles size={16} className="mr-2" />
                  Generar {aiNumQuestions} Preguntas
                </>
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default UniversityDetail;
