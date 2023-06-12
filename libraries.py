import pandas as pd
import numpy as np
import plotly.express as px
import geopandas as gd
import plotly.graph_objects as go


vietnam = gd.read_file("vietnamHigh.json")

vietnam["name"] = vietnam["name"].replace(
    {
        "Bà Rịa–Vũng Tàu": "Bà Rịa - Vũng Tàu",
        "Hòa Bình": "Hoà Bình",
        "Khánh Hòa": "Khánh Hoà",
        "Hồ Chí Minh": "TP. Hồ Chí Minh",
        "Thanh Hóa": "Thanh Hoá",
        "Thừa Thiên–Huế": "Thừa Thiên - Huế",
    }
)

vietnam = vietnam.rename(columns={"name": "new_places"})


def check_positions(df, tech_list, op_list, package_list):
    for tech in tech_list:
        df["{}".format(tech)] = df["description"].apply(
            lambda x: 1 if tech.upper() in x.upper() else 0
        )
    for op in op_list:
        df["{}".format(op)] = df["description"].apply(
            lambda x: 1 if op.upper() in x.upper() else 0
        )
    for pack in package_list:
        df["{}".format(pack)] = df["description"].apply(
            lambda x: 1 if pack.upper() in x.upper() else 0
        )
    return df


# Create dict for each category
tech = {}
operation = {}
package = {}


def create_dict(df):
    for item in df.columns[7:21]:
        tech["{}".format(item.strip())] = df["{}".format(item)].sum()
    for item in df.columns[22:38]:
        operation["{}".format(item.strip())] = df["{}".format(item)].sum()
    for item in df.columns[38:]:
        package["{}".format(item.strip())] = df["{}".format(item)].sum()
    return tech, operation, package


# Create chart from predefined dict


def create_chart_from_dict(dict_object, df):
    new_df = pd.DataFrame.from_dict([dict_object])
    new_df = new_df.transpose().reset_index()
    new_df = new_df.rename(columns={"index": "item", 0: "positions"})
    new_df["percentage"] = round(
        new_df["positions"] / sum(new_df["positions"]) * 100, 2
    )
    new_df = new_df[new_df["percentage"] > 0].sort_values(
        by="percentage", ascending=False
    )
    if dict_object == tech:
        title = "Technology"
    elif dict_object == operation:
        title = "Operation"
    elif dict_object == package:
        title = "Package"
    fig = px.bar(
        new_df,
        x="item",
        y="percentage",
        color="item",
        color_discrete_sequence=px.colors.sequential.Viridis,
        template="plotly_white",
        title="<b>{}</b> proportion across {} roles".format(title, df.shape[0]),
    )

    fig.update_xaxes(showgrid=False, tickangle=45)
    fig.update_yaxes(showgrid=False)
    fig.update_layout(
        {
            "plot_bgcolor": "rgba(0,0,0,0)",
            "showlegend": False,
            "xaxis": {"title": None},
            "yaxis": {
                "title": None,
            },
            "hovermode": "x unified",
            "font_family": "Inter",
            "autosize": True,
            "width": 400,
            "height": 250,
        }
    )
    fig.update_layout(margin=dict(l=35, r=50, t=50, b=0))
    fig.update_traces(hovertemplate="%{y}%")
    return fig
    # fig.show()


# Create donut chart


def create_donut(df, edu_level):
    for level in edu_level:
        df["{}".format(level)] = df["description"].apply(
            lambda x: 1 if level.upper() in x.upper() else 0
        )
    labels = ["Bachelors", "PhD", "Masters"]
    values = [df.bachelor.sum(), df.phd.sum(), df.master.sum() + df.msc.sum()]
    fig = px.pie(
        names=labels,
        values=values,
        hole=0.6,
        color_discrete_sequence=px.colors.sequential.Viridis,
        title="<b>Proportion of saught</b> after level of education",
    )
    fig.update_layout(
        {
            "font_family": "Inter",
            "legend": {
                "orientation": "h",
                "yanchor": "top",
                "xanchor": "center",
                "y": -0.1,
                "x": 0.5,
            },
            "autosize": True,
            "width": 400,
            "height": 250,
        }
    )
    fig.update_layout(margin=dict(l=60, r=60, t=50, b=40))
    fig.update_traces(hovertemplate="%{label}: %{percent}", textinfo="none")
    return fig


# Create map data


def create_map_data(df):
    new_places = []
    for place in df.place:
        if "Ho Chi Minh" in place:
            new_places.append("TP. Hồ Chí Minh")
        elif "Da Nang" in place:
            new_places.append("Đà Nẵng")
        elif "Ha Noi" in place:
            new_places.append("Hà Nội")
        else:
            new_places.append("Hà Nội")
    df["new_places"] = new_places
    df = df[df["title"] == query]
    proportion = pd.DataFrame(df.new_places.value_counts(normalize=True)).reset_index()
    map_df = vietnam.merge(proportion, how="left", on="new_places")
    map_df = map_df[["id", "new_places", "geometry", "proportion"]]
    map_df = map_df.to_crs(
        epsg=4326
    )  # convert the coordinate reference system to lat/long
    return map_df


###


def create_map(map_df):
    mapbox_token = "pk.eyJ1Ijoic3N1cGVybWFuMTgwOSIsImEiOiJjbDJqN3JyNHowdThrM2pwOTJuc3NkZmRoIn0.7iP6JPt9HuUxQnt2mgLmfw"

    zmin = map_df["proportion"].min()
    zmax = map_df["proportion"].max()

    lga_json = map_df.__geo_interface__  # covert to geoJSON

    data = go.Choroplethmapbox(
        geojson=lga_json,
        locations=map_df.index,
        z=map_df["proportion"],
        text=map_df["new_places"],
        colorbar=dict(thickness=20, ticklen=1, tickformat=".0%", outlinewidth=0),
        marker_line_width=1,
        marker_opacity=0.7,
        colorscale="Viridis",
        zmin=zmin,
        zmax=zmax,
        hovertemplate="<b>%{text}</b><br>" + "%{z:.0%}<br>" + "<extra></extra>",
    )

    layout = go.Layout(
        title={
            "text": f"<b>Spread of positions</b> across <b>Vietnam</b>",
            "xanchor": "left",
        },
        mapbox1=dict(
            domain={"x": [0, 1], "y": [0, 1]},
            center=dict(lat=21.3599, lon=105.7841),
            accesstoken=mapbox_token,
            zoom=5,
        ),
        font=dict(family="Inter"),
        autosize=True,
        height=250,
        width=380,
        margin=dict(l=20, r=20, t=50, b=0),
    )

    # Generate the map
    fig = go.Figure(data=data, layout=layout)
    return fig
