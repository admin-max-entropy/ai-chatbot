import dash
from dash import dcc, html
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import config
import interface.interface_callbacks

dash.register_page(__name__, order=0)

conversation = html.Div(
    id=config.APP_ID_CONVERSATION,
    style={
        "overflow-y": "auto",
        "display": "flex",
        "flex-direction": "column-reverse",
        "height": "calc(90vh - 132px)",  # Dynamically calculated height
        "width": "60%",  # Adjusts the width
        "margin": "0 auto",  # Centers the container horizontally
        "padding": "10px",  # Adds some padding to avoid content sticking to the edges
        "boxSizing": "border-box",  # Ensures padding is included in the width and height
    },
)

controls = dmc.Textarea(
    placeholder="Please ask questions related to topics in Federal Reserve speeches...",
    id=config.APP_ID_USER_INPUT,
    size="xl",
    radius="xl",
    autosize=True,
    minRows=6,
    style={
        "width": "60%",  # Adjusts the width to 80% of the parent container
        "margin": "0 auto",  # Centers the textarea on the screen
        "alignItems": "center",  # Vertical centering
        "justifyContent": "center",  # Horizontal centering,
        "fontSize": "16px",
    },
    rightSection=html.Div(
        children=[
            dmc.Button(
                size="xl",  # Small size for the button
                id=config.APP_ID_USER_SUBMIT,
                variant="subtle",
                rightSection=DashIconify(
                    icon="carbon:send-alt", width=26, color="white"
                ),
                style={
                    "position": "absolute",  # Allows precise positioning
                    "right": "10px",  # Distance from the right edge
                    "bottom": "10px",  # Distance from the bottom edge
                },
                loaderProps={"type": "dots"},
            )
        ],
    ),
)

layout = (
    html.Div(
        children=[
            dcc.Store(id=config.APP_ID_STORE_CONTENT, data=""),
            html.Div(children=[conversation], className="row"),
            html.Div(children=[controls], className="row"),
        ],
        className="row",
    ),
)
