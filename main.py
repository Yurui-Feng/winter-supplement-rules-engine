import argparse
from rules_engine.mtqq_wrapper import MQTTWinterSupplementRulesEngine

# Example usage: poetry run python main.py --topic-id <topic-id>
def main():
    parser = argparse.ArgumentParser(description="Winter Supplement Rules Engine")
    parser.add_argument("--topic-id", type=str, required=True, help="The topic ID for the MQTT messages")
    args = parser.parse_args()

    engine = MQTTWinterSupplementRulesEngine(args.topic_id)
    engine.connect_and_start()

if __name__ == "__main__":
    main()
