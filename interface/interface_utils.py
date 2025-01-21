
import dash_mantine_components as dmc
from dash import html
import json

def textbox(text, box):

    style = {
        "max-width": "60%",
        "width": "max-content",
        "padding": "5px 10px",
        "border-radius": 25,
        "margin-bottom": 20,
    }

    if box == "user":
        style["margin-left"] = "auto"
        style["margin-right"] = 0

        return html.Div(dmc.Card(text, style=style))

    elif box == "ai":
        style["margin-left"] = 0
        style["margin-right"] = "auto"

        thumbnail = html.Div(dmc.Avatar(
            src="/assets/favicon.ico",
            style={
                "top": "5px",  # Moves the avatar lower
            }
        ), className="one columns")

        json_format = json.loads(text)["summaries"]
        lists = []
        for row in json_format:
            lists += [dmc.ListItem(dmc.Text(row["Description"], style={"fontSize": "12px"}))]
        summary = dmc.List(lists)

        textbox = html.Div(dmc.Card(summary, style=style), className="nine columns")

        return html.Div([thumbnail, textbox])

    else:
        raise ValueError("Incorrect option for `box`.")

