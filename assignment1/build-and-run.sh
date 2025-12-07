#!/bin/bash

# Build and Run Script for Producer-Consumer Pattern
# This script compiles and runs the Java application

echo "=== Producer-Consumer Pattern Build Script ==="
echo ""

# Step 1: Clean previous build
echo "Cleaning previous build..."
rm -rf target
mkdir -p target/classes

# Step 2: Compile main source files
echo "Compiling source files..."
javac -d target/classes src/main/java/com/intuit/producerconsumer/*.java

if [ $? -ne 0 ]; then
    echo "ERROR: Compilation failed!"
    exit 1
fi

echo "✓ Compilation successful!"
echo ""

# Step 3: Run the application
echo "Running the application..."
echo "================================"
java -cp target/classes com.intuit.producerconsumer.ProducerConsumerApp

echo ""
echo "================================"
echo "✓ Application completed successfully!"
