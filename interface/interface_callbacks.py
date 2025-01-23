"""callback functions"""

from dash import (
    Output,
    callback,
    Input,
    State,
)
import config
import interface.interface_utils
import ai_utils
import json


@callback(
    Output(config.APP_ID_CONVERSATION, "children"),
    [
        Input(config.APP_ID_STORE_CONTENT, "data"),
    ],
)
def update_display(chat_history):

    if chat_history is None:
        chat_history = ""

    charts = reversed(chat_history.split("<split>")[:-1])

    responses = []
    for chat in charts:
        if chat.endswith("<user>"):
            rp = interface.interface_utils.textbox(
                chat.replace("<user>", ""), box="user"
            )
        elif chat.endswith("<ai>"):
            rp = interface.interface_utils.textbox(chat.replace("<ai>", ""), box="ai")
        else:
            raise RuntimeError("unknown chat type")
        responses.append(rp)
    return responses


@callback(
    Output(config.APP_ID_USER_INPUT, "value"),
    [
        Input(config.APP_ID_USER_SUBMIT, "n_clicks"),
        Input(config.APP_ID_USER_INPUT, "n_submit"),
    ],
)
def clear_input(n_clicks, n_submit):
    return ""


@callback(
    Output(config.APP_ID_STORE_CONTENT, "data"),
    [
        Input(config.APP_ID_USER_SUBMIT, "n_clicks"),
        Input(config.APP_ID_USER_INPUT, "n_submit"),
    ],
    [
        State(config.APP_ID_USER_INPUT, "value"),
        State(config.APP_ID_STORE_CONTENT, "data"),
    ],
    running=[(Output(config.APP_ID_USER_SUBMIT, "loading"), True, False)],
    prevent_initial_call=True,
)
def run_chatbot(n_clicks, n_submit, user_input, chat_history):

    if n_clicks == 0 and n_submit is None:
        return None

    if user_input is None or user_input == "":
        return chat_history

    chat_history += f"{user_input}<user><split>"

    prompt_input = user_input
    results = ai_utils.similarity_search_with_relevance_scores_pinecone(
        prompt_input, top_k=30
    )

    if len(results) == 0 or results[0][1] < 0.85:
        model_output = json.dumps(
            {
                "summaries": [
                    {"Description": config.DEFAULT_REPLY, "Source": "", "Date": ""}
                ]
            }
        )
    else:
        selected_text = ""
        for i, (doc, ratio) in enumerate(results, 1):
            print(doc)
            selected_text += (
                f"{i}. Author: {doc['author']}\n"
                f"   Publication Date: {doc['date']}\n"
                f"   Content Preview: {doc['text']}...\n\n"
                f"   URL in: {doc['link']}...\n\n"
            )
            selected_text += prompt_input

        model_output = ai_utils.summarize_speech(selected_text)

    chat_history += f"{model_output}<ai><split>"

    return chat_history
