import json
import pandas as pd
import re
import torch
from transformers import BartTokenizer, BartForConditionalGeneration, Trainer, TrainingArguments
from datasets import Dataset

# Load data from Parquet file
data = pd.read_parquet("/content/plantuml_generation/data/train-00000-of-00001-d16ae9e62c18f5c6.parquet")

# Extract descriptions from the data
descriptions = data["text"].tolist()

# Use a subset of the data for faster training
subset_size = 1000  # Use a smaller subset for both training and evaluation
descriptions = descriptions[:subset_size]

# Split data into training and evaluation sets
train_size = int(0.8 * len(descriptions))
train_descriptions = descriptions[:train_size]
eval_descriptions = descriptions[train_size:]

def preprocess_description(descriptions):
    plantuml_codes = []
    for description in descriptions:
        plantuml_code = "@startuml\n"
        use_case_name = ""
        use_case_id = ""
        use_case_actors = []
        use_case_triggers = []
        use_case_preconditions = []
        use_case_postconditions = []
        use_case_flow = []
        exceptions = []
        business_rules = []
        notes = []
        scenarios = []
        sections = re.split(r'\n\s*\n', description)
        for section in sections:
            if ":" not in section:
                continue     
            try:
                title, content = section.split(":", 1)
                x = len(title)
                if x >= 80:
                    section = section.split(":", 1)[1]
                    sections = section.split("\n")                   
                    title, content = sections[0].split(":", 1)
                title = title.strip()
                content = content.strip()
            except ValueError:
                continue
            if title == "Use Case Name":
                use_case_name = content
                try:
                    title, content = sections[1].split(":", 1)
                    if title == "Use Case ID":                
                        use_case_id = content
                except IndexError:
                    continue
            elif title == "Use Case Description":
                use_case_description = content
            elif title == "Use Case Actors":
                actors = content.split("\n")
                for actor in actors:
                    actor = actor.strip().strip("1. ").strip("2. ").strip("- ")
                    if actor:
                        use_case_actors.append(actor)
            elif title == "Use Case Triggers":
                triggers = content.split("- ")
                for trigger in triggers:
                    trigger = trigger.strip()
                    if trigger:
                        use_case_triggers.append(trigger)
            elif title == "Use Case Preconditions":
                preconditions = content.split("- ")
                for precondition in preconditions:
                    precondition = precondition.strip()
                    if precondition:
                        use_case_preconditions.append(precondition)
            elif title == "Use Case Postconditions":
                postconditions = content.split("- ")
                for postcondition in postconditions:
                    postcondition = postcondition.strip()
                    if postcondition:
                        use_case_postconditions.append(postcondition)
            elif title == "Use Case Flow":
                steps = content.split("\n")
                for step in steps:
                    step = step.strip().strip("1. ").strip("2. ").strip("3. ").strip("4. ").strip("5. ").strip("6. ").strip("7. ").strip("8. ").strip("9. ").strip("- ")
                    if step:
                        use_case_flow.append(step)
            elif title == "Exceptions":
                exception_list = content.split("\n")
                for exception in exception_list:
                    exception = exception.strip().strip("1. ").strip("2. ").strip("- ")
                    if exception:
                        exceptions.append(exception)
            elif title == "Business Rules":
                rules = content.split("- ")
                for rule in rules:
                    rule = rule.strip()
                    if rule:
                        business_rules.append(rule)
            elif title == "Notes":
                notes_content = content.split("- ")
                for note in notes_content:
                    note = note.strip()
                    if note:
                        notes.append(note)
            elif title == "Scenarios":
                scenario_list = content.split("\n")
                for scenario in scenario_list:
                    scenario = scenario.strip().strip("1. ").strip("2. ").strip("- ")
                    if scenario:
                        scenarios.append(scenario)
        if use_case_name:
            plantuml_code += f'title {use_case_name}\n'
        for actor in use_case_actors:
            plantuml_code += f'actor "{actor}"\n'
        plantuml_code += "participant \"System\" as System\n"
        if use_case_flow:
            plantuml_code += "== Use Case Flow ==\n"
            for i, step in enumerate(use_case_flow):
                if ": " in step:
                    step_number, step_description = step.split(": ", 1)
                else:
                    step_number, step_description = i + 1, step
                if use_case_actors:
                    plantuml_code += f'"{use_case_actors[0]}" -> "System": {step_description}\n'
                else:
                    plantuml_code += f'"Actor" -> "System": {step_description}\n'
        if exceptions:
            plantuml_code += "alt Exception Handling\n"
            for exception in exceptions:
                plantuml_code += f'note right: {exception}\n'
            plantuml_code += "end\n"
        if scenarios:
            plantuml_code += "alt Scenarios\n"
            for scenario in scenarios:
                plantuml_code += f'note right: {scenario}\n'
            plantuml_code += "end\n"
        plantuml_code += "@enduml"
        plantuml_code = "\n".join([line for line in plantuml_code.splitlines() if line.strip() != ""])
        plantuml_codes.append(plantuml_code)
    return plantuml_codes

# Preprocess and generate PlantUML code for training and evaluation sets
train_plantuml_codes = preprocess_description(train_descriptions)
eval_plantuml_codes = preprocess_description(eval_descriptions)

# Save PlantUML code to a JSON file
output_file = "plantuml_output.json"
with open(output_file, 'w') as f:
    json.dump({"train_plantuml_codes": train_plantuml_codes, "eval_plantuml_codes": eval_plantuml_codes}, f)

print("PlantUML code has been saved to", output_file)
print('-----------------------')

