# from rule import Rule
from enum import Enum

#priority functions similiar to a short circuit logic
#e.g. Egilibility has high priority where the rest have low priority
class Priority(Enum):
    High = 3
    Medium = 2
    Low = 1

class Rule:
    def __init__(self, condition_name, condition_type, action, depends_on=None):
        self.condition_name = condition_name
        self.action = action
        self.condition_type = condition_type
        self.depends_on = depends_on
        # self.priority = prioritity

Rule_Eligiblity = Rule("Eligibility", "Bool", "*1 or *0")
Rule_Have_Child = Rule("Have_Child", "Bool", "120", {Rule_Eligiblity})
Rule_Couple = Rule("Couple", "Bool", "60 or 120", {Rule_Eligiblity})
Rule_Child_Count = Rule("Child_Count", "Mulitiply", "20 per child", {Rule_Eligiblity, Rule_Have_Child})
        
class WinterSupplementRuleEngine():
    def __init__(self, *rules):
        self.rules = set(rules)
    
    def add_rule(self, rule):
        self.rules.add(rule)
    
    def run(self,state):
        for rule in self.rules:
            if rule.condition(state):
                return rule.action(state)

Engine = WinterSupplementRuleEngine()

#Eligible
# Engine.add_rule(Rule({"familyUnitInPayForDecember==False"}, {"isEligible":False, "baseAmount":0, "supplementAmount":0})) #short-circuit 
# #Single
# Engine.add_rule(Rule({"familyUnitInPayForDecember==True", "familyComposition==single", "dependent=int:n"}, {"isEligible":True, "baseAmount":60,"supplementAmount":20}))
# #Couple
# Engine.add_rule(Rule({"familyUnitInPayForDecember==True", "familyComposition==couple", "dependent=int:n"}, {"isEligible":True, "baseAmount":120,"supplementAmount":20}))

print(Engine.rules)