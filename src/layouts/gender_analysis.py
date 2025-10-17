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


def create_gender_analysis_section(df: pd.DataFrame, theme: str = "light") -> html.Div:
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
        category_orders={"sexo_label": ["Masculino", "Femenino"]},
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

    # Tabla comparativa
    table_sexo = create_comparison_table(
        df=df if not df.empty else pd.DataFrame(),
        index_col="diagnostico_principal",
        value_col="sexo_label",
        pivot_col="sexo_label",
        top_n=20,
        header_color="#6366f1",
        theme=theme,
    )

    return html.Div(
        [
            html.Div(
                [
                    html.H3(
                        "2️⃣ Análisis por Sexo: Perspectiva de Género",
                        className="section-title",
                    ),
                    html.P(
                        "Distribución de diagnósticos y patrones diferenciados por sexo del paciente",
                        className="section-subtitle",
                    ),
                ],
                style={"marginBottom": "32px"},
            ),
            # Gráficos en grid
            html.Div(
                [
                    # Gráfico 1
                    html.Div(
                        [
                            html.H4("Distribución General por Sexo"),
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
                            html.H4("Top 10 Diagnósticos por Sexo"),
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
            # Tabla comparativa
            html.Div(
                [
                    html.Div(
                        [
                            html.H4("Tabla Comparativa: Diagnósticos por Sexo"),
                            table_sexo,
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
