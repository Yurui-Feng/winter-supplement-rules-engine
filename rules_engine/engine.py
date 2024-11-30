from typing import Callable
from enum import Enum

#priority functions similiar to a short circuit logic
#e.g. Egilibility has high priority where the rest have low priority
class Priority(Enum):
    High = 3
    Medium = 2
    Low = 1

class Rule:
    def __init__(self, condition: Callable, action: Callable, priority:Priority, stop_on_false:bool=False, stop_on_true:bool=False):
        self.condition = condition
        self.action = action
        self.priority = priority
        self.stop_on_false = stop_on_false
        self.stop_on_true = stop_on_true

def get_priority_value(item):
    return item.priority.value
        
class WinterSupplementRulesEngine():
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
            if rule.stop_on_false and not rule.condition(state):
                return supplement_amount
            elif rule.stop_on_true and rule.condition(state):
                supplement_amount = rule.action(state)
                return supplement_amount

            if rule.condition(state):
                supplement_amount = rule.action(state)
        
        return supplement_amount