from app.models.fact import Fact
import json
from app.models.rule import Rule
from app.engine.forward_chaining import forward_chain
from app.engine.backward_chaining import backward_chain
from app.explanation.explanation_engine import explain_diagnosis
# -------------------------
# STEP 1: Create facts
# -------------------------
crop = input("Enter crop name: ").strip().lower()
fact1 = Fact("crop", crop)
supported_crops = ["tomato", "potato", "chilli", "brinjal", "cabbage"]

if crop not in supported_crops:
    print("Unsupported crop. Choose tomato, potato, chilli, brinjal, or cabbage.")
    exit()

symptom_questions = {
    "tomato": [
        ("brown_spots", "Are brown spots present?"),
        ("leaf_drying", "Are leaves drying?")
    ],
    "potato": [
        ("brown_spots", "Are brown spots present?"),
        ("leaf_drying", "Are leaves drying?")
    ],
    "chilli": [
        ("leaf_curling", "Are leaves curling?")
    ],
    "brinjal": [
        ("rapid_wilting", "Is the plant wilting rapidly?")
    ],
    "cabbage": [
        ("dark_leaf_spots", "Are dark spots present on leaves?")
    ]
}

symptom_facts = []

for symptom, question in symptom_questions[crop]:
    answer = input(question + " (yes/no): ").strip().lower()

    if answer not in ("yes", "no"):
        print("Invalid input. Please enter only yes or no.")
        exit()

    symptom_facts.append(Fact(symptom, answer == "yes"))

facts = [fact1] + symptom_facts
# -------------------------
# STEP 2: Create rules
# -------------------------
with open("app/knowledge/rules.json", "r") as file:
    rules_data = json.load(file)

rules = []

for item in rules_data:
    conditions = [
        Fact(condition["name"], condition["value"])
        for condition in item["conditions"]
    ]

    conclusion = Fact(
        item["conclusion"]["name"],
        item["conclusion"]["value"]
    )

    rules.append(Rule(item["id"], conditions, conclusion))

# -------------------------
# STEP 3: Display facts
# -------------------------
print("CURRENT FACTS")
print("----------------")


for fact in facts:
    print(fact)
# -------------------------
# STEP 4: Display rules
# -------------------------
print("\nRULES")
print("----------------")
for rule in rules:
    print(rule)
new_facts, trace = forward_chain(
    facts,
    rules
)

print("\nFORWARD CHAINING")
print("----------------")

for fact in new_facts:
    print(fact)
goal = None

for fact in rules:
    if fact.conclusion.name.startswith("possible_"):
        if any(
            f.name == fact.conclusion.name and f.value is True
            for f in new_facts
        ):
            goal = fact.conclusion
            break

if goal is None:
    print("No matching diagnosis found. More symptoms or expert assessment may be needed.")
    exit()
    
print("\nRULES TRIGGERED")
for rule_id in trace:
    print(rule_id)
    

result, backward_trace = backward_chain(
    goal,
    facts,
    rules
)

print("\nBACKWARD CHAINING")
print("----------------")

print("Goal:", goal)
print("Goal proven:", result)

print("Rules checked:", backward_trace)

if result:
    print("Possible disease detected. See the explanation below.")
    print("This is a preliminary result, not a confirmed diagnosis.")
    print("Action: Inspect affected leaves and consult a local agricultural expert.")
    
    explain_diagnosis(trace, backward_trace, goal)
else:
    print("No matching diagnosis found. More symptoms or expert assessment may be needed.")
    