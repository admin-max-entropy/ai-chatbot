
import dash_mantine_components as dmc
from dash import html

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

        return dmc.Card(text, style=style)

    elif box == "AI":
        style["margin-left"] = 0
        style["margin-right"] = "auto"

        thumbnail = html.Div(dmc.Avatar(
            src="/assets/favicon.ico",
            style={
                #"position": "absolute",
                "top": "5px",  # Moves the avatar lower
                #"transform": "translateX(-50%)"  # Adjusts for the avatar's width
            }
        ), className="one columns")

        textbox = html.Div(dmc.Card(text, style=style), className="nine columns")

        return html.Div([thumbnail, textbox])

    else:
        raise ValueError("Incorrect option for `box`.")

