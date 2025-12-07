"""
Unit tests for Sales Data Analysis Application

Tests the functional programming implementation including:
- Stream operations (map, filter, reduce)
- Lambda expressions
- Data aggregation and grouping
"""

import pytest
import os
import sys
from datetime import datetime
import tempfile
import csv

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sales_analysis import SalesRecord, SalesDataAnalyzer


@pytest.fixture
def sample_csv_file():
    """Create a temporary CSV file with sample sales data for testing."""
    data = [
        ['order_id', 'date', 'product', 'category', 'price', 'quantity', 'region', 'customer_id', 'salesperson'],
        ['1001', '2024-01-15', 'Laptop', 'Electronics', '1200.00', '2', 'North', 'C001', 'SP001'],
        ['1002', '2024-01-16', 'Mouse', 'Electronics', '25.50', '5', 'South', 'C002', 'SP002'],
        ['1003', '2024-01-16', 'Desk Chair', 'Furniture', '350.00', '1', 'East', 'C003', 'SP001'],
        ['1004', '2024-01-17', 'Notebook', 'Stationery', '5.00', '20', 'West', 'C004', 'SP003'],
        ['1005', '2024-02-15', 'Monitor', 'Electronics', '450.00', '2', 'North', 'C005', 'SP002'],
        ['1006', '2024-02-16', 'Desk', 'Furniture', '600.00', '1', 'South', 'C006', 'SP001'],
        ['1007', '2024-02-17', 'Pen Set', 'Stationery', '15.00', '10', 'East', 'C007', 'SP003'],
        ['1008', '2024-03-15', 'Laptop', 'Electronics', '1200.00', '1', 'West', 'C001', 'SP002'],
    ]
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
    writer = csv.writer(temp_file)
    writer.writerows(data)
    temp_file.close()
    
    yield temp_file.name
    
    # Cleanup
    os.unlink(temp_file.name)


@pytest.fixture
def analyzer(sample_csv_file):
    """Create a SalesDataAnalyzer instance with sample data."""
    return SalesDataAnalyzer(sample_csv_file)


class TestSalesRecord:
    """Test SalesRecord class functionality."""
    
    def test_sales_record_creation(self):
        """Test creating a SalesRecord from a dictionary."""
        row = {
            'order_id': '1001',
            'date': '2024-01-15',
            'product': 'Laptop',
            'category': 'Electronics',
            'price': '1200.00',
            'quantity': '2',
            'region': 'North',
            'customer_id': 'C001',
            'salesperson': 'SP001'
        }
        
        record = SalesRecord(row)
        
        assert record.order_id == '1001'
        assert record.product == 'Laptop'
        assert record.category == 'Electronics'
        assert record.price == 1200.00
        assert record.quantity == 2
        assert record.region == 'North'
        assert record.customer_id == 'C001'
        assert record.salesperson == 'SP001'
        assert record.date == datetime(2024, 1, 15)
    
    def test_total_amount_calculation(self):
        """Test total_amount property calculation."""
        row = {
            'order_id': '1001',
            'date': '2024-01-15',
            'product': 'Laptop',
            'category': 'Electronics',
            'price': '1200.00',
            'quantity': '2',
            'region': 'North',
            'customer_id': 'C001',
            'salesperson': 'SP001'
        }
        
        record = SalesRecord(row)
        assert record.total_amount == 2400.00
    
    def test_sales_record_repr(self):
        """Test string representation of SalesRecord."""
        row = {
            'order_id': '1001',
            'date': '2024-01-15',
            'product': 'Laptop',
            'category': 'Electronics',
            'price': '1200.00',
            'quantity': '2',
            'region': 'North',
            'customer_id': 'C001',
            'salesperson': 'SP001'
        }
        
        record = SalesRecord(row)
        repr_str = repr(record)
        
        assert 'SalesRecord' in repr_str
        assert 'Laptop' in repr_str
        assert '2400.00' in repr_str


