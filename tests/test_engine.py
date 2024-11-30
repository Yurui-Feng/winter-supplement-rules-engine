from unittest import TestCase
from rules_engine.engine import WinterSupplementRulesEngine
from rules_engine.rules import Rule_Child_Count,Rule_Couple,Rule_Eligiblity

class TestEngine(TestCase):
    def setUp(self):
        self.engine = WinterSupplementRulesEngine()
        self.engine.add_rule(Rule_Eligiblity)
        self.engine.add_rule(Rule_Couple)
        self.engine.add_rule(Rule_Child_Count)

    
    def test_engine_not_eligible(self):
        state = {"familyUnitInPayForDecember":False, "familyComposition":"single", "numberOfChildren":0}
        self.assertEqual(self.engine.run(state), 0)

    def test_engine_with_single(self):
        state = {"familyUnitInPayForDecember":True, "familyComposition":"single", "numberOfChildren":0}
        self.assertEqual(self.engine.run(state), 60)
    
    def test_engine_with_couple(self):
        state = {"familyUnitInPayForDecember":True, "familyComposition":"couple", "numberOfChildren":0}
        self.assertEqual(self.engine.run(state), 120)
    
    def test_engine_with_couple_and_child(self):
        state = {"familyUnitInPayForDecember":True, "familyComposition":"couple", "numberOfChildren":1}
        self.assertEqual(self.engine.run(state), 140)
    
    def test_engine_with_couple_and_two_children(self):
        state = {"familyUnitInPayForDecember":True, "familyComposition":"couple", "numberOfChildren":2}
        self.assertEqual(self.engine.run(state), 160)
    
    def test_engine_with_single_and_child(self):
        state = {"familyUnitInPayForDecember":True, "familyComposition":"single", "numberOfChildren":1}
        self.assertEqual(self.engine.run(state), 140)

