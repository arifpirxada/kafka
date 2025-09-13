import readline from "readline";
import produceMessages from "./kafka/producer";
import consumeMessages from "./kafka/consumer";

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});
const logInstructions = () => {
  console.log("COMMANDS: \n");
  console.log("produce: to start producing messages");
  console.log(
    "consume <type>: start consuming messages (type - public or private)"
  );
  console.log("clear: to clear console");
  console.log("exit: to quit the application \n");
};

logInstructions();

rl.setPrompt("Enter your COMMAND: ");
rl.prompt();

let producingMode = false;

rl.on("line", async (input) => {
  input = input.trim();

  if (producingMode) {
    rl.setPrompt("> ");
    rl.prompt();

    const [type, ...messageParts] = input.split(" ");
    const message = messageParts.join(" ");

    if (type !== "public" && type !== "private") {
      console.log("type can only be public or private. Exiting produce mode.");
      producingMode = false;
      rl.setPrompt("Enter your COMMAND: ");
      rl.prompt();
      return;
    }

    await produceMessages(type, message);
    rl.setPrompt("> ");
    rl.prompt();
    return;
  }

  input = input.toLowerCase();

  if (input === "produce") {
    console.log("Starting message production...");
    console.log("Format <type (public | private)> <message>");

    producingMode = true;
    rl.setPrompt("> ");
    rl.prompt();
    return;
  } else if (/^consume\s+\S+/.test(input)) {
    console.log("Starting message consumption...");
    const cmd = input.split(" ");

    consumeMessages(cmd[1]);
  } else if (input === "clear") {
    console.clear();

    logInstructions();
  } else if (input === "exit") {
    console.log("Exiting the application...");
    rl.close();
  } else {
    console.log(`Unknown command: ${input}`);
  }

  rl.setPrompt("Enter your COMMAND: ");
  rl.prompt();
}).on("close", () => {
  console.log("Goodbye!");
  process.exit(0);
});
