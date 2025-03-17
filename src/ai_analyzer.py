from sklearn.cluster import KMeans
import pandas as pd
from sklearn.linear_model import LinearRegression

def cluster_employees(df: pd.DataFrame, n_clusters: int = 3) -> pd.DataFrame:
    """
    Кластеризация сотрудников методом k-means.
    """
    X = df[['KPI', 'sales', 'satisfaction']]
    kmeans = KMeans(n_clusters=n_clusters)
    df['cluster'] = kmeans.fit_predict(X)
    return df

def predict_kpi(df: pd.DataFrame, features: list, target: str) -> dict:
    """
    Прогнозирование KPI с помощью линейной регрессии.
    """
    X = df[features]
    y = df[target]
    model = LinearRegression()
    model.fit(X, y)
    return {'model': model, 'score': model.score(X, y)}