import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { toast } from 'sonner';
import 'katex/dist/katex.min.css';
import { InlineMath, BlockMath } from 'react-katex';
import { 
  GraduationCap, Building2, BookOpen, 
  ChevronRight, Play, Loader2, ArrowLeft,
  CheckCircle, Image as ImageIcon, Lock
} from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../components/ui/select';
import { useAuth } from '../contexts/AuthContext';
import SubscriptionRequired from '../components/SubscriptionRequired';

const API_URL = process.env.REACT_APP_BACKEND_URL;

// Component to render text with LaTeX
const MathText = ({ text }) => {
  if (!text) return null;
  
  // Split by $ for inline math and $$ for block math
  const parts = [];
  let remaining = text;
  let key = 0;
  
  // Handle block math first ($$...$$)
  while (remaining.includes('$$')) {
    const start = remaining.indexOf('$$');
    const end = remaining.indexOf('$$', start + 2);
    
    if (end === -1) break;
    
    if (start > 0) {
      parts.push(<span key={key++}>{remaining.substring(0, start)}</span>);
    }
    
    const math = remaining.substring(start + 2, end);
    try {
      parts.push(<BlockMath key={key++} math={math} />);
    } catch (e) {
      parts.push(<span key={key++} className="text-red-500">{math}</span>);
    }
    remaining = remaining.substring(end + 2);
  }
  
  // Handle inline math ($...$)
  if (remaining.includes('$')) {
    const regex = /\$([^$]+)\$/g;
    let lastIndex = 0;
    let match;
    
    while ((match = regex.exec(remaining)) !== null) {
      if (match.index > lastIndex) {
        parts.push(<span key={key++}>{remaining.substring(lastIndex, match.index)}</span>);
      }
      try {
        parts.push(<InlineMath key={key++} math={match[1]} />);
      } catch (e) {
        parts.push(<span key={key++} className="text-red-500">{match[1]}</span>);
      }
      lastIndex = regex.lastIndex;
    }
    if (lastIndex < remaining.length) {
      parts.push(<span key={key++}>{remaining.substring(lastIndex)}</span>);
    }
  } else if (remaining) {
    parts.push(<span key={key++}>{remaining}</span>);
  }
  
  return <>{parts}</>;
};

