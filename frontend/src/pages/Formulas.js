import { useState, useEffect } from 'react';
import axios from 'axios';
import { Search, Calculator as CalcIcon, Loader2 } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Formulas = () => {
  const [formulas, setFormulas] = useState([]);
  const [filteredFormulas, setFilteredFormulas] = useState([]);
  const [courses, setCourses] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCourse, setSelectedCourse] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchCourses();
    searchFormulas();
  }, []);

  useEffect(() => {
    filterFormulas();
  }, [searchQuery, selectedCourse, formulas]);

  const fetchCourses = async () => {
    try {
      const response = await axios.get(`${API}/courses`);
      setCourses(response.data);
    } catch (error) {
      console.error('Error fetching courses:', error);
    }
  };

  const searchFormulas = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API}/formulas/search`, {
        query: '',
        course_id: null
      });
      setFormulas(response.data);
      setFilteredFormulas(response.data);
    } catch (error) {
      console.error('Error fetching formulas:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterFormulas = () => {
    let filtered = [...formulas];

    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(
        f =>
          f.name.toLowerCase().includes(query) ||
          f.topic.toLowerCase().includes(query) ||
          f.description.toLowerCase().includes(query)
      );
    }

    if (selectedCourse) {
      filtered = filtered.filter(f => f.course_id === selectedCourse);
    }

    setFilteredFormulas(filtered);
  };

  return (
    <div className="space-y-6 pb-24 lg:pb-8" data-testid="formulas-page">
      <div>
        <h1 className="text-3xl font-bold">Formulario Inteligente</h1>
        <p className="text-slate-600 mt-1">Encuentra la fórmula exacta en segundos</p>
      </div>

      {/* Search and Filter */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={20} />
          <Input
            placeholder="Buscar fórmulas por nombre o tema..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            data-testid="formula-search-input"
            className="pl-10"
          />
        </div>
        <Select value={selectedCourse} onValueChange={setSelectedCourse}>
          <SelectTrigger data-testid="formula-course-filter">
            <SelectValue placeholder="Filtrar por curso" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Todos los cursos</SelectItem>
            {courses.map(course => (
              <SelectItem key={course.id} value={course.id}>
                {course.title}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Formulas List */}
      {loading ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="animate-spin text-primary" size={32} />
        </div>
      ) : filteredFormulas.length === 0 ? (
        <Card className="text-center py-12">
          <CardContent>
            <CalcIcon className="mx-auto mb-4 text-slate-400" size={48} />
            <h3 className="text-xl font-semibold mb-2">
              {formulas.length === 0 ? 'No hay fórmulas disponibles' : 'No se encontraron fórmulas'}
            </h3>
            <p className="text-slate-500">
              {formulas.length === 0
                ? 'Las fórmulas aparecerán aquí cuando estén disponibles'
                : 'Intenta con otros términos de búsqueda'}
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {filteredFormulas.map((formula, index) => (
            <Card key={formula.id} className="formula-card" data-testid={`formula-card-${index}`}>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="text-xl">{formula.name}</CardTitle>
                    <CardDescription className="mt-1">{formula.topic}</CardDescription>
                  </div>
                  <Badge className="bg-cyan-100 text-cyan-800">
                    {courses.find(c => c.id === formula.course_id)?.title.split(' ')[0] || 'General'}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="bg-white border-2 border-cyan-200 rounded-lg p-4 font-mono text-center text-lg">
                  {formula.latex}
                </div>
                <p className="text-slate-600 leading-relaxed">{formula.description}</p>
                {formula.example && (
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                    <p className="text-sm text-blue-900">
                      <strong>Ejemplo:</strong> {formula.example}
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default Formulas;
