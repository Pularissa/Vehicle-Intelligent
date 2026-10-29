import pandas as pd
from django.test import TestCase
from django.urls import reverse

from .views import (
    frequency_table,
    high_value_cars,
    total_price_by_manufacturer,
    total_selling_price_by_manufacturer,
)


class DashboardViewTests(TestCase):
    def test_dashboard_renders_styled_tables(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vehicle Machine Learning Dashboard")
        self.assertContains(response, "Manufacturer frequency")
        self.assertContains(response, "Vehicles above 5,000")
        self.assertContains(response, "Price by manufacturer and transmission")
        self.assertContains(response, "Price by manufacturer")
        self.assertContains(response, "table-hover")
        self.assertContains(response, "Manufacturer")
        self.assertContains(response, "Count")
        self.assertContains(response, "Honda")
        self.assertContains(response, "Vehicles analyzed")

    def test_frequency_table_counts_manufacturers(self):
        df = pd.DataFrame(
            {"manufacturer": ["Honda", "Toyota", "Honda", "BMW"]}
        )

        result = frequency_table(df)

        self.assertEqual(
            result,
            [
                {"Manufacturer": "Honda", "Count": 2},
                {"Manufacturer": "Toyota", "Count": 1},
                {"Manufacturer": "BMW", "Count": 1},
            ],
        )

    def test_high_value_cars_only_includes_prices_above_5000(self):
        df = pd.DataFrame(
            {
                "manufacturer": ["Honda", "Toyota"],
                "selling_price": [5001, 5000],
            }
        )

        result = high_value_cars(df)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["manufacturer"], "Honda")
        self.assertEqual(result[0]["selling_price"], 5001)

    def test_total_price_is_grouped_by_manufacturer_and_transmission(self):
        df = pd.DataFrame(
            {
                "manufacturer": ["Honda", "Honda", "Honda", "Toyota"],
                "transmission": ["automatic", "automatic", "manual", "manual"],
                "selling_price": [6000, 7000, 8000, 9000],
            }
        )

        result = total_price_by_manufacturer(df)

        self.assertEqual(
            result,
            [
                {
                    "manufacturer": "Honda",
                    "transmission": "automatic",
                    "selling_price": 13000,
                },
                {
                    "manufacturer": "Honda",
                    "transmission": "manual",
                    "selling_price": 8000,
                },
                {
                    "manufacturer": "Toyota",
                    "transmission": "manual",
                    "selling_price": 9000,
                },
            ],
        )

    def test_total_selling_price_is_grouped_by_manufacturer_only(self):
        df = pd.DataFrame(
            {
                "manufacturer": ["Honda", "Honda", "Toyota"],
                "transmission": ["automatic", "manual", "manual"],
                "selling_price": [6000, 8000, 9000],
            }
        )

        result = total_selling_price_by_manufacturer(df)

        self.assertEqual(
            result,
            [
                {"manufacturer": "Honda", "selling_price": 14000},
                {"manufacturer": "Toyota", "selling_price": 9000},
            ],
        )
