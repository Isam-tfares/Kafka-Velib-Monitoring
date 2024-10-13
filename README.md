# Kafka-Velib-Monitoring

## Overview

**Kafka-Velib-Monitoring** is a real-time bike station monitoring system that tracks the availability of bikes at Velib stations across different cities. Using Kafka, the system sends messages when stations become empty or refill with bikes. The data is fetched from the JCDecaux Velib API, and messages are produced and consumed via Apache Kafka.

This project contains two main components:

- **Producer**: Fetches data from the Velib API, processes it, and sends messages to a Kafka topic.
- **Consumer**: Listens for messages from the Kafka topic and logs changes in bike availability.

## Features

- Fetches real-time bike station data from the JCDecaux Velib API.
- Tracks bike availability across cities.
- Sends Kafka messages when a station becomes empty or refills with bikes.
- Displays changes in station status using a Kafka consumer.

## Requirements

To run this project, you need the following software installed:

- Python 3.x
- Kafka (with Zookeeper)
- JCDecaux API key

### Python Packages

Install the required Python libraries using:

```bash
pip install kafka-python
```

## Setup

### 1. Start Kafka and Zookeeper

Ensure that Kafka and Zookeeper are installed and configured. You can start them using the following commands:

#### Start Zookeeper:

```bash
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
```

#### Start Kafka:

```bash
.\bin\windows\kafka-server-start.bat .\config\server.properties
```

### 2. Create Kafka Topic

Create a Kafka topic called `empty-stations`:

```bash
.\bin\windows\kafka-topics.bat --create --topic empty-stations --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### 3. Run Producer (get-stations.py)

The producer fetches data from the Velib API and sends messages when bike stations become empty or refill. Run the producer using:

```bash
python get_stations.py
```

### 4. Run Consumer (monitor_stations.py)

The consumer listens for messages from the Kafka topic and logs the status of the stations. Run the consumer using:

```bash
python monitor_stations.py
```

## How It Works

- The `get_stations.py` script continuously fetches data from the JCDecaux Velib API and monitors the number of available bikes at each station.
- If a station runs out of bikes or refills, a message is sent to the Kafka topic `empty-stations`.
- The `monitor_stations.py` script consumes messages from the `empty-stations` topic and logs the changes in the terminal.

## File Descriptions

- **get_stations.py**: This script fetches real-time bike station data and produces Kafka messages for bike availability changes.
- **monitor_stations.py**: This script consumes Kafka messages and logs the changes in bike availability.

## API Used

This project uses the **JCDecaux Velib API** to fetch real-time bike availability data for stations.

### Example Message

When a station becomes empty or refills, a message is produced with the following format:

```json
{
    "number": 12345,
    "adresse": "123 Rue Example",
    "ville": "Paris",
    "nombre": 0,
    "changeType": "empty"
}
```

- `number`: The station number.
- `adresse`: The station address.
- `ville`: The city where the station is located.
- `nombre`: The number of available bikes.
- `changeType`: Indicates if the station is "empty" or "refill".

## Troubleshooting

- **Zookeeper/Kafka not starting**: Ensure that the paths to your Kafka and Zookeeper configurations are correct.
- **Messages not appearing in the consumer**: Ensure that Kafka is running and the topic `empty-stations` has been created successfully. Check that the producer is sending messages to the correct topic.
- **Connection errors**: Ensure your Kafka server is running on the correct `localhost:9092` and is accessible.

