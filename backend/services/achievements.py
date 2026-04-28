"""
Achievements service — gamification engine for Remy.

Architecture:
  - ACHIEVEMENTS: data-driven registry (50+ definitions) with check predicates.
  - compute_user_stats(user_id, db): one query per metric, aggregated into a dict.
  - check_and_grant(user_id, db): runs all predicates, inserts newly-unlocked
    rows into `user_achievements`, returns the IDs that were just unlocked.
  - update_activity(user_id, db): bumps the daily streak; idempotent within a day.

Hooks live in the route handlers — call check_and_grant after any user action
that could plausibly unlock something (quiz submit, lesson complete, etc.).
"""
from __future__ import annotations

from datetime import datetime, timezone, date, timedelta
from typing import Callable, Optional, Any, Dict, List, Set


# ==================== TYPE DEFINITIONS ====================

# An achievement is a plain dict; no Pydantic, just data.
# `check` receives a stats dict (computed once per call) and returns bool.
# `icon` references a lucide-react icon name (frontend resolves it).
# `rarity` drives the visual badge color/glow.
# `hidden` = True hides the achievement until unlocked (avoids spoiling surprises).


# ==================== ACHIEVEMENT REGISTRY (50 logros) ====================

ACHIEVEMENTS: List[Dict[str, Any]] = [
    # ---------- Onboarding (5) ----------
    {"id": "welcome",            "name": "Bienvenido a Remy",   "description": "Crea tu cuenta y empieza a estudiar.",                "icon": "Sparkles",     "category": "onboarding", "rarity": "common",    "color": "cyan",    "check": lambda s: True},
    {"id": "first_enrollment",   "name": "Curso elegido",       "description": "Inscríbete en tu primer curso.",                      "icon": "BookOpen",     "category": "onboarding", "rarity": "common",    "color": "cyan",    "check": lambda s: s["courses_enrolled"] >= 1},
    {"id": "first_lesson",       "name": "Primera lección",     "description": "Completa tu primera lección.",                        "icon": "Play",         "category": "onboarding", "rarity": "common",    "color": "cyan",    "check": lambda s: s["lessons_completed"] >= 1},
    {"id": "first_quiz",         "name": "Primer simulacro",    "description": "Termina tu primer simulacro.",                        "icon": "Zap",          "category": "onboarding", "rarity": "common",    "color": "cyan",    "check": lambda s: s["quizzes_completed"] >= 1},
    {"id": "first_passed",       "name": "Primer aprobado",     "description": "Aprueba un simulacro con 4.0 o más.",                 "icon": "CheckCircle",  "category": "onboarding", "rarity": "common",    "color": "emerald", "check": lambda s: s["quizzes_passed"] >= 1},

    # ---------- Lessons milestones (8) ----------
    {"id": "lessons_5",          "name": "Curioso",             "description": "Completa 5 lecciones.",                               "icon": "BookOpen",     "category": "lessons",    "rarity": "common",    "color": "cyan",    "check": lambda s: s["lessons_completed"] >= 5},
    {"id": "lessons_10",         "name": "Constante",           "description": "Completa 10 lecciones.",                              "icon": "BookMarked",   "category": "lessons",    "rarity": "common",    "color": "cyan",    "check": lambda s: s["lessons_completed"] >= 10},
    {"id": "lessons_25",         "name": "Aplicado",            "description": "Completa 25 lecciones.",                              "icon": "Library",      "category": "lessons",    "rarity": "rare",      "color": "blue",    "check": lambda s: s["lessons_completed"] >= 25},
    {"id": "lessons_50",         "name": "Estudiante serio",    "description": "Completa 50 lecciones.",                              "icon": "GraduationCap","category": "lessons",    "rarity": "rare",      "color": "blue",    "check": lambda s: s["lessons_completed"] >= 50},
    {"id": "lessons_100",        "name": "Erudito",             "description": "Completa 100 lecciones. Estudias en serio.",          "icon": "Brain",        "category": "lessons",    "rarity": "epic",      "color": "violet",  "check": lambda s: s["lessons_completed"] >= 100},
    {"id": "lessons_250",        "name": "Sabio",               "description": "Completa 250 lecciones. Pocos llegan acá.",           "icon": "Crown",        "category": "lessons",    "rarity": "legendary", "color": "amber",   "check": lambda s: s["lessons_completed"] >= 250},
    {"id": "course_complete_1",  "name": "Curso terminado",     "description": "Completa el 100% de un curso.",                       "icon": "Trophy",       "category": "lessons",    "rarity": "epic",      "color": "violet",  "check": lambda s: s["courses_completed"] >= 1},
    {"id": "course_complete_3",  "name": "Multidisciplinario",  "description": "Completa 3 cursos al 100%.",                          "icon": "Medal",        "category": "lessons",    "rarity": "legendary", "color": "amber",   "check": lambda s: s["courses_completed"] >= 3},

    # ---------- Quizzes — quantity (8) ----------
    {"id": "quizzes_5",          "name": "Practicante",         "description": "Termina 5 simulacros.",                               "icon": "Target",       "category": "quizzes",    "rarity": "common",    "color": "cyan",    "check": lambda s: s["quizzes_completed"] >= 5},
    {"id": "quizzes_10",         "name": "Entrenado",           "description": "Termina 10 simulacros.",                              "icon": "Target",       "category": "quizzes",    "rarity": "common",    "color": "cyan",    "check": lambda s: s["quizzes_completed"] >= 10},
    {"id": "quizzes_25",         "name": "Constante",           "description": "Termina 25 simulacros.",                              "icon": "Activity",     "category": "quizzes",    "rarity": "rare",      "color": "blue",    "check": lambda s: s["quizzes_completed"] >= 25},
    {"id": "quizzes_50",         "name": "Veterano",            "description": "Termina 50 simulacros.",                              "icon": "Swords",       "category": "quizzes",    "rarity": "rare",      "color": "blue",    "check": lambda s: s["quizzes_completed"] >= 50},
    {"id": "quizzes_100",        "name": "Experto en práctica", "description": "Termina 100 simulacros.",                             "icon": "Award",        "category": "quizzes",    "rarity": "epic",      "color": "violet",  "check": lambda s: s["quizzes_completed"] >= 100},
    {"id": "quizzes_250",        "name": "Imparable",           "description": "Termina 250 simulacros.",                             "icon": "Rocket",       "category": "quizzes",    "rarity": "epic",      "color": "violet",  "check": lambda s: s["quizzes_completed"] >= 250},
    {"id": "quizzes_500",        "name": "Leyenda",             "description": "Termina 500 simulacros. Eres una leyenda.",           "icon": "Crown",        "category": "quizzes",    "rarity": "legendary", "color": "amber",   "check": lambda s: s["quizzes_completed"] >= 500},
    {"id": "quiz_marathon",      "name": "Maratón",             "description": "Termina 5 simulacros en un mismo día.",               "icon": "Timer",        "category": "quizzes",    "rarity": "rare",      "color": "rose",    "check": lambda s: s["max_quizzes_in_day"] >= 5},

    # ---------- Quizzes — grades (8) ----------
    {"id": "grade_55",           "name": "Notable",             "description": "Saca 5.5 o más en un simulacro.",                     "icon": "Star",         "category": "grades",     "rarity": "common",    "color": "cyan",    "check": lambda s: s["best_grade"] >= 5.5},
    {"id": "grade_60",           "name": "Sobresaliente",       "description": "Saca 6.0 o más en un simulacro.",                     "icon": "Star",         "category": "grades",     "rarity": "rare",      "color": "blue",    "check": lambda s: s["best_grade"] >= 6.0},
    {"id": "grade_65",           "name": "Excelente",           "description": "Saca 6.5 o más en un simulacro.",                     "icon": "Stars",        "category": "grades",     "rarity": "rare",      "color": "blue",    "check": lambda s: s["best_grade"] >= 6.5},
    {"id": "grade_70",           "name": "Nota perfecta",       "description": "Saca un 7.0 en un simulacro. ¡Impecable!",            "icon": "Trophy",       "category": "grades",     "rarity": "epic",      "color": "amber",   "check": lambda s: s["best_grade"] >= 7.0},
    {"id": "perfect_3",          "name": "Triple impecable",    "description": "Saca 7.0 en 3 simulacros distintos.",                 "icon": "Medal",        "category": "grades",     "rarity": "epic",      "color": "amber",   "check": lambda s: s["quizzes_perfect"] >= 3},
    {"id": "high_streak_3",      "name": "En racha",            "description": "3 simulacros seguidos con nota 6.0+.",                "icon": "Flame",        "category": "grades",     "rarity": "rare",      "color": "rose",    "check": lambda s: s["consecutive_high_scores"] >= 3},
    {"id": "high_streak_5",      "name": "Imparable académico", "description": "5 simulacros seguidos con nota 6.0+.",                "icon": "Flame",        "category": "grades",     "rarity": "epic",      "color": "rose",    "check": lambda s: s["consecutive_high_scores"] >= 5},
    {"id": "avg_60",             "name": "Promedio sólido",     "description": "Promedio de 6.0+ con al menos 10 simulacros.",        "icon": "TrendingUp",   "category": "grades",     "rarity": "epic",      "color": "violet",  "check": lambda s: s["quizzes_completed"] >= 10 and s["average_grade"] >= 6.0},

    # ---------- Quizzes — efficiency / quality (5) ----------
    {"id": "no_errors_1",        "name": "Sin errores",         "description": "Termina un simulacro sin equivocarte.",               "icon": "ShieldCheck",  "category": "quizzes",    "rarity": "rare",      "color": "emerald", "check": lambda s: s["no_error_quizzes"] >= 1},
    {"id": "no_errors_5",        "name": "Quintuple perfecto",  "description": "5 simulacros completos sin un solo error.",           "icon": "ShieldCheck",  "category": "quizzes",    "rarity": "epic",      "color": "emerald", "check": lambda s: s["no_error_quizzes"] >= 5},
    {"id": "speedy_1",           "name": "Velocista",           "description": "Termina un simulacro en menos del 50% del tiempo.",   "icon": "Zap",          "category": "quizzes",    "rarity": "rare",      "color": "amber",   "check": lambda s: s["fast_quizzes"] >= 1},
    {"id": "speedy_5",           "name": "Súper veloz",         "description": "5 simulacros bajo el 50% del tiempo asignado.",       "icon": "Zap",          "category": "quizzes",    "rarity": "epic",      "color": "amber",   "check": lambda s: s["fast_quizzes"] >= 5},
    {"id": "answered_500",       "name": "500 preguntas",       "description": "Responde 500 preguntas en simulacros.",               "icon": "MessageSquare","category": "quizzes",    "rarity": "rare",      "color": "blue",    "check": lambda s: s["total_questions_answered"] >= 500},

    # ---------- Streaks / consistency (6) ----------
    {"id": "streak_3",           "name": "3 días seguidos",     "description": "Estudia 3 días consecutivos.",                        "icon": "Flame",        "category": "streaks",    "rarity": "common",    "color": "rose",    "check": lambda s: s["max_streak_days"] >= 3},
    {"id": "streak_7",           "name": "Una semana",          "description": "Estudia 7 días consecutivos.",                        "icon": "Flame",        "category": "streaks",    "rarity": "rare",      "color": "rose",    "check": lambda s: s["max_streak_days"] >= 7},
    {"id": "streak_14",          "name": "Dos semanas",         "description": "Estudia 14 días consecutivos.",                       "icon": "Flame",        "category": "streaks",    "rarity": "rare",      "color": "rose",    "check": lambda s: s["max_streak_days"] >= 14},
    {"id": "streak_30",          "name": "Un mes entero",       "description": "Estudia 30 días consecutivos. Disciplina pura.",      "icon": "Flame",        "category": "streaks",    "rarity": "epic",      "color": "rose",    "check": lambda s: s["max_streak_days"] >= 30},
    {"id": "streak_100",         "name": "100 días",            "description": "Estudia 100 días consecutivos. Increíble.",           "icon": "Crown",        "category": "streaks",    "rarity": "legendary", "color": "amber",   "check": lambda s: s["max_streak_days"] >= 100},
    {"id": "comeback",           "name": "Vuelvo con todo",     "description": "Vuelve a estudiar después de 7+ días sin entrar.",    "icon": "Sunrise",      "category": "streaks",    "rarity": "common",    "color": "amber",   "check": lambda s: s["had_comeback"]},

    # ---------- Coverage / breadth (5) ----------
    {"id": "chapters_3",         "name": "Diversidad",          "description": "Practica simulacros de 3 capítulos distintos.",       "icon": "Layers",       "category": "coverage",   "rarity": "common",    "color": "blue",    "check": lambda s: len(s["chapters_with_quiz"]) >= 3},
    {"id": "chapters_5",         "name": "Multi-tópico",        "description": "Practica simulacros de 5 capítulos distintos.",       "icon": "Layers",       "category": "coverage",   "rarity": "rare",      "color": "blue",    "check": lambda s: len(s["chapters_with_quiz"]) >= 5},
    {"id": "chapters_10",        "name": "Cobertura total",     "description": "Practica simulacros de 10 capítulos distintos.",      "icon": "LayoutGrid",   "category": "coverage",   "rarity": "epic",      "color": "violet",  "check": lambda s: len(s["chapters_with_quiz"]) >= 10},
    {"id": "courses_2_enrolled", "name": "Doble jornada",       "description": "Inscríbete en 2 cursos a la vez.",                    "icon": "BookCopy",     "category": "coverage",   "rarity": "common",    "color": "cyan",    "check": lambda s: s["courses_enrolled"] >= 2},
    {"id": "courses_3_enrolled", "name": "Triple desafío",      "description": "Inscríbete en 3 cursos a la vez.",                    "icon": "BookCopy",     "category": "coverage",   "rarity": "rare",      "color": "blue",    "check": lambda s: s["courses_enrolled"] >= 3},

    # ---------- Special / fun (5) ----------
    {"id": "premium",            "name": "Apoya a Remy",        "description": "Activa tu suscripción premium.",                      "icon": "Crown",        "category": "special",    "rarity": "epic",      "color": "amber",   "check": lambda s: s["subscription_active"]},
    {"id": "veteran_30",         "name": "Un mes con Remy",     "description": "Llevas 30 días desde que te uniste.",                 "icon": "Calendar",     "category": "special",    "rarity": "common",    "color": "blue",    "check": lambda s: s["days_since_signup"] >= 30},
    {"id": "veteran_180",        "name": "Veterano",            "description": "Llevas 180 días en Remy.",                            "icon": "Calendar",     "category": "special",    "rarity": "epic",      "color": "violet",  "check": lambda s: s["days_since_signup"] >= 180},
    {"id": "perseverance",       "name": "Insistente",          "description": "Reintenta el mismo simulacro 3+ veces.",              "icon": "RotateCw",     "category": "special",    "rarity": "rare",      "color": "rose",    "check": lambda s: s["max_quiz_retries"] >= 3},
    {"id": "weekend_warrior",    "name": "Fin de semana",       "description": "Estudia un sábado o domingo.",                        "icon": "Coffee",       "category": "special",    "rarity": "common",    "color": "amber",   "check": lambda s: s["studied_weekend"]},
]


