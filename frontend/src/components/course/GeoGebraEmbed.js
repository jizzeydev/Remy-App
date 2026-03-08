import { useEffect, useRef, useState } from 'react';

const GeoGebraEmbed = ({ config, height = 400 }) => {
  const containerRef = useRef(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const appletId = useRef(`ggb-${Math.random().toString(36).substr(2, 9)}`);

  useEffect(() => {
    if (!containerRef.current || !config) return;

    const loadGeoGebra = () => {
      // Load GeoGebra API if not already loaded
      if (!window.GGBApplet) {
        const script = document.createElement('script');
        script.src = 'https://www.geogebra.org/apps/deployggb.js';
        script.async = true;
        script.onload = initGeoGebra;
        script.onerror = () => {
          setError('Error cargando GeoGebra');
          setLoading(false);
        };
        document.body.appendChild(script);
      } else {
        initGeoGebra();
      }
    };

    function initGeoGebra() {
      try {
        // Parse config - can be material ID, commands, or JSON config
        let params = {
          id: appletId.current,
          width: containerRef.current.offsetWidth || 700,
          height: height,
          showToolBar: false,
          showAlgebraInput: false,
          showMenuBar: false,
          enableRightClick: false,
          enableShiftDragZoom: true,
          showResetIcon: true,
          language: 'es',
          borderColor: '#e2e8f0',
          preventFocus: true,
        };

        // Check if config is a material ID (like "abc123")
        if (/^[a-zA-Z0-9]+$/.test(config) && config.length < 20) {
          params.material_id = config;
        } 
        // Check if config is GeoGebra commands
        else if (config.includes('=') || config.includes('(')) {
          params.appName = 'graphing';
          params.appletOnLoad = function() {
            const app = window[appletId.current];
            if (app) {
              // Split by semicolon and execute each command
              const commands = config.split(';').map(c => c.trim()).filter(c => c);
              commands.forEach(cmd => {
                try {
                  app.evalCommand(cmd);
                } catch (e) {
                  console.warn('GeoGebra command error:', cmd, e);
                }
              });
            }
          };
        }

        const applet = new window.GGBApplet(params, true);
        applet.inject(containerRef.current);
        setLoading(false);
        setError(null);
      } catch (err) {
        console.error('GeoGebra error:', err);
        setError(`Error: ${err.message}`);
        setLoading(false);
      }
    }

    loadGeoGebra();

    return () => {
      // Cleanup
      if (window[appletId.current]) {
        try {
          window[appletId.current] = null;
        } catch (e) {}
      }
    };
  }, [config, height]);

  if (!config) return null;

  return (
    <div className="my-6">
      <div className="bg-slate-50 rounded-lg p-3 border border-slate-200">
        <div className="flex items-center gap-2 mb-2 text-sm text-slate-600">
          <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="12" r="10" strokeWidth="2"/>
            <path d="M12 6v6l4 2" strokeWidth="2" strokeLinecap="round"/>
          </svg>
          <span className="font-medium">Geometría Interactiva</span>
          <span className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded">GeoGebra</span>
        </div>
        
        {error ? (
          <div className="text-red-500 text-sm p-4 bg-red-50 rounded">
            {error}
          </div>
        ) : (
          <>
            {loading && (
              <div className="flex items-center justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
              </div>
            )}
            <div 
              ref={containerRef}
              style={{ width: '100%', minHeight: `${height}px` }}
              className={`rounded-lg overflow-hidden bg-white ${loading ? 'hidden' : ''}`}
            />
          </>
        )}
        
        <div className="mt-2 text-xs text-slate-500">
          <span>💡 Tip: Arrastra los puntos para explorar la figura</span>
        </div>
      </div>
    </div>
  );
};

export default GeoGebraEmbed;
