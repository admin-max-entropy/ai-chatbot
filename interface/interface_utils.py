
import dash_mantine_components as dmc
from dash import html
import json
from dash_iconify import DashIconify

def textbox(text, box):

    style = {
        "max-width": "100%",
        "width": "max-content",
        "border-radius": 25,
        "margin-bottom": 20,
        'fontSize': '16px',
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
            sources = row["Source"]
            sources = sources.split(";")
            text_component = [f"{row['Description']}\n\n"]
            for source in sources:
                text_component += [dmc.Anchor(href=source, target="_blank",
                                              children=[
                                                  DashIconify(icon="noto:link"),  # Iconify icon
                                              ],
                                              )]

            text_component += [dmc.Button(row.get("Date", ""), variant="light", color="blue.3", radius="lg",
                                          style={"fontSize": "12px"})]
            lists += [dmc.ListItem(dmc.Text(text_component, style={"fontSize": "16px"}))]

        summary = dmc.List(lists)

        ai_style = style.copy()
        ai_style["backgroundColor"] = "#0d0d0d"
        textbox = html.Div(dmc.Card(summary, style=ai_style), className="eleven half columns")

        return html.Div([thumbnail, textbox])

    else:
        raise ValueError("Incorrect option for `box`.")

