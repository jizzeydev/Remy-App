/**
 * TrialCountdown — granular `Xd Yh Zm` countdown to trial_end_date.
 *
 * Renders nothing if the user has an active subscription, has no trial, or the
 * trial has already expired (the trial-expired banner handles that case).
 *
 * Ticks every 60 seconds — fine-grained enough to feel live without churning
 * React. We compute once per tick from `trial_end_date` so there's no drift
 * if the tab was backgrounded.
 */
import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Clock, Crown } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useAuth } from '../contexts/AuthContext';

const computeRemaining = (endIso) => {
  if (!endIso) return null;
  const end = new Date(endIso).getTime();
  const now = Date.now();
  const diff = end - now;
  if (diff <= 0) return { expired: true, days: 0, hours: 0, minutes: 0, totalMs: 0 };
  const days = Math.floor(diff / 86400000);
  const hours = Math.floor((diff % 86400000) / 3600000);
  const minutes = Math.floor((diff % 3600000) / 60000);
  return { expired: false, days, hours, minutes, totalMs: diff };
};

const TrialCountdown = ({ variant = 'card' }) => {
  const navigate = useNavigate();
  const { user, hasActiveSubscription } = useAuth();
  const [tick, setTick] = useState(0);

  useEffect(() => {
    const id = setInterval(() => setTick((t) => t + 1), 60_000);
    return () => clearInterval(id);
  }, []);

  const remaining = useMemo(
    () => computeRemaining(user?.trial_end_date),
    // tick is the trigger; we recompute on each interval.
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [user?.trial_end_date, tick]
  );

  if (hasActiveSubscription) return null;
  if (!user?.trial_active) return null;
  if (!remaining || remaining.expired) return null;

  const { days, hours, minutes } = remaining;
  // Visual urgency: red if <24h, amber if <3d, cyan otherwise.
  const urgent = days < 1;
  const warning = !urgent && days < 3;

  const tone = urgent
    ? 'from-red-500 to-rose-600 text-white'
    : warning
      ? 'from-amber-500 to-orange-500 text-white'
      : 'from-cyan-500 to-blue-600 text-white';

  if (variant === 'inline') {
    return (
      <span className="font-bold tabular-nums">
        {days}d {hours}h {minutes}m
      </span>
    );
  }

  return (
    <div
      className={`rounded-2xl bg-gradient-to-r ${tone} shadow-lg overflow-hidden`}
      data-testid="trial-countdown"
    >
      <div className="px-5 py-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="bg-white/20 rounded-full p-2.5">
            <Clock size={22} aria-hidden="true" />
          </div>
          <div>
            <p className="text-xs uppercase tracking-wider opacity-90">Prueba gratuita</p>
            <p className="text-2xl font-bold tabular-nums leading-tight">
              {days}d {String(hours).padStart(2, '0')}h {String(minutes).padStart(2, '0')}m
            </p>
            <p className="text-xs opacity-90">
              {urgent ? '¡Termina hoy!' : warning ? 'Está por terminar' : 'restantes para terminar tu prueba'}
            </p>
          </div>
        </div>
        <Button
          size="sm"
          onClick={() => navigate('/subscribe')}
          className="bg-white text-slate-900 hover:bg-slate-100 font-semibold rounded-full px-5"
          data-testid="trial-countdown-cta"
        >
          <Crown size={16} className="mr-1.5" />
          Suscribirme
        </Button>
      </div>
    </div>
  );
};

export default TrialCountdown;
