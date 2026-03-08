import { useState, useEffect } from 'react';
import axios from 'axios';
import { TrendingUp, Award, Target, Calendar, Loader2 } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Progreso = () => {
  const [progressData, setProgressData] = useState([]);
  const [loading, setLoading] = useState(true);
  const userId = 'demo-user-001';

  useEffect(() => {
    fetchProgress();
  }, []);

  const fetchProgress = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/progress/${userId}`);
      setProgressData(response.data);
    } catch (error) {
      console.error('Error fetching progress:', error);
    } finally {
      setLoading(false);
    }
  };

  const stats = {
    totalLessons: 45,
    completedLessons: 28,
    totalQuizzes: 12,
    completedQuizzes: 8,
    averageScore: 87,
    studyStreak: 7
  };

  const achievements = [
    { icon: Award, title: 'Primera victoria', description: 'Completaste tu primer simulacro', earned: true },
    { icon: Target, title: 'Experto en cálculo', description: 'Completa 10 lecciones de cálculo', earned: true },
    { icon: TrendingUp, title: 'Racha de estudio', description: 'Estudia 7 días seguidos', earned: true },
    { icon: Calendar, title: 'Mes completo', description: 'Estudia todos los días del mes', earned: false },
  ];

  return (
    <div className="space-y-6 pb-24 lg:pb-8" data-testid="progreso-page">
      <div>
        <h1 className="text-3xl font-bold">Tu Progreso</h1>
        <p className="text-slate-600 mt-1">Seguimiento detallado de tu aprendizaje</p>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Card data-testid="stat-lessons">
          <CardContent className="pt-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-primary mb-1">{stats.completedLessons}</div>
              <div className="text-sm text-slate-600">Lecciones completadas</div>
              <Progress value={(stats.completedLessons / stats.totalLessons) * 100} className="mt-3" />
            </div>
          </CardContent>
        </Card>

        <Card data-testid="stat-quizzes">
          <CardContent className="pt-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-primary mb-1">{stats.completedQuizzes}</div>
              <div className="text-sm text-slate-600">Simulacros realizados</div>
              <Progress value={(stats.completedQuizzes / stats.totalQuizzes) * 100} className="mt-3" />
            </div>
          </CardContent>
        </Card>

        <Card data-testid="stat-average">
          <CardContent className="pt-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-primary mb-1">{stats.averageScore}%</div>
              <div className="text-sm text-slate-600">Promedio general</div>
              <Progress value={stats.averageScore} className="mt-3" />
            </div>
          </CardContent>
        </Card>

        <Card data-testid="stat-streak">
          <CardContent className="pt-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-primary mb-1">{stats.studyStreak}</div>
              <div className="text-sm text-slate-600">Días de racha</div>
              <div className="mt-3 text-2xl">🔥</div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Progress */}
      <Tabs defaultValue="courses" className="w-full">
        <TabsList data-testid="progress-tabs">
          <TabsTrigger value="courses">Cursos</TabsTrigger>
          <TabsTrigger value="achievements">Logros</TabsTrigger>
          <TabsTrigger value="activity">Actividad</TabsTrigger>
        </TabsList>

        <TabsContent value="courses" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Progreso por curso</CardTitle>
              <CardDescription>Tu avance en cada curso</CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="animate-spin text-primary" size={32} />
                </div>
              ) : progressData.length === 0 ? (
                <div className="text-center py-8 text-slate-500">
                  No hay datos de progreso aún
                </div>
              ) : (
                <div className="space-y-6">
                  {progressData.map((progress, index) => (
                    <div key={progress.id} data-testid={`progress-item-${index}`}>
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-semibold">Curso {index + 1}</span>
                        <span className="text-sm text-slate-600">
                          {progress.completed_modules}/{progress.total_modules} módulos
                        </span>
                      </div>
                      <Progress
                        value={(progress.completed_modules / progress.total_modules) * 100}
                        className="h-3"
                      />
                      <div className="mt-2 flex items-center justify-between text-sm text-slate-500">
                        <span>Simulacros: {progress.quizzes_completed}</span>
                        <span>
                          Última actividad:{' '}
                          {new Date(progress.last_activity).toLocaleDateString('es-ES')}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="achievements" className="mt-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {achievements.map((achievement, index) => {
              const Icon = achievement.icon;
              return (
                <Card
                  key={index}
                  className={achievement.earned ? 'border-primary' : 'opacity-50'}
                  data-testid={`achievement-${index}`}
                >
                  <CardContent className="pt-6">
                    <div className="flex items-start gap-4">
                      <div
                        className={`w-12 h-12 rounded-xl flex items-center justify-center ${
                          achievement.earned
                            ? 'bg-gradient-to-br from-cyan-400 to-cyan-600 text-white'
                            : 'bg-slate-100 text-slate-400'
                        }`}
                      >
                        <Icon size={24} />
                      </div>
                      <div className="flex-1">
                        <h4 className="font-semibold mb-1">{achievement.title}</h4>
                        <p className="text-sm text-slate-600">{achievement.description}</p>
                        {achievement.earned && (
                          <div className="mt-2">
                            <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">
                              ✔ Desbloqueado
                            </span>
                          </div>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </TabsContent>

        <TabsContent value="activity" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Actividad reciente</CardTitle>
              <CardDescription>Últimas 7 días</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {[
                  { date: 'Hoy', activity: 'Completaste 3 lecciones de Cálculo II' },
                  { date: 'Ayer', activity: 'Realizaste un simulacro de Derivadas' },
                  { date: 'Hace 2 días', activity: 'Consultaste 5 fórmulas' },
                  { date: 'Hace 3 días', activity: 'Chateaste con Remy sobre integrales' },
                  { date: 'Hace 4 días', activity: 'Completaste un simulacro con 90%' },
                ].map((item, index) => (
                  <div
                    key={index}
                    className="flex items-start gap-4 pb-4 border-b border-slate-100 last:border-0"
                    data-testid={`activity-item-${index}`}
                  >
                    <div className="w-2 h-2 mt-2 rounded-full bg-primary"></div>
                    <div>
                      <div className="text-sm font-medium">{item.date}</div>
                      <div className="text-sm text-slate-600">{item.activity}</div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Progreso;
