import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import remarkGfm from 'remark-gfm';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';
import DesmosEmbed from './DesmosEmbed';

const MarkdownRenderer = ({ content }) => {
  if (!content) return null;

  // Process content to extract Desmos graphs
  const processContent = (text) => {
    const parts = [];
    // Match [DESMOS:equation] pattern - handle complex equations
    const desmosRegex = /\[DESMOS:([^\]]+)\]/g;
    let lastIndex = 0;
    let match;

    while ((match = desmosRegex.exec(text)) !== null) {
      if (match.index > lastIndex) {
        parts.push({
          type: 'markdown',
          content: text.substring(lastIndex, match.index)
        });
      }
      
      parts.push({
        type: 'desmos',
        equation: match[1].trim()
      });
      
      lastIndex = match.index + match[0].length;
    }
    
    if (lastIndex < text.length) {
      parts.push({
        type: 'markdown',
        content: text.substring(lastIndex)
      });
    }
    
    return parts.length > 0 ? parts : [{ type: 'markdown', content: text }];
  };

  const parts = processContent(content);

  return (
    <div className="markdown-content prose prose-slate max-w-none">
      {parts.map((part, index) => (
        part.type === 'markdown' ? (
          <ReactMarkdown
            key={index}
            remarkPlugins={[remarkGfm, remarkMath]}
            rehypePlugins={[rehypeKatex]}
            components={{
              h1: ({ node, ...props }) => (
                <h1 className="text-3xl font-bold mb-4 mt-6 text-slate-900" {...props} />
              ),
              h2: ({ node, ...props }) => (
                <h2 className="text-2xl font-semibold mb-3 mt-5 text-slate-800 border-b border-slate-200 pb-2" {...props} />
              ),
              h3: ({ node, ...props }) => (
                <h3 className="text-xl font-semibold mb-2 mt-4 text-slate-700" {...props} />
              ),
              p: ({ node, ...props }) => (
                <p className="mb-4 leading-relaxed text-slate-700" {...props} />
              ),
              ul: ({ node, ...props }) => (
                <ul className="list-disc ml-6 mb-4 space-y-2 text-slate-700" {...props} />
              ),
              ol: ({ node, ...props }) => (
                <ol className="list-decimal ml-6 mb-4 space-y-2 text-slate-700" {...props} />
              ),
              li: ({ node, ...props }) => (
                <li className="text-slate-700 leading-relaxed" {...props} />
              ),
              // Table styling
              table: ({ node, ...props }) => (
                <div className="overflow-x-auto my-6">
                  <table className="min-w-full border-collapse border border-slate-300 rounded-lg overflow-hidden" {...props} />
                </div>
              ),
              thead: ({ node, ...props }) => (
                <thead className="bg-gradient-to-r from-cyan-500 to-blue-500 text-white" {...props} />
              ),
              tbody: ({ node, ...props }) => (
                <tbody className="divide-y divide-slate-200" {...props} />
              ),
              tr: ({ node, ...props }) => (
                <tr className="hover:bg-cyan-50 transition-colors" {...props} />
              ),
              th: ({ node, ...props }) => (
                <th className="px-4 py-3 text-left font-semibold text-sm uppercase tracking-wider" {...props} />
              ),
              td: ({ node, ...props }) => (
                <td className="px-4 py-3 text-slate-700 border-b border-slate-200" {...props} />
              ),
              // Code blocks
              code: ({ node, inline, className, children, ...props }) => {
                if (inline) {
                  return (
                    <code className="bg-slate-100 px-2 py-1 rounded text-sm font-mono text-cyan-700" {...props}>
                      {children}
                    </code>
                  );
                }
                return (
                  <pre className="bg-slate-900 text-slate-100 p-4 rounded-lg mb-4 overflow-x-auto">
                    <code className="font-mono text-sm" {...props}>
                      {children}
                    </code>
                  </pre>
                );
              },
              blockquote: ({ node, ...props }) => (
                <blockquote 
                  className="border-l-4 border-cyan-500 bg-cyan-50 pl-4 py-3 my-4 text-slate-700 rounded-r-lg italic"
                  {...props} 
                />
              ),
              strong: ({ node, ...props }) => (
                <strong className="font-bold text-slate-900" {...props} />
              ),
              em: ({ node, ...props }) => (
                <em className="italic text-slate-600" {...props} />
              ),
              hr: ({ node, ...props }) => (
                <hr className="my-8 border-slate-300" {...props} />
              ),
              // Links
              a: ({ node, href, ...props }) => (
                <a 
                  href={href} 
                  className="text-cyan-600 hover:text-cyan-800 underline underline-offset-2"
                  target="_blank"
                  rel="noopener noreferrer"
                  {...props} 
                />
              ),
              // Images
              img: ({ node, src, alt, ...props }) => (
                <img 
                  src={src} 
                  alt={alt}
                  className="rounded-lg shadow-md my-4 max-w-full h-auto"
                  {...props} 
                />
              ),
            }}
          >
            {part.content}
          </ReactMarkdown>
        ) : (
          <DesmosEmbed key={index} equation={part.equation} />
        )
      ))}
    </div>
  );
};

export default MarkdownRenderer;
