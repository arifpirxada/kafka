import kafka from "./client";
import { ICustomPartitioner } from "kafkajs";

type Message = {
  type: 'public' | 'private',
  message: string
}

const customPartitioner: ICustomPartitioner = () => {
  return ({ topic, partitionMetadata, message }) => {
    if (!message.value) {
      console.warn("Received message with null value");
      return 0;
    }
    const messageVal: Message = JSON.parse(
      Buffer.isBuffer(message.value) ? message.value.toString() : message.value
    );

    console.log(messageVal);

    if (messageVal.type === 'public') {
      return 0;
    } else if (messageVal.type === 'private') {
      return 1;
    }

    return 0;
  };
};

const produceMessages = async (type: string, message: string) => {
  const producer = kafka.producer({
    createPartitioner: customPartitioner
  });

  await producer.connect();

  const newMessage = JSON.stringify({ type, message });
  await producer.send({
    topic: "messages",
    messages: [{ key: "new-message", value: newMessage }],
  });
};

export default produceMessages;
