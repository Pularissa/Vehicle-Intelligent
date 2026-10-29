from pathlib import Path

import pandas as pd
from django.shortcuts import render


def frequency_table(df):
    manufacturer_counts = (
        df["manufacturer"]
        .value_counts()
        .rename_axis("Manufacturer")
        .reset_index(name="Count")
    )
    return manufacturer_counts.to_dict(orient="records")


def high_value_cars(df):
    return df[df["selling_price"] > 5000].to_dict(orient="records")


def total_price_by_manufacturer(df):
    totals = (
        df.groupby(["manufacturer", "transmission"])[["selling_price"]]
        .sum()
        .reset_index()
    )
    return totals.to_dict(orient="records")


def total_selling_price_by_manufacturer(df):
    totals = df.groupby("manufacturer")[["selling_price"]].sum().reset_index()
    return totals.to_dict(orient="records")


def dashboard_view(request):
    data_path = Path(__file__).resolve().parent.parent / "dummy_data" / "vehicles_data_1000.csv"
    df = pd.read_csv(data_path)

    frequency_rows = frequency_table(df)
    high_value_rows = high_value_cars(df)
    transmission_rows = total_price_by_manufacturer(df)
    manufacturer_rows = total_selling_price_by_manufacturer(df)

    tables = [
        {
            "id": "frequency-table",
            "title": "Manufacturer frequency",
            "description": "Vehicle count for each manufacturer.",
            "columns": ["Manufacturer", "Count"],
            "rows": frequency_rows,
        },
        {
            "id": "high-value-cars",
            "title": "Vehicles above 5,000",
            "description": "Vehicles with a selling price greater than 5,000.",
            "columns": list(df.columns),
            "rows": high_value_rows,
        },
        {
            "id": "price-by-manufacturer",
            "title": "Price by manufacturer and transmission",
            "description": "Combined selling price grouped by manufacturer and transmission.",
            "columns": list(transmission_rows[0].keys()) if transmission_rows else [],
            "rows": transmission_rows,
        },
        {
            "id": "total-price-by-manufacturer",
            "title": "Price by manufacturer",
            "description": "Combined selling price for each manufacturer.",
            "columns": list(manufacturer_rows[0].keys()) if manufacturer_rows else [],
            "rows": manufacturer_rows,
        },
    ]

    return render(
        request,
        "vehicles/index.html",
        {"tables": tables, "vehicle_count": len(df)},
    )
