/**
 * Logros (Achievements) page — full catalog grouped by category.
 *
 * The summary stats up top double as motivation; the grouped grids let users
 * scan progress by area (lessons / quizzes / streaks / etc).
 */
import { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import axios from 'axios';
import {
  Award, ArrowLeft, Loader2, Sparkles, BookOpen, Target, Star, Flame, Layers, Crown
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import AchievementsGrid from '../components/AchievementsGrid';
import SubscriptionRequired from '../components/SubscriptionRequired';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const fadeUp = (i = 0) => ({
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.4, delay: i * 0.05, ease: [0.22, 1, 0.36, 1] }
});

// Display order + icons for category headers — keep in sync with backend categories.
const CATEGORIES = [
  { key: 'onboarding', label: 'Primeros pasos',     icon: Sparkles },
  { key: 'lessons',    label: 'Lecciones',          icon: BookOpen },
  { key: 'quizzes',    label: 'Simulacros',         icon: Target },
  { key: 'grades',     label: 'Notas',              icon: Star },
  { key: 'streaks',    label: 'Constancia',         icon: Flame },
  { key: 'coverage',   label: 'Cobertura',          icon: Layers },
  { key: 'special',    label: 'Especiales',         icon: Crown }
];

const Logros = () => {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('remy_session_token');
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    axios.get(`${API}/achievements/me`, { headers })
      .then((r) => setData(r.data))
      .catch((e) => console.error('Error loading achievements:', e))
      .finally(() => setLoading(false));
  }, []);

  // Group achievements by category for the gallery sections.
  const grouped = useMemo(() => {
    if (!data?.achievements) return {};
    const out = {};
    data.achievements.forEach((a) => {
      const cat = a.category || 'special';
      if (!out[cat]) out[cat] = [];
      out[cat].push(a);
    });
    return out;
  }, [data]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12" role="status" aria-live="polite">
        <Loader2 className="animate-spin text-primary" size={32} />
        <span className="sr-only">Cargando logros</span>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="max-w-2xl mx-auto py-12 text-center">
        <p className="text-muted-foreground">No se pudieron cargar tus logros.</p>
        <Button onClick={() => navigate('/progreso')} variant="outline" className="mt-4">
          Volver a progreso
        </Button>
      </div>
    );
  }

  const { achievements, stats, unlocked_count, total_count } = data;
  const overallPct = total_count > 0 ? Math.round((unlocked_count / total_count) * 100) : 0;

  return (
    <div className="space-y-6 pb-24 lg:pb-8" data-testid="logros-page">
      {/* Header */}
      <motion.div {...fadeUp(0)} className="flex items-center justify-between gap-3 flex-wrap">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold text-foreground tracking-tight">Logros</h1>
          <p className="text-muted-foreground mt-1">
            Tu colección de medallas y reconocimientos.
          </p>
        </div>
        <Button
          variant="ghost"
          onClick={() => navigate('/progreso')}
          className="text-muted-foreground hover:text-foreground"
        >
          <ArrowLeft size={18} className="mr-2" />
          Volver a progreso
        </Button>
      </motion.div>

      {/* Summary card */}
      <motion.div {...fadeUp(1)}>
        <Card className="border-border bg-gradient-to-br from-amber-500/10 via-card to-card overflow-hidden">
          <CardContent className="py-6 md:py-8">
            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-6">
              <div className="flex-shrink-0">
                <div className="w-20 h-20 rounded-2xl bg-amber-500/20 ring-1 ring-amber-400/40 flex items-center justify-center">
                  <Award size={40} className="text-amber-600 dark:text-amber-400" aria-hidden="true" />
                </div>
              </div>
              <div className="flex-1 min-w-0 w-full">
                <div className="flex items-baseline gap-2 mb-1">
                  <span className="text-3xl md:text-4xl font-bold text-foreground tabular-nums">{unlocked_count}</span>
                  <span className="text-lg text-muted-foreground tabular-nums">/ {total_count}</span>
                  <span className="text-sm text-muted-foreground ml-2">logros</span>
                </div>
                <Progress value={overallPct} className="h-2 mt-2" aria-label={`${overallPct}% de logros desbloqueados`} />
                <div className="flex flex-wrap gap-x-5 gap-y-1 mt-4 text-sm">
                  <span className="flex items-center gap-1.5 text-muted-foreground">
                    <Flame size={14} className="text-rose-500" aria-hidden="true" />
                    Racha actual: <span className="font-semibold text-foreground tabular-nums">{stats.current_streak_days}</span> días
                  </span>
                  <span className="flex items-center gap-1.5 text-muted-foreground">
                    <Crown size={14} className="text-amber-500" aria-hidden="true" />
                    Mejor racha: <span className="font-semibold text-foreground tabular-nums">{stats.max_streak_days}</span> días
                  </span>
                  <span className="flex items-center gap-1.5 text-muted-foreground">
                    <Star size={14} className="text-primary" aria-hidden="true" />
                    Promedio: <span className="font-semibold text-foreground tabular-nums">{stats.average_grade || '-'}</span>
                  </span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Categories */}
      {CATEGORIES.map((cat, i) => {
        const items = grouped[cat.key] || [];
        if (items.length === 0) return null;
        const unlocked = items.filter((a) => a.unlocked).length;
        const Icon = cat.icon;
        return (
          <motion.div key={cat.key} {...fadeUp(i + 2)}>
            <Card className="border-border bg-card">
              <CardHeader>
                <div className="flex items-center justify-between gap-3 flex-wrap">
                  <CardTitle className="flex items-center gap-2">
                    <Icon size={18} className="text-primary" aria-hidden="true" />
                    {cat.label}
                  </CardTitle>
                  <span className="text-sm text-muted-foreground tabular-nums">
                    {unlocked} / {items.length}
                  </span>
                </div>
                <CardDescription className="sr-only">{cat.label}</CardDescription>
              </CardHeader>
              <CardContent>
                <AchievementsGrid achievements={items} />
              </CardContent>
            </Card>
          </motion.div>
        );
      })}
    </div>
  );
};

export default function LogrosPage() {
  return (
    <SubscriptionRequired feature="los logros">
      <Logros />
    </SubscriptionRequired>
  );
}
