import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { LayoutDashboard, BookOpen, ClipboardList, Users, LogOut, DollarSign, Building2, Moon, Sun } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';
import { useTheme } from '../contexts/ThemeContext';

const AdminLayout = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { isDark, toggleTheme } = useTheme();

  const navItems = [
    { icon: LayoutDashboard, label: 'Dashboard', path: '/admin/dashboard' },
    { icon: BookOpen, label: 'Cursos', path: '/admin/courses' },
    { icon: ClipboardList, label: 'Preguntas', path: '/admin/questions' },
    { icon: Building2, label: 'Universidades', path: '/admin/universities' },
    { icon: Users, label: 'Usuarios', path: '/admin/users' },
    { icon: DollarSign, label: 'Precios', path: '/admin/pricing' },
  ];

  const handleLogout = () => {
    localStorage.removeItem('admin_token');
    toast.success('Sesión cerrada');
    navigate('/admin/login');
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Sidebar */}
      <aside className="fixed left-0 top-0 h-screen w-64 bg-slate-900 dark:bg-slate-950 text-white p-6">
        <div className="mb-8 flex items-center gap-3">
          <img 
            src="/remy-logo.png" 
            alt="Remy" 
            className="w-12 h-12 object-contain"
          />
          <div>
            <h1 className="text-xl font-bold">Remy Admin</h1>
            <p className="text-xs text-slate-400">Panel de administración</p>
          </div>
        </div>
        <nav className="flex-1 space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <button
                key={item.path}
                onClick={() => navigate(item.path)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                  isActive
                    ? 'bg-primary text-white'
                    : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                }`}
              >
                <Icon size={20} />
                <span className="font-medium">{item.label}</span>
              </button>
            );
          })}
        </nav>
        
        {/* Theme toggle */}
        <div className="mt-4 pt-4 border-t border-slate-700">
          <button
            onClick={toggleTheme}
            data-testid="admin-theme-toggle"
            className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition-all"
          >
            {isDark ? <Sun size={20} /> : <Moon size={20} />}
            <span className="font-medium">{isDark ? 'Modo claro' : 'Modo oscuro'}</span>
          </button>
        </div>
        
        <Button
          variant="ghost"
          className="w-full mt-4 text-slate-300 hover:text-white hover:bg-slate-800"
          onClick={handleLogout}
        >
          <LogOut size={20} className="mr-2" />
          Cerrar sesión
        </Button>
      </aside>

      {/* Main Content */}
      <main className="ml-64 min-h-screen p-8">
        <Outlet />
      </main>
    </div>
  );
};

export default AdminLayout;
