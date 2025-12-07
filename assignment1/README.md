# Producer-Consumer Pattern

Java implementation of the classic producer-consumer pattern using wait/notify for thread synchronization.

## What It Does

- Producer thread reads items from a source list and puts them in a shared queue
- Consumer thread takes items from the queue and stores them in a destination list
- Queue has bounded capacity - producer blocks when full, consumer blocks when empty
- Uses Java's wait/notify for thread coordination

## Structure

```
src/main/java/
  ????????? SharedQueue.java       - Thread-safe bounded queue
  ????????? Producer.java          - Produces items into queue
  ????????? Consumer.java          - Consumes items from queue
  ????????? ProducerConsumerApp.java - Demo application

src/test/java/
  ????????? SharedQueueTest.java
  ????????? ProducerTest.java
  ????????? ConsumerTest.java
  ????????? ProducerConsumerIntegrationTest.java
```

## Running

**With Maven:**
```bash
mvn compile
mvn exec:java -Dexec.mainClass="com.intuit.producerconsumer.ProducerConsumerApp"
mvn test
```

**Without Maven:**
```bash
./build-and-run.sh    # compile and run
./run-tests.sh        # run tests
```

**Manual:**
```bash
mkdir -p target/classes
javac -d target/classes src/main/java/com/intuit/producerconsumer/*.java
java -cp target/classes com.intuit.producerconsumer.ProducerConsumerApp
```

## How It Works

The `SharedQueue` uses synchronized methods with wait/notify:

- **put()** - adds item, waits if queue is full, notifies consumers
- **take()** - removes item, waits if queue is empty, notifies producers  
- **setProducerDone()** - signals no more items coming

Producer runs until source is empty, then signals completion. Consumer runs until producer is done and queue is empty.

## Testing

32 tests covering:
- Thread synchronization
- Blocking behavior  
- FIFO ordering
- Multiple consumers
- Edge cases (empty source, interruption, etc)
