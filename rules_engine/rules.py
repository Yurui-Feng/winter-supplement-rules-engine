#This file defines the business rules
from .engine import Rule, Priority

# Constants for benefit amounts
BASE_AMOUNT_SINGLE = 60.0
BASE_AMOUNT_COUPLE = 120.0
CHILD_AMOUNT = 20.0
FAMILY_COMPOSITION_COUPLE = "couple"

def condition_eligibility(state:dict):
    return state["familyUnitInPayForDecember"]

def action_eligibility(state:dict, results:dict):
    """
    Sets the eligibility status and base amounts
    """
    results["isEligible"] = True
    results["baseAmount"] = BASE_AMOUNT_SINGLE
    results["supplementAmount"] = BASE_AMOUNT_SINGLE
    return

def condition_children(state:dict):
    children_count = state["numberOfChildren"]
    return children_count > 0

def action_children_count(state:dict, results:dict):
    """
    Sets the base amount and children amount if there are children
    """
    children_count = state["numberOfChildren"]
    results["baseAmount"] = BASE_AMOUNT_COUPLE
    results["childrenAmount"] = CHILD_AMOUNT * children_count
    results["supplementAmount"] = results["baseAmount"] + results["childrenAmount"]
    return

def condition_couple_family(state:dict):
    if state["familyComposition"] == FAMILY_COMPOSITION_COUPLE:
        return True
    else:
        return False

def action_couple_family(state:dict, results:dict):
    """
    Sets the base amount
    """
    results["baseAmount"] = BASE_AMOUNT_COUPLE
    results["supplementAmount"] = BASE_AMOUNT_COUPLE
    return

Rule_Eligiblity = Rule(condition_eligibility, action_eligibility, Priority.High, stop_on_false=True)
Rule_Child_Count = Rule(condition_children, action_children_count, Priority.Medium, stop_on_true=True)
Rule_Couple = Rule(condition_couple_family, action_couple_family, Priority.Low)