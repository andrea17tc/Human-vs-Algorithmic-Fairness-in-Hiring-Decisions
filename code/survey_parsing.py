from classes import Candidate, Scenario

def parse_scenarios(file_path):
    scenarios = []
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Split by scenario headers (e.g., "Scenario 1", "Scenario 2", etc.)
    scenario_blocks = content.split('Scenario ')
    print(f"Found {len(scenario_blocks) - 1} scenarios in the file.")
    for block in scenario_blocks[1:]:  # Skip the first split (empty or preamble)
        lines = block.strip().split('\n')
        
        # Extract scenario number from the first line (e.g., "1 (Large Merit Gap)" -> "S1")
        first_line = lines[0].strip()
        scenario_number = first_line.split()[0]  # Get the number before any description
        scenario_name = f"S{scenario_number}"
        
        candidates_data = {'A': {}, 'B': {}}
        current_candidate = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this is a candidate header
            if line.startswith('Candidate A'):
                current_candidate = 'A'
            elif line.startswith('Candidate B'):
                current_candidate = 'B'
            # Parse candidate attributes
            elif current_candidate and ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                # Remove bullet points and other special characters
                key = key.replace('•', '').strip()
                value = value.strip()

                if key == 'test score':
                    candidates_data[current_candidate]['test_score'] = int(value)
                elif key == 'experience':
                    # Extract numeric value from "X years"
                    candidates_data[current_candidate]['experience'] = int(value.split()[0])
                elif key == 'degree':
                    candidates_data[current_candidate]['degree'] = value
                elif key == 'leadership':
                    candidates_data[current_candidate]['leadership'] = 1 if value.lower() == 'yes' else 0
                elif key == 'gender':
                    candidates_data[current_candidate]['gender'] = value
        
        # Create scenario if both candidates were parsed
        if candidates_data['A'] and candidates_data['B']:
            candidate1 = Candidate(**candidates_data['A'])
            candidate2 = Candidate(**candidates_data['B'])
            scenario = Scenario(name=scenario_name, candidate1=candidate1, candidate2=candidate2)
            scenarios.append(scenario)
    
    return scenarios

if __name__ == "__main__":
    print("Parsing scenarios from survey_questions.txt...")
    scenarios = parse_scenarios('survey\survey_questions.txt')
    for scenario in scenarios:
        print(f"{scenario.name}:")
        print(f"  Candidate A: {scenario.candidate1}")
        print(f"  Candidate B: {scenario.candidate2}")
        print()