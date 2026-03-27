import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { Home, ClipboardCheck, BookOpen, TrendingUp, Menu, LogOut, User, Crown, CreditCard, GraduationCap, Moon, Sun } from 'lucide-react';
import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useTheme } from '../contexts/ThemeContext';
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
  const { isDark, toggleTheme } = useTheme();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navItems = [
    { icon: Home, label: 'Inicio', path: '/dashboard' },
    { icon: ClipboardCheck, label: 'Simulacros', path: '/simulacros' },
    { icon: GraduationCap, label: 'Tu Universidad', path: '/tu-universidad' },
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
                ? 'bg-primary text-primary-foreground shadow-[0_4px_14px_rgba(0,188,212,0.3)]'
                : 'text-muted-foreground hover:bg-secondary hover:text-foreground'
            }`}
          >
            <Icon size={20} />
            <span className="font-medium">{item.label}</span>
          </button>
        );
      })}
    </div>
  );

  const ThemeToggle = () => (
    <button
      onClick={toggleTheme}
      data-testid="theme-toggle"
      className="p-2 rounded-lg hover:bg-secondary transition-colors text-muted-foreground hover:text-foreground"
      aria-label={isDark ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro'}
    >
      {isDark ? <Sun size={20} /> : <Moon size={20} />}
    </button>
  );

  const UserMenu = ({ className = "" }) => (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <button className={`flex items-center gap-3 p-3 rounded-xl hover:bg-secondary transition-colors w-full ${className}`}>
          {user?.picture ? (
            <img src={user.picture} alt={user.name} className="w-10 h-10 rounded-full" />
          ) : (
            <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center text-primary font-semibold">
              {user?.name?.charAt(0)?.toUpperCase() || 'U'}
            </div>
          )}
          <div className="flex-1 text-left">
            <p className="font-medium text-sm text-foreground truncate">{user?.name || 'Usuario'}</p>
            <div className="flex items-center gap-1">
              {hasActiveSubscription ? (
                <Badge className="bg-green-500/20 text-green-600 dark:text-green-400 text-xs py-0">
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
            <p className="text-xs text-muted-foreground truncate">{user?.email}</p>
          </div>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={() => navigate('/mi-suscripcion')}>
          <CreditCard size={16} className="mr-2" />
          Mi Suscripción
        </DropdownMenuItem>
        {!hasActiveSubscription && (
          <DropdownMenuItem onClick={() => navigate('/subscribe')} className="text-primary">
            <Crown size={16} className="mr-2" />
            Suscribirse
          </DropdownMenuItem>
        )}
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={handleLogout} className="text-destructive">
          <LogOut size={16} className="mr-2" />
          Cerrar sesión
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );

  return (
    <div className="min-h-screen bg-background">
      <aside className="hidden lg:fixed lg:left-0 lg:top-0 lg:h-screen lg:w-64 lg:flex lg:flex-col lg:border-r lg:border-border lg:bg-card lg:p-6">
        <div className="mb-8 flex items-center gap-3">
          <img 
            src="/remy-logo.png" 
            alt="Remy" 
            className="w-12 h-12 object-contain"
          />
          <div>
            <h1 className="text-2xl font-bold text-primary" data-testid="app-logo">Remy</h1>
            <p className="text-xs text-muted-foreground">Tu plataforma de estudio</p>
          </div>
        </div>
        <nav className="flex-1">
          <NavContent />
        </nav>
        
        {/* Theme toggle and user info at bottom of sidebar */}
        <div className="border-t border-border pt-4 mt-4 space-y-2">
          <div className="flex items-center justify-between px-2">
            <span className="text-sm text-muted-foreground">Tema</span>
            <ThemeToggle />
          </div>
          <UserMenu />
        </div>
      </aside>

      <header className="lg:hidden sticky top-0 z-50 bg-card border-b border-border px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <img 
            src="/remy-logo.png" 
            alt="Remy" 
            className="w-10 h-10 object-contain"
          />
          <div>
            <h1 className="text-xl font-bold text-primary" data-testid="app-logo-mobile">Remy</h1>
            <p className="text-xs text-muted-foreground">Tu plataforma de estudio</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <ThemeToggle />
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

      <nav className="lg:hidden fixed bottom-0 left-0 right-0 bg-card border-t border-border px-2 py-2 flex items-center justify-around z-50">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          return (
            <button
              key={item.path}
              onClick={() => navigate(item.path)}
              data-testid={`mobile-nav-${item.label.toLowerCase().replace(' ', '-')}`}
              className={`flex flex-col items-center gap-1 px-3 py-2 rounded-lg transition-colors min-w-[44px] ${
                isActive ? 'text-primary' : 'text-muted-foreground'
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
