from rules_engine.engine import WinterSupplementRulesEngine
from rules_engine.rules import Rule_Child_Count,Rule_Couple,Rule_Eligiblity
from paho.mqtt.client import Client
from paho.mqtt.enums import CallbackAPIVersion
import random
import json
import logging

logging.basicConfig(level=logging.DEBUG)

broker_url = "test.mosquitto.org"
port = 1883
client_id = f'rules-engine-{random.randint(0,1000)}'

#Reference https://www.emqx.com/en/blog/how-to-use-mqtt-in-python
def on_connect(client:Client, userdata, flags, rc, properties):
    if rc == 0:
        print(f"Connected to MQTT Broker! with client id {client._client_id}")
        client.subscribe(topic_input)
    else:
        print("Failed to connect, return code", rc)


def publish(client:Client, topic:str, input_data:dict):
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

def on_message(client, userdata, msg):
    input_str = msg.payload.decode()
    input_data = json.loads(input_str)
    print(f"Received `{input_data}` from `{msg.topic}` topic")
    publish(client, topic_output, input_data)
    # Run the calculations



topic_id = "8eccc4ca-889e-4ab6-a44c-2789b05da4ce"
topic_prefix_input = "BRE/calculateWinterSupplementInput/"
topic_prefix_output = "BRE/calculateWinterSupplementOutput/"
topic_input = topic_prefix_input + topic_id
topic_output = topic_prefix_output + topic_id

engine = WinterSupplementRulesEngine()
engine.add_rule(Rule_Eligiblity)
engine.add_rule(Rule_Child_Count)
engine.add_rule(Rule_Couple)

winter_supplement_mqtt_client = Client(CallbackAPIVersion.VERSION2, client_id)
winter_supplement_mqtt_client.on_connect = on_connect
winter_supplement_mqtt_client.on_message = on_message
winter_supplement_mqtt_client.connect(broker_url, port)
winter_supplement_mqtt_client.loop_forever()