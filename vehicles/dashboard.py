import plotly.express as px
import plotly.offline as opy
import plotly.graph_objects as go
import pandas as pd


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
