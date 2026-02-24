from matplotlib import pyplot as plt
import os

from weights import DEFAULT_WEIGHTS
from survey_parsing import parse_scenarios
from merit_model import compare_candidates
from preprocess import get_human_decision, get_human_weights

def analyze_scenarios(scenarios):
    results = []
    for scenario in scenarios:
        
        algorithmic_decision = compare_candidates(scenario)
        
        human_decision = get_human_decision(scenario.name)  
        
        results.append({
            "scenario": scenario,
            "algorithmic_decision": algorithmic_decision,
            "human_decision": human_decision
        })
    
    return results

def analyze_weights():
    human_weights= get_human_weights()  
    print("Differences between human and default weights for each attribute:")
    for attribute, human_weight in human_weights.items():
        default_weight = DEFAULT_WEIGHTS[attribute]
        print(f"{attribute}: Human={human_weight}, Default={default_weight}")

def plot_analysis_results(analysis_results):
    project_root = os.path.dirname(os.path.dirname(__file__))
    matches = sum(1 for result in analysis_results if result['algorithmic_decision'] == result['human_decision'] or result['algorithmic_decision'] == 0)
    mismatches = len(analysis_results) - matches
    plt.bar(['Matches', 'Mismatches'], [matches, mismatches], color=['green', 'red'])
    plt.title('Algorithmic vs Human Decisions')
    plt.ylabel('Number of Scenarios')
    plt.show()
    plt.savefig(os.path.join(project_root, "figures", "algorithmic_vs_human_decisions.png"))

def plot_weight_differences(human_weights):
    project_root = os.path.dirname(os.path.dirname(__file__))
    attributes = list(human_weights.keys())
    human_values = [human_weights[attr] for attr in attributes]
    default_values = [DEFAULT_WEIGHTS[attr] for attr in attributes]

    x = range(len(attributes))
    plt.bar(x, human_values, width=0.4, label='Human Weights', color='blue', align='center')
    plt.bar(x, default_values, width=0.4, label='Default Weights', color='orange', align='edge')
    plt.xticks(x, attributes, rotation=45)
    plt.title('Comparison of Human and Default Weights')
    plt.ylabel('Weight Value')
    plt.legend()
    plt.tight_layout()
    plt.show()
    plt.savefig(os.path.join(project_root, "figures", "human_vs_default_weights.png"))

if __name__ == "__main__":
    print("Parsing scenarios from survey_questions.txt...")
    scenarios = parse_scenarios('survey\survey_questions.txt')
    analysis_results = analyze_scenarios(scenarios)
    analyze_weights()
    plot_weight_differences(get_human_weights())
    for result in analysis_results:
        print(f"Scenario: {result['scenario']}")
        print(f"Algorithmic Decision: {result['algorithmic_decision']}")
        print(f"Human Decision: {result['human_decision']}")
        print()
    
    plot_analysis_results(analysis_results)

