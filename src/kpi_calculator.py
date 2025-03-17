import pandas as pd

def calculate_kpi(df: pd.DataFrame, weights: dict) -> pd.DataFrame:
    """
    Расчет KPI по формуле:
    KPI = w1*sales + w2*new_clients + w3*satisfaction.
    """
    df['KPI'] = (
        df['sales'] * weights['sales'] +
        df['new_clients'] * weights['new_clients'] +
        df['satisfaction'] * weights['satisfaction']
    )
    return df