def achievement_by_id(achievement_id: str) -> Optional[Dict[str, Any]]:
    return next((a for a in ACHIEVEMENTS if a["id"] == achievement_id), None)


def public_definitions() -> List[Dict[str, Any]]:
    """Strip the `check` callable for serialization to the frontend."""
    return [{k: v for k, v in a.items() if k != "check"} for a in ACHIEVEMENTS]


# ==================== STATS COMPUTATION ====================

async def compute_user_stats(user_id: str, db) -> Dict[str, Any]:
    """One DB hit per stat, returns a flat dict consumable by the predicates."""
    user = await db.users.find_one({"user_id": user_id}, {"_id": 0})
    if not user:
        user = await db.users.find_one({"id": user_id}, {"_id": 0})
    user = user or {}

    # Lessons completed (sum across all course progresses)
    progresses = await db.lesson_progress.find({"student_id": user_id}, {"_id": 0}).to_list(500)
    lessons_completed = sum(len(p.get("completed_lessons", [])) for p in progresses)

    # Courses completed (100% of lessons in the course done)
    # We approximate: a course is "completed" when its lesson_progress entry has lessons matching all chapter lessons.
    courses_completed = 0
    for p in progresses:
        course_id = p.get("course_id")
        if not course_id:
            continue
        chapters = await db.chapters.find({"course_id": course_id}, {"_id": 0, "id": 1}).to_list(500)
        total_lessons = 0
        for ch in chapters:
            ch_lessons = await db.lessons.count_documents({"chapter_id": ch["id"]})
            total_lessons += ch_lessons
        if total_lessons > 0 and len(p.get("completed_lessons", [])) >= total_lessons:
            courses_completed += 1

    # Quizzes — pull all completed attempts at once
    quizzes = await db.quiz_attempts.find(
        {"user_id": user_id, "completed": True}, {"_id": 0}
    ).sort("created_at", 1).to_list(2000)

    quizzes_completed = len(quizzes)
    grades = [q.get("grade", 0) for q in quizzes if q.get("grade") is not None]
    quizzes_perfect = sum(1 for g in grades if g >= 7.0)
    quizzes_passed = sum(1 for g in grades if g >= 4.0)
    best_grade = max(grades) if grades else 0
    average_grade = sum(grades) / len(grades) if grades else 0

    # Consecutive 6.0+ scores (longest run)
    consecutive_high_scores = 0
    current_run = 0
    for g in grades:
        if g >= 6.0:
            current_run += 1
            consecutive_high_scores = max(consecutive_high_scores, current_run)
        else:
            current_run = 0

    # No-error and fast quizzes
    no_error_quizzes = 0
    fast_quizzes = 0
    total_questions_answered = 0
    chapters_with_quiz: Set[str] = set()
    quizzes_per_day: Dict[str, int] = {}

    for q in quizzes:
        questions = q.get("questions", []) or []
        answers = q.get("answers", {}) or {}
        # Count correctness
        if questions:
            total_questions_answered += len(questions)
            correct = 0
            for idx, qu in enumerate(questions):
                if answers.get(str(idx)) == qu.get("correct_answer"):
                    correct += 1
            if correct == len(questions):
                no_error_quizzes += 1

        # Time efficiency
        time_limit = q.get("time_limit_minutes")
        time_spent = q.get("time_spent_seconds")
        if time_limit and time_spent and time_spent < (time_limit * 60 * 0.5):
            fast_quizzes += 1

        # Chapters covered
        for ch_id in q.get("chapter_ids") or []:
            chapters_with_quiz.add(ch_id)
        for qu in questions:
            ch_id = qu.get("chapter_id")
            if ch_id:
                chapters_with_quiz.add(ch_id)

        # Quizzes per day (for marathon)
        created = q.get("created_at")
        if created:
            if isinstance(created, str):
                try:
                    created = datetime.fromisoformat(created.replace("Z", "+00:00"))
                except Exception:
                    created = None
        if isinstance(created, datetime):
            day = created.date().isoformat()
            quizzes_per_day[day] = quizzes_per_day.get(day, 0) + 1

    max_quizzes_in_day = max(quizzes_per_day.values()) if quizzes_per_day else 0

    # Quiz retries (same chapter combination repeated)
    retry_counter: Dict[str, int] = {}
    for q in quizzes:
        key = ",".join(sorted(q.get("chapter_ids") or [])) + "|" + str(q.get("course_id", ""))
        retry_counter[key] = retry_counter.get(key, 0) + 1
    max_quiz_retries = max(retry_counter.values()) if retry_counter else 0

    # Enrollments
    courses_enrolled = await db.student_enrollments.count_documents({"student_id": user_id})

    # Subscription
    sub = user.get("subscription", {}) if isinstance(user.get("subscription"), dict) else {}
    subscription_active = (
        sub.get("status") == "authorized"
        or sub.get("manual_access") is True
        or user.get("subscription_status") == "active"
        or user.get("subscription_type") == "manual"
    )

    # Days since signup
    created_at = user.get("created_at")
    days_since_signup = 0
    if created_at:
        if isinstance(created_at, str):
            try:
                created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            except Exception:
                created_at = None
        if isinstance(created_at, datetime):
            if created_at.tzinfo is None:
                created_at = created_at.replace(tzinfo=timezone.utc)
            days_since_signup = (datetime.now(timezone.utc) - created_at).days

    # Streak (read-only: update happens in update_activity)
    max_streak_days = int(user.get("max_streak_days") or 0)
    current_streak_days = int(user.get("current_streak_days") or 0)
    had_comeback = bool(user.get("had_comeback") or False)
    studied_weekend = bool(user.get("studied_weekend") or False)

    return {
        "user": user,
        "quizzes_completed": quizzes_completed,
        "quizzes_perfect": quizzes_perfect,
        "quizzes_passed": quizzes_passed,
        "best_grade": best_grade,
        "average_grade": average_grade,
        "consecutive_high_scores": consecutive_high_scores,
        "no_error_quizzes": no_error_quizzes,
        "fast_quizzes": fast_quizzes,
        "total_questions_answered": total_questions_answered,
        "chapters_with_quiz": chapters_with_quiz,
        "max_quizzes_in_day": max_quizzes_in_day,
        "max_quiz_retries": max_quiz_retries,
        "lessons_completed": lessons_completed,
        "courses_enrolled": courses_enrolled,
        "courses_completed": courses_completed,
        "subscription_active": subscription_active,
        "days_since_signup": days_since_signup,
        "max_streak_days": max_streak_days,
        "current_streak_days": current_streak_days,
        "had_comeback": had_comeback,
        "studied_weekend": studied_weekend,
    }


