import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { 
  BookOpen, Brain, Target, Clock, CheckCircle, Star, 
  ChevronDown, ChevronRight, Sparkles, GraduationCap,
  TrendingUp, MessageSquare, Lock, Zap, Users, Award
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// ==================== HERO SECTION ====================
const HeroSection = () => {
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
      <nav className="absolute top-0 left-0 right-0 z-20 p-6">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <img src="/remy-logo.png" alt="Remy" className="w-10 h-10 object-contain" />
            <span className="text-white font-bold text-xl">Remy</span>
          </div>
          <div className="flex items-center gap-4">
            <Button 
              variant="ghost" 
              className="text-white hover:bg-white/10"
              onClick={() => navigate('/auth')}
            >
              Iniciar sesión
            </Button>
            <Button 
              className="bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-semibold"
              onClick={() => navigate('/auth')}
            >
              Comenzar gratis
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
            con tu tutor IA personal
          </span>
        </h1>
        
        <p className="text-xl md:text-2xl text-slate-300 max-w-3xl mx-auto mb-10 leading-relaxed">
          Remy te ayuda a aprobar tus cursos universitarios con 
          <span className="text-cyan-400 font-semibold"> lecciones de calidad</span>, 
          <span className="text-cyan-400 font-semibold"> simulacros personalizados</span> y 
          <span className="text-cyan-400 font-semibold"> asistencia IA 24/7</span>
        </p>
        
        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
          <Button 
            size="lg" 
            className="bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-bold text-lg px-8 py-6 rounded-full shadow-lg shadow-cyan-500/30 hover:shadow-cyan-400/40 transition-all"
            onClick={() => document.getElementById('pricing').scrollIntoView({ behavior: 'smooth' })}
          >
            <Zap className="mr-2" size={24} />
            Comenzar ahora
          </Button>
          <Button 
            size="lg" 
            variant="outline" 
            className="text-white border-slate-500 hover:bg-white/10 text-lg px-8 py-6 rounded-full"
            onClick={() => document.getElementById('courses').scrollIntoView({ behavior: 'smooth' })}
          >
            Ver cursos disponibles
          </Button>
        </div>
        
        {/* Scroll indicator */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
          <ChevronDown size={32} className="text-slate-500" />
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
      description: "Practica con exámenes personalizados. Elige los temas, dificultad y tiempo. Recibe tu nota al instante con explicaciones detalladas.",
      badge: "Disponible"
    },
    {
      icon: <BookOpen className="text-blue-500" size={40} />,
      title: "Lecciones de Calidad",
      description: "Contenido creado por expertos con fórmulas matemáticas, gráficos interactivos y explicaciones paso a paso.",
      badge: "Disponible"
    },
    {
      icon: <TrendingUp className="text-green-500" size={40} />,
      title: "Seguimiento de Progreso",
      description: "Visualiza tu avance en cada curso. Identifica tus fortalezas y áreas a mejorar con estadísticas detalladas.",
      badge: "Próximamente"
    },
    {
      icon: <MessageSquare className="text-purple-500" size={40} />,
      title: "Tutor IA Remy 24/7",
      description: "Pregúntale a Remy cualquier duda sobre tus materias. Disponible las 24 horas para ayudarte a entender los conceptos.",
      badge: "Próximamente"
    }
  ];

  return (
    <section id="features" className="py-24 bg-white">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center mb-16">
          <Badge className="mb-4 bg-cyan-100 text-cyan-700 hover:bg-cyan-100">
            Funcionalidades
          </Badge>
          <h2 className="text-4xl md:text-5xl font-bold text-slate-900 mb-4">
            Todo lo que necesitas para <span className="text-cyan-500">aprobar</span>
          </h2>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto">
            Remy combina las mejores herramientas de estudio con inteligencia artificial para maximizar tu aprendizaje
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {features.map((feature, index) => (
            <Card 
              key={index} 
              className="border-2 hover:border-cyan-200 hover:shadow-xl transition-all group"
            >
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="p-3 bg-slate-50 rounded-xl group-hover:bg-cyan-50 transition-colors">
                    {feature.icon}
                  </div>
                  <Badge variant={feature.badge === "Disponible" ? "default" : "secondary"}>
                    {feature.badge}
                  </Badge>
                </div>
                <CardTitle className="text-2xl mt-4">{feature.title}</CardTitle>
                <CardDescription className="text-lg">
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

// ==================== COURSES PREVIEW SECTION ====================
const CoursesPreviewSection = () => {
  const [courses, setCourses] = useState([]);
  const [expandedCourse, setExpandedCourse] = useState(null);
  const [chapters, setChapters] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    try {
      const response = await axios.get(`${API}/courses`);
      setCourses(response.data);
    } catch (error) {
      console.error('Error fetching courses:', error);
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
    <section id="courses" className="py-24 bg-slate-50">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center mb-16">
          <Badge className="mb-4 bg-blue-100 text-blue-700 hover:bg-blue-100">
            Contenido
          </Badge>
          <h2 className="text-4xl md:text-5xl font-bold text-slate-900 mb-4">
            Cursos <span className="text-cyan-500">disponibles</span>
          </h2>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto">
            Explora todo el contenido de nuestros cursos. Suscríbete para acceder a las lecciones completas.
          </p>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin w-8 h-8 border-4 border-cyan-500 border-t-transparent rounded-full mx-auto" />
          </div>
        ) : courses.length === 0 ? (
          <Card className="text-center py-12">
            <CardContent>
              <GraduationCap className="mx-auto mb-4 text-slate-400" size={48} />
              <p className="text-slate-500">Próximamente más cursos disponibles</p>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-6">
            {courses.map((course) => (
              <Card key={course.id} className="overflow-hidden">
                <CardHeader 
                  className="cursor-pointer hover:bg-slate-50 transition-colors"
                  onClick={() => toggleCourse(course.id)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="w-16 h-16 bg-gradient-to-br from-cyan-400 to-cyan-600 rounded-xl flex items-center justify-center text-white text-2xl font-bold shadow-lg">
                        {course.title.charAt(0)}
                      </div>
                      <div>
                        <CardTitle className="text-2xl">{course.title}</CardTitle>
                        <CardDescription className="text-base">
                          {course.description}
                        </CardDescription>
                        <div className="flex gap-2 mt-2">
                          <Badge variant="outline">{course.level}</Badge>
                          <Badge variant="outline">{course.category}</Badge>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      <span className="text-slate-500 hidden sm:block">Ver contenido</span>
                      {expandedCourse === course.id ? 
                        <ChevronDown size={24} className="text-cyan-500" /> : 
                        <ChevronRight size={24} className="text-slate-400" />
                      }
                    </div>
                  </div>
                </CardHeader>

                {expandedCourse === course.id && (
                  <CardContent className="bg-slate-50 border-t">
                    {!chapters[course.id] ? (
                      <div className="text-center py-8">
                        <div className="animate-spin w-6 h-6 border-2 border-cyan-500 border-t-transparent rounded-full mx-auto" />
                      </div>
                    ) : chapters[course.id].length === 0 ? (
                      <p className="text-slate-500 text-center py-4">Sin contenido disponible</p>
                    ) : (
                      <div className="space-y-4">
                        {chapters[course.id].map((chapter, chIndex) => (
                          <div key={chapter.id} className="bg-white rounded-lg p-4 shadow-sm">
                            <div className="flex items-center gap-3 mb-3">
                              <span className="w-8 h-8 bg-cyan-100 text-cyan-700 rounded-full flex items-center justify-center font-bold text-sm">
                                {chIndex + 1}
                              </span>
                              <h4 className="font-semibold text-lg">{chapter.title}</h4>
                              <Badge variant="secondary" className="ml-auto">
                                {chapter.lessons?.length || 0} lecciones
                              </Badge>
                            </div>
                            
                            {chapter.lessons && chapter.lessons.length > 0 && (
                              <div className="ml-11 space-y-2">
                                {chapter.lessons.map((lesson, lIndex) => (
                                  <div 
                                    key={lesson.id}
                                    className="flex items-center gap-3 p-3 bg-slate-50 rounded-lg group"
                                  >
                                    <Lock size={16} className="text-slate-400" />
                                    <span className="text-slate-600 flex-1">
                                      {lIndex + 1}. {lesson.title}
                                    </span>
                                    <span className="text-xs text-slate-400">
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

// ==================== PRICING SECTION ====================
const PricingSection = () => {
  const navigate = useNavigate();

  const plans = [
    {
      id: "monthly",
      name: "Mensual",
      price: "9.990",
      period: "/mes",
      description: "Acceso completo por 1 mes",
      features: [
        "Acceso a todos los cursos",
        "Simulacros ilimitados",
        "Seguimiento de progreso",
        "Tutor IA Remy 24/7",
        "Soporte prioritario"
      ],
      cta: "Suscribirse",
      popular: false
    },
    {
      id: "semestral",
      name: "Semestral",
      price: "29.990",
      originalPrice: "59.940",
      period: "/6 meses",
      description: "Ahorra 50% con el plan semestral",
      features: [
        "Acceso a todos los cursos",
        "Simulacros ilimitados",
        "Seguimiento de progreso",
        "Tutor IA Remy 24/7",
        "Soporte prioritario",
        "Contenido exclusivo",
        "Acceso anticipado a nuevos cursos"
      ],
      cta: "Suscribirse y Ahorrar",
      popular: true,
      badge: "50% DCTO"
    }
  ];

  return (
    <section id="pricing" className="py-24 bg-gradient-to-b from-white to-slate-50">
      <div className="max-w-5xl mx-auto px-6">
        <div className="text-center mb-16">
          <Badge className="mb-4 bg-green-100 text-green-700 hover:bg-green-100">
            Precios
          </Badge>
          <h2 className="text-4xl md:text-5xl font-bold text-slate-900 mb-4">
            Invierte en tu <span className="text-cyan-500">futuro</span>
          </h2>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto">
            Elige el plan que mejor se adapte a tus necesidades. Sin compromisos, cancela cuando quieras.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {plans.map((plan, index) => (
            <Card 
              key={index}
              className={`relative overflow-hidden transition-all hover:shadow-2xl ${
                plan.popular 
                  ? 'border-2 border-cyan-500 shadow-xl scale-105' 
                  : 'border-slate-200 hover:border-cyan-200'
              }`}
            >
              {plan.badge && (
                <div className="absolute top-4 right-4">
                  <Badge className="bg-red-500 text-white hover:bg-red-500 text-sm px-3 py-1">
                    {plan.badge}
                  </Badge>
                </div>
              )}
              
              <CardHeader className={plan.popular ? 'bg-cyan-50' : ''}>
                <CardTitle className="text-2xl">{plan.name}</CardTitle>
                <CardDescription>{plan.description}</CardDescription>
                
                <div className="mt-4">
                  {plan.originalPrice && (
                    <span className="text-slate-400 line-through text-lg mr-2">
                      ${plan.originalPrice}
                    </span>
                  )}
                  <span className="text-5xl font-bold text-slate-900">
                    ${plan.price}
                  </span>
                  <span className="text-slate-500 text-lg">{plan.period}</span>
                </div>
              </CardHeader>
              
              <CardContent className="pt-6">
                <ul className="space-y-4 mb-8">
                  {plan.features.map((feature, fIndex) => (
                    <li key={fIndex} className="flex items-center gap-3">
                      <CheckCircle className="text-cyan-500 flex-shrink-0" size={20} />
                      <span className="text-slate-600">{feature}</span>
                    </li>
                  ))}
                </ul>
                
                <Button 
                  className={`w-full py-6 text-lg rounded-full ${
                    plan.popular 
                      ? 'bg-cyan-500 hover:bg-cyan-400 text-white shadow-lg shadow-cyan-500/30' 
                      : 'bg-slate-900 hover:bg-slate-800 text-white'
                  }`}
                  onClick={() => navigate(`/auth?redirect=/subscribe?plan=${plan.id}`)}
                  data-testid={`subscribe-btn-${plan.name.toLowerCase()}`}
                >
                  {plan.cta}
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Guarantee */}
        <div className="text-center mt-12 p-6 bg-slate-100 rounded-2xl max-w-2xl mx-auto">
          <Award className="mx-auto mb-3 text-cyan-500" size={32} />
          <h4 className="font-semibold text-lg mb-2">Garantía de satisfacción</h4>
          <p className="text-slate-600">
            Si no estás satisfecho en los primeros 7 días, te devolvemos el 100% de tu dinero. Sin preguntas.
          </p>
        </div>
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
          
          <div className="flex gap-8 text-slate-400">
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
  return (
    <div className="min-h-screen">
      <HeroSection />
      <FeaturesSection />
      <CoursesPreviewSection />
      <PricingSection />
      <Footer />
    </div>
  );
};

export default Landing;
