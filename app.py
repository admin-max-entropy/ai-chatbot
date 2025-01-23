"""app.py"""
from dash import Dash, page_registry, page_container
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import html
import collections
from dash import _dash_renderer


_dash_renderer._set_react_version("18.2.0")


app = Dash(__name__, title="Max Entropy AI Tools", update_title="Updating...", use_pages=True)
server = app.server

def get_icon(name):
    icon_map = {"home": "wpf:ask-question"}
    return DashIconify(icon=icon_map["home"], height=16)

def __create_page_structure():
    result = {}
    for page in list(page_registry.values()):
        path = page["path"]
        sub_path = path.split("/")
        assert(len(sub_path) in [2, 3, 4])

        root = sub_path[1]
        if len(sub_path) == 2:
            result[root] = []
        elif len(sub_path) == 3:
            if root not in result:
                result[root] = []
            result[root] += [page]
        else:
            subroot = sub_path[2]
            if root not in result:
                result[root] = {}
            if subroot not in result[root]:
                result[root][subroot] = []
            result[root][subroot] += [page]
    return result

def __get_label(name):
    name = name.replace("-", " ").title()
    name = name.replace("On", "O/N").replace("Api", "API")
    return name

def get_icon_(icon):
    return DashIconify(icon=icon, height=16)

def create_sidebar():

    page_structure = __create_page_structure()
    children_by_order = {}

    for page in list(page_registry.values()):

        path = page["path"]
        sub_path = path.split("/")
        root = sub_path[1]
        data = page_structure[root]
        order = page["order"]

        if len(data) > 0:

            if isinstance(data, list):
                page_children = []
                for sub_page in data:
                    page_children += [dmc.NavLink(
                        label=sub_page["name"].title(),
                        href=sub_page["path"],
                        leftSection=get_icon(sub_page["name"]),
                        rightSection=get_icon_(icon="tabler-chevron-right"),
                    )]

                component = html.Div(
                    dmc.NavLink(
                    label=__get_label(root),
                    leftSection=get_icon(root.replace("-", " ")),
                        rightSection=get_icon_(icon="tabler-chevron-right"),

                        children=page_children,
                    opened=True)
                )

                children_by_order[order] = component

            else:

                sub_components = []
                for data_key in data:
                    sub_data = data[data_key]
                    page_children_ = []
                    for sub_page_ in sub_data:
                        page_children_ += [dmc.NavLink(
                            label=__get_label(sub_page_["name"]),
                            href=sub_page_["path"],
                            rightSection=get_icon_(icon="tabler-chevron-right"),
                            leftSection=get_icon(sub_page_["name"]))]
                    sub_components += [html.Div(
                        dmc.NavLink(
                            label=__get_label(sub_path[2]),
                            rightSection=get_icon_(icon="tabler-chevron-right"),
                            leftSection=get_icon(sub_path[2].replace("-", " ")),
                            children=page_children_,
                            opened=True,
                        ))]
                component = html.Div(
                    dmc.NavLink(
                        label=__get_label(root),
                        rightSection=get_icon_(icon="tabler-chevron-right"),
                        leftSection=get_icon(root.replace("-", " ")),
                        children=sub_components,
                        opened=True,
                    ))
                children_by_order[order] = component

        elif len(data) == 0:
            component = html.Div(dmc.NavLink(
                label=__get_label(page["name"]),
                href=path,
                rightSection=get_icon_(icon="tabler-chevron-right"),
                leftSection=get_icon(page["name"]),
                ), className="row")
            children_by_order[order] = component
        else:
            raise RuntimeError("unsupported page type")

    children_by_order = collections.OrderedDict(sorted(children_by_order.items()))
    children = list(children_by_order.values())

    return html.Div(children=children, className="twelve columns")


app.layout = dmc.MantineProvider(
    forceColorScheme="dark",
    theme={
        "colorScheme": "dark",
        "fontSize": "16px",
        "fontSizes": {
            "sm": "16px",
            "xl": "16px",
        },
        "components": {
            "Textarea": {
                "styles": {
                    "input": {
                        "backgroundColor": "#2a2a2e",  # Dark gray background
                        "color": "#E5E7EB",  # Light gray text color
                        "border": "none",  # Remove border
                        "padding": "10px",  # Add padding inside textarea
                    }
                }
            }
        }
    },
    children=[
    html.Div(
        children=[
            html.Div(
                children=[
                    create_sidebar()
                ], className="two columns", style={"paddingLeft": "30px", "paddingRight": "10px",
                                                   "background-color": "#202123",   "height": "100vh"},),

            html.Div(
                children= [html.Div(dmc.Affix(
    dmc.Group(children=[DashIconify(icon="mdi-light:email", width=25,
                                    color="#90d5ff"), dmc.TextInput("admin@max-entropy.com",
                                                                    styles={"input": {"color": "#90d5ff",
                                                                                      "fontSize": "16px"}},
                                                                    variant="transit",
                                                                    style={"width": "200px"}
                                                                    )]),
                    position={"top": 0, "right": 10}),
                    className="eleven columns", style={"paddingLeft": "0px", "paddingRight": "10px"}
)]+[
                    page_container
                ], className="eleven columns", style={"paddingLeft": "0px", "paddingRight": "10px"})
        ]
    )
])

if __name__ == '__main__':
    app.run(debug=True, port=8800)
