#!/bin/sh

echo "Waiting for Kafka..."

until kafka-topics.sh --list --bootstrap-server kafka:9092 >/dev/null 2>&1; do
  echo "Kafka not ready yet..."
  sleep 2
done

echo "Kafka is ready. Creating topics..."

kafka-topics.sh --create --if-not-exists \
  --topic order-events \
  --bootstrap-server kafka:9092 \
  --partitions 3 \
  --replication-factor 3

echo "Final topic list:"
kafka-topics.sh --list --bootstrap-server kafka:9092