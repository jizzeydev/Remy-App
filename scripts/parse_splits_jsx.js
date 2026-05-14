#!/usr/bin/env node
/**
 * Parsea un archivo .jsx de investigación de splits (docs/splits-data/*.jsx)
 * y dumpea a stdout un JSON con:
 *   {
 *     sigla: "UAI",
 *     base_courses: [...seRemontaCursos del .jsx],
 *     carreras: [...carreras del .jsx]
 *   }
 *
 * Por qué Node y no Python: los .jsx tienen literales JS válidos (arrays /
 * objetos con strings, números, null) pero NO son JSON puro — tienen
 * comentarios, trailing commas, comillas mixtas, etc. Lo más robusto es
 * usar el evaluador real de JS via `vm.runInNewContext`.
 *
 * Usage:
 *   node parse_splits_jsx.js path/to/uai.jsx
 */
const fs = require('fs');
const vm = require('vm');
const path = require('path');

const file = process.argv[2];
if (!file) {
  console.error('Usage: node parse_splits_jsx.js <path-to-jsx>');
  process.exit(1);
}

const src = fs.readFileSync(file, 'utf8');

// El .jsx mezcla la declaración de datos (const seRemontaCursos = [...]; const carreras = [...];)
// con componente React debajo. Aislamos sólo los `const` declarations al
// principio del archivo, sustituyendo imports/exports/JSX por noops.
//
// Estrategia: encontrar las declaraciones `const seRemontaCursos = [...]` y
// `const carreras = [...]` y reconstruir un script seguro.

function extractConst(name, src) {
  // Busca: const <name> = [ ... ];
  const re = new RegExp(`const\\s+${name}\\s*=\\s*`, 'g');
  const m = re.exec(src);
  if (!m) return null;
  const start = re.lastIndex;
  // Avanzar matcheando brackets para encontrar el cierre.
  // Soporta [ y { como primer caracter del valor.
  let i = start;
  // saltar espacios
  while (i < src.length && /\s/.test(src[i])) i++;
  const open = src[i];
  if (open !== '[' && open !== '{') {
    throw new Error(`expected array/object after const ${name}, got ${open}`);
  }
  const close = open === '[' ? ']' : '}';
  let depth = 0;
  let inStr = null;
  let escaped = false;
  for (let j = i; j < src.length; j++) {
    const ch = src[j];
    if (escaped) { escaped = false; continue; }
    if (inStr) {
      if (ch === '\\') { escaped = true; continue; }
      if (ch === inStr) { inStr = null; continue; }
      continue;
    }
    if (ch === '"' || ch === "'" || ch === '`') { inStr = ch; continue; }
    if (ch === open) depth++;
    else if (ch === close) {
      depth--;
      if (depth === 0) {
        // expr is src[i .. j], inclusive
        return src.slice(i, j + 1);
      }
    }
  }
  throw new Error(`unterminated ${open}...${close} in const ${name}`);
}

let seRemontaExpr, carrerasExpr;
try {
  seRemontaExpr = extractConst('seRemontaCursos', src);
  carrerasExpr = extractConst('carreras', src);
} catch (e) {
  console.error(`ERROR parseando ${file}: ${e.message}`);
  process.exit(2);
}

if (!seRemontaExpr) {
  console.error(`ERROR: ${file} no contiene 'const seRemontaCursos = [...]'`);
  process.exit(2);
}
if (!carrerasExpr) {
  console.error(`ERROR: ${file} no contiene 'const carreras = [...]'`);
  process.exit(2);
}

// Evaluar en sandbox aislado.
const ctx = {};
vm.createContext(ctx);
try {
  vm.runInContext(`base_courses = ${seRemontaExpr};\ncarreras = ${carrerasExpr};`, ctx);
} catch (e) {
  console.error(`ERROR evaluando datos de ${file}: ${e.message}`);
  process.exit(3);
}

const sigla = path.basename(file, '.jsx').toUpperCase();

const out = {
  sigla,
  base_courses: ctx.base_courses,
  carreras: ctx.carreras,
};

process.stdout.write(JSON.stringify(out));
