def backward_chain(goal, facts, rules):

    for fact in facts:
        if fact.name == goal.name and fact.value == goal.value:
            return True, []

    for rule in rules:

        if (
            rule.conclusion.name == goal.name
            and rule.conclusion.value == goal.value
        ):
            trace = [rule.rule_id]

            for condition in rule.conditions:
                proven, sub_trace = backward_chain(
                    condition, facts, rules
                )

                if not proven:
                    return False, []

                trace.extend(sub_trace)

            return True, trace

    return False, []