import { useState, useEffect, useMemo } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';
import { Loader2, Search, X, Layers, GraduationCap, BookOpen } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ANY = '__any__';

const AdminSplits = () => {
  const [loading, setLoading] = useState(true);
  const [rows, setRows] = useState([]);
  const [universities, setUniversities] = useState([]);
  const [baseCourses, setBaseCourses] = useState([]);
  const [totals, setTotals] = useState({ courses: 0, complete: 0, partial: 0, alto: 0, medio: 0 });

  // Filtros
  const [uniFilter, setUniFilter] = useState(ANY);
  const [baseFilter, setBaseFilter] = useState(ANY);
  const [matchFilter, setMatchFilter] = useState(ANY);
  const [coverageFilter, setCoverageFilter] = useState(ANY);
  const [search, setSearch] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('admin_token');
    if (!token) {
      toast.error('Sesión no iniciada');
      return;
    }
    setLoading(true);
    axios
      .get(`${API}/admin/splits-courses`, { headers: { Authorization: `Bearer ${token}` } })
      .then(({ data }) => {
        setRows(data.courses || []);
        setUniversities(data.universities || []);
        setBaseCourses(data.base_courses || []);
        setTotals(data.totals || { courses: 0, complete: 0, partial: 0, alto: 0, medio: 0 });
      })
      .catch((err) => {
        toast.error('Error cargando splits: ' + (err.response?.data?.detail || err.message));
      })
      .finally(() => setLoading(false));
  }, []);

  const filtered = useMemo(() => {
    const q = search.trim().toLowerCase();
    return rows.filter((r) => {
      if (uniFilter !== ANY && r.university_short_name !== uniFilter) return false;
      if (baseFilter !== ANY && !(r.base_course_ids || []).includes(baseFilter)) return false;
      if (matchFilter !== ANY && r.match_level !== matchFilter) return false;
      if (coverageFilter !== ANY && r.coverage_status !== coverageFilter) return false;
      if (q) {
        const hay =
          (r.title || '').toLowerCase().includes(q) ||
          (r.id || '').toLowerCase().includes(q) ||
          (r.code || '').toLowerCase().includes(q);
        if (!hay) return false;
      }
      return true;
    });
  }, [rows, uniFilter, baseFilter, matchFilter, coverageFilter, search]);

  const clearFilters = () => {
    setUniFilter(ANY);
    setBaseFilter(ANY);
    setMatchFilter(ANY);
    setCoverageFilter(ANY);
    setSearch('');
  };

  const anyFilterActive =
    uniFilter !== ANY ||
    baseFilter !== ANY ||
    matchFilter !== ANY ||
    coverageFilter !== ANY ||
    search.trim() !== '';

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="animate-spin" size={32} />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-1">Splits universitarios</h1>
        <p className="text-muted-foreground">
          {totals.courses} cursos universitarios derivados de los cursos base de Remy.
        </p>
      </div>

      {/* Stat cards */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        <StatCard label="Total" value={totals.courses} icon={GraduationCap} />
        <StatCard label="Cobertura completa" value={totals.complete} accent="emerald" />
        <StatCard label="Cobertura parcial" value={totals.partial} accent="amber" />
        <StatCard label="Match alto" value={totals.alto} />
        <StatCard label="Match medio" value={totals.medio} />
      </div>

      {/* Filters */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-lg flex items-center gap-2">
            <Search size={18} /> Filtros
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-3">
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">Buscar (título / código / id)</label>
              <Input
                placeholder="ej. MA1102, álgebra..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">Universidad</label>
              <Select value={uniFilter} onValueChange={setUniFilter}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value={ANY}>Todas ({rows.length})</SelectItem>
                  {universities.map((u) => (
                    <SelectItem key={u.short_name} value={u.short_name}>
                      {u.short_name} (T{u.tier ?? '?'}) — {u.courses_count}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">Curso base</label>
              <Select value={baseFilter} onValueChange={setBaseFilter}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value={ANY}>Todos</SelectItem>
                  {baseCourses.map((b) => (
                    <SelectItem key={b.id} value={b.id}>
                      {b.title} ({b.courses_count})
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">Match</label>
              <Select value={matchFilter} onValueChange={setMatchFilter}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value={ANY}>Cualquiera</SelectItem>
                  <SelectItem value="alto">Alto</SelectItem>
                  <SelectItem value="medio">Medio</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">Cobertura</label>
              <Select value={coverageFilter} onValueChange={setCoverageFilter}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value={ANY}>Cualquiera</SelectItem>
                  <SelectItem value="complete">Completa</SelectItem>
                  <SelectItem value="partial">Parcial</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <div className="mt-3 flex items-center gap-3">
            <span className="text-sm text-muted-foreground">
              Mostrando <strong>{filtered.length}</strong> de {rows.length}
            </span>
            {anyFilterActive && (
              <Button variant="ghost" size="sm" onClick={clearFilters}>
                <X size={14} className="mr-1" /> Limpiar filtros
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Tabla */}
      <Card>
        <CardContent className="p-0 overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-muted/40 text-left">
              <tr>
                <th className="px-3 py-2 font-medium">U</th>
                <th className="px-3 py-2 font-medium">Curso</th>
                <th className="px-3 py-2 font-medium">Código</th>
                <th className="px-3 py-2 font-medium">Sem</th>
                <th className="px-3 py-2 font-medium">Base</th>
                <th className="px-3 py-2 font-medium">Match</th>
                <th className="px-3 py-2 font-medium">Cobertura</th>
                <th className="px-3 py-2 font-medium text-right">Caps</th>
                <th className="px-3 py-2 font-medium text-right">Ejes</th>
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 && (
                <tr>
                  <td colSpan={9} className="px-3 py-10 text-center text-muted-foreground">
                    Ningún curso con los filtros aplicados.
                  </td>
                </tr>
              )}
              {filtered.map((r) => (
                <tr key={r.id} className="border-t hover:bg-muted/30">
                  <td className="px-3 py-2 whitespace-nowrap">
                    <Badge variant="outline" className="font-mono text-xs">
                      {r.university_short_name}
                    </Badge>
                  </td>
                  <td className="px-3 py-2">
                    <div className="font-medium">{r.title}</div>
                    <div className="text-xs text-muted-foreground font-mono">{r.id}</div>
                  </td>
                  <td className="px-3 py-2 font-mono text-xs">{r.code || '—'}</td>
                  <td className="px-3 py-2">{r.semester ?? '—'}</td>
                  <td className="px-3 py-2 max-w-[280px]">
                    <div className="flex flex-wrap gap-1">
                      {(r.base_course_titles || []).map((t, i) => (
                        <Badge key={i} variant="secondary" className="text-xs">
                          {t}
                        </Badge>
                      ))}
                    </div>
                  </td>
                  <td className="px-3 py-2">
                    <Badge variant={r.match_level === 'alto' ? 'default' : 'outline'} className="text-xs">
                      {r.match_level}
                    </Badge>
                  </td>
                  <td className="px-3 py-2">
                    <Badge
                      variant={r.coverage_status === 'complete' ? 'default' : 'outline'}
                      className={
                        r.coverage_status === 'complete'
                          ? 'bg-emerald-100 text-emerald-700 hover:bg-emerald-100 border-emerald-200'
                          : 'bg-amber-100 text-amber-700 hover:bg-amber-100 border-amber-200'
                      }
                    >
                      {r.coverage_status === 'complete' ? 'Completa' : 'Parcial'}
                    </Badge>
                  </td>
                  <td className="px-3 py-2 text-right text-muted-foreground">{r.chapters_count}</td>
                  <td className="px-3 py-2 text-right text-muted-foreground">{r.axes_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </CardContent>
      </Card>
    </div>
  );
};

const StatCard = ({ label, value, icon: Icon, accent }) => {
  const accents = {
    emerald: 'text-emerald-600 dark:text-emerald-400',
    amber: 'text-amber-600 dark:text-amber-400',
  };
  return (
    <Card>
      <CardContent className="p-4">
        <div className="flex items-center gap-2 text-xs text-muted-foreground mb-1">
          {Icon && <Icon size={14} />}
          {label}
        </div>
        <div className={`text-2xl font-bold ${accent ? accents[accent] : ''}`}>{value}</div>
      </CardContent>
    </Card>
  );
};

export default AdminSplits;
