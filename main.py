import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

from func import get_data_per_person

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = dbc.Container(

    children=
    [
        dbc.Row(
            dbc.Col(dcc.Loading(
                id="loading_graph",
                type="default",
                children=html.Div(children=[html.Div(dcc.Graph(id='graph'))], id='div_for_graph'),
            ), width=12)

        ),

        dbc.Row(
            [
                dbc.Col(dbc.Col(html.H5("Выберите интервал дат")), width=4),
                dbc.Col(dbc.Col(html.Div(id='div_for_picker', children=[
                    dcc.DatePickerRange(
                        id='date-picker',
                    ),
                ], )), width=4)
            ]),

        dcc.Store(id='data-store')

    ]
    ,
    className="p-5", )


@app.callback(
    Output('div_for_picker', 'children'),
    [Input('data-store', 'data')])
def make_picker(data):
    tree = ET.parse('sample.xml')
    root = tree.getroot()
    all_date_list = [datetime.strptime(item.text, "%d-%m-%Y %H:%M:%S") for item in root.findall('person/end')]
    start_date = min(all_date_list)
    end_date = max(all_date_list)

    return dcc.DatePickerRange(
        id='date-picker',
        min_date_allowed=start_date - timedelta(days=1),
        max_date_allowed=end_date,
        end_date=end_date.strftime("%Y-%m-%d"),
        start_date=start_date.strftime("%Y-%m-%d"),
    )


@app.callback(
    dash.dependencies.Output('div_for_graph', 'children'),
    [dash.dependencies.Input('date-picker', 'start_date'),
     dash.dependencies.Input('date-picker', 'end_date')])
def update_output(start_date, end_date):
    if start_date and end_date:
        df, mess = get_data_per_person(start_date=start_date, end_date=end_date)

        if not df.empty:
            data = [
                {
                    'labels': list(df.index),
                    'values': list(df.work_time),
                    'type': 'pie',
                    'textinfo': 'label+value',
                    'insidetextorientation': 'radial',
                }]

            return dcc.Graph(
                id='graph',
                figure={
                    'data': data,
                    'layout': {
                        'title': {
                            'text': f'Общее время - {round(df.work_time.sum())},ч',
                            'font': {
                                'size': 30,
                                'color': 'black'
                            },
                            'height': 800}

                    }
                }
            )
        else:
            return dcc.Graph(
                id='graph',
                figure={
                    "layout": {
                        "xaxis": {
                            "visible": False
                        },
                        "yaxis": {
                            "visible": False
                        },
                        "annotations": [
                            {
                                "text": mess,
                                "xref": "paper",
                                "yref": "paper",
                                "showarrow": False,
                                "font": {
                                    "size": 28
                                }
                            }
                        ]
                    }
                }
            )


if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=False)
