import { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import { toast } from 'sonner';
import { Settings, School, Loader2 } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/admin`;

const AdminSettings = () => {
  const [settings, setSettings] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.get(`${API}/settings`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setSettings(response.data);
    } catch (error) {
      console.error('Error fetching settings:', error);
      toast.error('Error al cargar configuración');
    } finally {
      setLoading(false);
    }
  };

  const updateSetting = async (key, value) => {
    setSaving(true);
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.put(
        `${API}/settings`,
        { [key]: value },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setSettings(response.data.settings);
      toast.success('Configuración guardada');
    } catch (error) {
      console.error('Error updating settings:', error);
      toast.error('Error al guardar configuración');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="animate-spin" size={32} />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Configuración</h1>
        <p className="text-slate-600 dark:text-slate-400">
          Ajustes generales de la aplicación
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Settings size={20} />
            Funcionalidades
          </CardTitle>
          <CardDescription>
            Activa o desactiva funcionalidades de la aplicación
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Tu Universidad Toggle */}
          <div className="flex items-center justify-between p-4 border rounded-lg">
            <div className="flex items-start gap-4">
              <div className="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
                <School className="text-blue-600" size={24} />
              </div>
              <div>
                <Label htmlFor="tu-universidad" className="text-base font-medium">
                  Tu Universidad (Banco de Exámenes)
                </Label>
                <p className="text-sm text-slate-500 mt-1">
                  Permite a los estudiantes practicar con exámenes específicos de su universidad.
                  Esta función está actualmente en desarrollo.
                </p>
              </div>
            </div>
            <Switch
              id="tu-universidad"
              checked={settings?.tu_universidad_enabled || false}
              onCheckedChange={(checked) => updateSetting('tu_universidad_enabled', checked)}
              disabled={saving}
              data-testid="toggle-tu-universidad"
            />
          </div>

          <p className="text-xs text-slate-400 text-center">
            Los cambios se aplican inmediatamente
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

export default AdminSettings;
