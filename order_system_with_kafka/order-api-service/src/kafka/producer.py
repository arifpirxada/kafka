import os
import json
import asyncio
from confluent_kafka import Producer
from dotenv import load_dotenv

load_dotenv()

KAFKA_URL = os.getenv("KAFKA_URL", "kafka:9092")
KAFKA_URL_2 = os.getenv("KAFKA_URL_2")

kafka_urls = [KAFKA_URL]

if KAFKA_URL_2 is not None:
    kafka_urls.append(KAFKA_URL_2)

class KafkaProducer:
    def __init__(self):
        self.conf = {
            "bootstrap.servers": ",".join(kafka_urls),
            "client.id": "order-api-service",

            "linger.ms": 5,
            "compression.type": "snappy"
        }
        self.producer = Producer(self.conf)

    def delivery_callback(self, err, msg):
        if err:
            print('ERROR: Message failed delivery: {}'.format(err))
        else:
            key = msg.key().decode("utf-8") if msg.key() else None
            value = msg.value().decode("utf-8") if msg.value() else None
            print(
                f"Produced event to topic {msg.topic()} "
                f"partition={msg.partition()} offset={msg.offset()} "
                f"key={key} value={value}"
            )
            

    async def send_message(self, topic: str, key: str, value: dict):
        try:
            payload = json.dumps(value).encode("utf-8")

            self.producer.produce(topic, key=key.encode("utf-8"), value=payload, callback=self.delivery_callback)

            await asyncio.to_thread(self.producer.poll, 0)

        except Exception as e:
            print(f"Error producing to Kafka: {e}")


    def flush(self):
        """Ensure all messages are sent before shutdown"""
        self.producer.flush()


kafka_producer = KafkaProducer()