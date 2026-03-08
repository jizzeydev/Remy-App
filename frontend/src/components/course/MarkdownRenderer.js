import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';
import DesmosEmbed from './DesmosEmbed';

const MarkdownRenderer = ({ content }) => {
  const processContent = (text) => {
    const parts = [];
    const desmosRegex = /\[DESMOS:(.*?)\]/g;
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
        equation: match[1]
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
            remarkPlugins={[remarkMath]}
            rehypePlugins={[rehypeKatex]}
            components={{
              h1: ({ node, ...props }) => <h1 className="text-3xl font-bold mb-4 mt-6 text-slate-900" {...props} />,
              h2: ({ node, ...props }) => <h2 className="text-2xl font-semibold mb-3 mt-5 text-slate-800" {...props} />,
              h3: ({ node, ...props }) => <h3 className="text-xl font-semibold mb-2 mt-4 text-slate-700" {...props} />,
              p: ({ node, ...props }) => <p className="mb-4 leading-relaxed text-slate-700" {...props} />,
              ul: ({ node, ...props }) => <ul className="list-disc list-inside mb-4 space-y-2 text-slate-700" {...props} />,
              ol: ({ node, ...props }) => <ol className="list-decimal list-inside mb-4 space-y-2 text-slate-700" {...props} />,
              li: ({ node, ...props }) => <li className="ml-4 text-slate-700" {...props} />,
              code: ({ node, inline, ...props }) => 
                inline ? (
                  <code className="bg-slate-100 px-2 py-1 rounded text-sm font-mono text-slate-800" {...props} />
                ) : (
                  <code className="block bg-slate-900 text-slate-100 p-4 rounded-lg mb-4 overflow-x-auto font-mono text-sm" {...props} />
                ),
              blockquote: ({ node, ...props }) => (
                <blockquote className="border-l-4 border-primary bg-cyan-50 pl-4 py-2 italic my-4 text-slate-700 rounded-r" {...props} />
              ),
              strong: ({ node, ...props }) => <strong className="font-bold text-slate-900" {...props} />,
              em: ({ node, ...props }) => <em className="italic text-slate-700" {...props} />,
              hr: ({ node, ...props }) => <hr className="my-6 border-slate-200" {...props} />,
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
