"""
Sección de análisis de peso APR-GRD y estancia hospitalaria
"""

from dash import html, dcc
import pandas as pd

from ..components import create_scatter_chart, create_data_table
from ..utils.helpers import format_number


def create_weight_stay_section(df: pd.DataFrame, theme: str = "light") -> html.Div:
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
        theme=theme,
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
            html.Div(
                [
                    html.H3(
                        "4️⃣ Peso APR-GRD y Estancia Hospitalaria",
                        className="section-title",
                    ),
                    html.P(
                        "Correlación entre el peso APR-GRD español y los días de estancia hospitalaria",
                        className="section-subtitle",
                    ),
                ],
                style={"marginBottom": "32px"},
            ),
            # Gráfico de dispersión
            html.Div(
                [
                    html.Div(
                        [
                            html.H4(
                                "Relación entre Peso APR-GRD y Estancia Hospitalaria"
                            ),
                            dcc.Graph(
                                id="grafico-peso-estancia",
                                config={"displayModeBar": False},
                                figure=fig_scatter,
                            ),
                        ],
                        className="chart-card",
                    )
                ],
                style={"margin": "0 24px 32px 24px"},
            ),
            # Tabla de datos
            html.Div(
                [
                    html.Div(
                        [
                            html.H4("Datos de Peso y Estancia"),
                            table_peso,
                        ],
                        className="chart-card",
                    )
                ],
                style={"margin": "0 24px 32px 24px"},
            ),
        ],
        className="section-container",
        role="region",
    )
