import { useEffect, useRef } from 'react';

const DesmosEmbed = ({ equation, height = 400 }) => {
  const calculatorRef = useRef(null);
  const containerRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Load Desmos API if not already loaded
    if (!window.Desmos) {
      const script = document.createElement('script');
      script.src = 'https://www.desmos.com/api/v1.9/calculator.js?apiKey=dcb31709b452b1cf9dc26972add0fda6';
      script.async = true;
      script.onload = () => initCalculator();
      document.body.appendChild(script);
    } else {
      initCalculator();
    }

    function initCalculator() {
      if (calculatorRef.current) {
        calculatorRef.current.destroy();
      }

      const calculator = window.Desmos.GraphingCalculator(containerRef.current, {
        keypad: false,
        expressions: false,
        settingsMenu: false,
        zoomButtons: true,
        lockViewport: false,
        expressionsTopbar: false
      });

      calculatorRef.current = calculator;

      // Parse and add equations
      const equations = equation.split(';').map(eq => eq.trim());
      equations.forEach((eq, index) => {
        calculator.setExpression({
          id: `graph-${index}`,
          latex: eq,
          color: index === 0 ? '#00BCD4' : '#2196F3'
        });
      });
    }

    return () => {
      if (calculatorRef.current) {
        calculatorRef.current.destroy();
      }
    };
  }, [equation]);

  return (
    <div className="my-6">
      <div 
        ref={containerRef} 
        style={{ width: '100%', height: `${height}px` }}
        className="border border-slate-200 rounded-lg"
      />
    </div>
  );
};

export default DesmosEmbed;
