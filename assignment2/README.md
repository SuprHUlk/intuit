# Sales Data Analysis - Assignment 2

A Python application that performs data analysis on CSV sales data using functional programming paradigms.

## Setup

### Requirements

-   Python 3.8+
-   pip

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Running the Application

```bash
# Run the analysis
./run-analysis.sh

# Or run directly
cd src
python sales_analysis.py
```

## Running Tests

```bash
# Run tests
./run-tests.sh

# Or run with pytest
pytest tests/test_sales_analysis.py -v
```

## Sample Output

```
================================================================================
SALES DATA ANALYSIS REPORT
================================================================================

1. TOTAL REVENUE
--------------------------------------------------------------------------------
Total Revenue: $28,473.50

2. REVENUE BY CATEGORY
--------------------------------------------------------------------------------
Electronics         : $20,363.50
Furniture           : $6,415.00
Stationery          : $1,695.00

3. REVENUE BY REGION
--------------------------------------------------------------------------------
West                : $10,040.00
North               : $8,776.50
East                : $4,845.00
South               : $4,812.00

4. TOP 5 PRODUCTS BY REVENUE
--------------------------------------------------------------------------------
1. Laptop                         - Revenue: $12,000.00, Quantity: 10
2. Monitor                        - Revenue: $2,250.00, Quantity: 5
3. Office Suite Software          - Revenue: $1,350.00, Quantity: 3
4. Conference Table               - Revenue: $1,200.00, Quantity: 1
5. Desktop Computer               - Revenue: $950.00, Quantity: 1

5. REVENUE BY MONTH
--------------------------------------------------------------------------------
2024-01: $8,306.00
2024-02: $11,037.50
2024-03: $9,130.00

6. AVERAGE ORDER VALUE
--------------------------------------------------------------------------------
Average Order Value: $569.47

7. PERFORMANCE BY SALESPERSON
--------------------------------------------------------------------------------
SP003: Revenue: $11,096.00, Orders: 16, Avg Order: $693.50
SP002: Revenue: $8,962.50, Orders: 17, Avg Order: $527.21
SP001: Revenue: $8,415.00, Orders: 17, Avg Order: $495.00

8. DETAILED CATEGORY STATISTICS
--------------------------------------------------------------------------------

Electronics:
  Total Revenue: $20,363.50
  Total Orders: 26
  Total Quantity: 65
  Average Price: $475.10
  Max Order: $3,600.00
  Min Order: $96.00

Furniture:
  Total Revenue: $6,415.00
  Total Orders: 12
  Total Quantity: 19
  Average Price: $452.92
  Max Order: $1,200.00
  Min Order: $135.00

Stationery:
  Total Revenue: $1,695.00
  Total Orders: 12
  Total Quantity: 126
  Average Price: $24.42
  Max Order: $250.00
  Min Order: $72.00

9. HIGH VALUE CUSTOMERS (>$1000)
--------------------------------------------------------------------------------
C016: $3,600.00 (1 orders)
C001: $2,400.00 (1 orders)
C025: $2,400.00 (1 orders)
C050: $1,350.00 (1 orders)
C008: $1,200.00 (1 orders)
C024: $1,200.00 (1 orders)
C031: $1,200.00 (1 orders)
C044: $1,200.00 (1 orders)

================================================================================
10. FILTERING EXAMPLES
--------------------------------------------------------------------------------
Electronics sales count: 26
January sales count: 15
Sales over $500: 17
```

## Project Structure

```
assignment2/
├── src/
│   └── sales_analysis.py    # Main analysis application
├── tests/
│   └── test_sales_analysis.py  # Test suite
├── data/
│   └── sales.csv            # Sample sales data
├── README.md
├── requirements.txt
├── run-analysis.sh
└── run-tests.sh
```

## Features

-   Total revenue calculation
-   Revenue grouping by category, region, and month
-   Top products analysis
-   Salesperson performance metrics
-   Customer segmentation
-   Filtering operations (category, date range, amount)
-   Comprehensive statistics per category

## Functional Programming Concepts

This project demonstrates:

-   **map** - Data transformation
-   **filter** - Data selection
-   **reduce** - Data aggregation
-   **lambda expressions** - Anonymous functions
-   **Higher-order functions** - Generic operations
