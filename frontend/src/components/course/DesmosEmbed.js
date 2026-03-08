import { useEffect, useRef, useState } from 'react';

const DesmosEmbed = ({ equation, height = 400 }) => {
  const calculatorRef = useRef(null);
  const containerRef = useRef(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!containerRef.current || !equation) return;

    const loadDesmos = () => {
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

        // Process equation(s) - can be single or multiple separated by semicolon
        let equations = equation
          .split(';')
          .map(eq => eq.trim())
          .filter(eq => eq.length > 0);

        const colors = ['#0891b2', '#dc2626', '#16a34a', '#9333ea', '#ea580c', '#0284c7'];
        
        equations.forEach((eq, index) => {
          // Clean up the equation
          let cleanEq = eq.trim();
          
          // Check if it's a slider definition (like "a=1" or "h=0.5")
          const sliderMatch = cleanEq.match(/^([a-z])=(-?\d*\.?\d+)$/i);
          
          if (sliderMatch) {
            // It's a slider - create with bounds
            const varName = sliderMatch[1];
            const value = parseFloat(sliderMatch[2]);
            calculator.setExpression({
              id: `expr-${index}`,
              latex: `${varName}=${value}`,
              sliderBounds: { min: -10, max: 10, step: 0.1 }
            });
          } else {
            // Regular equation
            calculator.setExpression({
              id: `expr-${index}`,
              latex: cleanEq,
              color: colors[index % colors.length]
            });
          }
        });

        // Auto-fit viewport
        setTimeout(() => {
          if (calculatorRef.current) {
            // Smarter bounds based on equation type
            const hasOnlyY = equations.some(eq => eq.toLowerCase().startsWith('y'));
            const bounds = hasOnlyY 
              ? { left: -10, right: 10, bottom: -6, top: 6 }
              : { left: -5, right: 5, bottom: -5, top: 5 };
            calculatorRef.current.setMathBounds(bounds);
          }
        }, 200);

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
        } catch (e) {}
      }
    };
  }, [equation]);

  if (!equation) return null;

  // Check if this is a multi-equation setup
  const isMultiEquation = equation.includes(';');
  const equationDisplay = isMultiEquation 
    ? equation.split(';').slice(0, 3).join(' | ') + (equation.split(';').length > 3 ? '...' : '')
    : equation;

  return (
    <div className="my-6">
      <div className="bg-slate-50 rounded-lg p-3 border border-slate-200 shadow-sm">
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
        
        <div className="mt-2 text-xs text-slate-500 flex items-center gap-1 flex-wrap">
          <span>Ecuación:</span>
          <code className="bg-slate-200 px-2 py-0.5 rounded font-mono">{equationDisplay}</code>
        </div>
        <div className="mt-1 text-xs text-cyan-600">
          💡 Mueve los sliders para ver cómo cambia el gráfico
        </div>
      </div>
    </div>
  );
};

export default DesmosEmbed;
