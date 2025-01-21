import dash
from dash import dcc, html
from dash import _dash_renderer
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import config
import interface.interface_callbacks

_dash_renderer._set_react_version("18.2.0")

app = dash.Dash(__name__)
server = app.server

conversation = html.Div(
    id = config.APP_ID_CONVERSATION,
    style={
        "overflow-y": "auto",
        "display": "flex",
        "height": "calc(90vh - 132px)",
        "flex-direction": "column-reverse",
    },
)

controls = dmc.Textarea(
                placeholder="Type something...",
                id=config.APP_ID_USER_INPUT,
                size = "xl",
                radius="xl",
                autosize=True,
                minRows=6,
                rightSection=dmc.Button(
                    size="xl",  # Small size for the button
                    id=config.APP_ID_USER_SUBMIT,
                    variant="subtle",
                    rightSection=DashIconify(icon="carbon:send-alt", width=26, color="white"),
                    style={
                        "position": "absolute",  # Allows precise positioning
                        "right": "10px",  # Distance from the right edge
                        "bottom": "10px",  # Distance from the bottom edge
                    }
                ),
            )

app.layout = dmc.MantineProvider(dmc.Container(
    fluid=False,
    children=[
        dcc.Store(id=config.APP_ID_STORE_CONTENT, data=""),
        conversation,
        controls,
    ],
),
    forceColorScheme="dark",
theme={
        "colorScheme": "dark",
    },
)

if __name__ == "__main__":
    app.run_server(debug=True, port=5000)