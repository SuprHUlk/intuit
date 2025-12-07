package com.intuit.producerconsumer;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Arrays;
import java.util.List;

public class ProducerTest {
    private SharedQueue<Integer> queue;
    private List<Integer> source;

    @BeforeEach
    public void setUp() {
        queue = new SharedQueue<>(5);
        source = Arrays.asList(1, 2, 3, 4, 5);
    }

    @Test
    public void testNullParameters() {
        assertThrows(IllegalArgumentException.class, 
            () -> new Producer<>(null, queue, "Producer"));
        assertThrows(IllegalArgumentException.class, 
            () -> new Producer<>(source, null, "Producer"));
    }

    @Test
    public void testProduceAllItems() throws InterruptedException {
        Producer<Integer> producer = new Producer<>(source, queue, "TestProducer");
        Thread t = new Thread(producer);
        t.start();
        t.join(5000);
        
        assertTrue(queue.isProducerDone());
        assertEquals(5, queue.size());
    }

    @Test
    public void testProducerName() {
        Producer<Integer> producer = new Producer<>(source, queue, "MyProducer");
        assertEquals("MyProducer", producer.getProducerName());
    }

    @Test
    public void testEmptySource() throws InterruptedException {
        Producer<Integer> producer = new Producer<>(Arrays.asList(), queue, "EmptyProducer");
        Thread t = new Thread(producer);
        t.start();
        t.join(2000);
        
        assertTrue(queue.isProducerDone());
        assertTrue(queue.isEmpty());
    }

    @Test
    public void testProducerOrder() throws InterruptedException {
        List<String> strings = Arrays.asList("A", "B", "C");
        SharedQueue<String> strQueue = new SharedQueue<>(5);
        Producer<String> producer = new Producer<>(strings, strQueue, "OrderProducer");
        
        Thread t = new Thread(producer);
        t.start();
        t.join(3000);
        
        assertEquals("A", strQueue.take());
        assertEquals("B", strQueue.take());
        assertEquals("C", strQueue.take());
    }

    @Test
    public void testProducerBlocking() throws InterruptedException {
        SharedQueue<Integer> smallQueue = new SharedQueue<>(2);
        List<Integer> largeSource = Arrays.asList(1, 2, 3, 4, 5);
        Producer<Integer> producer = new Producer<>(largeSource, smallQueue, "BlockingProducer");
        
        final boolean[] running = {true};
        Thread t = new Thread(() -> {
            producer.run();
            running[0] = false;
        });
        
        t.start();
        Thread.sleep(500);
        assertTrue(running[0]);
        
        while (smallQueue.size() > 0) {
            smallQueue.take();
        }
        
        t.join(3000);
        assertFalse(running[0]);
    }

    @Test
    public void testProducerInterruption() throws InterruptedException {
        List<Integer> largeSource = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
        Producer<Integer> producer = new Producer<>(largeSource, queue, "InterruptProducer");
        
        Thread t = new Thread(producer);
        t.start();
        Thread.sleep(200);
        t.interrupt();
        t.join(2000);
        
        assertFalse(t.isAlive());
    }
}
