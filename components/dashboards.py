from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar
from globals import *
from app import app







card_icon = {
    "color": "white",
    "textAling": "center",
    "fontSize": 30,
    "margin": "auto",

}

graph_margin = dict(l=25, r=25, t=25, b=0)

# =========  Layout  =========== #
layout = dbc.Col([
    dbc.Row([
    # Saldo Total
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Saldo', className="light", style={"color":"white"}),
                    html.H5('R$ 5.400,00', id='p-saldo-dashboards', style={'background-color': "rgb(17,17,17)", "color":"white"})
                ], style={'padding-left': '20px', 'padding-top': '10px', 'background-color': "rgb(17,17,17)"}, ),
                dbc.Card(
                    html.Div(className='fa fa-university', style=card_icon),
                    color='warning',
                    style={'maxWidth': 75, 'height': 100, 'margin-left': '-10px'} 
    
                )
            ])
        ], width = 4),

    # Receita
        dbc.Col([
                dbc.CardGroup([
                    dbc.Card([
                        html.Legend('Receita', className="light", style={"color":"white"}),
                        html.H5('R$ 10.400,00', id='p-receita-dashboards', style={'background-color': "rgb(17,17,17)","color":"white"})
                    ], style={'padding-left': '20px', 'padding-top': '10px','background-color': "rgb(17,17,17)"}, ),
                    dbc.Card(
                        html.Div(className='fa fa-money', style=card_icon),
                        color='green',
                        style={'maxWidth': 75, 'height': 100, 'margin-left': '-10px'} 
        
                    )
                ])
            ], width = 4),

    # despesa
        dbc.Col([
                dbc.CardGroup([
                    dbc.Card([
                        html.Legend('Despesa', className="light", style={"color":"white"}),
                        html.H5('R$ 5.000,00', id='p-despesa-dashboards', style={'background-color': "rgb(17,17,17)","color":"white"})
                    ], style={'padding-left': '20px', 'padding-top': '10px','background-color': "rgb(17,17,17)"}, ),
                    dbc.Card(
                        html.Div(className='fa fa-money', style=card_icon),
                        color='red',
                        style={'maxWidth': 75, 'height': 100, 'margin-left': '-10px'} 
        
                    )
                ])
            ], width = 4),

        ], style={'margin': '10px'}),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    html.Legend("Filtrar lançamentos", className="light", style={"color":"white"}),
                    html.Label("Categoria das receitas", className="light", style={"color": "#00FF7F"}),
                    html.Div(
                        dcc.Dropdown(
                            id="dropdown-receita",
                            clearable=False,
                            style={"width": "100%"},
                            persistence=True,
                            persistence_type="session",
                            multi=True)
                    ),
                    html.Label("Categoria das despesas", className="light", style={"margin-top": "10px", "color": "#FF0000"}),
                    html.Div(
                        dcc.Dropdown(
                            id="dropdown-despesa",
                            clearable=False,
                            style={"width": "100%"},
                            persistence=True,
                            persistence_type="session",
                            multi=True)
                    ),
                     html.Legend("Período de Análise", className="light", style={"margin-top": "10px", "color": "white"}),
                        dcc.DatePickerRange(
                            month_format='DD, MMM, YY',
                            end_date_placeholder_text='Data...',
                            start_date=datetime.today() -  + timedelta(days=90),
                            end_date=datetime.today() + timedelta(days=0),
                            display_format='DD/MM/YYYY', # Definindo o formato de exibição da data
                            with_portal=True,
                            updatemode='singledate',
                            id='date-picker-config',
                            style={'z-index': '100' }, ),
                ], style={'height': "100%", 'padding': '20px', 'background-color': 'rgb(17,17,17)'})
    
            ], width=4),
              
            dbc.Col(
                dbc.Card(dcc.Graph(id="graph1"), style={"height": "100%", "padding": "10px",'background-color': "rgb(17,17,17)"}), width=8
            )
    
        ], style={"margin": "10px"}),
        
        dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(id="graph2"), style={"padding": "10px", 'background-color': "rgb(17,17,17)"}), width=6),
            dbc.Col(dbc.Card(dcc.Graph(id="graph3"), style={"padding": "10px", 'background-color': "rgb(17,17,17)"}), width=3),
            dbc.Col(dbc.Card(dcc.Graph(id="graph4"), style={"padding": "10px", 'background-color': "rgb(17,17,17)"}), width=3),
        ], style={"margin": "10px"})
       
    ])




# ========== Callbacks ========== #
@app.callback([Output("dropdown-receita", "options"),
               Output("dropdown-receita", "value"),
               Output("p-receita-dashboards", "children")],
               Input("store-receitas", "data"))
def populate_dropdownvalues(data):
    df = pd.DataFrame(data)
    valor = df['Valor'].sum()
    val = df.Categoria.unique().tolist()

    
    return ([{"label": x, "value": x} for x in val], val, f"R$ {valor}")

# ========== Callbacks ========== #
@app.callback([Output("dropdown-despesa", "options"),
               Output("dropdown-despesa", "value"),
               Output("p-despesa-dashboards", "children")],
               Input("store-despesas", "data"))
