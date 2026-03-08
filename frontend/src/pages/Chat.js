import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Send, Loader2, BookOpen } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState('');
  const messagesEndRef = useRef(null);
  const userId = 'demo-user-001';

  useEffect(() => {
    fetchCourses();
    fetchChatHistory();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchCourses = async () => {
    try {
      const response = await axios.get(`${API}/courses`);
      setCourses(response.data);
    } catch (error) {
      console.error('Error fetching courses:', error);
    }
  };

  const fetchChatHistory = async () => {
    try {
      const response = await axios.get(`${API}/chat/history/${userId}`);
      const history = response.data.map(msg => ({
        role: msg.role,
        content: msg.content
      }));
      setMessages(history);
    } catch (error) {
      console.error('Error fetching chat history:', error);
    }
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const courseContext = selectedCourse
        ? courses.find(c => c.id === selectedCourse)?.title
        : null;

      const response = await axios.post(`${API}/chat`, {
        user_id: userId,
        message: input,
        course_context: courseContext
      });

      const assistantMessage = {
        role: 'assistant',
        content: response.data.message
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      toast.error('Error al enviar el mensaje. Intenta nuevamente.');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="h-[calc(100vh-12rem)] lg:h-[calc(100vh-8rem)] flex flex-col" data-testid="chat-page">
      <Card className="flex-1 flex flex-col">
        <CardHeader className="border-b">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <CardTitle className="flex items-center gap-2">
                <div className="w-10 h-10 bg-gradient-to-br from-cyan-400 to-cyan-600 rounded-full flex items-center justify-center text-white font-bold">
                  R
                </div>
                <span>Remy - Tu Tutor IA</span>
              </CardTitle>
              <p className="text-sm text-slate-500 mt-1">Pregunta cualquier duda sobre tus cursos</p>
            </div>
            <div className="w-full sm:w-64">
              <Select value={selectedCourse} onValueChange={setSelectedCourse}>
                <SelectTrigger data-testid="course-selector">
                  <SelectValue placeholder="Selecciona un curso" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="none">Sin curso específico</SelectItem>
                  {courses.map(course => (
                    <SelectItem key={course.id} value={course.id}>
                      {course.title}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardHeader>

        <CardContent className="flex-1 overflow-y-auto p-6 space-y-4" data-testid="chat-messages">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center p-8">
              <div className="w-20 h-20 bg-gradient-to-br from-cyan-400 to-cyan-600 rounded-full flex items-center justify-center text-white text-3xl font-bold mb-4">
                R
              </div>
              <h3 className="text-xl font-semibold mb-2">¡Hola! Soy Remy 👋</h3>
              <p className="text-slate-500 max-w-md">
                Estoy aquí para ayudarte con tus dudas de cálculo, álgebra, física y más. ¿Qué quieres aprender hoy?
              </p>
              <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-2xl">
                {[
                  '¿Cómo resuelvo una integral?',
                  'Explícame derivadas',
                  '¿Qué es un límite?',
                  'Ayuda con vectores'
                ].map((suggestion, i) => (
                  <button
                    key={i}
                    onClick={() => setInput(suggestion)}
                    data-testid={`suggestion-${i}`}
                    className="p-3 text-sm border border-slate-200 rounded-xl hover:bg-secondary hover:border-primary transition-all text-left"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            messages.map((msg, index) => (
              <div
                key={index}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                data-testid={`chat-message-${index}`}
              >
                <div className={`chat-bubble ${msg.role}`}>
                  {msg.content}
                </div>
              </div>
            ))
          )}
          {loading && (
            <div className="flex justify-start" data-testid="loading-indicator">
              <div className="chat-bubble assistant flex items-center gap-2">
                <Loader2 className="animate-spin" size={16} />
                <span>Remy está pensando...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </CardContent>

        <div className="border-t p-4">
          <div className="flex gap-2">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Escribe tu pregunta aquí..."
              disabled={loading}
              data-testid="chat-input"
              className="flex-1"
            />
            <Button
              onClick={handleSend}
              disabled={loading || !input.trim()}
              data-testid="send-button"
              className="rounded-full px-6"
            >
              {loading ? <Loader2 className="animate-spin" size={20} /> : <Send size={20} />}
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default Chat;
