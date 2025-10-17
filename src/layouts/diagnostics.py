"""
Sección de análisis de diagnósticos y demografía
"""

from dash import html, dcc
import pandas as pd

from ..components import (
    create_bar_chart,
    create_pie_chart,
    create_line_chart,
)
from ..utils.helpers import format_number, get_mode_value


from typing import Union


def create_diagnostics_section(
    df: pd.DataFrame, theme: str = "light"
) -> Union[html.Div, html.Section]:
    """
    Crea la sección completa de análisis de diagnósticos y demografía.

    Args:
        df: DataFrame con los datos de diagnósticos
        theme: Tema (dark/light)

    Returns:
        html.Section: Sección de diagnósticos
    """
    # Preparar datos
    total_registros = len(df) if not df.empty else 0
    diagnosticos_unicos = df["diagnostico_principal"].nunique() if not df.empty else 0
    rango_edad_comun = get_mode_value(df["rango_de_edad"]) if not df.empty else "N/A"
    diagnostico_frecuente = (
        get_mode_value(df["diagnostico_principal"]) if not df.empty else "N/A"
    )

    # Gráfico 1: Top 10 diagnósticos
    df_top_diagnosticos = (
        df["diagnostico_principal"].value_counts().head(10).reset_index()
        if not df.empty
        else pd.DataFrame()
    )

    fig_diagnosticos = create_bar_chart(
        df=df_top_diagnosticos,
        x="count",
        y="diagnostico_principal",
        orientation="h",
        labels={
            "diagnostico_principal": "Diagnóstico",
            "count": "Número de Casos",
        },
        color_continuous_scale="Blues",
        height=400,
        theme=theme,
    )

    # Gráfico 2: Distribución por edad
    df_edad = (
        df["rango_de_edad"].value_counts().reset_index()
        if not df.empty
        else pd.DataFrame()
    )

    # Define age range order for legend sorting
    age_order = [
        "0-5",
        "6-10",
        "11-15",
        "16-20",
        "21-25",
        "26-30",
        "31-35",
        "36-40",
        "41-45",
        "46-50",
        "51-55",
        "56-60",
        "61-65",
        "66-70",
        "71-75",
        "76-80",
        "81-85",
        "+85",
    ]

    # Vibrant color palette for age ranges
    age_colors = [
        "#0891b2",
        "#06b6d4",
        "#10b981",
        "#14b8a6",
        "#059669",
        "#16a34a",
        "#84cc16",
        "#eab308",
        "#f59e0b",
        "#f97316",
        "#ef4444",
        "#dc2626",
        "#991b1b",
        "#7c2d12",
        "#6366f1",
        "#8b5cf6",
        "#a855f7",
        "#d946ef",
    ]

    fig_edad = create_pie_chart(
        df=df_edad,
        values="count",
        names="rango_de_edad",
        category_orders={"rango_de_edad": age_order},
        color_discrete_sequence=age_colors,
        height=400,
        theme=theme,
    )

    # Gráfico 3: Ingresos por mes
    df_temporal = (
        df["mes_de_ingreso"].value_counts().sort_index().reset_index()
        if not df.empty
        else pd.DataFrame()
    )

    fig_temporal = create_line_chart(
        df=df_temporal,
        x="mes_de_ingreso",
        y="count",
        labels={
            "mes_de_ingreso": "Mes de Ingreso",
            "count": "Número de Ingresos",
        },
        height=350,
        theme=theme,
    )

    return html.Div(
        [
            html.Div(
                [
                    html.H3(
                        "1️⃣ Análisis de Diagnósticos y Demografía",
                        className="section-title",
                        id="section-diagnostics-title",
                    ),
                    html.P(
                        "Distribución de diagnósticos principales, tendencias temporales y análisis demográfico",
                        className="section-subtitle",
                    ),
                ],
                style={"marginBottom": "32px"},
            ),
            # Gráficos en grid
            html.Div(
                [
                    # Gráfico 1: Distribución por diagnóstico
                    html.Div(
                        [
                            html.H4(
                                "Top 10 Diagnósticos Principales",
                                id="chart-title-diagnosticos",
                            ),
                            html.Div(
                                "Gráfico de barras horizontales mostrando los 10 diagnósticos principales más frecuentes",
                                className="sr-only",
                                id="chart-desc-diagnosticos",
                            ),
                            dcc.Graph(
                                id="grafico-diagnosticos",
                                config={"displayModeBar": False},
                                figure=fig_diagnosticos,
                            ),
                        ],
                        className="chart-card chart-large",
                        tabIndex=0,
                    ),
                    # Gráfico 2: Distribución por edad
                    html.Div(
                        [
                            html.H4(
                                "Distribución por Rango de Edad", id="chart-title-edad"
                            ),
                            html.Div(
                                "Gráfico circular mostrando la distribución de casos por rangos de edad",
                                className="sr-only",
                                id="chart-desc-edad",
                            ),
                            dcc.Graph(
                                id="grafico-edad",
                                config={"displayModeBar": False},
                                figure=fig_edad,
                            ),
                        ],
                        className="chart-card chart-small",
                        tabIndex=0,
                    ),
                ],
                className="charts-grid",
            ),
            # Gráfico de tendencia temporal
            html.Div(
                [
                    html.Div(
                        [
                            html.H4("Ingresos por Mes", id="chart-title-temporal"),
                            html.Div(
                                "Gráfico de líneas mostrando la evolución temporal de ingresos mensuales",
                                className="sr-only",
                                id="chart-desc-temporal",
                            ),
                            dcc.Graph(
                                id="grafico-temporal",
                                config={"displayModeBar": False},
                                figure=fig_temporal,
                            ),
                        ],
                        className="chart-card",
                        tabIndex=0,
                    )
                ],
                style={"margin": "0 24px 32px 24px"},
            ),
        ],
        className="section-container",
        role="region",
    )
