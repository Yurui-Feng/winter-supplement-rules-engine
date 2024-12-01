from rules_engine.rules import Rule_Child_Count,Rule_Couple,Rule_Eligiblity
from unittest import TestCase
from rules_engine.engine import Priority

class TestRules(TestCase):
    def test_rule_child_count(self):
        results = {}
        #function has no return, so we need to check the results dictionary
        self.assertEqual(Rule_Child_Count.condition({"numberOfChildren":0}), False)
        self.assertEqual(Rule_Child_Count.condition({"numberOfChildren":1}), True)
        Rule_Child_Count.action({"numberOfChildren":1}, results)
        self.assertEqual(results, {'baseAmount': 120.0, 'childrenAmount': 20.0, "supplementAmount": 140.0})

    def test_rule_couple(self):
        results = {}
        self.assertEqual(Rule_Couple.condition({"familyComposition":"couple"}), True)
        self.assertEqual(Rule_Couple.condition({"familyComposition":"single"}), False)
        Rule_Couple.action({"familyComposition":"couple"}, results)
        self.assertEqual(results, {'baseAmount': 120.0, 'supplementAmount': 120.0})
    
    def test_rule_eligiblity(self):
        results = {}
        self.assertEqual(Rule_Eligiblity.condition({"familyUnitInPayForDecember":True}), True)
        self.assertEqual(Rule_Eligiblity.condition({"familyUnitInPayForDecember":False}), False)
        Rule_Eligiblity.action({"familyUnitInPayForDecember":True}, results)
        self.assertEqual(results, {"isEligible": True, "baseAmount": 60.0, "supplementAmount": 60.0})
    
    def test_rule_priority(self):
        self.assertEqual(Rule_Eligiblity.priority, Priority.High)
        self.assertEqual(Rule_Child_Count.priority, Priority.Medium)
        self.assertEqual(Rule_Couple.priority, Priority.Low)
    


