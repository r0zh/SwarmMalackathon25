"""
Sección de análisis por sexo/género
"""

from dash import html, dcc
import pandas as pd

from ..components import (
    create_pie_chart,
    create_histogram,
    create_comparison_table,
)
from ..utils.helpers import format_number


def create_gender_analysis_section(df: pd.DataFrame, theme: str = "dark") -> html.Div:
    """
    Crea la sección completa de análisis por sexo.

    Args:
        df: DataFrame con los datos de diagnóstico por sexo
        theme: Tema (dark/light)

    Returns:
        html.Div: Sección de análisis por género
    """
    # Estadísticas
    total_masculino = len(df[df["sexo_label"] == "Masculino"]) if not df.empty else 0
    total_femenino = len(df[df["sexo_label"] == "Femenino"]) if not df.empty else 0
    diagnosticos_masculino = (
        df[df["sexo_label"] == "Masculino"]["diagnostico_principal"].nunique()
        if not df.empty
        else 0
    )
    diagnosticos_femenino = (
        df[df["sexo_label"] == "Femenino"]["diagnostico_principal"].nunique()
        if not df.empty
        else 0
    )

    # Gráfico 1: Distribución general por sexo
    df_sexo = (
        df["sexo_label"].value_counts().reset_index()
        if not df.empty
        else pd.DataFrame()
    )

    fig_sexo = create_pie_chart(
        df=df_sexo,
        values="count",
        names="sexo_label",
        color_discrete_sequence=[
            "#3b82f6",
            "#ec4899",
        ],  # Blue for Masculino, Pink for Femenino
        height=400,
        theme=theme,
    )

    # Gráfico 2: Top diagnósticos por sexo
    df_top_sexo = (
        df[
            df["diagnostico_principal"].isin(
                df["diagnostico_principal"].value_counts().head(10).index
            )
        ]
        if not df.empty
        else pd.DataFrame()
    )

    fig_diagnosticos_sexo = create_histogram(
        df=df_top_sexo,
        x="diagnostico_principal",
        color="sexo_label",
        barmode="group",
        labels={
            "diagnostico_principal": "Diagnóstico",
            "count": "Número de Casos",
            "sexo_label": "Sexo",
        },
        color_discrete_map={
            "Masculino": "#3b82f6",
            "Femenino": "#ec4899",
        },
        height=400,
        theme=theme,
    )

    # Gráfico 3: Proporción por diagnóstico
    df_proporcion = (
        df[
            df["diagnostico_principal"].isin(
                df["diagnostico_principal"].value_counts().head(15).index
            )
        ]
        if not df.empty
        else pd.DataFrame()
    )

    fig_proporcion = create_histogram(
        df=df_proporcion,
        x="sexo_label",
        color="sexo_label",
        barmode="stack",
        labels={
            "diagnostico_principal": "Diagnóstico",
            "count": "Número de Casos",
            "sexo_label": "Sexo",
        },
        color_discrete_map={
            "Masculino": "#3b82f6",
            "Femenino": "#ec4899",
        },
        height=500,
        theme=theme,
    )

    # Tabla comparativa
    table_sexo = create_comparison_table(
        df=df if not df.empty else pd.DataFrame(),
        index_col="diagnostico_principal",
        value_col="sexo_label",
        pivot_col="sexo_label",
        top_n=20,
        header_color="#6366f1",
    )

    return html.Div(
        [
            html.H3(
                "2️⃣ Análisis por Sexo: Perspectiva de Género",
                className="chart-title",
            ),
            html.P(
                "Distribución de diagnósticos y patrones diferenciados por sexo del paciente",
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
                    # Gráfico 1
                    html.Div(
                        [
                            html.H4(
                                "Distribución General por Sexo",
                                style={
                                    "textAlign": "center",
                                    "marginBottom": "15px",
                                },
                            ),
                            dcc.Graph(
                                id="grafico-sexo-general",
                                config={"displayModeBar": False},
                                figure=fig_sexo,
                            ),
                        ],
                        className="chart-card chart-small",
                    ),
                    # Gráfico 2
                    html.Div(
                        [
                            html.H4(
                                "Top 10 Diagnósticos por Sexo",
                                style={
                                    "textAlign": "center",
                                    "marginBottom": "15px",
                                },
                            ),
                            dcc.Graph(
                                id="grafico-diagnosticos-sexo",
                                config={"displayModeBar": False},
                                figure=fig_diagnosticos_sexo,
                            ),
                        ],
                        className="chart-card chart-large",
                    ),
                ],
                className="charts-grid",
            ),
            # Gráfico de proporción
            html.Div(
                [
                    html.H4(
                        "Proporción de Sexo en Diagnósticos Principales",
                        style={"textAlign": "center", "marginBottom": "15px"},
                    ),
                    dcc.Graph(
                        id="grafico-proporcion-sexo",
                        config={"displayModeBar": False},
                        figure=fig_proporcion,
                    ),
                ],
                style={"marginTop": "20px"},
            ),
            # Tabla comparativa
            html.Div(
                [
                    html.H4(
                        "Tabla Comparativa: Diagnósticos por Sexo",
                        style={"textAlign": "center", "marginBottom": "15px"},
                    ),
                    table_sexo,
                ],
                style={"marginTop": "30px"},
            ),
            # Estadísticas resumen
            html.Div(
                [
                    html.Div(
                        [
                            html.H4(
                                "📊 Estadísticas por Sexo",
                                style={"marginBottom": "15px"},
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H5(
                                                "👨 Masculino",
                                                style={"color": "#3b82f6"},
                                            ),
                                            html.P(
                                                f"Total casos: {format_number(total_masculino)}"
                                            ),
                                            html.P(
                                                f"Diagnósticos únicos: {format_number(diagnosticos_masculino)}"
                                            ),
                                        ],
                                        style={
                                            "flex": "1",
                                            "padding": "15px",
                                            "backgroundColor": "#eff6ff",
                                            "borderRadius": "8px",
                                            "border": "2px solid #bfdbfe",
                                        },
                                    ),
                                    html.Div(
                                        [
                                            html.H5(
                                                "👩 Femenino",
                                                style={"color": "#ec4899"},
                                            ),
                                            html.P(
                                                f"Total casos: {format_number(total_femenino)}"
                                            ),
                                            html.P(
                                                f"Diagnósticos únicos: {format_number(diagnosticos_femenino)}"
                                            ),
                                        ],
                                        style={
                                            "flex": "1",
                                            "padding": "15px",
                                            "backgroundColor": "#fdf2f8",
                                            "borderRadius": "8px",
                                            "border": "2px solid #fbcfe8",
                                        },
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "gap": "20px",
                                    "marginTop": "15px",
                                },
                            ),
                        ],
                        style={
                            "backgroundColor": "#f8fafc",
                            "padding": "20px",
                            "borderRadius": "8px",
                            "marginTop": "20px",
                            "border": "1px solid #e2e8f0",
                        },
                    )
                ]
            ),
        ],
        className="chart-card full",
    )
