import { useEffect, useRef, useState } from 'react';

const GeoGebraEmbed = ({ config, height = 450 }) => {
  const containerRef = useRef(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const appletId = useRef(`ggb-${Math.random().toString(36).substr(2, 9)}`);

  useEffect(() => {
    if (!containerRef.current || !config) return;

    let mounted = true;

    const loadGeoGebra = () => {
      if (!window.GGBApplet) {
        const script = document.createElement('script');
        script.src = 'https://www.geogebra.org/apps/deployggb.js';
        script.async = true;
        script.onload = () => mounted && initGeoGebra();
        script.onerror = () => {
          if (mounted) {
            setError('Error cargando GeoGebra');
            setLoading(false);
          }
        };
        document.body.appendChild(script);
      } else {
        initGeoGebra();
      }
    };

    function initGeoGebra() {
      if (!mounted) return;
      
      try {
        // Determine app type based on commands
        const hasAdvancedCommands = /Tangent|Derivative|Integral|Polygon|Circle|Line|Segment|Vector|Point/i.test(config);
        const hasFunction = /[a-z]\s*\([a-z]\)\s*=/i.test(config);
        
        // Use 'classic' for advanced commands, 'graphing' for simple
        const appName = (hasAdvancedCommands || hasFunction) ? 'classic' : 'graphing';
        
        const params = {
          id: appletId.current,
          width: containerRef.current.offsetWidth || 700,
          height: height,
          showToolBar: false,
          showAlgebraInput: true,
          showMenuBar: false,
          enableRightClick: true,
          enableShiftDragZoom: true,
          showResetIcon: true,
          language: 'es',
          borderColor: '#e2e8f0',
          appName: appName,
          showAlgebraInput: false,
          algebraInputPosition: 'bottom',
          preventFocus: true,
          appletOnLoad: function() {
            if (!mounted) return;
            
            const app = window[appletId.current];
            if (app) {
              // Split commands by semicolon and execute each
              const commands = config.split(';').map(c => c.trim()).filter(c => c);
              
              commands.forEach((cmd, index) => {
                try {
                  // Small delay between commands for stability
                  setTimeout(() => {
                    if (window[appletId.current]) {
                      window[appletId.current].evalCommand(cmd);
                    }
                  }, index * 100);
                } catch (e) {
                  console.warn('GeoGebra command error:', cmd, e);
                }
              });
              
              // Zoom to fit after all commands
              setTimeout(() => {
                if (window[appletId.current]) {
                  try {
                    window[appletId.current].setCoordSystem(-5, 5, -3, 5);
                  } catch (e) {}
                }
              }, commands.length * 100 + 200);
            }
            setLoading(false);
          }
        };

        const applet = new window.GGBApplet(params, true);
        applet.inject(containerRef.current);
        setError(null);
        
        // Fallback timeout in case onLoad doesn't fire
        setTimeout(() => {
          if (mounted) setLoading(false);
        }, 5000);
        
      } catch (err) {
        console.error('GeoGebra error:', err);
        if (mounted) {
          setError(`Error: ${err.message}`);
          setLoading(false);
        }
      }
    }

    loadGeoGebra();

    return () => {
      mounted = false;
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
      <div className="bg-slate-50 rounded-lg p-3 border border-slate-200 shadow-sm">
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
              <div className="flex items-center justify-center py-12 bg-white rounded-lg">
                <div className="flex flex-col items-center gap-3">
                  <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-500"></div>
                  <span className="text-slate-500 text-sm">Cargando GeoGebra...</span>
                </div>
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
          💡 Arrastra los puntos para explorar. Click derecho para más opciones.
        </div>
      </div>
    </div>
  );
};

export default GeoGebraEmbed;
