#This file defines the business rules
from .engine import Rule, Priority

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

Rule_Eligiblity = Rule(condition_eligibility, action_eligibility, Priority.High, stop_on_false=True)
Rule_Child_Count = Rule(condition_children, action_children_count, Priority.Medium, stop_on_true=True)
Rule_Couple = Rule(condition_couple_family, action_couple_family, Priority.Low)