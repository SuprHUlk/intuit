package com.intuit.producerconsumer;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

public class SharedQueueTest {
    private SharedQueue<Integer> queue;

    @BeforeEach
    public void setUp() {
        queue = new SharedQueue<>(3);
    }

    @Test
    public void testInitialization() {
        assertTrue(queue.isEmpty());
        assertEquals(0, queue.size());
        assertFalse(queue.isProducerDone());
    }

    @Test
    public void testInvalidCapacity() {
        assertThrows(IllegalArgumentException.class, () -> new SharedQueue<>(0));
        assertThrows(IllegalArgumentException.class, () -> new SharedQueue<>(-1));
    }

    @Test
    public void testPut() throws InterruptedException {
        queue.put(1);
        queue.put(2);
        assertEquals(2, queue.size());
        assertFalse(queue.isEmpty());
    }

    @Test
    public void testTake() throws InterruptedException {
        queue.put(10);
        queue.put(20);
        
        assertEquals(10, queue.take());
        assertEquals(20, queue.take());
        assertTrue(queue.isEmpty());
    }

    @Test
    public void testPutBlocking() throws InterruptedException {
        queue.put(1);
        queue.put(2);
        queue.put(3);
        
        final boolean[] putSucceeded = {false};
        
        Thread producerThread = new Thread(() -> {
            try {
                queue.put(4);
                putSucceeded[0] = true;
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        producerThread.start();
        Thread.sleep(100);
        assertFalse(putSucceeded[0]);
        
        queue.take();
        producerThread.join(1000);
        assertTrue(putSucceeded[0]);
    }

    @Test
    public void testTakeBlocking() throws InterruptedException {
        final Integer[] result = {null};
        
        Thread consumerThread = new Thread(() -> {
            try {
                result[0] = queue.take();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        consumerThread.start();
        Thread.sleep(100);
        assertNull(result[0]);
        
        queue.put(42);
        consumerThread.join(1000);
        assertEquals(42, result[0]);
    }

    @Test
    public void testTakeWhenProducerDone() throws InterruptedException {
        queue.setProducerDone();
        assertNull(queue.take());
    }

    @Test
    public void testFIFOOrdering() throws InterruptedException {
        queue.put(1);
        queue.put(2);
        queue.put(3);
        
        assertEquals(1, queue.take());
        assertEquals(2, queue.take());
        assertEquals(3, queue.take());
    }

    @Test
    public void testMultipleThreads() throws InterruptedException {
        final int numItems = 10;
        final Integer[] consumedCount = {0};
        
        Thread producer = new Thread(() -> {
            try {
                for (int i = 0; i < numItems; i++) {
                    queue.put(i);
                }
                queue.setProducerDone();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        Thread consumer = new Thread(() -> {
            try {
                Integer item;
                while ((item = queue.take()) != null) {
                    consumedCount[0]++;
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        producer.start();
        consumer.start();
        producer.join(5000);
        consumer.join(5000);
        
        assertEquals(numItems, consumedCount[0]);
        assertTrue(queue.isEmpty());
    }

    @Test
    public void testSetProducerDone() throws InterruptedException {
        final Integer[] result = {-1};
        
        Thread consumer = new Thread(() -> {
            try {
                result[0] = queue.take();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        consumer.start();
        Thread.sleep(100);
        queue.setProducerDone();
        consumer.join(1000);
        
        assertNull(result[0]);
        assertTrue(queue.isProducerDone());
    }
}
