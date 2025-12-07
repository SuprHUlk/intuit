"""
Sales data analysis using functional programming.
"""

import csv
from functools import reduce
from typing import List, Dict, Any, Callable
from datetime import datetime
import os


class SalesRecord:
    
    def __init__(self, row: Dict[str, str]):
        self.order_id = row['order_id']
        self.date = datetime.strptime(row['date'], '%Y-%m-%d')
        self.product = row['product']
        self.category = row['category']
        self.price = float(row['price'])
        self.quantity = int(row['quantity'])
        self.region = row['region']
        self.customer_id = row['customer_id']
        self.salesperson = row['salesperson']
    
    @property
    def total_amount(self) -> float:
        return self.price * self.quantity
    
    def __repr__(self):
        return f"SalesRecord({self.order_id}, {self.product}, ${self.total_amount:.2f})"


class SalesDataAnalyzer:
    
    def __init__(self, csv_file_path: str):
        self.csv_file_path = csv_file_path
        self.sales_data: List[SalesRecord] = []
        self._load_data()
    
    def _load_data(self) -> None:
        if not os.path.exists(self.csv_file_path):
            raise FileNotFoundError(f"CSV file not found: {self.csv_file_path}")
        
        with open(self.csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            self.sales_data = list(map(lambda row: SalesRecord(row), reader))
    
    def get_total_revenue(self) -> float:
        return reduce(lambda acc, r: acc + r.total_amount, self.sales_data, 0.0)
    
    def get_revenue_by_category(self) -> Dict[str, float]:
        groups = self._group_by(lambda r: r.category)
        return {
            cat: reduce(lambda acc, r: acc + r.total_amount, records, 0.0)
            for cat, records in groups.items()
        }
    
    def get_revenue_by_region(self) -> Dict[str, float]:
        groups = self._group_by(lambda r: r.region)
        return {
            region: reduce(lambda acc, r: acc + r.total_amount, records, 0.0)
            for region, records in groups.items()
        }
    
    def get_top_products(self, n: int = 5) -> List[Dict[str, Any]]:
        groups = self._group_by(lambda r: r.product)
        
        stats = [
            {
                'product': prod,
                'revenue': reduce(lambda acc, r: acc + r.total_amount, recs, 0.0),
                'quantity_sold': reduce(lambda acc, r: acc + r.quantity, recs, 0)
            }
            for prod, recs in groups.items()
        ]
        
        return sorted(stats, key=lambda x: x['revenue'], reverse=True)[:n]
    
    def get_sales_by_month(self) -> Dict[str, float]:
        groups = self._group_by(lambda r: r.date.strftime('%Y-%m'))
        return {
            month: reduce(lambda acc, r: acc + r.total_amount, records, 0.0)
            for month, records in sorted(groups.items())
        }
    
    def get_average_order_value(self) -> float:
        if not self.sales_data:
            return 0.0
        return self.get_total_revenue() / len(self.sales_data)
    
    def get_sales_by_salesperson(self) -> Dict[str, Dict[str, Any]]:
        groups = self._group_by(lambda r: r.salesperson)
        
        result = {}
        for sp, records in groups.items():
            total = reduce(lambda acc, r: acc + r.total_amount, records, 0.0)
            result[sp] = {
                'total_revenue': total,
                'total_orders': len(records),
                'average_order_value': total / len(records) if records else 0.0
            }
        return result
    
    def filter_by_category(self, category: str) -> List[SalesRecord]:
        return list(filter(lambda r: r.category == category, self.sales_data))
    
    def filter_by_date_range(self, start_date: str, end_date: str) -> List[SalesRecord]:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        return list(filter(lambda r: start <= r.date <= end, self.sales_data))
    
    def filter_by_minimum_amount(self, min_amount: float) -> List[SalesRecord]:
        return list(filter(lambda r: r.total_amount >= min_amount, self.sales_data))
    
    def get_category_statistics(self) -> Dict[str, Dict[str, Any]]:
        groups = self._group_by(lambda r: r.category)
        
        stats = {}
        for cat, records in groups.items():
            amounts = list(map(lambda r: r.total_amount, records))
            stats[cat] = {
                'total_revenue': reduce(lambda acc, r: acc + r.total_amount, records, 0.0),
                'total_orders': len(records),
                'total_quantity': reduce(lambda acc, r: acc + r.quantity, records, 0),
                'average_price': reduce(lambda acc, r: acc + r.price, records, 0.0) / len(records) if records else 0.0,
                'max_order': max(amounts, default=0.0),
                'min_order': min(amounts, default=0.0)
            }
        return stats
    
    def get_high_value_customers(self, min_spending: float = 1000.0) -> List[Dict[str, Any]]:
        groups = self._group_by(lambda r: r.customer_id)
        
        customers = [
            {
                'customer_id': cust_id,
                'total_spending': reduce(lambda acc, r: acc + r.total_amount, records, 0.0),
                'order_count': len(records)
            }
            for cust_id, records in groups.items()
        ]
        
        return list(filter(lambda c: c['total_spending'] >= min_spending, customers))
    
    def _group_by(self, key_func: Callable[[SalesRecord], Any]) -> Dict[Any, List[SalesRecord]]:
        return reduce(
            lambda grps, rec: {**grps, key_func(rec): grps.get(key_func(rec), []) + [rec]},
            self.sales_data,
            {}
        )


def print_analysis_results(analyzer: SalesDataAnalyzer) -> None:
    print("=" * 80)
    print("SALES DATA ANALYSIS REPORT")
    print("=" * 80)
    print()
    
    print("1. TOTAL REVENUE")
    print("-" * 80)
    total = analyzer.get_total_revenue()
    print(f"Total Revenue: ${total:,.2f}")
    print()
    
    print("2. REVENUE BY CATEGORY")
    print("-" * 80)
    cat_rev = analyzer.get_revenue_by_category()
    for cat, rev in sorted(cat_rev.items(), key=lambda x: x[1], reverse=True):
        print(f"{cat:20s}: ${rev:,.2f}")
    print()
    
    print("3. REVENUE BY REGION")
    print("-" * 80)
    reg_rev = analyzer.get_revenue_by_region()
    for reg, rev in sorted(reg_rev.items(), key=lambda x: x[1], reverse=True):
        print(f"{reg:20s}: ${rev:,.2f}")
    print()
    
    print("4. TOP 5 PRODUCTS BY REVENUE")
    print("-" * 80)
    top_prods = analyzer.get_top_products(5)
    for i, p in enumerate(top_prods, 1):
        print(f"{i}. {p['product']:30s} - Revenue: ${p['revenue']:,.2f}, Quantity: {p['quantity_sold']}")
    print()
    
    print("5. REVENUE BY MONTH")
    print("-" * 80)
    monthly = analyzer.get_sales_by_month()
    for month, rev in monthly.items():
        print(f"{month}: ${rev:,.2f}")
    print()
    
    print("6. AVERAGE ORDER VALUE")
    print("-" * 80)
    avg = analyzer.get_average_order_value()
    print(f"Average Order Value: ${avg:,.2f}")
    print()
    
    print("7. PERFORMANCE BY SALESPERSON")
    print("-" * 80)
    sp_stats = analyzer.get_sales_by_salesperson()
    for sp, stats in sorted(sp_stats.items(), key=lambda x: x[1]['total_revenue'], reverse=True):
        print(f"{sp}: Revenue: ${stats['total_revenue']:,.2f}, Orders: {stats['total_orders']}, "
              f"Avg Order: ${stats['average_order_value']:,.2f}")
    print()
    
    print("8. DETAILED CATEGORY STATISTICS")
    print("-" * 80)
    cat_stats = analyzer.get_category_statistics()
    for cat, stats in sorted(cat_stats.items(), key=lambda x: x[1]['total_revenue'], reverse=True):
        print(f"\n{cat}:")
        print(f"  Total Revenue: ${stats['total_revenue']:,.2f}")
        print(f"  Total Orders: {stats['total_orders']}")
        print(f"  Total Quantity: {stats['total_quantity']}")
        print(f"  Average Price: ${stats['average_price']:,.2f}")
        print(f"  Max Order: ${stats['max_order']:,.2f}")
        print(f"  Min Order: ${stats['min_order']:,.2f}")
    print()
    
    print("9. HIGH VALUE CUSTOMERS (>$1000)")
    print("-" * 80)
    high_val = analyzer.get_high_value_customers(1000.0)
    for c in sorted(high_val, key=lambda x: x['total_spending'], reverse=True):
        print(f"{c['customer_id']}: ${c['total_spending']:,.2f} ({c['order_count']} orders)")
    print()
    
    print("=" * 80)


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(current_dir, '..', 'data', 'sales.csv')
    
    try:
        analyzer = SalesDataAnalyzer(csv_file)
        print_analysis_results(analyzer)
        
        print("10. FILTERING EXAMPLES")
        print("-" * 80)
        
        elec = analyzer.filter_by_category('Electronics')
        print(f"Electronics sales count: {len(elec)}")
        
        jan = analyzer.filter_by_date_range('2024-01-01', '2024-01-31')
        print(f"January sales count: {len(jan)}")
        
        high_sales = analyzer.filter_by_minimum_amount(500.0)
        print(f"Sales over $500: {len(high_sales)}")
        print()
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
