package com.intuit.producerconsumer;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Arrays;
import java.util.List;

public class ProducerConsumerIntegrationTest {

    @Test
    public void testSingleProducerSingleConsumer() throws InterruptedException {
        List<Integer> data = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
        SharedQueue<Integer> queue = new SharedQueue<>(5);
        
        Producer<Integer> producer = new Producer<>(data, queue, "Producer");
        Consumer<Integer> consumer = new Consumer<>(queue, "Consumer");
        
        Thread pt = new Thread(producer);
        Thread ct = new Thread(consumer);
        
        pt.start();
        ct.start();
        pt.join(10000);
        ct.join(10000);
        
        List<Integer> consumed = consumer.getConsumed();
        assertEquals(data.size(), consumed.size());
        assertTrue(consumed.containsAll(data));
    }

    @Test
    public void testMultipleConsumers() throws InterruptedException {
        List<Integer> data = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12);
        SharedQueue<Integer> queue = new SharedQueue<>(4);
        
        Producer<Integer> producer = new Producer<>(data, queue, "Producer");
        Consumer<Integer> c1 = new Consumer<>(queue, "Consumer-1");
        Consumer<Integer> c2 = new Consumer<>(queue, "Consumer-2");
        
        Thread pt = new Thread(producer);
        Thread ct1 = new Thread(c1);
        Thread ct2 = new Thread(c2);
        
        pt.start();
        ct1.start();
        ct2.start();
        pt.join(10000);
        ct1.join(10000);
        ct2.join(10000);
        
        int total = c1.getConsumed().size() + c2.getConsumed().size();
        assertEquals(data.size(), total);
    }

    @Test
    public void testDifferentTypes() throws InterruptedException {
        List<String> data = Arrays.asList("Alpha", "Beta", "Gamma", "Delta", "Epsilon");
        SharedQueue<String> queue = new SharedQueue<>(3);
        
        Producer<String> producer = new Producer<>(data, queue, "Producer");
        Consumer<String> consumer = new Consumer<>(queue, "Consumer");
        
        Thread pt = new Thread(producer);
        Thread ct = new Thread(consumer);
        
        pt.start();
        ct.start();
        pt.join(5000);
        ct.join(5000);
        
        assertEquals(data, consumer.getConsumed());
    }

    @Test
    public void testConcurrentStress() throws InterruptedException {
        List<Integer> data = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 
                                           11, 12, 13, 14, 15, 16, 17, 18, 19, 20);
        SharedQueue<Integer> queue = new SharedQueue<>(3);
        
        Producer<Integer> producer = new Producer<>(data, queue, "Producer");
        Consumer<Integer> c1 = new Consumer<>(queue, "C1");
        Consumer<Integer> c2 = new Consumer<>(queue, "C2");
        Consumer<Integer> c3 = new Consumer<>(queue, "C3");
        
        Thread pt = new Thread(producer);
        Thread ct1 = new Thread(c1);
        Thread ct2 = new Thread(c2);
        Thread ct3 = new Thread(c3);
        
        pt.start();
        ct1.start();
        ct2.start();
        ct3.start();
        
        pt.join(15000);
        ct1.join(15000);
        ct2.join(15000);
        ct3.join(15000);
        
        int total = c1.getConsumed().size() + c2.getConsumed().size() + c3.getConsumed().size();
        assertEquals(data.size(), total);
        
        // Check no duplicates
        for (Integer item : c1.getConsumed()) {
            assertFalse(c2.getConsumed().contains(item) || c3.getConsumed().contains(item));
        }
    }

    @Test
    public void testEmptySource() throws InterruptedException {
        List<Integer> data = Arrays.asList();
        SharedQueue<Integer> queue = new SharedQueue<>(5);
        
        Producer<Integer> producer = new Producer<>(data, queue, "Producer");
        Consumer<Integer> consumer = new Consumer<>(queue, "Consumer");
        
        Thread pt = new Thread(producer);
        Thread ct = new Thread(consumer);
        
        pt.start();
        ct.start();
        pt.join(2000);
        ct.join(2000);
        
        assertTrue(consumer.getConsumed().isEmpty());
        assertTrue(queue.isEmpty());
        assertTrue(queue.isProducerDone());
    }
}
