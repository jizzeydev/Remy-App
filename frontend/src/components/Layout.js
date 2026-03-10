import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { Home, ClipboardCheck, BookOpen, TrendingUp, Menu, LogOut, User, Crown, CreditCard } from 'lucide-react';
import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import { Badge } from '@/components/ui/badge';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

const Layout = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout, hasActiveSubscription } = useAuth();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navItems = [
    { icon: Home, label: 'Inicio', path: '/dashboard' },
    { icon: ClipboardCheck, label: 'Simulacros', path: '/simulacros' },
    { icon: BookOpen, label: 'Biblioteca', path: '/biblioteca' },
    { icon: TrendingUp, label: 'Progreso', path: '/progreso' },
  ];

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  const NavContent = () => (
    <div className="flex flex-col gap-2">
      {navItems.map((item) => {
        const Icon = item.icon;
        const isActive = location.pathname === item.path;
        return (
          <button
            key={item.path}
            onClick={() => {
              navigate(item.path);
              setIsMobileMenuOpen(false);
            }}
            data-testid={`nav-${item.label.toLowerCase().replace(' ', '-')}`}
            className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
              isActive
                ? 'bg-primary text-white shadow-[0_4px_14px_rgba(0,188,212,0.3)]'
                : 'text-slate-600 hover:bg-secondary hover:text-primary'
            }`}
          >
            <Icon size={20} />
            <span className="font-medium">{item.label}</span>
          </button>
        );
      })}
    </div>
  );

  const UserMenu = ({ className = "" }) => (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <button className={`flex items-center gap-3 p-3 rounded-xl hover:bg-slate-50 transition-colors w-full ${className}`}>
          {user?.picture ? (
            <img src={user.picture} alt={user.name} className="w-10 h-10 rounded-full" />
          ) : (
            <div className="w-10 h-10 rounded-full bg-cyan-100 flex items-center justify-center text-cyan-700 font-semibold">
              {user?.name?.charAt(0)?.toUpperCase() || 'U'}
            </div>
          )}
          <div className="flex-1 text-left">
            <p className="font-medium text-sm text-slate-900 truncate">{user?.name || 'Usuario'}</p>
            <div className="flex items-center gap-1">
              {hasActiveSubscription() ? (
                <Badge className="bg-green-100 text-green-700 text-xs py-0">
                  <Crown size={10} className="mr-1" />
                  Premium
                </Badge>
              ) : (
                <Badge variant="secondary" className="text-xs py-0">Free</Badge>
              )}
            </div>
          </div>
        </button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-56">
        <DropdownMenuLabel>
          <div>
            <p className="font-medium">{user?.name}</p>
            <p className="text-xs text-slate-500 truncate">{user?.email}</p>
          </div>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={() => navigate('/mi-suscripcion')}>
          <CreditCard size={16} className="mr-2" />
          Mi Suscripción
        </DropdownMenuItem>
        {!hasActiveSubscription() && (
          <DropdownMenuItem onClick={() => navigate('/subscribe')} className="text-cyan-600">
            <Crown size={16} className="mr-2" />
            Suscribirse
          </DropdownMenuItem>
        )}
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={handleLogout} className="text-red-600">
          <LogOut size={16} className="mr-2" />
          Cerrar sesión
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-cyan-50/30">
      <aside className="hidden lg:fixed lg:left-0 lg:top-0 lg:h-screen lg:w-64 lg:flex lg:flex-col lg:border-r lg:border-slate-100 lg:bg-white lg:p-6">
        <div className="mb-8 flex items-center gap-3">
          <img 
            src="/remy-logo.png" 
            alt="Remy" 
            className="w-12 h-12 object-contain"
          />
          <div>
            <h1 className="text-2xl font-bold text-primary" data-testid="app-logo">Remy</h1>
            <p className="text-xs text-slate-500">Tu plataforma de estudio</p>
          </div>
        </div>
        <nav className="flex-1">
          <NavContent />
        </nav>
        
        {/* User info at bottom of sidebar */}
        <div className="border-t border-slate-100 pt-4 mt-4">
          <UserMenu />
        </div>
      </aside>

      <header className="lg:hidden sticky top-0 z-50 bg-white border-b border-slate-100 px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <img 
            src="/remy-logo.png" 
            alt="Remy" 
            className="w-10 h-10 object-contain"
          />
          <div>
            <h1 className="text-xl font-bold text-primary" data-testid="app-logo-mobile">Remy</h1>
            <p className="text-xs text-slate-500">Tu plataforma de estudio</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <UserMenu className="p-2" />
          <Sheet open={isMobileMenuOpen} onOpenChange={setIsMobileMenuOpen}>
            <SheetTrigger asChild>
              <Button variant="ghost" size="icon" data-testid="mobile-menu-button">
                <Menu className="h-6 w-6" />
              </Button>
            </SheetTrigger>
            <SheetContent side="left" className="w-64">
              <div className="mb-6">
                <h2 className="text-xl font-bold text-primary">Menú</h2>
              </div>
              <nav>
                <NavContent />
              </nav>
            </SheetContent>
          </Sheet>
        </div>
      </header>

      <main className="lg:ml-64 min-h-screen pb-20 lg:pb-0">
        <div className="max-w-7xl mx-auto p-4 sm:p-6 lg:p-8">
          <Outlet />
        </div>
      </main>

      <nav className="lg:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-slate-100 px-2 py-2 flex items-center justify-around z-50">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          return (
            <button
              key={item.path}
              onClick={() => navigate(item.path)}
              data-testid={`mobile-nav-${item.label.toLowerCase().replace(' ', '-')}`}
              className={`flex flex-col items-center gap-1 px-3 py-2 rounded-lg transition-colors min-w-[44px] ${
                isActive ? 'text-primary' : 'text-slate-500'
              }`}
            >
              <Icon size={20} />
              <span className="text-xs font-medium">{item.label.split(' ')[0]}</span>
            </button>
          );
        })}
      </nav>
    </div>
  );
};

export default Layout;
