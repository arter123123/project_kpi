import dash
from dash import dcc, html, Input, Output
import plotly.express as px
from src.data_loader import load_data
from src.preprocessor import preprocess_data
from src.kpi_calculator import calculate_kpi
from src.ai_analyzer import cluster_employees

app = dash.Dash(__name__)

# Загрузка и обработка данных
def load_and_process_data():
    df = load_data('../data/raw/employee_data.csv')  # Путь исправлен!
    df = preprocess_data(df)
    weights = {'sales': 0.4, 'new_clients': 0.3, 'satisfaction': 0.3}
    df = calculate_kpi(df, weights)
    df = cluster_employees(df, n_clusters=3)
    return df

df = load_and_process_data()

# Интерфейс Dash
app.layout = html.Div([
    html.H1('Дашборд KPI сотрудников', style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='cluster-filter',
        options=[{'label': f'Кластер {i}', 'value': i} for i in df['cluster'].unique()],
        value=df['cluster'].unique(),
        multi=True,
        placeholder='Выберите кластеры'
    ),
    dcc.Graph(id='kpi-scatter')
])

# Обновление графика по фильтру
@app.callback(
    Output('kpi-scatter', 'figure'),
    [Input('cluster-filter', 'value')]
)
def update_graph(selected_clusters):
    filtered_df = df[df['cluster'].isin(selected_clusters)]
    fig = px.scatter(
        filtered_df, 
        x='sales', 
        y='KPI', 
        color='cluster',
        hover_data=['employee_id', 'new_clients']
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)  # Исправлено!