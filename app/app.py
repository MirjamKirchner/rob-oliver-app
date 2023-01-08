# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.io as pio
from datetime import datetime
from dash import Dash, html, dcc, Input, Output
from datetime import date
from create_app_assets import (
    create_part_to_whole,
    create_time_series,
    create_bubbles,
    DF_ROB,
)

# Theme for plotly plots
pio.templates.default = "simple_white"

# App
app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "/static/seehundstation_friedrichskoog.css",
    ],
)

app.layout = html.Div(
    [
        html.A(
            href="https://unsplash.com/@hen63",
            children=[
                html.Img(
                    src="/static/img/Seehundheader2.png",
                    alt="A cute baby seal",
                    style={"width": "100%"},
                )
            ],
        ),
        html.Div(
            [
                html.Small(
                    children=[
                        "Daten werden bereitgestellt durch die ",
                        html.A(
                            href="https://www.seehundstation-friedrichskoog.de/",
                            children="Seehundstation Friedrichskoog ",
                            style={"color": "#004d9e"},
                        ),
                        "(zuletzt aktualisiert am {}).".format(
                            DF_ROB["Sys_aktualisiert_am"].max().strftime("%d.%m.%Y")
                        ),
                    ]
                )
            ],
            style={"background-color": "#e9e2d8"},
        ),
        html.Div(html.P("")),
        html.Div(
            [
                dbc.Container(
                    dbc.Card(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        html.Div(
                                                            dcc.Graph(
                                                                id="fig-part-to-whole"
                                                            ),
                                                            style={
                                                                "width": "100%",
                                                                "height": "400px",
                                                            },
                                                        ),
                                                        width=3,
                                                    ),
                                                    dbc.Col(
                                                        html.Div(
                                                            [
                                                                html.P(
                                                                    [
                                                                        "Willkommen Robben-Freund!",
                                                                        html.Br(),
                                                                        "Hier kannst du Informationen zu den Robbenfunden der ",
                                                                        html.A(
                                                                            href="https://www.seehundstation-friedrichskoog.de/",
                                                                            children="Seehundstation Friedrichskoog ",
                                                                            style={
                                                                                "color": "#004d9e"
                                                                            },
                                                                        ),
                                                                        "untersuchen.",
                                                                    ]
                                                                ),
                                                                html.P(
                                                                    [
                                                                        "Im Diagramm links siehst du den Anteil der",
                                                                        html.A(
                                                                            children=" in Reha befindlichen",
                                                                            style={
                                                                                "color": "#94613d"
                                                                            },
                                                                        ),
                                                                        ", ",
                                                                        html.A(
                                                                            children="ausgewilderten",
                                                                            style={
                                                                                "color": "#3d8c18"
                                                                            },
                                                                        ),
                                                                        " und ",
                                                                        html.A(
                                                                            children="verstorbenen",
                                                                            style={
                                                                                "color": "#101a1c"
                                                                            },
                                                                        ),
                                                                        " Robben  im Zeitraum: ",
                                                                        html.A(
                                                                            dcc.DatePickerRange(
                                                                                id="date-picker",
                                                                                start_date_placeholder_text="Start Period",
                                                                                end_date_placeholder_text="End Period",
                                                                                calendar_orientation="vertical",
                                                                                start_date=pd.Timestamp(
                                                                                    DF_ROB[
                                                                                        "Einlieferungsdatum"
                                                                                    ].min()
                                                                                    - pd.Timedelta(
                                                                                        days=14
                                                                                    )
                                                                                ).date(),
                                                                                end_date=pd.Timestamp(
                                                                                    DF_ROB[
                                                                                        "Erstellt_am"
                                                                                    ].max()
                                                                                    + pd.Timedelta(
                                                                                        days=14
                                                                                    )
                                                                                ).date(),
                                                                                display_format="D.M.Y",
                                                                            )
                                                                        ),
                                                                        html.Br(),
                                                                        "Unter diesem Text siehst du eine Karte, in der die ungefähren Fundorte der eingelieferten Robben "
                                                                        "eingetragen sind.",
                                                                        html.Br(),
                                                                        "Im letzten Bild kannst du dir ansehen, wann wie viele Robben in die Station eingeliefert worden sind.",
                                                                    ]
                                                                ),
                                                                html.P(
                                                                    [
                                                                        "Wenn du ein bestimmtes Zeitfenster genauer betrachten möchtest,"
                                                                        " musst du nur die obigen Daten anpassen, um den Start- bzw. den Endzeitpunkt zu verändern.",
                                                                        html.Br(),
                                                                        "Probier es doch mal aus 😄 Viel Spaß! ",
                                                                        html.A(
                                                                            href="https://www.mirjam-kirchner.com/",
                                                                            children="🐼💚",
                                                                        ),
                                                                    ]
                                                                ),
                                                                html.P(
                                                                    [
                                                                        html.A(
                                                                            children="Das kannst du tun:",
                                                                            style={
                                                                                "color": "#0d6efd"
                                                                            },
                                                                        ),
                                                                        html.Br(),
                                                                        dbc.Button(
                                                                            "Robben helfen!",
                                                                            href="https://www.seehundstation-friedrichskoog.de/spenden/",
                                                                        ),
                                                                        " ",
                                                                        dbc.Button(
                                                                            "Source Code ansehen!",
                                                                            href="https://github.com/MirjamKirchner/rob-oliver",
                                                                        ),
                                                                    ]
                                                                ),
                                                            ]
                                                        )
                                                    ),
                                                ]
                                            )
                                        ]
                                    ),
                                    html.Div(dcc.Graph(id="fig-bubbles")),
                                    html.Div(dcc.Graph(id="fig-time-series")),
                                ]
                            )
                        ],
                        color="#e9e2d8",
                        style={"border-radius": "10px"},
                    )
                )
            ]
        ),
        html.Div(html.P("")),
    ]
)


