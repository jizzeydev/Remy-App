import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { motion, useReducedMotion, MotionConfig, AnimatePresence } from 'framer-motion';
import { useAuth } from '../contexts/AuthContext';
import { usePricing } from '../hooks/usePricing';
import {
  BookOpen, Target, Clock, CheckCircle,
  ChevronDown, GraduationCap,
  Lock, Zap, Award, FileText,
  Search, ClipboardList, Lightbulb, BarChart3,
  ArrowRight, X, Sparkles, ShieldCheck, Users,
  Menu
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  Accordion, AccordionContent, AccordionItem, AccordionTrigger
} from '@/components/ui/accordion';
import InlineMd from '@/components/course/InlineMd';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Shared motion presets — respect reduced-motion via MotionConfig wrapper
const fadeUp = {
  initial: { opacity: 0, y: 24 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true, margin: '-80px' },
  transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] }
};

const fadeIn = {
  initial: { opacity: 0 },
  whileInView: { opacity: 1 },
  viewport: { once: true, margin: '-80px' },
  transition: { duration: 0.6 }
};

const staggerChildren = {
  initial: {},
  whileInView: {},
  viewport: { once: true, margin: '-80px' },
  transition: { staggerChildren: 0.08 }
};

// ==================== STICKY NAV ====================
const StickyNav = ({ trialEnabled }) => {
  const navigate = useNavigate();
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 32);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  const links = [
    { href: '#features', label: 'Funcionalidades' },
    { href: '#courses', label: 'Cursos' },
    { href: '#pricing', label: 'Precios' },
    { href: '#faq', label: 'Preguntas' }
  ];

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? 'bg-slate-900/75 backdrop-blur-lg border-b border-white/10 py-3'
          : 'bg-transparent py-4 md:py-6'
      }`}
      aria-label="Navegación principal"
    >
      <div className="max-w-6xl mx-auto px-4 md:px-6 flex items-center justify-between">
        <a
          href="#top"
          className="flex items-center gap-2 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 rounded-md"
          aria-label="Remy — inicio"
        >
          <img src="/remy-logo.png" alt="" className="w-8 h-8 md:w-9 md:h-9 object-contain" />
          <span className="text-white font-bold text-lg md:text-xl tracking-tight">Remy</span>
        </a>

        <div className="hidden md:flex items-center gap-1">
          {links.map((l) => (
            <a
              key={l.href}
              href={l.href}
              className="text-slate-200 hover:text-white px-3 py-2 rounded-lg text-sm font-medium hover:bg-white/5 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400"
            >
              {l.label}
            </a>
          ))}
        </div>

        <div className="flex items-center gap-2 md:gap-3">
          <Button
            variant="ghost"
            className="text-white hover:bg-white/10 text-sm md:text-base px-3 md:px-4"
            onClick={() => navigate('/auth')}
            data-testid="nav-login-btn"
          >
            Ingresar
          </Button>
          <Button
            className="bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-semibold text-sm md:text-base px-3 md:px-4 shadow-lg shadow-cyan-500/20"
            onClick={() => navigate('/auth')}
            data-testid="nav-signup-btn"
          >
            <span className="hidden sm:inline">{trialEnabled ? 'Empieza gratis' : 'Suscríbete'}</span>
            <span className="sm:hidden">{trialEnabled ? 'Gratis' : 'Iniciar'}</span>
          </Button>
          <button
            type="button"
            className="md:hidden text-white p-2 -mr-2 rounded-lg hover:bg-white/10 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400"
            aria-label={mobileOpen ? 'Cerrar menú' : 'Abrir menú'}
            aria-expanded={mobileOpen}
            onClick={() => setMobileOpen((v) => !v)}
          >
            {mobileOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </div>

      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.18 }}
            className="md:hidden border-t border-white/10 bg-slate-900/95 backdrop-blur-lg"
          >
            <div className="px-4 py-3 flex flex-col">
              {links.map((l) => (
                <a
                  key={l.href}
                  href={l.href}
                  onClick={() => setMobileOpen(false)}
                  className="text-slate-100 hover:text-cyan-300 px-3 py-3 rounded-lg text-base font-medium hover:bg-white/5"
                >
                  {l.label}
                </a>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
};

// ==================== HERO PRODUCT MOCKUP ====================
// Stylized fake "simulator question" card to give visual context of the product
const HeroMockup = () => {
  return (
    <div className="relative mx-auto max-w-md md:max-w-lg" aria-hidden="true">
      {/* Glow */}
      <div className="absolute -inset-4 bg-gradient-to-tr from-cyan-500/30 via-blue-500/20 to-transparent blur-2xl rounded-3xl" />

      <div className="relative rounded-2xl border border-white/15 bg-slate-900/60 backdrop-blur-md shadow-2xl overflow-hidden">
        {/* Top bar */}
        <div className="flex items-center gap-2 px-4 py-3 border-b border-white/10 bg-white/5">
          <span className="w-2.5 h-2.5 rounded-full bg-red-400/70" />
          <span className="w-2.5 h-2.5 rounded-full bg-amber-400/70" />
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-400/70" />
          <span className="ml-3 text-xs text-slate-400 font-mono">Simulacro · Cálculo I</span>
          <span className="ml-auto text-xs text-cyan-300 font-medium tabular-nums">04 / 10</span>
        </div>

        {/* Content */}
        <div className="p-5 md:p-6 space-y-4">
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded-full bg-cyan-500/15 text-cyan-300 text-[11px] font-semibold tracking-wide">
              DERIVADAS
            </span>
            <span className="px-2 py-0.5 rounded-full bg-white/10 text-slate-300 text-[11px] font-semibold tracking-wide">
              MEDIO
            </span>
          </div>

          <p className="text-slate-100 text-sm md:text-base leading-relaxed">
            Calcula la derivada de <span className="font-mono text-cyan-300">f(x) = x³ · ln(x)</span> y evalúa en x = e.
          </p>

          <div className="space-y-2">
            {[
              { letter: 'A', text: '3e²·(ln e + 1/3)', state: 'idle' },
              { letter: 'B', text: 'e²·(3 ln e + 1)', state: 'correct' },
              { letter: 'C', text: 'e²·(ln e + 3)', state: 'idle' },
              { letter: 'D', text: '3e³', state: 'idle' }
            ].map((opt) => (
              <div
                key={opt.letter}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-lg border text-sm transition-colors ${
                  opt.state === 'correct'
                    ? 'border-emerald-400/40 bg-emerald-400/10 text-emerald-100'
                    : 'border-white/10 bg-white/5 text-slate-200'
                }`}
              >
                <span
                  className={`w-6 h-6 rounded-md flex items-center justify-center text-xs font-bold ${
                    opt.state === 'correct'
                      ? 'bg-emerald-400 text-slate-900'
                      : 'bg-white/10 text-slate-300'
                  }`}
                >
                  {opt.letter}
                </span>
                <span className="font-mono">{opt.text}</span>
                {opt.state === 'correct' && (
                  <CheckCircle size={16} className="ml-auto text-emerald-300" />
                )}
              </div>
            ))}
          </div>

          <div className="flex items-center gap-2 pt-1">
            <div className="flex-1 h-1.5 bg-white/10 rounded-full overflow-hidden">
              <div className="h-full w-2/5 bg-gradient-to-r from-cyan-400 to-blue-400" />
            </div>
            <span className="text-xs text-slate-400 tabular-nums">4 / 10</span>
          </div>
        </div>
      </div>
    </div>
  );
};

