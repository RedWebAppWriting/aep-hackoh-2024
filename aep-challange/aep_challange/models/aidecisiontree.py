from transformers import pipeline
import pandas as pd
from tokenedcomments.py import *
# Load the GPT-J model for text generation
model = pipeline("text-generation", model="EleutherAI/gpt-j-6B")


def get_binary_response(prompt):
    while True:
        response = model(f"{prompt} Please respond with ONLY YES or NO.", max_new_tokens=5, num_return_sequences=1)
        response_text = response[0]['generated_text'].strip().lower()

        if response_text in ["yes", "y"]:
            return "YES"
        elif response_text in ["no", "n"]:
            return "NO"
        else:
            print(f"Received invalid response: '{response_text}'. Please try again, ONLY answer with YES or NO.")

def classify_decision_tree(value):
    context_prompt = f"Analyze the following sentence for connotations and context: '{value}'."
    context_response = model(context_prompt, max_new_tokens=30, num_return_sequences=1)[0]['generated_text'].strip()

    # Batch questions to reduce calls
    questions = [
        f"{context_response} Was high energy present? (YES/NO)",
        f"{context_response} Was there a high-energy incident? (YES/NO)",
        f"{context_response} Was a serious injury sustained? (YES/NO)",
        f"{context_response} Was a direct control present? (YES/NO)"
    ]

    responses = [get_binary_response(q) for q in questions]

    # Map responses to decision tree logic
    high_energy_present, high_energy_incident, serious_injury, direct_control = responses

    if high_energy_present == "YES":
        if high_energy_incident == "YES":
            return "HSIF" if serious_injury == "YES" else "Capacity" if direct_control == "YES" else "PSIF"
        else:
            return "SUCCESS" if direct_control == "YES" else "EXPOSURE"
    else:
        return "LSIF" if serious_injury == "YES" else "Low Severity"

skipping t





# Load your CSV file, he first row
df = pd.read_csv('cleanedtext.csv', skiprows=1)
first_column_values = df.iloc[:, 0].tolist()

results = []
for i in range(10):
    classification = classify_decision_tree(first_column_values[i])
    results.append((value, classification))

results_df = pd.DataFrame(results, columns=['Original', 'Category'])
results_df.to_csv('categorized_sentences.csv', index=False)
