import { useState, useRef, useEffect, useCallback, memo } from 'react';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { toast } from 'sonner';
import { Sparkles, Send, X, MessageSquare } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const ADMIN_API = `${BACKEND_URL}/api/admin`;

// Memoized chat message component to prevent re-renders
const ChatMessage = memo(({ message }) => (
  <div 
    className={`p-3 rounded-lg text-sm ${
      message.role === 'user' 
        ? 'bg-cyan-500 text-white ml-8' 
        : 'bg-white border shadow-sm mr-4 text-slate-700'
    }`}
  >
    <div className="whitespace-pre-wrap leading-relaxed">{message.content}</div>
  </div>
));

ChatMessage.displayName = 'ChatMessage';

// Loading indicator component
const LoadingIndicator = memo(() => (
  <div className="bg-white border shadow-sm mr-4 p-3 rounded-lg text-sm flex items-center gap-2">
    <div className="animate-spin w-4 h-4 border-2 border-cyan-500 border-t-transparent rounded-full"></div>
    <span className="text-slate-500">Remy está trabajando...</span>
  </div>
));

LoadingIndicator.displayName = 'LoadingIndicator';

/**
 * RemyChat - Optimized chat component for editing lessons and questions
 * 
 * Props:
 * - isOpen: boolean - whether chat is visible
 * - onClose: function - callback to close chat
 * - currentContent: string - the current content being edited
 * - onContentUpdate: function(newContent) - callback when content is updated
 * - context: object - { type: 'lesson' | 'question', title, chapterTitle, courseTitle, questionData }
 */
