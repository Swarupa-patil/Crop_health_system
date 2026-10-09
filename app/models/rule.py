class Rule:
    def __init__(self, rule_id, conditions, conclusion):
        self.rule_id = rule_id
        self.conditions = conditions
        self.conclusion = conclusion

    def __str__(self):
        conditions_text = " AND ".join(str(fact) for fact in self.conditions)

        return f"{self.rule_id}: IF {conditions_text} THEN {self.conclusion}"