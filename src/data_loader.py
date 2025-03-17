import pandas as pd

def load_data(path: str, source_type: str = 'csv') -> pd.DataFrame:
    """
    Загружает данные из CSV или БД.
    """
    if source_type == 'csv':
        return pd.read_csv(path)
    else:
        raise ValueError("Неподдерживаемый формат данных.")