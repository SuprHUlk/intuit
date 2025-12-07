#!/bin/bash

# Sales Data Analysis - Test Runner Script
# This script runs the test suite for the sales data analysis application

echo "=========================================="
echo "Sales Data Analysis - Test Suite"
echo "=========================================="
echo ""

# Get the directory of the script
SCRIPT_DIR="$(dirname "$0")"
cd "$SCRIPT_DIR"

# Check if Python is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "Using Python $PYTHON_VERSION"
echo ""

# Check if pytest is installed
if ! $PYTHON_CMD -c "import pytest" 2>/dev/null; then
    echo "pytest is not installed."
    echo "Installing pytest..."
    $PYTHON_CMD -m pip install pytest pytest-cov --quiet
    
    if [ $? -eq 0 ]; then
        echo "pytest installed successfully!"
        echo ""
    else
        echo "Error: Failed to install pytest"
        echo "Please install it manually: pip install pytest pytest-cov"
        exit 1
    fi
fi

# Run tests
echo "Running tests..."
echo ""

# Check if pytest-cov is available for coverage
if $PYTHON_CMD -c "import pytest_cov" 2>/dev/null; then
    # Run with coverage
    $PYTHON_CMD -m pytest tests/test_sales_analysis.py -v --cov=src --cov-report=term-missing
else
    # Run without coverage
    $PYTHON_CMD -m pytest tests/test_sales_analysis.py -v
fi

# Capture exit code
EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "=========================================="
    echo "All tests passed! ✅"
    echo "=========================================="
else
    echo "=========================================="
    echo "Some tests failed! ❌"
    echo "=========================================="
fi

exit $EXIT_CODE
