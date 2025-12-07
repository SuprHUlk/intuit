#!/bin/bash

# Test Script for Producer-Consumer Pattern
# Compiles and runs all unit tests

echo "=== Producer-Consumer Pattern Test Script ==="
echo ""

# Check if JUnit JAR exists
JUNIT_JAR="junit-platform-console-standalone-1.9.3.jar"
JUNIT_URL="https://repo1.maven.org/maven2/org/junit/platform/junit-platform-console-standalone/1.9.3/junit-platform-console-standalone-1.9.3.jar"

if [ ! -f "$JUNIT_JAR" ]; then
    echo "JUnit standalone JAR not found. Downloading..."
    curl -L -o "$JUNIT_JAR" "$JUNIT_URL"
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to download JUnit JAR"
        echo "Please download it manually from: $JUNIT_URL"
        exit 1
    fi
    echo "✓ JUnit JAR downloaded"
fi

# Step 1: Clean and create directories
echo "Preparing build directories..."
rm -rf target
mkdir -p target/classes
mkdir -p target/test-classes

# Step 2: Compile main source files
echo "Compiling source files..."
javac -d target/classes src/main/java/com/intuit/producerconsumer/*.java

if [ $? -ne 0 ]; then
    echo "ERROR: Source compilation failed!"
    exit 1
fi

echo "✓ Source files compiled"

# Step 3: Compile test files
echo "Compiling test files..."
javac -cp "$JUNIT_JAR:target/classes" -d target/test-classes src/test/java/com/intuit/producerconsumer/*.java

if [ $? -ne 0 ]; then
    echo "ERROR: Test compilation failed!"
    exit 1
fi

echo "✓ Test files compiled"

# Step 4: Run tests
echo ""
echo "Running tests..."
echo "================================"
java -jar "$JUNIT_JAR" \
    --class-path "target/classes:target/test-classes" \
    --scan-class-path \
    --disable-banner

echo ""
echo "================================"
echo "✓ Tests completed!"
