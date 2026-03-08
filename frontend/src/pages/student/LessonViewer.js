import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ArrowLeft, Clock, BookOpen } from 'lucide-react';
import { toast } from 'sonner';
import MarkdownRenderer from '@/components/course/MarkdownRenderer';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const LessonViewer = () => {
  const { lessonId } = useParams();
  const navigate = useNavigate();
  const [lesson, setLesson] = useState(null);
  const [chapter, setChapter] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLesson();
  }, [lessonId]);

  const fetchLesson = async () => {
    try {
      const lessonRes = await axios.get(`${API}/lessons/${lessonId}`);
      setLesson(lessonRes.data);

      const chaptersRes = await axios.get(`${API}/chapters/${lessonRes.data.chapter_id}/lessons`);
      const chapterData = await db.chapters.find_one({"id": lessonRes.data.chapter_id});
      setChapter(chapterData);
    } catch (error) {
      console.error('Error fetching lesson:', error);
      toast.error('Error al cargar la lección');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="text-center py-12">Cargando...</div>;
  if (!lesson) return <div className="text-center py-12">Lección no encontrada</div>;

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-24 lg:pb-8">
      <Button variant="ghost" onClick={() => navigate(-1)}>
        <ArrowLeft size={20} className="mr-2" />
        Volver
      </Button>

      <Card>
        <CardContent className="pt-6">
          <div className="mb-6">
            <div className="flex items-center gap-2 text-sm text-slate-500 mb-2">
              <BookOpen size={16} />
              <span>Lección</span>
            </div>
            <h1 className="text-3xl font-bold mb-3">{lesson.title}</h1>
            <div className="flex items-center gap-2 text-sm text-slate-600">
              <Clock size={16} />
              <span>{lesson.duration_minutes} minutos</span>
            </div>
          </div>

          <div className="prose prose-slate max-w-none">
            <MarkdownRenderer content={lesson.content} />
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default LessonViewer;
