def explain_diagnosis(forward_trace, backward_trace, diagnosis):
    print("\nEXPLANATION")
    print("----------------")

    name = diagnosis.name.replace("possible_", "").replace("_", " ").title()
    print("Possible diagnosis:", name) 

    print("\nForward chaining rules:")
    for rule_id in forward_trace:
        print("-", rule_id)

    print("\nBackward chaining rules:")
    for rule_id in backward_trace:
        print("-", rule_id)