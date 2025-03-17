import pandas as pd

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Очистка данных: удаление пропусков, нормализация.
    """
    # Удаление строк с пропусками
    df = df.dropna()

    # Нормализация числовых признаков (min-max)
    numeric_cols = ['sales', 'new_clients', 'satisfaction']
    df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].min()) / (df[numeric_cols].max() - df[numeric_cols].min())

    return df