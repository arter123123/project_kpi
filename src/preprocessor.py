import pandas as pd


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Проверяет типы данных, удаляет пропуски, нормализует.
    """
    numeric_cols = ['sales', 'new_clients', 'satisfaction']

    # Проверка типов
    for col in numeric_cols:
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"Колонка {col} содержит нечисловые данные")

    # Удаление пропусков
    df = df.dropna()

    # Нормализация
    df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].min()) / (df[numeric_cols].max() - df[numeric_cols].min())

    return df