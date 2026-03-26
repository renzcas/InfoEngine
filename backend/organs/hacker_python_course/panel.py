from typing import Dict
from .tracker import tracker
from .lessons import LESSONS
from .labs import LABS


def _next_lesson(done_ids):
    for lid in LESSONS.keys():
        if lid not in done_ids:
            return lid
    return None


def get_hacker_python_panel() -> Dict:
    snap = tracker.snapshot()
    next_lesson_id = _next_lesson(snap["lessons_done"])
    next_lesson = LESSONS.get(next_lesson_id) if next_lesson_id else None

    return {
        "progress": snap,
        "next_lesson": {
            "id": next_lesson_id,
            "title": next_lesson["title"],
            "summary": next_lesson["summary"],
        } if next_lesson else None,
        "labs": LABS,
    }
