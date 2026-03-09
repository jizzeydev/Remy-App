import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { BookOpen, Loader2, Layers, GraduationCap } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Biblioteca = () => {
  const navigate = useNavigate();
  const [courses, setCourses] = useState([]);
  const [coursesStats, setCoursesStats] = useState({});
  const [loading, setLoading] = useState(true);

  // Get student ID from localStorage or generate one
  const getStudentId = () => {
    let studentId = localStorage.getItem('student_id');
    if (!studentId) {
      studentId = 'student_' + Date.now();
      localStorage.setItem('student_id', studentId);
    }
    return studentId;
  };

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/courses`);
      setCourses(response.data);
      
      const studentId = getStudentId();
      const stats = {};
      
      for (const course of response.data) {
        try {
          const chaptersRes = await axios.get(`${API}/courses/${course.id}/chapters`);
          const chapters = chaptersRes.data;
          let totalLessons = 0;
          const allLessonIds = [];
          
          for (const chapter of chapters) {
            try {
              const lessonsRes = await axios.get(`${API}/chapters/${chapter.id}/lessons`);
              totalLessons += lessonsRes.data.length;
              lessonsRes.data.forEach(l => allLessonIds.push(l.id));
            } catch (e) {
              console.error('Error fetching lessons:', e);
            }
          }
          
          // Fetch progress for this course
          let completedLessons = 0;
          try {
            const progressRes = await axios.get(`${API}/progress/${studentId}/${course.id}`);
            completedLessons = progressRes.data.completed_lessons?.length || 0;
          } catch (e) {
            // No progress yet
          }
          
          stats[course.id] = {
            chapters: chapters.length,
            lessons: totalLessons,
            completedLessons,
            progress: totalLessons > 0 ? Math.round((completedLessons / totalLessons) * 100) : 0
          };
        } catch (e) {
          stats[course.id] = { chapters: 0, lessons: 0, completedLessons: 0, progress: 0 };
        }
      }
      setCoursesStats(stats);
    } catch (error) {
      console.error('Error fetching courses:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCourseClick = (course) => {
    navigate(`/course/${course.id}`);
  };

  const getLevelColor = (level) => {
    const colors = {
      'Básico': 'bg-green-100 text-green-800',
      'Intermedio': 'bg-blue-100 text-blue-800',
      'Avanzado': 'bg-purple-100 text-purple-800'
    };
    return colors[level] || 'bg-gray-100 text-gray-800';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="animate-spin text-primary" size={32} />
      </div>
    );
  }

  return (
    <div className="space-y-6 pb-24 lg:pb-8" data-testid="biblioteca-page">
      <div>
        <h1 className="text-3xl font-bold">Biblioteca de Cursos</h1>
        <p className="text-slate-600 mt-1">Explora todos los cursos disponibles</p>
      </div>

      {courses.length === 0 ? (
        <Card className="text-center py-12">
          <CardContent>
            <GraduationCap className="mx-auto mb-4 text-slate-400" size={48} />
            <h3 className="text-xl font-semibold mb-2">No hay cursos disponibles</h3>
            <p className="text-slate-500">Los cursos aparecerán aquí cuando estén disponibles</p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses.map((course, index) => {
            const stats = coursesStats[course.id] || { chapters: 0, lessons: 0, completedLessons: 0, progress: 0 };
            return (
              <Card
                key={course.id}
                className="cursor-pointer hover:shadow-lg transition-all course-card"
                onClick={() => handleCourseClick(course)}
                data-testid={`course-card-${index}`}
              >
                <CardHeader>
                  <div className="aspect-video bg-gradient-to-br from-cyan-400 to-cyan-600 rounded-lg mb-4 flex items-center justify-center text-white text-3xl font-bold">
                    {course.title.charAt(0)}
                  </div>
                  <div className="flex items-center justify-between mb-2">
                    <Badge className={getLevelColor(course.level)}>
                      {course.level}
                    </Badge>
                    <div className="flex items-center gap-3 text-sm text-slate-500">
                      <span className="flex items-center gap-1">
                        <Layers size={14} />
                        {stats.chapters}
                      </span>
                      <span className="flex items-center gap-1">
                        <BookOpen size={14} />
                        {stats.lessons}
                      </span>
                    </div>
                  </div>
                  <CardTitle className="text-lg">{course.title}</CardTitle>
                  <CardDescription className="line-clamp-2">
                    {course.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between text-sm mb-3">
                    <span className="text-slate-600">{course.instructor || 'Se Remonta'}</span>
                    <span className="text-xs bg-slate-100 px-2 py-1 rounded">{course.category}</span>
                  </div>
                  
                  {/* Progress bar */}
                  <div className="mb-3">
                    <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
                      <span>Progreso</span>
                      <span>{stats.completedLessons}/{stats.lessons} lecciones</span>
                    </div>
                    <Progress value={stats.progress} className="h-2" />
                  </div>
                  
                  <Button
                    className="w-full"
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(`/course/${course.id}`);
                    }}
                  >
                    {stats.progress === 0 ? 'Comenzar' : stats.progress === 100 ? 'Repasar' : 'Continuar'}
                  </Button>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default Biblioteca;
