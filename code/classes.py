from attr import dataclass

@dataclass(frozen=True)
class Candidate:
    test_score: int           # 0–100
    experience: int           # years
    leadership: int             # 1 = Yes, 0 = No
    degree: str                 # Degree field
    gender: str = None          # Included but NOT used in merit

@dataclass(frozen=True)
class Scenario:
    candidate1: Candidate
    candidate2: Candidate
    name: str = None