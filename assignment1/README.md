# Producer-Consumer Pattern

A Java implementation of the producer-consumer pattern with thread synchronization.

## Prerequisites

-   Java 11 or higher
-   Maven 3.6+

## Setup & Run

```bash
# Build and run the application
./build-and-run.sh

# Run tests
./run-tests.sh
```

**Windows (PowerShell):**

```powershell
# Build and run
mvn clean compile exec:java -Dexec.mainClass="com.intuit.producerconsumer.ProducerConsumerApp"

# Run tests
mvn test
```

## Sample Output

```
Producer produced: 1
Consumer consumed: 1
Producer produced: 2
Consumer consumed: 2
Producer produced: 3
Consumer consumed: 3
Producer produced: 4
Consumer consumed: 4
Producer produced: 5
Consumer consumed: 5
Producer produced: 6
Consumer consumed: 6
Producer produced: 7
Consumer consumed: 7
Producer produced: 8
Consumer consumed: 8
Producer produced: 9
Consumer consumed: 9
Producer produced: 10
Consumer consumed: 10
Processed: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```
