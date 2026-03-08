import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def seed_database():
    print("🌱 Iniciando población de base de datos...")
    
    await db.courses.delete_many({})
    await db.formulas.delete_many({})
    
    courses = [
        {
            "id": "course-001",
            "title": "Cálculo I",
            "description": "Aprende los fundamentos del cálculo: límites, derivadas y sus aplicaciones",
            "category": "Matemáticas",
            "level": "Intermedio",
            "modules_count": 50,
            "instructor": "Jesus Bravo",
            "rating": 4.8,
            "thumbnail_url": None,
            "created_at": "2024-01-01T00:00:00"
        },
        {
            "id": "course-002",
            "title": "Cálculo II",
            "description": "Integrales, series y ecuaciones diferenciales para nivel universitario",
            "category": "Matemáticas",
            "level": "Intermedio",
            "modules_count": 43,
            "instructor": "Jesus Bravo",
            "rating": 4.8,
            "thumbnail_url": None,
            "created_at": "2024-01-01T00:00:00"
        },
        {
            "id": "course-003",
            "title": "Álgebra Lineal",
            "description": "Vectores, matrices, espacios vectoriales y transformaciones lineales",
            "category": "Matemáticas",
            "level": "Intermedio",
            "modules_count": 35,
            "instructor": "Jesus Bravo",
            "rating": 4.8,
            "thumbnail_url": None,
            "created_at": "2024-01-01T00:00:00"
        },
        {
            "id": "course-004",
            "title": "Física Mecánica",
            "description": "Cinemática, dinámica, trabajo y energía en sistemas físicos",
            "category": "Física",
            "level": "Básico",
            "modules_count": 40,
            "instructor": "Jesus Bravo",
            "rating": 4.7,
            "thumbnail_url": None,
            "created_at": "2024-01-01T00:00:00"
        },
        {
            "id": "course-005",
            "title": "Ecuaciones Diferenciales",
            "description": "Aprende todo sobre EDO de primer orden y superior, sistemas de EDO",
            "category": "Matemáticas",
            "level": "Avanzado",
            "modules_count": 42,
            "instructor": "Jesus Bravo",
            "rating": 4.9,
            "thumbnail_url": None,
            "created_at": "2024-01-01T00:00:00"
        },
        {
            "id": "course-006",
            "title": "Nivelación Ingeniería",
            "description": "Aprende todo lo esencial para tu primer año de ingeniería",
            "category": "General",
            "level": "Intermedio",
            "modules_count": 43,
            "instructor": "Jesus Bravo",
            "rating": 4.8,
            "thumbnail_url": None,
            "created_at": "2024-01-01T00:00:00"
        }
    ]
    
    formulas = [
        {
            "id": "formula-001",
            "course_id": "course-001",
            "topic": "Derivadas",
            "name": "Regla de la potencia",
            "latex": "d/dx(x^n) = n·x^(n-1)",
            "description": "La derivada de x elevado a n es igual a n multiplicado por x elevado a n-1",
            "example": "d/dx(x³) = 3x²"
        },
        {
            "id": "formula-002",
            "course_id": "course-001",
            "topic": "Derivadas",
            "name": "Regla del producto",
            "latex": "d/dx(f·g) = f'·g + f·g'",
            "description": "La derivada del producto de dos funciones es la derivada de la primera por la segunda más la primera por la derivada de la segunda",
            "example": "d/dx(x²·sin(x)) = 2x·sin(x) + x²·cos(x)"
        },
        {
            "id": "formula-003",
            "course_id": "course-001",
            "topic": "Derivadas",
            "name": "Regla del cociente",
            "latex": "d/dx(f/g) = (f'·g - f·g')/g²",
            "description": "La derivada de un cociente es la derivada del numerador por el denominador menos el numerador por la derivada del denominador, todo sobre el denominador al cuadrado",
            "example": "d/dx(x/sin(x)) = (sin(x) - x·cos(x))/sin²(x)"
        },
        {
            "id": "formula-004",
            "course_id": "course-002",
            "topic": "Integrales",
            "name": "Integral de potencia",
            "latex": "∫x^n dx = x^(n+1)/(n+1) + C",
            "description": "La integral de x elevado a n es x elevado a n+1 dividido por n+1, más la constante de integración",
            "example": "∫x³ dx = x⁴/4 + C"
        },
        {
            "id": "formula-005",
            "course_id": "course-002",
            "topic": "Integrales",
            "name": "Integral por partes",
            "latex": "∫u dv = uv - ∫v du",
            "description": "Técnica de integración que transforma el producto de funciones en una integral más simple",
            "example": "∫x·e^x dx = x·e^x - e^x + C"
        },
        {
            "id": "formula-006",
            "course_id": "course-003",
            "topic": "Vectores",
            "name": "Producto punto",
            "latex": "a·b = |a||b|cos(θ)",
            "description": "El producto punto de dos vectores es igual al producto de sus magnitudes por el coseno del ángulo entre ellos",
            "example": "(1,2)·(3,4) = 1·3 + 2·4 = 11"
        },
        {
            "id": "formula-007",
            "course_id": "course-003",
            "topic": "Matrices",
            "name": "Determinante 2x2",
            "latex": "det(A) = ad - bc",
            "description": "El determinante de una matriz 2x2 es el producto de la diagonal principal menos el producto de la diagonal secundaria",
            "example": "det([[1,2],[3,4]]) = 1·4 - 2·3 = -2"
        },
        {
            "id": "formula-008",
            "course_id": "course-004",
            "topic": "Cinemática",
            "name": "Velocidad",
            "latex": "v = Δx/Δt",
            "description": "La velocidad es el cambio de posición dividido por el cambio de tiempo",
            "example": "Si un objeto se mueve 10m en 2s, v = 10/2 = 5 m/s"
        },
        {
            "id": "formula-009",
            "course_id": "course-004",
            "topic": "Dinámica",
            "name": "Segunda ley de Newton",
            "latex": "F = ma",
            "description": "La fuerza neta sobre un objeto es igual a su masa por su aceleración",
            "example": "Si m=2kg y a=3m/s², entonces F=6N"
        },
        {
            "id": "formula-010",
            "course_id": "course-004",
            "topic": "Energía",
            "name": "Energía cinética",
            "latex": "Ec = (1/2)mv²",
            "description": "La energía cinética de un objeto es la mitad de su masa por su velocidad al cuadrado",
            "example": "Si m=2kg y v=4m/s, entonces Ec=16J"
        }
    ]
    
    await db.courses.insert_many(courses)
    print(f"✅ Insertados {len(courses)} cursos")
    
    await db.formulas.insert_many(formulas)
    print(f"✅ Insertadas {len(formulas)} fórmulas")
    
    print("🎉 Base de datos poblada exitosamente!")

if __name__ == "__main__":
    asyncio.run(seed_database())
