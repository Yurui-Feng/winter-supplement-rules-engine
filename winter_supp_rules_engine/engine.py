# from rule import Rule
from enum import Enum
from typing import Callable

#priority functions similiar to a short circuit logic
#e.g. Egilibility has high priority where the rest have low priority
class Priority(Enum):
    High = 3
    Medium = 2
    Low = 1

def get_priority_value(item):
    return item.priority.value

def condition_eligibility(state:dict):
    return state["familyUnitInPayForDecember"]

def action_eligibility(state:dict):
    return 60

def condition_children(state:dict):
    children_count = state["numberOfChildren"]
    return children_count > 0

def action_children_count(state:dict):
    children_count = state["numberOfChildren"]
    return 120 + 20 * children_count

def condition_couple_family(state:dict):
    if state["familyComposition"] == "couple":
        return True
    else:
        return False

def action_couple_family(state:dict):
    return 120

class Rule:
    def __init__(self, condition: Callable, action: Callable, priority:Priority):
        self.condition = condition
        self.action = action
        self.priority = priority

Rule_Eligiblity = Rule(condition_eligibility, action_eligibility, Priority.High)
Rule_Child_Count = Rule(condition_children, action_children_count, Priority.Medium)
Rule_Couple = Rule(condition_couple_family, action_couple_family, Priority.Low)
        
class winter_supplement_rule_engine():
    def __init__(self, *rules):
        self.rules = set(rules)
    
    def add_rule(self, rule):
        self.rules.add(rule)
    
    def run(self,state):
        supplement_amount = 0
        #Use sorted to return a list and make sure high priorities are iterated first for short-circuit
        rules_list = sorted(self.rules, key=get_priority_value, reverse=True)
        for rule in rules_list:
            #short-circuit for the eligibility criterion
            if rule.priority == Priority.High:
                if rule.condition(state) == False:
                    return supplement_amount
            if rule.condition(state):
                supplement_amount = max(supplement_amount, rule.action(state))
        
        return supplement_amount

Engine = winter_supplement_rule_engine()
Engine.add_rule(Rule_Eligiblity)
Engine.add_rule(Rule_Child_Count)
Engine.add_rule(Rule_Couple)

state = {"familyUnitInPayForDecember":True, "familyComposition":"single", "numberOfChildren":0}
print(Engine.run(state))