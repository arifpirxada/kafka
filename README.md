# Kafka

This repository contains basic minimal code for kafka. It uses kafka.js

**What It can do?**   

- You can send messages in one terminal.
- And consume them in another terminal, you can specify consumer groups.

<br>       

## Prequisites

- Docker
    
<br>       

# Get Started

### 1. Clone the repository

```bash
git clone git@github.com:arifpirxada/kafka.git
```

### 2. RUN

```bash
docker compose up -d
```

<br>

# How to use

### 1. Open three terminals

### 2. RUN

Run these in all three terminals

```bash
docker exec -it kafka-node-1 bash
```

Now run

```bash
pnpm dev
```

You can use below commands for producing & consuming messages

**produce**: to start producing messages"    
**consume <group>**: start consuming messages"   
- Example
- ```consume default```
