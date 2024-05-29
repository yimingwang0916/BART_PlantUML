import pandas as pd
import json
import re


def preprocess_description(descriptions):
    plantuml_codes = []

    for description in descriptions:
        # Uncomment for debugging: print(f"Processing description: {description[:1000]}...")
        plantuml_code = "@startuml\n"

        # Initialize storage for various sections
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

        # Parse the description into sections
        sections = re.split(r'\n\s*\n', description)
        # Uncomment for debugging: print('sections 0:', sections[0])
        # Uncomment for debugging: print('sections_type :', type(sections[3]))
        for section in sections:
            if ":" not in section:
                continue     
            try:
                title, content = section.split(":", 1)
                # Uncomment for debugging: print('title is:', title)
                # Uncomment for debugging: print('title_len is:', len(title))
                # Uncomment for debugging: print('content is:', content)
                x = len(title)
                if x >= 80:
                    section = section.split(":", 1)[1]
                    sections = section.split("\n")                   
                    title, content = sections[0].split(":", 1)
                    # Uncomment for debugging: print('title is:', title)
                    # Uncomment for debugging: print('content is:', content)                  
                title = title.strip()
                content = content.strip()
            except ValueError:
                continue

            # Parse content based on different titles
            if title == "Use Case Name":
                # Uncomment for debugging: print('section is:', section)
                use_case_name = content
                try:
                    title, content = sections[1].split(":", 1)
                    # Uncomment for debugging: print('title is:', title)
                    # Uncomment for debugging: print('content is:', content)
                    # Uncomment for debugging: print('use case name:', use_case_name)
                    if title == "Use Case ID":                
                        use_case_id = content
                        # Uncomment for debugging: print('use case id:', use_case_id)
                except IndexError:
                    continue

            elif title == "Use Case Description":
                use_case_description = content
                # Uncomment for debugging: print('use case Description:', use_case_description)
            elif title == "Use Case Actors":
                actors = content.split("\n")
                for actor in actors:
                    actor = actor.strip().strip("1. ").strip("2. ").strip("- ")
                    if actor:
                        use_case_actors.append(actor)
                    # Uncomment for debugging: print('use case actors:', actor)
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

        # Generate PlantUML code
        if use_case_name:
            plantuml_code += f'title {use_case_name}\n'
            # Uncomment for debugging: print(f"Use Case Name: {use_case_name}")

        for actor in use_case_actors:
            plantuml_code += f'actor "{actor}"\n'
            # Uncomment for debugging: print(f"Actor: {actor}")

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
                # Uncomment for debugging: print(f"Step {i + 1}: {step_description}")

        if exceptions:
            plantuml_code += "alt Exception Handling\n"
            for exception in exceptions:
                plantuml_code += f'note right: {exception}\n'
                # Uncomment for debugging: print(f"Exception: {exception}")
            plantuml_code += "end\n"

        if scenarios:
            plantuml_code += "alt Scenarios\n"
            for scenario in scenarios:
                plantuml_code += f'note right: {scenario}\n'
                # Uncomment for debugging: print(f"Scenario: {scenario}")
            plantuml_code += "end\n"

        plantuml_code += "@enduml"

        # Remove extra blank lines in PlantUML code
        plantuml_code = "\n".join([line for line in plantuml_code.splitlines() if line.strip() != ""])

        # Ensure each description generates PlantUML code, even if some parts are empty
        plantuml_codes.append(plantuml_code)

    return plantuml_codes



import json
import pandas as pd

data = pd.read_parquet("/content/plantuml_generation/data/train-00000-of-00001-d16ae9e62c18f5c6.parquet")

descriptions = data["text"].tolist()
print(type(descriptions))
print(len(descriptions))

plantuml_codes = preprocess_description(descriptions)

print(type(plantuml_codes))
print(len(plantuml_codes))

output_file = "plantuml_output.json"
with open(output_file, 'w') as f:
  json.dump({"plantuml_codes": plantuml_codes}, f)

print("PlantUML is downloaded as", output_file)

#print(descriptions[0])
print('-----------------------')
#print(plantuml_codes[0])
  
