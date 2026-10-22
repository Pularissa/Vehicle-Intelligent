from django.test import TestCase
from django.urls import reverse


class DashboardViewTests(TestCase):
    def test_dashboard_renders_summary_charts_and_vehicle_data(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vehicle management")
        self.assertContains(response, "Total vehicles")
        self.assertContains(response, "Vehicles by manufacturer")
        self.assertContains(response, "Model year distribution")
        self.assertContains(response, "plotly-4.1.1.min.js")
        self.assertContains(response, "Honda")
        self.assertContains(response, "Frequency by make")
        self.assertEqual(response.context["summary"]["vehicle_count"], 10000)
        self.assertEqual(response.context["summary"]["manufacturer_count"], 4)
        self.assertEqual(response.context["summary"]["active_count"], 4980)
        self.assertEqual(response.context["summary"]["missing_kilometer_count"], 1)
        self.assertEqual(set(response.context["charts"]), {"manufacturer", "fuel", "year"})
        self.assertIn("plotly-graph-div", response.context["charts"]["manufacturer"])
        self.assertEqual(len(response.context["vehicles"]), 10)
        self.assertNotIn("client_name", response.context["vehicles"][0])
