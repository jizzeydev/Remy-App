import { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { 
  BookOpen, ClipboardList, Users, GraduationCap, 
  DollarSign, TrendingUp, Calendar, CreditCard,
  UserCheck, UserX, RefreshCw
} from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Helper to format currency
const formatCLP = (amount) => {
  return new Intl.NumberFormat('es-CL', {
    style: 'currency',
    currency: 'CLP',
    minimumFractionDigits: 0
  }).format(amount);
};

// Helper to get date range
const getDateRange = (range) => {
  const now = new Date();
  let start, end;
  
  switch (range) {
    case 'today':
      start = new Date(now.getFullYear(), now.getMonth(), now.getDate());
      end = now;
      break;
    case 'week':
      start = new Date(now.getFullYear(), now.getMonth(), now.getDate() - 7);
      end = now;
      break;
    case 'month':
      start = new Date(now.getFullYear(), now.getMonth(), 1);
      end = now;
      break;
    case 'last_month':
      start = new Date(now.getFullYear(), now.getMonth() - 1, 1);
      end = new Date(now.getFullYear(), now.getMonth(), 0);
      break;
    case '3months':
      start = new Date(now.getFullYear(), now.getMonth() - 2, 1);
      end = now;
      break;
    case '6months':
      start = new Date(now.getFullYear(), now.getMonth() - 5, 1);
      end = now;
      break;
    case 'year':
      start = new Date(now.getFullYear(), 0, 1);
      end = now;
      break;
    default:
      start = new Date(now.getFullYear(), now.getMonth(), 1);
      end = now;
  }
  
  return { start, end };
};

const AdminDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [dateRange, setDateRange] = useState('month');
  
  // Content stats
  const [contentStats, setContentStats] = useState({
    courses: 0,
    lessons: 0,
    questions: 0
  });
  
  // User/subscription stats
  const [userStats, setUserStats] = useState({
    total_users: 0,
    subscription_stats: { active: 0, inactive: 0, cancelled: 0, expired: 0 },
    subscription_types: { mercadopago: 0, manual: 0 },
    recent_registrations: 0
  });
  
  // Revenue stats
  const [revenueStats, setRevenueStats] = useState({
    total_revenue: 0,
    total_subscriptions: 0,
    revenue_by_plan: {},
    daily_revenue: []
  });
  
  // Monthly comparison
  const [monthlyData, setMonthlyData] = useState([]);

  const token = localStorage.getItem('admin_token');
  const authHeaders = { Authorization: `Bearer ${token}` };

  useEffect(() => {
    fetchAllStats();
  }, []);

  useEffect(() => {
    fetchRevenueStats();
  }, [dateRange]);

  const fetchAllStats = async () => {
    setLoading(true);
    await Promise.all([
      fetchContentStats(),
      fetchUserStats(),
      fetchRevenueStats(),
      fetchMonthlyData()
    ]);
    setLoading(false);
  };

  const fetchContentStats = async () => {
    try {
      const coursesRes = await axios.get(`${API}/courses`);
      const questionsRes = await axios.get(`${API}/admin/questions`, { headers: authHeaders });
      
      let totalLessons = 0;
      for (const course of coursesRes.data) {
        try {
          const chaptersRes = await axios.get(`${API}/courses/${course.id}/chapters`);
          for (const chapter of chaptersRes.data) {
            const lessonsRes = await axios.get(`${API}/chapters/${chapter.id}/lessons`);
            totalLessons += lessonsRes.data.length;
          }
        } catch (e) {}
      }

      setContentStats({
        courses: coursesRes.data.length,
        lessons: totalLessons,
        questions: questionsRes.data.length
      });
    } catch (error) {
      console.error('Error fetching content stats:', error);
    }
  };

  const fetchUserStats = async () => {
    try {
      const response = await axios.get(`${API}/admin/users/stats`, { headers: authHeaders });
      setUserStats(response.data);
    } catch (error) {
      console.error('Error fetching user stats:', error);
    }
  };

  const fetchRevenueStats = async () => {
    try {
      const { start, end } = getDateRange(dateRange);
      const response = await axios.get(`${API}/admin/users/revenue/summary`, {
        headers: authHeaders,
        params: {
          start_date: start.toISOString(),
          end_date: end.toISOString()
        }
      });
      setRevenueStats(response.data);
    } catch (error) {
      console.error('Error fetching revenue stats:', error);
    }
  };

  const fetchMonthlyData = async () => {
    try {
      const response = await axios.get(`${API}/admin/users/revenue/monthly`, {
        headers: authHeaders,
        params: { months: 6 }
      });
      setMonthlyData(response.data.monthly_data || []);
    } catch (error) {
      console.error('Error fetching monthly data:', error);
    }
  };

  const handleRefresh = () => {
    toast.promise(fetchAllStats(), {
      loading: 'Actualizando estadísticas...',
      success: 'Estadísticas actualizadas',
      error: 'Error al actualizar'
    });
  };

  // Get max revenue for chart scaling
  const maxDailyRevenue = Math.max(...(revenueStats.daily_revenue?.map(d => d.amount) || [0]), 1);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
          <p className="text-slate-600">Panel de control de Remy</p>
        </div>
        <Button variant="outline" onClick={handleRefresh} disabled={loading}>
          <RefreshCw className={`mr-2 h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
          Actualizar
        </Button>
      </div>

      {/* Revenue & Subscriptions Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold flex items-center gap-2">
            <TrendingUp className="h-5 w-5 text-emerald-600" />
            Ingresos y Suscripciones
          </h2>
          <Select value={dateRange} onValueChange={setDateRange}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Rango de tiempo" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="today">Hoy</SelectItem>
              <SelectItem value="week">Últimos 7 días</SelectItem>
              <SelectItem value="month">Este mes</SelectItem>
              <SelectItem value="last_month">Mes anterior</SelectItem>
              <SelectItem value="3months">Últimos 3 meses</SelectItem>
              <SelectItem value="6months">Últimos 6 meses</SelectItem>
              <SelectItem value="year">Este año</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Revenue Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card className="border-l-4 border-l-emerald-500">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-600 mb-1">Ingresos del Período</p>
                  <p className="text-2xl font-bold text-emerald-600">
                    {formatCLP(revenueStats.total_revenue)}
                  </p>
                </div>
                <div className="bg-emerald-100 p-3 rounded-lg">
                  <DollarSign className="text-emerald-600" size={24} />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-blue-500">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-600 mb-1">Suscripciones Activas</p>
                  <p className="text-2xl font-bold text-blue-600">
                    {userStats.subscription_stats?.active || 0}
                  </p>
                </div>
                <div className="bg-blue-100 p-3 rounded-lg">
                  <UserCheck className="text-blue-600" size={24} />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-purple-500">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-600 mb-1">Nuevas Suscripciones</p>
                  <p className="text-2xl font-bold text-purple-600">
                    {revenueStats.total_subscriptions}
                  </p>
                  <p className="text-xs text-slate-500">en el período</p>
                </div>
                <div className="bg-purple-100 p-3 rounded-lg">
                  <CreditCard className="text-purple-600" size={24} />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-orange-500">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-600 mb-1">Total Usuarios</p>
                  <p className="text-2xl font-bold text-orange-600">
                    {userStats.total_users}
                  </p>
                  <p className="text-xs text-slate-500">
                    +{userStats.recent_registrations} esta semana
                  </p>
                </div>
                <div className="bg-orange-100 p-3 rounded-lg">
                  <Users className="text-orange-600" size={24} />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Monthly Revenue Chart */}
      {monthlyData.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Calendar className="h-5 w-5" />
              Ingresos Mensuales
            </CardTitle>
            <CardDescription>Comparativa de los últimos 6 meses</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {monthlyData.map((month, index) => {
                const maxRevenue = Math.max(...monthlyData.map(m => m.revenue), 1);
                const percentage = (month.revenue / maxRevenue) * 100;
                
                return (
                  <div key={index} className="flex items-center gap-4">
                    <div className="w-24 text-sm text-slate-600">
                      {month.month_name}
                    </div>
                    <div className="flex-1 h-8 bg-slate-100 rounded-lg overflow-hidden">
                      <div 
                        className="h-full bg-gradient-to-r from-emerald-500 to-emerald-400 rounded-lg transition-all duration-500"
                        style={{ width: `${Math.max(percentage, 2)}%` }}
                      />
                    </div>
                    <div className="w-28 text-right font-semibold">
                      {formatCLP(month.revenue)}
                    </div>
                    <div className="w-16 text-right text-sm text-slate-500">
                      {month.subscriptions} sub.
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Subscription Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* By Status */}
        <Card>
          <CardHeader>
            <CardTitle>Estado de Suscripciones</CardTitle>
            <CardDescription>Distribución actual de usuarios</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-emerald-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <UserCheck className="text-emerald-600" size={20} />
                  <span>Activas</span>
                </div>
                <span className="font-bold text-emerald-600">
                  {userStats.subscription_stats?.active || 0}
                </span>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <Users className="text-slate-600" size={20} />
                  <span>Inactivas (sin suscripción)</span>
                </div>
                <span className="font-bold text-slate-600">
                  {userStats.subscription_stats?.inactive || 0}
                </span>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-red-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <UserX className="text-red-600" size={20} />
                  <span>Canceladas</span>
                </div>
                <span className="font-bold text-red-600">
                  {userStats.subscription_stats?.cancelled || 0}
                </span>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-amber-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <Calendar className="text-amber-600" size={20} />
                  <span>Expiradas</span>
                </div>
                <span className="font-bold text-amber-600">
                  {userStats.subscription_stats?.expired || 0}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* By Type */}
        <Card>
          <CardHeader>
            <CardTitle>Tipo de Suscripción</CardTitle>
            <CardDescription>Cómo se suscribieron los usuarios activos</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <CreditCard className="text-blue-600" size={20} />
                  <span>Mercado Pago</span>
                </div>
                <span className="font-bold text-blue-600">
                  {userStats.subscription_types?.mercadopago || 0}
                </span>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <Users className="text-purple-600" size={20} />
                  <span>Acceso Manual (Admin)</span>
                </div>
                <span className="font-bold text-purple-600">
                  {userStats.subscription_types?.manual || 0}
                </span>
              </div>
            </div>

            {/* Revenue by Plan */}
            {Object.keys(revenueStats.revenue_by_plan || {}).length > 0 && (
              <div className="mt-6 pt-4 border-t">
                <h4 className="font-semibold mb-3">Ingresos por Plan</h4>
                {Object.entries(revenueStats.revenue_by_plan).map(([plan, amount]) => (
                  <div key={plan} className="flex items-center justify-between py-2">
                    <span className="capitalize">{plan}</span>
                    <span className="font-semibold">{formatCLP(amount)}</span>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Content Stats */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold flex items-center gap-2">
          <BookOpen className="h-5 w-5 text-blue-600" />
          Contenido de la Plataforma
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-600 mb-1">Cursos</p>
                  <p className="text-3xl font-bold">{contentStats.courses}</p>
                </div>
                <div className="bg-blue-500 p-3 rounded-lg">
                  <BookOpen className="text-white" size={24} />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-600 mb-1">Lecciones</p>
                  <p className="text-3xl font-bold">{contentStats.lessons}</p>
                </div>
                <div className="bg-emerald-500 p-3 rounded-lg">
                  <GraduationCap className="text-white" size={24} />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-600 mb-1">Preguntas</p>
                  <p className="text-3xl font-bold">{contentStats.questions}</p>
                </div>
                <div className="bg-purple-500 p-3 rounded-lg">
                  <ClipboardList className="text-white" size={24} />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
