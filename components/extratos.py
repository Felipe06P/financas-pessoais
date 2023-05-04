import dash
from dash.dependencies import Input, Output
from dash import dash_table
from dash.dash_table.Format import Group
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import urllib
from dash_table.Format import Format, Scheme, Sign, Symbol

import io
import base64
import pandas as pd
from dash.dependencies import Input, Output, State

from app import app

# =========  Layout  =========== #
layout = dbc.Col([

    
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H1("Despesas", className="text-danger"),
                    html.Legend("R$ -", id="valor_despesa_card",  style={'font-size': '40px', 'background-color': "rgb(17,17,17)","color":"#1E90FF" },className="text-danger"),
                    #html.H6("Total de despesas"),
                ],
                  style={'text-align': 'center',  'background-color': "rgb(17,17,17)"}), style={ 'background-color': "rgb(17,17,17)"})
        ], width=6),

        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H1("Receitas", className="text-success"),
                    html.Legend("R$ -", id="valor_receita_card",  style={'font-size': '40px', 'background-color': "rgb(17,17,17)","color":"#1E90FF" },className="text-success"),
                    #html.H6("Total de receitas"),
                ],
                  style={'text-align': 'center',  'background-color': "rgb(17,17,17)"}), style={ 'background-color': "rgb(17,17,17)"})
        ], width=6),
        dbc.Col([
            dcc.Graph(id='bar-graph', style={'padding-top': '10px'}),
        ], width=6),
        dbc.Col([
            dcc.Graph(id='bar-graph2', style={'padding-top': '10px'}
),
        ], width=6)
    ], style={'background-color': "rgb(17,17,17)"}),
    

        dbc.Row([
        html.Legend("Tabela Receita / Despesa", className="text-white", style={'background-color': "rgb(17,17,17)","color":"#1E90FF" },),
        html.Div(id="tabela-extrato", className="text-primary", style={'background-color': "rgb(17,17,17)","color":"#1E90FF" }),
    ]),
        dbc.Button(
        "Baixar tabela em CSV",
        id="download-csv" ,
        className="mt-3",
        download="tabela-extrato.csv",
),
      #  dbc.Button(
       # "Baixar tabela em xlsx",
        #id="download-xlsx",
        #className="mt-3",
        #download="textratos.xlsx",
    #),
], style={"margin": "10px"})

# =========  Callbacks  =========== #
# Tabela
"""@app.callback(
    Output('tabela-despesas', 'children'),
    Input('store-despesas', 'data')
    
)
def imprimir_tabela (data):
    df = pd.DataFrame(data)
    df['Data'] = pd.to_datetime(df['Data']).dt.date

    df.loc[df['Efetuado'] == 0, 'Efetuado'] = 'Não'
    df.loc[df['Efetuado'] == 1, 'Efetuado'] = 'Sim'

    df.loc[df['Fixo'] == 0, 'Fixo'] = 'Não'
    df.loc[df['Fixo'] == 1, 'Fixo'] = 'Sim'

    df = df.fillna('-')

    df.sort_values(by='Data', ascending=False)

    tabela = dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": True}
            if i == "Descrição" or i == "Fixo" or i == "Efetuado"
            else {"name": i, "id": i, "deletable": False, "selectable": False}
            for i in df.columns
        ],

        data=df.to_dict('records'),
        filter_action="native",    
        sort_action="native",       
        sort_mode="single",  
        selected_columns=[],        
        selected_rows=[],          
        page_action="native",      
        page_current=0,             
        page_size=10,                        
    ),

    return tabela"""


