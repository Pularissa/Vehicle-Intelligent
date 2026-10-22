from pathlib import Path

import pandas as pd
from django.conf import settings
from django.shortcuts import render

from .dashboard import build_charts, frequency_table


def dashboard_view(request):
    data_path = Path(settings.BASE_DIR) / "dummy_data" / "vehicles_data_1000.csv"
    vehicles = pd.read_csv(data_path)
    charts = build_charts(vehicles)
    vehicles["vehicle_condition"] = (
        vehicles["vehicle_condition"].fillna("unknown").astype(str).str.title()
    )
    kilometers = pd.to_numeric(vehicles["kilometers_driven"], errors="coerce")
    summary = {
        "vehicle_count": len(vehicles),
        "manufacturer_count": vehicles["manufacturer"].nunique(),
        "active_count": int(vehicles["vehicle_condition"].eq("Active").sum()),
        "average_price": vehicles["selling_price"].mean(),
        "average_kilometers": kilometers.mean(),
        "missing_kilometer_count": int(kilometers.isna().sum()),
    }
    inventory_columns = [
        "manufacturer",
        "year",
        "body_type",
        "fuel_type",
        "vehicle_condition",
        "selling_price",
    ]
    inventory = vehicles[inventory_columns].head(10).to_dict("records")

    return render(
        request,
        "vehicles/index.html",
        {
            "frequency_table": frequency_table(vehicles),
            "charts": charts,
            "summary": summary,
            "vehicles": inventory,
        },
    )
