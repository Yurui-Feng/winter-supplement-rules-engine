import unittest
import json
from unittest.mock import Mock
from rules_engine.mtqq_wrapper import MQTTWinterSupplementRulesEngine

class TestMQTTWrapperInitialization(unittest.TestCase):
    def test_initialization(self):
        topic_id = "test-topic"
        engine = MQTTWinterSupplementRulesEngine(topic_id)
        
        self.assertEqual(engine.broker_url, "test.mosquitto.org")
        self.assertEqual(engine.port, 1883)
        self.assertEqual(engine.topic_id, topic_id)
        self.assertEqual(engine.topic_input, f"BRE/calculateWinterSupplementInput/{topic_id}")
        self.assertEqual(engine.topic_output, f"BRE/calculateWinterSupplementOutput/{topic_id}")
        self.assertIsNotNone(engine.client)
        self.assertTrue(len(engine.rules) > 0)

class TestMQTTWrapperOnConnect(unittest.TestCase):
    def test_on_connect(self):
        # Mock the client object and its methods
        self.engine = MQTTWinterSupplementRulesEngine("test-topic")
        self.engine.client = Mock()

        # Test connection
        self.engine.on_connect(self.engine.client, None, None, 0, None)

        self.engine.client.subscribe.assert_called_once_with(self.engine.topic_input)

class TestMQTTWrapperOnMessage(unittest.TestCase):
    def setUp(self):
        self.topic_id = "test-topic"
        self.engine = MQTTWinterSupplementRulesEngine(self.topic_id)

    def test_on_message(self):
        # Use Mock to mock the client object
        client = Mock()
        input_data = {"id": "test-id", 
                      "familyUnitInPayForDecember": True,
                      "numberOfChildren": 1,
                      "familyComposition": "single"}
                      
        # Mock an MQTT message
        msg = Mock()
        msg.payload = json.dumps(input_data).encode()
        msg.topic = self.engine.topic_input.encode()

        self.engine.on_message(client, None, msg)
        output = self.engine.run(input_data)

        # Parse the expected output data
        expected_output = {"isEligible": True, "baseAmount": 120.0, "childrenAmount": 20.0, "supplementAmount": 140.0}

        # Assert that the output is as expected
        self.assertEqual(output, expected_output)
