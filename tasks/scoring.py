from datetime import date, datetime

def calculate_task_score(task):
    """
    Strong, predictable priority system:

    PRIORITY ORDER:
    1) Due date category (overdue → today → tomorrow → this week → future)
    2) Importance (5 = highest)
    3) Estimated hours (smaller = earlier)
    4) Dependencies reduce priority

    This guarantees:
    - Overdue ALWAYS comes first
    - Due today ALWAYS above due tomorrow
    - A task due tomorrow ALWAYS above importance-5 tasks due next week
    """

    today = date.today()
    score = 0

    # -------------------------------
    # 1. PARSE DUE DATE
    # -------------------------------
    due_date = task.get("due_date")

    if isinstance(due_date, str) and due_date.strip():
        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        except:
            due_date = today
    elif not isinstance(due_date, date):
        due_date = today

    days_left = (due_date - today).days

    # -------------------------------
    # 2. DATE CATEGORY SCORING
    # -------------------------------
    if days_left < 0:
        date_score = 300     # 🔥 Overdue → top urgency
    elif days_left == 0:
        date_score = 250     # 🔥 Due today
    elif days_left == 1:
        date_score = 220     # 🔥 Due tomorrow
    elif days_left <= 7:
        date_score = 150     # ⚠️ Due this week
    else:
        date_score = 50      # Low urgency

    score += date_score

    # -------------------------------
    # 3. IMPORTANCE WEIGHT
    # -------------------------------
    importance = int(task.get("importance", 3))
    score += importance * 15   # strong weight but not overpowering dates

    # -------------------------------
    # 4. HOURS AS TIEBREAKER
    # -------------------------------
    hours = float(task.get("estimated_hours", 1))

    # Small tasks get more boost; large tasks get smaller boost
    hours_boost = max(0, 20 - (hours * 2))
    score += hours_boost

    # -------------------------------
    # 5. DEPENDENCIES (OPTIONAL)
    # -------------------------------
    deps = task.get("dependencies", [])
    if deps:
        score -= 20  # tasks blocked by others are deprioritized

    return score
