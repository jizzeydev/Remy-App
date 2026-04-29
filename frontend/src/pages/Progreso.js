/**
 * Progreso Page — student progress hub.
 *
 * Sections (top → bottom):
 *   1. Stats overview (lessons / quizzes / avg grade / streak)
 *   2. Grade trend chart (last 12 attempts, line chart)
 *   3. Weak areas: top 3 chapters with most errors + CTA to practice them
 *   4. Course progress list
 *   5. Recent quiz grades
 *   6. Achievements grid (gamification hub) with link to full /logros page
 */
import { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import axios from 'axios';
import {
  BookOpen, ClipboardCheck, TrendingUp, Award, Loader2, ChevronRight,
  Flame, Target, AlertTriangle, ArrowRight
} from 'lucide-react';
import {
  LineChart, Line, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  ReferenceLine, Cell
} from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { useAuth } from '../contexts/AuthContext';
import SubscriptionRequired from '../components/SubscriptionRequired';
import AchievementsGrid from '../components/AchievementsGrid';
import { getStudentId } from '@/lib/studentId';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const fadeUp = (i = 0) => ({
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.4, delay: i * 0.05, ease: [0.22, 1, 0.36, 1] }
});

const getGradeColor = (grade) => {
  if (grade >= 6) return 'text-emerald-600 dark:text-emerald-400';
  if (grade >= 5) return 'text-primary';
  if (grade >= 4) return 'text-amber-600 dark:text-amber-400';
  return 'text-red-600 dark:text-red-400';
};

