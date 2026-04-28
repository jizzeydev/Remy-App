import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import remarkGfm from 'remark-gfm';
import rehypeKatex from 'rehype-katex';
import { Check, X, ImageIcon, Lightbulb } from 'lucide-react';
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
                <code className="bg-muted text-foreground px-1 py-0.5 rounded text-sm font-mono" {...props}>
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
                <code className="bg-muted text-foreground px-1.5 py-0.5 rounded text-sm font-mono" {...props}>
                  {codeChildren}
                </code>
              );
            }
            return (
              <pre className="bg-slate-950 dark:bg-black/50 text-slate-100 p-3 rounded-lg mb-3 overflow-x-auto border border-border">
                <code className="font-mono text-sm" {...props}>
                  {codeChildren}
                </code>
              </pre>
            );
          },
          blockquote: ({ node, ...props }) => (
            <blockquote
              className="border-l-4 border-primary bg-primary/5 pl-3 py-2 my-2 rounded-r"
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
                <figcaption className="text-center text-xs text-muted-foreground mt-1 italic">
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
      <div className="bg-amber-500/10 border-2 border-dashed border-amber-500/40 rounded-lg p-4 text-center">
        <div className="flex items-center justify-center gap-2 mb-2">
          <ImageIcon size={18} className="text-amber-600 dark:text-amber-400" aria-hidden="true" />
          <span className="text-xs font-medium text-amber-700 dark:text-amber-300">Imagen por insertar</span>
        </div>
        <p className="text-amber-800 dark:text-amber-200 text-sm leading-relaxed">
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

  // Build container classes based on state — all theme-aware
  const baseClasses = 'group w-full p-4 text-left border-2 rounded-xl transition-all focus:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-background';

  let stateClasses = '';
  if (showCorrectStyle) {
    stateClasses = 'border-emerald-500 bg-emerald-500/10';
  } else if (showIncorrectStyle) {
    stateClasses = 'border-red-500 bg-red-500/10';
  } else if (isSelected) {
    stateClasses = 'border-primary bg-primary/10 shadow-md shadow-primary/10';
  } else {
    stateClasses = 'border-border bg-card';
  }

  const interactiveClasses = !disabled && !showResult
    ? 'hover:border-primary/60 hover:bg-primary/5 cursor-pointer'
    : '';

  // Letter circle classes
  let letterClasses = '';
  if (showCorrectStyle) {
    letterClasses = 'bg-emerald-500 text-white';
  } else if (showIncorrectStyle) {
    letterClasses = 'bg-red-500 text-white';
  } else if (isSelected) {
    letterClasses = 'bg-primary text-primary-foreground';
  } else {
    letterClasses = 'bg-muted text-foreground border border-border';
  }

  // Text color classes
  let textClasses = 'text-foreground';
  if (showCorrectStyle) {
    textClasses = 'text-emerald-700 dark:text-emerald-200 font-medium';
  } else if (showIncorrectStyle) {
    textClasses = 'text-red-700 dark:text-red-200 font-medium';
  } else if (isSelected) {
    textClasses = 'text-foreground font-medium';
  }

  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      data-testid={testId}
      aria-pressed={isSelected}
      className={`${baseClasses} ${stateClasses} ${interactiveClasses}`}
    >
      <div className="flex items-start gap-3">
        <span
          className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold transition-colors ${letterClasses}`}
          aria-hidden="true"
        >
          {letter}
        </span>
        <div className="flex-1 pt-1 min-w-0">
          <MathText className={textClasses}>{content}</MathText>
        </div>
        {showCorrectStyle && (
          <Check size={22} className="text-emerald-600 dark:text-emerald-400 flex-shrink-0" aria-label="Respuesta correcta" />
        )}
        {showIncorrectStyle && (
          <X size={22} className="text-red-600 dark:text-red-400 flex-shrink-0" aria-label="Respuesta incorrecta" />
        )}
      </div>
    </button>
  );
};

// Explanation renderer
export const ExplanationBlock = ({ explanation }) => {
  if (!explanation) return null;

  return (
    <div className="bg-primary/5 border border-primary/20 rounded-xl p-4 mt-4">
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/15 ring-1 ring-primary/30 flex items-center justify-center">
          <Lightbulb size={16} className="text-primary" aria-hidden="true" />
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-semibold text-foreground mb-2">Explicación:</p>
          <QuestionContent content={explanation} className="text-muted-foreground text-sm" />
        </div>
      </div>
    </div>
  );
};

export default { MathText, MathBlock, QuestionContent, QuestionOption, ExplanationBlock, ImagePlaceholder };
