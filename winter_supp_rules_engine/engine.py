from winter_supp_rules_engine import rule

class winter_supplement_rule_engine():
    def __init__(self, *rules):
        self.rules = rules
    
    def run(self,state):
        for rule in self.rules:
            if rule.condition(state):
                return rule.action(state)