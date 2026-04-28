import { useState, useEffect, useRef, useCallback } from 'react';
import axios from 'axios';
import {
  Plus, Loader2, Clock, Trash2, Play, CheckCircle, XCircle,
  ChevronDown, ChevronRight, BookOpen, Layers, Timer, Award, Eye, AlertCircle
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import { Badge } from '@/components/ui/badge';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { toast } from 'sonner';
import { QuestionContent, QuestionOption, ExplanationBlock } from '@/components/course/QuestionRenderer';
import SubscriptionRequired from '@/components/SubscriptionRequired';
import { useAuth } from '../contexts/AuthContext';
import { showAchievementToasts } from '@/lib/achievementToast';

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
  if (grade >= 6.0) return 'text-green-600 dark:text-green-400 bg-green-500/20';
  if (grade >= 5.0) return 'text-blue-600 dark:text-blue-400 bg-blue-500/20';
  if (grade >= 4.0) return 'text-yellow-600 dark:text-yellow-400 bg-yellow-500/20';
  return 'text-red-600 dark:text-red-400 bg-red-500/20';
};

// ==================== QUIZ CARD COMPONENT ====================
const QuizCard = ({ quiz, onStart, onView, onDelete }) => {
  const isCompleted = quiz.completed && quiz.grade !== null && quiz.grade !== undefined;

  return (
    <Card className="hover:shadow-lg transition-all border-border bg-card" data-testid={`quiz-card-${quiz.id}`}>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between gap-2">
          <Badge variant="outline" className="text-xs">
            {quiz.difficulty || 'medio'}
          </Badge>
          {isCompleted && (
            <div className={`px-3 py-1 rounded-full font-bold text-sm tabular-nums ${getGradeColor(quiz.grade)}`}>
              {quiz.grade}
            </div>
          )}
        </div>
        <CardTitle className="text-lg mt-2 text-foreground">{quiz.topic || 'Simulacro'}</CardTitle>
        <CardDescription className="space-y-1">
          <span className="block">{quiz.course_title || 'Curso'}</span>
          <span className="block text-xs flex items-center gap-2">
            <BookOpen size={12} />
            <span className="tabular-nums">{quiz.questions?.length || 0} preguntas</span>
            {quiz.time_limit_minutes && (
              <>
                <Clock size={12} className="ml-2" />
                <span className="tabular-nums">{quiz.time_limit_minutes} min</span>
              </>
            )}
          </span>
          <span className="block text-xs text-muted-foreground">
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
          {isCompleted && onView && (
            <Button
              onClick={() => onView(quiz)}
              variant="outline"
              className="flex-1 rounded-full"
              data-testid={`view-result-btn-${quiz.id}`}
            >
              <Eye size={16} className="mr-2" />
              Ver resultado
            </Button>
          )}
          <Button
            onClick={() => onStart(quiz)}
            className="flex-1 rounded-full"
            variant={isCompleted ? 'ghost' : 'default'}
          >
            <Play size={16} className="mr-2" />
            {isCompleted ? 'Reintentar' : 'Comenzar'}
          </Button>
          <Button
            variant="ghost"
            size="icon"
            className="text-muted-foreground hover:text-destructive"
            onClick={() => onDelete(quiz.id)}
            aria-label="Eliminar simulacro"
          >
            <Trash2 size={18} />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

// Reconstruct the quiz/submit response shape from a stored attempt so the
// review screen can render exactly the same way as a freshly-submitted quiz.
const buildResultsFromAttempt = (quiz) => {
  const questions = quiz.questions || [];
  const answers = quiz.answers || {};
  let correct = 0;
  const results = questions.map((q, idx) => {
    const userAnswer = answers[String(idx)] ?? answers[idx];
    const isCorrect = userAnswer === q.correct_answer;
    if (isCorrect) correct += 1;
    return {
      question_index: idx,
      question_text: q.question_text || q.question || '',
      user_answer: userAnswer,
      correct_answer: q.correct_answer,
      is_correct: isCorrect,
      explanation: q.explanation || ''
    };
  });
  return {
    score: quiz.score ?? (questions.length ? (correct / questions.length) * 100 : 0),
    grade: quiz.grade ?? 0,
    correct_count: correct,
    total_questions: questions.length,
    results
  };
};

// ==================== LAST ATTEMPT BANNER ====================
const LastAttemptBanner = ({ quiz, onView, onRetry }) => {
  if (!quiz) return null;
  const grade = quiz.grade;
  const date = quiz.created_at ? new Date(quiz.created_at) : null;
  return (
    <Card
      className="border-border bg-gradient-to-r from-primary/10 via-primary/5 to-transparent"
      data-testid="last-attempt-banner"
    >
      <CardContent className="py-5">
        <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4">
          <div className={`flex-shrink-0 w-14 h-14 rounded-2xl flex items-center justify-center text-2xl font-bold tabular-nums ${getGradeColor(grade)}`}>
            {Number(grade).toFixed(1)}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs uppercase tracking-wider text-muted-foreground font-semibold">
              Tu último simulacro
            </p>
            <p className="text-base md:text-lg font-semibold text-foreground truncate">
              {quiz.topic || 'Simulacro'} · {quiz.course_title || ''}
            </p>
            <p className="text-xs text-muted-foreground mt-0.5">
              {date && date.toLocaleDateString('es-CL', { day: 'numeric', month: 'long', year: 'numeric' })}
              {quiz.questions?.length ? ` · ${quiz.questions.length} preguntas` : ''}
            </p>
          </div>
          <div className="flex gap-2 flex-shrink-0">
            <Button variant="outline" onClick={() => onView(quiz)} className="rounded-full" data-testid="last-attempt-view">
              <Eye size={16} className="mr-2" />
              Ver resultado
            </Button>
            <Button onClick={() => onRetry(quiz)} className="rounded-full" data-testid="last-attempt-retry">
              <Play size={16} className="mr-2" />
              Reintentar
            </Button>
          </div>
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
  const [hasEnrolledCourses, setHasEnrolledCourses] = useState(true);

  useEffect(() => {
    if (open) {
      fetchEnrolledCourses();
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

  const fetchEnrolledCourses = async () => {
    try {
      const token = localStorage.getItem('remy_session_token');
      if (token) {
        // Fetch enrolled courses
        const response = await axios.get(`${API}/enrollments`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setCourses(response.data);
        setHasEnrolledCourses(response.data.length > 0);
      } else {
        // Fallback to all courses if not logged in
        const response = await axios.get(`${API}/courses`);
        setCourses(response.data);
      }
    } catch (error) {
      console.error('Error fetching courses:', error);
      // Fallback to all courses
      try {
        const response = await axios.get(`${API}/courses`);
        setCourses(response.data);
      } catch (e) {
        console.error('Error fetching all courses:', e);
      }
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
      
      // Check if it's a trial limit error
      if (error.response?.status === 403 && errorMsg.includes('límite')) {
        toast.error(errorMsg, {
          duration: 8000,
          action: {
            label: 'Suscribirme',
            onClick: () => window.location.href = '/subscribe'
          }
        });
      } else {
        toast.error(errorMsg);
      }
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
          {/* No enrolled courses message */}
          {!hasEnrolledCourses && (
            <div className="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg p-4 text-center">
              <p className="text-amber-800 dark:text-amber-200 text-sm mb-3">
                No tienes cursos inscritos. Inscríbete en un curso desde la Biblioteca para crear simulacros.
              </p>
              <Button 
                variant="outline"
                onClick={() => {
                  onOpenChange(false);
                  window.location.href = '/biblioteca';
                }}
              >
                <BookOpen className="mr-2" size={16} />
                Ir a Biblioteca
              </Button>
            </div>
          )}
          
          {/* Course Selection */}
          {hasEnrolledCourses && (
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
                  <SelectValue placeholder="Selecciona un curso inscrito" />
                </SelectTrigger>
                <SelectContent>
                  {courses.map(course => (
                    <SelectItem key={course.id} value={course.id}>
                      <span className="flex items-center gap-2">
                        {course.title}
                        {course.university?.short_name && course.university.short_name !== 'GEN' && (
                          <Badge variant="outline" className="text-xs ml-2">
                            {course.university.short_name}
                          </Badge>
                        )}
                      </span>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <p className="text-xs text-muted-foreground mt-1">
                Solo se muestran cursos en los que estás inscrito
              </p>
            </div>
          )}

          {/* Chapters and Lessons Selection */}
          {selectedCourse && (
            <div>
              <Label className="mb-2 block">Contenido a evaluar</Label>
              {loading ? (
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="animate-spin text-primary" size={24} />
                </div>
              ) : chapters.length === 0 ? (
                <p className="text-sm text-muted-foreground py-4">
                  Este curso no tiene capítulos disponibles
                </p>
              ) : (
                <div className="border border-border rounded-lg divide-y divide-border max-h-[250px] overflow-y-auto">
                  {chapters.map(chapter => (
                    <div key={chapter.id}>
                      <div 
                        className="flex items-center gap-3 p-3 hover:bg-secondary cursor-pointer"
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
                        <span className="font-medium flex-1 text-foreground">{chapter.title}</span>
                        <Badge variant="secondary" className="text-xs">
                          {chapter.lessons?.length || 0} lecciones
                        </Badge>
                      </div>
                      
                      {expandedChapters[chapter.id] && chapter.lessons?.length > 0 && (
                        <div className="bg-secondary/50 pl-12 pr-3 py-2 space-y-2">
                          {chapter.lessons.map(lesson => (
                            <div key={lesson.id} className="flex items-center gap-3">
                              <Checkbox
                                checked={selectedLessons[lesson.id] || false}
                                onCheckedChange={(checked) => handleLessonToggle(lesson, chapter.id, checked)}
                              />
                              <span className="text-sm text-foreground">{lesson.title}</span>
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

// ==================== WRONG-ANSWERS BY CHAPTER CHART ====================
// Surfaces where the student lost points so they can target practice next time.
const WrongAnswersChart = ({ quiz, results }) => {
  const [chapterTitles, setChapterTitles] = useState({});

  // Fetch all chapters for the quiz course so we can show titles instead of UUIDs.
  useEffect(() => {
    if (!quiz?.course_id) return;
    let cancelled = false;
    axios.get(`${API}/courses/${quiz.course_id}/chapters`)
      .then((r) => {
        if (cancelled) return;
        const map = {};
        (r.data || []).forEach((ch) => { map[ch.id] = ch.title; });
        setChapterTitles(map);
      })
      .catch(() => {});
    return () => { cancelled = true; };
  }, [quiz?.course_id]);

  // Aggregate per-chapter stats from per-question results.
  const data = (() => {
    const buckets = {};
    (quiz.questions || []).forEach((q, idx) => {
      const chId = q.chapter_id || 'sin-capitulo';
      if (!buckets[chId]) buckets[chId] = { id: chId, total: 0, wrong: 0 };
      buckets[chId].total += 1;
      const r = results?.results?.[idx];
      if (r && r.is_correct === false) buckets[chId].wrong += 1;
    });
    return Object.values(buckets)
      .filter((b) => b.total > 0)
      .map((b) => ({
        id: b.id,
        name: chapterTitles[b.id] || (b.id === 'sin-capitulo' ? 'Sin capítulo' : 'Capítulo'),
        wrong: b.wrong,
        total: b.total,
        correct: b.total - b.wrong,
        // Truncated label for X axis to avoid clipping
        shortName: (chapterTitles[b.id] || 'Cap.').slice(0, 18) + ((chapterTitles[b.id]?.length || 0) > 18 ? '…' : ''),
      }))
      .sort((a, b) => b.wrong - a.wrong);
  })();

  if (data.length === 0) return null;

  const hasErrors = data.some((d) => d.wrong > 0);

  return (
    <Card className="border-border bg-card" data-testid="wrong-answers-chart">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg flex items-center gap-2 text-foreground">
          <AlertCircle size={18} className="text-amber-500 dark:text-amber-400" aria-hidden="true" />
          Errores por capítulo
        </CardTitle>
        <CardDescription>
          {hasErrors
            ? 'Capítulos ordenados por cantidad de errores. Practica los de arriba.'
            : '¡No tuviste errores! Excelente trabajo.'}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-56 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} margin={{ top: 8, right: 12, left: -16, bottom: 8 }}>
              <XAxis
                dataKey="shortName"
                stroke="hsl(var(--muted-foreground))"
                tick={{ fontSize: 11 }}
                interval={0}
                angle={data.length > 4 ? -20 : 0}
                textAnchor={data.length > 4 ? 'end' : 'middle'}
                height={data.length > 4 ? 50 : 30}
              />
              <YAxis
                stroke="hsl(var(--muted-foreground))"
                tick={{ fontSize: 11 }}
                allowDecimals={false}
              />
              <Tooltip
                contentStyle={{
                  background: 'hsl(var(--card))',
                  border: '1px solid hsl(var(--border))',
                  borderRadius: 8,
                  fontSize: 12,
                  color: 'hsl(var(--foreground))'
                }}
                formatter={(value, name, props) => {
                  if (name === 'wrong') return [`${value} de ${props.payload.total}`, 'Errores'];
                  return [value, name];
                }}
                labelFormatter={(_, payload) => payload?.[0]?.payload?.name || ''}
              />
              <Bar dataKey="wrong" radius={[8, 8, 0, 0]} maxBarSize={56}>
                {data.map((entry, i) => (
                  <Cell
                    key={i}
                    fill={
                      entry.wrong === 0
                        ? 'hsl(var(--primary))'
                        : entry.wrong / entry.total >= 0.6
                        ? '#ef4444' // red-500
                        : entry.wrong / entry.total >= 0.3
                        ? '#f59e0b' // amber-500
                        : '#22c55e' // green-500
                    }
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Legend with per-chapter counts (more accessible than just hover tooltips) */}
        <ul className="mt-3 space-y-1.5 text-sm">
          {data.map((d) => (
            <li key={d.id} className="flex items-center justify-between gap-3">
              <span className="text-foreground truncate">{d.name}</span>
              <span className={`flex-shrink-0 tabular-nums text-xs px-2 py-0.5 rounded-full ${
                d.wrong === 0
                  ? 'bg-emerald-500/15 text-emerald-700 dark:text-emerald-300'
                  : d.wrong / d.total >= 0.6
                  ? 'bg-red-500/15 text-red-700 dark:text-red-300'
                  : d.wrong / d.total >= 0.3
                  ? 'bg-amber-500/15 text-amber-700 dark:text-amber-300'
                  : 'bg-emerald-500/10 text-emerald-700 dark:text-emerald-300'
              }`}>
                {d.wrong}/{d.total} errores
              </span>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
};

// ==================== ACTIVE QUIZ VIEW ====================
// `quiz.viewOnly === true` skips the timer and pre-loads the saved answers/results
// so a completed simulacro can be reviewed without re-answering.
const ActiveQuizView = ({ quiz, onComplete, onCancel }) => {
  const isViewOnly = !!quiz.viewOnly;
  const [answers, setAnswers] = useState(quiz.initialAnswers || {});
  const [showResults, setShowResults] = useState(isViewOnly);
  const [results, setResults] = useState(quiz.initialResults || null);
  const [timeLeft, setTimeLeft] = useState(
    isViewOnly ? null : (quiz.time_limit_minutes ? quiz.time_limit_minutes * 60 : null)
  );
  const [timeSpent, setTimeSpent] = useState(quiz.initialTimeSpent || 0);
  const [submitting, setSubmitting] = useState(false);
  const timerRef = useRef(null);
  const startTimeRef = useRef(Date.now());

  // Timer effect — disabled in view-only mode (just reviewing past attempt).
  useEffect(() => {
    if (isViewOnly) return;
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
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isViewOnly]);

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
      showAchievementToasts(response.data.newly_unlocked_achievements);
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
      <div className="sticky top-0 z-40 bg-card border-b border-border mb-6 -mx-4 px-4 py-3 sm:-mx-6 sm:px-6 lg:-mx-8 lg:px-8">
        <div className="flex items-center justify-between max-w-4xl mx-auto">
          <div>
            <h2 className="font-bold text-lg text-foreground">{quiz.course_title || 'Simulacro'}</h2>
            <p className="text-sm text-muted-foreground">
              {answeredCount}/{totalQuestions} respondidas
            </p>
          </div>
          
          <div className="flex items-center gap-4">
            {/* Timer display */}
            <div className={`flex items-center gap-2 px-4 py-2 rounded-full font-mono text-lg ${
              timeLeft !== null && timeLeft < 60 
                ? 'bg-red-500/20 text-red-600 dark:text-red-400 animate-pulse' 
                : 'bg-secondary text-foreground'
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

      {/* Wrong-answers chart (above questions, after results header) */}
      {showResults && results && (
        <div className="mb-6">
          <WrongAnswersChart quiz={quiz} results={results} />
        </div>
      )}

      {/* Results header */}
      {showResults && results && (
        <Card className="mb-6 bg-gradient-to-r from-primary/10 to-primary/5">
          <CardContent className="py-6">
            <div className="flex items-center justify-around text-center">
              <div>
                <div className={`text-4xl font-bold ${getGradeColor(results.grade)} inline-block px-4 py-2 rounded-full`}>
                  {results.grade}
                </div>
                <p className="text-sm text-muted-foreground mt-2">Nota Final</p>
              </div>
              <div>
                <div className="text-3xl font-bold text-foreground">
                  {results.correct_count}/{results.total_questions}
                </div>
                <p className="text-sm text-muted-foreground mt-2">Correctas</p>
              </div>
              <div>
                <div className="text-3xl font-bold text-foreground">
                  {Math.round(results.score)}%
                </div>
                <p className="text-sm text-muted-foreground mt-2">Porcentaje</p>
              </div>
              <div>
                <div className="text-3xl font-bold text-foreground">
                  {formatTime(timeSpent)}
                </div>
                <p className="text-sm text-muted-foreground mt-2">Tiempo</p>
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
    // If quiz already has questions (from history), use them. We strip the
    // saved answers so a "Reintentar" starts fresh.
    if (quiz.questions) {
      setActiveQuiz({
        id: quiz.id,
        questions: quiz.questions,
        course_id: quiz.course_id,
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
          course_id: response.data.course_id,
          time_limit_minutes: response.data.time_limit_minutes,
          course_title: response.data.course_title || response.data.topic
        });
      } catch (error) {
        console.error('Error fetching quiz:', error);
        toast.error('Error al cargar el simulacro');
      }
    }
  };

  // Open a completed simulacro in read-only review mode (with stored answers/results).
  const handleViewQuiz = async (quiz) => {
    let full = quiz;
    if (!full.answers || !full.questions) {
      try {
        const response = await axios.get(`${API}/quiz/${quiz.id}`);
        full = response.data;
      } catch (error) {
        toast.error('Error al cargar el resultado');
        return;
      }
    }
    setActiveQuiz({
      id: full.id,
      questions: full.questions,
      course_id: full.course_id,
      time_limit_minutes: full.time_limit_minutes,
      course_title: full.course_title || full.topic,
      viewOnly: true,
      initialAnswers: full.answers || {},
      initialResults: buildResultsFromAttempt(full),
      initialTimeSpent: full.time_spent_seconds || 0
    });
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

  // Most recent COMPLETED quiz for the "last attempt" banner.
  const lastCompletedQuiz = quizzes.find(
    (q) => q.completed && q.grade !== null && q.grade !== undefined
  );

  return (
    <div className="space-y-6 pb-24 lg:pb-8" data-testid="simulacros-page">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold text-foreground tracking-tight">Simulacros de Prueba</h1>
          <p className="text-muted-foreground mt-1">Practica con exámenes personalizados</p>
        </div>
        <Button
          onClick={() => setCreateDialogOpen(true)}
          className="rounded-full bg-primary hover:bg-primary/90"
          data-testid="create-quiz-button"
        >
          <Plus size={20} className="mr-2" />
          Crear simulacro
        </Button>
      </div>

      {!loading && lastCompletedQuiz && (
        <LastAttemptBanner
          quiz={lastCompletedQuiz}
          onView={handleViewQuiz}
          onRetry={handleStartQuiz}
        />
      )}

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
            <Clock className="mx-auto mb-4 text-muted-foreground" size={48} />
            <h3 className="text-xl font-semibold mb-2 text-foreground">No hay simulacros aún</h3>
            <p className="text-muted-foreground mb-6">Crea tu primer simulacro para empezar a practicar</p>
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
              onView={handleViewQuiz}
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
