from typing import Callable
from enum import Enum

#priority functions similiar to a short circuit logic
#e.g. Egilibility has high priority where the rest have low priority
class Priority(Enum):
    High = 3
    Medium = 2
    Low = 1

class Rule:
    def __init__(self, condition: Callable, action: Callable, priority:Priority):
        self.condition = condition
        self.action = action
        self.priority = priority

def get_priority_value(item):
    return item.priority.value
        
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
            #short-circuit for the eligibility OR family have children
            #since order is always from high-to-low, it will short-circuit on the correct condition
            if rule.priority == Priority.High or rule.priority == Priority.Medium:
                if rule.condition(state) == False:
                    return supplement_amount
            if rule.condition(state):
                supplement_amount = rule.action(state)
        
        return supplement_amount