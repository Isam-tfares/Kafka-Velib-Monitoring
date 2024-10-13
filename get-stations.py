import json
import time
import urllib.request
from kafka import KafkaProducer

API_KEY = "YOUR KEY"
url = f"https://api.jcdecaux.com/vls/v1/stations?apiKey={API_KEY}"

# Dictionary to track stations' availability
tracked_stations = {}

# Create a Kafka producer
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),  # Serialize values to JSON
    key_serializer=lambda k: str(k).encode('utf-8')  # Serialize keys to string
)

while True:
    try:
        # Fetch data from the API
        response = urllib.request.urlopen(url)
        stations = json.loads(response.read().decode())

        # Produce messages to the Kafka topic
        for station in stations:
            station_number = station["number"]
            contract = station["contract_name"]
            available_bikes = station["available_bikes"]

            data_to_send = {"number":station_number,"adresse": station["address"], "ville": contract, "nombre": available_bikes,"changeType":""}

            # Initialize contract in tracked_stations if not present
            if contract not in tracked_stations:
                tracked_stations[contract] = {}

            city_stations = tracked_stations[contract]

            # Initialize station number in city_stations if not present
            if station_number not in city_stations:
                city_stations[station_number] = available_bikes

            # Check and send messages for empty or non-empty stations
            if available_bikes == 0 and city_stations[station_number] != 0:
                city_stations[station_number] = 0
                # Send message to Kafka when station becomes empty
                data_to_send["changeType"] = "empty"
                producer.send("empty-stations", value=data_to_send, key=station["number"])
                print(f"Produced empty station message for {station['address']}")
            elif available_bikes != 0 and city_stations[station_number] == 0:
                city_stations[station_number] = available_bikes
                data_to_send["changeType"] = "refill"
                # Send message to Kafka when station refills
                producer.send("empty-stations", value=data_to_send, key=station["number"])
                print(f"Produced refill station message for {station['address']}")

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(1)  # Wait before the next API call
