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
        self.assertEqual(self.engine.run(state),{'isEligible': False, 'baseAmount': 0.0, 'childrenAmount': 0.0, 'supplementAmount': 0.0})

    def test_engine_with_single(self):
        state = {"familyUnitInPayForDecember":True, "familyComposition":"single", "numberOfChildren":0}
        self.assertEqual(self.engine.run(state),{'isEligible': True, 'baseAmount': 60.0, 'childrenAmount': 0.0, 'supplementAmount': 60.0})
    
    def test_engine_with_couple(self):
        state = {"familyUnitInPayForDecember":True, "familyComposition":"couple", "numberOfChildren":0}
        self.assertEqual(self.engine.run(state),{'isEligible': True, 'baseAmount': 120.0, 'childrenAmount': 0.0, 'supplementAmount': 120.0})
    
    def test_engine_with_couple_and_child(self):
        state = {"familyUnitInPayForDecember":True, "familyComposition":"couple", "numberOfChildren":1}
        self.assertEqual(self.engine.run(state),{'isEligible': True, 'baseAmount': 120.0, 'childrenAmount': 20.0, 'supplementAmount': 140.0})
    
    def test_engine_with_couple_and_two_children(self):
        state = {"familyUnitInPayForDecember":True, "familyComposition":"couple", "numberOfChildren":2}
        self.assertEqual(self.engine.run(state),{'isEligible': True, 'baseAmount': 120.0, 'childrenAmount': 40.0, 'supplementAmount': 160.0})
    
    def test_engine_with_single_and_child(self):
        state = {"familyUnitInPayForDecember":True, "familyComposition":"single", "numberOfChildren":1}
        self.assertEqual(self.engine.run(state),{'isEligible': True, 'baseAmount': 120.0, 'childrenAmount': 20.0, 'supplementAmount': 140.0})
    
    def test_engine_negative_children(self):
       state = {"familyUnitInPayForDecember": True, "familyComposition": "single", "numberOfChildren": -1}
       with self.assertRaises(ValueError):
           self.engine.run(state)

    def test_engine_missing_fields(self):
       state = {"familyComposition": "single", "numberOfChildren": 0}
       with self.assertRaises(KeyError):
           self.engine.run(state)
    
    def test_engine_non_integer_children(self):
       state = {"familyUnitInPayForDecember": True, "familyComposition": "single", "numberOfChildren": 2.5}
       with self.assertRaises(TypeError):
           self.engine.run(state)

