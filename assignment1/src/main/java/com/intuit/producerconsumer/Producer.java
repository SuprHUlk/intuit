package com.intuit.producerconsumer;

import java.util.List;

public class Producer<T> implements Runnable {
    private final List<T> source;
    private final SharedQueue<T> queue;
    private final String name;

    public Producer(List<T> source, SharedQueue<T> queue, String name) {
        if (source == null || queue == null) {
            throw new IllegalArgumentException("Source and queue cannot be null");
        }
        this.source = source;
        this.queue = queue;
        this.name = name;
    }

    @Override
    public void run() {
        Thread.currentThread().setName(name);
        
        try {
            for (T item : source) {
                queue.put(item);
                Thread.sleep(50); // simulate work
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            queue.setProducerDone();
        }
    }

    public String getProducerName() {
        return name;
    }
}
