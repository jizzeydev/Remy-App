import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Toaster } from '@/components/ui/sonner';
import Layout from './components/Layout';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Chat from './pages/Chat';
import Simulacros from './pages/Simulacros';
import Biblioteca from './pages/Biblioteca';
import Formulas from './pages/Formulas';
import Progreso from './pages/Progreso';
import '@/App.css';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route element={<Layout />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/chat" element={<Chat />} />
            <Route path="/simulacros" element={<Simulacros />} />
            <Route path="/biblioteca" element={<Biblioteca />} />
            <Route path="/formulas" element={<Formulas />} />
            <Route path="/progreso" element={<Progreso />} />
          </Route>
        </Routes>
      </BrowserRouter>
      <Toaster richColors position="top-right" />
    </div>
  );
}

export default App;