# ==================== STREAK / ACTIVITY TRACKING ====================

async def update_activity(user_id: str, db) -> Dict[str, Any]:
    """Bump daily-streak counters. Idempotent within the same UTC day.

    Sets/updates on the user document:
      - last_active_date    (yyyy-mm-dd string)
      - current_streak_days (int)
      - max_streak_days     (int)
      - had_comeback        (bool, set True once on a >7 day gap return)
      - studied_weekend     (bool, set True once on Sat/Sun activity)
    """
    user = await db.users.find_one({"user_id": user_id}, {"_id": 0})
    user_filter = {"user_id": user_id}
    if not user:
        user = await db.users.find_one({"id": user_id}, {"_id": 0})
        user_filter = {"id": user_id}
    if not user:
        return {}

    today = datetime.now(timezone.utc).date()
    today_str = today.isoformat()
    last_str = user.get("last_active_date")

    current = int(user.get("current_streak_days") or 0)
    max_streak = int(user.get("max_streak_days") or 0)
    had_comeback = bool(user.get("had_comeback") or False)
    studied_weekend = bool(user.get("studied_weekend") or False)

    update: Dict[str, Any] = {}

    if last_str == today_str:
        # Already counted for today — nothing to bump.
        pass
    else:
        last_date: Optional[date] = None
        if last_str:
            try:
                last_date = date.fromisoformat(last_str)
            except Exception:
                last_date = None

        if last_date is None:
            current = 1
        else:
            gap = (today - last_date).days
            if gap == 1:
                current += 1
            elif gap > 1:
                if gap >= 7 and not had_comeback:
                    update["had_comeback"] = True
                    had_comeback = True
                current = 1
            # gap == 0 shouldn't happen because we'd have hit the same-day branch

        max_streak = max(max_streak, current)
        update["last_active_date"] = today_str
        update["current_streak_days"] = current
        update["max_streak_days"] = max_streak

    if not studied_weekend and today.weekday() >= 5:  # 5=Sat, 6=Sun
        update["studied_weekend"] = True

    if update:
        await db.users.update_one(user_filter, {"$set": update})

    return {
        "current_streak_days": current,
        "max_streak_days": max_streak,
        "had_comeback": had_comeback or update.get("had_comeback", False),
    }


