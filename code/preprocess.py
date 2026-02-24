import pandas as pd

from file_paths import INPUT_FILE, OUTPUT_FILE

def preprocess_data(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Drop the first column
    df = df.iloc[:, 1:]

    # Rename columns that start with 'S#', where # is a number to just the number, to S and that number
    rename_dict = {col: f'S{i}' for i, col in enumerate(df.columns[:15], 1)}
    df = df.rename(columns=rename_dict)
    
    #Rename the rest of the column with what is between [ and ] in the original column name
    for col in df.columns[15:]:
        new_name = col.split('[')[-1].split(']')[0]
        df = df.rename(columns={col: new_name})
    return df

#save the preprocessed data to a new CSV file
def save_preprocessed_data(df, output_file_path):
    df.to_csv(output_file_path, index=False)

def create_human_weight_mapping(df):
    weight_mapping = {}
    for col in df.columns[15:]:
        new_col=col.lower().replace(' ', '_')  # Normalize column name to match attribute names
        weight_mapping[new_col] = float(df[col].mean())

    total = float(sum(weight_mapping.values()))
    if total > 0:
        weight_mapping = {key: float(value / total) for key, value in weight_mapping.items()}

    print(f"Human weight mapping: {weight_mapping}")
    return weight_mapping

#create a dictionary mapping scenario numbers to the majority human decision for that scenario, which will be used in the analysis step to compare against the algorithmic decisions, if ties exist, we can assign a value of 0 to indicate no majority decision
def create_human_decision_mapping(df):
    human_decision_mapping = {}
    
    for scenario in df.columns[:15].unique():
        #scenario data is the whole column without the header
        scenario_data = df[scenario]
        #the majority decision has to be computed, options are Candidate A and Candidate B, we can use value_counts to get the count of each decision and then determine the majority
        majority_decision = scenario_data.value_counts().idxmax()

        if len(majority_decision) > 0:
            if majority_decision == 'Candidate A':
                human_decision_mapping[scenario] = 1
            elif majority_decision == 'Candidate B':
                human_decision_mapping[scenario] = -1
        else:
            human_decision_mapping[scenario] = 0  # No majority decision
    
    return human_decision_mapping

#if data hasn't been preprocessed yet, preprocess it and save it to a new file, otherwise just load the preprocessed data
def load_data(OUTPUT_FILE):
    try:
        df = pd.read_csv(OUTPUT_FILE)
        print(f"Loaded preprocessed data from {OUTPUT_FILE}")
        human_decision_mapping = create_human_decision_mapping(df)
        human_weight_mapping = create_human_weight_mapping(df)
    except FileNotFoundError:
        print(f"Preprocessed file not found. Preprocessing data from {INPUT_FILE}...")
        df = preprocess_data(INPUT_FILE)
        save_preprocessed_data(df, OUTPUT_FILE)
        print(f"Preprocessed data saved to {OUTPUT_FILE}")
        human_decision_mapping = create_human_decision_mapping(df)
        human_weight_mapping = create_human_weight_mapping(df)
    except Exception as e:
        print(f"Error loading preprocessed data: {e}")
        df = preprocess_data(INPUT_FILE)
        save_preprocessed_data(df, OUTPUT_FILE)
        human_decision_mapping = create_human_decision_mapping(df)
        human_weight_mapping = create_human_weight_mapping(df)
    return df, human_decision_mapping, human_weight_mapping

def get_human_decision(scenario):
    df, human_decision_mapping, human_weight_mapping = load_data(OUTPUT_FILE)  # Ensure data is loaded and mapping is created
    #print human_decision_mapping to check if it is correct
    print(f"Human decision mapping: {human_decision_mapping}")
    return human_decision_mapping.get(scenario, 0)  # Return 0 if scenario not found in mapping

def get_human_weights():
    df, human_decision_mapping, human_weight_mapping = load_data(OUTPUT_FILE)  # Ensure data is loaded and mapping is created
    return human_weight_mapping
