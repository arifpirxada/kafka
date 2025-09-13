const { Kafka } = require("kafkajs");

const kafka = new Kafka({
  clientId: "my-app",
  brokers: ["kafka:9092"],
});

(async () => {
  const admin = kafka.admin();
  try {
    console.log("Admin connecting...");
    await admin.connect();
    console.log("Admin connection success.");

    const created = await admin.createTopics({
      topics: [
        {
          topic: "messages",
          numPartitions: 2,
          replicationFactor: 1,
        },
      ],
      waitForLeaders: true,
    });

    if (created) {
      console.log('Topic "messages" created.');
    } else {
      console.log('Topic "messages" already exists or not created.');
    }
  } catch (err) {
    console.error("Admin error:", err);
  } finally {
    console.log("Disconnecting admin...");
    await admin.disconnect();
  }
})();