# ==================== CHECK & GRANT ====================

async def check_and_grant(user_id: str, db) -> List[Dict[str, Any]]:
    """Run all achievement checks; insert any new unlocks; return them.

    Returns the achievement *definitions* (with `check` stripped) of the ones
    just unlocked, so the caller can surface them to the user (toast / response).
    """
    if not user_id:
        return []

    # Refresh activity counters before computing stats.
    await update_activity(user_id, db)

    stats = await compute_user_stats(user_id, db)

    # Pull existing unlocks once.
    existing_docs = await db.user_achievements.find(
        {"user_id": user_id}, {"_id": 0, "achievement_id": 1}
    ).to_list(500)
    existing_ids: Set[str] = {d["achievement_id"] for d in existing_docs}

    newly_unlocked: List[Dict[str, Any]] = []
    now_iso = datetime.now(timezone.utc).isoformat()

    for ach in ACHIEVEMENTS:
        if ach["id"] in existing_ids:
            continue
        try:
            passed = bool(ach["check"](stats))
        except Exception:
            passed = False
        if passed:
            doc = {
                "user_id": user_id,
                "achievement_id": ach["id"],
                "unlocked_at": now_iso,
            }
            await db.user_achievements.insert_one(doc)
            # Strip `check` for the response payload.
            newly_unlocked.append({k: v for k, v in ach.items() if k != "check"})

    return newly_unlocked