class TestSalesDataAnalyzer:
    """Test SalesDataAnalyzer class functionality."""
    
    def test_analyzer_initialization(self, analyzer):
        """Test analyzer initialization and data loading."""
        assert len(analyzer.sales_data) == 8
        assert all(isinstance(record, SalesRecord) for record in analyzer.sales_data)
    
    def test_file_not_found(self):
        """Test that FileNotFoundError is raised for non-existent file."""
        with pytest.raises(FileNotFoundError):
            SalesDataAnalyzer('nonexistent_file.csv')
    
    def test_get_total_revenue(self, analyzer):
        """Test total revenue calculation using reduce."""
        # Expected: (1200*2) + (25.50*5) + (350*1) + (5*20) + (450*2) + (600*1) + (15*10) + (1200*1)
        # = 2400 + 127.50 + 350 + 100 + 900 + 600 + 150 + 1200 = 5827.50
        total_revenue = analyzer.get_total_revenue()
        assert pytest.approx(total_revenue, 0.01) == 5827.50
    
    def test_get_revenue_by_category(self, analyzer):
        """Test revenue grouping by category."""
        category_revenue = analyzer.get_revenue_by_category()
        
        assert 'Electronics' in category_revenue
        assert 'Furniture' in category_revenue
        assert 'Stationery' in category_revenue
        
        # Electronics: (1200*2) + (25.50*5) + (450*2) + (1200*1) = 2400 + 127.50 + 900 + 1200 = 4627.50
        assert pytest.approx(category_revenue['Electronics'], 0.01) == 4627.50
        
        # Furniture: (350*1) + (600*1) = 950
        assert pytest.approx(category_revenue['Furniture'], 0.01) == 950.00
        
        # Stationery: (5*20) + (15*10) = 100 + 150 = 250
        assert pytest.approx(category_revenue['Stationery'], 0.01) == 250.00
    
    def test_get_revenue_by_region(self, analyzer):
        """Test revenue grouping by region."""
        region_revenue = analyzer.get_revenue_by_region()
        
        assert len(region_revenue) == 4
        assert 'North' in region_revenue
        assert 'South' in region_revenue
        assert 'East' in region_revenue
        assert 'West' in region_revenue
    
    def test_get_top_products(self, analyzer):
        """Test top products calculation and sorting."""
        top_products = analyzer.get_top_products(3)
        
        assert len(top_products) <= 3
        assert all('product' in p for p in top_products)
        assert all('revenue' in p for p in top_products)
        assert all('quantity_sold' in p for p in top_products)
        
        # Verify sorting (descending by revenue)
        revenues = [p['revenue'] for p in top_products]
        assert revenues == sorted(revenues, reverse=True)
        
        # Laptop should be top product (appears twice)
        assert top_products[0]['product'] == 'Laptop'
        assert pytest.approx(top_products[0]['revenue'], 0.01) == 3600.00  # (1200*2) + (1200*1)
        assert top_products[0]['quantity_sold'] == 3
    
    def test_get_sales_by_month(self, analyzer):
        """Test revenue grouping by month."""
        monthly_sales = analyzer.get_sales_by_month()
        
        assert '2024-01' in monthly_sales
        assert '2024-02' in monthly_sales
        assert '2024-03' in monthly_sales
        
        # Verify sorted by month
        months = list(monthly_sales.keys())
        assert months == sorted(months)
    
    def test_get_average_order_value(self, analyzer):
        """Test average order value calculation."""
        avg_order = analyzer.get_average_order_value()
        total_revenue = analyzer.get_total_revenue()
        
        assert pytest.approx(avg_order, 0.01) == total_revenue / 8
    
    def test_get_average_order_value_empty_data(self):
        """Test average order value with empty data."""
        # Create empty CSV file
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        temp_file.write('order_id,date,product,category,price,quantity,region,customer_id,salesperson\n')
        temp_file.close()
        
        try:
            analyzer = SalesDataAnalyzer(temp_file.name)
            assert analyzer.get_average_order_value() == 0.0
        finally:
            os.unlink(temp_file.name)
    
    def test_get_sales_by_salesperson(self, analyzer):
        """Test sales metrics grouped by salesperson."""
        salesperson_stats = analyzer.get_sales_by_salesperson()
        
        assert 'SP001' in salesperson_stats
        assert 'SP002' in salesperson_stats
        assert 'SP003' in salesperson_stats
        
        for stats in salesperson_stats.values():
            assert 'total_revenue' in stats
            assert 'total_orders' in stats
            assert 'average_order_value' in stats
            assert stats['total_revenue'] >= 0
            assert stats['total_orders'] >= 0
            assert stats['average_order_value'] >= 0
    
    def test_filter_by_category(self, analyzer):
        """Test filtering by category using filter and lambda."""
        electronics = analyzer.filter_by_category('Electronics')
        
        assert len(electronics) == 4
        assert all(record.category == 'Electronics' for record in electronics)
    
    def test_filter_by_date_range(self, analyzer):
        """Test filtering by date range."""
        january_sales = analyzer.filter_by_date_range('2024-01-01', '2024-01-31')
        
        assert len(january_sales) == 4
        assert all(record.date.month == 1 for record in january_sales)
        
        february_sales = analyzer.filter_by_date_range('2024-02-01', '2024-02-28')
        assert len(february_sales) == 3
        assert all(record.date.month == 2 for record in february_sales)
    
    def test_filter_by_minimum_amount(self, analyzer):
        """Test filtering by minimum amount."""
        high_value_sales = analyzer.filter_by_minimum_amount(500.0)
        
        assert all(record.total_amount >= 500.0 for record in high_value_sales)
        assert len(high_value_sales) > 0
        
        # Test with very high threshold
        very_high_value = analyzer.filter_by_minimum_amount(2000.0)
        assert all(record.total_amount >= 2000.0 for record in very_high_value)
    
    def test_get_category_statistics(self, analyzer):
        """Test comprehensive category statistics calculation."""
        category_stats = analyzer.get_category_statistics()
        
        assert 'Electronics' in category_stats
        
        electronics_stats = category_stats['Electronics']
        assert 'total_revenue' in electronics_stats
        assert 'total_orders' in electronics_stats
        assert 'total_quantity' in electronics_stats
        assert 'average_price' in electronics_stats
        assert 'max_order' in electronics_stats
        assert 'min_order' in electronics_stats
        
        assert electronics_stats['total_orders'] == 4
        assert electronics_stats['max_order'] >= electronics_stats['min_order']
    
    def test_get_high_value_customers(self, analyzer):
        """Test high value customer identification."""
        high_value_customers = analyzer.get_high_value_customers(1000.0)
        
        assert all(customer['total_spending'] >= 1000.0 for customer in high_value_customers)
        
        for customer in high_value_customers:
            assert 'customer_id' in customer
            assert 'total_spending' in customer
            assert 'order_count' in customer
    
    def test_group_by_generic(self, analyzer):
        """Test the generic _group_by function."""
        # Group by category
        category_groups = analyzer._group_by(lambda record: record.category)
        
        assert isinstance(category_groups, dict)
        assert len(category_groups) > 0
        
        # Verify all records in each group have the same category
        for category, records in category_groups.items():
            assert all(record.category == category for record in records)
    
    def test_lambda_expressions_in_operations(self, analyzer):
        """Test that lambda expressions are used correctly in various operations."""
        # This test verifies that operations using lambda work correctly
        
        # Test map operation (implicit in data loading)
        assert len(analyzer.sales_data) > 0
        
        # Test filter operation
        filtered = list(filter(lambda r: r.price > 100, analyzer.sales_data))
        assert all(record.price > 100 for record in filtered)
        
        # Test reduce operation (used in revenue calculation)
        from functools import reduce
        total = reduce(lambda acc, record: acc + record.total_amount, analyzer.sales_data, 0.0)
        assert total > 0
    
    def test_functional_composition(self, analyzer):
        """Test composition of functional operations."""
        # Filter electronics, then calculate total revenue
        electronics = analyzer.filter_by_category('Electronics')
        from functools import reduce
        electronics_revenue = reduce(
            lambda total, record: total + record.total_amount,
            electronics,
            0.0
        )
        
        # Should match the category revenue
        category_revenue = analyzer.get_revenue_by_category()
        assert pytest.approx(electronics_revenue, 0.01) == category_revenue['Electronics']


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_filters(self, analyzer):
        """Test filters that return no results."""
        # Filter with non-existent category
        result = analyzer.filter_by_category('NonExistent')
        assert len(result) == 0
        
        # Filter with future date range
        result = analyzer.filter_by_date_range('2025-01-01', '2025-12-31')
        assert len(result) == 0
        
        # Filter with very high minimum amount
        result = analyzer.filter_by_minimum_amount(1000000.0)
        assert len(result) == 0
    
    def test_high_value_customers_no_results(self, analyzer):
        """Test high value customers with threshold higher than any customer spending."""
        high_value = analyzer.get_high_value_customers(1000000.0)
        assert len(high_value) == 0
    
    def test_top_products_more_than_available(self, analyzer):
        """Test requesting more top products than available."""
        top_products = analyzer.get_top_products(100)
        # Should return all available products without error
        assert len(top_products) <= 100


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
