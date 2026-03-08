import { lazy, Suspense } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import remarkGfm from 'remark-gfm';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';

// Only Desmos for visualizations
const DesmosEmbed = lazy(() => import('./DesmosEmbed'));

// Loading fallback for visualizations
const VisualizationLoader = ({ type }) => (
  <div className="my-6 p-8 bg-slate-100 rounded-lg border border-slate-200 animate-pulse">
    <div className="flex items-center justify-center gap-3">
      <div className="w-6 h-6 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin"></div>
      <span className="text-slate-600">Cargando {type}...</span>
    </div>
  </div>
);

const MarkdownRenderer = ({ content }) => {
  if (!content) return null;

  // Process content to extract all visualization blocks
  const processContent = (text) => {
    const parts = [];
    
    // Unified regex for all visualization types
    const vizRegex = /\[(DESMOS|GEOGEBRA|PLOTLY|3D|THREE):([^\]]+)\]/gi;
    
    let lastIndex = 0;
    let match;
    let pendingDesmos = []; // Collect consecutive Desmos for combining

    const flushDesmos = () => {
      if (pendingDesmos.length > 0) {
        // Combine all pending Desmos equations into one
        const combined = pendingDesmos.join(';');
        parts.push({
          type: 'DESMOS',
          config: combined
        });
        pendingDesmos = [];
      }
    };

    while ((match = vizRegex.exec(text)) !== null) {
      const vizType = match[1].toUpperCase();
      const vizConfig = match[2].trim();
      
      // Check if there's meaningful markdown content before this match
      const contentBefore = text.substring(lastIndex, match.index).trim();
      
      if (vizType === 'DESMOS') {
        // If there's significant content between Desmos blocks, flush and add content
        if (contentBefore.length > 20) {
          flushDesmos();
          parts.push({
            type: 'markdown',
            content: text.substring(lastIndex, match.index)
          });
        }
        pendingDesmos.push(vizConfig);
      } else {
        // Non-Desmos visualization - flush any pending Desmos first
        flushDesmos();
        
        if (match.index > lastIndex) {
          parts.push({
            type: 'markdown',
            content: text.substring(lastIndex, match.index)
          });
        }
        
        parts.push({
          type: vizType === '3D' ? 'THREE' : vizType,
          config: vizConfig
        });
      }
      
      lastIndex = match.index + match[0].length;
    }
    
    // Flush any remaining Desmos
    flushDesmos();
    
    // Add remaining markdown content
    if (lastIndex < text.length) {
      parts.push({
        type: 'markdown',
        content: text.substring(lastIndex)
      });
    }
    
    return parts.length > 0 ? parts : [{ type: 'markdown', content: text }];
  };

  const parts = processContent(content);

  // Render visualization based on type
  const renderVisualization = (part, index) => {
    const key = `viz-${index}`;
    
    if (part.type === 'DESMOS') {
      return (
        <Suspense key={key} fallback={<VisualizationLoader type="Desmos" />}>
          <DesmosEmbed equation={part.config} />
        </Suspense>
      );
    }
    
    // For any other visualization type (GeoGebra, Plotly, 3D), show a message
    return (
      <div key={key} className="my-4 p-4 bg-slate-100 border border-slate-200 rounded-lg text-slate-600 text-sm">
        <span className="font-medium">📊 Visualización:</span> Este contenido requiere actualización. 
        Usa [DESMOS:ecuación] para gráficos interactivos.
      </div>
    );
  };

  return (
    <div className="markdown-content prose prose-slate max-w-none">
      {parts.map((part, index) => (
        part.type === 'markdown' ? (
          <ReactMarkdown
            key={`md-${index}`}
            remarkPlugins={[remarkGfm, remarkMath]}
            rehypePlugins={[rehypeKatex]}
            components={{
              // Headings with nice styling
              h1: ({ node, ...props }) => (
                <h1 className="text-3xl font-bold mb-4 mt-6 text-slate-900 border-b-2 border-cyan-500 pb-2" {...props} />
              ),
              h2: ({ node, ...props }) => (
                <h2 className="text-2xl font-semibold mb-3 mt-6 text-slate-800 border-b border-slate-200 pb-2" {...props} />
              ),
              h3: ({ node, ...props }) => (
                <h3 className="text-xl font-semibold mb-2 mt-4 text-slate-700" {...props} />
              ),
              h4: ({ node, ...props }) => (
                <h4 className="text-lg font-semibold mb-2 mt-3 text-slate-600" {...props} />
              ),
              
              // Paragraphs and text
              p: ({ node, ...props }) => (
                <p className="mb-4 leading-relaxed text-slate-700" {...props} />
              ),
              strong: ({ node, ...props }) => (
                <strong className="font-bold text-slate-900" {...props} />
              ),
              em: ({ node, ...props }) => (
                <em className="italic text-slate-600" {...props} />
              ),
              
              // Lists
              ul: ({ node, ...props }) => (
                <ul className="list-disc ml-6 mb-4 space-y-2 text-slate-700" {...props} />
              ),
              ol: ({ node, ...props }) => (
                <ol className="list-decimal ml-6 mb-4 space-y-2 text-slate-700" {...props} />
              ),
              li: ({ node, ...props }) => (
                <li className="text-slate-700 leading-relaxed pl-1" {...props} />
              ),
              
              // Tables with professional styling
              table: ({ node, ...props }) => (
                <div className="overflow-x-auto my-6 rounded-lg border border-slate-200 shadow-sm">
                  <table className="min-w-full divide-y divide-slate-200" {...props} />
                </div>
              ),
              thead: ({ node, ...props }) => (
                <thead className="bg-gradient-to-r from-cyan-500 to-blue-500" {...props} />
              ),
              tbody: ({ node, ...props }) => (
                <tbody className="bg-white divide-y divide-slate-100" {...props} />
              ),
              tr: ({ node, ...props }) => (
                <tr className="hover:bg-cyan-50/50 transition-colors" {...props} />
              ),
              th: ({ node, ...props }) => (
                <th className="px-4 py-3 text-left text-sm font-semibold text-white uppercase tracking-wider" {...props} />
              ),
              td: ({ node, ...props }) => (
                <td className="px-4 py-3 text-slate-700 text-sm" {...props} />
              ),
              
              // Code blocks
              code: ({ node, inline, className, children, ...props }) => {
                if (inline) {
                  return (
                    <code className="bg-cyan-50 text-cyan-700 px-1.5 py-0.5 rounded text-sm font-mono border border-cyan-100" {...props}>
                      {children}
                    </code>
                  );
                }
                return (
                  <pre className="bg-slate-900 text-slate-100 p-4 rounded-lg mb-4 overflow-x-auto shadow-lg">
                    <code className="font-mono text-sm" {...props}>
                      {children}
                    </code>
                  </pre>
                );
              },
              
              // Blockquotes for tips and important notes
              blockquote: ({ node, ...props }) => (
                <blockquote 
                  className="border-l-4 border-cyan-500 bg-gradient-to-r from-cyan-50 to-white pl-4 py-3 my-4 text-slate-700 rounded-r-lg shadow-sm"
                  {...props} 
                />
              ),
              
              // Horizontal rules
              hr: ({ node, ...props }) => (
                <hr className="my-8 border-slate-200" {...props} />
              ),
              
              // Links
              a: ({ node, href, ...props }) => (
                <a 
                  href={href} 
                  className="text-cyan-600 hover:text-cyan-800 underline underline-offset-2 font-medium transition-colors"
                  target="_blank"
                  rel="noopener noreferrer"
                  {...props} 
                />
              ),
              
              // Images
              img: ({ node, src, alt, ...props }) => (
                <figure className="my-6">
                  <img 
                    src={src} 
                    alt={alt}
                    className="rounded-lg shadow-md max-w-full h-auto mx-auto"
                    {...props} 
                  />
                  {alt && (
                    <figcaption className="text-center text-sm text-slate-500 mt-2 italic">
                      {alt}
                    </figcaption>
                  )}
                </figure>
              ),
            }}
          >
            {part.content}
          </ReactMarkdown>
        ) : (
          renderVisualization(part, index)
        )
      ))}
    </div>
  );
};

export default MarkdownRenderer;
