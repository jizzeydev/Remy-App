import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';
import DesmosEmbed from './DesmosEmbed';

const MarkdownRenderer = ({ content }) => {
  // Process content to handle Desmos embeds
  const processContent = (text) => {
    const parts = [];
    const desmosRegex = /\[DESMOS:(.*?)\]/g;
    let lastIndex = 0;
    let match;

    while ((match = desmosRegex.exec(text)) !== null) {
      // Add text before the match
      if (match.index > lastIndex) {
        parts.push({
          type: 'markdown',
          content: text.substring(lastIndex, match.index)
        });
      }
      
      // Add Desmos embed
      parts.push({
        type: 'desmos',
        equation: match[1]
      });
      
      lastIndex = match.index + match[0].length;
    }
    
    // Add remaining text
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
    <div className="markdown-content">
      {parts.map((part, index) => (
        part.type === 'markdown' ? (
          <ReactMarkdown
            key={index}
            remarkPlugins={[remarkMath]}
            rehypePlugins={[rehypeKatex]}
            components={{
              h1: ({ node, ...props }) => <h1 className="text-3xl font-bold mb-4 mt-6" {...props} />,
              h2: ({ node, ...props }) => <h2 className="text-2xl font-semibold mb-3 mt-5" {...props} />,
              h3: ({ node, ...props }) => <h3 className="text-xl font-semibold mb-2 mt-4" {...props} />,
              p: ({ node, ...props }) => <p className="mb-4 leading-relaxed" {...props} />,
              ul: ({ node, ...props }) => <ul className="list-disc list-inside mb-4 space-y-2" {...props} />,
              ol: ({ node, ...props }) => <ol className="list-decimal list-inside mb-4 space-y-2" {...props} />,
              li: ({ node, ...props }) => <li className="ml-4" {...props} />,
              code: ({ node, inline, ...props }) => 
                inline ? (
                  <code className="bg-slate-100 px-2 py-1 rounded text-sm" {...props} />
                ) : (
                  <code className="block bg-slate-100 p-4 rounded-lg mb-4 overflow-x-auto" {...props} />
                ),
              blockquote: ({ node, ...props }) => (
                <blockquote className="border-l-4 border-primary pl-4 italic my-4 text-slate-700" {...props} />
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
