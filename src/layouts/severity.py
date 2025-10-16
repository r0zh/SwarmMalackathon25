"""
Sección de análisis de severidad y mortalidad APR
"""

from dash import html, dcc
import pandas as pd

from ..components import (
    create_pie_chart,
    create_histogram,
    create_heatmap,
    create_crosstab_table,
)
from ..utils.helpers import format_number, get_mode_value


def create_severity_section(df: pd.DataFrame, theme: str = "dark") -> html.Div:
    """
    Crea la sección completa de análisis de severidad y mortalidad.

    Args:
        df: DataFrame con los datos de severidad y mortalidad
        theme: Tema (dark/light)

    Returns:
        html.Div: Sección de severidad
    """
    # Estadísticas
    total_casos = len(df) if not df.empty else 0
    severidad_comun = get_mode_value(df["severidad_label"]) if not df.empty else "N/A"
    mortalidad_comun = get_mode_value(df["mortalidad_label"]) if not df.empty else "N/A"
    casos_extremos_severidad = (
        len(df[df["severidad_label"] == "Extremo"]) if not df.empty else 0
    )
    casos_extremos_mortalidad = (
        len(df[df["mortalidad_label"] == "Extremo"]) if not df.empty else 0
    )

    # Mapeo de colores
    color_map_severidad = {
        "Leve": "#22c55e",
        "Moderado": "#eab308",
        "Grave": "#f97316",
        "Extremo": "#dc2626",
    }

    color_map_mortalidad = {
        "Bajo": "#22c55e",
        "Moderado": "#eab308",
        "Alto": "#f97316",
        "Extremo": "#dc2626",
    }

    # Gráfico 1: Distribución de severidad
    df_severidad = (
        df["severidad_label"].value_counts().reset_index()
        if not df.empty
        else pd.DataFrame()
    )

    fig_severidad = create_pie_chart(
        df=df_severidad,
        values="count",
        names="severidad_label",
        color_discrete_sequence=[
            color_map_severidad.get(cat, "#94a3b8")
            for cat in ["Leve", "Moderado", "Grave", "Extremo"]
        ],
        height=400,
        theme=theme,
    )

    # Gráfico 2: Distribución de mortalidad
    df_mortalidad = (
        df["mortalidad_label"].value_counts().reset_index()
        if not df.empty
        else pd.DataFrame()
    )

    fig_mortalidad = create_pie_chart(
        df=df_mortalidad,
        values="count",
        names="mortalidad_label",
        color_discrete_sequence=[
            color_map_mortalidad.get(cat, "#94a3b8")
            for cat in ["Bajo", "Moderado", "Alto", "Extremo"]
        ],
        height=400,
        theme=theme,
    )

    # Gráfico 3: Mapa de calor severidad vs mortalidad
    fig_heatmap = create_heatmap(
        df=df if not df.empty else pd.DataFrame(),
        x="severidad_label",
        y="mortalidad_label",
        labels={
            "severidad_label": "Nivel de Severidad APR",
            "mortalidad_label": "Riesgo de Mortalidad APR",
        },
        color_continuous_scale="RdYlGn_r",
        category_orders={
            "severidad_label": ["Leve", "Moderado", "Grave", "Extremo"],
            "mortalidad_label": ["Bajo", "Moderado", "Alto", "Extremo"],
        },
        height=500,
        theme=theme,
    )

    # Gráfico 4: Barras agrupadas
    fig_bars = create_histogram(
        df=df if not df.empty else pd.DataFrame(),
        x="severidad_label",
        color="mortalidad_label",
        barmode="group",
        labels={
            "severidad_label": "Nivel de Severidad APR",
            "mortalidad_label": "Riesgo de Mortalidad",
            "count": "Número de Casos",
        },
        color_discrete_map=color_map_mortalidad,
        category_orders={
            "severidad_label": ["Leve", "Moderado", "Grave", "Extremo"],
            "mortalidad_label": ["Bajo", "Moderado", "Alto", "Extremo"],
        },
        height=450,
        theme=theme,
    )

    # Tabla de contingencia
    table_crosstab = create_crosstab_table(
        df=df if not df.empty else pd.DataFrame(),
        row_col="severidad_label",
        col_col="mortalidad_label",
        margins=True,
        margins_name="Total",
    )

    return html.Div(
        [
            html.H3(
                "3️⃣ Severidad y Riesgo de Mortalidad APR",
                className="chart-title",
            ),
            html.P(
                "Evaluación de la gravedad clínica y correlación con el riesgo de mortalidad",
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
                    html.Div(
                        [
                            html.H4(
                                "Distribución de Niveles de Severidad",
                                style={
                                    "textAlign": "center",
                                    "marginBottom": "15px",
                                },
                            ),
                            dcc.Graph(
                                id="grafico-severidad-dist",
                                config={"displayModeBar": False},
                                figure=fig_severidad,
                            ),
                        ],
                        className="chart-card chart-small",
                    ),
                    html.Div(
                        [
                            html.H4(
                                "Distribución de Riesgo de Mortalidad",
                                style={
                                    "textAlign": "center",
                                    "marginBottom": "15px",
                                },
                            ),
                            dcc.Graph(
                                id="grafico-mortalidad-dist",
                                config={"displayModeBar": False},
                                figure=fig_mortalidad,
                            ),
                        ],
                        className="chart-card chart-small",
                    ),
                ],
                className="charts-grid",
            ),
            # Mapa de calor
            html.Div(
                [
                    html.H4(
                        "Mapa de Calor: Correlación Severidad vs Mortalidad",
                        style={"textAlign": "center", "marginBottom": "15px"},
                    ),
                    dcc.Graph(
                        id="grafico-severidad-mortalidad-heatmap",
                        config={"displayModeBar": False},
                        figure=fig_heatmap,
                    ),
                ],
                style={"marginTop": "20px"},
            ),
            # Barras agrupadas
            html.Div(
                [
                    html.H4(
                        "Distribución Combinada: Severidad y Mortalidad",
                        style={"textAlign": "center", "marginBottom": "15px"},
                    ),
                    dcc.Graph(
                        id="grafico-severidad-mortalidad-bars",
                        config={"displayModeBar": False},
                        figure=fig_bars,
                    ),
                ],
                style={"marginTop": "20px"},
            ),
            # Tabla de contingencia
            html.Div(
                [
                    html.H4(
                        "Tabla de Contingencia: Severidad vs Mortalidad",
                        style={"textAlign": "center", "marginBottom": "15px"},
                    ),
                    table_crosstab,
                ],
                style={"marginTop": "30px"},
            ),
            # Estadísticas resumen
            html.Div(
                [
                    html.Div(
                        [
                            html.H4(
                                "📊 Análisis Estadístico",
                                style={"marginBottom": "15px"},
                            ),
                            html.P(f"Total de casos: {format_number(total_casos)}"),
                            html.P(f"Severidad más común: {severidad_comun}"),
                            html.P(
                                f"Riesgo de mortalidad más común: {mortalidad_comun}"
                            ),
                            html.P(
                                f"Casos de severidad extrema: {format_number(casos_extremos_severidad)}"
                            ),
                            html.P(
                                f"Casos de mortalidad extrema: {format_number(casos_extremos_mortalidad)}"
                            ),
                        ],
                        style={
                            "backgroundColor": "#fef2f2",
                            "padding": "20px",
                            "borderRadius": "8px",
                            "marginTop": "20px",
                            "border": "2px solid #fecaca",
                        },
                    )
                ]
            ),
        ],
        className="chart-card full",
    )
