import { useNavigate } from 'react-router-dom';
import { Smartphone, ArrowLeft, Globe } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';

/**
 * Pantalla mostrada en lugar de SubscribePage cuando el usuario está
 * dentro de la app móvil nativa.
 *
 * Por qué existe: hasta que integremos Google Play Billing (F2), no
 * podemos cobrar por Mercado Pago dentro de la app sin violar la política
 * 4.5 de Google Play (Payments). Tampoco queremos abrir un browser embed
 * a Mercado Pago — eso suele dar fricción y los stores lo desaconsejan.
 *
 * Mientras tanto, mostramos esta pantalla. Cuando IAP esté integrado,
 * App.js deja de redirigir acá y SubscribePage detecta la plataforma
 * para usar Play Billing en Android y StoreKit en iOS.
 */
export default function MobileSubscribeBlock() {
  const navigate = useNavigate();

  return (
    <div className="min-h-[70vh] flex items-center justify-center px-4">
      <Card className="max-w-md w-full">
        <CardContent className="p-8 text-center space-y-5">
          <div className="mx-auto h-16 w-16 rounded-full bg-primary/10 flex items-center justify-center">
            <Smartphone className="text-primary" size={32} />
          </div>
          <div>
            <h2 className="text-2xl font-bold mb-2">Suscripción próximamente</h2>
            <p className="text-muted-foreground">
              Estamos integrando los pagos dentro de la app. Mientras tanto,
              suscríbete desde la web — tu cuenta se sincroniza automáticamente
              con la app y vas a poder seguir desde donde lo dejaste.
            </p>
          </div>
          <div className="flex flex-col gap-2">
            <Button
              size="lg"
              className="w-full"
              onClick={() => {
                // Abrimos la web en el browser del sistema, no en la WebView,
                // para que el alumno pueda completar el flujo MP sin problemas
                // de cookies / ventana emergente.
                window.open('https://remy.seremonta.store/subscribe', '_system');
              }}
              data-testid="mobile-subscribe-open-web"
            >
              <Globe className="mr-2" size={18} />
              Abrir web para suscribirte
            </Button>
            <Button
              variant="ghost"
              onClick={() => navigate(-1)}
              data-testid="mobile-subscribe-back"
            >
              <ArrowLeft className="mr-2" size={18} />
              Volver
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
