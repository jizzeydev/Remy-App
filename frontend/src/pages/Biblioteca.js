import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import axios from 'axios';
import { BookOpen, Loader2, GraduationCap, Crown, Lock, CheckCircle, Search, Building2, Filter, Plus } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useAuth } from '../contexts/AuthContext';
import { usePricing } from '../hooks/usePricing';
import TrialBanner from '../components/TrialBanner';
import { toast } from 'sonner';
import InlineMd from '@/components/course/InlineMd';
import { showAchievementToasts } from '@/lib/achievementToast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Biblioteca = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { canAccessContent } = useAuth();
  const { monthly, formatPrice, getLowestPrice, loading: pricingLoading } = usePricing();
  const [courses, setCourses] = useState([]);
  const [filteredCourses, setFilteredCourses] = useState([]);
  const [universities, setUniversities] = useState([]);
  const [enrolledCourseIds, setEnrolledCourseIds] = useState([]);
  const [enrollmentStats, setEnrollmentStats] = useState({ can_enroll_more: true });
  const [loading, setLoading] = useState(true);
  const [enrolling, setEnrolling] = useState(null);
  
  // Filters
  const [searchTerm, setSearchTerm] = useState('');
  const [filterUniversity, setFilterUniversity] = useState('all');

  // Check for subscription success message
  useEffect(() => {
    if (searchParams.get('subscription') === 'success') {
      toast.success('¡Bienvenido! Tu suscripción está activa.');
      window.history.replaceState({}, '', '/biblioteca');
    }
  }, [searchParams]);

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    // Apply filters
    let filtered = [...courses];
    
    if (searchTerm) {
      filtered = filtered.filter(c => 
        c.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        c.description?.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    
    if (filterUniversity && filterUniversity !== 'all') {
      if (filterUniversity === 'general') {
        filtered = filtered.filter(c => !c.university_id);
      } else {
        filtered = filtered.filter(c => c.university_id === filterUniversity);
      }
    }
    
    setFilteredCourses(filtered);
  }, [courses, searchTerm, filterUniversity]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('remy_session_token');

      // Catalog-only fetch: course title/category/level/university — no chapters,
      // no lessons, no progress. Counts and progress live on Mis Cursos / Progreso.
      const [coursesRes, unisRes] = await Promise.all([
        axios.get(`${API}/courses`),
        axios.get(`${API}/library-universities`)
      ]);

      setCourses(coursesRes.data);
      setUniversities(unisRes.data);

      // Enrolled course IDs + enrollment limits (only when authed). Both endpoints
      // are user-scoped and small; running them in parallel keeps the page fast.
      if (token) {
        const headers = { Authorization: `Bearer ${token}` };
        const [enrollmentsRes, statsRes] = await Promise.all([
          axios.get(`${API}/enrollments`, { headers }).catch(() => ({ data: [] })),
          axios.get(`${API}/enrollments/stats`, { headers }).catch(() => null)
        ]);
        setEnrolledCourseIds((enrollmentsRes.data || []).map((c) => c.id));
        if (statsRes?.data) setEnrollmentStats(statsRes.data);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEnroll = async (e, course) => {
    e.stopPropagation();
    
    const token = localStorage.getItem('remy_session_token');
    if (!token) {
      navigate('/auth');
      return;
    }
    
    if (!enrollmentStats.can_enroll_more && !enrollmentStats.has_subscription) {
      toast.error('Límite de inscripción alcanzado. Suscríbete para acceso ilimitado.');
      navigate('/subscribe');
      return;
    }
    
    setEnrolling(course.id);
    try {
      const res = await axios.post(
        `${API}/enrollments`,
        { course_id: course.id },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      toast.success(`Inscrito en "${course.title}"`);
      showAchievementToasts(res.data?.newly_unlocked_achievements);
      setEnrolledCourseIds(prev => [...prev, course.id]);
      
      // Refresh stats
      const statsRes = await axios.get(`${API}/enrollments/stats`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setEnrollmentStats(statsRes.data);
    } catch (error) {
      console.error('Error enrolling:', error);
      toast.error(error.response?.data?.detail || 'Error al inscribirse');
    } finally {
      setEnrolling(null);
    }
  };

  const handleCourseClick = (course) => {
    navigate(`/course/${course.id}`);
  };

  const getLevelColor = (level) => {
    const colors = {
      'Básico': 'bg-green-500/20 text-green-700 dark:text-green-400',
      'Intermedio': 'bg-blue-500/20 text-blue-700 dark:text-blue-400',
      'Avanzado': 'bg-purple-500/20 text-purple-700 dark:text-purple-400'
    };
    return colors[level] || 'bg-muted text-muted-foreground';
  };

  const isEnrolled = (courseId) => enrolledCourseIds.includes(courseId);
  const hasAccess = canAccessContent();
  const lowestPrice = pricingLoading ? '...' : formatPrice(getLowestPrice());

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12" role="status" aria-live="polite">
        <Loader2 className="animate-spin text-primary" size={32} />
        <span className="sr-only">Cargando cursos</span>
      </div>
    );
  }

  const fadeUp = (i = 0) => ({
    initial: { opacity: 0, y: 16 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.4, delay: i * 0.04, ease: [0.22, 1, 0.36, 1] }
  });

  return (
    <div className="space-y-6 pb-24 lg:pb-8" data-testid="biblioteca-page">
      <TrialBanner />
      
      {!hasAccess && (
        <motion.div {...fadeUp(0)}>
          <Card className="bg-gradient-to-r from-cyan-500 to-blue-600 text-white border-0 shadow-lg shadow-cyan-500/20">
            <CardContent className="flex flex-col sm:flex-row items-center justify-between py-6 gap-4">
              <div className="flex items-center gap-4">
                <div className="bg-white/20 rounded-full p-3 backdrop-blur-sm" aria-hidden="true">
                  <Crown size={24} />
                </div>
                <div>
                  <h3 className="font-bold text-lg">Desbloquea todo el contenido</h3>
                  <p className="text-cyan-50 text-sm">
                    Accede a todos los cursos, simulacros ilimitados y más desde {lowestPrice}/{monthly.period}
                  </p>
                </div>
              </div>
              <Button
                className="bg-white text-cyan-700 hover:bg-cyan-50 font-semibold px-6"
                onClick={() => navigate('/subscribe')}
                data-testid="subscribe-banner-btn"
              >
                Suscribirme ahora
              </Button>
            </CardContent>
          </Card>
        </motion.div>
      )}

      <motion.div {...fadeUp(1)} className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold text-foreground tracking-tight">Biblioteca de Cursos</h1>
          <p className="text-muted-foreground mt-1">
            Explora y encuentra cursos para tu universidad
          </p>
        </div>
        {enrolledCourseIds.length > 0 && (
          <Button variant="outline" onClick={() => navigate('/mis-cursos')}>
            <BookOpen className="mr-2" size={18} />
            Mis Cursos ({enrolledCourseIds.length})
          </Button>
        )}
      </motion.div>

      {/* Filters */}
      <motion.div {...fadeUp(2)} className="flex flex-wrap gap-3 md:gap-4 items-center">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" size={18} aria-hidden="true" />
          <Input
            placeholder="Buscar cursos..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
            data-testid="course-search"
            aria-label="Buscar cursos"
          />
        </div>
        <div className="flex items-center gap-2">
          <Filter size={18} className="text-muted-foreground" aria-hidden="true" />
          <Select value={filterUniversity} onValueChange={setFilterUniversity}>
            <SelectTrigger className="w-[200px]" data-testid="university-filter" aria-label="Filtrar por universidad">
              <SelectValue placeholder="Universidad" />
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
                  <span className="flex items-center gap-2">
                    {uni.logo_url && (
                      <img src={uni.logo_url} alt="" className="w-4 h-4 rounded object-cover" />
                    )}
                    {uni.short_name}
                  </span>
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <div className="text-sm text-muted-foreground">
          {filteredCourses.length} curso(s)
        </div>
      </motion.div>

      {filteredCourses.length === 0 ? (
        <Card className="text-center py-12">
          <CardContent>
            <GraduationCap className="mx-auto mb-4 text-muted-foreground" size={48} />
            <h3 className="text-xl font-semibold mb-2 text-foreground">
              {courses.length === 0 ? 'No hay cursos disponibles' : 'No se encontraron cursos'}
            </h3>
            <p className="text-muted-foreground">
              {courses.length === 0 
                ? 'Los cursos aparecerán aquí cuando estén disponibles'
                : 'Prueba con otros filtros de búsqueda'
              }
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 md:gap-6">
          {filteredCourses.map((course, index) => {
            const enrolled = isEnrolled(course.id);

            return (
              <motion.div key={course.id} {...fadeUp(index + 3)}>
                <Card
                  className={`group cursor-pointer hover:shadow-xl hover:-translate-y-0.5 hover:border-primary/40 transition-all duration-200 border-border bg-card overflow-hidden h-full flex flex-col ${
                    !hasAccess ? 'opacity-95' : ''
                  }`}
                  onClick={() => handleCourseClick(course)}
                  data-testid={`course-card-${index}`}
                >
                  <CardHeader className="relative">
                    {!hasAccess && (
                      <div className="absolute top-4 right-4 z-10">
                        <div className="bg-background/80 backdrop-blur-sm text-foreground rounded-full p-2 border border-border" aria-label="Contenido bloqueado">
                          <Lock size={16} />
                        </div>
                      </div>
                    )}
                    <div className="aspect-video bg-gradient-to-br from-cyan-400 via-cyan-500 to-blue-600 rounded-lg mb-4 flex items-center justify-center relative overflow-hidden">
                      {course.university?.logo_url ? (
                        <img
                          src={course.university.logo_url}
                          alt=""
                          className="absolute inset-0 w-full h-full object-cover opacity-20"
                        />
                      ) : null}
                      {/* Decorative gloss */}
                      <div className="absolute inset-0 bg-gradient-to-tr from-white/0 via-white/10 to-white/20 pointer-events-none" aria-hidden="true" />
                      <span className="text-white text-4xl font-bold relative z-10 tracking-tight group-hover:scale-105 transition-transform duration-300">
                        {course.title.charAt(0)}
                      </span>
                    </div>
                  <div className="flex items-center gap-2 flex-wrap mb-2">
                    <Badge className={getLevelColor(course.level)}>
                      {course.level}
                    </Badge>
                    {course.university && course.university.short_name !== 'GEN' && (
                      <Badge variant="outline" className="text-xs">
                        {course.university.short_name}
                      </Badge>
                    )}
                  </div>
                  <CardTitle className="text-lg text-foreground">{course.title}</CardTitle>
                  <CardDescription className="line-clamp-2">
                    <InlineMd>{course.description}</InlineMd>
                  </CardDescription>
                </CardHeader>
                <CardContent className="flex-1 flex flex-col">
                  <div className="flex items-center justify-between text-sm mb-3">
                    <span className="text-muted-foreground">
                      {course.university?.name || 'General'}
                    </span>
                    <span className="text-xs bg-secondary text-secondary-foreground px-2 py-1 rounded">
                      {course.category}
                    </span>
                  </div>
                  
                  <div className="mt-auto">
                    {hasAccess ? (
                      enrolled ? (
                        <Button
                          className="w-full bg-primary hover:bg-primary/90"
                          onClick={(e) => {
                            e.stopPropagation();
                            navigate(`/course/${course.id}`);
                          }}
                        >
                          <CheckCircle className="mr-2" size={16} />
                          Continuar
                        </Button>
                      ) : (
                        <Button
                          className="w-full"
                          variant="outline"
                          onClick={(e) => handleEnroll(e, course)}
                          disabled={enrolling === course.id}
                        >
                          {enrolling === course.id ? (
                            <Loader2 className="animate-spin mr-2" size={16} />
                          ) : (
                            <Plus className="mr-2" size={16} />
                          )}
                          Inscribirse
                        </Button>
                      )
                    ) : (
                      <Button
                        className="w-full"
                        variant="secondary"
                        onClick={(e) => {
                          e.stopPropagation();
                          navigate('/auth');
                        }}
                      >
                        Crear cuenta gratis
                      </Button>
                    )}
                  </div>
                </CardContent>
                </Card>
              </motion.div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default Biblioteca;
