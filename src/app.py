import dash
from dash import dcc, html, Input, Output, State, dash_table
import plotly.express as px
import pandas as pd
import base64
import io
from src.data_loader import load_data
from src.preprocessor import preprocess_data
from src.kpi_calculator import calculate_kpi
from src.ai_analyzer import cluster_employees

# Инициализация приложения Dash
app = dash.Dash(__name__)

# Данные по умолчанию (для демонстрации)
default_df = pd.DataFrame({
    'employee_id': [1, 2, 3, 4],
    'sales': [150, 90, 200, 130],
    'new_clients': [12, 5, 8, 10],
    'satisfaction': [4.5, 3.2, 4.8, 4.1]
})

# Макет приложения
app.layout = html.Div([
    # Заголовок
    html.H1('Дашборд KPI сотрудников', style={'textAlign': 'center'}),

    # Блок загрузки файла (оставляем ваш существующий)
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Перетащите или ', html.A('выберите CSV-файл')]),
        style={
            'border': '1px dashed #ccc',
            'padding': '20px',
            'margin': '10px 0'
        }
    ),

    # Статус загрузки
    html.Div(id='upload-status', style={'margin': '10px 0'}),

    # НОВЫЙ БЛОК: Гистограмма KPI
    dcc.Graph(
        id='kpi-histogram',
        style={'margin': '20px 0', 'border': '1px solid #eee'}
    ),

    # Таблица предпросмотра (оставляем ваш существующий)
    html.Div(
        id='preview-table',
        style={'margin': '20px 0'}
    ),

    # Фильтр кластеров (оставляем ваш существующий)
    dcc.Dropdown(
        id='cluster-filter',
        multi=True,
        placeholder='Выберите кластеры',
        style={'margin': '10px 0'}
    ),

    # Точечный график (оставляем ваш существующий)
    dcc.Graph(
        id='kpi-scatter',
        style={'margin': '20px 0'}
    )
])


def process_data(contents):
    """Обрабатывает загруженные данные."""
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    df = load_data(df=df)
    df = preprocess_data(df)
    weights = {'sales': 0.4, 'new_clients': 0.3, 'satisfaction': 0.3}
    df = calculate_kpi(df, weights)
    df = cluster_employees(df, n_clusters=3)
    return df


# Основной callback
@app.callback(
    [Output('cluster-filter', 'options'),
     Output('cluster-filter', 'value'),
     Output('kpi-scatter', 'figure'),
     Output('preview-table', 'children'),
     Output('upload-status', 'children'),
     Output('kpi-histogram', 'figure')],  # Добавляем новый Output для гистограммы
    [Input('upload-data', 'contents')]
)
def update_all(contents):
    if not contents:
        # Используем демо-данные
        df = default_df.copy()
        df = calculate_kpi(df, {'sales': 0.4, 'new_clients': 0.3, 'satisfaction': 0.3})
        df = cluster_employees(df)

        # Генерация гистограммы
        hist_fig = px.histogram(
            df,
            x='KPI',
            title='Распределение KPI (демо-данные)',
            nbins=10,
            color_discrete_sequence=['#636EFA']
        )
        hist_fig.update_layout(bargap=0.1)

        # Возвращаем все значения
        return (
            [{'label': f'Кластер {c}', 'value': c} for c in df['cluster'].unique()],
            df['cluster'].unique(),
            px.scatter(df, x='sales', y='KPI', color='cluster'),
            dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in df.columns],
                page_size=5
            ),
            'Используются демо-данные',
            hist_fig
        )

    try:
        # Обработка загруженного файла
        df = process_data(contents)

        # Генерация гистограммы
        hist_fig = px.histogram(
            df,
            x='KPI',
            title='Распределение KPI после нормализации',
            nbins=10,
            color_discrete_sequence=['#00CC96']
        )
        hist_fig.update_layout(bargap=0.1)

        return (
            [{'label': f'Кластер {c}', 'value': c} for c in df['cluster'].unique()],
            df['cluster'].unique(),
            px.scatter(df, x='sales', y='KPI', color='cluster'),
            dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in df.columns],
                page_size=5
            ),
            'Файл успешно загружен!',
            hist_fig
        )
    except Exception as e:
        return (
            [],
            [],
            {},
            html.Div(f"Ошибка: {str(e)}", style={'color': 'red'}),
            html.Div("Ошибка загрузки файла!", style={'color': 'red'}),
            {}  # Пустая фигура при ошибке
        )


if __name__ == '__main__':
    app.run(debug=True)