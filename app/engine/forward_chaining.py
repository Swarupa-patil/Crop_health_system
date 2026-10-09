def forward_chain(facts, rules):

    new_facts = list(facts)
    reasoning_trace = []

    changed = True

    while changed:
        changed = False

        for rule in rules:

            if all(
                any(
                    fact.name == condition.name
                    and fact.value == condition.value
                    for fact in new_facts
                )
                for condition in rule.conditions
            ):

                if not any(
                    fact.name == rule.conclusion.name
                    and fact.value == rule.conclusion.value
                    for fact in new_facts
                ):
                    new_facts.append(rule.conclusion)
                    reasoning_trace.append(rule.rule_id)
                    changed = True

    return new_facts, reasoning_trace