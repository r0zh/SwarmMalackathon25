"""
Sección de análisis de diagnósticos y demografía
"""

from dash import html, dcc
import pandas as pd

from ..components import (
    create_bar_chart,
    create_pie_chart,
    create_line_chart,
    create_heatmap,
)
from ..utils.helpers import format_number, get_mode_value


def create_diagnostics_section(df: pd.DataFrame, theme: str = "dark") -> html.Div:
    """
    Crea la sección completa de análisis de diagnósticos y demografía.

    Args:
        df: DataFrame con los datos de diagnósticos
        theme: Tema (dark/light)

    Returns:
        html.Div: Sección de diagnósticos
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

    fig_edad = create_pie_chart(
        df=df_edad, values="count", names="rango_de_edad", height=400, theme=theme
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

    # Gráfico 4: Mapa de calor
    fig_heatmap = create_heatmap(
        df=df if not df.empty else pd.DataFrame(),
        x="rango_de_edad",
        y="diagnostico_principal",
        labels={
            "rango_de_edad": "Rango de Edad",
            "diagnostico_principal": "Diagnóstico",
        },
        color_continuous_scale="YlOrRd",
        height=600,
        theme=theme,
    )

    return html.Div(
        [
            html.H3(
                "1️⃣ Análisis de Diagnósticos y Demografía",
                className="chart-title",
            ),
            html.P(
                "Distribución de diagnósticos principales, tendencias temporales y análisis demográfico",
                style={
                    "textAlign": "center",
                    "color": "#64748b",
                    "marginBottom": "20px",
                    "fontSize": "0.95rem",
                },
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
                                style={
                                    "textAlign": "center",
                                    "marginBottom": "15px",
                                },
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
                                "Distribución por Rango de Edad",
                                id="chart-title-edad",
                                style={
                                    "textAlign": "center",
                                    "marginBottom": "15px",
                                },
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
                    html.H4(
                        "Ingresos por Mes",
                        id="chart-title-temporal",
                        style={"textAlign": "center", "marginBottom": "15px"},
                    ),
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
                style={"marginTop": "20px"},
                tabIndex=0,
            ),
            # Mapa de calor: Diagnóstico vs Edad
            html.Div(
                [
                    html.H4(
                        "Mapa de Calor: Diagnósticos más frecuentes por Rango de Edad",
                        id="chart-title-heatmap",
                        style={"textAlign": "center", "marginBottom": "15px"},
                    ),
                    html.Div(
                        "Mapa de calor mostrando la relación entre diagnósticos y rangos de edad, donde los colores más intensos indican mayor frecuencia",
                        className="sr-only",
                        id="chart-desc-heatmap",
                    ),
                    dcc.Graph(
                        id="grafico-heatmap",
                        config={"displayModeBar": False},
                        figure=fig_heatmap,
                    ),
                ],
                style={"marginTop": "20px"},
                tabIndex=0,
            ),
            # Estadísticas resumen
            html.Div(
                [
                    html.Div(
                        [
                            html.H4(
                                "📊 Estadísticas Generales",
                                style={"marginBottom": "15px"},
                            ),
                            html.P(
                                f"Total de registros: {format_number(total_registros)}"
                            ),
                            html.P(
                                f"Diagnósticos únicos: {format_number(diagnosticos_unicos)}"
                            ),
                            html.P(f"Rango de edad más común: {rango_edad_comun}"),
                            html.P(
                                f"Diagnóstico más frecuente: {diagnostico_frecuente}"
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
