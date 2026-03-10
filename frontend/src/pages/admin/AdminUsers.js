/**
 * Admin Users Management Page
 * Allows admin to view and manage user subscriptions
 */
import { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  Users, Search, UserPlus, CheckCircle, XCircle, 
  Clock, CreditCard, Gift, ChevronLeft, ChevronRight,
  TrendingUp, Mail, Calendar, MoreVertical
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Label } from '@/components/ui/label';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter,
} from '@/components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AdminUsers = () => {
  const [users, setUsers] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  
  // Grant access dialog
  const [grantDialogOpen, setGrantDialogOpen] = useState(false);
  const [grantEmail, setGrantEmail] = useState('');
  const [grantName, setGrantName] = useState('');
  const [grantDuration, setGrantDuration] = useState('1');
  const [grantLoading, setGrantLoading] = useState(false);

  const getAuthHeader = () => ({
    headers: {
      Authorization: `Bearer ${localStorage.getItem('admin_token')}`
    }
  });

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API}/admin/users/stats`, getAuthHeader());
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({
        page: page.toString(),
        limit: '20'
      });
      
      if (search) params.append('search', search);
      if (statusFilter && statusFilter !== 'all') params.append('status_filter', statusFilter);
      
      const response = await axios.get(
        `${API}/admin/users?${params.toString()}`,
        getAuthHeader()
      );
      
      setUsers(response.data.users);
      setTotalPages(response.data.pages);
    } catch (error) {
      console.error('Error fetching users:', error);
      toast.error('Error al cargar usuarios');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  useEffect(() => {
    fetchUsers();
  }, [page, statusFilter]);

  const handleSearch = (e) => {
    e.preventDefault();
    setPage(1);
    fetchUsers();
  };

  const handleGrantAccess = async () => {
    if (!grantEmail) {
      toast.error('Email requerido');
      return;
    }
    
    setGrantLoading(true);
    try {
      const response = await axios.post(
        `${API}/admin/users/grant-access`,
        {
          email: grantEmail,
          name: grantName || undefined,
          duration_months: parseInt(grantDuration)
        },
        getAuthHeader()
      );
      
      toast.success(response.data.message);
      setGrantDialogOpen(false);
      setGrantEmail('');
      setGrantName('');
      setGrantDuration('1');
      fetchUsers();
      fetchStats();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Error al otorgar acceso');
    } finally {
      setGrantLoading(false);
    }
  };

  const handleRevokeAccess = async (userId, email) => {
    if (!confirm(`¿Revocar acceso de ${email}?`)) return;
    
    try {
      await axios.post(
        `${API}/admin/users/${userId}/revoke-access`,
        {},
        getAuthHeader()
      );
      
      toast.success('Acceso revocado');
      fetchUsers();
      fetchStats();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Error al revocar acceso');
    }
  };

  const handleExtendAccess = async (userId, months = 1) => {
    try {
      const response = await axios.post(
        `${API}/admin/users/${userId}/extend-access?months=${months}`,
        {},
        getAuthHeader()
      );
      
      toast.success(response.data.message);
      fetchUsers();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Error al extender acceso');
    }
  };

  const getStatusBadge = (status) => {
    const badges = {
      active: <Badge className="bg-green-100 text-green-700">Activo</Badge>,
      inactive: <Badge variant="secondary">Inactivo</Badge>,
      cancelled: <Badge variant="destructive">Cancelado</Badge>,
      expired: <Badge className="bg-orange-100 text-orange-700">Expirado</Badge>,
      pending: <Badge className="bg-yellow-100 text-yellow-700">Pendiente</Badge>
    };
    return badges[status] || <Badge variant="secondary">{status}</Badge>;
  };

  const getTypeBadge = (type) => {
    if (type === 'mercadopago') {
      return <Badge variant="outline" className="text-blue-600"><CreditCard size={12} className="mr-1" />MP</Badge>;
    }
    if (type === 'manual') {
      return <Badge variant="outline" className="text-purple-600"><Gift size={12} className="mr-1" />Manual</Badge>;
    }
    return null;
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return '-';
    try {
      return new Date(dateStr).toLocaleDateString('es-CL', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      });
    } catch {
      return '-';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Gestión de Usuarios</h1>
          <p className="text-slate-500 mt-1">Administra usuarios y suscripciones</p>
        </div>
        
        <Dialog open={grantDialogOpen} onOpenChange={setGrantDialogOpen}>
          <DialogTrigger asChild>
            <Button className="bg-cyan-500 hover:bg-cyan-600">
              <UserPlus className="mr-2" size={18} />
              Otorgar Acceso
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Otorgar Acceso Manual</DialogTitle>
              <DialogDescription>
                Otorga acceso gratuito a un estudiante por un período determinado.
              </DialogDescription>
            </DialogHeader>
            
            <div className="space-y-4 py-4">
              <div className="space-y-2">
                <Label htmlFor="grant-email">Email del estudiante *</Label>
                <Input
                  id="grant-email"
                  type="email"
                  placeholder="estudiante@email.com"
                  value={grantEmail}
                  onChange={(e) => setGrantEmail(e.target.value)}
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="grant-name">Nombre (opcional)</Label>
                <Input
                  id="grant-name"
                  type="text"
                  placeholder="Nombre del estudiante"
                  value={grantName}
                  onChange={(e) => setGrantName(e.target.value)}
                />
                <p className="text-xs text-slate-500">
                  Si no existe, se creará una cuenta con este nombre
                </p>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="grant-duration">Duración</Label>
                <Select value={grantDuration} onValueChange={setGrantDuration}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="1">1 mes</SelectItem>
                    <SelectItem value="2">2 meses</SelectItem>
                    <SelectItem value="3">3 meses</SelectItem>
                    <SelectItem value="6">6 meses</SelectItem>
                    <SelectItem value="12">12 meses</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            
            <DialogFooter>
              <Button variant="outline" onClick={() => setGrantDialogOpen(false)}>
                Cancelar
              </Button>
              <Button 
                onClick={handleGrantAccess} 
                disabled={grantLoading}
                className="bg-cyan-500 hover:bg-cyan-600"
              >
                {grantLoading ? 'Otorgando...' : 'Otorgar Acceso'}
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-500">Total Usuarios</p>
                  <p className="text-3xl font-bold">{stats.total_users}</p>
                </div>
                <Users className="text-slate-400" size={32} />
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-500">Suscripciones Activas</p>
                  <p className="text-3xl font-bold text-green-600">{stats.subscription_stats.active}</p>
                </div>
                <CheckCircle className="text-green-500" size={32} />
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-500">Mercado Pago</p>
                  <p className="text-3xl font-bold text-blue-600">{stats.subscription_types.mercadopago}</p>
                </div>
                <CreditCard className="text-blue-500" size={32} />
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-500">Acceso Manual</p>
                  <p className="text-3xl font-bold text-purple-600">{stats.subscription_types.manual}</p>
                </div>
                <Gift className="text-purple-500" size={32} />
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Search and Filters */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-col md:flex-row gap-4">
            <form onSubmit={handleSearch} className="flex-1 flex gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                <Input
                  placeholder="Buscar por email o nombre..."
                  className="pl-10"
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                />
              </div>
              <Button type="submit" variant="secondary">Buscar</Button>
            </form>
            
            <Select value={statusFilter} onValueChange={(v) => { setStatusFilter(v); setPage(1); }}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Estado" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Todos</SelectItem>
                <SelectItem value="active">Activos</SelectItem>
                <SelectItem value="inactive">Inactivos</SelectItem>
                <SelectItem value="cancelled">Cancelados</SelectItem>
                <SelectItem value="expired">Expirados</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Users Table */}
      <Card>
        <CardContent className="p-0">
          {loading ? (
            <div className="text-center py-12">
              <div className="animate-spin w-8 h-8 border-4 border-cyan-500 border-t-transparent rounded-full mx-auto" />
            </div>
          ) : users.length === 0 ? (
            <div className="text-center py-12 text-slate-500">
              No se encontraron usuarios
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Usuario</TableHead>
                  <TableHead>Estado</TableHead>
                  <TableHead>Tipo</TableHead>
                  <TableHead>Plan</TableHead>
                  <TableHead>Vence</TableHead>
                  <TableHead>Registro</TableHead>
                  <TableHead className="text-right">Acciones</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {users.map((user) => (
                  <TableRow key={user.user_id}>
                    <TableCell>
                      <div className="flex items-center gap-3">
                        {user.picture ? (
                          <img 
                            src={user.picture} 
                            alt={user.name} 
                            className="w-8 h-8 rounded-full"
                          />
                        ) : (
                          <div className="w-8 h-8 rounded-full bg-cyan-100 flex items-center justify-center text-cyan-700 font-medium">
                            {user.name?.charAt(0)?.toUpperCase() || 'U'}
                          </div>
                        )}
                        <div>
                          <p className="font-medium">{user.name}</p>
                          <p className="text-sm text-slate-500">{user.email}</p>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>{getStatusBadge(user.subscription_status)}</TableCell>
                    <TableCell>{getTypeBadge(user.subscription_type)}</TableCell>
                    <TableCell>
                      {user.subscription_plan ? (
                        <span className="capitalize">{user.subscription_plan}</span>
                      ) : '-'}
                    </TableCell>
                    <TableCell>{formatDate(user.subscription_end)}</TableCell>
                    <TableCell>{formatDate(user.created_at)}</TableCell>
                    <TableCell className="text-right">
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" size="icon">
                            <MoreVertical size={18} />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuItem onClick={() => handleExtendAccess(user.user_id, 1)}>
                            <Clock size={16} className="mr-2" />
                            Extender 1 mes
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={() => handleExtendAccess(user.user_id, 6)}>
                            <Clock size={16} className="mr-2" />
                            Extender 6 meses
                          </DropdownMenuItem>
                          {user.subscription_type === 'manual' && user.subscription_status === 'active' && (
                            <DropdownMenuItem 
                              className="text-red-600"
                              onClick={() => handleRevokeAccess(user.user_id, user.email)}
                            >
                              <XCircle size={16} className="mr-2" />
                              Revocar Acceso
                            </DropdownMenuItem>
                          )}
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
        
        {/* Pagination */}
        {totalPages > 1 && (
          <div className="flex items-center justify-between p-4 border-t">
            <p className="text-sm text-slate-500">Página {page} de {totalPages}</p>
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={page === 1}
              >
                <ChevronLeft size={16} />
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
              >
                <ChevronRight size={16} />
              </Button>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
};

export default AdminUsers;