"""##extratos original
@app.callback(
    Output('tabela-extrato', 'children'),
    [Input('store-despesas', 'data'), Input('store-receitas', 'data')]
)
def imprimir_tabela(data_despesas, data_receitas):
    # Combina os dados das despesas e receitas em um único dataframe
    df_despesas = pd.DataFrame(data_despesas)
    df_receitas = pd.DataFrame(data_receitas)
    df_despesas['Valor'] = -df_despesas['Valor']
    df = pd.concat([df_despesas, df_receitas], ignore_index=True, sort=False)
    
    # Faz o processamento dos dados e cria a tabela
    df['Data'] = pd.to_datetime(df['Data']).dt.strftime('%d/%m/%Y')
    df.loc[df['Efetuado'] == 0, 'Efetuado'] = 'Não'
    df.loc[df['Efetuado'] == 1, 'Efetuado'] = 'Sim'
    df.loc[df['Fixo'] == 0, 'Fixo'] = 'Não'
    df.loc[df['Fixo'] == 1, 'Fixo'] = 'Sim'
    df = df.fillna('-')
    df.sort_values(by='Data', ascending=False, inplace=True)
    tabela = dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": True}
            if i == "Descrição" or i == "Fixo" or i == "Efetuado"
            else {"name": i, "id": i, "deletable": False, "selectable": False}
            for i in df.columns
        ],
        data=df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        sort_mode="single",
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
        style_header={'backgroundColor': 'black'},
        style_cell={
        'backgroundColor': 'rgb(17,17,17)',
        'color': 'white'
        }
    )

    return tabela
"""
data_store = {}
data_store_id = 'minha_tabela'
data_table_id = 'minha_tabela_editavel'
# extratos teste
@app.callback(
    Output('tabela-extrato', 'children'),
    [Input('store-despesas', 'data'), Input('store-receitas', 'data')],
    [State('tabela-extrato', 'data')]
)
def imprimir_tabela(data_despesas, data_receitas, table_data):
    # Combina os dados das despesas e receitas em um único dataframe
    df_despesas = pd.DataFrame(data_despesas)
    df_receitas = pd.DataFrame(data_receitas)
    df_despesas['Valor'] = -df_despesas['Valor']
    df = pd.concat([df_despesas, df_receitas], ignore_index=True, sort=False)
    
    # Faz o processamento dos dados e cria a tabela
    df['Data'] = pd.to_datetime(df['Data']).dt.strftime('%d/%m/%Y')
    df.loc[df['Efetuado'] == 0, 'Efetuado'] = 'Não'
    df.loc[df['Efetuado'] == 1, 'Efetuado'] = 'Sim'
    df.loc[df['Fixo'] == 0, 'Fixo'] = 'Não'
    df.loc[df['Fixo'] == 1, 'Fixo'] = 'Sim'
    df = df.fillna('-')
    df.sort_values(by='Data', ascending=False, inplace=True)
    tabela = dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True, "editable": i != "Data"}
            if i == "Descrição" or i == "Fixo" or i == "Efetuado"
            else {"name": i, "id": i, "deletable": True, "selectable": True, "editable": i != "Data"}
            for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=True,
        filter_action="native",
        #filter_mode="any",
        filter_options={"columns": ["Descrição", "Categoria"]},
        sort_action="native",
        sort_mode="single",
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
        style_header={'backgroundColor': 'black'},
        style_cell={
        'backgroundColor': 'rgb(17,17,17)',
        'color': 'white'
        }
    )

   
    return tabela



# Bar Graph            
@app.callback(
    Output('bar-graph', 'figure'),
    [Input('store-despesas', 'data')]
   # Input(ThemeChangerAIO.ids.radio("theme"), "value")]
)
def bar_chart(data):
    df = pd.DataFrame(data)   
    df_grouped = df.groupby("Categoria").sum(numeric_only=True)[["Valor"]].reset_index()
    graph = px.bar(df_grouped, x='Categoria', y='Valor', title="Despesas Gerais",
                   color_discrete_sequence=['#CC0000']*len(df_grouped))
    #graph.update_layout(template=template_from_url(theme))
    #graph.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    graph.update_layout(margin=dict(l=25, r=25, t=25, b=0), height=400)
    graph.update_layout(
    template="plotly_dark",
    plot_bgcolor = 'rgba(0,0,0,0)',
    font=dict(color="white"))
    graph.update_xaxes(showgrid=False, zeroline=False)
    graph.update_yaxes(showgrid=False, zeroline=False)
    graph.update_layout(title_x=0.5)
    return graph

# Simple card
@app.callback(
    Output('valor_despesa_card', 'children'),
    Input('store-despesas', 'data')
)
def display_desp(data):
    df = pd.DataFrame(data)
    valor = df['Valor'].sum()
    
    return f"R$ {valor}"

