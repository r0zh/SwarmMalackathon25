"""
Sección de análisis de peso APR-GRD y estancia hospitalaria
"""

from dash import html, dcc
import pandas as pd

from ..components import create_scatter_chart, create_data_table
from ..utils.helpers import format_number


def create_weight_stay_section(df: pd.DataFrame, theme: str = "dark") -> html.Div:
    """
    Crea la sección completa de análisis de peso APR-GRD y estancia.

    Args:
        df: DataFrame con los datos de peso y estancia
        theme: Tema (dark/light)

    Returns:
        html.Div: Sección de peso y estancia
    """
    # Estadísticas
    total_registros = len(df) if not df.empty else 0
    peso_promedio = df["peso_espanol_apr"].mean() if not df.empty else 0
    estancia_promedio = df["estancia_dias"].mean() if not df.empty else 0
    estancia_max = df["estancia_dias"].max() if not df.empty else 0
    estancia_min = df["estancia_dias"].min() if not df.empty else 0

    # Gráfico de dispersión
    fig_scatter = create_scatter_chart(
        df=df if not df.empty else pd.DataFrame(),
        x="peso_espanol_apr",
        y="estancia_dias",
        title="Relación entre Peso APR-GRD y Estancia Hospitalaria",
        labels={
            "peso_espanol_apr": "Peso APR-GRD Español",
            "estancia_dias": "Días de Estancia",
        },
        color="estancia_dias",
        size="peso_espanol_apr",
        color_continuous_scale="Viridis",
        hover_data={
            "peso_espanol_apr": ":.3f",
            "estancia_dias": True,
        },
        height=400,
        theme=theme,
    )

    # Tabla de datos
    table_peso = create_data_table(
        df=df if not df.empty else pd.DataFrame(),
        columns=[
            {"name": "Peso APR-GRD Español", "id": "peso_espanol_apr"},
            {"name": "Estancia (días)", "id": "estancia_dias"},
        ],
        page_size=10,
        style_header={
            "backgroundColor": "#2563eb",
            "color": "white",
            "fontWeight": "bold",
            "textAlign": "center",
            "border": "1px solid #1e40af",
        },
    )

    return html.Div(
        [
            html.H3(
                "4️⃣ Peso APR-GRD y Estancia Hospitalaria",
                className="chart-title",
            ),
            html.P(
                "Correlación entre el peso APR-GRD español y los días de estancia hospitalaria",
                style={
                    "textAlign": "center",
                    "color": "#64748b",
                    "marginBottom": "20px",
                    "fontSize": "0.95rem",
                },
            ),
            # Gráfico de dispersión
            dcc.Graph(
                id="grafico-peso-estancia",
                config={"displayModeBar": False},
                figure=fig_scatter,
                style={"marginBottom": "30px"},
            ),
            # Tabla de datos
            table_peso,
            # Estadísticas resumen
            html.Div(
                [
                    html.Div(
                        [
                            html.H4("📈 Estadísticas", style={"marginBottom": "15px"}),
                            html.P(
                                f"Total de registros: {format_number(total_registros)}"
                            ),
                            html.P(f"Peso promedio: {peso_promedio:.3f}"),
                            html.P(f"Estancia promedio: {estancia_promedio:.1f} días"),
                            html.P(
                                f"Estancia máxima: {format_number(estancia_max)} días"
                            ),
                            html.P(
                                f"Estancia mínima: {format_number(estancia_min)} días"
                            ),
                        ],
                        style={
                            "backgroundColor": "#f0f9ff",
                            "padding": "20px",
                            "borderRadius": "8px",
                            "marginTop": "20px",
                            "border": "1px solid #bae6fd",
                        },
                    )
                ]
            ),
        ],
        className="chart-card full",
    )
