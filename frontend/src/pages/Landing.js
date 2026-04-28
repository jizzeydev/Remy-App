import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import { usePricing } from '../hooks/usePricing';
import { 
  BookOpen, Target, Clock, CheckCircle, 
  ChevronDown, ChevronRight, GraduationCap,
  TrendingUp, Lock, Zap, Award, FileText, 
  Search, ClipboardList, Lightbulb, BarChart3,
  ArrowRight, X
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import InlineMd from '@/components/course/InlineMd';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// ==================== HERO SECTION ====================
const HeroSection = ({ trialEnabled = true, trialDays = 7 }) => {
  const navigate = useNavigate();
  
  return (
    <section className="relative min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-cyan-900 overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-cyan-500/20 rounded-full blur-3xl" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-500/20 rounded-full blur-3xl" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-cyan-400/5 rounded-full blur-3xl" />
      </div>
      
      {/* Top Navigation */}
      <nav className="absolute top-0 left-0 right-0 z-20 p-4 md:p-6">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <img src="/remy-logo.png" alt="Remy" className="w-8 h-8 md:w-10 md:h-10 object-contain" />
            <span className="text-white font-bold text-lg md:text-xl">Remy</span>
          </div>
          <div className="flex items-center gap-2 md:gap-4">
            <Button 
              variant="ghost" 
              className="text-white hover:bg-white/10 text-sm md:text-base px-2 md:px-4"
              onClick={() => navigate('/auth')}
              data-testid="nav-login-btn"
            >
              Ingresar
            </Button>
            <Button 
              className="bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-semibold text-sm md:text-base px-3 md:px-4"
              onClick={() => navigate('/auth')}
              data-testid="nav-signup-btn"
            >
              <span className="hidden sm:inline">{trialEnabled ? 'Empieza gratis' : 'Suscríbete'}</span>
              <span className="sm:hidden">{trialEnabled ? 'Gratis' : 'Iniciar'}</span>
            </Button>
          </div>
        </div>
      </nav>
      
      <div className="relative z-10 max-w-6xl mx-auto px-6 py-20 text-center">
        {/* Main heading */}
        <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
          <span className="text-cyan-400">Remonta</span> tus ramos
          <br />
          <span className="text-3xl md:text-5xl font-normal text-slate-300">
            con la mejor plataforma de estudio para la universidad
          </span>
        </h1>
        
        <p className="text-lg md:text-xl text-slate-300 max-w-3xl mx-auto mb-10 leading-relaxed">
          Remy te ayuda a aprobar tus cursos universitarios con 
          <span className="text-cyan-400 font-semibold"> lecciones claras</span>, 
          <span className="text-cyan-400 font-semibold"> simulacros personalizados</span> y 
          <span className="text-cyan-400 font-semibold"> preguntas de prueba adaptadas a tu universidad</span>
        </p>
        
        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
          <Button 
            size="lg" 
            className="bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-bold text-lg px-8 py-6 rounded-full shadow-lg shadow-cyan-500/30 hover:shadow-cyan-400/40 transition-all"
            onClick={() => navigate('/auth')}
            data-testid="hero-cta-primary"
          >
            <Zap className="mr-2" size={24} />
            {trialEnabled ? 'Empieza gratis' : 'Suscríbete ahora'}
          </Button>
          <Button 
            size="lg" 
            variant="outline" 
            className="text-white border-slate-500 hover:bg-white/10 text-lg px-8 py-6 rounded-full"
            onClick={() => document.getElementById('courses').scrollIntoView({ behavior: 'smooth' })}
            data-testid="hero-cta-secondary"
          >
            Ver cursos disponibles
          </Button>
        </div>
        
        {/* Free Trial Badge - Only show if trial enabled */}
        {trialEnabled && (
          <div className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm border border-white/20 rounded-full px-4 py-2 mb-8">
            <Clock size={18} className="text-cyan-400" />
            <span className="text-white/90 text-sm">Prueba gratuita de {trialDays} días · Sin tarjeta de crédito</span>
          </div>
        )}
        
        {/* Scroll indicator */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
          <ChevronDown size={32} className="text-slate-500" />
        </div>
      </div>
    </section>
  );
};

// ==================== PROBLEM SECTION ====================
const ProblemSection = () => {
  const beforeItems = [
    { icon: <Search size={20} />, text: "Buscar PDFs en internet" },
    { icon: <FileText size={20} />, text: "Resolver ejercicios sueltos" },
    { icon: <ClipboardList size={20} />, text: "Intentar encontrar pruebas antiguas" }
  ];

  const afterItems = [
    { icon: <BookOpen size={20} />, text: "Lecciones claras e interactivas" },
    { icon: <Target size={20} />, text: "Simulacros instantáneos" },
    { icon: <GraduationCap size={20} />, text: "Práctica tipo examen" }
  ];

  return (
    <section className="py-20 md:py-28 bg-white">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center mb-12 md:mb-16">
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-slate-900 mb-6 leading-tight">
            Estudiar matemáticas en la universidad
            <br />
            <span className="text-cyan-500">no debería ser tan caótico</span>
          </h2>
          <p className="text-lg md:text-xl text-slate-600 max-w-3xl mx-auto leading-relaxed">
            Muchos estudiantes estudian con PDFs desordenados, ejercicios sueltos y pruebas antiguas difíciles de encontrar.
            <br className="hidden md:block" />
            <span className="block mt-4">
              Esto hace que estudiar tome demasiado tiempo y que practicar para los exámenes sea poco eficiente.
            </span>
          </p>
        </div>

        {/* Highlight box */}
        <div className="bg-cyan-50 border border-cyan-200 rounded-2xl p-6 md:p-8 mb-12 md:mb-16 text-center max-w-4xl mx-auto">
          <Lightbulb className="mx-auto mb-4 text-cyan-500" size={36} />
          <p className="text-lg md:text-xl text-slate-700 font-medium">
            <span className="text-cyan-600 font-bold">Remy</span> organiza el contenido, simplifica el estudio y te permite aprender y practicar en un solo lugar.
          </p>
        </div>

        {/* Before/After comparison */}
        <div className="grid md:grid-cols-2 gap-6 md:gap-8 max-w-4xl mx-auto">
          {/* Before */}
          <Card className="border-2 border-slate-200 bg-slate-50">
            <CardHeader className="pb-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-slate-200 rounded-full flex items-center justify-center">
                  <X className="text-slate-500" size={20} />
                </div>
                <CardTitle className="text-xl text-slate-600">ANTES</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="pt-0">
              <ul className="space-y-4">
                {beforeItems.map((item, index) => (
                  <li key={index} className="flex items-center gap-3 text-slate-600">
                    <span className="text-slate-400">{item.icon}</span>
                    <span>{item.text}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>

          {/* After */}
          <Card className="border-2 border-cyan-300 bg-gradient-to-br from-cyan-50 to-white shadow-lg">
            <CardHeader className="pb-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-cyan-500 rounded-full flex items-center justify-center">
                  <CheckCircle className="text-white" size={20} />
                </div>
                <CardTitle className="text-xl text-cyan-700">CON REMY</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="pt-0">
              <ul className="space-y-4">
                {afterItems.map((item, index) => (
                  <li key={index} className="flex items-center gap-3 text-slate-700 font-medium">
                    <span className="text-cyan-500">{item.icon}</span>
                    <span>{item.text}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
};

// ==================== FEATURES SECTION ====================
const FeaturesSection = () => {
  const features = [
    {
      icon: <Target className="text-cyan-500" size={40} />,
      title: "Simulacros de Prueba",
      description: "Genera simulacros de 5 a 15 preguntas a partir de una gran base de ejercicios inspirados en pruebas reales de tu ramo.",
      color: "cyan"
    },
    {
      icon: <BookOpen className="text-blue-500" size={40} />,
      title: "Lecciones de Calidad",
      description: "Lecciones claras con fórmulas, imágenes y gráficos interactivos diseñados para entender rápido los contenidos.",
      color: "blue"
    },
    {
      icon: <GraduationCap className="text-purple-500" size={40} />,
      title: "Práctica tipo Examen",
      description: "Entrena con simulacros diseñados para parecerse a evaluaciones reales de distintas universidades.",
      color: "purple"
    },
    {
      icon: <BarChart3 className="text-green-500" size={40} />,
      title: "Progreso y Correcciones Inteligentes",
      description: "Después de cada simulacro obtienes tu nota, ves exactamente en qué te equivocaste, accedes a las soluciones paso a paso y recibes recomendaciones sobre qué contenido debes repasar.",
      color: "green"
    }
  ];

  return (
    <section id="features" className="py-20 md:py-28 bg-slate-50">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center mb-12 md:mb-16">
          <Badge className="mb-4 bg-cyan-100 text-cyan-700 hover:bg-cyan-100">
            Funcionalidades
          </Badge>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-slate-900 mb-4">
            Todo lo que necesitas para <span className="text-cyan-500">aprobar</span>
          </h2>
          <p className="text-lg md:text-xl text-slate-600 max-w-2xl mx-auto">
            Herramientas diseñadas para que estudies de forma más inteligente
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6 md:gap-8">
          {features.map((feature, index) => (
            <Card 
              key={index} 
              className="border-2 border-slate-200 hover:border-cyan-200 hover:shadow-xl transition-all group bg-white"
              data-testid={`feature-card-${index}`}
            >
              <CardHeader>
                <div className="p-3 bg-slate-50 rounded-xl group-hover:bg-cyan-50 transition-colors w-fit">
                  {feature.icon}
                </div>
                <CardTitle className="text-xl md:text-2xl mt-4">{feature.title}</CardTitle>
                <CardDescription className="text-base md:text-lg leading-relaxed">
                  {feature.description}
                </CardDescription>
              </CardHeader>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

// ==================== COURSES SECTION (DYNAMIC) ====================
const CoursesSection = () => {
  const [courses, setCourses] = useState([]);
  const [filteredCourses, setFilteredCourses] = useState([]);
  const [universities, setUniversities] = useState([]);
  const [expandedCourse, setExpandedCourse] = useState(null);
  const [chapters, setChapters] = useState({});
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterUniversity, setFilterUniversity] = useState('general'); // Default to General
  const navigate = useNavigate();

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    // Apply filters
    let filtered = [...courses];
    
    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(c => 
        c.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        c.description?.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    
    // University filter
    if (filterUniversity === 'general') {
      filtered = filtered.filter(c => !c.university_id);
    } else if (filterUniversity !== 'all') {
      filtered = filtered.filter(c => c.university_id === filterUniversity);
    }
    
    setFilteredCourses(filtered);
  }, [courses, searchTerm, filterUniversity]);

  const fetchData = async () => {
    try {
      const [coursesRes, unisRes] = await Promise.all([
        axios.get(`${API}/courses`),
        axios.get(`${API}/library-universities`)
      ]);
      setCourses(coursesRes.data);
      setUniversities(unisRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchChapters = async (courseId) => {
    if (chapters[courseId]) return;
    
    try {
      const chaptersRes = await axios.get(`${API}/courses/${courseId}/chapters`);
      const chaptersWithLessons = await Promise.all(
        chaptersRes.data.map(async (chapter) => {
          const lessonsRes = await axios.get(`${API}/chapters/${chapter.id}/lessons`);
          return { ...chapter, lessons: lessonsRes.data };
        })
      );
      setChapters(prev => ({ ...prev, [courseId]: chaptersWithLessons }));
    } catch (error) {
      console.error('Error fetching chapters:', error);
    }
  };

  const toggleCourse = (courseId) => {
    if (expandedCourse === courseId) {
      setExpandedCourse(null);
    } else {
      setExpandedCourse(courseId);
      fetchChapters(courseId);
    }
  };

  return (
    <section id="courses" className="py-20 md:py-28 bg-white">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center mb-12 md:mb-16">
          <Badge className="mb-4 bg-blue-100 text-blue-700 hover:bg-blue-100">
            Contenido
          </Badge>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-slate-900 mb-4">
            Cursos <span className="text-cyan-500">disponibles</span>
          </h2>
          <p className="text-lg md:text-xl text-slate-600 max-w-3xl mx-auto mb-4">
            Nuestros cursos cubren los contenidos fundamentales de matemáticas universitarias.
          </p>
          <p className="text-base text-slate-500 max-w-2xl mx-auto">
            Las lecciones están diseñadas para estudiantes de cualquier universidad. 
            Los simulacros pueden adaptarse según el tipo de evaluación de distintas universidades.
          </p>
        </div>
        
        {/* Filters */}
        <div className="flex flex-col sm:flex-row gap-4 items-center justify-center mb-8">
          <div className="relative w-full sm:w-64">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
            <input
              type="text"
              placeholder="Buscar cursos..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent"
            />
          </div>
          <select
            value={filterUniversity}
            onChange={(e) => setFilterUniversity(e.target.value)}
            className="w-full sm:w-48 px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent bg-white"
          >
            <option value="general">General</option>
            <option value="all">Todas las universidades</option>
            {universities.map((uni) => (
              <option key={uni.id} value={uni.id}>
                {uni.short_name} - {uni.name}
              </option>
            ))}
          </select>
          <span className="text-sm text-slate-500">
            {filteredCourses.length} curso(s)
          </span>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin w-8 h-8 border-4 border-cyan-500 border-t-transparent rounded-full mx-auto" />
          </div>
        ) : filteredCourses.length === 0 ? (
          <Card className="text-center py-12 bg-white border-slate-200">
            <CardContent>
              <GraduationCap className="mx-auto mb-4 text-slate-400" size={48} />
              <p className="text-slate-500">
                {courses.length === 0 
                  ? 'Próximamente más cursos disponibles'
                  : 'No se encontraron cursos con esos filtros'
                }
              </p>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-6">
            {filteredCourses.map((course) => (
              <Card key={course.id} className="overflow-hidden bg-white border-slate-200" data-testid={`course-card-${course.id}`}>
                <CardHeader 
                  className="cursor-pointer hover:bg-slate-50 transition-colors bg-white"
                  onClick={() => toggleCourse(course.id)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="w-14 h-14 md:w-16 md:h-16 bg-gradient-to-br from-cyan-400 to-cyan-600 rounded-xl flex items-center justify-center text-white text-xl md:text-2xl font-bold shadow-lg">
                        {course.title.charAt(0)}
                      </div>
                      <div>
                        <CardTitle className="text-xl md:text-2xl text-slate-900">{course.title}</CardTitle>
                        <CardDescription className="text-sm md:text-base text-slate-600">
                          <InlineMd>{course.description}</InlineMd>
                        </CardDescription>
                        <div className="flex gap-2 mt-2 flex-wrap">
                          <Badge variant="outline" className="border-slate-300 text-slate-700 bg-white">{course.level}</Badge>
                          <Badge variant="outline" className="border-slate-300 text-slate-700 bg-white">{course.category}</Badge>
                          {course.university ? (
                            <Badge className="bg-blue-100 text-blue-700 hover:bg-blue-100">
                              {course.university.short_name === 'GEN' ? 'General' : course.university.short_name}
                            </Badge>
                          ) : (
                            <Badge className="bg-blue-100 text-blue-700 hover:bg-blue-100">General</Badge>
                          )}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      <span className="text-slate-500 hidden sm:block text-sm">Ver contenido</span>
                      {expandedCourse === course.id ? 
                        <ChevronDown size={24} className="text-cyan-500" /> : 
                        <ChevronRight size={24} className="text-slate-400" />
                      }
                    </div>
                  </div>
                </CardHeader>

                {expandedCourse === course.id && (
                  <CardContent className="bg-slate-50 border-t border-slate-200">
                    {!chapters[course.id] ? (
                      <div className="text-center py-8">
                        <div className="animate-spin w-6 h-6 border-2 border-cyan-500 border-t-transparent rounded-full mx-auto" />
                      </div>
                    ) : chapters[course.id].length === 0 ? (
                      <p className="text-slate-500 text-center py-4">Sin contenido disponible</p>
                    ) : (
                      <div className="space-y-4">
                        {chapters[course.id].map((chapter, chIndex) => (
                          <div key={chapter.id} className="bg-white rounded-lg p-4 shadow-sm border border-slate-100">
                            <div className="flex items-center gap-3 mb-3">
                              <span className="w-8 h-8 bg-cyan-100 text-cyan-700 rounded-full flex items-center justify-center font-bold text-sm">
                                {chIndex + 1}
                              </span>
                              <h4 className="font-semibold text-base md:text-lg text-slate-900">{chapter.title}</h4>
                              <Badge variant="secondary" className="ml-auto bg-slate-100 text-slate-700">
                                {chapter.lessons?.length || 0} lecciones
                              </Badge>
                            </div>
                            
                            {chapter.lessons && chapter.lessons.length > 0 && (
                              <div className="ml-11 space-y-2">
                                {chapter.lessons.map((lesson, lIndex) => (
                                  <div 
                                    key={lesson.id}
                                    className="flex items-center gap-3 p-3 bg-slate-50 rounded-lg group border border-slate-100"
                                  >
                                    <Lock size={16} className="text-slate-400" />
                                    <span className="text-slate-700 flex-1 text-sm md:text-base">
                                      {lIndex + 1}. {lesson.title}
                                    </span>
                                    <span className="text-xs text-slate-500">
                                      {lesson.duration_minutes} min
                                    </span>
                                  </div>
                                ))}
                              </div>
                            )}
                          </div>
                        ))}
                        
                        {/* CTA to subscribe */}
                        <div className="text-center pt-4">
                          <Button 
                            className="bg-cyan-500 hover:bg-cyan-400 text-white rounded-full"
                            onClick={() => document.getElementById('pricing').scrollIntoView({ behavior: 'smooth' })}
                            data-testid="course-subscribe-btn"
                          >
                            <Lock className="mr-2" size={18} />
                            Suscríbete para acceder
                          </Button>
                        </div>
                      </div>
                    )}
                  </CardContent>
                )}
              </Card>
            ))}
          </div>
        )}
      </div>
    </section>
  );
};

// ==================== SIMULATION SECTION ====================
const SimulationSection = () => {
  const benefits = [
    { text: "Práctica rápida", icon: <Clock size={20} /> },
    { text: "Preguntas variadas", icon: <Target size={20} /> },
    { text: "Entrenamiento tipo examen", icon: <GraduationCap size={20} /> }
  ];

  return (
    <section className="py-20 md:py-28 bg-gradient-to-br from-slate-900 via-slate-800 to-cyan-900 text-white">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center mb-12">
          <Badge className="mb-4 bg-cyan-500/20 text-cyan-300 hover:bg-cyan-500/20 border-cyan-500/30">
            Simulacros
          </Badge>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-6">
            Practica como si estuvieras en un <span className="text-cyan-400">examen real</span>
          </h2>
          <p className="text-lg md:text-xl text-slate-300 max-w-3xl mx-auto mb-10">
            Con Remy puedes generar simulacros en segundos y entrenar como si estuvieras rindiendo una prueba.
          </p>
        </div>

        {/* Benefits */}
        <div className="flex flex-col sm:flex-row justify-center items-center gap-6 md:gap-12 mb-12">
          {benefits.map((benefit, index) => (
            <div key={index} className="flex items-center gap-3">
              <div className="w-10 h-10 bg-cyan-500/20 rounded-full flex items-center justify-center text-cyan-400">
                {benefit.icon}
              </div>
              <span className="text-lg font-medium">{benefit.text}</span>
            </div>
          ))}
        </div>

        {/* Closing line */}
        <div className="text-center">
          <p className="text-lg text-cyan-300 font-medium italic">
            "Una de las formas más efectivas de prepararte para tus evaluaciones."
          </p>
        </div>
      </div>
    </section>
  );
};

// ==================== PRICING SECTION (DYNAMIC) ====================
const PricingSection = () => {
  const navigate = useNavigate();
  const { monthly, semestral, plans, formatPrice, loading } = usePricing();

  if (loading) {
    return (
      <section id="pricing" className="py-20 md:py-28 bg-slate-50">
        <div className="max-w-5xl mx-auto px-6 text-center">
          <div className="animate-spin w-8 h-8 border-4 border-cyan-500 border-t-transparent rounded-full mx-auto" />
        </div>
      </section>
    );
  }

  // Create plans array for rendering
  const pricingPlans = [monthly, semestral];

  return (
    <section id="pricing" className="py-20 md:py-28 bg-slate-50">
      <div className="max-w-5xl mx-auto px-6">
        <div className="text-center mb-12 md:mb-16">
          <Badge className="mb-4 bg-green-100 text-green-700 hover:bg-green-100">
            Precios
          </Badge>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-slate-900 mb-4">
            Invierte en tu <span className="text-cyan-500">futuro</span>
          </h2>
          <p className="text-lg md:text-xl text-slate-600 max-w-2xl mx-auto">
            Elige el plan que mejor se adapte a tus necesidades. Sin compromisos, cancela cuando quieras.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6 md:gap-8 max-w-4xl mx-auto">
          {pricingPlans.map((plan) => {
            const isPopular = plan.is_popular;
            const hasDiscount = plan.discount_active && plan.discount_percentage > 0;
            
            return (
              <Card 
                key={plan.id}
                className={`relative overflow-hidden transition-all hover:shadow-2xl bg-white ${
                  isPopular 
                    ? 'border-2 border-cyan-500 shadow-xl md:scale-105' 
                    : 'border-slate-200 hover:border-cyan-200'
                }`}
                data-testid={`pricing-card-${plan.id}`}
              >
                {/* Popular badge */}
                {isPopular && (
                  <div className="absolute top-0 left-0 right-0 bg-cyan-500 text-white text-center py-1 text-sm font-semibold">
                    MÁS POPULAR
                  </div>
                )}
                
                {/* Discount badge */}
                {hasDiscount && (
                  <div className="absolute top-4 right-4">
                    <Badge className="bg-red-500 text-white hover:bg-red-500 text-sm px-3 py-1">
                      {plan.discount_percentage}% DCTO
                    </Badge>
                  </div>
                )}
                
                <CardHeader className={`${isPopular ? 'pt-10 bg-cyan-50' : 'bg-white'}`}>
                  <CardTitle className="text-xl md:text-2xl text-slate-900">{plan.name}</CardTitle>
                  <CardDescription className="text-base text-slate-600">{plan.description}</CardDescription>
                  
                  <div className="mt-4">
                    {hasDiscount && plan.original_amount && (
                      <span className="text-slate-400 line-through text-lg mr-2">
                        {formatPrice(plan.original_amount)}
                      </span>
                    )}
                    <span className="text-4xl md:text-5xl font-bold text-slate-900">
                      {formatPrice(plan.amount)}
                    </span>
                    <span className="text-slate-500 text-base md:text-lg">
                      /{plan.period}
                    </span>
                  </div>
                </CardHeader>
                
                <CardContent className="pt-6 bg-white">
                  <ul className="space-y-3 md:space-y-4 mb-8">
                    {plan.features.map((feature, fIndex) => (
                      <li key={fIndex} className="flex items-start gap-3">
                        <CheckCircle className="text-cyan-500 flex-shrink-0 mt-0.5" size={20} />
                        <span className="text-slate-600 text-sm md:text-base">{feature}</span>
                      </li>
                    ))}
                  </ul>
                  
                  <Button 
                    className={`w-full py-5 md:py-6 text-base md:text-lg rounded-full ${
                      isPopular 
                        ? 'bg-cyan-500 hover:bg-cyan-400 text-white shadow-lg shadow-cyan-500/30' 
                        : 'bg-slate-900 hover:bg-slate-800 text-white'
                    }`}
                    onClick={() => navigate(`/auth?redirect=/subscribe?plan=${plan.id}`)}
                    data-testid={`subscribe-btn-${plan.id}`}
                  >
                    {isPopular ? 'Suscribirse y Ahorrar' : 'Suscribirse'}
                  </Button>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Guarantee */}
        <div className="text-center mt-10 md:mt-12 p-6 bg-white rounded-2xl border border-slate-200 max-w-2xl mx-auto shadow-sm">
          <Award className="mx-auto mb-3 text-cyan-500" size={32} />
          <h4 className="font-semibold text-lg mb-2 text-slate-900">Garantía de satisfacción</h4>
          <p className="text-slate-600">
            Si no estás satisfecho en los primeros 7 días, te devolvemos el 100% de tu dinero. Sin preguntas.
          </p>
        </div>
      </div>
    </section>
  );
};

// ==================== FREE TRIAL SECTION ====================
const FreeTrialSection = ({ trialDays = 7 }) => {
  const navigate = useNavigate();

  const trialFeatures = [
    "Acceso a todas las lecciones",
    "Hasta 10 simulacros durante la prueba",
    "Seguimiento de progreso",
    "Cancela cuando quieras"
  ];

  return (
    <section className="py-20 md:py-28 bg-gradient-to-br from-slate-900 via-slate-800 to-cyan-900 text-white overflow-hidden relative">
      {/* Background decorations */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl" />
      <div className="absolute bottom-0 left-0 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl" />
      
      <div className="max-w-5xl mx-auto px-6 relative z-10">
        <div className="text-center mb-12">
          <Badge className="mb-4 bg-cyan-500/20 text-cyan-300 hover:bg-cyan-500/20 border-cyan-500/30 px-4 py-1">
            <Clock size={14} className="mr-1 inline" />
            Sin tarjeta de crédito
          </Badge>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4">
            Pruébalo <span className="text-cyan-400">gratis</span> por {trialDays} días
          </h2>
          <p className="text-lg md:text-xl text-slate-300 max-w-2xl mx-auto">
            Explora todas las lecciones, genera simulacros y descubre cómo Remy puede ayudarte a estudiar más rápido.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-4 mb-12">
          {trialFeatures.map((feature, index) => (
            <div 
              key={index}
              className="bg-white/10 backdrop-blur-sm border border-white/10 rounded-xl p-4 text-center"
            >
              <CheckCircle className="mx-auto mb-2 text-cyan-400" size={24} />
              <p className="text-sm font-medium">{feature}</p>
            </div>
          ))}
        </div>

        {/* CTA */}
        <div className="text-center">
          <Button 
            size="lg" 
            className="bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-bold text-lg px-10 py-6 rounded-full shadow-lg shadow-cyan-500/30"
            onClick={() => navigate('/auth')}
            data-testid="trial-section-cta"
          >
            <Zap className="mr-2" size={24} />
            Crear cuenta gratis
          </Button>
          <p className="text-slate-400 text-sm mt-4">
            Configura tu cuenta en menos de 1 minuto
          </p>
        </div>
      </div>
    </section>
  );
};

// ==================== FINAL CTA SECTION ====================
const FinalCTASection = () => {
  const navigate = useNavigate();

  return (
    <section className="py-20 md:py-28 bg-white">
      <div className="max-w-4xl mx-auto px-6 text-center">
        <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-slate-900 mb-6">
          Empieza a estudiar matemáticas de forma más <span className="text-cyan-500">inteligente</span>
        </h2>
        <p className="text-lg md:text-xl text-slate-600 mb-10 max-w-2xl mx-auto">
          Menos tiempo buscando material. Más tiempo aprendiendo y practicando.
        </p>
        <Button 
          size="lg" 
          className="bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-bold text-lg px-10 py-6 rounded-full shadow-lg shadow-cyan-500/30 hover:shadow-cyan-400/40 transition-all"
          onClick={() => navigate('/auth')}
          data-testid="final-cta-btn"
        >
          Crear cuenta gratis
          <ArrowRight className="ml-2" size={24} />
        </Button>
      </div>
    </section>
  );
};

// ==================== FOOTER ====================
const Footer = () => {
  return (
    <footer className="bg-slate-900 text-white py-12">
      <div className="max-w-6xl mx-auto px-6">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-3">
            <img 
              src="/remy-logo.png" 
              alt="Remy" 
              className="w-12 h-12 object-contain"
            />
            <div>
              <h3 className="font-bold text-xl">Remy</h3>
              <p className="text-slate-400 text-sm">by Se Remonta</p>
            </div>
          </div>
          
          <div className="flex gap-6 md:gap-8 text-slate-400 text-sm md:text-base">
            <a href="#features" className="hover:text-cyan-400 transition-colors">
              Funcionalidades
            </a>
            <a href="#courses" className="hover:text-cyan-400 transition-colors">
              Cursos
            </a>
            <a href="#pricing" className="hover:text-cyan-400 transition-colors">
              Precios
            </a>
          </div>
          
          <p className="text-slate-500 text-sm">
            © 2026 Se Remonta. Todos los derechos reservados.
          </p>
        </div>
      </div>
    </footer>
  );
};

// ==================== MAIN LANDING PAGE ====================
const Landing = () => {
  const navigate = useNavigate();
  const { isAuthenticated, loading } = useAuth();
  const [trialEnabled, setTrialEnabled] = useState(true);
  const [trialDays, setTrialDays] = useState(7);

  // Force light mode on landing page - remove dark class if present
  useEffect(() => {
    const root = document.documentElement;
    const wasDark = root.classList.contains('dark');
    if (wasDark) {
      root.classList.remove('dark');
    }
    // Restore dark mode when leaving if it was set
    return () => {
      const theme = localStorage.getItem('remy-theme');
      if (theme === 'dark') {
        root.classList.add('dark');
      }
    };
  }, []);

  // Load trial status from backend
  useEffect(() => {
    const fetchTrialStatus = async () => {
      try {
        const response = await axios.get(`${API}/admin/analytics/public/trial-status`);
        setTrialEnabled(response.data.enabled);
        setTrialDays(response.data.trial_days || 7);
      } catch (error) {
        // Default to enabled if API fails
        console.error('Error fetching trial status:', error);
      }
    };
    fetchTrialStatus();
  }, []);

  // Redirect authenticated users to dashboard
  useEffect(() => {
    if (!loading && isAuthenticated) {
      navigate('/dashboard', { replace: true });
    }
  }, [isAuthenticated, loading, navigate]);

  // Show loading while checking auth
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-cyan-900 flex items-center justify-center">
        <div className="text-center">
          <img src="/remy-logo.png" alt="Remy" className="w-16 h-16 mx-auto mb-4 animate-pulse" />
          <div className="animate-spin w-8 h-8 border-4 border-cyan-500 border-t-transparent rounded-full mx-auto" />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <HeroSection trialEnabled={trialEnabled} trialDays={trialDays} />
      <ProblemSection />
      <FeaturesSection />
      <CoursesSection />
      <SimulationSection />
      <PricingSection />
      {trialEnabled && <FreeTrialSection trialDays={trialDays} />}
      <FinalCTASection trialEnabled={trialEnabled} />
      <Footer />
    </div>
  );
};

export default Landing;
