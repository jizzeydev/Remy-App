import { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { BookOpen, ClipboardList, Users, GraduationCap } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AdminDashboard = () => {
  const [stats, setStats] = useState({
    courses: 0,
    lessons: 0,
    questions: 0,
    users: 0
  });

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const coursesRes = await axios.get(`${API}/courses`);
      
      const token = localStorage.getItem('admin_token');
      const questionsRes = await axios.get(`${BACKEND_URL}/api/admin/questions`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      // Count lessons by fetching chapters and their lessons
      let totalLessons = 0;
      for (const course of coursesRes.data) {
        try {
          const chaptersRes = await axios.get(`${API}/courses/${course.id}/chapters`);
          for (const chapter of chaptersRes.data) {
            const lessonsRes = await axios.get(`${API}/chapters/${chapter.id}/lessons`);
            totalLessons += lessonsRes.data.length;
          }
        } catch (e) {
          console.error('Error fetching lessons:', e);
        }
      }

      setStats({
        courses: coursesRes.data.length,
        lessons: totalLessons,
        questions: questionsRes.data.length,
        users: 0
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const statCards = [
    { icon: BookOpen, label: 'Cursos', value: stats.courses, color: 'bg-blue-500' },
    { icon: GraduationCap, label: 'Lecciones', value: stats.lessons, color: 'bg-emerald-500' },
    { icon: ClipboardList, label: 'Preguntas', value: stats.questions, color: 'bg-purple-500' },
    { icon: Users, label: 'Usuarios', value: stats.users, color: 'bg-orange-500' },
  ];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
        <p className="text-slate-600">Bienvenido al panel de administración de Remy</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <Card key={index}>
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-slate-600 mb-1">{stat.label}</p>
                    <p className="text-3xl font-bold">{stat.value}</p>
                  </div>
                  <div className={`${stat.color} p-3 rounded-lg`}>
                    <Icon className="text-white" size={24} />
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Guía de Uso</CardTitle>
          <CardDescription>Cómo usar el panel de administración</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <h3 className="font-semibold mb-2">📚 Cursos</h3>
            <p className="text-sm text-slate-600">
              Crea y administra cursos con capítulos y lecciones. Usa la AI "Remy" (GPT-5.2) para generar 
              contenido educativo de alta calidad con visualizaciones Desmos interactivas.
            </p>
          </div>
          <div>
            <h3 className="font-semibold mb-2">❓ Preguntas</h3>
            <p className="text-sm text-slate-600">
              Crea bancos de preguntas manualmente o genera automáticamente usando AI.
              Las preguntas se organizan por curso, tema, subtema y dificultad para los Simulacros.
            </p>
          </div>
          <div>
            <h3 className="font-semibold mb-2">🖼️ Imágenes</h3>
            <p className="text-sm text-slate-600">
              Puedes generar imágenes con AI (GPT Image 1) o subir tus propias imágenes desde el editor 
              de lecciones para completar los placeholders de imagen.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default AdminDashboard;
