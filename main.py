from rules_engine.engine import Rule, WinterSupplementRulesEngine
from rules_engine.rules import Rule_Child_Count,Rule_Couple,Rule_Eligiblity

engine = WinterSupplementRulesEngine()
engine.add_rule(Rule_Eligiblity)
engine.add_rule(Rule_Child_Count)
engine.add_rule(Rule_Couple)

state = {"familyUnitInPayForDecember":True, "familyComposition":"couple", "numberOfChildren":1}
print(engine.run(state))