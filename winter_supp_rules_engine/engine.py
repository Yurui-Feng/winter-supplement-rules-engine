# from rule import Rule

class Rule:
    def __init__(self, condition, action):
        self.condition = condition
        self.action = action
    

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

#Eligible
Engine.add_rule(Rule({"familyUnitInPayForDecember==False"}, {"isEligible":False, "baseAmount":0, "supplementAmount":0})) #short-circuit 
#Single
Engine.add_rule(Rule({"familyUnitInPayForDecember==True", "familyComposition==single", "dependent=int:n"}, {"isEligible":True, "baseAmount":60,"supplementAmount":20}))
#Couple
Engine.add_rule(Rule({"familyUnitInPayForDecember==True", "familyComposition==couple", "dependent=int:n"}, {"isEligible":True, "baseAmount":120,"supplementAmount":20}))

print(Engine.rules)