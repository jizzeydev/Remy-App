import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { Checkbox } from '@/components/ui/checkbox';
import { toast } from 'sonner';
import InlineMd from '@/components/course/InlineMd';
import { Plus, Edit, Trash2, ArrowLeft, ArrowUp, ArrowDown, GripVertical, BookOpen, FileText, X, Link2, Unlink, Layers, AlertTriangle, EyeOff, Eye, GitFork, Undo2, ChevronDown, ChevronRight } from 'lucide-react';
import BlockEditor from '@/components/admin/BlockEditor';
import BlockRenderer from '@/components/course/BlockRenderer';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const ADMIN_API = `${BACKEND_URL}/api/admin`;

// Small subcomponent for the "Lecciones excluidas" footer in linked chapters.
// Lazy-fetches the template's lessons so we can show the title of each
// excluded id (otherwise we'd just have UUIDs).
const ExcludedLessonsSection = ({ chapter, templateLessons, onMount, onInclude }) => {
  useEffect(() => {
    onMount?.();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const excludedIds = chapter.excluded_lesson_ids || [];
  if (excludedIds.length === 0) return null;

  const titleFor = (id) => {
    const t = (templateLessons || []).find((l) => l.id === id);
    return t?.title || 'Lección excluida';
  };

  return (
    <div className="mt-3 pt-3 border-t border-dashed border-slate-300 dark:border-slate-700">
      <p className="text-xs text-muted-foreground mb-2 flex items-center gap-1.5">
        <EyeOff size={12} />
        Lecciones excluidas en este curso ({excludedIds.length})
      </p>
      <div className="flex flex-wrap gap-2">
        {excludedIds.map((id) => (
          <button
            key={id}
            type="button"
            onClick={() => onInclude(id)}
            className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs bg-slate-100 dark:bg-slate-800 text-muted-foreground hover:bg-slate-200 dark:hover:bg-slate-700 hover:text-foreground transition-colors"
            title="Re-incluir en este curso"
          >
            <Eye size={11} />
            <span className="truncate max-w-[200px]">{titleFor(id)}</span>
          </button>
        ))}
      </div>
    </div>
  );
};

const CourseContentEditor = () => {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const [course, setCourse] = useState(null);
  const [chapters, setChapters] = useState([]);
  const [loading, setLoading] = useState(false);
  const [chapterDialogOpen, setChapterDialogOpen] = useState(false);
  const [lessonDialogOpen, setLessonDialogOpen] = useState(false);
  const [editingChapter, setEditingChapter] = useState(null);
  const [editingLesson, setEditingLesson] = useState(null);
  const [selectedChapter, setSelectedChapter] = useState(null);

  // Link chapters state — `selectedTemplateChapters` is now an object keyed
  // by template chapter id; the value is the array of EXCLUDED lesson ids
  // for that chapter (empty = include everything). The expand state controls
  // which chapters in the dialog are showing their per-lesson checkboxes.
  const [linkDialogOpen, setLinkDialogOpen] = useState(false);
  const [templateChapters, setTemplateChapters] = useState([]);
  const [selectedTemplateChapters, setSelectedTemplateChapters] = useState({});
  const [expandedTemplateChapters, setExpandedTemplateChapters] = useState({});
  const [linking, setLinking] = useState(false);

  // For each linked chapter we may show its excluded lessons (so the admin
  // can re-include them). This lazily-fetched cache holds the template
  // chapter's lessons by template_chapter_id.
  const [templateLessonsCache, setTemplateLessonsCache] = useState({});

  const [chapterForm, setChapterForm] = useState({
    title: '',
    description: '',
    order: 1
  });

  const [lessonForm, setLessonForm] = useState({
    title: '',
    blocks: [],
    order: 1,
    duration_minutes: 30
  });

  useEffect(() => {
    fetchCourse();
    fetchChapters();
  }, [courseId]);

  const fetchCourse = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/api/courses/${courseId}`);
      setCourse(response.data);
    } catch (error) {
      console.error('Error fetching course:', error);
      toast.error('Error al cargar curso');
    }
  };

  const fetchChapters = async () => {
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.get(`${ADMIN_API}/courses/${courseId}/chapters`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      // Fetch lessons for each chapter
      const chaptersWithLessons = await Promise.all(
        response.data.map(async (chapter) => {
          const lessonsResponse = await axios.get(`${ADMIN_API}/chapters/${chapter.id}/lessons`, {
            headers: { Authorization: `Bearer ${token}` }
          });
          return { ...chapter, lessons: lessonsResponse.data };
        })
      );
      
      setChapters(chaptersWithLessons);
    } catch (error) {
      console.error('Error fetching chapters:', error);
      toast.error('Error al cargar capítulos');
    }
  };

  const handleSaveChapter = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const token = localStorage.getItem('admin_token');
      const payload = {
        ...chapterForm,
        course_id: courseId,
        id: editingChapter?.id || undefined
      };

      if (editingChapter) {
        await axios.put(`${ADMIN_API}/chapters/${editingChapter.id}`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Capítulo actualizado');
      } else {
        await axios.post(`${ADMIN_API}/chapters`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Capítulo creado');
      }

      fetchChapters();
      setChapterDialogOpen(false);
      resetChapterForm();
    } catch (error) {
      console.error('Error saving chapter:', error);
      toast.error('Error al guardar capítulo');
    } finally {
      setLoading(false);
    }
  };

  // Move a chapter up or down by swapping with its neighbor and persisting
  // the new order. Works on both linked and owned chapters because order
  // lives on the local chapter doc, not the template.
  const handleReorderChapter = async (chapterId, direction) => {
    const idx = chapters.findIndex((c) => c.id === chapterId);
    if (idx === -1) return;
    const targetIdx = direction === 'up' ? idx - 1 : idx + 1;
    if (targetIdx < 0 || targetIdx >= chapters.length) return;

    const next = [...chapters];
    [next[idx], next[targetIdx]] = [next[targetIdx], next[idx]];
    // Optimistic local update with refreshed `order` numbers so the UI doesn't flicker.
    setChapters(next.map((c, i) => ({ ...c, order: i + 1 })));

    try {
      const token = localStorage.getItem('admin_token');
      await axios.post(
        `${ADMIN_API}/courses/${courseId}/reorder-chapters`,
        { chapter_ids: next.map((c) => c.id) },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      // Refetch to pull canonical order from server.
      fetchChapters();
    } catch (error) {
      console.error('Error reordering chapters:', error);
      toast.error('Error al reordenar capítulos');
      fetchChapters();
    }
  };

  const handleDeleteChapter = async (chapterId) => {
    if (!window.confirm('¿Eliminar este capítulo y todas sus lecciones?')) return;

    try {
      const token = localStorage.getItem('admin_token');
      await axios.delete(`${ADMIN_API}/chapters/${chapterId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      toast.success('Capítulo eliminado');
      fetchChapters();
    } catch (error) {
      console.error('Error deleting chapter:', error);
      toast.error('Error al eliminar capítulo');
    }
  };

  const handleSaveLesson = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const token = localStorage.getItem('admin_token');
      const payload = {
        ...lessonForm,
        chapter_id: selectedChapter.id,
        id: editingLesson?.id || undefined
      };

      if (editingLesson) {
        await axios.put(`${ADMIN_API}/lessons/${editingLesson.id}`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Lección actualizada');
      } else {
        await axios.post(`${ADMIN_API}/lessons`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Lección creada');
      }

      fetchChapters();
      setLessonDialogOpen(false);
      resetLessonForm();
    } catch (error) {
      console.error('Error saving lesson:', error);
      toast.error('Error al guardar lección');
    } finally {
      setLoading(false);
    }
  };

  // Smart delete: dispatches based on what kind of lesson this is inside a
  // (possibly linked) chapter.
  //   - Inherited (template lesson surfaced through linkage) → exclude from
  //     this course (template stays untouched in General).
  //   - Override (a fork): "delete" reverts to the template by removing the
  //     local override doc.
  //   - Pure local lesson on a linked chapter, or any lesson on a non-linked
  //     chapter: real DELETE (moves to trash).
  const handleDeleteLesson = async (chapter, lesson) => {
    const token = localStorage.getItem('admin_token');
    const headers = { Authorization: `Bearer ${token}` };

    try {
      if (chapter.is_linked && lesson.inherited_from_template && !lesson.overrides_template) {
        if (!window.confirm(`¿Excluir "${lesson.title}" de este curso? La lección queda intacta en el curso general.`)) return;
        await axios.post(
          `${ADMIN_API}/chapters/${chapter.id}/exclude-lessons`,
          { ids: [lesson.id] },
          { headers }
        );
        toast.success('Lección excluida de este curso');
      } else if (lesson.overrides_template) {
        if (!window.confirm('¿Revertir esta lección a la versión del curso general? Se perderán los cambios locales.')) return;
        await axios.delete(`${ADMIN_API}/lessons/${lesson.id}`, { headers });
        toast.success('Revertido a la versión general');
      } else {
        if (!window.confirm('¿Eliminar esta lección?')) return;
        await axios.delete(`${ADMIN_API}/lessons/${lesson.id}`, { headers });
        toast.success('Lección eliminada');
      }
      fetchChapters();
    } catch (error) {
      console.error('Error deleting lesson:', error);
      toast.error(error.response?.data?.detail || 'Error al eliminar lección');
    }
  };

  // Re-include a previously-excluded lesson on a linked chapter.
  const handleIncludeLesson = async (chapterId, lessonId) => {
    try {
      const token = localStorage.getItem('admin_token');
      await axios.post(
        `${ADMIN_API}/chapters/${chapterId}/include-lessons`,
        { ids: [lessonId] },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      toast.success('Lección re-incluida');
      fetchChapters();
    } catch (error) {
      console.error('Error including lesson:', error);
      toast.error(error.response?.data?.detail || 'Error al re-incluir');
    }
  };

  // Fork an inherited lesson, then open the editor on the new override.
  // Idempotent server-side, so calling it multiple times returns the same fork.
  const handleForkAndEditLesson = async (chapter, templateLesson) => {
    try {
      const token = localStorage.getItem('admin_token');
      const res = await axios.post(
        `${ADMIN_API}/chapters/${chapter.id}/fork-lesson/${templateLesson.id}`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      const fork = res.data.lesson;
      if (res.data.created) {
        toast.success('Lección clonada localmente, ahora podés editarla.');
      }
      // Refresh and open the editor on the new override.
      await fetchChapters();
      openEditLesson(chapter, fork);
    } catch (error) {
      console.error('Error forking lesson:', error);
      toast.error(error.response?.data?.detail || 'Error al clonar lección');
    }
  };

  // Lazy-fetch the template chapter's lessons so we can show titles for
  // excluded-lesson chips in the per-chapter UI.
  const ensureTemplateLessons = async (templateChapterId) => {
    if (!templateChapterId || templateLessonsCache[templateChapterId]) return;
    try {
      const token = localStorage.getItem('admin_token');
      const res = await axios.get(`${ADMIN_API}/chapters/${templateChapterId}/lessons`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setTemplateLessonsCache((prev) => ({ ...prev, [templateChapterId]: res.data || [] }));
    } catch (e) { /* silent */ }
  };

  const openAddChapter = () => {
    resetChapterForm();
    setChapterDialogOpen(true);
  };

  const openEditChapter = (chapter) => {
    setEditingChapter(chapter);
    setChapterForm({
      title: chapter.title,
      description: chapter.description,
      order: chapter.order
    });
    setChapterDialogOpen(true);
  };

  const openAddLesson = (chapter) => {
    setSelectedChapter(chapter);
    resetLessonForm();
    setLessonDialogOpen(true);
  };

  const openEditLesson = (chapter, lesson) => {
    // If the user clicks edit on an inherited lesson, transparently fork it
    // first — never mutate the General-course lesson by accident.
    if (chapter.is_linked && lesson.inherited_from_template && !lesson.overrides_template) {
      handleForkAndEditLesson(chapter, lesson);
      return;
    }
    setSelectedChapter(chapter);
    setEditingLesson(lesson);
    setLessonForm({
      title: lesson.title,
      blocks: Array.isArray(lesson.blocks) ? lesson.blocks : [],
      order: lesson.order,
      duration_minutes: lesson.duration_minutes
    });
    setLessonDialogOpen(true);
  };

  const resetChapterForm = () => {
    setEditingChapter(null);
    setChapterForm({ title: '', description: '', order: chapters.length + 1 });
  };

  const resetLessonForm = () => {
    setEditingLesson(null);
    setLessonForm({ title: '', blocks: [], order: 1, duration_minutes: 30 });
  };

  if (!course) return <div>Cargando...</div>;

  // Check if this is a university course (can link chapters)
  const isUniversityCourse = course.university_id !== null && course.university_id !== undefined;

  // Fetch template chapters when link dialog opens
  const openLinkDialog = async () => {
    setLinkDialogOpen(true);
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.get(`${ADMIN_API}/template-chapters`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setTemplateChapters(response.data);
      setSelectedTemplateChapters({});
      setExpandedTemplateChapters({});
    } catch (error) {
      console.error('Error fetching templates:', error);
      toast.error('Error al cargar plantillas');
    }
  };

  const handleLinkChapters = async () => {
    const entries = Object.entries(selectedTemplateChapters);
    if (entries.length === 0) {
      toast.error('Selecciona al menos un capítulo');
      return;
    }

    setLinking(true);
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.post(
        `${ADMIN_API}/courses/${courseId}/link-chapters`,
        {
          chapters: entries.map(([template_chapter_id, excluded_lesson_ids]) => ({
            template_chapter_id,
            excluded_lesson_ids: excluded_lesson_ids || []
          }))
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      if (response.data.errors?.length > 0) {
        toast.warning(`Vinculados ${response.data.linked_chapters.length} capítulos. Errores: ${response.data.errors.join(', ')}`);
      } else {
        toast.success(`Vinculados ${response.data.linked_chapters.length} capítulos`);
      }

      setLinkDialogOpen(false);
      fetchChapters();
    } catch (error) {
      console.error('Error linking chapters:', error);
      toast.error(error.response?.data?.detail || 'Error al vincular capítulos');
    } finally {
      setLinking(false);
    }
  };

  const handleUnlinkChapter = async (chapterId) => {
    if (!window.confirm('¿Desvincular este capítulo? Se copiará el contenido y será independiente.')) return;

    try {
      const token = localStorage.getItem('admin_token');
      await axios.post(
        `${ADMIN_API}/chapters/${chapterId}/unlink`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      toast.success('Capítulo desvinculado. Ahora es independiente.');
      fetchChapters();
    } catch (error) {
      console.error('Error unlinking chapter:', error);
      toast.error(error.response?.data?.detail || 'Error al desvincular');
    }
  };

  // Toggle whether a template chapter is selected for linking. Selected →
  // entry exists with [] excluded (= include all lessons by default).
  const toggleTemplateChapter = (chapterId) => {
    setSelectedTemplateChapters((prev) => {
      if (chapterId in prev) {
        const next = { ...prev };
        delete next[chapterId];
        return next;
      }
      return { ...prev, [chapterId]: [] };
    });
  };

  // Toggle one specific lesson in/out of the per-chapter exclusion list.
  const toggleTemplateLesson = (chapterId, lessonId) => {
    setSelectedTemplateChapters((prev) => {
      const current = prev[chapterId] || [];
      // If chapter wasn't selected yet, auto-select it with the lesson INCLUDED
      // (excluded = all-other-lessons + leaves this one in).
      if (!(chapterId in prev)) return { ...prev, [chapterId]: [] };
      const isExcluded = current.includes(lessonId);
      const next = isExcluded
        ? current.filter((id) => id !== lessonId)
        : [...current, lessonId];
      return { ...prev, [chapterId]: next };
    });
  };

  const toggleExpandTemplateChapter = (chapterId) => {
    setExpandedTemplateChapters((prev) => ({ ...prev, [chapterId]: !prev[chapterId] }));
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" onClick={() => navigate('/admin/courses')}>
          <ArrowLeft size={20} className="mr-2" />
          Volver
        </Button>
        <div className="flex-1">
          <h1 className="text-3xl font-bold">{course.title}</h1>
          <p className="text-slate-600 dark:text-slate-400">
            Editar contenido del curso
            {course.university && course.university.short_name !== 'GEN' && (
              <Badge variant="outline" className="ml-2">{course.university.short_name}</Badge>
            )}
          </p>
        </div>
        <div className="flex gap-2">
          {isUniversityCourse && (
            <Button variant="outline" onClick={openLinkDialog}>
              <Link2 size={20} className="mr-2" />
              Vincular Plantillas
            </Button>
          )}
          <Button onClick={openAddChapter}>
            <Plus size={20} className="mr-2" />
            Nuevo Capítulo
          </Button>
        </div>
      </div>

      {/* Info banner for university courses */}
      {isUniversityCourse && (
        <Card className="bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800">
          <CardContent className="py-3">
            <p className="text-sm text-blue-800 dark:text-blue-200 flex items-center gap-2">
              <Link2 size={16} />
              <span>
                <strong>Curso universitario:</strong> Puedes vincular capítulos de cursos Generales (plantillas). 
                Los cambios en las plantillas se reflejarán automáticamente aquí.
              </span>
            </p>
          </CardContent>
        </Card>
      )}

      <div className="space-y-4">
        {chapters.length === 0 ? (
          <Card>
            <CardContent className="text-center py-12">
              <BookOpen className="mx-auto mb-4 text-slate-400" size={48} />
              <h3 className="text-xl font-semibold mb-2">No hay capítulos</h3>
              <p className="text-slate-500 mb-4">
                {isUniversityCourse 
                  ? 'Vincula capítulos de plantillas o crea uno nuevo'
                  : 'Comienza agregando el primer capítulo'
                }
              </p>
              <div className="flex gap-2 justify-center">
                {isUniversityCourse && (
                  <Button variant="outline" onClick={openLinkDialog}>
                    <Link2 size={16} className="mr-2" />
                    Vincular Plantillas
                  </Button>
                )}
                <Button onClick={openAddChapter}>Crear Capítulo</Button>
              </div>
            </CardContent>
          </Card>
        ) : (
          chapters.map((chapter, chapterIndex) => (
            <Card key={chapter.id} className={chapter.is_linked ? 'border-blue-300 dark:border-blue-700' : ''}>
              <CardHeader className={chapter.is_linked ? 'bg-blue-50 dark:bg-blue-900/20' : 'bg-slate-50 dark:bg-slate-800/50'}>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="flex flex-col gap-0.5">
                      <Button
                        size="icon"
                        variant="ghost"
                        className="h-6 w-6"
                        onClick={() => handleReorderChapter(chapter.id, 'up')}
                        disabled={chapterIndex === 0}
                        title="Subir capítulo"
                      >
                        <ArrowUp size={14} />
                      </Button>
                      <Button
                        size="icon"
                        variant="ghost"
                        className="h-6 w-6"
                        onClick={() => handleReorderChapter(chapter.id, 'down')}
                        disabled={chapterIndex === chapters.length - 1}
                        title="Bajar capítulo"
                      >
                        <ArrowDown size={14} />
                      </Button>
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <CardTitle className="text-lg">
                          Capítulo {chapter.order}: {chapter.title}
                        </CardTitle>
                        {chapter.is_linked && (
                          <Badge variant="secondary" className="bg-blue-100 text-blue-700 dark:bg-blue-800 dark:text-blue-200">
                            <Link2 size={12} className="mr-1" />
                            Vinculado
                          </Badge>
                        )}
                      </div>
                      <p className="text-sm text-slate-600 dark:text-slate-400 mt-1"><InlineMd>{chapter.description}</InlineMd></p>
                      {chapter.template_info && (
                        <p className="text-xs text-blue-600 dark:text-blue-400 mt-1">
                          Plantilla: {chapter.template_info.course_title}
                        </p>
                      )}
                    </div>
                  </div>
                  <div className="flex gap-2">
                    {/* Add lesson is always available; on linked chapters it
                        creates a course-specific lesson (not in the template). */}
                    <Button size="sm" variant="outline" onClick={() => openAddLesson(chapter)}>
                      <Plus size={16} className="mr-1" />
                      Lección
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => openEditChapter(chapter)}
                      title={chapter.is_linked ? 'Editar título/orden de este curso (no afecta el general)' : 'Editar capítulo'}
                    >
                      <Edit size={16} />
                    </Button>
                    {chapter.is_linked && (
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => handleUnlinkChapter(chapter.id)}
                        title="Desvincular y hacer independiente (deep copy)"
                      >
                        <Unlink size={16} className="mr-1" />
                        Desvincular
                      </Button>
                    )}
                    <Button size="sm" variant="destructive" onClick={() => handleDeleteChapter(chapter.id)}>
                      <Trash2 size={16} />
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="pt-4">
                {chapter.lessons?.length === 0 && !(chapter.excluded_lesson_ids?.length) ? (
                  <div className="text-center py-8 text-slate-500">
                    <FileText className="mx-auto mb-2 text-slate-400" size={32} />
                    <p className="text-sm">No hay lecciones en este capítulo</p>
                  </div>
                ) : (
                  <div className="space-y-2">
                    {chapter.lessons?.map((lesson) => {
                      const isInherited = lesson.inherited_from_template;
                      const isOverride = lesson.overrides_template;
                      const isPureLocal = chapter.is_linked && !isInherited && !isOverride;

                      return (
                        <div
                          key={lesson.id}
                          className={`flex items-center justify-between p-3 border rounded-lg transition-colors ${
                            isOverride
                              ? 'border-amber-300 dark:border-amber-700 bg-amber-50/50 dark:bg-amber-900/10 hover:bg-amber-50 dark:hover:bg-amber-900/20'
                              : 'border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800/50'
                          }`}
                        >
                          <div className="flex items-center gap-3 min-w-0 flex-1">
                            <GripVertical className="text-slate-400 flex-shrink-0" size={16} />
                            <FileText className="text-primary flex-shrink-0" size={20} />
                            <div className="min-w-0 flex-1">
                              <div className="flex items-center gap-2 flex-wrap">
                                <p className="font-medium truncate">{lesson.title}</p>
                                {isInherited && !isOverride && (
                                  <Badge variant="secondary" className="text-[10px] bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300">
                                    <Link2 size={10} className="mr-0.5" /> Heredada
                                  </Badge>
                                )}
                                {isOverride && (
                                  <Badge variant="secondary" className="text-[10px] bg-amber-100 dark:bg-amber-900/40 text-amber-700 dark:text-amber-300">
                                    <GitFork size={10} className="mr-0.5" /> Editada localmente
                                  </Badge>
                                )}
                                {isPureLocal && (
                                  <Badge variant="secondary" className="text-[10px] bg-emerald-100 dark:bg-emerald-900/40 text-emerald-700 dark:text-emerald-300">
                                    Específica de este curso
                                  </Badge>
                                )}
                              </div>
                              <p className="text-xs text-slate-500">{lesson.duration_minutes} min</p>
                            </div>
                          </div>
                          <div className="flex gap-2 flex-shrink-0">
                            <Button
                              size="sm"
                              variant="ghost"
                              onClick={() => openEditLesson(chapter, lesson)}
                              title={isInherited && !isOverride ? 'Clonar localmente y editar' : 'Editar'}
                            >
                              {isInherited && !isOverride ? <GitFork size={14} /> : <Edit size={14} />}
                            </Button>
                            <Button
                              size="sm"
                              variant="ghost"
                              onClick={() => handleDeleteLesson(chapter, lesson)}
                              title={
                                isInherited && !isOverride
                                  ? 'Excluir de este curso (no afecta general)'
                                  : isOverride
                                  ? 'Revertir a versión general'
                                  : 'Eliminar'
                              }
                            >
                              {isInherited && !isOverride ? <EyeOff size={14} /> : isOverride ? <Undo2 size={14} /> : <Trash2 size={14} />}
                            </Button>
                          </div>
                        </div>
                      );
                    })}

                    {/* Excluded lessons (linked chapters only) — let the admin
                        re-include them. Lazy-loads template lesson titles. */}
                    {chapter.is_linked && (chapter.excluded_lesson_ids?.length || 0) > 0 && (
                      <ExcludedLessonsSection
                        chapter={chapter}
                        templateLessons={templateLessonsCache[chapter.template_chapter_id]}
                        onMount={() => ensureTemplateLessons(chapter.template_chapter_id)}
                        onInclude={(lessonId) => handleIncludeLesson(chapter.id, lessonId)}
                      />
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          ))
        )}
      </div>

      {/* Chapter Dialog */}
      <Dialog open={chapterDialogOpen} onOpenChange={setChapterDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{editingChapter ? 'Editar Capítulo' : 'Nuevo Capítulo'}</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSaveChapter} className="space-y-4">
            <div>
              <Label>Título</Label>
              <Input
                value={chapterForm.title}
                onChange={(e) => setChapterForm({ ...chapterForm, title: e.target.value })}
                required
              />
            </div>
            <div>
              <Label>Descripción</Label>
              <Textarea
                value={chapterForm.description}
                onChange={(e) => setChapterForm({ ...chapterForm, description: e.target.value })}
                required
              />
            </div>
            <div>
              <Label>Orden</Label>
              <Input
                type="number"
                value={chapterForm.order}
                onChange={(e) => setChapterForm({ ...chapterForm, order: parseInt(e.target.value) })}
                min={1}
                required
              />
            </div>
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? 'Guardando...' : editingChapter ? 'Actualizar' : 'Crear'}
            </Button>
          </form>
        </DialogContent>
      </Dialog>

      {/* Lesson Dialog */}
      <Dialog open={lessonDialogOpen} onOpenChange={setLessonDialogOpen}>
        <DialogContent className="max-h-[90vh] overflow-y-auto max-w-5xl">
          <DialogHeader>
            <DialogTitle>
              {editingLesson ? 'Editar Lección' : 'Nueva Lección'} - {selectedChapter?.title}
            </DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSaveLesson} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label>Título de la Lección</Label>
                <Input
                  value={lessonForm.title}
                  onChange={(e) => setLessonForm({ ...lessonForm, title: e.target.value })}
                  required
                />
              </div>
              <div>
                <Label>Duración (minutos)</Label>
                <Input
                  type="number"
                  value={lessonForm.duration_minutes}
                  onChange={(e) => setLessonForm({ ...lessonForm, duration_minutes: parseInt(e.target.value) })}
                  min={1}
                  required
                />
              </div>
            </div>

            {/* Editor Layout - 2 cols (block editor + preview) */}
            <div className="grid gap-4 grid-cols-1 lg:grid-cols-2">
              {/* Block editor */}
              <div>
                <Label className="mb-2 block">Bloques de la lección</Label>
                <div className="border rounded-lg p-3 max-h-[600px] overflow-y-auto bg-secondary/20">
                  <BlockEditor
                    blocks={lessonForm.blocks}
                    onChange={(blocks) => setLessonForm({ ...lessonForm, blocks })}
                  />
                </div>
              </div>

              {/* Preview */}
              <div>
                <Label className="mb-2 block">Vista previa (alumno)</Label>
                <div className="border rounded-lg p-4 max-h-[600px] overflow-y-auto bg-background">
                  <BlockRenderer blocks={lessonForm.blocks} />
                </div>
              </div>
            </div>

            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? 'Guardando...' : editingLesson ? 'Actualizar Lección' : 'Crear Lección'}
            </Button>
          </form>
        </DialogContent>
      </Dialog>

      {/* Link Chapters Dialog — granular: each chapter can be expanded to
          select which lessons to bring. Unselected lessons end up in the
          chapter's `excluded_lesson_ids` so the General course is unaffected. */}
      <Dialog open={linkDialogOpen} onOpenChange={setLinkDialogOpen}>
        <DialogContent className="max-w-3xl max-h-[85vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Link2 size={20} />
              Vincular Capítulos de Plantillas
            </DialogTitle>
            <DialogDescription>
              Selecciona capítulos de cursos Generales y, opcionalmente, qué lecciones
              traer. Lo que NO marques se "excluye" en este curso pero queda intacto
              en el general. Los cambios en las plantillas se reflejan automáticamente.
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4 mt-4">
            {templateChapters.length === 0 ? (
              <div className="text-center py-8">
                <Layers className="mx-auto mb-4 text-slate-400" size={48} />
                <p className="text-slate-500">No hay capítulos en cursos Generales</p>
                <p className="text-sm text-slate-400">Crea capítulos en cursos sin universidad asignada</p>
              </div>
            ) : (
              templateChapters.map((courseGroup) => (
                <Card key={courseGroup.course.id}>
                  <CardHeader className="py-3">
                    <CardTitle className="text-base flex items-center gap-2">
                      <BookOpen size={16} />
                      {courseGroup.course.title}
                      <Badge variant="secondary" className="text-xs">General</Badge>
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="pt-0">
                    <div className="space-y-2">
                      {courseGroup.chapters.map((chapter) => {
                        const isSelected = chapter.id in selectedTemplateChapters;
                        const excludedLessonIds = selectedTemplateChapters[chapter.id] || [];
                        const isAlreadyLinked = chapters.some((c) => c.template_chapter_id === chapter.id);
                        const isExpanded = !!expandedTemplateChapters[chapter.id];
                        const lessons = chapter.lessons || [];
                        const includedCount = lessons.length - excludedLessonIds.length;

                        return (
                          <div
                            key={chapter.id}
                            className={`border rounded-lg transition-colors ${
                              isAlreadyLinked
                                ? 'bg-slate-100 dark:bg-slate-800 opacity-60'
                                : isSelected
                                ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                                : 'hover:bg-slate-50 dark:hover:bg-slate-800/50'
                            }`}
                          >
                            <div className="flex items-center gap-3 p-3">
                              <Checkbox
                                id={chapter.id}
                                checked={isSelected}
                                onCheckedChange={() => !isAlreadyLinked && toggleTemplateChapter(chapter.id)}
                                disabled={isAlreadyLinked}
                              />
                              <label htmlFor={chapter.id} className="flex-1 cursor-pointer min-w-0">
                                <div className="font-medium truncate">{chapter.title}</div>
                                <div className="text-xs text-slate-500 flex gap-3 mt-1">
                                  <span>
                                    {isSelected
                                      ? `${includedCount}/${lessons.length} lecciones`
                                      : `${lessons.length} lecciones`}
                                  </span>
                                  <span>{chapter.question_count || 0} preguntas</span>
                                </div>
                              </label>
                              {isAlreadyLinked ? (
                                <Badge variant="secondary" className="text-xs">Ya vinculado</Badge>
                              ) : (
                                lessons.length > 0 && (
                                  <Button
                                    type="button"
                                    size="sm"
                                    variant="ghost"
                                    onClick={(e) => {
                                      e.stopPropagation();
                                      toggleExpandTemplateChapter(chapter.id);
                                    }}
                                    title={isExpanded ? 'Ocultar lecciones' : 'Elegir lecciones específicas'}
                                  >
                                    {isExpanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                                  </Button>
                                )
                              )}
                            </div>

                            {/* Per-lesson granular selection */}
                            {isSelected && isExpanded && lessons.length > 0 && (
                              <div className="border-t border-blue-200 dark:border-blue-800 px-3 py-2 space-y-1.5 bg-background/50">
                                {lessons.map((l) => {
                                  const isExcluded = excludedLessonIds.includes(l.id);
                                  return (
                                    <label
                                      key={l.id}
                                      className="flex items-center gap-2.5 px-2 py-1.5 rounded hover:bg-slate-100 dark:hover:bg-slate-800 cursor-pointer"
                                    >
                                      <Checkbox
                                        checked={!isExcluded}
                                        onCheckedChange={() => toggleTemplateLesson(chapter.id, l.id)}
                                      />
                                      <FileText size={14} className="text-muted-foreground flex-shrink-0" />
                                      <span className={`text-sm flex-1 truncate ${isExcluded ? 'line-through text-muted-foreground' : ''}`}>
                                        {l.title}
                                      </span>
                                      <span className="text-xs text-muted-foreground tabular-nums flex-shrink-0">
                                        {l.duration_minutes || 0} min
                                      </span>
                                    </label>
                                  );
                                })}
                              </div>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </div>

          <DialogFooter className="mt-4">
            <Button variant="outline" onClick={() => setLinkDialogOpen(false)}>
              Cancelar
            </Button>
            <Button
              onClick={handleLinkChapters}
              disabled={Object.keys(selectedTemplateChapters).length === 0 || linking}
            >
              {linking ? 'Vinculando...' : `Vincular ${Object.keys(selectedTemplateChapters).length} capítulo(s)`}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default CourseContentEditor;
