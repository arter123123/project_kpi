import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

def plot_kpi_distribution(df: pd.DataFrame):
    """
    Гистограмма распределения KPI (matplotlib).
    """
    plt.hist(df['KPI'], bins=10)
    plt.title('Распределение KPI сотрудников')
    plt.xlabel('KPI')
    plt.ylabel('Количество сотрудников')
    plt.show()

def interactive_scatter(df: pd.DataFrame):
    """
    Интерактивный график Plotly.
    """
    fig = px.scatter(df, x='sales', y='KPI', color='cluster')
    fig.show()