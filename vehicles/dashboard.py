import plotly.express as px


def frequency_table(df):
    manufacturer_counts = df["manufacturer"].value_counts().rename_axis(
        "Manufacturer"
    ).reset_index(name="Count")
    return manufacturer_counts.to_html(
        classes="table table-hover align-middle mb-0",
        index=False,
        escape=True,
        justify="center",
    )


def build_charts(df):
    manufacturer_counts = (
        df["manufacturer"].value_counts().rename_axis("Manufacturer").reset_index(name="Vehicles")
    )
    manufacturer_chart = px.bar(
        manufacturer_counts.sort_values("Vehicles"),
        x="Vehicles",
        y="Manufacturer",
        orientation="h",
        color="Vehicles",
        color_continuous_scale=["#dbeafe", "#2563eb"],
        labels={"Vehicles": "Vehicles", "Manufacturer": ""},
    )
    manufacturer_chart.update_layout(
        template="plotly_white",
        coloraxis_showscale=False,
        margin=dict(l=8, r=8, t=8, b=8),
        font=dict(family="Inter, sans-serif", color="#475569"),
        xaxis=dict(showgrid=True, gridcolor="#e9eef5", zeroline=False),
        yaxis=dict(showgrid=False),
    )

    fuel_counts = df["fuel_type"].value_counts().rename_axis("Fuel type").reset_index(name="Vehicles")
    fuel_chart = px.pie(
        fuel_counts,
        names="Fuel type",
        values="Vehicles",
        hole=0.68,
        color_discrete_sequence=["#2563eb", "#14b8a6", "#f59e0b", "#8b5cf6"],
    )
    fuel_chart.update_layout(
        template="plotly_white",
        margin=dict(l=8, r=8, t=8, b=8),
        font=dict(family="Inter, sans-serif", color="#475569"),
        legend=dict(orientation="h", y=-0.08, x=0.5, xanchor="center"),
    )

    year_counts = df.groupby("year", as_index=False).size().rename(columns={"size": "Vehicles"})
    year_chart = px.area(
        year_counts,
        x="year",
        y="Vehicles",
        markers=True,
        labels={"year": "Model year", "Vehicles": "Vehicles"},
    )
    year_chart.update_traces(
        line=dict(color="#2563eb", width=3),
        fillcolor="rgba(37, 99, 235, 0.12)",
        marker=dict(size=7, color="#2563eb"),
    )
    year_chart.update_layout(
        template="plotly_white",
        margin=dict(l=8, r=8, t=8, b=8),
        font=dict(family="Inter, sans-serif", color="#475569"),
        xaxis=dict(showgrid=False, dtick=1),
        yaxis=dict(showgrid=True, gridcolor="#e9eef5", zeroline=False),
    )

    chart_config = {"responsive": True, "displayModeBar": False}
    return {
        "manufacturer": manufacturer_chart.to_html(
            full_html=False, include_plotlyjs=False, config=chart_config
        ),
        "fuel": fuel_chart.to_html(
            full_html=False, include_plotlyjs=False, config=chart_config
        ),
        "year": year_chart.to_html(
            full_html=False, include_plotlyjs=False, config=chart_config
        ),
    }
