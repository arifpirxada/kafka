import kafka from "./client";

const consumeMessages = async (group: string) => {
  const consumer = kafka.consumer({ groupId: group });

  await consumer.connect();

  await consumer.subscribe({ topics: ["messages"] });

  await consumer.run({
    eachMessage: async ({ topic, partition, message, heartbeat, pause }) => {
      if (!message.value) {
        console.warn("Received message with null value");
        return;
      }

      console.log(
        `\nGROUP: ${group}, TOPIC: ${topic}, PARTITION: ${partition}`
      );
      console.log(`MESSAGE: ${message.value.toString()}`);
    },
  });
};

export default consumeMessages;
