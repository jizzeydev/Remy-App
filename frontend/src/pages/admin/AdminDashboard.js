import { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { BookOpen, Calculator, ClipboardList, Users } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AdminDashboard = () => {
  const [stats, setStats] = useState({
    courses: 0,
    formulas: 0,
    questions: 0,
    users: 0
  });

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const [coursesRes, formulasRes] = await Promise.all([
        axios.get(`${API}/courses`),
        axios.post(`${API}/formulas/search`, { query: '', course_id: null })
      ]);
      
      const token = localStorage.getItem('admin_token');
      const questionsRes = await axios.get(`${BACKEND_URL}/api/admin/questions`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      setStats({
        courses: coursesRes.data.length,
        formulas: formulasRes.data.length,
        questions: questionsRes.data.length,
        users: 0
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const statCards = [
    { icon: BookOpen, label: 'Cursos', value: stats.courses, color: 'bg-blue-500' },
    { icon: Calculator, label: 'Fórmulas', value: stats.formulas, color: 'bg-emerald-500' },
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
              Crea y administra cursos. Puedes subir PDFs teóricos y generar resúmenes automáticos con Gemini.
            </p>
          </div>
          <div>
            <h3 className="font-semibold mb-2">🔢 Fórmulas</h3>
            <p className="text-sm text-slate-600">
              Agrega fórmulas matemáticas con soporte LaTeX para que los estudiantes puedan buscarlas.
            </p>
          </div>
          <div>
            <h3 className="font-semibold mb-2">❓ Preguntas</h3>
            <p className="text-sm text-slate-600">
              Crea bancos de preguntas manualmente o genera automáticamente desde PDFs de ejercicios usando Gemini.
              Las preguntas se organizan por curso, tema, subtema y dificultad.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default AdminDashboard;