const RemyChat = memo(({ 
  isOpen, 
  onClose, 
  currentContent, 
  onContentUpdate, 
  context = {} 
}) => {
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState([]);
  const chatEndRef = useRef(null);
  const inputRef = useRef(null);
  const isInitializedRef = useRef(false);

  // Initialize chat with welcome message when opened
  useEffect(() => {
    if (isOpen && !isInitializedRef.current) {
      const welcomeMessage = getWelcomeMessage(context);
      setMessages([{ role: 'assistant', content: welcomeMessage }]);
      isInitializedRef.current = true;
      
      // Focus input after a short delay
      setTimeout(() => inputRef.current?.focus(), 100);
    }
    
    if (!isOpen) {
      isInitializedRef.current = false;
    }
  }, [isOpen, context]);

  // Scroll to bottom when messages change
  useEffect(() => {
    if (messages.length > 0) {
      setTimeout(() => {
        chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    }
  }, [messages.length]);

  const getWelcomeMessage = (ctx) => {
    if (ctx.type === 'question') {
      return `¡Hola! Soy Remy 🎓

Estoy listo para mejorar esta pregunta${ctx.topic ? ` sobre "${ctx.topic}"` : ''}.

**Puedo ayudarte a:**
• Reformular el enunciado para que sea más claro
• Mejorar las opciones de respuesta (distractores más plausibles)
• Expandir la explicación paso a paso
• Cambiar el nivel de dificultad
• Agregar fórmulas LaTeX donde falten

**Ejemplos de instrucciones:**
"Haz el enunciado más corto y directo"
"Mejora los distractores, son muy obvios"
"Agrega más pasos en la explicación"
"Cambia los números del ejercicio"`;
    }
    
    return `¡Hola! Soy Remy 🎓

Estoy listo para mejorar la lección "${ctx.title || 'actual'}".
${ctx.chapterTitle ? `📂 Capítulo: ${ctx.chapterTitle}` : ''}
${ctx.courseTitle ? `📚 Curso: ${ctx.courseTitle}` : ''}

**Puedo ayudarte a:**
• Agregar ejemplos más claros y paso a paso
• Mejorar explicaciones confusas
• Añadir gráficos Desmos interactivos
• Quitar contenido innecesario
• Agregar tips para el examen
• Insertar placeholders para imágenes

**Ejemplos de instrucciones:**
"Agrega un ejemplo paso a paso de cómo derivar x³"
"La explicación del límite está confusa, simplifícala"
"Pon un Desmos donde se vea la tangente moviéndose"
"Agrega una imagen para explicar la discontinuidad"`;
  };

  // Optimized input handler - doesn't cause parent re-renders
  const handleInputChange = useCallback((e) => {
    setInputValue(e.target.value);
  }, []);

  const handleSend = useCallback(async () => {
    const trimmedInput = inputValue.trim();
    if (!trimmedInput || isLoading) return;

    // Clear input immediately for better UX
    setInputValue('');
    
    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: trimmedInput }]);
    setIsLoading(true);

    try {
      const token = localStorage.getItem('admin_token');
      
      let endpoint, payload;
      
      if (context.type === 'question') {
        // Edit question content
        endpoint = `${ADMIN_API}/edit-question-content`;
        payload = {
          current_content: currentContent,
          user_instruction: trimmedInput,
          question_data: context.questionData || {},
          topic: context.topic || '',
          course_title: context.courseTitle || ''
        };
      } else {
        // Edit lesson content
        endpoint = `${ADMIN_API}/edit-lesson-content`;
        payload = {
          current_content: currentContent,
          user_instruction: trimmedInput,
          lesson_title: context.title || '',
          chapter_title: context.chapterTitle || '',
          course_title: context.courseTitle || ''
        };
      }

      const response = await axios.post(endpoint, payload, {
        headers: { Authorization: `Bearer ${token}` }
      });

      // Update parent content
      if (response.data.content) {
        onContentUpdate(response.data.content);
      }

      // Add success message
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: response.data.message || '✅ ¡Listo! He actualizado el contenido. Revisa los cambios en la vista previa.' 
      }]);
      
      toast.success('Contenido actualizado');
    } catch (error) {
      console.error('Error editing content:', error);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: '❌ Hubo un error. Intenta ser más específico en tu instrucción o verifica que el contenido no esté vacío.' 
      }]);
      toast.error('Error al editar contenido');
    } finally {
      setIsLoading(false);
    }
  }, [inputValue, isLoading, currentContent, context, onContentUpdate]);

  const handleKeyDown = useCallback((e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }, [handleSend]);

  if (!isOpen) return null;

  return (
    <div 
      className="absolute inset-0 bg-white border rounded-lg shadow-2xl z-[60] flex flex-col" 
      data-testid="remy-chat"
      onClick={(e) => e.stopPropagation()}
    >
      {/* Header */}
      <div className="p-3 bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-t-lg flex items-center justify-between">
        <span className="font-medium flex items-center gap-2">
          <Sparkles size={16} />
          Chat con Remy - {context.type === 'question' ? 'Editar Pregunta' : 'Editar Lección'}
        </span>
        <button 
          onClick={onClose} 
          className="hover:bg-white/20 rounded p-1 transition-colors"
          data-testid="close-chat"
        >
          <X size={16} />
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-3 space-y-3 bg-slate-50 min-h-[200px] max-h-[280px]">
        {messages.map((msg, i) => (
          <ChatMessage key={i} message={msg} />
        ))}
        {isLoading && <LoadingIndicator />}
        <div ref={chatEndRef} />
      </div>

      {/* Input */}
      <div className="p-3 border-t bg-white rounded-b-lg">
        <div className="flex gap-2">
          <Textarea
            ref={inputRef}
            value={inputValue}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder={context.type === 'question' 
              ? "Ej: Mejora los distractores, son muy obvios..." 
              : "Ej: Agrega un ejemplo de derivada de x³..."
            }
            disabled={isLoading}
            className="text-sm min-h-[40px] max-h-[100px] resize-none"
            rows={1}
            data-testid="chat-input"
          />
          <Button 
            type="button" 
            size="sm" 
            onClick={handleSend}
            disabled={isLoading || !inputValue.trim()}
            className="bg-cyan-500 hover:bg-cyan-600 self-end"
            data-testid="send-message"
          >
            <Send size={14} />
          </Button>
        </div>
        <p className="text-xs text-slate-400 mt-2">
          {context.type === 'question' 
            ? 'Tip: "Reformula el enunciado" o "Cambia los números del problema"'
            : 'Tip: Sé específico. "Agrega un Desmos que muestre cómo cambia la pendiente"'
          }
        </p>
      </div>
    </div>
  );
});

RemyChat.displayName = 'RemyChat';

export default RemyChat;
