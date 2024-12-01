from typing import Callable
from enum import Enum

def get_priority_value(item):
    return item.priority.value
#priority functions similiar to a short circuit logic
#e.g. Egilibility has high priority where the rest have low priority
class Priority(Enum):
    High = 3
    Medium = 2
    Low = 1
class Rule:
    """
    Represents a business rule with a condition and an action.

    :param condition: A callable that takes the state dict and returns a boolean.
    :param action: A callable that takes the state and results dicts and performs an action.
    :param priority: The priority of the rule.
    :param stop_on_false: If True and the condition evaluates to False, stop processing further rules.
    :param stop_on_true: If True and the condition evaluates to True, stop processing further rules.
    """
    def __init__(self, condition: Callable, action: Callable, priority:Priority, stop_on_false:bool=False, stop_on_true:bool=False):
        self.condition = condition
        self.action = action
        self.priority = priority
        self.stop_on_false = stop_on_false
        self.stop_on_true = stop_on_true
        
class WinterSupplementRulesEngine():
    def __init__(self, *rules:Rule):
        """
        Initializes the rules engine with a set of rules.

        :param rules: The rules to be added to the engine.
        """
        self.rules = set(rules)
    
    def add_rule(self, rule:Rule):
        self.rules.add(rule)
    
    def run(self,state:dict) -> dict:
        """
        Executes the rules engine with the provided state.

        :param state: A dictionary representing the client's state.
        :return: A dictionary containing the results of the rules engine.
        """
        #Validate inputs
        if not isinstance(state["numberOfChildren"], int):
            raise TypeError("numberOfChildren must be an integer")
        if state["numberOfChildren"] < 0:
            raise ValueError("numberOfChildren cannot be negative")
        if not isinstance(state["familyUnitInPayForDecember"], bool):
            raise TypeError("familyUnitInPayForDecember must be a boolean")
        if state["familyComposition"] not in ["single", "couple"]:
            raise ValueError("familyComposition must be either single or couple")
        
        results = {"isEligible": False, 
                   "baseAmount": 0.0,
                   "childrenAmount": 0.0, 
                   "supplementAmount": 0.0
        }
        #Use sorted to return a list and make sure high priorities are iterated first for short-circuit
        rules_list = sorted(self.rules, key=get_priority_value, reverse=True)
        for rule in rules_list:
            #short-circuit for the eligibility OR family have children
            if rule.stop_on_false and not rule.condition(state):
                return results
            elif rule.stop_on_true and rule.condition(state):
                rule.action(state, results)
                return results

            if rule.condition(state):
                rule.action(state, results)
        
        return results