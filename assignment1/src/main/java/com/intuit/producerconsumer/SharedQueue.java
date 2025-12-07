package com.intuit.producerconsumer;

import java.util.LinkedList;
import java.util.Queue;

public class SharedQueue<T> {
    private final Queue<T> queue;
    private final int capacity;
    private volatile boolean producerDone = false;

    public SharedQueue(int capacity) {
        if (capacity <= 0) {
            throw new IllegalArgumentException("Capacity must be positive");
        }
        this.capacity = capacity;
        this.queue = new LinkedList<>();
    }

    public synchronized void put(T item) throws InterruptedException {
        while (queue.size() == capacity) {
            wait();
        }
        queue.add(item);
        notifyAll();
    }

    public synchronized T take() throws InterruptedException {
        while (queue.isEmpty() && !producerDone) {
            wait();
        }
        
        if (queue.isEmpty()) {
            return null;
        }
        
        T item = queue.poll();
        notifyAll();
        return item;
    }

    public synchronized void setProducerDone() {
        this.producerDone = true;
        notifyAll();
    }

    public synchronized int size() {
        return queue.size();
    }

    public synchronized boolean isEmpty() {
        return queue.isEmpty();
    }

    public synchronized boolean isProducerDone() {
        return producerDone;
    }
}
