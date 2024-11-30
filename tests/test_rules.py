from rules_engine.rules import Rule_Child_Count,Rule_Couple,Rule_Eligiblity
from unittest import TestCase
from rules_engine.engine import Priority

class TestRules(TestCase):
    def test_rule_child_count(self):
        self.assertEqual(Rule_Child_Count.condition({"numberOfChildren":0}), False)
        self.assertEqual(Rule_Child_Count.condition({"numberOfChildren":1}), True)
        self.assertEqual(Rule_Child_Count.action({"numberOfChildren":1}), 140)

    def test_rule_couple(self):
        self.assertEqual(Rule_Couple.condition({"familyComposition":"couple"}), True)
        self.assertEqual(Rule_Couple.condition({"familyComposition":"single"}), False)
        self.assertEqual(Rule_Couple.action({"familyComposition":"couple"}), 120)
    
    def test_rule_eligiblity(self):
        self.assertEqual(Rule_Eligiblity.condition({"familyUnitInPayForDecember":True}), True)
        self.assertEqual(Rule_Eligiblity.condition({"familyUnitInPayForDecember":False}), False)
        self.assertEqual(Rule_Eligiblity.action({"familyUnitInPayForDecember":True}), 60)
    
    def test_rule_priority(self):
        self.assertEqual(Rule_Eligiblity.priority, Priority.High)
        self.assertEqual(Rule_Child_Count.priority, Priority.Medium)
        self.assertEqual(Rule_Couple.priority, Priority.Low)
    


