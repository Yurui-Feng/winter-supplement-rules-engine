import json
import random
from .engine import WinterSupplementRulesEngine
from .rules import Rule_Eligiblity, Rule_Child_Count, Rule_Couple
from paho.mqtt.client import Client
from paho.mqtt.enums import CallbackAPIVersion

# MQTT Wrapper Class for the Rules Engine
class MQTTWinterSupplementRulesEngine(WinterSupplementRulesEngine):
    """
    A wrapper class for the WinterSupplementRulesEngine that adds MQTT functionality.
    """
    def __init__(self, topic_id: str, broker_url: str = "test.mosquitto.org", port: int = 1883):
        super().__init__()

        # Set up broker details
        self.broker_url = broker_url
        self.port = port
        
        # Add rules to the engine
        self.add_rule(Rule_Eligiblity)
        self.add_rule(Rule_Child_Count)
        self.add_rule(Rule_Couple)

        # Initialize MQTT Client
        self.client_id = f'rules-engine-{random.randint(0,1000)}'
        self.client = Client(
            callback_api_version=CallbackAPIVersion.VERSION2,
            client_id=self.client_id
        )

        # Set up topics
        self.topic_id = topic_id
        self.topic_input = f"BRE/calculateWinterSupplementInput/{topic_id}"
        self.topic_output = f"BRE/calculateWinterSupplementOutput/{topic_id}"

    def on_connect(self, client, userdata, flags, rc, properties):
        try:
            if rc == 0:
                print(f"Connected to MQTT Broker!")
                result, _ = self.client.subscribe(self.topic_input)
                if result == 0:
                    print(f"Subscribed to topic `{self.topic_input}` successfully")
                else:
                    print(f"Failed to subscribe to topic `{self.topic_input}`, result code: {result}")
            else:
                print("Failed to connect, return code", rc)
        except Exception as e:
            print(f"Error in on_connect: {e}")
    
    def on_message(self, client, userdata, msg):
        try:
            print(f"Received `{msg.payload}` from `{msg.topic}` topic")
            # Decode the input message
            input_str = msg.payload.decode()
            input_data = json.loads(input_str)
            print(f"Received `{input_data}` from `{msg.topic}` topic")

            # Run the rules engine
            output_data = self.run(input_data)
            output_data["id"] = input_data.get("id")

            # Publish the output data   
            self.publish(output_data)
        except Exception as e:
            print(f"Error in on_message: {e}")

    def publish(self, output_data: dict):
        try:
            output_msg = json.dumps(output_data)
            print(f"Publishing `{output_msg}` to topic `{self.topic_output}`")
            result = self.client.publish(self.topic_output, output_msg)
            status = result[0]
            if status == 0:
                print(f"Send `{output_msg}` to topic `{self.topic_output}`")
            else:
                print(f"Failed to send message to topic {self.topic_output}")
        except Exception as e:
            print(f"Error in publish: {e}")

    def connect_and_start(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker_url, self.port)
        self.client.loop_forever()
    

    

    
