"""
Sección de insights y conclusiones
"""

from dash import html
import pandas as pd

from ..utils.helpers import calculate_percentage, format_number, get_mode_value


def create_insights_section(
    df_diagnosticos: pd.DataFrame, df_severidad: pd.DataFrame, df_peso: pd.DataFrame
) -> html.Div:
    """
    Crea la sección de insights clave y conclusiones.

    Args:
        df_diagnosticos: DataFrame de diagnósticos
        df_severidad: DataFrame de severidad y mortalidad
        df_peso: DataFrame de peso y estancia

    Returns:
        html.Div: Sección de insights
    """
    # Calcular insights
    diagnosticos_unicos = (
        df_diagnosticos["diagnostico_principal"].nunique()
        if not df_diagnosticos.empty
        else 0
    )

    casos_graves = (
        (df_severidad["nivel_severidad_apr"] >= 3).sum()
        if not df_severidad.empty
        else 0
    )
    total_severidad = len(df_severidad) if not df_severidad.empty else 1
    porcentaje_graves = calculate_percentage(casos_graves, total_severidad)

    rango_edad_predominante = (
        get_mode_value(df_diagnosticos["rango_de_edad"])
        if not df_diagnosticos.empty
        else "N/A"
    )

    estancia_promedio = df_peso["estancia_dias"].mean() if not df_peso.empty else 0

    return html.Div(
        [
            html.H3("5️⃣ Insights Clave y Conclusiones", className="chart-title"),
            html.Div(
                [
                    html.Div(
                        [
                            html.H4("🎯 Diagnósticos"),
                            html.P(
                                f"Los {format_number(diagnosticos_unicos)} diagnósticos únicos muestran una alta diversidad en condiciones de salud mental"
                                if diagnosticos_unicos > 0
                                else "Datos no disponibles"
                            ),
                        ],
                        className="tip-card",
                    ),
                    html.Div(
                        [
                            html.H4("⚕️ Severidad"),
                            html.P(
                                f"El {porcentaje_graves} de casos presentan severidad grave o extrema"
                                if casos_graves > 0
                                else "Datos no disponibles"
                            ),
                        ],
                        className="tip-card",
                    ),
                    html.Div(
                        [
                            html.H4("👥 Demografía"),
                            html.P(
                                f"Rango de edad predominante: {rango_edad_predominante} años"
                                if rango_edad_predominante != "N/A"
                                else "Datos no disponibles"
                            ),
                        ],
                        className="tip-card",
                    ),
                    html.Div(
                        [
                            html.H4("🏥 Estancia"),
                            html.P(
                                f"Estancia promedio: {estancia_promedio:.1f} días con correlación al peso APR-GRD"
                                if estancia_promedio > 0
                                else "Datos no disponibles"
                            ),
                        ],
                        className="tip-card",
                    ),
                ],
                className="tips-grid",
            ),
        ],
        className="chart-card full tips-section",
    )