const TuUniversidad = () => {
  const navigate = useNavigate();
  const { user, hasActiveSubscription, isInTrial, trialSimulationsRemaining } = useAuth();
  
  // Check access
  const hasAccess = hasActiveSubscription || isInTrial;
  const uniSimsUsed = user?.trial_university_simulations_used || 0;
  const uniSimsLimit = user?.trial_university_simulations_limit || 1;
  const canDoUniSimulation = hasActiveSubscription || (isInTrial && uniSimsUsed < uniSimsLimit);
  
  // Selection state
  const [universities, setUniversities] = useState([]);
  const [selectedUniversity, setSelectedUniversity] = useState(null);
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [evaluations, setEvaluations] = useState([]);
  const [selectedEvaluation, setSelectedEvaluation] = useState(null);
  
  // Quiz state
  const [numQuestions, setNumQuestions] = useState(5);
  const [loading, setLoading] = useState(false);
  const [generatingQuiz, setGeneratingQuiz] = useState(false);
  
  // Active quiz state
  const [activeQuiz, setActiveQuiz] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [quizResult, setQuizResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (hasAccess) {
      fetchUniversities();
    }
  }, [hasAccess]);

  const fetchUniversities = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}/api/universities`);
      setUniversities(response.data);
    } catch (error) {
      toast.error('Error al cargar universidades');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectUniversity = async (university) => {
    setSelectedUniversity(university);
    setSelectedCourse(null);
    setSelectedEvaluation(null);
    setEvaluations([]);
    
    try {
      const response = await axios.get(`${API_URL}/api/universities/${university.id}`);
      setCourses(response.data.courses || []);
    } catch (error) {
      toast.error('Error al cargar cursos');
    }
  };

  const handleSelectCourse = async (course) => {
    setSelectedCourse(course);
    setSelectedEvaluation(null);
    
    try {
      const response = await axios.get(
        `${API_URL}/api/universities/${selectedUniversity.id}/courses/${course.id}`
      );
      setEvaluations(response.data.evaluations || []);
    } catch (error) {
      toast.error('Error al cargar evaluaciones');
    }
  };

  const handleStartSimulation = async () => {
    if (!selectedEvaluation) {
      toast.error('Selecciona una evaluación primero');
      return;
    }
    
    setGeneratingQuiz(true);
    try {
      const token = localStorage.getItem('token');
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      
      const response = await axios.post(
        `${API_URL}/api/universities/${selectedUniversity.id}/courses/${selectedCourse.id}/simulation`,
        {
          evaluation_id: selectedEvaluation.id,
          num_questions: numQuestions
        },
        { headers }
      );
      
      setActiveQuiz(response.data);
      setCurrentQuestionIndex(0);
      setAnswers({});
      setQuizResult(null);
      toast.success(`Simulacro iniciado con ${response.data.total_questions} preguntas`);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Error al iniciar simulacro');
    } finally {
      setGeneratingQuiz(false);
    }
  };

  const handleSelectAnswer = (questionId, answer) => {
    setAnswers(prev => ({ ...prev, [questionId]: answer }));
  };

  const handleSubmitQuiz = async () => {
    if (Object.keys(answers).length < activeQuiz.questions.length) {
      const unanswered = activeQuiz.questions.length - Object.keys(answers).length;
      if (!window.confirm(`Tienes ${unanswered} pregunta(s) sin responder. ¿Enviar de todas formas?`)) {
        return;
      }
    }
    
    setSubmitting(true);
    try {
      const token = localStorage.getItem('token');
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      
      const response = await axios.post(
        `${API_URL}/api/universities/simulation/${activeQuiz.simulation_id}/submit`,
        { answers },
        { headers }
      );
      
      setQuizResult(response.data);
      toast.success(`Resultado: ${response.data.score}%`);
    } catch (error) {
      toast.error('Error al enviar respuestas');
    } finally {
      setSubmitting(false);
    }
  };

  const resetQuiz = () => {
    setActiveQuiz(null);
    setQuizResult(null);
    setAnswers({});
    setCurrentQuestionIndex(0);
  };

  // Show paywall if no access
  if (!hasAccess) {
    return (
      <SubscriptionRequired 
        feature="Tu Universidad" 
        description="Accede a simulacros personalizados con preguntas de exámenes reales de tu universidad."
      />
    );
  }

  // Render active quiz
  if (activeQuiz && !quizResult) {
    const currentQuestion = activeQuiz.questions[currentQuestionIndex];
    
    return (
      <div className="min-h-screen bg-background py-8 px-4">
        <div className="max-w-3xl mx-auto">
          {/* Quiz Header */}
          <div className="mb-6 flex items-center justify-between">
            <div>
              <h1 className="text-xl font-bold text-foreground">{activeQuiz.evaluation}</h1>
              <p className="text-muted-foreground text-sm">{activeQuiz.course} - {activeQuiz.university}</p>
            </div>
            <Badge className="bg-primary/20 text-primary">
              {currentQuestionIndex + 1} / {activeQuiz.total_questions}
            </Badge>
          </div>
          
          {/* Progress bar */}
          <div className="h-2 bg-secondary rounded-full mb-8 overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-primary to-blue-500 transition-all duration-300"
              style={{ width: `${((currentQuestionIndex + 1) / activeQuiz.total_questions) * 100}%` }}
            />
          </div>
          
          {/* Question Card */}
          <Card className="mb-6 shadow-lg">
            <CardContent className="pt-6">
              <div className="text-lg text-foreground mb-6">
                <MathText text={currentQuestion.question_content} />
              </div>
              
              {/* Question Image */}
              {currentQuestion.image_url && (
                <div className="mb-6 flex justify-center">
                  <img 
                    src={currentQuestion.image_url} 
                    alt="Imagen de la pregunta"
                    className="max-w-full max-h-80 rounded-lg border border-border"
                  />
                </div>
              )}
              
              {/* Options */}
              <div className="space-y-3">
                {currentQuestion.options.map((option, idx) => {
                  const letter = String.fromCharCode(65 + idx);
                  const isSelected = answers[currentQuestion.id] === letter;
                  
                  return (
                    <button
                      key={idx}
                      onClick={() => handleSelectAnswer(currentQuestion.id, letter)}
                      className={`w-full p-4 rounded-lg text-left transition-all flex items-start gap-3 border-2 ${
                        isSelected 
                          ? 'bg-primary/10 border-primary text-foreground' 
                          : 'bg-card border-border text-muted-foreground hover:border-primary/50 hover:bg-primary/5'
                      }`}
                    >
                      <span className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0 ${
                        isSelected ? 'bg-primary text-primary-foreground' : 'bg-secondary text-muted-foreground'
                      }`}>
                        {letter}
                      </span>
                      <span className="flex-1 pt-1">
                        <MathText text={option} />
                      </span>
                    </button>
                  );
                })}
              </div>
            </CardContent>
          </Card>
          
          {/* Navigation */}
          <div className="flex items-center justify-between">
            <Button
              variant="outline"
              onClick={() => setCurrentQuestionIndex(prev => prev - 1)}
              disabled={currentQuestionIndex === 0}
            >
              Anterior
            </Button>
            
            <div className="flex gap-2 flex-wrap justify-center">
              {activeQuiz.questions.map((_, idx) => (
                <button
                  key={idx}
                  onClick={() => setCurrentQuestionIndex(idx)}
                  className={`w-8 h-8 rounded-full text-xs font-medium transition-all ${
                    idx === currentQuestionIndex
                      ? 'bg-primary text-primary-foreground'
                      : answers[activeQuiz.questions[idx].id]
                        ? 'bg-green-500/20 text-green-600 dark:text-green-400 border-2 border-green-500'
                        : 'bg-secondary text-muted-foreground'
                  }`}
                >
                  {idx + 1}
                </button>
              ))}
            </div>
            
            {currentQuestionIndex < activeQuiz.total_questions - 1 ? (
              <Button onClick={() => setCurrentQuestionIndex(prev => prev + 1)} className="bg-primary hover:bg-primary/90">
                Siguiente
              </Button>
            ) : (
              <Button onClick={handleSubmitQuiz} disabled={submitting} className="bg-green-500 hover:bg-green-600">
                {submitting ? <><Loader2 className="animate-spin mr-2" size={16} /> Enviando...</> : 'Finalizar'}
              </Button>
            )}
          </div>
        </div>
      </div>
    );
  }

  // Render quiz result
  if (quizResult) {
    return (
      <div className="min-h-screen bg-background py-8 px-4">
        <div className="max-w-3xl mx-auto">
          {/* Result Header */}
          <Card className="mb-6 shadow-lg">
            <CardContent className="pt-6 text-center">
              <div className={`w-24 h-24 mx-auto rounded-full flex items-center justify-center mb-4 ${
                quizResult.score >= 60 ? 'bg-green-500/20' : 'bg-red-500/20'
              }`}>
                <span className={`text-4xl font-bold ${
                  quizResult.score >= 60 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'
                }`}>
                  {quizResult.score}%
                </span>
              </div>
              <h2 className="text-2xl font-bold text-foreground mb-2">
                {quizResult.score >= 60 ? '¡Buen trabajo!' : 'Sigue practicando'}
              </h2>
              <p className="text-muted-foreground">
                {quizResult.correct_count} de {quizResult.total_questions} respuestas correctas
              </p>
              <div className="mt-4 text-sm text-muted-foreground">
                {quizResult.university} - {quizResult.course} - {quizResult.evaluation}
              </div>
            </CardContent>
          </Card>
          
          {/* Results Detail */}
          <div className="space-y-4 mb-6">
            {quizResult.results.map((r, idx) => (
              <Card 
                key={idx} 
                className={`border-l-4 ${r.is_correct ? 'border-l-green-500' : 'border-l-red-500'}`}
              >
                <CardContent className="pt-4">
                  <div className="flex items-start gap-3">
                    <div className={`w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0 ${
                      r.is_correct ? 'bg-green-500' : 'bg-red-500'
                    }`}>
                      {r.is_correct ? (
                        <CheckCircle size={14} className="text-white" />
                      ) : (
                        <span className="text-white text-xs font-bold">X</span>
                      )}
                    </div>
                    <div className="flex-1">
                      <div className="text-foreground text-sm mb-2">
                        <MathText text={r.question_content} />
                      </div>
                      
                      {/* Question Image in Results */}
                      {r.image_url && (
                        <div className="mb-3">
                          <img 
                            src={r.image_url} 
                            alt="Imagen"
                            className="max-w-xs max-h-40 rounded border border-border"
                          />
                        </div>
                      )}
                      
                      <div className="flex gap-4 text-xs">
                        <span className={r.is_correct ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}>
                          Tu respuesta: {r.user_answer || '-'}
                        </span>
                        {!r.is_correct && (
                          <span className="text-green-600 dark:text-green-400">Correcta: {r.correct_answer}</span>
                        )}
                      </div>
                      {r.solution_content && (
                        <div className="mt-2 p-3 bg-secondary rounded text-sm text-foreground border border-border">
                          <strong>Solución:</strong> <MathText text={r.solution_content} />
                        </div>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
          
          {/* Actions */}
          <div className="flex gap-4">
            <Button variant="outline" onClick={resetQuiz} className="flex-1">
              <ArrowLeft size={16} className="mr-2" /> Volver
            </Button>
            <Button onClick={handleStartSimulation} className="flex-1 bg-primary hover:bg-primary/90">
              <Play size={16} className="mr-2" /> Nuevo Simulacro
            </Button>
          </div>
        </div>
      </div>
    );
  }

  // Render selection UI
  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <div className="w-16 h-16 bg-gradient-to-br from-primary to-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
          <GraduationCap size={32} className="text-white" />
        </div>
        <h1 className="text-3xl font-bold text-foreground mb-2">Tu Universidad</h1>
        <p className="text-muted-foreground max-w-xl mx-auto">
          Selecciona tu universidad, curso y evaluación para generar un simulacro 
          personalizado con preguntas de exámenes anteriores.
        </p>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-20">
          <Loader2 className="animate-spin text-primary" size={40} />
        </div>
      ) : (
        <div className="grid md:grid-cols-3 gap-6">
          {/* Step 1: Universities */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-bold">1</div>
              <h2 className="text-lg font-semibold text-foreground">Universidad</h2>
            </div>
            <div className="space-y-2">
              {universities.map(uni => (
                <button
                  key={uni.id}
                  onClick={() => handleSelectUniversity(uni)}
                  className={`w-full p-4 rounded-lg text-left transition-all border-2 ${
                    selectedUniversity?.id === uni.id
                      ? 'bg-primary/10 border-primary'
                      : 'bg-card border-border hover:border-primary/50'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-gradient-to-br from-primary to-blue-600 rounded-lg flex items-center justify-center text-white font-bold text-sm">
                      {uni.short_name?.substring(0, 2) || uni.name.charAt(0)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-foreground font-medium truncate">{uni.name}</p>
                      <p className="text-muted-foreground text-sm">{uni.courses_count} cursos</p>
                    </div>
                    {selectedUniversity?.id === uni.id && (
                      <ChevronRight className="text-primary" size={20} />
                    )}
                  </div>
                </button>
              ))}
              {universities.length === 0 && (
                <p className="text-muted-foreground text-center py-8">No hay universidades disponibles</p>
              )}
            </div>
          </div>

          {/* Step 2: Courses */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold ${
                selectedUniversity ? 'bg-primary text-primary-foreground' : 'bg-secondary text-muted-foreground'
              }`}>2</div>
              <h2 className="text-lg font-semibold text-foreground">Curso</h2>
            </div>
            {selectedUniversity ? (
              <div className="space-y-2">
                {courses.map(course => (
                  <button
                    key={course.id}
                    onClick={() => handleSelectCourse(course)}
                    className={`w-full p-4 rounded-lg text-left transition-all border-2 ${
                      selectedCourse?.id === course.id
                        ? 'bg-primary/10 border-primary'
                        : 'bg-card border-border hover:border-primary/50'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-foreground font-medium">{course.name}</p>
                        {course.code && (
                          <Badge variant="outline" className="text-muted-foreground mt-1">{course.code}</Badge>
                        )}
                      </div>
                      <span className="text-muted-foreground text-sm">{course.evaluations_count} eval.</span>
                    </div>
                  </button>
                ))}
                {courses.length === 0 && (
                  <p className="text-muted-foreground text-center py-8">No hay cursos disponibles</p>
                )}
              </div>
            ) : (
              <div className="bg-secondary/50 rounded-lg p-8 text-center border-2 border-dashed border-border">
                <Building2 className="mx-auto text-muted-foreground mb-2" size={32} />
                <p className="text-muted-foreground">Selecciona una universidad</p>
              </div>
            )}
          </div>

          {/* Step 3: Evaluations & Start */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold ${
                selectedCourse ? 'bg-primary text-primary-foreground' : 'bg-secondary text-muted-foreground'
              }`}>3</div>
              <h2 className="text-lg font-semibold text-foreground">Evaluación</h2>
            </div>
            {selectedCourse ? (
              <div className="space-y-4">
                <div className="space-y-2">
                  {evaluations.map(evaluation => (
                    <button
                      key={evaluation.id}
                      onClick={() => setSelectedEvaluation(evaluation)}
                      className={`w-full p-4 rounded-lg text-left transition-all border-2 ${
                        selectedEvaluation?.id === evaluation.id
                          ? 'bg-primary/10 border-primary'
                          : 'bg-card border-border hover:border-primary/50'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-foreground font-medium">{evaluation.name}</p>
                          {evaluation.description && (
                            <p className="text-muted-foreground text-sm mt-1">{evaluation.description}</p>
                          )}
                        </div>
                        <Badge className="bg-secondary text-secondary-foreground">{evaluation.questions_count} preg.</Badge>
                      </div>
                    </button>
                  ))}
                  {evaluations.length === 0 && (
                    <p className="text-muted-foreground text-center py-4">No hay evaluaciones disponibles</p>
                  )}
                </div>

                {/* Quiz Configuration */}
                {selectedEvaluation && (
                  <Card className="shadow-md">
                    <CardHeader className="pb-3">
                      <CardTitle className="text-base">Configuración</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div>
                        <label className="text-sm text-muted-foreground mb-1 block">Número de preguntas</label>
                        <Select value={numQuestions.toString()} onValueChange={(v) => setNumQuestions(parseInt(v))}>
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="5">5 preguntas</SelectItem>
                            <SelectItem value="10">10 preguntas</SelectItem>
                            <SelectItem value="15">15 preguntas</SelectItem>
                            <SelectItem value="20">20 preguntas</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      
                      {/* Trial limit warning */}
                      {isInTrial && !hasActiveSubscription && (
                        <div className={`p-3 rounded-lg text-sm ${
                          canDoUniSimulation 
                            ? 'bg-amber-500/10 border border-amber-500/30 text-amber-600 dark:text-amber-400'
                            : 'bg-red-500/10 border border-red-500/30 text-red-600 dark:text-red-400'
                        }`}>
                          {canDoUniSimulation ? (
                            <>
                              <Lock size={14} className="inline mr-1" />
                              Prueba gratuita: {uniSimsLimit - uniSimsUsed} simulacro(s) universitario(s) disponible(s)
                            </>
                          ) : (
                            <>
                              <Lock size={14} className="inline mr-1" />
                              Ya usaste tu simulacro universitario de prueba. 
                              <Button 
                                variant="link" 
                                className="p-0 h-auto text-red-600 dark:text-red-400 underline ml-1"
                                onClick={() => navigate('/suscribirse')}
                              >
                                Suscríbete para acceso ilimitado
                              </Button>
                            </>
                          )}
                        </div>
                      )}
                      
                      <Button 
                        onClick={handleStartSimulation}
                        disabled={generatingQuiz || selectedEvaluation.questions_count === 0 || !canDoUniSimulation}
                        className="w-full bg-gradient-to-r from-primary to-blue-600 hover:from-primary/90 hover:to-blue-700"
                      >
                        {generatingQuiz ? (
                          <><Loader2 className="animate-spin mr-2" size={16} /> Generando...</>
                        ) : !canDoUniSimulation ? (
                          <><Lock size={16} className="mr-2" /> Límite alcanzado</>
                        ) : (
                          <><Play size={16} className="mr-2" /> Iniciar Simulacro</>
                        )}
                      </Button>
                      
                      {selectedEvaluation.questions_count === 0 && (
                        <p className="text-amber-600 dark:text-amber-400 text-xs text-center">Esta evaluación aún no tiene preguntas</p>
                      )}
                    </CardContent>
                  </Card>
                )}
              </div>
            ) : (
              <div className="bg-secondary/50 rounded-lg p-8 text-center border-2 border-dashed border-border">
                <BookOpen className="mx-auto text-muted-foreground mb-2" size={32} />
                <p className="text-muted-foreground">Selecciona un curso</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default TuUniversidad;
