"""
Componente de métricas principales (KPIs) del dashboard
"""

from dash import html
import pandas as pd

from ..components import create_metrics_grid, get_metric_colors
from ..utils.helpers import format_number


def create_main_metrics(
    df_diagnosticos: pd.DataFrame,
    df_peso_estancia: pd.DataFrame,
    df_severidad: pd.DataFrame,
) -> html.Main:
    """
    Crea el grid de métricas principales del dashboard.

    Args:
        df_diagnosticos: DataFrame de diagnósticos
        df_peso_estancia: DataFrame de peso y estancia
        df_severidad: DataFrame de severidad y mortalidad

    Returns:
        html.Div: Grid de métricas principales
    """
    # Calcular valores
    total_casos = len(df_diagnosticos) if not df_diagnosticos.empty else 0
    estancia_media = (
        df_peso_estancia["estancia_dias"].mean() if not df_peso_estancia.empty else 0
    )
    casos_graves = (
        (df_severidad["nivel_severidad_apr"] >= 3).sum()
        if not df_severidad.empty
        else 0
    )
    diagnosticos_unicos = (
        df_diagnosticos["diagnostico_principal"].nunique()
        if not df_diagnosticos.empty
        else 0
    )

    # Definir métricas
    metrics = [
        {
            "title": "Total de Casos",
            "value": format_number(total_casos),
            "subtitle": "Registros analizados",
            "icon": "📊",
            **get_metric_colors("blue"),
        },
        {
            "title": "Estancia Media",
            "value": f"{estancia_media:.1f}" if estancia_media > 0 else "N/A",
            "subtitle": "Días promedio",
            "icon": "⚕️",
            **get_metric_colors("green"),
        },
        {
            "title": "Casos Graves",
            "value": format_number(casos_graves),
            "subtitle": "Severidad grave/extrema",
            "icon": "🔴",
            **get_metric_colors("red"),
        },
        {
            "title": "Diagnósticos",
            "value": format_number(diagnosticos_unicos),
            "subtitle": "Condiciones únicas",
            "icon": "🏥",
            **get_metric_colors("purple"),
        },
    ]

    return html.Main(
        id="main-content",
        children=[create_metrics_grid(metrics)],
        className="metrics-grid",
    )
