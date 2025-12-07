package com.intuit.producerconsumer;

import java.util.Arrays;
import java.util.List;

public class ProducerConsumerApp {

    public static void main(String[] args) {
        List<Integer> data = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
        SharedQueue<Integer> queue = new SharedQueue<>(5);
        
        Producer<Integer> producer = new Producer<>(data, queue, "Producer");
        Consumer<Integer> consumer = new Consumer<>(queue, "Consumer");
        
        Thread producerThread = new Thread(producer);
        Thread consumerThread = new Thread(consumer);
        
        producerThread.start();
        consumerThread.start();
        
        try {
            producerThread.join();
            consumerThread.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        System.out.println("Processed: " + consumer.getConsumed());
    }
}