@app.callback(
    Output("fig-part-to-whole", "figure"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date"),
)
def update_fig_part_to_whole(start_date: str, end_date: str) -> go.Figure:
    """
    Updates the donut chart displaying the fraction of animals in rehabilitation, released, and dead based on the
    selected date range.

    Parameters
    ----------
    start_date
        Start date of the considered time period.

    end_date
        End date of the considered time period.

    Returns
    -------
        A `plotly.graph_objects`-figure describing a donut chart.
    """
    min_date = pd.to_datetime(start_date, format="%Y-%m-%d")
    max_date = pd.to_datetime(end_date, format="%Y-%m-%d")
    ds_part_to_whole = create_part_to_whole(min_date=min_date, max_date=max_date)

    fig_part_to_whole = go.Figure(
        data=[
            go.Pie(
                labels=ds_part_to_whole.index,
                values=ds_part_to_whole.values,
                hole=0.4,
                marker_colors=["#3d8c18", "#101a1c", "#94613d"],
            )
        ]
    )
    fig_part_to_whole.update_layout(
        showlegend=False,
        annotations=[
            dict(
                text="keine Daten<br>verfügbar"
                if ds_part_to_whole.sum() == 0
                else str(ds_part_to_whole.sum()) + "<br>total",
                x=0.5,
                y=0.5,
                xref="paper",
                yref="paper",
                ax=0,
                ay=0,
                font_size=22,
                showarrow=False,
            )
        ],
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
    )

    return fig_part_to_whole


@app.callback(
    Output("fig-bubbles", "figure"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date"),
)
def update_fig_bubbles(start_date: str, end_date: str) -> go.Figure:
    """
    Updates the bubble chart displaying the count of seals at different finding places and the location of the
    Seehundstation Friedrichskoog based on the selected date range.

    Parameters
    ----------
    start_date
        Start date of the considered time period.

    end_date
        End date of the considered time period.

    Returns
    -------
    A `plotly.graph_objects`-figure describing a bubble chart.
    """
    min_date = pd.to_datetime(start_date, format="%Y-%m-%d")
    max_date = pd.to_datetime(end_date, format="%Y-%m-%d")
    df_bubbles = create_bubbles(max_date=max_date, min_date=min_date)

    fig_bubbles = go.Figure()
    # finding places
    fig_bubbles.add_trace(
        go.Scattermapbox(
            lat=df_bubbles["Lat"],
            lon=df_bubbles["Long"],
            mode="markers",
            marker=go.scattermapbox.Marker(
                color="#FF7F3F",
                size=df_bubbles["Anzahl"],
                sizeref=df_bubbles["Anzahl"].max() / (17**2),
                sizemin=3,
                sizemode="area",
            ),
            text=(
                pd.Series(["Fundort"] * df_bubbles["Fundort"].size).str.cat(
                    df_bubbles["Fundort"].astype(str), sep="="
                )
            ).str.cat(
                pd.Series(["Anzahl"] * df_bubbles["Anzahl"].size).str.cat(
                    df_bubbles["Anzahl"].astype(str), sep="="
                ),
                sep="<br>",
            ),
            hoverinfo="text",
            name="Fundort",
        )
    )
    # Seehundstation Friedrichskoog
    fig_bubbles.add_trace(
        go.Scattermapbox(
            lat=[54.00089266779337],
            lon=[8.876683012541077],
            mode="markers+text",
            marker=go.scattermapbox.Marker(color="#004d9e", size=15),
            text="Seehundstation Friedrichskoog",
            hoverinfo="text",
            name="Seehundstation",
        )
    )
    # Layout
    fig_bubbles.update_layout(
        mapbox=dict(
            style="stamen-terrain",  # "open-street-map", "carto-positron", "carto-darkmatter", "stamen-terrain", "stamen-toner" or "stamen-watercolor"
            zoom=6.5,
            center=dict(lat=54.43388, lon=9.57109),
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            itemsizing="constant",
        ),
    )
    return fig_bubbles


@app.callback(
    Output("fig-time-series", "figure"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date"),
)
def update_fig_time_series(start_date: str, end_date: str) -> px.line:
    """
    Updates the time-series chart displaying the count of animals admitted to the Seehundstation Friedrichskoog based on
    the selected date range.

    Parameters
    ----------
    start_date
        Start date of the considered time period.

    end_date
        End date of the considered time period.

    Returns
    -------
    A `plotly.express.line`-figure describing a a time-series chart.
    """
    min_date = pd.to_datetime(start_date, format="%Y-%m-%d")
    max_date = pd.to_datetime(end_date, format="%Y-%m-%d")
    df_time_series_range = create_time_series(max_date=max_date, min_date=min_date)
    color_discrete_map = {
        "Seehund": "#086E7D",
        "Kegelrobbe": "#34BE82",
        "sonstige": "#DC434A",
    }
    fig_time_series = px.line(
        df_time_series_range,
        x="Einlieferungswoche",
        y="Anzahl",
        color="Tierart",
        markers=True,
        color_discrete_map=color_discrete_map,
    )
    fig_time_series.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
    )
    return fig_time_series


if __name__ == "__main__":
    app.run_server(debug=True)
