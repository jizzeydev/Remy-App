import { useState, useEffect } from 'react';
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
import { Plus, Edit, Trash2, Sparkles, FileText, Filter } from 'lucide-react';
import { InlineMath } from 'react-katex';
import 'katex/dist/katex.min.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const ADMIN_API = `${BACKEND_URL}/api/admin`;

const AdminQuestions = () => {
  const [questions, setQuestions] = useState([]);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [pdfDialogOpen, setPdfDialogOpen] = useState(false);
  const [editingQuestion, setEditingQuestion] = useState(null);
  const [pdfFile, setPdfFile] = useState(null);
  const [pdfText, setPdfText] = useState('');
  const [generatingQuestions, setGeneratingQuestions] = useState(false);
  const [generatedQuestions, setGeneratedQuestions] = useState([]);
  const [filterCourse, setFilterCourse] = useState('');
  const [filterTopic, setFilterTopic] = useState('');

  const [formData, setFormData] = useState({
    course_id: '',
    topic: '',
    subtopic: '',
    difficulty: 'medio',
    question_text: '',
    options: ['', '', '', ''],
    correct_answer: 'A',
    explanation: '',
    latex_content: ''
  });

  const [generatorData, setGeneratorData] = useState({
    course_id: '',
    topic: '',
    num_questions: 5
  });

  useEffect(() => {
    fetchQuestions();
    fetchCourses();
  }, []);

  const fetchQuestions = async () => {
    try {
      const token = localStorage.getItem('admin_token');
      const params = new URLSearchParams();
      if (filterCourse) params.append('course_id', filterCourse);
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const token = localStorage.getItem('admin_token');
      const payload = {
        ...formData,
        id: editingQuestion?.id || undefined,
        options: formData.options.filter(opt => opt.trim() !== '')
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
    setFormData({
      course_id: question.course_id,
      topic: question.topic,
      subtopic: question.subtopic || '',
      difficulty: question.difficulty,
      question_text: question.question_text,
      options: question.options,
      correct_answer: question.correct_answer,
      explanation: question.explanation,
      latex_content: question.latex_content || ''
    });
    setDialogOpen(true);
  };

  const resetForm = () => {
    setEditingQuestion(null);
    setFormData({
      course_id: '',
      topic: '',
      subtopic: '',
      difficulty: 'medio',
      question_text: '',
      options: ['', '', '', ''],
      correct_answer: 'A',
      explanation: '',
      latex_content: ''
    });
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
      toast.success(`${response.data.questions.length} preguntas generadas con Gemini`);
    } catch (error) {
      console.error('Error generating questions:', error);
      toast.error('Error al generar preguntas con Gemini');
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
          topic: generatorData.topic,
          subtopic: '',
          difficulty: question.difficulty || 'medio',
          question_text: question.question_text,
          options: question.options,
          correct_answer: question.correct_answer,
          explanation: question.explanation,
          latex_content: question.latex_content || ''
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      toast.success('Pregunta guardada en el banco');
      fetchQuestions();
    } catch (error) {
      console.error('Error saving generated question:', error);
      toast.error('Error al guardar pregunta');
    }
  };

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
            <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle>Generar Preguntas con Gemini</DialogTitle>
              </DialogHeader>
              <Tabs defaultValue="upload">
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="upload">1. Subir PDF</TabsTrigger>
                  <TabsTrigger value="generate">2. Generar</TabsTrigger>
                </TabsList>
                <TabsContent value="upload" className="space-y-4">
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
                      <Textarea value={pdfText} readOnly className="h-32 text-xs" />
                    </div>
                  )}
                </TabsContent>
                <TabsContent value="generate" className="space-y-4">
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
                      placeholder="Ej: Derivadas"
                    />
                  </div>
                  <div>
                    <Label>Cantidad de preguntas</Label>
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
                    {generatingQuestions ? 'Generando con Gemini...' : 'Generar Preguntas'}
                  </Button>
                  {generatedQuestions.length > 0 && (
                    <div className="space-y-4 mt-4">
                      <h3 className="font-semibold">Preguntas Generadas ({generatedQuestions.length})</h3>
                      {generatedQuestions.map((q, idx) => (
                        <Card key={idx}>
                          <CardContent className="pt-4">
                            <p className="font-medium mb-2">{idx + 1}. {q.question_text}</p>
                            <div className="space-y-1 text-sm mb-2">
                              {q.options?.map((opt, i) => (
                                <p key={i} className={opt.charAt(0) === q.correct_answer ? 'text-green-600 font-medium' : ''}>
                                  {opt}
                                </p>
                              ))}
                            </div>
                            <p className="text-xs text-slate-600 mb-2"><strong>Explicación:</strong> {q.explanation}</p>
                            <Button size="sm" onClick={() => handleSaveGeneratedQuestion(q)}>
                              Guardar en banco
                            </Button>
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
            <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle>{editingQuestion ? 'Editar Pregunta' : 'Nueva Pregunta'}</DialogTitle>
              </DialogHeader>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <Label>Curso</Label>
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
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <Label>Tema</Label>
                    <Input
                      value={formData.topic}
                      onChange={(e) => setFormData({ ...formData, topic: e.target.value })}
                      required
                    />
                  </div>
                  <div>
                    <Label>Subtema (opcional)</Label>
                    <Input
                      value={formData.subtopic}
                      onChange={(e) => setFormData({ ...formData, subtopic: e.target.value })}
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
                <div>
                  <Label>Pregunta</Label>
                  <Textarea
                    value={formData.question_text}
                    onChange={(e) => setFormData({ ...formData, question_text: e.target.value })}
                    required
                  />
                </div>
                <div>
                  <Label>Opciones</Label>
                  {formData.options.map((opt, idx) => (
                    <Input
                      key={idx}
                      value={opt}
                      onChange={(e) => {
                        const newOpts = [...formData.options];
                        newOpts[idx] = e.target.value;
                        setFormData({ ...formData, options: newOpts });
                      }}
                      placeholder={`${String.fromCharCode(65 + idx)}) Opción ${idx + 1}`}
                      className="mt-2"
                    />
                  ))}
                </div>
                <div>
                  <Label>Respuesta Correcta</Label>
                  <Select
                    value={formData.correct_answer}
                    onValueChange={(value) => setFormData({ ...formData, correct_answer: value })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="A">A</SelectItem>
                      <SelectItem value="B">B</SelectItem>
                      <SelectItem value="C">C</SelectItem>
                      <SelectItem value="D">D</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label>Explicación</Label>
                  <Textarea
                    value={formData.explanation}
                    onChange={(e) => setFormData({ ...formData, explanation: e.target.value })}
                    required
                  />
                </div>
                <div>
                  <Label>LaTeX (opcional)</Label>
                  <Input
                    value={formData.latex_content}
                    onChange={(e) => setFormData({ ...formData, latex_content: e.target.value })}
                    placeholder="Fórmula en LaTeX"
                  />
                  {formData.latex_content && (
                    <div className="mt-2 p-2 bg-slate-50 rounded">
                      <InlineMath math={formData.latex_content} />
                    </div>
                  )}
                </div>
                <Button type="submit" className="w-full" disabled={loading}>
                  {loading ? 'Guardando...' : editingQuestion ? 'Actualizar' : 'Crear'}
                </Button>
              </form>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Filter size={20} />
            Filtros
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <Label>Curso</Label>
              <Select value={filterCourse} onValueChange={setFilterCourse}>
                <SelectTrigger>
                  <SelectValue placeholder="Todos los cursos" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">Todos</SelectItem>
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

      <div className="grid grid-cols-1 gap-4">
        <p className="text-sm text-slate-600">Total: {questions.length} preguntas en el banco</p>
        {questions.map((question, idx) => (
          <Card key={question.id}>
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <CardTitle className="text-base">
                    {idx + 1}. {question.question_text}
                  </CardTitle>
                  <div className="flex items-center gap-2 mt-2">
                    <span className="text-xs bg-primary/10 text-primary px-2 py-1 rounded">
                      {question.topic}
                    </span>
                    {question.subtopic && (
                      <span className="text-xs bg-slate-100 text-slate-600 px-2 py-1 rounded">
                        {question.subtopic}
                      </span>
                    )}
                    <span className={`text-xs px-2 py-1 rounded ${
                      question.difficulty === 'fácil' ? 'bg-green-100 text-green-700' :
                      question.difficulty === 'medio' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-red-100 text-red-700'
                    }`}>
                      {question.difficulty}
                    </span>
                  </div>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 mb-3">
                {question.options?.map((opt, i) => (
                  <p key={i} className={`text-sm ${
                    opt.charAt(0) === question.correct_answer ? 'text-green-600 font-medium' : ''
                  }`}>
                    {opt} {opt.charAt(0) === question.correct_answer && '✓'}
                  </p>
                ))}
              </div>
              {question.latex_content && (
                <div className="bg-slate-50 p-2 rounded mb-3">
                  <InlineMath math={question.latex_content} />
                </div>
              )}
              <div className="bg-blue-50 border border-blue-200 rounded p-3 mb-3">
                <p className="text-xs font-semibold text-blue-900 mb-1">Explicación:</p>
                <p className="text-sm text-blue-800">{question.explanation}</p>
              </div>
              <div className="flex gap-2">
                <Button size="sm" variant="outline" onClick={() => handleEdit(question)} className="flex-1">
                  <Edit size={16} className="mr-1" />
                  Editar
                </Button>
                <Button size="sm" variant="destructive" onClick={() => handleDelete(question.id)}>
                  <Trash2 size={16} />
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default AdminQuestions;
