from weights import DEFAULT_WEIGHTS, DEGREE_WEIGHTS
from classes import Candidate, Scenario

def normalize_test_score(score: float) -> float:
    """Normalize test score to 0-1 range."""
    return score / 100.0


def normalize_experience(exp: float, max_exp: float = 5.0) -> float:
    """Normalize experience assuming max_exp years."""
    return min(exp / max_exp, 1.0)


def encode_degree(degree: str) -> float:
    """Return degree relevance weight."""
    return DEGREE_WEIGHTS.get(degree, 0.8)  # default 

def calculate_merit(candidate: Candidate, weights=DEFAULT_WEIGHTS) -> float:
    test_score = normalize_test_score(candidate.test_score)
    experience = normalize_experience(candidate.experience)
    degree_score = encode_degree(candidate.degree)

    merit_score = (
        test_score * weights['test_score'] +
        experience * weights['experience'] +
        candidate.leadership * weights['leadership'] +
        degree_score * weights['degree']
    )
    
    return merit_score

def compare_candidates(scenario:Scenario, weights=DEFAULT_WEIGHTS) -> int:
    merit1 = calculate_merit(scenario.candidate1, weights)
    merit2 = calculate_merit(scenario.candidate2, weights)
    if merit1 > merit2 and abs(merit1 - merit2) > 0.05:  # Adding a small threshold to avoid ties due to minor differences
        return 1  # Candidate A is better
    elif merit2 > merit1 and abs(merit2 - merit1) > 0.05:
        return -1 # Candidate B is better
    else:
        return 0  # Both candidates are equal in merit
    