// ==================== HERO SECTION ====================
const HeroSection = ({ trialEnabled = true, trialDays = 7 }) => {
  const navigate = useNavigate();

  return (
    <section
      id="top"
      className="relative pt-28 md:pt-32 pb-16 md:pb-24 min-h-screen flex items-center"
    >
      {/* Hero accent glows — intentionally NOT inside an overflow-hidden container,
          so they bleed into the section below for a smooth dark→dark transition. */}
      <div className="absolute inset-0 pointer-events-none" aria-hidden="true">
        <div className="absolute -top-40 -right-40 w-[500px] h-[500px] bg-cyan-500/15 rounded-full blur-[120px]" />
        <div className="absolute -bottom-60 -left-40 w-[500px] h-[500px] bg-blue-500/12 rounded-full blur-[120px]" />
        <div className="absolute -bottom-40 right-1/4 w-[400px] h-[300px] bg-cyan-400/8 rounded-full blur-[100px]" />
      </div>

      <div className="relative z-10 max-w-6xl mx-auto px-6 w-full">
        <div className="grid lg:grid-cols-12 gap-10 lg:gap-12 items-center">
          {/* Copy column */}
          <motion.div
            className="lg:col-span-7 text-center lg:text-left"
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          >
            {trialEnabled && (
              <div className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm border border-white/15 rounded-full px-3 py-1.5 mb-6">
                <Sparkles size={14} className="text-cyan-300" />
                <span className="text-white/90 text-xs md:text-sm">
                  {trialDays} días gratis · Sin tarjeta de crédito
                </span>
              </div>
            )}

            <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-6xl font-bold text-white mb-5 leading-[1.05] tracking-tight">
              <span className="text-cyan-400">Remonta</span> tus ramos
              <br className="hidden sm:block" />
              <span className="block mt-2 text-2xl sm:text-3xl md:text-4xl lg:text-4xl font-medium text-slate-300">
                la mejor plataforma de estudio para la universidad
              </span>
            </h1>

            <p className="text-base md:text-lg text-slate-300 max-w-2xl mx-auto lg:mx-0 mb-8 leading-relaxed">
              Lecciones claras, simulacros instantáneos y preguntas tipo prueba adaptadas a tu universidad.
              Todo en un solo lugar.
            </p>

            <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center lg:justify-start items-center mb-6">
              <Button
                size="lg"
                className="bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-bold text-base md:text-lg px-7 py-6 rounded-full shadow-lg shadow-cyan-500/30 transition-all w-full sm:w-auto"
                onClick={() => navigate('/auth')}
                data-testid="hero-cta-primary"
              >
                <Zap className="mr-2" size={20} />
                {trialEnabled ? 'Empieza gratis' : 'Suscríbete ahora'}
              </Button>
              <Button
                size="lg"
                variant="outline"
                className="bg-white/5 text-white border-white/20 hover:bg-white/10 hover:text-white text-base md:text-lg px-7 py-6 rounded-full w-full sm:w-auto"
                onClick={() => document.getElementById('courses').scrollIntoView({ behavior: 'smooth' })}
                data-testid="hero-cta-secondary"
              >
                Ver cursos
              </Button>
            </div>

            <div className="flex flex-wrap items-center justify-center lg:justify-start gap-x-5 gap-y-2 text-xs md:text-sm text-slate-400">
              <span className="inline-flex items-center gap-1.5">
                <CheckCircle size={14} className="text-cyan-400" /> Cancela cuando quieras
              </span>
              <span className="inline-flex items-center gap-1.5">
                <CheckCircle size={14} className="text-cyan-400" /> Sin compromisos
              </span>
              <span className="inline-flex items-center gap-1.5">
                <CheckCircle size={14} className="text-cyan-400" /> Soporte en español
              </span>
            </div>
          </motion.div>

          {/* Mockup column */}
          <motion.div
            className="lg:col-span-5"
            initial={{ opacity: 0, y: 32, rotate: -2 }}
            animate={{ opacity: 1, y: 0, rotate: -1.5 }}
            transition={{ duration: 0.7, delay: 0.15, ease: [0.22, 1, 0.36, 1] }}
          >
            <HeroMockup />
          </motion.div>
        </div>
      </div>
    </section>
  );
};

