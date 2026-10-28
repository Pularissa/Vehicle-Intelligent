import pandas as pd
from django.test import TestCase
from django.urls import reverse

from .dashboard import (
    frequency_table,
    high_value_cars,
    total_price_by_manufacturer,
    total_selling_price_by_manufacturer,
)


class DashboardViewTests(TestCase):
    def test_dashboard_renders_manufacturer_frequency_table(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vehicle Machine Learning Dashboard")
        self.assertContains(response, "Frequency Tables (One-way)")
        self.assertContains(response, "Vehicles with selling price above 5,000")
        self.assertContains(response, "Total selling price by manufacturer and transmission")
        self.assertContains(response, "Total selling price by manufacturer")
        self.assertContains(response, "table-bordered")
        self.assertContains(response, "Manufacturer")
        self.assertContains(response, "Count")
        self.assertContains(response, "Honda")

    def test_frequency_table_counts_manufacturers(self):
        df = pd.DataFrame(
            {"manufacturer": ["Honda", "Toyota", "Honda", "BMW"]}
        )

        table_html = frequency_table(df)

        self.assertIn("table table-bordered table-striped table-sm", table_html)
        self.assertIn("<th>Manufacturer</th>", table_html)
        self.assertIn("<th>Count</th>", table_html)
        self.assertNotIn("<th></th>", table_html)
        self.assertIn("Honda", table_html)
        self.assertIn(">2<", table_html)

    def test_high_value_cars_only_includes_prices_above_5000(self):
        df = pd.DataFrame(
            {
                "manufacturer": ["Honda", "Toyota"],
                "selling_price": [5001, 5000],
            }
        )

        table_html = high_value_cars(df)

        self.assertIn("Honda", table_html)
        self.assertNotIn("Toyota", table_html)
        self.assertNotIn("<th></th>", table_html)

    def test_total_price_is_grouped_by_manufacturer_and_transmission(self):
        df = pd.DataFrame(
            {
                "manufacturer": ["Honda", "Honda", "Honda", "Toyota"],
                "transmission": ["automatic", "automatic", "manual", "manual"],
                "selling_price": [6000, 7000, 8000, 9000],
            }
        )

        table_html = total_price_by_manufacturer(df)

        self.assertIn("automatic", table_html)
        self.assertIn("manual", table_html)
        self.assertIn("13000", table_html)
        self.assertIn("8000", table_html)
        self.assertIn("9000", table_html)

    def test_total_selling_price_is_grouped_by_manufacturer_only(self):
        df = pd.DataFrame(
            {
                "manufacturer": ["Honda", "Honda", "Toyota"],
                "transmission": ["automatic", "manual", "manual"],
                "selling_price": [6000, 8000, 9000],
            }
        )

        table_html = total_selling_price_by_manufacturer(df)

        self.assertIn("Honda", table_html)
        self.assertIn("Toyota", table_html)
        self.assertIn("14000", table_html)
        self.assertIn("9000", table_html)
        self.assertNotIn("automatic", table_html)
        self.assertNotIn("manual", table_html)
