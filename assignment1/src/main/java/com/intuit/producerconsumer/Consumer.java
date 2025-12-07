package com.intuit.producerconsumer;

import java.util.ArrayList;
import java.util.List;

public class Consumer<T> implements Runnable {
    private final SharedQueue<T> queue;
    private final List<T> consumed;
    private final String name;

    public Consumer(SharedQueue<T> queue, String name) {
        if (queue == null) {
            throw new IllegalArgumentException("Queue cannot be null");
        }
        this.queue = queue;
        this.consumed = new ArrayList<>();
        this.name = name;
    }

    @Override
    public void run() {
        Thread.currentThread().setName(name);
        
        try {
            T item;
            while ((item = queue.take()) != null) {
                consumed.add(item);
                Thread.sleep(75); // simulate work
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    public List<T> getConsumed() {
        return new ArrayList<>(consumed);
    }

    public String getConsumerName() {
        return name;
    }
}
