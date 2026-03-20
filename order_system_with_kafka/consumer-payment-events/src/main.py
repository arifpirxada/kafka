import asyncio
import signal
from .consumer import KafkaConsumer
from .db.db import check_connection

async def main():
    await check_connection()

    consumer = KafkaConsumer(topics=["order-events"])

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, consumer.stop)

    await consumer.run()

if __name__ == "__main__":
    asyncio.run(main())