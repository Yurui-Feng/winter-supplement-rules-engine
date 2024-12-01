import random
import json
from paho.mqtt.client import Client
from paho.mqtt.enums import CallbackAPIVersion
from rules_engine.engine import WinterSupplementRulesEngine
from rules_engine.rules import Rule_Child_Count, Rule_Couple, Rule_Eligiblity

# MQTT Configuration
broker_url = "test.mosquitto.org"
port = 1883
client_id = f'rules-engine-{random.randint(0,1000)}'

topic_id = "8b4a8cf8-5b53-4aa9-b139-23d434713094"
topic_prefix_input = "BRE/calculateWinterSupplementInput/"
topic_prefix_output = "BRE/calculateWinterSupplementOutput/"
topic_input = topic_prefix_input + topic_id
topic_output = topic_prefix_output + topic_id

# Rules Engine Setup
engine = WinterSupplementRulesEngine()
engine.add_rule(Rule_Eligiblity)
engine.add_rule(Rule_Child_Count)
engine.add_rule(Rule_Couple)

# MQTT Callback Functions, reference https://www.emqx.com/en/blog/how-to-use-mqtt-in-python
def on_connect(client: Client, userdata, flags, rc, properties):
    try:
        if rc == 0:
            print(f"Connected to MQTT Broker!")
            result, _ = client.subscribe(topic_input)
            if result == 0:
                print(f"Subscribed to topic `{topic_input}` successfully")
            else:
                print(f"Failed to subscribe to topic `{topic_input}`, result code: {result}")
        else:
            print("Failed to connect, return code", rc)
    except Exception as e:
        print(f"Error in on_connect: {e}")

def on_message(client, userdata, msg):
    try:
        input_str = msg.payload.decode()
        input_data = json.loads(input_str)
        print(f"Received `{input_data}` from `{msg.topic}` topic")
        publish(client, topic_output, input_data)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"Error in on_message: {e}")

def publish(client: Client, topic: str, input_data: dict):
    try:
        message_id = input_data["id"]
        output_data = engine.run(input_data)
        output_data["id"] = message_id
        output_msg = json.dumps(output_data)
        result = client.publish(topic, output_msg)
        status = result[0]
        if status == 0:
            print(f"Send `{output_msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
    except Exception as e:
        print(f"Error in publish: {e}")

# MQTT Client Setup
winter_supplement_mqtt_client = Client(callback_api_version=CallbackAPIVersion.VERSION2, client_id=client_id)
winter_supplement_mqtt_client.on_connect = on_connect
winter_supplement_mqtt_client.on_message = on_message
winter_supplement_mqtt_client.connect(broker_url, port)
winter_supplement_mqtt_client.loop_forever()