#Receita
@app.callback(
    Output('bar-graph2', 'figure'),
    [Input('store-receitas', 'data')]
   # Input(ThemeChangerAIO.ids.radio("theme"), "value")]
)
def bar_chart(data):
    df = pd.DataFrame(data)   
    df_grouped = df.groupby("Categoria").sum(numeric_only=True)[["Valor"]].reset_index()
    graph = px.bar(df_grouped, x='Categoria', y='Valor', title="Receitas Gerais",
                   color_discrete_sequence=['LimeGreen']*len(df_grouped))
    #graph.update_layout(template=template_from_url(theme))
    graph.update_layout( plot_bgcolor='rgba(0,0,0,0)')
    graph.update_layout(margin=dict(l=25, r=25, t=25, b=0), height=400)
    graph.update_layout(
    template="plotly_dark",
    plot_bgcolor = 'rgba(0,0,0,0)',
    font=dict(color="white"))
    graph.update_xaxes(showgrid=False, zeroline=False)
    graph.update_yaxes(showgrid=False, zeroline=False)
    graph.update_layout(title_x=0.5)

    return graph

# Simple card
@app.callback(
    Output('valor_receita_card', 'children'),
    Input('store-receitas', 'data')
)
def display_desp(data):
    df = pd.DataFrame(data)
    valor = df['Valor'].sum()
    
    return f"R$ {valor}"

#baixar extratos

@app.callback(
    Output("download-csv", "href"),
    Input("store-despesas", "data"),
    Input("store-receitas", "data"),
)
def generate_csv(data_despesas, data_receitas):
    # Combina os dados das despesas e receitas em um único dataframe
    df_despesas = pd.DataFrame(data_despesas)
    df_receitas = pd.DataFrame(data_receitas)
    df_despesas['Valor'] = -df_despesas['Valor']
    df = pd.concat([df_despesas, df_receitas], ignore_index=True, sort=False)

    # Faz o processamento dos dados e cria a tabela
    df['Data'] = pd.to_datetime(df['Data']).dt.strftime('%d/%m/%Y')
    df.loc[df['Efetuado'] == 0, 'Efetuado'] = 'Não'
    df.loc[df['Efetuado'] == 1, 'Efetuado'] = 'Sim'
    df.loc[df['Fixo'] == 0, 'Fixo'] = 'Não'
    df.loc[df['Fixo'] == 1, 'Fixo'] = 'Sim'
    df = df.fillna('-')
    df.sort_values(by='Data', ascending=False, inplace=True)

    # Cria o arquivo CSV e retorna o link para download
    csv_string = df.to_csv(index=False, sep=';', encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
    return csv_string

#baixar extratos em excel

"""@app.callback(
        Output('download-xlsx', 'href'),
        Input('store-despesas', 'data'),
        Input('store-receitas', 'data'))
def generate_csv(data_despesas, data_receitas):
    # Combina os dados das despesas e receitas em um único dataframe
    df_despesas = pd.DataFrame(data_despesas)
    df_receitas = pd.DataFrame(data_receitas)
    df_despesas['Valor'] = -df_despesas['Valor']
    df = pd.concat([df_despesas, df_receitas], ignore_index=True, sort=False)

    # Faz o processamento dos dados e cria a tabela
    df['Data'] = pd.to_datetime(df['Data']).dt.strftime('%d/%m/%Y')
    df.loc[df['Efetuado'] == 0, 'Efetuado'] = 'Não'
    df.loc[df['Efetuado'] == 1, 'Efetuado'] = 'Sim'
    df.loc[df['Fixo'] == 0, 'Fixo'] = 'Não'
    df.loc[df['Fixo'] == 1, 'Fixo'] = 'Sim'
    df = df.fillna('-')
    df.sort_values(by='Data', ascending=False, inplace=True)

    # Cria o arquivo XLSX e retorna o link para download
    xlsx_io = io.BytesIO()
    with pd.ExcelWriter(xlsx_io, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, encoding='utf-8')
    xlsx_io.seek(0)
    xlsx_base64 = base64.b64encode(xlsx_io.read()).decode()
    href = html.A('Download Excel', href='data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,' + xlsx_base64, download='extratos.xlsx')
    return href
"""