// ==================== SOCIAL PROOF SECTION ====================
const SocialProofSection = () => {
  const [universities, setUniversities] = useState([]);

  useEffect(() => {
    axios
      .get(`${API}/library-universities`)
      .then((r) => setUniversities(r.data || []))
      .catch(() => {});
  }, []);

  const trustItems = [
    { icon: <ShieldCheck size={18} />, label: 'Contenido alineado con sílabos chilenos' },
    { icon: <Target size={18} />, label: 'Simulacros tipo prueba real' },
    { icon: <Users size={18} />, label: 'Diseñado por estudiantes para estudiantes' }
  ];

  return (
    <section className="py-12 md:py-16 relative">
      <div className="max-w-6xl mx-auto px-6">
        <motion.p
          {...fadeIn}
          className="text-center text-sm uppercase tracking-wider text-slate-400 mb-6"
        >
          Cubrimos cursos de matemática para
        </motion.p>

        {universities.length > 0 ? (
          <motion.div
            {...fadeUp}
            className="flex flex-wrap items-center justify-center gap-2 md:gap-3 mb-10"
          >
            {universities.slice(0, 12).map((uni) => (
              <span
                key={uni.id}
                className="px-3 py-1.5 rounded-full border border-white/10 bg-white/5 text-slate-200 text-sm font-semibold"
                title={uni.name}
              >
                {uni.short_name}
              </span>
            ))}
            <span className="px-3 py-1.5 rounded-full bg-cyan-500/15 border border-cyan-400/30 text-cyan-200 text-sm font-semibold">
              y más
            </span>
          </motion.div>
        ) : (
          <div className="h-10 mb-10" />
        )}

        <motion.div
          {...staggerChildren}
          className="grid grid-cols-1 sm:grid-cols-3 gap-3 md:gap-4 max-w-4xl mx-auto"
        >
          {trustItems.map((item, i) => (
            <motion.div
              key={i}
              variants={fadeUp}
              className="flex items-center gap-3 px-4 py-3 rounded-xl bg-white/5 border border-white/10"
            >
              <span className="text-cyan-300 flex-shrink-0">{item.icon}</span>
              <span className="text-sm md:text-[15px] text-slate-200 font-medium">{item.label}</span>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
};

// ==================== PROBLEM SECTION ====================
const ProblemSection = () => {
  const beforeItems = [
    { icon: <Search size={20} />, text: 'Buscar PDFs en internet' },
    { icon: <FileText size={20} />, text: 'Resolver ejercicios sueltos' },
    { icon: <ClipboardList size={20} />, text: 'Intentar encontrar pruebas antiguas' }
  ];

  const afterItems = [
    { icon: <BookOpen size={20} />, text: 'Lecciones claras e interactivas' },
    { icon: <Target size={20} />, text: 'Simulacros instantáneos' },
    { icon: <GraduationCap size={20} />, text: 'Práctica tipo examen' }
  ];

  return (
    <section className="py-20 md:py-28 relative">
      <div className="max-w-6xl mx-auto px-6">
        <motion.div {...fadeUp} className="text-center mb-12 md:mb-16">
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-6 leading-tight tracking-tight">
            Estudiar matemáticas en la universidad
            <br />
            <span className="text-cyan-400">no debería ser tan caótico</span>
          </h2>
          <p className="text-lg md:text-xl text-slate-300 max-w-3xl mx-auto leading-relaxed">
            Muchos estudiantes pierden tiempo con PDFs desordenados, ejercicios sueltos y pruebas antiguas
            difíciles de encontrar. Eso hace que estudiar tome demasiado tiempo y practicar para los
            exámenes sea poco eficiente.
          </p>
        </motion.div>

        <motion.div
          {...fadeUp}
          className="bg-cyan-500/10 border border-cyan-400/30 rounded-2xl p-6 md:p-8 mb-12 md:mb-16 text-center max-w-4xl mx-auto"
        >
          <Lightbulb className="mx-auto mb-4 text-cyan-300" size={36} aria-hidden="true" />
          <p className="text-lg md:text-xl text-slate-100 font-medium">
            <span className="text-cyan-300 font-bold">Remy</span> organiza el contenido, simplifica el
            estudio y te permite aprender y practicar en un solo lugar.
          </p>
        </motion.div>

        <motion.div
          {...staggerChildren}
          className="grid md:grid-cols-2 gap-6 md:gap-8 max-w-4xl mx-auto"
        >
          <motion.div variants={fadeUp}>
            <Card className="border border-white/10 bg-white/5 h-full">
              <CardHeader className="pb-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center">
                    <X className="text-slate-300" size={20} aria-hidden="true" />
                  </div>
                  <CardTitle className="text-xl text-slate-300">ANTES</CardTitle>
                </div>
              </CardHeader>
              <CardContent className="pt-0">
                <ul className="space-y-4">
                  {beforeItems.map((item, index) => (
                    <li key={index} className="flex items-center gap-3 text-slate-400">
                      <span className="text-slate-500" aria-hidden="true">{item.icon}</span>
                      <span>{item.text}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div variants={fadeUp}>
            <Card className="border border-cyan-400/40 bg-gradient-to-br from-cyan-500/15 to-cyan-500/5 shadow-2xl shadow-cyan-500/10 h-full">
              <CardHeader className="pb-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-cyan-500 rounded-full flex items-center justify-center">
                    <CheckCircle className="text-slate-900" size={20} aria-hidden="true" />
                  </div>
                  <CardTitle className="text-xl text-cyan-200">CON REMY</CardTitle>
                </div>
              </CardHeader>
              <CardContent className="pt-0">
                <ul className="space-y-4">
                  {afterItems.map((item, index) => (
                    <li key={index} className="flex items-center gap-3 text-slate-100 font-medium">
                      <span className="text-cyan-300" aria-hidden="true">{item.icon}</span>
                      <span>{item.text}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
};

// ==================== FEATURES SECTION ====================
const FeaturesSection = () => {
  const features = [
    {
      icon: <Target size={28} />,
      title: 'Simulacros de Prueba',
      description:
        'Genera simulacros de 5 a 15 preguntas a partir de una gran base de ejercicios inspirados en pruebas reales de tu ramo.',
      tone: 'cyan'
    },
    {
      icon: <BookOpen size={28} />,
      title: 'Lecciones de Calidad',
      description:
        'Lecciones claras con fórmulas, imágenes y gráficos interactivos diseñados para entender rápido los contenidos.',
      tone: 'blue'
    },
    {
      icon: <GraduationCap size={28} />,
      title: 'Práctica tipo Examen',
      description:
        'Entrena con simulacros diseñados para parecerse a evaluaciones reales de distintas universidades.',
      tone: 'violet'
    },
    {
      icon: <BarChart3 size={28} />,
      title: 'Progreso y Correcciones Inteligentes',
      description:
        'Después de cada simulacro obtienes tu nota, ves exactamente en qué te equivocaste, accedes a las soluciones paso a paso y recibes recomendaciones sobre qué repasar.',
      tone: 'emerald'
    }
  ];

  const toneMap = {
    cyan: 'from-cyan-500/20 to-cyan-500/5 text-cyan-300 ring-cyan-400/30',
    blue: 'from-blue-500/20 to-blue-500/5 text-blue-300 ring-blue-400/30',
    violet: 'from-violet-500/20 to-violet-500/5 text-violet-300 ring-violet-400/30',
    emerald: 'from-emerald-500/20 to-emerald-500/5 text-emerald-300 ring-emerald-400/30'
  };

  return (
    <section id="features" className="py-20 md:py-28 relative">
      <div className="max-w-6xl mx-auto px-6">
        <motion.div {...fadeUp} className="text-center mb-12 md:mb-16">
          <Badge className="mb-4 bg-cyan-500/15 text-cyan-200 hover:bg-cyan-500/15 border border-cyan-400/30">
            Funcionalidades
          </Badge>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-4 tracking-tight">
            Todo lo que necesitas para <span className="text-cyan-400">aprobar</span>
          </h2>
          <p className="text-lg md:text-xl text-slate-300 max-w-2xl mx-auto">
            Herramientas diseñadas para que estudies de forma más inteligente
          </p>
        </motion.div>

        <motion.div
          {...staggerChildren}
          className="grid md:grid-cols-2 gap-5 md:gap-6"
        >
          {features.map((feature, index) => (
            <motion.div key={index} variants={fadeUp}>
              <Card
                className="border border-white/10 hover:border-cyan-400/40 hover:shadow-2xl hover:shadow-cyan-500/10 hover:-translate-y-0.5 transition-all duration-200 group bg-white/5 backdrop-blur-sm h-full"
                data-testid={`feature-card-${index}`}
              >
                <CardHeader>
                  <div
                    className={`w-14 h-14 rounded-xl bg-gradient-to-br ${toneMap[feature.tone]} ring-1 flex items-center justify-center mb-3`}
                    aria-hidden="true"
                  >
                    {feature.icon}
                  </div>
                  <CardTitle className="text-xl md:text-2xl text-white">{feature.title}</CardTitle>
                  <CardDescription className="text-base md:text-[17px] leading-relaxed text-slate-300">
                    {feature.description}
                  </CardDescription>
                </CardHeader>
              </Card>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
};

// ==================== COURSES SECTION ====================
const CoursesSection = () => {
  const [courses, setCourses] = useState([]);
  const [filteredCourses, setFilteredCourses] = useState([]);
  const [universities, setUniversities] = useState([]);
  const [expandedCourse, setExpandedCourse] = useState(null);
  const [chapters, setChapters] = useState({});
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterUniversity, setFilterUniversity] = useState('general');
  const navigate = useNavigate();

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    let filtered = [...courses];
    if (searchTerm) {
      filtered = filtered.filter(
        (c) =>
          c.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
          c.description?.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    if (filterUniversity === 'general') {
      filtered = filtered.filter((c) => !c.university_id);
    } else if (filterUniversity !== 'all') {
      filtered = filtered.filter((c) => c.university_id === filterUniversity);
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
      setChapters((prev) => ({ ...prev, [courseId]: chaptersWithLessons }));
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
    <section id="courses" className="py-20 md:py-28 relative">
      <div className="max-w-6xl mx-auto px-6">
        <motion.div {...fadeUp} className="text-center mb-12 md:mb-16">
          <Badge className="mb-4 bg-blue-500/15 text-blue-200 hover:bg-blue-500/15 border border-blue-400/30">
            Contenido
          </Badge>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-4 tracking-tight">
            Cursos <span className="text-cyan-400">disponibles</span>
          </h2>
          <p className="text-lg md:text-xl text-slate-300 max-w-3xl mx-auto mb-3">
            Nuestros cursos cubren los contenidos fundamentales de matemáticas universitarias.
          </p>
          <p className="text-base text-slate-400 max-w-2xl mx-auto">
            Las lecciones sirven para cualquier universidad. Los simulacros se adaptan al tipo de
            evaluación de cada una.
          </p>
        </motion.div>

        <motion.div
          {...fadeUp}
          className="flex flex-col sm:flex-row gap-3 sm:gap-4 items-stretch sm:items-center justify-center mb-8"
        >
          <div className="relative w-full sm:w-72">
            <Search
              className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
              size={18}
              aria-hidden="true"
            />
            <label htmlFor="course-search" className="sr-only">
              Buscar cursos
            </label>
            <input
              id="course-search"
              type="text"
              placeholder="Buscar cursos..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 border border-white/10 bg-white/5 rounded-lg text-slate-100 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent"
            />
          </div>
          <label htmlFor="university-filter" className="sr-only">
            Filtrar por universidad
          </label>
          <select
            id="university-filter"
            value={filterUniversity}
            onChange={(e) => setFilterUniversity(e.target.value)}
            className="w-full sm:w-56 px-4 py-2.5 border border-white/10 bg-white/5 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent"
          >
            <option value="general" className="bg-slate-900 text-slate-100">General</option>
            <option value="all" className="bg-slate-900 text-slate-100">Todas las universidades</option>
            {universities.map((uni) => (
              <option key={uni.id} value={uni.id} className="bg-slate-900 text-slate-100">
                {uni.short_name} - {uni.name}
              </option>
            ))}
          </select>
          <span className="text-sm text-slate-400 text-center sm:text-left">
            {filteredCourses.length} curso(s)
          </span>
        </motion.div>

        {loading ? (
          <div className="text-center py-12" role="status" aria-live="polite">
            <div className="animate-spin w-8 h-8 border-4 border-cyan-400 border-t-transparent rounded-full mx-auto" />
            <span className="sr-only">Cargando cursos</span>
          </div>
        ) : filteredCourses.length === 0 ? (
          <Card className="text-center py-12 bg-white/5 border-white/10">
            <CardContent>
              <GraduationCap className="mx-auto mb-4 text-slate-500" size={48} aria-hidden="true" />
              <p className="text-slate-400">
                {courses.length === 0
                  ? 'Próximamente más cursos disponibles'
                  : 'No se encontraron cursos con esos filtros'}
              </p>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-4">
            {filteredCourses.map((course) => {
              const isExpanded = expandedCourse === course.id;
              const panelId = `course-panel-${course.id}`;
              const buttonId = `course-button-${course.id}`;
              return (
                <Card
                  key={course.id}
                  className="overflow-hidden bg-white/5 border-white/10 hover:border-cyan-400/30 transition-colors"
                  data-testid={`course-card-${course.id}`}
                >
                  <CardHeader className="p-0">
                    <button
                      id={buttonId}
                      type="button"
                      onClick={() => toggleCourse(course.id)}
                      aria-expanded={isExpanded}
                      aria-controls={panelId}
                      className="w-full text-left p-5 md:p-6 hover:bg-white/5 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-inset"
                    >
                      <div className="flex items-center justify-between gap-3">
                        <div className="flex items-center gap-4 min-w-0">
                          <div
                            className="w-14 h-14 md:w-16 md:h-16 bg-gradient-to-br from-cyan-400 to-cyan-600 rounded-xl flex items-center justify-center text-slate-900 text-xl md:text-2xl font-bold shadow-lg shadow-cyan-500/20 flex-shrink-0"
                            aria-hidden="true"
                          >
                            {course.title.charAt(0)}
                          </div>
                          <div className="min-w-0">
                            <CardTitle className="text-lg md:text-xl text-white">
                              {course.title}
                            </CardTitle>
                            <CardDescription className="text-sm md:text-base text-slate-400 line-clamp-2 mt-0.5">
                              <InlineMd>{course.description}</InlineMd>
                            </CardDescription>
                            <div className="flex gap-2 mt-2 flex-wrap">
                              <Badge
                                variant="outline"
                                className="border-white/15 text-slate-300 bg-white/5 text-xs"
                              >
                                {course.level}
                              </Badge>
                              <Badge
                                variant="outline"
                                className="border-white/15 text-slate-300 bg-white/5 text-xs"
                              >
                                {course.category}
                              </Badge>
                              {course.university ? (
                                <Badge className="bg-blue-500/15 text-blue-200 hover:bg-blue-500/15 border border-blue-400/30 text-xs">
                                  {course.university.short_name === 'GEN'
                                    ? 'General'
                                    : course.university.short_name}
                                </Badge>
                              ) : (
                                <Badge className="bg-blue-500/15 text-blue-200 hover:bg-blue-500/15 border border-blue-400/30 text-xs">
                                  General
                                </Badge>
                              )}
                            </div>
                          </div>
                        </div>
                        <div className="flex items-center gap-2 flex-shrink-0">
                          <span className="text-slate-400 hidden sm:block text-sm">
                            {isExpanded ? 'Ocultar' : 'Ver contenido'}
                          </span>
                          <motion.span
                            animate={{ rotate: isExpanded ? 180 : 0 }}
                            transition={{ duration: 0.2 }}
                            className="inline-flex"
                          >
                            <ChevronDown
                              size={22}
                              className={isExpanded ? 'text-cyan-300' : 'text-slate-500'}
                            />
                          </motion.span>
                        </div>
                      </div>
                    </button>
                  </CardHeader>

                  <AnimatePresence initial={false}>
                    {isExpanded && (
                      <motion.div
                        id={panelId}
                        role="region"
                        aria-labelledby={buttonId}
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.25, ease: 'easeOut' }}
                        className="overflow-hidden"
                      >
                        <CardContent className="bg-black/20 border-t border-white/10 p-5 md:p-6">
                          {!chapters[course.id] ? (
                            <div className="text-center py-8" role="status" aria-live="polite">
                              <div className="animate-spin w-6 h-6 border-2 border-cyan-400 border-t-transparent rounded-full mx-auto" />
                              <span className="sr-only">Cargando contenido</span>
                            </div>
                          ) : chapters[course.id].length === 0 ? (
                            <p className="text-slate-400 text-center py-4">Sin contenido disponible</p>
                          ) : (
                            <div className="space-y-4">
                              {chapters[course.id].map((chapter, chIndex) => (
                                <div
                                  key={chapter.id}
                                  className="bg-white/5 rounded-lg p-4 border border-white/10"
                                >
                                  <div className="flex items-center gap-3 mb-3">
                                    <span
                                      className="w-8 h-8 bg-cyan-500/20 text-cyan-300 rounded-full flex items-center justify-center font-bold text-sm flex-shrink-0"
                                      aria-hidden="true"
                                    >
                                      {chIndex + 1}
                                    </span>
                                    <h4 className="font-semibold text-base md:text-lg text-white">
                                      {chapter.title}
                                    </h4>
                                    <Badge
                                      variant="secondary"
                                      className="ml-auto bg-white/10 text-slate-200 hover:bg-white/10 border-0"
                                    >
                                      {chapter.lessons?.length || 0} lecciones
                                    </Badge>
                                  </div>

                                  {chapter.lessons && chapter.lessons.length > 0 && (
                                    <ul className="ml-11 space-y-2">
                                      {chapter.lessons.map((lesson, lIndex) => (
                                        <li
                                          key={lesson.id}
                                          className="flex items-center gap-3 p-3 bg-black/20 rounded-lg border border-white/5"
                                        >
                                          <Lock size={16} className="text-slate-500" aria-hidden="true" />
                                          <span className="text-slate-200 flex-1 text-sm md:text-base">
                                            {lIndex + 1}. {lesson.title}
                                          </span>
                                          <span className="text-xs text-slate-400 tabular-nums">
                                            {lesson.duration_minutes} min
                                          </span>
                                        </li>
                                      ))}
                                    </ul>
                                  )}
                                </div>
                              ))}

                              <div className="text-center pt-2">
                                <Button
                                  className="bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-semibold rounded-full"
                                  onClick={() =>
                                    document
                                      .getElementById('pricing')
                                      .scrollIntoView({ behavior: 'smooth' })
                                  }
                                  data-testid="course-subscribe-btn"
                                >
                                  <Lock className="mr-2" size={18} />
                                  Suscríbete para acceder
                                </Button>
                              </div>
                            </div>
                          )}
                        </CardContent>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </Card>
              );
            })}
          </div>
        )}
      </div>
    </section>
  );
};

// ==================== SIMULATION SECTION ====================
const SimulationSection = () => {
  const benefits = [
    { text: 'Práctica rápida', icon: <Clock size={20} /> },
    { text: 'Preguntas variadas', icon: <Target size={20} /> },
    { text: 'Entrenamiento tipo examen', icon: <GraduationCap size={20} /> }
  ];

  return (
    <section className="py-20 md:py-28 text-white relative">
      <div className="absolute inset-0 pointer-events-none" aria-hidden="true">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[900px] h-[500px] bg-cyan-500/12 rounded-full blur-[140px]" />
        <div className="absolute -top-40 right-0 w-[400px] h-[400px] bg-cyan-500/8 rounded-full blur-[120px]" />
        <div className="absolute -bottom-40 left-0 w-[400px] h-[400px] bg-blue-500/8 rounded-full blur-[120px]" />
      </div>

      <div className="max-w-6xl mx-auto px-6 relative z-10">
        <motion.div {...fadeUp} className="text-center mb-12">
          <Badge className="mb-4 bg-cyan-500/15 text-cyan-200 hover:bg-cyan-500/15 border border-cyan-500/30">
            Simulacros
          </Badge>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-6 tracking-tight">
            Practica como si estuvieras en un <span className="text-cyan-400">examen real</span>
          </h2>
          <p className="text-lg md:text-xl text-slate-300 max-w-3xl mx-auto mb-10">
            Con Remy puedes generar simulacros en segundos y entrenar como si estuvieras rindiendo
            una prueba.
          </p>
        </motion.div>

        <motion.div
          {...staggerChildren}
          className="flex flex-col sm:flex-row justify-center items-center gap-6 md:gap-12 mb-10"
        >
          {benefits.map((benefit, index) => (
            <motion.div key={index} variants={fadeUp} className="flex items-center gap-3">
              <div
                className="w-10 h-10 bg-cyan-500/15 ring-1 ring-cyan-400/30 rounded-full flex items-center justify-center text-cyan-300"
                aria-hidden="true"
              >
                {benefit.icon}
              </div>
              <span className="text-lg font-medium">{benefit.text}</span>
            </motion.div>
          ))}
        </motion.div>

        <motion.div {...fadeIn} className="text-center">
          <p className="text-base md:text-lg text-cyan-200/90 font-medium italic">
            "Una de las formas más efectivas de prepararte para tus evaluaciones."
          </p>
        </motion.div>
      </div>
    </section>
  );
};

// ==================== PRICING SECTION ====================
const PricingSection = ({ trialEnabled = true, trialDays = 7 }) => {
  const navigate = useNavigate();
  const { monthly, semestral, formatPrice, loading } = usePricing();

  if (loading) {
    return (
      <section id="pricing" className="py-20 md:py-28 relative">
        <div className="max-w-5xl mx-auto px-6 text-center">
          <div className="animate-spin w-8 h-8 border-4 border-cyan-400 border-t-transparent rounded-full mx-auto" />
        </div>
      </section>
    );
  }

  const pricingPlans = [monthly, semestral].filter(Boolean);

  return (
    <section id="pricing" className="py-20 md:py-28 relative">
      <div className="max-w-5xl mx-auto px-6">
        <motion.div {...fadeUp} className="text-center mb-12 md:mb-16">
          <Badge className="mb-4 bg-emerald-500/15 text-emerald-200 hover:bg-emerald-500/15 border border-emerald-400/30">
            Precios
          </Badge>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-4 tracking-tight">
            Invierte en tu <span className="text-cyan-400">futuro</span>
          </h2>
          <p className="text-lg md:text-xl text-slate-300 max-w-2xl mx-auto">
            Elige el plan que mejor se adapte. Sin compromisos, cancela cuando quieras.
          </p>
          {trialEnabled && (
            <div className="inline-flex items-center gap-2 mt-5 bg-white/5 border border-cyan-400/30 rounded-full px-4 py-1.5">
              <Sparkles size={14} className="text-cyan-300" />
              <span className="text-sm text-slate-200">
                Antes de pagar, prueba <span className="font-semibold text-white">{trialDays} días gratis</span>
              </span>
            </div>
          )}
        </motion.div>

        <motion.div
          {...staggerChildren}
          className="grid md:grid-cols-2 gap-6 md:gap-8 max-w-4xl mx-auto"
        >
          {pricingPlans.map((plan) => {
            const isPopular = plan.is_popular;
            const hasDiscount = plan.discount_active && plan.discount_percentage > 0;

            return (
              <motion.div key={plan.id} variants={fadeUp}>
                <Card
                  className={`relative overflow-hidden transition-all hover:shadow-2xl h-full flex flex-col backdrop-blur-sm ${
                    isPopular
                      ? 'border-2 border-cyan-400/60 bg-gradient-to-br from-cyan-500/10 to-white/5 shadow-2xl shadow-cyan-500/20 md:scale-[1.02]'
                      : 'border border-white/10 bg-white/5 hover:border-cyan-400/30'
                  }`}
                  data-testid={`pricing-card-${plan.id}`}
                >
                  {isPopular && (
                    <div className="absolute top-0 left-0 right-0 bg-cyan-500 text-slate-900 text-center py-1.5 text-xs font-bold tracking-wide">
                      MÁS POPULAR
                    </div>
                  )}

                  {hasDiscount && (
                    <div className="absolute top-3 right-3 z-10">
                      <Badge className="bg-red-500 text-white hover:bg-red-500 border-0 text-xs px-2.5 py-1">
                        {plan.discount_percentage}% DCTO
                      </Badge>
                    </div>
                  )}

                  <CardHeader className={isPopular ? 'pt-10' : ''}>
                    <CardTitle className="text-xl md:text-2xl text-white">{plan.name}</CardTitle>
                    <CardDescription className="text-base text-slate-300">
                      {plan.description}
                    </CardDescription>

                    <div className="mt-4 flex items-baseline gap-2 flex-wrap">
                      {hasDiscount && plan.original_amount && (
                        <span className="text-slate-400 line-through text-base font-medium">
                          {formatPrice(plan.original_amount)}
                        </span>
                      )}
                      <span className="text-4xl md:text-5xl font-bold text-white tracking-tight">
                        {formatPrice(plan.amount)}
                      </span>
                      <span className="text-slate-300 text-base">/{plan.period}</span>
                    </div>
                  </CardHeader>

                  <CardContent className="pt-6 flex-1 flex flex-col">
                    <ul className="space-y-3 md:space-y-4 mb-8 flex-1">
                      {plan.features.map((feature, fIndex) => (
                        <li key={fIndex} className="flex items-start gap-3">
                          <CheckCircle
                            className="text-cyan-300 flex-shrink-0 mt-0.5"
                            size={20}
                            aria-hidden="true"
                          />
                          <span className="text-slate-200 text-sm md:text-base">{feature}</span>
                        </li>
                      ))}
                    </ul>

                    <Button
                      className={`w-full py-5 md:py-6 text-base md:text-lg rounded-full ${
                        isPopular
                          ? 'bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-bold shadow-lg shadow-cyan-500/30'
                          : 'bg-white/10 hover:bg-white/15 text-white border border-white/15'
                      }`}
                      onClick={() => navigate(`/auth?redirect=/subscribe?plan=${plan.id}`)}
                      data-testid={`subscribe-btn-${plan.id}`}
                    >
                      {trialEnabled
                        ? 'Empieza gratis'
                        : isPopular
                        ? 'Suscribirse y Ahorrar'
                        : 'Suscribirse'}
                    </Button>
                  </CardContent>
                </Card>
              </motion.div>
            );
          })}
        </motion.div>

        <motion.div
          {...fadeUp}
          className="text-center mt-10 md:mt-12 p-6 bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 max-w-2xl mx-auto"
        >
          <Award className="mx-auto mb-3 text-cyan-300" size={32} aria-hidden="true" />
          <h3 className="font-semibold text-lg mb-2 text-white">Garantía de satisfacción</h3>
          <p className="text-slate-300">
            Si no estás satisfecho en los primeros 7 días, te devolvemos el 100% de tu dinero. Sin
            preguntas.
          </p>
        </motion.div>
      </div>
    </section>
  );
};

// ==================== FAQ SECTION ====================
const FAQSection = ({ trialEnabled = true, trialDays = 7 }) => {
  const faqs = [
    {
      q: '¿Cómo funciona la prueba gratuita?',
      a: trialEnabled
        ? `Creas tu cuenta en menos de un minuto y obtienes ${trialDays} días de acceso completo. No te pedimos tarjeta de crédito. Si no quieres seguir, simplemente no suscribes y la cuenta queda en pausa.`
        : 'Puedes suscribirte directamente al plan mensual o semestral y cancelar cuando quieras desde tu cuenta.'
    },
    {
      q: '¿Para qué universidades sirve Remy?',
      a: 'Las lecciones cubren los contenidos fundamentales de matemáticas universitarias y sirven para cualquier universidad. Los simulacros se pueden adaptar al estilo de evaluación de distintas universidades chilenas.'
    },
    {
      q: '¿Qué cursos hay disponibles?',
      a: 'Cubrimos los ramos de matemáticas más demandados en primer y segundo año (Cálculo, Álgebra Lineal y similares). Puedes ver el detalle exacto en la sección "Cursos disponibles" más arriba.'
    },
    {
      q: '¿Puedo cancelar cuando quiera?',
      a: 'Sí. Cancelas desde tu cuenta en un par de clics y mantienes acceso hasta el final del período que ya pagaste. No hay letra chica.'
    },
    {
      q: '¿Los simulacros son tipo prueba real?',
      a: 'Sí. Cada simulacro se arma con preguntas inspiradas en pruebas reales del ramo, con dificultad y formato similares a lo que vas a encontrar en tu universidad.'
    },
    {
      q: '¿En qué se diferencia de buscar PDFs gratis?',
      a: 'Remy tiene todo organizado y conectado: las lecciones, los ejercicios, las soluciones paso a paso y el seguimiento de tu progreso. No pierdes tiempo buscando ni adivinando qué practicar.'
    }
  ];

  return (
    <section id="faq" className="py-20 md:py-28 relative">
      <div className="max-w-3xl mx-auto px-6">
        <motion.div {...fadeUp} className="text-center mb-10 md:mb-14">
          <Badge className="mb-4 bg-white/10 text-slate-200 hover:bg-white/10 border border-white/10">
            Preguntas frecuentes
          </Badge>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-white tracking-tight">
            Antes de empezar, <span className="text-cyan-400">resolvamos dudas</span>
          </h2>
        </motion.div>

        <motion.div {...fadeUp}>
          <Accordion type="single" collapsible className="w-full space-y-3">
            {faqs.map((faq, i) => (
              <AccordionItem
                key={i}
                value={`faq-${i}`}
                className="border border-white/10 rounded-xl bg-white/5 px-5 data-[state=open]:border-cyan-400/40 data-[state=open]:bg-white/[0.07] transition-colors"
              >
                <AccordionTrigger className="text-left text-base md:text-lg font-semibold text-white hover:no-underline py-4 [&>svg]:text-slate-400">
                  {faq.q}
                </AccordionTrigger>
                <AccordionContent className="text-slate-300 text-sm md:text-base leading-relaxed pb-4">
                  {faq.a}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </motion.div>
      </div>
    </section>
  );
};

// ==================== FINAL CTA SECTION ====================
const FinalCTASection = ({ trialEnabled = true, trialDays = 7 }) => {
  const navigate = useNavigate();

  return (
    <section className="py-20 md:py-28 text-white relative">
      <div className="absolute inset-0 pointer-events-none" aria-hidden="true">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[1000px] h-[600px] bg-cyan-500/15 rounded-full blur-[140px]" />
        <div className="absolute -top-40 left-1/4 w-[400px] h-[400px] bg-cyan-400/8 rounded-full blur-[120px]" />
      </div>

      <div className="max-w-3xl mx-auto px-6 text-center relative z-10">
        <motion.h2
          {...fadeUp}
          className="text-3xl md:text-4xl lg:text-5xl font-bold mb-5 tracking-tight"
        >
          Empieza a estudiar matemáticas de forma{' '}
          <span className="text-cyan-400">más inteligente</span>
        </motion.h2>
        <motion.p
          {...fadeUp}
          className="text-lg md:text-xl text-slate-300 mb-9 max-w-2xl mx-auto"
        >
          Menos tiempo buscando material. Más tiempo aprendiendo y practicando.
        </motion.p>
        <motion.div {...fadeUp}>
          <Button
            size="lg"
            className="bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-bold text-lg px-10 py-6 rounded-full shadow-lg shadow-cyan-500/30 transition-all"
            onClick={() => navigate('/auth')}
            data-testid="final-cta-btn"
          >
            {trialEnabled ? `Empieza gratis · ${trialDays} días` : 'Crear cuenta'}
            <ArrowRight className="ml-2" size={22} />
          </Button>
          <p className="text-slate-400 text-sm mt-4">
            {trialEnabled
              ? 'Sin tarjeta de crédito · Configura tu cuenta en menos de 1 minuto'
              : 'Configura tu cuenta en menos de 1 minuto'}
          </p>
        </motion.div>
      </div>
    </section>
  );
};

// ==================== FOOTER ====================
const Footer = () => {
  return (
    <footer className="bg-slate-950 text-white py-12 border-t border-white/10">
      <div className="max-w-6xl mx-auto px-6">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-3">
            <img src="/remy-logo.png" alt="" className="w-12 h-12 object-contain" />
            <div>
              <h3 className="font-bold text-xl">Remy</h3>
              <p className="text-slate-400 text-sm">by Se Remonta</p>
            </div>
          </div>

          <nav aria-label="Enlaces del pie" className="flex gap-6 md:gap-8 text-slate-400 text-sm md:text-base">
            <a href="#features" className="hover:text-cyan-400 transition-colors">
              Funcionalidades
            </a>
            <a href="#courses" className="hover:text-cyan-400 transition-colors">
              Cursos
            </a>
            <a href="#pricing" className="hover:text-cyan-400 transition-colors">
              Precios
            </a>
            <a href="#faq" className="hover:text-cyan-400 transition-colors">
              FAQ
            </a>
          </nav>

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
  const prefersReducedMotion = useReducedMotion();

  // Landing is fully dark — strip any inherited "dark" class so shadcn theme tokens
  // (used by some components like Card defaults) don't fight our explicit colors.
  useEffect(() => {
    const root = document.documentElement;
    const wasDark = root.classList.contains('dark');
    if (wasDark) {
      root.classList.remove('dark');
    }
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

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-cyan-950 flex items-center justify-center">
        <div className="text-center">
          <img src="/remy-logo.png" alt="" className="w-16 h-16 mx-auto mb-4 animate-pulse" />
          <div
            className="animate-spin w-8 h-8 border-4 border-cyan-500 border-t-transparent rounded-full mx-auto"
            role="status"
            aria-label="Cargando"
          />
        </div>
      </div>
    );
  }

  return (
    <MotionConfig reducedMotion={prefersReducedMotion ? 'always' : 'never'}>
      <div className="min-h-screen bg-slate-950 relative overflow-hidden">
        {/* Global ambient decoration — continuous cyan/blue glow distributed
            across the page so transitions between sections stay seamless. */}
        <div className="absolute inset-0 pointer-events-none z-0" aria-hidden="true">
          <div className="absolute top-[8%] -left-40 w-[600px] h-[600px] bg-cyan-500/[0.10] rounded-full blur-[140px]" />
          <div className="absolute top-[22%] -right-32 w-[550px] h-[550px] bg-blue-500/[0.09] rounded-full blur-[140px]" />
          <div className="absolute top-[38%] left-1/4 w-[700px] h-[500px] bg-cyan-500/[0.08] rounded-full blur-[160px]" />
          <div className="absolute top-[52%] -right-40 w-[600px] h-[600px] bg-cyan-400/[0.09] rounded-full blur-[140px]" />
          <div className="absolute top-[68%] left-1/2 -translate-x-1/2 w-[800px] h-[500px] bg-cyan-500/[0.10] rounded-full blur-[160px]" />
          <div className="absolute top-[82%] -left-32 w-[550px] h-[550px] bg-blue-500/[0.09] rounded-full blur-[140px]" />
          <div className="absolute top-[94%] right-1/4 w-[500px] h-[500px] bg-cyan-500/[0.08] rounded-full blur-[140px]" />
          {/* Faint grid texture across the whole page */}
          <div
            className="absolute inset-0 opacity-[0.03]"
            style={{
              backgroundImage:
                'linear-gradient(to right, white 1px, transparent 1px), linear-gradient(to bottom, white 1px, transparent 1px)',
              backgroundSize: '64px 64px'
            }}
          />
        </div>

        <div className="relative z-10">
          <StickyNav trialEnabled={trialEnabled} />
          <HeroSection trialEnabled={trialEnabled} trialDays={trialDays} />
          <SocialProofSection />
          <ProblemSection />
          <FeaturesSection />
          <CoursesSection />
          <SimulationSection />
          <PricingSection trialEnabled={trialEnabled} trialDays={trialDays} />
          <FAQSection trialEnabled={trialEnabled} trialDays={trialDays} />
          <FinalCTASection trialEnabled={trialEnabled} trialDays={trialDays} />
          <Footer />
        </div>
      </div>
    </MotionConfig>
  );
};

export default Landing;
