import { useEffect, useRef, useState } from 'react';

const DesmosEmbed = ({ equation, height = 350 }) => {
  const calculatorRef = useRef(null);
  const containerRef = useRef(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!containerRef.current || !equation) return;

    const loadDesmos = () => {
      // Load Desmos API if not already loaded
      if (!window.Desmos) {
        const script = document.createElement('script');
        script.src = 'https://www.desmos.com/api/v1.9/calculator.js?apiKey=dcb31709b452b1cf9dc26972add0fda6';
        script.async = true;
        script.onload = initCalculator;
        script.onerror = () => setError('Error cargando Desmos');
        document.body.appendChild(script);
      } else {
        initCalculator();
      }
    };

    function initCalculator() {
      try {
        if (calculatorRef.current) {
          calculatorRef.current.destroy();
        }

        const calculator = window.Desmos.GraphingCalculator(containerRef.current, {
          keypad: false,
          expressions: true,
          settingsMenu: false,
          zoomButtons: true,
          lockViewport: false,
          expressionsTopbar: false,
          border: false,
          autosize: true
        });

        calculatorRef.current = calculator;

        // Convert equation to Desmos-compatible LaTeX
        let latexEquation = equation.trim();
        
        // Handle common formats
        // Convert "y = expression" format
        if (latexEquation.startsWith('y')) {
          // Already in correct format
        } else if (latexEquation.includes('=')) {
          // Already has equals sign
        } else {
          // Assume it's just an expression, make it y = expression
          latexEquation = `y = ${latexEquation}`;
        }

        // Split by semicolon for multiple equations
        const equations = latexEquation.split(';').map(eq => eq.trim()).filter(eq => eq);
        
        const colors = ['#00BCD4', '#FF5722', '#4CAF50', '#9C27B0', '#FF9800'];
        
        equations.forEach((eq, index) => {
          calculator.setExpression({
            id: `graph-${index}`,
            latex: eq,
            color: colors[index % colors.length]
          });
        });

        // Auto-fit the viewport after a short delay
        setTimeout(() => {
          if (calculatorRef.current) {
            calculatorRef.current.setMathBounds({
              left: -10,
              right: 10,
              bottom: -6,
              top: 6
            });
          }
        }, 100);

        setError(null);
      } catch (err) {
        console.error('Desmos error:', err);
        setError(`Error: ${err.message}`);
      }
    }

    loadDesmos();

    return () => {
      if (calculatorRef.current) {
        try {
          calculatorRef.current.destroy();
        } catch (e) {
          // Ignore cleanup errors
        }
      }
    };
  }, [equation]);

  if (!equation) return null;

  return (
    <div className="my-6">
      <div className="bg-slate-50 rounded-lg p-3 border border-slate-200">
        <div className="flex items-center gap-2 mb-2 text-sm text-slate-600">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <span className="font-medium">Gráfico Interactivo</span>
          <span className="text-xs bg-cyan-100 text-cyan-700 px-2 py-0.5 rounded">Desmos</span>
        </div>
        
        {error ? (
          <div className="text-red-500 text-sm p-4 bg-red-50 rounded">
            {error}
          </div>
        ) : (
          <div 
            ref={containerRef} 
            style={{ width: '100%', height: `${height}px` }}
            className="rounded-lg overflow-hidden bg-white"
          />
        )}
        
        <div className="mt-2 text-xs text-slate-500 flex items-center gap-1">
          <span>Ecuación:</span>
          <code className="bg-slate-200 px-2 py-0.5 rounded font-mono">{equation}</code>
        </div>
      </div>
    </div>
  );
};

export default DesmosEmbed;