def populate_dropdownvalues(data):
    df = pd.DataFrame(data)
    valor = df['Valor'].sum()
    val = df.Categoria.unique().tolist()

    
    return ([{"label": x, "value": x} for x in val], val, f"R$ {valor}")

@app.callback(
    Output("p-saldo-dashboards", "children"),
    [Input("store-despesas", "data"),
     Input("store-receitas", "data")])
def saldo_total(despesas, receitas):
    df_despesas = pd.DataFrame(despesas)
    df_receitas = pd.DataFrame(receitas)

    valor = df_receitas['Valor'].sum() - df_despesas['Valor'].sum()

    return f"R$ {valor}"

@app.callback(
    Output('graph1', 'figure'),

    [Input('store-despesas', 'data'),
     Input('store-receitas', 'data'),
     Input("dropdown-despesa","value"),
    Input("dropdown-receita", "value"),]
)

def update_output(data_despesa, data_receita, despesa, receita):
    
    df_despesas = pd.DataFrame(data_despesa).set_index("Data")[["Valor"]]
    df_ds = df_despesas.groupby("Data").sum().rename(columns={"Valor": "Despesa"})

    df_receitas = pd.DataFrame(data_receita).set_index("Data")[["Valor"]]
    df_rc = df_receitas.groupby("Data").sum().rename(columns={"Valor": "Receita"})

    df_acum = df_ds.join(df_rc, how="outer").fillna(0)
    df_acum["Acum"] = df_acum["Receita"] - df_acum["Despesa"]
    df_acum["Acum"] = df_acum["Acum"].cumsum()

    fig = go.Figure()
    fig.add_trace(go.Scatter(name="Fluxo de caixa", x=df_acum.index, y=df_acum["Acum"], mode="lines+markers"))

    fig.update_layout(margin=graph_margin, height = 400)
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    fig.update_layout(title="Saldo diário", title_x=0.5)
    #fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)')
    fig.update_layout(
    template="plotly_dark",
    plot_bgcolor = 'rgba(0,0,0,0)',
    font=dict(color="white")
)

    return fig

@app.callback(
    Output('graph2', 'figure'),
    [Input('store-receitas', 'data'),
    Input('store-despesas', 'data'),
    Input('dropdown-receita', 'value'),
    Input('dropdown-despesa', 'value'),
    Input('date-picker-config', 'start_date'),
    Input('date-picker-config', 'end_date')]
    #Input(ThemeChangerAIO.ids.radio("theme"), "value")] 
)
def graph2_show(data_receita, data_despesa, receita, despesa, start_date, end_date):
    df_rc = pd.DataFrame(data_receita)
    df_ds = pd.DataFrame(data_despesa)
    

    dfs = [df_ds, df_rc]

    df_rc['Output'] = 'Receitas'
    df_ds['Output'] = 'Despesas'
    df_final = pd.concat(dfs)

    df_final['Data'] = pd.to_datetime(df_final['Data']) # conversão de dados para datetime


    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_final = df_final[(df_final["Data"] >= start_date) & (df_final["Data"] <= end_date)]
    df_final = df_final[(df_final['Categoria'].isin(receita)) | (df_final['Categoria'].isin(despesa))]

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    #mask = (df_final['Data'] > start_date) & (df_final['Data'] <= end_date) 
    #df_final = df_final.loc[mask]

    

    fig = px.bar(df_final, x="Data", y="Valor", color='Output', barmode="group", color_discrete_sequence=['red', 'LimeGreen'])
    fig.update_layout(margin=graph_margin, height=350)
    #fig.update_traces(marker_line_color='white')
    #fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    fig.update_layout(
    template="plotly_dark",
    plot_bgcolor = 'rgba(0,0,0,0)',
    font=dict(color="white"))

    return fig



# Gráfico 3
@app.callback(
    Output('graph3', "figure"),
    [Input('store-receitas', 'data'),
    Input('dropdown-receita', 'value')]
)
def pie_receita(data_receita, receita):
    df = pd.DataFrame(data_receita)
    df = df[df['Categoria'].isin(receita)]

    fig = px.pie(df, values=df.Valor, names=df.Categoria, hole=.2)
    fig.update_layout(title={'text': "Receitas"})
    fig.update_layout(margin=graph_margin, height=350)
    #fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(
    template="plotly_dark",
    plot_bgcolor = 'rgba(0,0,0,0)',
    font=dict(color="white"))
                  
    return fig    

# Gráfico 4
@app.callback(
    Output('graph4', "figure"),
    [Input('store-despesas', 'data'),
    Input('dropdown-despesa', 'value')]
)
def pie_despesa(data_despesa, despesa):
    df = pd.DataFrame(data_despesa)
    df = df[df['Categoria'].isin(despesa)]

    fig = px.pie(df, values=df.Valor, names=df.Categoria, hole=.2)
    fig.update_layout(title={'text': "Despesas"})

    fig.update_layout(margin=graph_margin, height=350)
    #fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(
    template="plotly_dark",
    plot_bgcolor = 'rgba(0,0,0,0)',
    font=dict(color="white"))

    return fig