async def list_for_user(user_id: str, db) -> Dict[str, Any]:
    """Return all achievement definitions plus per-user unlock state + stats."""
    stats = await compute_user_stats(user_id, db)
    unlocks = await db.user_achievements.find(
        {"user_id": user_id}, {"_id": 0}
    ).to_list(500)
    unlock_map = {u["achievement_id"]: u.get("unlocked_at") for u in unlocks}

    result = []
    for ach in ACHIEVEMENTS:
        unlocked_at = unlock_map.get(ach["id"])
        item = {k: v for k, v in ach.items() if k != "check"}
        item["unlocked"] = unlocked_at is not None
        item["unlocked_at"] = unlocked_at
        result.append(item)

    # Stats subset for the UI (no PII or huge sets)
    public_stats = {
        "quizzes_completed": stats["quizzes_completed"],
        "lessons_completed": stats["lessons_completed"],
        "courses_completed": stats["courses_completed"],
        "best_grade": stats["best_grade"],
        "average_grade": round(stats["average_grade"], 2),
        "current_streak_days": stats["current_streak_days"],
        "max_streak_days": stats["max_streak_days"],
        "chapters_practiced": len(stats["chapters_with_quiz"]),
    }

    return {
        "achievements": result,
        "stats": public_stats,
        "unlocked_count": sum(1 for r in result if r["unlocked"]),
        "total_count": len(result),
    }
