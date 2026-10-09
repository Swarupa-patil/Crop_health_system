
from flask import Flask, render_template, request
from pathlib import Path
import json

from app.models.fact import Fact
from app.models.rule import Rule
from app.engine.forward_chaining import forward_chain
from app.engine.backward_chaining import backward_chain

app = Flask(
    __name__,
    template_folder=str(Path(__file__).parent / "templates")
)

RULES_PATH = Path(__file__).parent / "knowledge" / "rules.json"

with open(RULES_PATH, "r", encoding="utf-8") as file:
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


SYMPTOMS = {
    "tomato": ["brown_spots", "leaf_drying"],
    "potato": ["brown_spots", "leaf_drying"],
    "chilli": ["leaf_curling"],
    "brinjal": ["rapid_wilting"],
    "cabbage": ["dark_leaf_spots"]
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/diagnose", methods=["POST"])
def diagnose():
    crop = request.form.get("crop", "").strip().lower()

    if crop not in SYMPTOMS:
        return render_template("index.html",
                               diagnosis="Unsupported vegetable",
                               explanation="Please select a supported vegetable.",
                               rules_used="None")

    selected_symptoms = request.form.getlist("symptoms")

    facts = [Fact("crop", crop)]
    facts.extend(
        Fact(symptom, symptom in selected_symptoms)
        for symptom in SYMPTOMS[crop]
    )

    new_facts, forward_trace = forward_chain(facts, rules)

    diagnosis_fact = next(
        (
            fact for fact in new_facts
            if fact.name.startswith("possible_") and fact.value is True
        ),
        None
    )

    if diagnosis_fact is None:
        return render_template(
        "index.html",
        selected_crop=crop,
        diagnosis="No matching diagnosis found",
        explanation="The selected symptoms do not match a rule in the knowledge base.",
        rules_used=", ".join(forward_trace) or "None"
    )

    result, backward_trace = backward_chain(
        diagnosis_fact, facts, rules
    )

    if not result:
        return render_template(
            "index.html",  
            selected_crop=crop,
            diagnosis="Diagnosis could not be verified",
            explanation="The backward-chaining engine could not prove this goal.",
            rules_used=", ".join(forward_trace) or "None"
        )

    readable_name = (
        diagnosis_fact.name
        .replace("possible_", "")
        .replace("_", " ")
        .title()
    )

    return render_template(
        "index.html",
        selected_crop=crop,
        diagnosis=f"Possible {readable_name}",
        explanation="This preliminary result was derived from the selected symptoms and stored IF–THEN rules. It is not a confirmed diagnosis.",
        rules_used=", ".join(backward_trace) or "None"
    )


if __name__ == "__main__":
    app.run(debug=False)
