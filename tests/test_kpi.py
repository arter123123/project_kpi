import pytest
import pandas as pd
from src.kpi_calculator import calculate_kpi

def test_kpi_calculation():
    data = pd.DataFrame({
        'sales': [150, 90],
        'new_clients': [12, 5],
        'satisfaction': [4.5, 3.2]
    })
    weights = {'sales': 0.4, 'new_clients': 0.3, 'satisfaction': 0.3}
    result = calculate_kpi(data, weights)
    assert round(result['KPI'][0], 2) == 64.95  # 150*0.4 + 12*0.3 + 4.5*0.3 = 64.95
    assert round(result['KPI'][1], 2) == 38.46  # Исправлено с 37.26 на 38.46