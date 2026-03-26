from dataclasses import dataclass, field
from typing import Set, Dict
import time

LEVELS = [
    (120, "Level 5 – Cyber Agent Developer"),
    (90,  "Level 4 – Payload Engineer"),
    (60,  "Level 3 – Recon Specialist"),
    (30,  "Level 2 – Automator"),
    (10,  "Level 1 – Operator"),
]


def current_level(score: int) -> str:
    for threshold, name in LEVELS:
        if score >= threshold:
            return name
    return "Unranked"


@dataclass
class ProgressState:
    lessons_done: Set[str] = field(default_factory=set)
    labs_done: Set[str] = field(default_factory=set)
    last_update: float = field(default_factory=time.time)

    def skill_score(self) -> int:
        return len(self.lessons_done) * 3 + len(self.labs_done) * 5


class HackerPythonTracker:
    def __init__(self):
        self.state = ProgressState()

    def complete_lesson(self, lesson_id: str):
        self.state.lessons_done.add(lesson_id)
        self.state.last_update = time.time()

    def complete_lab(self, lab_id: str):
        self.state.labs_done.add(lab_id)
        self.state.last_update = time.time()

    def snapshot(self) -> Dict:
        score = self.state.skill_score()
        return {
            "lessons_completed": len(self.state.lessons_done),
            "labs_completed": len(self.state.labs_done),
            "skill_score": score,
            "level": current_level(score),
            "lessons_done": sorted(self.state.lessons_done),
            "labs_done": sorted(self.state.labs_done),
            "last_update": self.state.last_update,
        }


tracker = HackerPythonTracker()
