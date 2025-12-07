package com.intuit.producerconsumer;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

import java.util.List;

public class ConsumerTest {
    private SharedQueue<Integer> queue;

    @BeforeEach
    public void setUp() {
        queue = new SharedQueue<>(5);
    }

    @Test
    public void testNullQueue() {
        assertThrows(IllegalArgumentException.class, 
            () -> new Consumer<>(null, "Consumer"));
    }

    @Test
    public void testConsumeAll() throws InterruptedException {
        queue.put(1);
        queue.put(2);
        queue.put(3);
        queue.setProducerDone();
        
        Consumer<Integer> consumer = new Consumer<>(queue, "TestConsumer");
        Thread t = new Thread(consumer);
        t.start();
        t.join(3000);
        
        List<Integer> consumed = consumer.getConsumed();
        assertEquals(3, consumed.size());
        assertTrue(consumed.contains(1));
        assertTrue(consumed.contains(2));
        assertTrue(consumed.contains(3));
    }

    @Test
    public void testConsumerName() {
        Consumer<Integer> consumer = new Consumer<>(queue, "MyConsumer");
        assertEquals("MyConsumer", consumer.getConsumerName());
    }

    @Test
    public void testEmptyQueue() throws InterruptedException {
        queue.setProducerDone();
        Consumer<Integer> consumer = new Consumer<>(queue, "EmptyConsumer");
        
        Thread t = new Thread(consumer);
        t.start();
        t.join(2000);
        
        assertTrue(consumer.getConsumed().isEmpty());
    }

    @Test
    public void testOrder() throws InterruptedException {
        queue.put(10);
        queue.put(20);
        queue.put(30);
        queue.setProducerDone();
        
        Consumer<Integer> consumer = new Consumer<>(queue, "OrderConsumer");
        Thread t = new Thread(consumer);
        t.start();
        t.join(3000);
        
        List<Integer> consumed = consumer.getConsumed();
        assertEquals(3, consumed.size());
        assertEquals(10, consumed.get(0));
        assertEquals(20, consumed.get(1));
        assertEquals(30, consumed.get(2));
    }

    @Test
    public void testBlocking() throws InterruptedException {
        Consumer<Integer> consumer = new Consumer<>(queue, "BlockingConsumer");
        final boolean[] finished = {false};
        
        Thread t = new Thread(() -> {
            consumer.run();
            finished[0] = true;
        });
        
        t.start();
        Thread.sleep(300);
        assertFalse(finished[0]);
        
        queue.put(42);
        queue.setProducerDone();
        t.join(2000);
        
        assertTrue(finished[0]);
        assertEquals(1, consumer.getConsumed().size());
        assertEquals(42, consumer.getConsumed().get(0));
    }

    @Test
    public void testInterruption() throws InterruptedException {
        Consumer<Integer> consumer = new Consumer<>(queue, "InterruptConsumer");
        Thread t = new Thread(consumer);
        t.start();
        Thread.sleep(200);
        t.interrupt();
        t.join(2000);
        
        assertFalse(t.isAlive());
    }

    @Test
    public void testGetConsumedReturnsCopy() throws InterruptedException {
        queue.put(1);
        queue.setProducerDone();
        
        Consumer<Integer> consumer = new Consumer<>(queue, "CopyConsumer");
        Thread t = new Thread(consumer);
        t.start();
        t.join(2000);
        
        List<Integer> list1 = consumer.getConsumed();
        List<Integer> list2 = consumer.getConsumed();
        
        assertNotSame(list1, list2);
        assertEquals(list1, list2);
    }

    @Test
    public void testDifferentTypes() throws InterruptedException {
        SharedQueue<String> strQueue = new SharedQueue<>(5);
        strQueue.put("Hello");
        strQueue.put("World");
        strQueue.setProducerDone();
        
        Consumer<String> consumer = new Consumer<>(strQueue, "StringConsumer");
        Thread t = new Thread(consumer);
        t.start();
        t.join(2000);
        
        List<String> consumed = consumer.getConsumed();
        assertEquals(2, consumed.size());
        assertEquals("Hello", consumed.get(0));
        assertEquals("World", consumed.get(1));
    }
}
