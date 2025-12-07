#!/bin/bash

# Sales Data Analysis - Run Script
# This script runs the sales data analysis application

echo "=========================================="
echo "Sales Data Analysis Application"
echo "=========================================="
echo ""

# Navigate to src directory
cd "$(dirname "$0")/src"

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

# Run the analysis
echo "Running sales data analysis..."
echo ""
$PYTHON_CMD sales_analysis.py

# Capture exit code
EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "Analysis completed successfully!"
else
    echo "Analysis failed with exit code: $EXIT_CODE"
fi

exit $EXIT_CODE
