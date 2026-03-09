import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import remarkGfm from 'remark-gfm';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';

// KaTeX options to handle errors gracefully
const katexOptions = {
  throwOnError: false,
  errorColor: '#cc0000',
  strict: false,
  trust: true,
  macros: {
    "\\cases": "\\begin{cases}",
  }
};

// Component to render text with KaTeX and Markdown support
export const MathText = ({ children, className = '' }) => {
  if (!children) return null;
  
  return (
    <span className={className}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[[rehypeKatex, katexOptions]]}
        components={{
          p: ({ node, ...props }) => <span {...props} />,
          // Inline rendering - no block elements
          code: ({ node, inline, children: codeChildren, ...props }) => {
            if (inline) {
              return (
                <code className="bg-slate-100 text-slate-700 px-1 py-0.5 rounded text-sm font-mono" {...props}>
                  {codeChildren}
                </code>
              );
            }
            return <code {...props}>{codeChildren}</code>;
          },
        }}
      >
        {children}
      </ReactMarkdown>
    </span>
  );
};

// Component to render a full block of content (for explanations, question text)
export const MathBlock = ({ children, className = '' }) => {
  if (!children) return null;
  
  return (
    <div className={`math-content ${className}`}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[[rehypeKatex, katexOptions]]}
        components={{
          p: ({ node, ...props }) => (
            <p className="mb-2 leading-relaxed" {...props} />
          ),
          strong: ({ node, ...props }) => (
            <strong className="font-bold" {...props} />
          ),
          em: ({ node, ...props }) => (
            <em className="italic" {...props} />
          ),
          ul: ({ node, ...props }) => (
            <ul className="list-disc ml-4 mb-2 space-y-1" {...props} />
          ),
          ol: ({ node, ...props }) => (
            <ol className="list-decimal ml-4 mb-2 space-y-1" {...props} />
          ),
          li: ({ node, ...props }) => (
            <li className="leading-relaxed" {...props} />
          ),
          code: ({ node, inline, children: codeChildren, ...props }) => {
            if (inline) {
              return (
                <code className="bg-slate-100 text-slate-700 px-1.5 py-0.5 rounded text-sm font-mono" {...props}>
                  {codeChildren}
                </code>
              );
            }
            return (
              <pre className="bg-slate-900 text-slate-100 p-3 rounded-lg mb-3 overflow-x-auto">
                <code className="font-mono text-sm" {...props}>
                  {codeChildren}
                </code>
              </pre>
            );
          },
          blockquote: ({ node, ...props }) => (
            <blockquote 
              className="border-l-4 border-cyan-500 bg-cyan-50 pl-3 py-2 my-2 rounded-r"
              {...props} 
            />
          ),
          img: ({ node, src, alt, ...props }) => (
            <figure className="my-3">
              <img 
                src={src} 
                alt={alt}
                className="rounded-lg shadow-sm max-w-full h-auto mx-auto"
                {...props} 
              />
              {alt && (
                <figcaption className="text-center text-xs text-slate-500 mt-1 italic">
                  {alt}
                </figcaption>
              )}
            </figure>
          ),
        }}
      >
        {children}
      </ReactMarkdown>
    </div>
  );
};

// Image placeholder component for questions
export const ImagePlaceholder = ({ description }) => {
  if (!description) return null;
  
  return (
    <div className="my-3 mx-auto max-w-lg">
      <div className="bg-gradient-to-r from-amber-50 to-orange-50 border-2 border-dashed border-amber-300 rounded-lg p-4 text-center">
        <div className="flex items-center justify-center gap-2 mb-2">
          <svg className="w-5 h-5 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <span className="text-xs font-medium text-amber-600">Imagen por insertar</span>
        </div>
        <p className="text-amber-700 text-sm leading-relaxed">
          {description}
        </p>
      </div>
    </div>
  );
};

// Process content to handle image placeholders
const processContent = (text) => {
  if (!text) return [];
  
  const parts = [];
  // Match **[INSERTAR IMAGEN: ...]** pattern
  const imgRegex = /\*\*\[INSERTAR IMAGEN:\s*([^\]]+)\]\*\*/gi;
  
  let lastIndex = 0;
  let match;
  
  while ((match = imgRegex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      parts.push({
        type: 'text',
        content: text.substring(lastIndex, match.index)
      });
    }
    
    parts.push({
      type: 'image_placeholder',
      content: match[1].trim()
    });
    
    lastIndex = match.index + match[0].length;
  }
  
  if (lastIndex < text.length) {
    parts.push({
      type: 'text',
      content: text.substring(lastIndex)
    });
  }
  
  return parts.length > 0 ? parts : [{ type: 'text', content: text }];
};

// Full question content renderer with image placeholders support
export const QuestionContent = ({ content, className = '' }) => {
  if (!content) return null;
  
  const parts = processContent(content);
  
  return (
    <div className={className}>
      {parts.map((part, idx) => (
        part.type === 'image_placeholder' ? (
          <ImagePlaceholder key={idx} description={part.content} />
        ) : (
          <MathBlock key={idx}>{part.content}</MathBlock>
        )
      ))}
    </div>
  );
};

// Option renderer that handles KaTeX in options
export const QuestionOption = ({ option, isSelected, isCorrect, showResult, onClick, disabled, testId }) => {
  // Extract option letter and content
  const optionMatch = option.match(/^([A-D])\)\s*(.*)/s);
  const letter = optionMatch ? optionMatch[1] : option.charAt(0);
  const content = optionMatch ? optionMatch[2] : option.substring(2).trim();
  
  const showCorrectStyle = showResult && isCorrect;
  const showIncorrectStyle = showResult && isSelected && !isCorrect;
  
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      data-testid={testId}
      className={`w-full p-4 text-left border-2 rounded-xl transition-all ${
        isSelected && !showResult ? 'border-cyan-500 bg-cyan-50' : 'border-slate-200'
      } ${showCorrectStyle ? 'border-green-500 bg-green-50' : ''} ${
        showIncorrectStyle ? 'border-red-500 bg-red-50' : ''
      } ${!disabled ? 'hover:border-cyan-400 hover:bg-slate-50' : ''}`}
    >
      <div className="flex items-start gap-3">
        <span className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
          showCorrectStyle ? 'bg-green-500 text-white' : 
          showIncorrectStyle ? 'bg-red-500 text-white' :
          isSelected ? 'bg-cyan-500 text-white' : 'bg-slate-200 text-slate-700'
        }`}>
          {letter}
        </span>
        <div className="flex-1 pt-1">
          <MathText className="text-slate-700">{content}</MathText>
        </div>
        {showCorrectStyle && (
          <svg className="w-6 h-6 text-green-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        )}
        {showIncorrectStyle && (
          <svg className="w-6 h-6 text-red-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        )}
      </div>
    </button>
  );
};

// Explanation renderer
export const ExplanationBlock = ({ explanation }) => {
  if (!explanation) return null;
  
  return (
    <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-xl p-4 mt-4">
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center">
          <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div className="flex-1">
          <p className="text-sm font-semibold text-blue-900 mb-2">Explicación:</p>
          <QuestionContent content={explanation} className="text-blue-800 text-sm" />
        </div>
      </div>
    </div>
  );
};

export default { MathText, MathBlock, QuestionContent, QuestionOption, ExplanationBlock, ImagePlaceholder };
