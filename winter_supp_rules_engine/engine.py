# from rule import Rule
from enum import Enum

#priority functions similiar to a short circuit logic
#e.g. Egilibility has high priority where the rest have low priority
class Priority(Enum):
    High = 3
    Medium = 2
    Low = 1

def condition_eligibility(state):
    return state["familyUnitInPayForDecember"]

def action_eligibility(condition):
    if condition:
        return 60
    else:
        return 0

class Rule:
    def __init__(self, condition, action, prioritity:Priority):
        self.condition = condition
        # self.supplement_amount = supplement_amount
        self.action = action
        self.priority = prioritity
    
    def judge_condition(self, state):
        # assume state is json parse into a dictionary
        self.condition_bool = self.condition(state)
    
    def action(self):
        self.judge_condition()
        return self.action(self.condition_bool)


Rule_Eligiblity = Rule(condition_eligibility, action_eligibility, Priority.High)
# Rule_Have_Child = Rule("Have_Child", "Bool", "120", Priority.Medium)
# Rule_Couple = Rule("Couple", "Bool", "60 or 120", Priority.Low)
# Rule_Child_Count = Rule("Child_Count", "Mulitiply", "20 per child", Priority.Low)
        
class winter_supplement_rule_engine():
    def __init__(self, *rules):
        self.rules = set(rules)
    
    def add_rule(self, rule):
        self.rules.add(rule)
    
    def run(self,state):
        for rule in self.rules:
            if rule.condition(state):
                return rule.action(state)

Engine = winter_supplement_rule_engine()
Engine.add_rule(Rule_Eligiblity)

state = {"familyUnitInPayForDecember":True}
print(Engine.run(state))