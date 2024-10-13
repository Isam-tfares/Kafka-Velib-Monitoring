#! /usr/bin/env python3
import json
from kafka import KafkaConsumer

consumer = KafkaConsumer("empty-stations", bootstrap_servers='localhost:9092',
                         group_id="velib-monitor-stations")

for message in consumer:
    try:
        station = json.loads(message.value.decode())
        print(f"Station {station['adresse']} in {station['ville']} is now {station['changeType']} with {station['nombre']} bikes")
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
    except KeyError as e:
        print(f"Missing expected key in message: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")