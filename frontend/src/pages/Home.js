import { useNavigate } from 'react-router-dom';
import { ClipboardCheck, BookOpen, Calculator, TrendingUp, Zap, GraduationCap, Target } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { motion } from 'framer-motion';

const Home = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: ClipboardCheck,
      title: 'Simulacros de Prueba',
      description: 'Practica con exámenes reales antes de la prueba. Si apruebas el simulacro, vas a aprobar el examen.',
      color: 'from-blue-400 to-blue-600',
    },
    {
      icon: BookOpen,
      title: 'Lecciones que se Entienden',
      description: 'Cursos completos explicados de forma clara. Por fin vas a entender la materia, no solo memorizarla.',
      color: 'from-purple-400 to-purple-600',
    },
    {
      icon: GraduationCap,
      title: 'Preguntas por Universidad',
      description: 'Banco de preguntas tipo examen de tu universidad y curso. Practica con lo que de verdad te van a tomar.',
      color: 'from-cyan-400 to-cyan-600',
    },
    {
      icon: Calculator,
      title: 'Formulario',
      description: 'Encuentra la fórmula exacta en segundos. Todas las fórmulas organizadas por curso y tema.',
      color: 'from-emerald-400 to-emerald-600',
    },
    {
      icon: TrendingUp,
      title: 'Tu Progreso en Tiempo Real',
      description: 'Notas de simulacro, lecciones completadas y puntos débiles. Sabrás exactamente qué repasar.',
      color: 'from-amber-400 to-amber-600',
    },
    {
      icon: Target,
      title: 'Tu Escritorio de Estudio',
      description: 'Cursos, simulacros, fórmulas y progreso. Todo conectado para que no pierdas tiempo buscando material.',
      color: 'from-rose-400 to-rose-600',
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-background via-primary/5 to-background">
      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center"
          >
            <div className="inline-block mb-4 px-4 py-2 bg-secondary rounded-full">
              <span className="text-primary font-semibold flex items-center gap-2">
                <Zap size={16} />
                Nueva plataforma
              </span>
            </div>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight mb-6 text-foreground">
              Domina ciencias y
              <span className="block text-primary mt-2">matemáticas sin estrés</span>
            </h1>
            <p className="text-lg sm:text-xl text-muted-foreground max-w-3xl mx-auto mb-8 leading-relaxed">
              Remy es tu plataforma de estudio para ramos universitarios. Lecciones claras, simulacros con preguntas reales por universidad y seguimiento de progreso — todo en un solo lugar.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Button
                onClick={() => navigate('/dashboard')}
                data-testid="get-started-button"
                className="px-8 py-6 text-lg rounded-full bg-primary hover:bg-primary/90 shadow-[0_4px_14px_rgba(0,188,212,0.3)] transition-all hover:shadow-[0_6px_20px_rgba(0,188,212,0.4)]"
              >
                <GraduationCap className="mr-2" size={20} />
                Comenzar ahora
              </Button>
              <Button
                variant="outline"
                onClick={() => window.open('https://seremonta.store', '_blank')}
                data-testid="learn-more-button"
                className="px-8 py-6 text-lg rounded-full border-2 border-primary text-primary hover:bg-secondary"
              >
                Ver cómo funciona
              </Button>
            </div>
          </motion.div>

          {/* Hero Image/Illustration */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="mt-16 relative"
          >
            <div className="relative mx-auto max-w-4xl">
              <div className="absolute inset-0 bg-gradient-to-r from-primary/20 to-blue-500/20 blur-3xl rounded-full"></div>
              <img
                src="https://images.unsplash.com/photo-1758521541622-d1e6be8c39bb"
                alt="Estudiante usando Remy"
                className="relative rounded-2xl shadow-2xl w-full"
                data-testid="hero-image"
              />
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-card">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4 text-foreground">
              ¿Por qué elegir Remy?
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Una herramienta suprema para la educación. Todo lo que necesitas para dominar tus ramos.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  viewport={{ once: true }}
                  data-testid={`feature-card-${index}`}
                  className="bg-card border border-border rounded-2xl p-6 hover:shadow-[0_8px_24px_rgba(0,188,212,0.15)] transition-all duration-300 hover:-translate-y-1"
                >
                  <div className={`inline-flex p-3 rounded-xl bg-gradient-to-br ${feature.color} mb-4`}>
                    <Icon className="text-white" size={24} />
                  </div>
                  <h3 className="text-xl font-semibold mb-3 text-foreground">{feature.title}</h3>
                  <p className="text-muted-foreground leading-relaxed">{feature.description}</p>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-primary to-blue-500">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-6">
            Comienza a estudiar de forma inteligente
          </h2>
          <p className="text-xl text-white/80 mb-8">
            Únete a más de 1,000 estudiantes que ya están mejorando sus calificaciones con Remy.
          </p>
          <Button
            onClick={() => navigate('/dashboard')}
            data-testid="cta-button"
            className="px-8 py-6 text-lg rounded-full bg-white text-primary hover:bg-white/90 shadow-xl"
          >
            Empezar gratis
          </Button>
        </div>
      </section>
    </div>
  );
};

export default Home;
