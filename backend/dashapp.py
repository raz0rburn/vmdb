from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import json
import pandas as pd 
import dash_bootstrap_components as dbc


from pandas import json_normalize 
import configparser
from mysql.connector import MySQLConnection, Error




app = Dash(__name__)


def read_mysql_config(filename='/opt/vmware-api/config-mysql',section='client'):
    parser = configparser.ConfigParser()
    parser.read(filename)
    db={}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1].replace("\"","")
    else:
        raise Exception('{0} not found in the {1} file'.format(section,filename))
    return db

mysql_config = read_mysql_config()
conn = MySQLConnection(**mysql_config)
df = pd.read_sql("SELECT * FROM vminfo WHERE DATE(datetime) = CURDATE() ",conn)
df['date'] = pd.to_datetime(df["datetime"]).dt.date   
a=df.groupby("datetime").size().values
df= df.drop_duplicates(subset="datetime").assign(count=a)

df_ds = pd.read_sql("SELECT datetime,ds_name,is_local_vmfs,capacity,provisioned,free_space,hosts_quantity,vm_quantity FROM dsinfo WHERE DATE(datetime) = CURDATE()",conn)
df_ds['date'] = pd.to_datetime(df_ds["datetime"]).dt.date
df_ds['free_percent'] = df_ds['free_space'] / df_ds['capacity'] * 100
df_ds.sort_values(by=['is_local_vmfs'], inplace=True)
df_ds.sort_values(by=['free_percent'], inplace=True)

a=df_ds.groupby("datetime").size().values
#df_ds= df_ds.drop_duplicates(subset="datetime").assign(count=a)

df_host = pd.read_sql("SELECT * FROM hostinfo order by host_name",conn)
df_host['date'] = pd.to_datetime(df_host["datetime"]).dt.date   
a=df_host.groupby("datetime").size().values
#df_host= df_host.drop_duplicates(subset="datetime").assign(count=a)






import requests
#read from rest api
r_topapp = requests.get('http://')
d_topapp = json.loads(r_topapp.text)
df_topapp = pd.json_normalize(d_topapp, record_path='topApp')
start_time_topapp = d_topapp['startTime']
end_time_topapp = d_topapp['endTime']
df_topapp[3] = df_topapp[0] + ' - '+ df_topapp[1]

print(df_topapp)
r_topdst = requests.get('http://')
d_topdst = json.loads(r_topdst.text)
df_topdst = pd.json_normalize(d_topdst, record_path='topDst')
df_topdst[3] = df_topdst[0] + ' - '+ df_topdst[1]
   

print(df_topdst)
r_topsrc = requests.get('http://')
d_topsrc = json.loads(r_topsrc.text)
df_topsrc = pd.json_normalize(d_topsrc, record_path='topSrc')
df_topsrc[3] = df_topsrc[0] + ' - '+ df_topsrc[1]

print(df_topsrc)


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    dbc.Row([
            html.P(start_time_topapp+' - '+end_time_topapp),
            dbc.Col(
                [html.H4("Top Applications"),dcc.Graph(id="graph1")],
                md=4,
                ),
            dbc.Col(
                [html.H4("Top Destinations"),dcc.Graph(id="graph2")],
                md=4,
                ),
            dbc.Col(
                [html.H4("Top Source"),dcc.Graph(id="graph3")],
                md=4,
                )
        ],justify="center",),
    dbc.Row([
                dcc.RadioItems(options=['mem', 'provisioned_space', 'cpu'], value='provisioned_space', id='controls-and-radio-item'),
                dcc.Graph(figure={}, id='controls-and-graph')
            ]),
        
            
    dbc.Row([
            html.P('DATASTORE'),
            dash_table.DataTable(data=df_ds.to_dict('records'), page_size=20),
            dcc.Graph(figure=px.histogram(df, x='datetime', y='count', histfunc='sum'))
            ]),          
    dbc.Row([
            html.Div(children='HOST INFO'),
            dash_table.DataTable(data=df_host.to_dict('records'), page_size=20),
            ]),    

  
],fluid=True)

@app.callback(

    
    Output(component_id='controls-and-graph', component_property='figure'),
    Output("graph1", "figure"),
    Output("graph2", "figure"),
    Output("graph3", "figure"),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='cluster', y=col_chosen, histfunc='sum')
    fig_pie1 = px.pie(df_topapp, values=2, names=3, hole=0.3)
    fig_pie2 = px.pie(df_topdst, values=2, names=3, hole=0.3)
    fig_pie3 = px.pie(df_topsrc, values=2, names=3, hole=0.3)

    
    
    return (fig,fig_pie1,fig_pie2,fig_pie3)


if __name__ == "__main__":
    
    app.run_server(debug=True, host='0.0.0.0')
