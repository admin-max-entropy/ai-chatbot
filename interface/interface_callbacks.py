"""callback functions"""
from dash import html, dcc, Output, callback, Input, State, ctx, callback_context
import config
import interface.interface_utils

@callback(
    Output(config.APP_ID_CONVERSATION, "children"),
    [Input(config.APP_ID_STORE_CONTENT, "data")]
)
def update_display(chat_history):
    if chat_history is None:
        chat_history = ""
    return [
        interface.interface_utils.textbox(x, box="user") if i % 2 == 1 else
        interface.interface_utils.textbox(x, box="AI")
        for i, x in enumerate(chat_history.split("<split>")[:-1])
    ]


@callback(
    Output(config.APP_ID_USER_INPUT, "value"),
    [Input(config.APP_ID_USER_SUBMIT, "n_clicks"),
     Input(config.APP_ID_USER_INPUT, "n_submit")],
)
def clear_input(n_clicks, n_submit):
    return ""


@callback(
    Output(config.APP_ID_STORE_CONTENT, "data"),
    [Input(config.APP_ID_USER_SUBMIT, "n_clicks"),
     Input(config.APP_ID_USER_INPUT, "n_submit")],
    [State(config.APP_ID_USER_INPUT, "value"),
     State(config.APP_ID_STORE_CONTENT, "data")],
)
def run_chatbot(n_clicks, n_submit, user_input, chat_history):
    if n_clicks == 0 and n_submit is None:
        return None

    if user_input is None or user_input == "":
        return chat_history

    chat_history += f"{user_input}<split>"
    model_output = "hello" #response.choices[0].text.strip()

    chat_history += f"{model_output}<split>"

    return chat_history

