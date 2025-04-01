import pandas as pd
from typing import Optional


def load_data(file_path: Optional[str] = None, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """
    Загружает данные из CSV или принимает DataFrame.
    Проверяет обязательные колонки.
    """
    REQUIRED_COLUMNS = ['employee_id', 'sales', 'new_clients', 'satisfaction']

    if df is not None:
        data = df
    elif file_path:
        data = pd.read_csv(file_path)
    else:
        raise ValueError("Не указан источник данных")

    # Проверка колонок
    missing = [col for col in REQUIRED_COLUMNS if col not in data.columns]
    if missing:
        raise ValueError(f"Отсутствуют колонки: {missing}")

    return data