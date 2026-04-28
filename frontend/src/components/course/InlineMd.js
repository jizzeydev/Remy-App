import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import remarkGfm from 'remark-gfm';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';

const KATEX_OPTIONS = {
  throwOnError: false,
  errorColor: '#cc0000',
  strict: false,
  trust: true,
  macros: { '\\cases': '\\begin{cases}' },
};

// Render markdown inline (without wrapping the result in <p>).
// Supports inline LaTeX via $...$ — used for titles, list items, captions.
const inlineComponents = {
  p: ({ children }) => <>{children}</>,
};

export default function InlineMd({ children, className = '' }) {
  if (!children && children !== 0) return null;
  return (
    <span className={className}>
      <ReactMarkdown
        remarkPlugins={[remarkMath, remarkGfm]}
        rehypePlugins={[[rehypeKatex, KATEX_OPTIONS]]}
        components={inlineComponents}
      >
        {String(children)}
      </ReactMarkdown>
    </span>
  );
}
