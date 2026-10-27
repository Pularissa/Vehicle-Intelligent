import pandas as pd
from django.test import TestCase
from django.urls import reverse

from .dashboard import frequency_table


class DashboardViewTests(TestCase):
    def test_dashboard_renders_manufacturer_frequency_table(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vehicle Machine Learning Dashboard")
        self.assertContains(response, "Frequency Tables (One-way)")
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
