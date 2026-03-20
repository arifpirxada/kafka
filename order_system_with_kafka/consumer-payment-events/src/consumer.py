import os
import logging
import asyncio
import json
from confluent_kafka import Consumer
from .db.db import async_session
from .models.order_model import Order
from sqlalchemy import update
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("consumer-payment-events")

# Get Kafka broker urls
KAFKA_URL = os.getenv("KAFKA_URL", "kafka:9092")
KAFKA_URL_2 = os.getenv("KAFKA_URL_2")

kafka_servers = [KAFKA_URL]

if KAFKA_URL_2 is not None:
    kafka_servers.append(KAFKA_URL_2)


class KafkaConsumer:
    def __init__(self, topics):
        self.conf = {
            "bootstrap.servers": ",".join(kafka_servers),
            "group.id": "consumer-payment-events",
            "enable.auto.commit": False,
        }
        self.consumer = Consumer(self.conf)
        self.running = True
        self.topics = topics

    async def process_message(self, msg):
        data = json.loads(msg.value().decode("utf-8"))

        logger.info(f"type: {data['type']}, order_id: {data['order_id']}")

        pay_status = "SUCCESS" if data["type"] == "PAYMENT_SUCCESS" else "FAILED"

        async with async_session() as db:          # ← real AsyncSession
            await db.execute(
                update(Order)
                .where(Order.id == data["order_id"])
                .values(payment_status=pay_status)
            )
            await db.commit()

        self.consumer.commit(asynchronous=False)


    async def run(self):
        self.consumer.subscribe(self.topics)

        logger.info(f"Consumer Subscribed: {', '.join(self.topics)}")

        try:
            while self.running:
                msg = await asyncio.to_thread(self.consumer.poll, 1.0)

                if msg is None:
                    # logger.info("Waiting...")
                    continue
                elif msg.error():
                    logger.error(f"Error: {msg.error()}")
                    raise
                else:
                    await self.process_message(msg)

        except Exception as e:
            logger.error(f"Error consuming messages: {e}")
            raise
        finally:
            self.consumer.close()
            logger.info("🛑 Consumer connection closed.")
                
    def stop(self):
        self.running = False