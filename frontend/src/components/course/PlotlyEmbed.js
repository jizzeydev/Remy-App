import { useEffect, useRef, useState } from 'react';

const PlotlyEmbed = ({ config, height = 400 }) => {
  const containerRef = useRef(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!containerRef.current || !config) return;

    const loadPlotly = async () => {
      try {
        // Dynamic import of Plotly
        const Plotly = await import('plotly.js-dist-min');
        
        // Parse the config
        let plotConfig;
        try {
          // Try to parse as JSON first
          plotConfig = JSON.parse(config);
        } catch {
          // If not JSON, treat as a simple function expression
          plotConfig = parseSimpleConfig(config);
        }

        const { data, layout, options } = plotConfig;

        // Default layout settings
        const defaultLayout = {
          autosize: true,
          height: height,
          margin: { l: 50, r: 30, t: 40, b: 50 },
          paper_bgcolor: 'rgba(0,0,0,0)',
          plot_bgcolor: 'rgba(248,250,252,1)',
          font: { family: 'Inter, system-ui, sans-serif', color: '#334155' },
          xaxis: { 
            gridcolor: '#e2e8f0',
            zerolinecolor: '#94a3b8'
          },
          yaxis: { 
            gridcolor: '#e2e8f0',
            zerolinecolor: '#94a3b8'
          },
          ...layout
        };

        const defaultOptions = {
          responsive: true,
          displayModeBar: true,
          modeBarButtonsToRemove: ['lasso2d', 'select2d'],
          displaylogo: false,
          ...options
        };

        Plotly.default.newPlot(containerRef.current, data, defaultLayout, defaultOptions);
        setError(null);
      } catch (err) {
        console.error('Plotly error:', err);
        setError(`Error renderizando gráfico: ${err.message}`);
      }
    };

    loadPlotly();

    return () => {
      if (containerRef.current) {
        import('plotly.js-dist-min').then(Plotly => {
          Plotly.default.purge(containerRef.current);
        });
      }
    };
  }, [config, height]);

  // Parse simple config strings like "scatter:x=[1,2,3];y=[1,4,9];title=Cuadrática"
  const parseSimpleConfig = (configStr) => {
    const parts = configStr.split(';').reduce((acc, part) => {
      const [key, value] = part.split('=').map(s => s.trim());
      if (key && value) {
        try {
          acc[key] = JSON.parse(value);
        } catch {
          acc[key] = value;
        }
      }
      return acc;
    }, {});

    const type = parts.type || 'scatter';
    const mode = parts.mode || (type === 'scatter' ? 'lines+markers' : undefined);
    
    return {
      data: [{
        type,
        mode,
        x: parts.x || [],
        y: parts.y || [],
        z: parts.z,
        name: parts.name || 'Serie',
        marker: { 
          color: parts.color || '#0891b2',
          size: parts.size || 8
        },
        line: {
          color: parts.lineColor || '#0891b2',
          width: parts.lineWidth || 2
        }
      }],
      layout: {
        title: parts.title || '',
        xaxis: { title: parts.xlabel || '' },
        yaxis: { title: parts.ylabel || '' }
      }
    };
  };

  if (!config) return null;

  return (
    <div className="my-6">
      <div className="bg-slate-50 rounded-lg p-3 border border-slate-200">
        <div className="flex items-center gap-2 mb-2 text-sm text-slate-600">
          <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M3 3v18h18" strokeWidth="2" strokeLinecap="round"/>
            <path d="M7 14l4-4 4 4 5-6" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          <span className="font-medium">Visualización de Datos</span>
          <span className="text-xs bg-purple-100 text-purple-700 px-2 py-0.5 rounded">Plotly</span>
        </div>
        
        {error ? (
          <div className="text-red-500 text-sm p-4 bg-red-50 rounded">
            {error}
          </div>
        ) : (
          <div 
            ref={containerRef}
            style={{ width: '100%', minHeight: `${height}px` }}
            className="rounded-lg overflow-hidden bg-white"
          />
        )}
        
        <div className="mt-2 text-xs text-slate-500">
          <span>💡 Tip: Pasa el cursor sobre los puntos para ver valores. Usa zoom con scroll.</span>
        </div>
      </div>
    </div>
  );
};

export default PlotlyEmbed;
