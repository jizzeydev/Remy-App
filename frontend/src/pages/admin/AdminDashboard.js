import { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { 
  Users, DollarSign, TrendingUp, CreditCard, 
  ClipboardList, BookOpen, GraduationCap, RefreshCw,
  ArrowUpRight, ArrowDownRight, Activity, UserPlus,
  Building2, Target
} from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Format currency
const formatCLP = (amount) => {
  return '$' + new Intl.NumberFormat('es-CL').format(amount);
};

// Simple bar chart component
const MiniBarChart = ({ data, dataKey, color = "#06b6d4", height = 60 }) => {
  if (!data || data.length === 0) return <div className="h-[60px] bg-slate-100 rounded animate-pulse" />;
  
  const max = Math.max(...data.map(d => d[dataKey] || 0), 1);
  
  return (
    <div className="flex items-end gap-[2px] h-[60px]">
      {data.slice(-14).map((item, index) => (
        <div
          key={index}
          className="flex-1 rounded-t transition-all hover:opacity-80"
          style={{
            height: `${Math.max(4, (item[dataKey] / max) * 100)}%`,
            backgroundColor: color,
            minWidth: '4px'
          }}
          title={`${item.date}: ${item[dataKey]}`}
        />
      ))}
    </div>
  );
};

// Stat Card Component
const StatCard = ({ title, value, subtitle, icon: Icon, trend, trendValue, color = "cyan" }) => {
  const colorClasses = {
    cyan: "bg-cyan-50 text-cyan-600",
    green: "bg-green-50 text-green-600",
    purple: "bg-purple-50 text-purple-600",
    blue: "bg-blue-50 text-blue-600",
    yellow: "bg-yellow-50 text-yellow-600"
  };

  return (
    <Card>
      <CardContent className="pt-6">
        <div className="flex items-start justify-between">
          <div className={`p-2 rounded-lg ${colorClasses[color]}`}>
            <Icon size={20} />
          </div>
          {trend !== undefined && (
            <div className={`flex items-center gap-1 text-sm ${trend >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              {trend >= 0 ? <ArrowUpRight size={16} /> : <ArrowDownRight size={16} />}
              {Math.abs(trendValue || trend)}%
            </div>
          )}
        </div>
        <div className="mt-4">
          <h3 className="text-2xl font-bold">{value}</h3>
          <p className="text-sm text-slate-500">{title}</p>
          {subtitle && <p className="text-xs text-slate-400 mt-1">{subtitle}</p>}
        </div>
      </CardContent>
    </Card>
  );
};

const AdminDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [chartDays, setChartDays] = useState(30);
  
  // Dashboard data
  const [metrics, setMetrics] = useState(null);
  const [revenueChart, setRevenueChart] = useState([]);
  const [usersChart, setUsersChart] = useState([]);
  const [simulationsChart, setSimulationsChart] = useState([]);
  const [recentActivity, setRecentActivity] = useState([]);
  
  useEffect(() => {
    fetchAllData();
  }, []);

  useEffect(() => {
    fetchCharts();
  }, [chartDays]);

  const fetchAllData = async () => {
    setLoading(true);
    await Promise.all([
      fetchMetrics(),
      fetchCharts(),
      fetchRecentActivity()
    ]);
    setLoading(false);
  };

  const fetchMetrics = async () => {
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.get(`${API}/admin/analytics/dashboard`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setMetrics(response.data);
    } catch (error) {
      console.error('Error fetching metrics:', error);
      toast.error('Error al cargar métricas');
    }
  };

  const fetchCharts = async () => {
    try {
      const token = localStorage.getItem('admin_token');
      
      const [revenue, users, simulations] = await Promise.all([
        axios.get(`${API}/admin/analytics/revenue/chart?days=${chartDays}`, {
          headers: { Authorization: `Bearer ${token}` }
        }),
        axios.get(`${API}/admin/analytics/users/chart?days=${chartDays}`, {
          headers: { Authorization: `Bearer ${token}` }
        }),
        axios.get(`${API}/admin/analytics/simulations/chart?days=${chartDays}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
      ]);
      
      setRevenueChart(revenue.data.data || []);
      setUsersChart(users.data.data || []);
      setSimulationsChart(simulations.data.data || []);
    } catch (error) {
      console.error('Error fetching charts:', error);
    }
  };

  const fetchRecentActivity = async () => {
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.get(`${API}/admin/analytics/activity/recent?limit=10`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setRecentActivity(response.data || []);
    } catch (error) {
      console.error('Error fetching activity:', error);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchAllData();
    setRefreshing(false);
    toast.success('Datos actualizados');
  };

  if (loading || !metrics) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold">Dashboard</h1>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[1, 2, 3, 4].map(i => (
            <Card key={i}>
              <CardContent className="pt-6">
                <div className="h-24 bg-slate-100 rounded animate-pulse" />
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-slate-500 mt-1">Métricas de negocio y contenido</p>
        </div>
        <div className="flex items-center gap-4">
          <Select value={String(chartDays)} onValueChange={(v) => setChartDays(Number(v))}>
            <SelectTrigger className="w-[140px]">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="7">7 días</SelectItem>
              <SelectItem value="14">14 días</SelectItem>
              <SelectItem value="30">30 días</SelectItem>
              <SelectItem value="60">60 días</SelectItem>
              <SelectItem value="90">90 días</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="outline" onClick={handleRefresh} disabled={refreshing}>
            <RefreshCw size={16} className={`mr-2 ${refreshing ? 'animate-spin' : ''}`} />
            Actualizar
          </Button>
        </div>
      </div>

      {/* Key Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard 
          title="Ingresos Totales"
          value={formatCLP(metrics.revenue.total)}
          subtitle={`${formatCLP(metrics.revenue.this_month)} este mes`}
          icon={DollarSign}
          trend={metrics.revenue.growth_percent}
          color="green"
        />
        <StatCard 
          title="Suscripciones Activas"
          value={metrics.subscriptions.active}
          subtitle={`${metrics.subscriptions.mercadopago} MP + ${metrics.subscriptions.manual} manual`}
          icon={CreditCard}
          color="purple"
        />
        <StatCard 
          title="Usuarios Totales"
          value={metrics.users.total}
          subtitle={`${metrics.users.new_this_month} nuevos este mes`}
          icon={Users}
          trend={metrics.users.growth_percent}
          color="blue"
        />
        <StatCard 
          title="Simulacros Totales"
          value={metrics.simulations.total}
          subtitle={`${metrics.simulations.this_month} este mes`}
          icon={Target}
          color="cyan"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Revenue Chart */}
        <Card>
          <CardHeader className="pb-2">
            <div className="flex items-center justify-between">
              <CardTitle className="text-base">Ingresos</CardTitle>
              <Badge variant="secondary">{chartDays} días</Badge>
            </div>
          </CardHeader>
          <CardContent>
            <MiniBarChart data={revenueChart} dataKey="revenue" color="#22c55e" />
            <div className="mt-2 text-sm text-slate-500">
              Total período: {formatCLP(revenueChart.reduce((sum, d) => sum + (d.revenue || 0), 0))}
            </div>
          </CardContent>
        </Card>

        {/* Users Chart */}
        <Card>
          <CardHeader className="pb-2">
            <div className="flex items-center justify-between">
              <CardTitle className="text-base">Nuevos Usuarios</CardTitle>
              <Badge variant="secondary">{chartDays} días</Badge>
            </div>
          </CardHeader>
          <CardContent>
            <MiniBarChart data={usersChart} dataKey="new_users" color="#3b82f6" />
            <div className="mt-2 text-sm text-slate-500">
              Total período: {usersChart.reduce((sum, d) => sum + (d.new_users || 0), 0)} usuarios
            </div>
          </CardContent>
        </Card>

        {/* Simulations Chart */}
        <Card>
          <CardHeader className="pb-2">
            <div className="flex items-center justify-between">
              <CardTitle className="text-base">Simulacros</CardTitle>
              <Badge variant="secondary">{chartDays} días</Badge>
            </div>
          </CardHeader>
          <CardContent>
            <MiniBarChart data={simulationsChart} dataKey="simulations" color="#06b6d4" />
            <div className="mt-2 text-sm text-slate-500">
              Total período: {simulationsChart.reduce((sum, d) => sum + (d.simulations || 0), 0)} simulacros
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Second Row - Content Stats & Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Content Stats */}
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BookOpen size={20} className="text-cyan-500" />
              Contenido
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
              <div className="flex items-center gap-3">
                <GraduationCap size={20} className="text-blue-500" />
                <span>Cursos</span>
              </div>
              <span className="font-bold">{metrics.content.courses}</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
              <div className="flex items-center gap-3">
                <BookOpen size={20} className="text-green-500" />
                <span>Lecciones</span>
              </div>
              <span className="font-bold">{metrics.content.lessons}</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
              <div className="flex items-center gap-3">
                <ClipboardList size={20} className="text-purple-500" />
                <span>Preguntas</span>
              </div>
              <span className="font-bold">{metrics.content.questions}</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
              <div className="flex items-center gap-3">
                <Building2 size={20} className="text-orange-500" />
                <span>Universidades</span>
              </div>
              <span className="font-bold">{metrics.content.universities}</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
              <div className="flex items-center gap-3">
                <Target size={20} className="text-red-500" />
                <span>Preguntas Uni.</span>
              </div>
              <span className="font-bold">{metrics.content.university_questions}</span>
            </div>
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity size={20} className="text-cyan-500" />
              Actividad Reciente
            </CardTitle>
          </CardHeader>
          <CardContent>
            {recentActivity.length === 0 ? (
              <p className="text-slate-500 text-center py-8">Sin actividad reciente</p>
            ) : (
              <div className="space-y-3 max-h-[400px] overflow-y-auto">
                {recentActivity.map((activity, index) => (
                  <div 
                    key={index}
                    className="flex items-center gap-4 p-3 bg-slate-50 rounded-lg"
                  >
                    <div className={`p-2 rounded-full ${
                      activity.type === 'user_registration' ? 'bg-blue-100 text-blue-600' :
                      activity.type === 'subscription' ? 'bg-green-100 text-green-600' :
                      'bg-cyan-100 text-cyan-600'
                    }`}>
                      {activity.type === 'user_registration' && <UserPlus size={16} />}
                      {activity.type === 'subscription' && <CreditCard size={16} />}
                      {activity.type === 'simulation' && <Target size={16} />}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-sm truncate">
                        {activity.type === 'user_registration' && `Nuevo usuario: ${activity.name || activity.email}`}
                        {activity.type === 'subscription' && `Suscripción ${activity.plan}: ${activity.name || activity.email}`}
                        {activity.type === 'simulation' && `Simulacro: ${activity.course || 'N/A'}`}
                      </p>
                      <p className="text-xs text-slate-400">
                        {activity.timestamp ? new Date(activity.timestamp).toLocaleString('es-CL') : ''}
                      </p>
                    </div>
                    {activity.type === 'simulation' && activity.grade && (
                      <Badge variant={activity.grade >= 4 ? 'default' : 'destructive'}>
                        {activity.grade.toFixed(1)}
                      </Badge>
                    )}
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Conversion Stats */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp size={20} className="text-green-500" />
            Métricas de Conversión
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="text-center p-4 bg-slate-50 rounded-xl">
              <p className="text-3xl font-bold text-cyan-600">{metrics.subscriptions.conversion_rate}%</p>
              <p className="text-sm text-slate-500 mt-1">Tasa de conversión</p>
              <p className="text-xs text-slate-400">Usuarios → Suscriptores</p>
            </div>
            <div className="text-center p-4 bg-slate-50 rounded-xl">
              <p className="text-3xl font-bold text-purple-600">{metrics.users.trial_active}</p>
              <p className="text-sm text-slate-500 mt-1">En prueba gratuita</p>
              <p className="text-xs text-slate-400">Trial activo</p>
            </div>
            <div className="text-center p-4 bg-slate-50 rounded-xl">
              <p className="text-3xl font-bold text-green-600">{formatCLP(metrics.revenue.mrr)}</p>
              <p className="text-sm text-slate-500 mt-1">MRR</p>
              <p className="text-xs text-slate-400">Ingresos recurrentes</p>
            </div>
            <div className="text-center p-4 bg-slate-50 rounded-xl">
              <p className="text-3xl font-bold text-blue-600">
                {metrics.users.total > 0 ? (metrics.simulations.total / metrics.users.total).toFixed(1) : 0}
              </p>
              <p className="text-sm text-slate-500 mt-1">Simulacros/Usuario</p>
              <p className="text-xs text-slate-400">Engagement promedio</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default AdminDashboard;
