#!/bin/sh

echo "Waiting for Kafka cluster (3 brokers)..."

until [ "$(/opt/kafka/bin/kafka-broker-api-versions.sh --bootstrap-server kafka:9092 2>/dev/null | grep -c 'id:')" -ge 3 ]; do
  echo "Waiting for all 3 brokers to register..."
  sleep 2
done

echo "All 3 brokers ready. Creating topics..."

/opt/kafka/bin/kafka-topics.sh --create --if-not-exists \
  --topic order-events \
  --bootstrap-server kafka:9092 \
  --partitions 3 \
  --replication-factor 3

echo "Final topic list:"
/opt/kafka/bin/kafka-topics.sh --list --bootstrap-server kafka:9092