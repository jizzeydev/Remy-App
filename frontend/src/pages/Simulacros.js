import { useState, useEffect } from 'react';
import axios from 'axios';
import { Plus, Loader2, CheckCircle2, XCircle, Clock } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Simulacros = () => {
  const [quizzes, setQuizzes] = useState([]);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [open, setOpen] = useState(false);
  const [activeQuiz, setActiveQuiz] = useState(null);
  const [answers, setAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);
  const userId = 'demo-user-001';

  const [formData, setFormData] = useState({
    course_id: '',
    topic: '',
    num_questions: 5
  });

  useEffect(() => {
    fetchCourses();
    fetchQuizzes();
  }, []);

  const fetchCourses = async () => {
    try {
      const response = await axios.get(`${API}/courses`);
      setCourses(response.data);
    } catch (error) {
      console.error('Error fetching courses:', error);
    }
  };

  const fetchQuizzes = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/quiz/history/${userId}`);
      setQuizzes(response.data);
    } catch (error) {
      console.error('Error fetching quizzes:', error);
      setQuizzes([]);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async () => {
    if (!formData.course_id || !formData.topic) {
      toast.error('Por favor completa todos los campos');
      return;
    }

    setGenerating(true);
    try {
      const response = await axios.post(`${API}/quiz/start`, {
        user_id: userId,
        course_id: formData.course_id,
        topic: formData.topic,
        num_questions: formData.num_questions
      });

      // Start quiz immediately with the returned data
      setActiveQuiz({
        id: response.data.quiz_id,
        title: `Simulacro de ${formData.topic}`,
        questions: response.data.questions
      });
      toast.success('¡Simulacro iniciado!');
      setOpen(false);
      setFormData({ course_id: '', topic: '', num_questions: 5 });
    } catch (error) {
      console.error('Error generating quiz:', error);
      const errorMsg = error.response?.data?.detail || 'Error al generar el simulacro. Verifica que haya preguntas disponibles para este tema.';
      toast.error(errorMsg);
    } finally {
      setGenerating(false);
    }
  };

  const handleStartQuiz = (quiz) => {
    // If quiz comes from history, it has the full structure
    setActiveQuiz({
      id: quiz.id,
      title: `Simulacro de ${quiz.topic}`,
      questions: quiz.questions
    });
    setAnswers({});
    setShowResults(false);
  };

  const handleAnswerSelect = (questionIndex, answer) => {
    setAnswers(prev => ({ ...prev, [questionIndex]: answer }));
  };

  const handleSubmitQuiz = async () => {
    setShowResults(true);
    const correct = activeQuiz.questions.filter(
      (q, i) => answers[i] === (q.correct_answer || q.correct_option)
    ).length;
    const percentage = ((correct / activeQuiz.questions.length) * 100).toFixed(0);
    toast.success(`¡Completado! Obtuviste ${percentage}% (${correct}/${activeQuiz.questions.length})`);
    
    // Submit to backend if quiz has an id
    if (activeQuiz.id) {
      try {
        await axios.post(`${API}/quiz/submit`, {
          quiz_id: activeQuiz.id,
          answers: answers
        });
      } catch (error) {
        console.error('Error submitting quiz:', error);
      }
    }
  };

  if (activeQuiz) {
    return (
      <div className="max-w-4xl mx-auto pb-24 lg:pb-8" data-testid="active-quiz">
        <Card>
          <CardHeader>
            <CardTitle>{activeQuiz.title}</CardTitle>
            <CardDescription>
              {activeQuiz.questions.length} preguntas
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {activeQuiz.questions.map((question, index) => (
              <div key={index} className="space-y-3" data-testid={`quiz-question-${index}`}>
                <h3 className="font-semibold text-lg">
                  {index + 1}. {question.question_text || question.question}
                </h3>
                <div className="space-y-2">
                  {question.options.map((option, optIndex) => {
                    const optionLetter = option.charAt(0);
                    const isSelected = answers[index] === optionLetter;
                    const isCorrect = optionLetter === (question.correct_answer || question.correct_option);
                    const showCorrect = showResults && isCorrect;
                    const showIncorrect = showResults && isSelected && !isCorrect;

                    return (
                      <button
                        key={optIndex}
                        onClick={() => !showResults && handleAnswerSelect(index, optionLetter)}
                        disabled={showResults}
                        data-testid={`quiz-option-${index}-${optIndex}`}
                        className={`w-full p-4 text-left border-2 rounded-xl quiz-option ${
                          isSelected ? 'selected' : ''
                        } ${showCorrect ? 'correct' : ''} ${showIncorrect ? 'incorrect' : ''}`}
                      >
                        <div className="flex items-center justify-between">
                          <span>{option}</span>
                          {showCorrect && <CheckCircle2 className="text-green-600" size={20} />}
                          {showIncorrect && <XCircle className="text-red-600" size={20} />}
                        </div>
                      </button>
                    );
                  })}
                </div>
                {showResults && question.explanation && (
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mt-3">
                    <p className="text-sm text-blue-900">
                      <strong>Explicación:</strong> {question.explanation}
                    </p>
                  </div>
                )}
              </div>
            ))}

            <div className="flex gap-3 pt-4">
              {!showResults ? (
                <>
                  <Button
                    onClick={handleSubmitQuiz}
                    disabled={Object.keys(answers).length !== activeQuiz.questions.length}
                    data-testid="submit-quiz-button"
                    className="flex-1 rounded-full"
                  >
                    Enviar respuestas
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() => setActiveQuiz(null)}
                    data-testid="cancel-quiz-button"
                  >
                    Cancelar
                  </Button>
                </>
              ) : (
                <Button
                  onClick={() => setActiveQuiz(null)}
                  data-testid="finish-quiz-button"
                  className="w-full rounded-full"
                >
                  Volver a simulacros
                </Button>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6 pb-24 lg:pb-8" data-testid="simulacros-page">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold">Simulacros de Prueba</h1>
          <p className="text-slate-600 mt-1">Practica con exámenes reales antes de la prueba</p>
        </div>
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger asChild>
            <Button className="rounded-full" data-testid="create-quiz-button">
              <Plus size={20} className="mr-2" />
              Crear simulacro
            </Button>
          </DialogTrigger>
          <DialogContent data-testid="create-quiz-dialog">
            <DialogHeader>
              <DialogTitle>Generar nuevo simulacro</DialogTitle>
              <DialogDescription>
                Remy creará un simulacro personalizado basado en el tema que elijas
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4 mt-4">
              <div>
                <Label htmlFor="course">Curso</Label>
                <Select
                  value={formData.course_id}
                  onValueChange={(value) => setFormData(prev => ({ ...prev, course_id: value }))}
                >
                  <SelectTrigger id="course" data-testid="quiz-course-select">
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
              <div>
                <Label htmlFor="topic">Tema</Label>
                <Input
                  id="topic"
                  placeholder="Ej: Derivadas, Integrales, Vectores"
                  value={formData.topic}
                  onChange={(e) => setFormData(prev => ({ ...prev, topic: e.target.value }))}
                  data-testid="quiz-topic-input"
                />
              </div>
              <div>
                <Label htmlFor="num_questions">Número de preguntas</Label>
                <Select
                  value={formData.num_questions.toString()}
                  onValueChange={(value) => setFormData(prev => ({ ...prev, num_questions: parseInt(value) }))}
                >
                  <SelectTrigger id="num_questions" data-testid="quiz-num-questions-select">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="5">5 preguntas</SelectItem>
                    <SelectItem value="10">10 preguntas</SelectItem>
                    <SelectItem value="15">15 preguntas</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <Button
                onClick={handleGenerate}
                disabled={generating}
                data-testid="generate-quiz-button"
                className="w-full rounded-full"
              >
                {generating ? (
                  <>
                    <Loader2 className="animate-spin mr-2" size={20} />
                    Generando...
                  </>
                ) : (
                  'Generar simulacro'
                )}
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

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
            <Button onClick={() => setOpen(true)} data-testid="create-first-quiz-button" className="rounded-full">
              <Plus size={20} className="mr-2" />
              Crear mi primer simulacro
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {quizzes.map((quiz, index) => (
            <Card key={quiz.id} className="hover:shadow-lg transition-all" data-testid={`quiz-card-${index}`}>
              <CardHeader>
                <CardTitle className="text-lg">{quiz.topic || quiz.title || 'Simulacro'}</CardTitle>
                <CardDescription className="space-y-1">
                  <span className="block">{quiz.questions?.length || 0} preguntas</span>
                  {quiz.score !== null && quiz.score !== undefined && (
                    <span className="block text-primary font-medium">
                      Puntuación: {quiz.score}%
                    </span>
                  )}
                  {quiz.created_at && (
                    <span className="block text-xs">
                      {new Date(quiz.created_at).toLocaleDateString('es-ES', {
                        day: 'numeric',
                        month: 'short',
                        year: 'numeric'
                      })}
                    </span>
                  )}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button
                  onClick={() => handleStartQuiz(quiz)}
                  data-testid={`start-quiz-${index}`}
                  className="w-full rounded-full"
                >
                  {quiz.score !== null && quiz.score !== undefined ? 'Reintentar' : 'Comenzar simulacro'}
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default Simulacros;
