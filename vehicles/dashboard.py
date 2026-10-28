def frequency_table(df):
    manufacturer_counts = (
        df["manufacturer"].value_counts().reset_index()
    )
    manufacturer_counts.columns = ["Manufacturer", "Count"]
    table_html = manufacturer_counts.to_html(
        classes="table table-bordered table-striped table-sm",
        index=False,
        float_format="%.2f",
        justify="center",
    )
    return table_html


def high_value_cars(df):
    return df[df["selling_price"] > 5000].to_html(
        classes="table table-bordered table-striped table-sm",
        index=False,
    )


def total_price_by_manufacturer(df):
    totals = df.groupby(["manufacturer", "transmission"])[["selling_price"]].sum()
    return totals.to_html(
        classes="table table-bordered table-striped table-sm",
        float_format="%.2f",
    )


def total_selling_price_by_manufacturer(df):
    totals = df.groupby("manufacturer")[["selling_price"]].sum()
    return totals.to_html(
        classes="table table-bordered table-striped table-sm",
        float_format="%.2f",
    )
