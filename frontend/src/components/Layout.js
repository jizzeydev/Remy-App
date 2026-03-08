import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { Home, ClipboardCheck, BookOpen, Calculator, TrendingUp, Menu } from 'lucide-react';
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';

const Layout = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navItems = [
    { icon: Home, label: 'Inicio', path: '/dashboard' },
    { icon: ClipboardCheck, label: 'Simulacros', path: '/simulacros' },
    { icon: BookOpen, label: 'Biblioteca', path: '/biblioteca' },
    { icon: Calculator, label: 'Fórmulas', path: '/formulas' },
    { icon: TrendingUp, label: 'Progreso', path: '/progreso' },
  ];

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

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-cyan-50/30">
      <aside className="hidden lg:fixed lg:left-0 lg:top-0 lg:h-screen lg:w-64 lg:flex lg:flex-col lg:border-r lg:border-slate-100 lg:bg-white lg:p-6">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-primary" data-testid="app-logo">Remy</h1>
          <p className="text-sm text-slate-500">Tu plataforma de estudio</p>
        </div>
        <nav className="flex-1">
          <NavContent />
        </nav>
      </aside>

      <header className="lg:hidden sticky top-0 z-50 bg-white border-b border-slate-100 px-4 py-3 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-primary" data-testid="app-logo-mobile">Remy</h1>
          <p className="text-xs text-slate-500">Tu plataforma de estudio</p>
        </div>
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
      </header>

      <main className="lg:ml-64 min-h-screen">
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
