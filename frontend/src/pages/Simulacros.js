import { useState, useEffect, useRef, useCallback } from 'react';
import axios from 'axios';
import { 
  Plus, Loader2, Clock, Trash2, Play, CheckCircle, XCircle,
  ChevronDown, ChevronRight, BookOpen, Layers, Timer, Award
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import { Badge } from '@/components/ui/badge';
import { toast } from 'sonner';
import { QuestionContent, QuestionOption, ExplanationBlock } from '@/components/course/QuestionRenderer';
import SubscriptionRequired from '@/components/SubscriptionRequired';
import { useAuth } from '../contexts/AuthContext';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Get or create student ID
const getStudentId = () => {
  let studentId = localStorage.getItem('student_id');
  if (!studentId) {
    studentId = 'student_' + Date.now();
    localStorage.setItem('student_id', studentId);
  }
  return studentId;
};

// Format time as MM:SS
const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
};

// Get grade color based on Chilean scale
const getGradeColor = (grade) => {
  if (grade >= 6.0) return 'text-green-600 bg-green-100';
  if (grade >= 5.0) return 'text-blue-600 bg-blue-100';
  if (grade >= 4.0) return 'text-yellow-600 bg-yellow-100';
  return 'text-red-600 bg-red-100';
};

// ==================== QUIZ CARD COMPONENT ====================
const QuizCard = ({ quiz, onStart, onDelete }) => {
  const isCompleted = quiz.completed && quiz.grade !== null && quiz.grade !== undefined;
  
  return (
    <Card className="hover:shadow-lg transition-all" data-testid={`quiz-card-${quiz.id}`}>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <Badge variant="outline" className="text-xs">
            {quiz.difficulty || 'medio'}
          </Badge>
          {isCompleted && (
            <div className={`px-3 py-1 rounded-full font-bold ${getGradeColor(quiz.grade)}`}>
              Nota: {quiz.grade}
            </div>
          )}
        </div>
        <CardTitle className="text-lg mt-2">{quiz.topic || 'Simulacro'}</CardTitle>
        <CardDescription className="space-y-1">
          <span className="block">{quiz.course_title || 'Curso'}</span>
          <span className="block text-xs flex items-center gap-2">
            <BookOpen size={12} />
            {quiz.questions?.length || 0} preguntas
            {quiz.time_limit_minutes && (
              <>
                <Clock size={12} className="ml-2" />
                {quiz.time_limit_minutes} min
              </>
            )}
          </span>
          <span className="block text-xs text-slate-400">
            {quiz.created_at && new Date(quiz.created_at).toLocaleDateString('es-CL', {
              day: 'numeric',
              month: 'short',
              year: 'numeric'
            })}
          </span>
        </CardDescription>
      </CardHeader>
      <CardContent className="pt-0">
        <div className="flex gap-2">
          <Button
            onClick={() => onStart(quiz)}
            className="flex-1 rounded-full"
            variant={isCompleted ? "outline" : "default"}
          >
            <Play size={16} className="mr-2" />
            {isCompleted ? 'Reintentar' : 'Comenzar'}
          </Button>
          <Button
            variant="ghost"
            size="icon"
            className="text-red-500 hover:text-red-700 hover:bg-red-50"
            onClick={() => onDelete(quiz.id)}
          >
            <Trash2 size={18} />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

// ==================== CREATE QUIZ DIALOG ====================
const CreateQuizDialog = ({ open, onOpenChange, onQuizCreated }) => {
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [chapters, setChapters] = useState([]);
  const [selectedChapters, setSelectedChapters] = useState({});
  const [selectedLessons, setSelectedLessons] = useState({});
  const [expandedChapters, setExpandedChapters] = useState({});
  const [numQuestions, setNumQuestions] = useState("10");
  const [difficulty, setDifficulty] = useState("todos");
  const [timeLimit, setTimeLimit] = useState("none");
  const [loading, setLoading] = useState(false);
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    if (open) {
      fetchCourses();
    }
  }, [open]);

  useEffect(() => {
    if (selectedCourse) {
      fetchChaptersWithLessons(selectedCourse.id);
    } else {
      setChapters([]);
      setSelectedChapters({});
      setSelectedLessons({});
    }
  }, [selectedCourse]);

  const fetchCourses = async () => {
    try {
      const response = await axios.get(`${API}/courses`);
      setCourses(response.data);
    } catch (error) {
      console.error('Error fetching courses:', error);
    }
  };

  const fetchChaptersWithLessons = async (courseId) => {
    setLoading(true);
    try {
      const chaptersRes = await axios.get(`${API}/courses/${courseId}/chapters`);
      const chaptersWithLessons = await Promise.all(
        chaptersRes.data.map(async (chapter) => {
          const lessonsRes = await axios.get(`${API}/chapters/${chapter.id}/lessons`);
          return { ...chapter, lessons: lessonsRes.data };
        })
      );
      setChapters(chaptersWithLessons);
      
      // Initialize expanded state
      const expanded = {};
      chaptersWithLessons.forEach(ch => { expanded[ch.id] = false; });
      setExpandedChapters(expanded);
    } catch (error) {
      console.error('Error fetching chapters:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleChapter = (chapterId) => {
    setExpandedChapters(prev => ({
      ...prev,
      [chapterId]: !prev[chapterId]
    }));
  };

  const handleChapterToggle = (chapter, checked) => {
    setSelectedChapters(prev => ({
      ...prev,
      [chapter.id]: checked
    }));
    
    // Also toggle all lessons in this chapter
    const lessonUpdates = {};
    chapter.lessons?.forEach(lesson => {
      lessonUpdates[lesson.id] = checked;
    });
    setSelectedLessons(prev => ({ ...prev, ...lessonUpdates }));
  };

  const handleLessonToggle = (lesson, chapterId, checked) => {
    setSelectedLessons(prev => ({
      ...prev,
      [lesson.id]: checked
    }));
    
    // Update chapter selection based on lessons
    const chapter = chapters.find(ch => ch.id === chapterId);
    if (chapter) {
      const newLessonState = { ...selectedLessons, [lesson.id]: checked };
      const allLessonsSelected = chapter.lessons?.every(l => newLessonState[l.id]);
      const anyLessonSelected = chapter.lessons?.some(l => newLessonState[l.id]);
      
      setSelectedChapters(prev => ({
        ...prev,
        [chapterId]: allLessonsSelected || anyLessonSelected
      }));
    }
  };

  const getSelectedChapterIds = () => {
    return Object.entries(selectedChapters)
      .filter(([_, selected]) => selected)
      .map(([id]) => id);
  };

  const getSelectedLessonIds = () => {
    return Object.entries(selectedLessons)
      .filter(([_, selected]) => selected)
      .map(([id]) => id);
  };

  const handleCreate = async () => {
    const chapterIds = getSelectedChapterIds();
    const lessonIds = getSelectedLessonIds();
    
    if (!selectedCourse || (chapterIds.length === 0 && lessonIds.length === 0)) {
      toast.error('Selecciona un curso y al menos un capítulo o lección');
      return;
    }

    setCreating(true);
    try {
      const response = await axios.post(`${API}/quiz/start`, {
        user_id: getStudentId(),
        course_id: selectedCourse.id,
        chapter_ids: chapterIds,
        lesson_ids: lessonIds,
        difficulty: difficulty,
        num_questions: parseInt(numQuestions),
        time_limit_minutes: timeLimit !== "none" ? parseInt(timeLimit) : null
      });

      onQuizCreated({
        id: response.data.quiz_id,
        questions: response.data.questions,
        time_limit_minutes: response.data.time_limit_minutes,
        total_questions: response.data.total_questions,
        course_title: selectedCourse.title
      });
      
      toast.success('¡Simulacro creado!');
      onOpenChange(false);
      
      // Reset form
      setSelectedCourse(null);
      setSelectedChapters({});
      setSelectedLessons({});
      setNumQuestions("10");
      setDifficulty("todos");
      setTimeLimit("none");
    } catch (error) {
      console.error('Error creating quiz:', error);
      const errorMsg = error.response?.data?.detail || 'Error al crear el simulacro';
      toast.error(errorMsg);
    } finally {
      setCreating(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Award className="text-primary" />
            Crear Nuevo Simulacro
          </DialogTitle>
          <DialogDescription>
            Selecciona el contenido que quieres practicar
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6 mt-4">
          {/* Course Selection */}
          <div>
            <Label>Curso</Label>
            <Select
              value={selectedCourse?.id || ""}
              onValueChange={(value) => {
                const course = courses.find(c => c.id === value);
                setSelectedCourse(course);
              }}
            >
              <SelectTrigger data-testid="quiz-course-select">
                <SelectValue placeholder="Selecciona un curso" />
              </SelectTrigger>
              <SelectContent>
                {courses.map(course => (
                  <SelectItem key={course.id} value={course.id}>
                    {course.title}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Chapters and Lessons Selection */}
          {selectedCourse && (
            <div>
              <Label className="mb-2 block">Contenido a evaluar</Label>
              {loading ? (
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="animate-spin text-primary" size={24} />
                </div>
              ) : chapters.length === 0 ? (
                <p className="text-sm text-slate-500 py-4">
                  Este curso no tiene capítulos disponibles
                </p>
              ) : (
                <div className="border rounded-lg divide-y max-h-[250px] overflow-y-auto">
                  {chapters.map(chapter => (
                    <div key={chapter.id}>
                      <div 
                        className="flex items-center gap-3 p-3 hover:bg-slate-50 cursor-pointer"
                        onClick={() => toggleChapter(chapter.id)}
                      >
                        <Checkbox
                          checked={selectedChapters[chapter.id] || false}
                          onCheckedChange={(checked) => handleChapterToggle(chapter, checked)}
                          onClick={(e) => e.stopPropagation()}
                        />
                        {expandedChapters[chapter.id] ? 
                          <ChevronDown size={16} /> : 
                          <ChevronRight size={16} />
                        }
                        <span className="font-medium flex-1">{chapter.title}</span>
                        <Badge variant="secondary" className="text-xs">
                          {chapter.lessons?.length || 0} lecciones
                        </Badge>
                      </div>
                      
                      {expandedChapters[chapter.id] && chapter.lessons?.length > 0 && (
                        <div className="bg-slate-50 pl-12 pr-3 py-2 space-y-2">
                          {chapter.lessons.map(lesson => (
                            <div key={lesson.id} className="flex items-center gap-3">
                              <Checkbox
                                checked={selectedLessons[lesson.id] || false}
                                onCheckedChange={(checked) => handleLessonToggle(lesson, chapter.id, checked)}
                              />
                              <span className="text-sm">{lesson.title}</span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Quiz Settings */}
          <div className="grid grid-cols-3 gap-4">
            <div>
              <Label>Preguntas</Label>
              <Select value={numQuestions} onValueChange={setNumQuestions}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {[5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15].map(n => (
                    <SelectItem key={n} value={String(n)}>{n}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            
            <div>
              <Label>Dificultad</Label>
              <Select value={difficulty} onValueChange={setDifficulty}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="todos">Todas</SelectItem>
                  <SelectItem value="fácil">Fácil</SelectItem>
                  <SelectItem value="medio">Medio</SelectItem>
                  <SelectItem value="difícil">Difícil</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div>
              <Label>Tiempo límite</Label>
              <Select value={timeLimit} onValueChange={setTimeLimit}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="none">Sin límite</SelectItem>
                  <SelectItem value="10">10 minutos</SelectItem>
                  <SelectItem value="15">15 minutos</SelectItem>
                  <SelectItem value="20">20 minutos</SelectItem>
                  <SelectItem value="30">30 minutos</SelectItem>
                  <SelectItem value="45">45 minutos</SelectItem>
                  <SelectItem value="60">60 minutos</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <Button
            onClick={handleCreate}
            disabled={creating || !selectedCourse || (getSelectedChapterIds().length === 0)}
            className="w-full"
          >
            {creating ? (
              <>
                <Loader2 className="animate-spin mr-2" size={18} />
                Creando simulacro...
              </>
            ) : (
              <>
                <Play className="mr-2" size={18} />
                Crear y Comenzar
              </>
            )}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};

// ==================== ACTIVE QUIZ VIEW ====================
const ActiveQuizView = ({ quiz, onComplete, onCancel }) => {
  const [answers, setAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);
  const [results, setResults] = useState(null);
  const [timeLeft, setTimeLeft] = useState(quiz.time_limit_minutes ? quiz.time_limit_minutes * 60 : null);
  const [timeSpent, setTimeSpent] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const timerRef = useRef(null);
  const startTimeRef = useRef(Date.now());

  // Timer effect
  useEffect(() => {
    timerRef.current = setInterval(() => {
      setTimeSpent(prev => prev + 1);
      
      if (timeLeft !== null) {
        setTimeLeft(prev => {
          if (prev <= 1) {
            // Time's up - auto submit
            clearInterval(timerRef.current);
            handleSubmit(true);
            return 0;
          }
          return prev - 1;
        });
      }
    }, 1000);

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, []);

  const handleAnswerSelect = (questionIndex, answer) => {
    if (showResults) return;
    setAnswers(prev => ({ ...prev, [questionIndex]: answer }));
  };

  const handleSubmit = async (isTimeout = false) => {
    if (timerRef.current) clearInterval(timerRef.current);
    setSubmitting(true);

    try {
      const response = await axios.post(`${API}/quiz/submit`, {
        quiz_id: quiz.id,
        answers: answers,
        time_spent_seconds: timeSpent
      });

      setResults(response.data);
      setShowResults(true);

      if (isTimeout) {
        toast.warning('¡Se acabó el tiempo!');
      } else {
        toast.success(`¡Completado! Nota: ${response.data.grade}`);
      }
    } catch (error) {
      console.error('Error submitting quiz:', error);
      toast.error('Error al enviar respuestas');
    } finally {
      setSubmitting(false);
    }
  };

  const answeredCount = Object.keys(answers).length;
  const totalQuestions = quiz.questions?.length || 0;

  return (
    <div className="max-w-4xl mx-auto pb-24 lg:pb-8" data-testid="active-quiz">
      {/* Header with timer */}
      <div className="sticky top-0 z-40 bg-white border-b mb-6 -mx-4 px-4 py-3 sm:-mx-6 sm:px-6 lg:-mx-8 lg:px-8">
        <div className="flex items-center justify-between max-w-4xl mx-auto">
          <div>
            <h2 className="font-bold text-lg">{quiz.course_title || 'Simulacro'}</h2>
            <p className="text-sm text-slate-500">
              {answeredCount}/{totalQuestions} respondidas
            </p>
          </div>
          
          <div className="flex items-center gap-4">
            {/* Timer display */}
            <div className={`flex items-center gap-2 px-4 py-2 rounded-full font-mono text-lg ${
              timeLeft !== null && timeLeft < 60 
                ? 'bg-red-100 text-red-600 animate-pulse' 
                : 'bg-slate-100 text-slate-700'
            }`}>
              <Timer size={20} />
              {timeLeft !== null ? formatTime(timeLeft) : formatTime(timeSpent)}
            </div>
            
            {!showResults && (
              <Button variant="outline" onClick={onCancel}>
                Cancelar
              </Button>
            )}
          </div>
        </div>
      </div>

      {/* Results header */}
      {showResults && results && (
        <Card className="mb-6 bg-gradient-to-r from-primary/10 to-cyan-50">
          <CardContent className="py-6">
            <div className="flex items-center justify-around text-center">
              <div>
                <div className={`text-4xl font-bold ${getGradeColor(results.grade)} inline-block px-4 py-2 rounded-full`}>
                  {results.grade}
                </div>
                <p className="text-sm text-slate-600 mt-2">Nota Final</p>
              </div>
              <div>
                <div className="text-3xl font-bold text-slate-800">
                  {results.correct_count}/{results.total_questions}
                </div>
                <p className="text-sm text-slate-600 mt-2">Correctas</p>
              </div>
              <div>
                <div className="text-3xl font-bold text-slate-800">
                  {Math.round(results.score)}%
                </div>
                <p className="text-sm text-slate-600 mt-2">Porcentaje</p>
              </div>
              <div>
                <div className="text-3xl font-bold text-slate-800">
                  {formatTime(timeSpent)}
                </div>
                <p className="text-sm text-slate-600 mt-2">Tiempo</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Questions */}
      <Card>
        <CardContent className="pt-6 space-y-8">
          {quiz.questions?.map((question, index) => {
            const userAnswer = answers[index];
            const correctAnswer = showResults ? (results?.results?.[index]?.correct_answer || question.correct_answer) : null;
            const isCorrect = showResults ? userAnswer === correctAnswer : null;

            return (
              <div key={index} className="space-y-4" data-testid={`quiz-question-${index}`}>
                {/* Question header */}
                <div className="flex items-start gap-3">
                  {showResults && (
                    <div className={`mt-1 ${isCorrect ? 'text-green-500' : 'text-red-500'}`}>
                      {isCorrect ? <CheckCircle size={20} /> : <XCircle size={20} />}
                    </div>
                  )}
                  <div className="font-medium text-lg flex-1">
                    <QuestionContent content={`**${index + 1}.** ${question.question_text || question.question}`} />
                  </div>
                </div>

                {/* Options */}
                <div className="space-y-3 ml-8">
                  {question.options?.map((option, optIndex) => {
                    const optionLetter = option.charAt(0);
                    const isSelected = userAnswer === optionLetter;
                    const isCorrectOption = optionLetter === correctAnswer;

                    return (
                      <QuestionOption
                        key={optIndex}
                        option={option}
                        isSelected={isSelected}
                        isCorrect={isCorrectOption}
                        showResult={showResults}
                        onClick={() => handleAnswerSelect(index, optionLetter)}
                        disabled={showResults}
                        testId={`quiz-option-${index}-${optIndex}`}
                      />
                    );
                  })}
                </div>

                {/* Explanation */}
                {showResults && results?.results?.[index]?.explanation && (
                  <div className="ml-8">
                    <ExplanationBlock explanation={results.results[index].explanation} />
                  </div>
                )}
              </div>
            );
          })}

          {/* Actions */}
          <div className="flex gap-3 pt-4 border-t">
            {!showResults ? (
              <Button
                onClick={() => handleSubmit(false)}
                disabled={submitting || answeredCount === 0}
                className="flex-1"
              >
                {submitting ? (
                  <>
                    <Loader2 className="animate-spin mr-2" size={18} />
                    Enviando...
                  </>
                ) : (
                  `Enviar respuestas (${answeredCount}/${totalQuestions})`
                )}
              </Button>
            ) : (
              <Button onClick={onComplete} className="w-full">
                Volver a Simulacros
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

// ==================== MAIN COMPONENT ====================
const Simulacros = () => {
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [activeQuiz, setActiveQuiz] = useState(null);

  useEffect(() => {
    fetchQuizzes();
  }, []);

  const fetchQuizzes = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/quiz/history/${getStudentId()}`);
      setQuizzes(response.data);
    } catch (error) {
      console.error('Error fetching quizzes:', error);
      setQuizzes([]);
    } finally {
      setLoading(false);
    }
  };

  const handleStartQuiz = async (quiz) => {
    // If quiz already has questions (from history), use them
    if (quiz.questions) {
      setActiveQuiz({
        id: quiz.id,
        questions: quiz.questions,
        time_limit_minutes: quiz.time_limit_minutes,
        course_title: quiz.course_title || quiz.topic
      });
    } else {
      // Fetch quiz details
      try {
        const response = await axios.get(`${API}/quiz/${quiz.id}`);
        setActiveQuiz({
          id: response.data.id,
          questions: response.data.questions,
          time_limit_minutes: response.data.time_limit_minutes,
          course_title: response.data.course_title || response.data.topic
        });
      } catch (error) {
        console.error('Error fetching quiz:', error);
        toast.error('Error al cargar el simulacro');
      }
    }
  };

  const handleDeleteQuiz = async (quizId) => {
    if (!window.confirm('¿Eliminar este simulacro?')) return;
    
    try {
      await axios.delete(`${API}/quiz/${quizId}?user_id=${getStudentId()}`);
      toast.success('Simulacro eliminado');
      fetchQuizzes();
    } catch (error) {
      console.error('Error deleting quiz:', error);
      toast.error('Error al eliminar el simulacro');
    }
  };

  const handleQuizCreated = (quizData) => {
    setActiveQuiz(quizData);
  };

  const handleQuizComplete = () => {
    setActiveQuiz(null);
    fetchQuizzes();
  };

  // Active quiz view
  if (activeQuiz) {
    return (
      <ActiveQuizView
        quiz={activeQuiz}
        onComplete={handleQuizComplete}
        onCancel={() => setActiveQuiz(null)}
      />
    );
  }

  return (
    <div className="space-y-6 pb-24 lg:pb-8" data-testid="simulacros-page">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold">Simulacros de Prueba</h1>
          <p className="text-slate-600 mt-1">Practica con exámenes personalizados</p>
        </div>
        <Button 
          onClick={() => setCreateDialogOpen(true)} 
          className="rounded-full"
          data-testid="create-quiz-button"
        >
          <Plus size={20} className="mr-2" />
          Crear simulacro
        </Button>
      </div>

      <CreateQuizDialog
        open={createDialogOpen}
        onOpenChange={setCreateDialogOpen}
        onQuizCreated={handleQuizCreated}
      />

      {loading ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="animate-spin text-primary" size={32} />
        </div>
      ) : quizzes.length === 0 ? (
        <Card className="text-center py-12">
          <CardContent>
            <Clock className="mx-auto mb-4 text-slate-400" size={48} />
            <h3 className="text-xl font-semibold mb-2">No hay simulacros aún</h3>
            <p className="text-slate-500 mb-6">Crea tu primer simulacro para empezar a practicar</p>
            <Button 
              onClick={() => setCreateDialogOpen(true)} 
              className="rounded-full"
              data-testid="create-first-quiz-button"
            >
              <Plus size={20} className="mr-2" />
              Crear mi primer simulacro
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {quizzes.map((quiz) => (
            <QuizCard
              key={quiz.id}
              quiz={quiz}
              onStart={handleStartQuiz}
              onDelete={handleDeleteQuiz}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default function SimulacrosPage() {
  return (
    <SubscriptionRequired feature="los simulacros de práctica">
      <Simulacros />
    </SubscriptionRequired>
  );
}
