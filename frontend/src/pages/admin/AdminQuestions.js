import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { toast } from 'sonner';
import InlineMd from '@/components/course/InlineMd';
import {
  Plus, Edit, Trash2, FileText, Upload,
  ArrowLeft, BookOpen, Layers, HelpCircle,
  ChevronDown, ChevronRight, Loader2,
  Search, Filter, Building2,
  Link2, GitFork, EyeOff, Undo2
} from 'lucide-react';
import { QuestionContent, QuestionOption, ExplanationBlock } from '@/components/course/QuestionRenderer';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const ADMIN_API = `${BACKEND_URL}/api/admin`;

// ==================== COURSE SELECTOR VIEW ====================
const CourseSelector = ({ courses, universities, onSelectCourse, searchTerm, setSearchTerm, filterUniversity, setFilterUniversity }) => {
  // Apply filters
  let filteredCourses = [...courses];
  
  if (searchTerm) {
    filteredCourses = filteredCourses.filter(c => 
      c.title.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }
  
  if (filterUniversity && filterUniversity !== 'all') {
    if (filterUniversity === 'general') {
      filteredCourses = filteredCourses.filter(c => !c.university_id);
    } else {
      filteredCourses = filteredCourses.filter(c => c.university_id === filterUniversity);
    }
  }
  
  return (
    <div className="space-y-6" data-testid="questions-course-selector">
      <div>
        <h1 className="text-3xl font-bold">Banco de Preguntas</h1>
        <p className="text-slate-600 dark:text-slate-400 mt-1">Selecciona un curso para gestionar sus preguntas</p>
      </div>
      
      {/* Filters */}
      <div className="flex flex-wrap gap-4 items-center">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
          <Input
            placeholder="Buscar cursos..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
            data-testid="question-course-search"
          />
        </div>
        <div className="flex items-center gap-2">
          <Filter size={18} className="text-slate-500" />
          <Select value={filterUniversity} onValueChange={setFilterUniversity}>
            <SelectTrigger className="w-[200px]" data-testid="question-filter-university">
              <SelectValue placeholder="Filtrar por universidad" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todas las universidades</SelectItem>
              <SelectItem value="general">
                <span className="flex items-center gap-2">
                  <Building2 size={14} />
                  General
                </span>
              </SelectItem>
              {universities.map((uni) => (
                <SelectItem key={uni.id} value={uni.id}>
                  {uni.short_name} - {uni.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <div className="text-sm text-slate-500">
          {filteredCourses.length} de {courses.length} cursos
        </div>
      </div>

      {filteredCourses.length === 0 ? (
        <Card className="text-center py-12">
          <CardContent>
            <BookOpen className="mx-auto mb-4 text-slate-400" size={48} />
            <h3 className="text-xl font-semibold mb-2">
              {courses.length === 0 ? 'No hay cursos disponibles' : 'No se encontraron cursos'}
            </h3>
            <p className="text-slate-500">
              {courses.length === 0 ? 'Primero crea un curso en la sección de Cursos' : 'Prueba con otros filtros'}
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredCourses.map((course) => (
            <Card
              key={course.id}
              className="cursor-pointer hover:shadow-lg hover:border-primary transition-all"
              onClick={() => onSelectCourse(course)}
              data-testid={`course-card-${course.id}`}
            >
              <CardHeader>
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <Badge variant="outline">{course.level}</Badge>
                    {course.university ? (
                      <Badge variant="secondary" className="text-xs">
                        {course.university.short_name === 'GEN' ? 'General' : course.university.short_name}
                      </Badge>
                    ) : (
                      <Badge variant="secondary" className="text-xs">General</Badge>
                    )}
                  </div>
                  <span className="text-sm text-slate-500 flex items-center gap-1">
                    <HelpCircle size={14} />
                    {course.questionCount || 0}
                  </span>
                </div>
                <CardTitle>{course.title}</CardTitle>
                <CardDescription className="line-clamp-2">
                  <InlineMd>{course.description}</InlineMd>
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
  const [editingQuestion, setEditingQuestion] = useState(null);

  // CSV import state
  const [csvImportOpen, setCsvImportOpen] = useState(false);
  const [csvFile, setCsvFile] = useState(null);
  const [importingCsv, setImportingCsv] = useState(false);

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

  useEffect(() => {
    fetchData();
  }, [course.id]);

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

  const getUncategorizedQuestions = () => {
    return questions.filter(q => !q.chapter_id);
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

  // Smart delete that mirrors the lesson dispatch in CourseContentEditor.
  // Inherited template question → exclude from this course (template intact).
  // Override (forked) → revert by deleting the local override.
  // Pure local → real DELETE.
  const handleDeleteQuestion = async (chapter, question) => {
    const token = localStorage.getItem('admin_token');
    const headers = { Authorization: `Bearer ${token}` };

    try {
      if (chapter?.is_linked && question.inherited_from_template && !question.overrides_template) {
        if (!window.confirm('¿Excluir esta pregunta de este curso? La pregunta queda intacta en el curso general.')) return;
        await axios.post(
          `${ADMIN_API}/chapters/${chapter.id}/exclude-questions`,
          { ids: [question.id] },
          { headers }
        );
        toast.success('Pregunta excluida de este curso');
      } else if (question.overrides_template) {
        if (!window.confirm('¿Revertir esta pregunta a la versión general? Se perderán los cambios locales.')) return;
        await axios.delete(`${ADMIN_API}/questions/${question.id}`, { headers });
        toast.success('Revertida a la versión general');
      } else {
        if (!window.confirm('¿Eliminar esta pregunta?')) return;
        await axios.delete(`${ADMIN_API}/questions/${question.id}`, { headers });
        toast.success('Pregunta eliminada');
      }
      fetchData();
    } catch (error) {
      console.error('Error deleting question:', error);
      toast.error(error.response?.data?.detail || 'Error al eliminar pregunta');
    }
  };

  // Fork an inherited question into a course-specific override, then open the
  // editor on the fork. Idempotent server-side.
  const handleForkAndEditQuestion = async (chapter, templateQuestion) => {
    try {
      const token = localStorage.getItem('admin_token');
      const res = await axios.post(
        `${ADMIN_API}/chapters/${chapter.id}/fork-question/${templateQuestion.id}`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      const fork = res.data.question;
      if (res.data.created) toast.success('Pregunta clonada localmente, ahora podés editarla.');
      await fetchData();
      openEditQuestion(fork);
    } catch (error) {
      console.error('Error forking question:', error);
      toast.error(error.response?.data?.detail || 'Error al clonar pregunta');
    }
  };

  // ==================== CSV IMPORT ====================
  const handleCsvImport = async () => {
    if (!csvFile) {
      toast.error('Selecciona un archivo CSV');
      return;
    }
    
    setImportingCsv(true);
    try {
      const token = localStorage.getItem('admin_token');
      const formData = new FormData();
      formData.append('csv_file', csvFile);
      
      const response = await axios.post(
        `${ADMIN_API}/questions/import-csv/${course.id}`,
        formData,
        { 
          headers: { 
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          } 
        }
      );
      
      if (response.data.success) {
        toast.success(`${response.data.created_count} preguntas importadas correctamente`);
        if (response.data.errors_count > 0) {
          toast.warning(`${response.data.errors_count} errores durante la importación`);
          console.log('Import errors:', response.data.errors);
        }
        setCsvImportOpen(false);
        setCsvFile(null);
        fetchData(); // Refresh questions
      }
    } catch (error) {
      console.error('Error importing CSV:', error);
      toast.error(error.response?.data?.detail || 'Error al importar CSV');
    } finally {
      setImportingCsv(false);
    }
  };

  const handleDownloadCsvTemplate = async () => {
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.get(
        `${ADMIN_API}/questions/csv-template`,
        { 
          headers: { Authorization: `Bearer ${token}` },
          responseType: 'blob'
        }
      );
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `plantilla_preguntas_${course.id}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      toast.success('Plantilla descargada');
    } catch (error) {
      toast.error('Error al descargar plantilla');
    }
  };

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
          <Button variant="outline" onClick={() => setCsvImportOpen(true)}>
            <Upload size={18} className="mr-2" />
            Importar CSV
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
              <Card key={chapter.id} className={chapter.is_linked ? 'border-blue-300 dark:border-blue-700' : ''}>
                <CardHeader
                  className={`cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-800/50 ${chapter.is_linked ? 'bg-blue-50 dark:bg-blue-900/20' : ''}`}
                  onClick={() => toggleChapter(chapter.id)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      {isExpanded ? <ChevronDown size={20} /> : <ChevronRight size={20} />}
                      <CardTitle className="text-lg">{chapter.title}</CardTitle>
                      {chapter.is_linked && (
                        <Badge variant="secondary" className="text-xs bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300">
                          <Link2 size={11} className="mr-0.5" /> Heredado
                        </Badge>
                      )}
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
                        {chapterQuestions.map((question, idx) => {
                          const isInherited = question.inherited_from_template;
                          const isOverride = question.overrides_template;
                          return (
                          <div
                            key={question.id}
                            className={`border rounded-lg p-4 transition-colors ${
                              isOverride
                                ? 'border-amber-300 dark:border-amber-700 bg-amber-50/50 dark:bg-amber-900/10 hover:bg-amber-50 dark:hover:bg-amber-900/20'
                                : 'hover:bg-slate-50 dark:hover:bg-slate-800/50'
                            }`}
                          >
                            <div className="flex items-start justify-between gap-4">
                              <div className="flex-1 min-w-0">
                                <div className="flex items-center gap-2 mb-2 flex-wrap">
                                  <Badge className={getDifficultyBadge(question.difficulty)}>
                                    {question.difficulty}
                                  </Badge>
                                  {question.lesson_id && (
                                    <Badge variant="outline" className="text-xs">
                                      {lessons.find(l => l.id === question.lesson_id)?.title || 'Lección'}
                                    </Badge>
                                  )}
                                  {isInherited && !isOverride && (
                                    <Badge variant="secondary" className="text-[10px] bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300">
                                      <Link2 size={10} className="mr-0.5" /> Heredada
                                    </Badge>
                                  )}
                                  {isOverride && (
                                    <Badge variant="secondary" className="text-[10px] bg-amber-100 dark:bg-amber-900/40 text-amber-700 dark:text-amber-300">
                                      <GitFork size={10} className="mr-0.5" /> Editada localmente
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
                              <div className="flex gap-2 flex-shrink-0">
                                <Button
                                  size="sm"
                                  variant="ghost"
                                  onClick={() => isInherited && !isOverride
                                    ? handleForkAndEditQuestion(chapter, question)
                                    : openEditQuestion(question)
                                  }
                                  title={isInherited && !isOverride ? 'Clonar localmente y editar' : 'Editar'}
                                >
                                  {isInherited && !isOverride ? <GitFork size={16} /> : <Edit size={16} />}
                                </Button>
                                <Button
                                  size="sm"
                                  variant="ghost"
                                  className="text-red-600 hover:text-red-700"
                                  onClick={() => handleDeleteQuestion(chapter, question)}
                                  title={
                                    isInherited && !isOverride
                                      ? 'Excluir de este curso (no afecta general)'
                                      : isOverride
                                      ? 'Revertir a versión general'
                                      : 'Eliminar'
                                  }
                                >
                                  {isInherited && !isOverride ? <EyeOff size={16} /> : isOverride ? <Undo2 size={16} /> : <Trash2 size={16} />}
                                </Button>
                              </div>
                            </div>
                          </div>
                          );
                        })}
                        ))}
                      </div>
                    )}
                  </CardContent>
                )}
              </Card>
            );
          })
        )}
        
        {/* Uncategorized Questions Section */}
        {getUncategorizedQuestions().length > 0 && (
          <Card className="border-orange-200 bg-orange-50/30">
            <CardHeader 
              className="cursor-pointer hover:bg-orange-50"
              onClick={() => toggleChapter('uncategorized')}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  {expandedChapters['uncategorized'] ? <ChevronDown size={20} /> : <ChevronRight size={20} />}
                  <CardTitle className="text-lg text-orange-800">Sin Categorizar (Importadas CSV)</CardTitle>
                  <Badge className="bg-orange-200 text-orange-800">{getUncategorizedQuestions().length} preguntas</Badge>
                </div>
              </div>
            </CardHeader>
            
            {expandedChapters['uncategorized'] && (
              <CardContent className="pt-0">
                <p className="text-sm text-orange-700 mb-4 p-3 bg-orange-100 rounded-lg">
                  Estas preguntas fueron importadas sin capítulo asignado. Puedes editarlas para asignarles un capítulo.
                </p>
                <div className="space-y-3">
                  {getUncategorizedQuestions().map((question, idx) => (
                    <div 
                      key={question.id}
                      className="border border-orange-200 rounded-lg p-4 hover:bg-orange-50 transition-colors bg-white"
                    >
                      <div className="flex items-start justify-between gap-4">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <Badge className={getDifficultyBadge(question.difficulty)}>
                              {question.difficulty}
                            </Badge>
                            <Badge variant="outline" className="text-xs text-orange-600 border-orange-300">
                              CSV Import
                            </Badge>
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
                            onClick={() => handleDeleteQuestion(null, question)}
                          >
                            <Trash2 size={16} />
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            )}
          </Card>
        )}
      </div>

      {/* ==================== QUESTION EDITOR DIALOG ==================== */}
      <Dialog open={editorOpen} onOpenChange={setEditorOpen}>
        <DialogContent className="max-h-[90vh] overflow-y-auto max-w-5xl">
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
          <div className="grid gap-4 grid-cols-2">
            {/* Left: Editor */}
            <div className="space-y-4">
              <div>
                <Label>Enunciado (Markdown + LaTeX)</Label>
                <Textarea
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
                <Label>Explicación</Label>
                <Textarea
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

      {/* CSV Import Dialog */}
      <Dialog open={csvImportOpen} onOpenChange={setCsvImportOpen}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>Importar Preguntas desde CSV</DialogTitle>
            <DialogDescription>
              Sube un archivo CSV con preguntas para importarlas masivamente al curso
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-4">
            {/* Download Template Button */}
            <div className="bg-cyan-50 border border-cyan-200 rounded-lg p-4">
              <h4 className="font-medium text-sm mb-2">Formato CSV (columnas separadas):</h4>
              <p className="text-xs text-slate-600 mb-2 font-mono bg-white p-2 rounded border">
                capitulo, leccion, dificultad, enunciado, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta, explicacion
              </p>
              <Button 
                variant="outline" 
                size="sm"
                onClick={handleDownloadCsvTemplate}
                className="w-full"
              >
                <FileText size={16} className="mr-2" />
                Descargar Plantilla CSV
              </Button>
            </div>
            
            {/* File Upload */}
            <div>
              <Label htmlFor="csv-upload-questions">Archivo CSV</Label>
              <Input
                id="csv-upload-questions"
                type="file"
                accept=".csv"
                onChange={(e) => setCsvFile(e.target.files[0])}
                className="mt-1"
              />
              {csvFile && (
                <p className="text-sm text-green-600 mt-1">
                  Archivo seleccionado: {csvFile.name}
                </p>
              )}
            </div>
            
            {/* Tips */}
            <div className="text-xs text-slate-500 space-y-1">
              <p>• <strong>capitulo</strong> y <strong>leccion</strong>: Nombres tal como aparecen en el curso</p>
              <p>• <strong>dificultad</strong>: fácil, medio o difícil</p>
              <p>• <strong>opcion_a-d</strong>: Cada alternativa en su columna</p>
              <p>• <strong>respuesta_correcta</strong>: A, B, C o D</p>
              <p>• LaTeX: usa $ como delimitador (ej: $\frac{'{x}'}{'{2}'}$)</p>
            </div>
          </div>
          
          <DialogFooter>
            <Button variant="outline" onClick={() => setCsvImportOpen(false)}>
              Cancelar
            </Button>
            <Button onClick={handleCsvImport} disabled={!csvFile || importingCsv}>
              {importingCsv ? (
                <>
                  <Loader2 className="animate-spin mr-2" size={16} />
                  Importando...
                </>
              ) : (
                <>
                  <Upload size={16} className="mr-2" />
                  Importar
                </>
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

// ==================== MAIN COMPONENT ====================
const AdminQuestions = () => {
  const [courses, setCourses] = useState([]);
  const [universities, setUniversities] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterUniversity, setFilterUniversity] = useState('all');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const token = localStorage.getItem('admin_token');
      
      // Fetch courses and universities in parallel
      const [coursesRes, unisRes] = await Promise.all([
        axios.get(`${ADMIN_API}/courses`, {
          headers: { Authorization: `Bearer ${token}` }
        }),
        axios.get(`${API}/admin/library-universities`, {
          headers: { Authorization: `Bearer ${token}` }
        })
      ]);
      
      setUniversities(unisRes.data);
      
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
      console.error('Error fetching data:', error);
      toast.error('Error al cargar datos');
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
          fetchData(); // Refresh counts
        }} 
      />
    );
  }

  return (
    <CourseSelector 
      courses={courses}
      universities={universities}
      onSelectCourse={setSelectedCourse}
      searchTerm={searchTerm}
      setSearchTerm={setSearchTerm}
      filterUniversity={filterUniversity}
      setFilterUniversity={setFilterUniversity}
    />
  );
};

export default AdminQuestions;