const Progreso = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [courses, setCourses] = useState([]);
  const [courseProgress, setCourseProgress] = useState({});
  const [quizHistory, setQuizHistory] = useState([]);
  const [chapterTitles, setChapterTitles] = useState({});
  const [achievementsData, setAchievementsData] = useState(null);

  useEffect(() => {
    fetchAllData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchAllData = async () => {
    setLoading(true);
    const studentId = getStudentId(user);
    if (!studentId) { setLoading(false); return; }
    const token = localStorage.getItem('remy_session_token');
    const authHeaders = token ? { Authorization: `Bearer ${token}` } : {};

    try {
      // Three parallel calls. with-stats returns courses + chapter list +
      // per-course completed_lessons in a single shot, eliminating the legacy
      // 1+N+M waterfall.
      const [coursesRes, quizzesRes, achRes] = await Promise.all([
        axios.get(`${API}/courses/with-stats?student_id=${encodeURIComponent(studentId)}`),
        axios.get(`${API}/quiz/history/${studentId}?limit=100`).catch(() => ({ data: [] })),
        token
          ? axios.get(`${API}/achievements/me`, { headers: authHeaders }).catch(() => null)
          : Promise.resolve(null)
      ]);

      // Only show courses the student is enrolled in. with-stats already returns
      // an `enrolled` flag per course when student_id is set, so we filter here.
      const enrolledCourses = (coursesRes.data || []).filter((c) => c.enrolled);
      setCourses(enrolledCourses);

      const progressMap = {};
      const titlesMap = {};
      enrolledCourses.forEach((c) => {
        const total = c.lesson_count || 0;
        const completed = c.completed_lessons || 0;
        progressMap[c.id] = {
          total,
          completed,
          percentage: total > 0 ? Math.round((completed / total) * 100) : 0
        };
        (c.chapters || []).forEach((ch) => { titlesMap[ch.id] = ch.title; });
      });
      setCourseProgress(progressMap);
      setChapterTitles(titlesMap);

      setQuizHistory(quizzesRes.data || []);
      if (achRes?.data) setAchievementsData(achRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  // ==================== DERIVED STATS ====================
  const totalLessons = Object.values(courseProgress).reduce((sum, p) => sum + p.total, 0);
  const completedLessons = Object.values(courseProgress).reduce((sum, p) => sum + p.completed, 0);
  const overallProgress = totalLessons > 0 ? Math.round((completedLessons / totalLessons) * 100) : 0;

  const completedQuizzes = useMemo(
    () => quizHistory.filter((q) => q.completed && q.grade !== null && q.grade !== undefined),
    [quizHistory]
  );
  const grades = completedQuizzes.map((q) => q.grade);
  const quizAverage = grades.length ? +(grades.reduce((a, b) => a + b, 0) / grades.length).toFixed(1) : 0;
  const recentGrades = grades.slice(0, 10);

  // Trend data: last 12 quizzes ascending, with a sequential index for the X axis.
  const trendData = useMemo(() => {
    const sorted = [...completedQuizzes]
      .reverse()                                  // history is desc → flip to asc
      .slice(-12)
      .map((q, i) => ({
        idx: i + 1,
        grade: q.grade,
        date: q.created_at ? new Date(q.created_at) : null
      }));
    return sorted;
  }, [completedQuizzes]);

  // Weak chapters: aggregate wrong/total per chapter_id across all completed quizzes.
  const weakChapters = useMemo(() => {
    const buckets = {};
    completedQuizzes.forEach((q) => {
      const questions = q.questions || [];
      const answers = q.answers || {};
      questions.forEach((qu, idx) => {
        const chId = qu.chapter_id;
        if (!chId) return;
        if (!buckets[chId]) buckets[chId] = { id: chId, total: 0, wrong: 0, course_id: q.course_id };
        buckets[chId].total += 1;
        const ua = answers[String(idx)] ?? answers[idx];
        if (ua !== qu.correct_answer) buckets[chId].wrong += 1;
      });
    });
    return Object.values(buckets)
      .filter((b) => b.total >= 3)               // need a few datapoints to be meaningful
      .map((b) => ({
        ...b,
        title: chapterTitles[b.id] || 'Capítulo',
        ratio: b.wrong / b.total
      }))
      .sort((a, b) => b.ratio - a.ratio);
  }, [completedQuizzes, chapterTitles]);

  const top3Weak = weakChapters.slice(0, 3);
  // Bar-chart data for ALL practiced chapters (or top 8 if many).
  const chapterChartData = weakChapters.slice(0, 8).map((c) => ({
    short: (c.title || 'Cap.').slice(0, 16) + ((c.title?.length || 0) > 16 ? '…' : ''),
    name: c.title,
    wrong: c.wrong,
    total: c.total,
    ratio: c.ratio
  }));

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12" role="status" aria-live="polite">
        <Loader2 className="animate-spin text-primary" size={32} />
        <span className="sr-only">Cargando progreso</span>
      </div>
    );
  }

  return (
    <div className="space-y-6 pb-24 lg:pb-8" data-testid="progreso-page">
      <motion.div {...fadeUp(0)}>
        <h1 className="text-2xl md:text-3xl font-bold text-foreground tracking-tight">Mi Progreso</h1>
        <p className="text-muted-foreground mt-1">Tu avance de aprendizaje en Remy</p>
      </motion.div>

      {/* ==================== STATS OVERVIEW ==================== */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 md:gap-4">
        <motion.div {...fadeUp(1)}>
          <Card className="border-border bg-gradient-to-br from-primary/10 to-card h-full">
            <CardContent className="pt-5">
              <div className="flex items-start justify-between">
                <div className="min-w-0">
                  <p className="text-xs text-muted-foreground mb-1">Lecciones</p>
                  <p className="text-2xl md:text-3xl font-bold text-foreground tabular-nums">{completedLessons}</p>
                  <p className="text-xs text-muted-foreground mt-0.5">de {totalLessons}</p>
                </div>
                <div className="bg-primary/20 p-2.5 rounded-xl flex-shrink-0" aria-hidden="true">
                  <BookOpen className="text-primary" size={20} />
                </div>
              </div>
              <Progress value={overallProgress} className="mt-3 h-1.5" />
            </CardContent>
          </Card>
        </motion.div>

        <motion.div {...fadeUp(2)}>
          <Card className="border-border bg-gradient-to-br from-violet-500/10 to-card h-full">
            <CardContent className="pt-5">
              <div className="flex items-start justify-between">
                <div className="min-w-0">
                  <p className="text-xs text-muted-foreground mb-1">Simulacros</p>
                  <p className="text-2xl md:text-3xl font-bold text-foreground tabular-nums">{completedQuizzes.length}</p>
                  <p className="text-xs text-muted-foreground mt-0.5">completados</p>
                </div>
                <div className="bg-violet-500/20 p-2.5 rounded-xl flex-shrink-0" aria-hidden="true">
                  <ClipboardCheck className="text-violet-600 dark:text-violet-400" size={20} />
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div {...fadeUp(3)}>
          <Card className="border-border bg-gradient-to-br from-emerald-500/10 to-card h-full">
            <CardContent className="pt-5">
              <div className="flex items-start justify-between">
                <div className="min-w-0">
                  <p className="text-xs text-muted-foreground mb-1">Promedio</p>
                  {completedQuizzes.length > 0 ? (
                    <p className={`text-2xl md:text-3xl font-bold tabular-nums ${getGradeColor(quizAverage)}`}>{quizAverage}</p>
                  ) : (
                    <p className="text-2xl md:text-3xl font-bold text-muted-foreground">-</p>
                  )}
                  <p className="text-xs text-muted-foreground mt-0.5">escala 1.0 - 7.0</p>
                </div>
                <div className="bg-emerald-500/20 p-2.5 rounded-xl flex-shrink-0" aria-hidden="true">
                  <Award className="text-emerald-600 dark:text-emerald-400" size={20} />
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div {...fadeUp(4)}>
          <Card className="border-border bg-gradient-to-br from-rose-500/10 to-card h-full">
            <CardContent className="pt-5">
              <div className="flex items-start justify-between">
                <div className="min-w-0">
                  <p className="text-xs text-muted-foreground mb-1">Racha</p>
                  <p className="text-2xl md:text-3xl font-bold text-foreground tabular-nums">
                    {achievementsData?.stats?.current_streak_days ?? 0}
                  </p>
                  <p className="text-xs text-muted-foreground mt-0.5">
                    días seguidos · máx {achievementsData?.stats?.max_streak_days ?? 0}
                  </p>
                </div>
                <div className="bg-rose-500/20 p-2.5 rounded-xl flex-shrink-0" aria-hidden="true">
                  <Flame className="text-rose-600 dark:text-rose-400" size={20} />
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* ==================== GRADE TREND ==================== */}
      {trendData.length >= 2 && (
        <motion.div {...fadeUp(5)}>
          <Card className="border-border bg-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp size={18} className="text-primary" aria-hidden="true" />
                Tendencia de notas
              </CardTitle>
              <CardDescription>Tus últimos {trendData.length} simulacros</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-56 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={trendData} margin={{ top: 8, right: 12, left: -16, bottom: 8 }}>
                    <XAxis
                      dataKey="idx"
                      stroke="hsl(var(--muted-foreground))"
                      tick={{ fontSize: 11 }}
                      tickFormatter={(v) => `#${v}`}
                    />
                    <YAxis
                      stroke="hsl(var(--muted-foreground))"
                      tick={{ fontSize: 11 }}
                      domain={[1, 7]}
                      ticks={[1, 4, 5.5, 7]}
                    />
                    <ReferenceLine y={4} stroke="#f59e0b" strokeDasharray="3 3" label={{ value: 'Aprobado', fontSize: 10, fill: '#f59e0b', position: 'right' }} />
                    <Tooltip
                      contentStyle={{
                        background: 'hsl(var(--card))',
                        border: '1px solid hsl(var(--border))',
                        borderRadius: 8,
                        fontSize: 12,
                        color: 'hsl(var(--foreground))'
                      }}
                      formatter={(v) => [`${v}`, 'Nota']}
                      labelFormatter={(idx) => {
                        const point = trendData.find((p) => p.idx === idx);
                        return point?.date
                          ? point.date.toLocaleDateString('es-CL', { day: 'numeric', month: 'short' })
                          : `Simulacro ${idx}`;
                      }}
                    />
                    <Line
                      type="monotone"
                      dataKey="grade"
                      stroke="hsl(var(--primary))"
                      strokeWidth={2.5}
                      dot={{ r: 4, fill: 'hsl(var(--primary))', strokeWidth: 0 }}
                      activeDot={{ r: 6 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}

      {/* ==================== WEAK AREAS ==================== */}
      {top3Weak.length > 0 && (
        <motion.div {...fadeUp(6)}>
          <Card className="border-border bg-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertTriangle size={18} className="text-amber-500 dark:text-amber-400" aria-hidden="true" />
                Áreas para mejorar
              </CardTitle>
              <CardDescription>
                Capítulos con más errores en tus simulacros. Practica estos primero.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Top 3 cards with quick CTA */}
              <ul className="space-y-2">
                {top3Weak.map((c, i) => (
                  <li
                    key={c.id}
                    className="flex items-center justify-between gap-3 p-3 rounded-xl bg-muted/40 border border-border"
                  >
                    <div className="flex items-center gap-3 min-w-0">
                      <span className="flex-shrink-0 w-7 h-7 rounded-full bg-amber-500/15 text-amber-700 dark:text-amber-300 font-bold text-sm flex items-center justify-center">
                        {i + 1}
                      </span>
                      <div className="min-w-0">
                        <p className="text-sm font-medium text-foreground truncate">{c.title}</p>
                        <p className="text-xs text-muted-foreground tabular-nums">
                          {c.wrong}/{c.total} errores · {Math.round(c.ratio * 100)}%
                        </p>
                      </div>
                    </div>
                    <Button
                      size="sm"
                      variant="outline"
                      className="flex-shrink-0 rounded-full"
                      onClick={() => navigate('/simulacros')}
                    >
                      <Target size={14} className="mr-1.5" />
                      Practicar
                    </Button>
                  </li>
                ))}
              </ul>

              {/* Bar chart with all practiced chapters */}
              {chapterChartData.length >= 2 && (
                <div className="h-56 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chapterChartData} margin={{ top: 8, right: 12, left: -16, bottom: 8 }}>
                      <XAxis
                        dataKey="short"
                        stroke="hsl(var(--muted-foreground))"
                        tick={{ fontSize: 10 }}
                        interval={0}
                        angle={chapterChartData.length > 4 ? -25 : 0}
                        textAnchor={chapterChartData.length > 4 ? 'end' : 'middle'}
                        height={chapterChartData.length > 4 ? 56 : 30}
                      />
                      <YAxis stroke="hsl(var(--muted-foreground))" tick={{ fontSize: 11 }} allowDecimals={false} />
                      <Tooltip
                        contentStyle={{
                          background: 'hsl(var(--card))',
                          border: '1px solid hsl(var(--border))',
                          borderRadius: 8,
                          fontSize: 12,
                          color: 'hsl(var(--foreground))'
                        }}
                        formatter={(v, _, props) => [`${v} de ${props.payload.total}`, 'Errores']}
                        labelFormatter={(_, payload) => payload?.[0]?.payload?.name || ''}
                      />
                      <Bar dataKey="wrong" radius={[8, 8, 0, 0]} maxBarSize={48}>
                        {chapterChartData.map((entry, i) => (
                          <Cell
                            key={i}
                            fill={
                              entry.ratio >= 0.6 ? '#ef4444' :
                              entry.ratio >= 0.3 ? '#f59e0b' : '#22c55e'
                            }
                          />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              )}
            </CardContent>
          </Card>
        </motion.div>
      )}

      {/* ==================== COURSE PROGRESS ==================== */}
      <motion.div {...fadeUp(7)}>
        <Card className="border-border bg-card">
          <CardHeader>
            <CardTitle>Progreso por curso</CardTitle>
            <CardDescription>Tu avance en los cursos en los que estás inscrito</CardDescription>
          </CardHeader>
          <CardContent>
            {courses.length === 0 ? (
              <div className="text-center py-8 space-y-3">
                <p className="text-muted-foreground">
                  Aún no estás inscrito en ningún curso.
                </p>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => navigate('/biblioteca')}
                  className="rounded-full"
                >
                  <BookOpen size={14} className="mr-1.5" />
                  Explorar biblioteca
                </Button>
              </div>
            ) : (
              <div className="space-y-3">
                {courses.map((course) => {
                  const progress = courseProgress[course.id] || { total: 0, completed: 0, percentage: 0 };
                  return (
                    <div
                      key={course.id}
                      className="p-4 rounded-xl bg-secondary/40 hover:bg-secondary transition-colors cursor-pointer focus:outline-none focus-visible:ring-2 focus-visible:ring-primary"
                      role="button"
                      tabIndex={0}
                      onClick={() => navigate(`/course/${course.id}`)}
                      onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); navigate(`/course/${course.id}`); } }}
                    >
                      <div className="flex items-center justify-between mb-3 gap-2">
                        <div className="min-w-0">
                          <h4 className="font-semibold text-foreground truncate">{course.title}</h4>
                          <p className="text-sm text-muted-foreground">{course.category}</p>
                        </div>
                        <div className="text-right flex-shrink-0">
                          <p className="text-lg font-bold text-primary tabular-nums">{progress.percentage}%</p>
                          <p className="text-xs text-muted-foreground tabular-nums">
                            {progress.completed}/{progress.total} lecciones
                          </p>
                        </div>
                      </div>
                      <Progress value={progress.percentage} className="h-2" />
                    </div>
                  );
                })}
              </div>
            )}
          </CardContent>
        </Card>
      </motion.div>

      {/* ==================== RECENT QUIZ GRADES ==================== */}
      {recentGrades.length > 0 && (
        <motion.div {...fadeUp(8)}>
          <Card className="border-border bg-card">
            <CardHeader>
              <CardTitle>Últimas notas en simulacros</CardTitle>
              <CardDescription>Tus {recentGrades.length} simulacros más recientes</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex gap-3 flex-wrap">
                {recentGrades.map((grade, idx) => (
                  <div
                    key={idx}
                    className={`w-12 h-12 rounded-xl flex items-center justify-center font-bold text-lg tabular-nums ${
                      grade >= 6 ? 'bg-emerald-500/20 text-emerald-700 dark:text-emerald-400' :
                      grade >= 5 ? 'bg-primary/20 text-primary' :
                      grade >= 4 ? 'bg-amber-500/20 text-amber-700 dark:text-amber-400' :
                      'bg-red-500/20 text-red-700 dark:text-red-400'
                    }`}
                    title={`Nota ${Number(grade).toFixed(1)}`}
                  >
                    {Number(grade).toFixed(1)}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}

      {/* ==================== ACHIEVEMENTS ==================== */}
      {achievementsData && (
        <motion.div {...fadeUp(9)}>
          <Card className="border-border bg-card">
            <CardHeader className="flex flex-row items-start justify-between gap-3">
              <div>
                <CardTitle className="flex items-center gap-2">
                  <Award size={18} className="text-amber-500 dark:text-amber-400" aria-hidden="true" />
                  Logros
                </CardTitle>
                <CardDescription>
                  {achievementsData.unlocked_count} de {achievementsData.total_count} desbloqueados
                </CardDescription>
              </div>
              <Button variant="ghost" size="sm" onClick={() => navigate('/logros')} className="rounded-full">
                Ver todos
                <ArrowRight size={14} className="ml-1" />
              </Button>
            </CardHeader>
            <CardContent>
              <AchievementsGrid achievements={achievementsData.achievements} maxToShow={12} />
            </CardContent>
          </Card>
        </motion.div>
      )}

      {/* ==================== EMPTY STATE FOR NEW USERS ==================== */}
      {completedLessons === 0 && completedQuizzes.length === 0 && (
        <motion.div {...fadeUp(10)}>
          <Card className="border-dashed border-border bg-card">
            <CardContent className="py-12 text-center">
              <div className="w-16 h-16 bg-primary/20 rounded-full mx-auto mb-4 flex items-center justify-center">
                <TrendingUp className="text-primary" size={32} />
              </div>
              <h3 className="text-xl font-semibold text-foreground mb-2 tracking-tight">
                ¡Comienza tu aventura de aprendizaje!
              </h3>
              <p className="text-muted-foreground mb-6 max-w-md mx-auto">
                Completa lecciones y realiza simulacros para ver tu progreso aquí.
              </p>
              <Button onClick={() => navigate('/biblioteca')} className="bg-primary hover:bg-primary/90">
                Explorar cursos
              </Button>
            </CardContent>
          </Card>
        </motion.div>
      )}
    </div>
  );
};

// Wrap with subscription guard
export default function ProgresoPage() {
  return (
    <SubscriptionRequired feature="tu página de progreso">
      <Progreso />
    </SubscriptionRequired>
  );
}
