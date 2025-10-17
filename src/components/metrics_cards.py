"""
Componentes de tarjetas de métricas (KPIs) reutilizables
"""

from dash import html
from typing import Optional, Dict, Any


def create_metric_card(
    title: str,
    value: str,
    subtitle: str,
    icon: str = "📊",
    color: str = "#2563eb",
    background: str = "#eff6ff",
    border: str = "#bfdbfe",
) -> html.Div:
    """
    Crea una tarjeta de métrica (KPI) individual.

    Args:
        title: Título de la métrica
        value: Valor principal a mostrar
        subtitle: Texto secundario
        icon: Emoji o icono
        color: Color del valor
        background: Color de fondo
        border: Color del borde

    Returns:
        html.Div: Componente de tarjeta de métrica
    """
    # Crear un ID único para el título basado en el título
    title_id = f"metric-title-{title.lower().replace(' ', '-')}"

    return html.Div(
        [
            html.Div(
                [
                    html.Span(
                        icon,
                        className="metric-icon",
                        style={
                            "fontSize": "2.5rem",
                            "marginBottom": "16px",
                            "display": "block",
                        },
                        role="img",
                        title=f"Icono de {title}",
                    ),
                    html.H3(
                        title,
                        id=title_id,
                        style={
                            "marginBottom": "20px",
                            "fontSize": "0.875rem",
                            "fontWeight": "600",
                            "color": "#64748b",
                            "textTransform": "uppercase",
                            "letterSpacing": "0.5px",
                        },
                    ),
                    html.H2(
                        value,
                        className="metric-value",
                        style={
                            "color": color,
                            "marginBottom": "12px",
                            "fontSize": "2.75rem",
                            "fontWeight": "700",
                            "lineHeight": "1",
                        },
                    ),
                    html.P(
                        subtitle,
                        style={
                            "fontSize": "0.875rem",
                            "color": "#64748b",
                            "fontWeight": "400",
                            "margin": "0",
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "center",
                    "justifyContent": "center",
                },
            ),
            # Hidden description for screen readers
            html.Span(
                f"{title}: {value}, {subtitle}",
                className="sr-only",
            ),
        ],
        className="metric-card",
        style={
            "backgroundColor": background,
            "border": f"2px solid {border}",
            "borderRadius": "16px",
            "padding": "32px 24px",
            "textAlign": "center",
            "minHeight": "200px",
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "center",
        },
        role="region",
        tabIndex=0,
    )


def create_metrics_grid(metrics: list) -> html.Div:
    """
    Crea un grid de tarjetas de métricas.

    Args:
        metrics: Lista de diccionarios con los parámetros para cada tarjeta

    Returns:
        html.Div: Grid de métricas

    Example:
        metrics = [
            {
                "title": "Total Casos",
                "value": "1,234",
                "subtitle": "Registros analizados",
                "icon": "📊",
                "color": "#2563eb",
                "background": "#eff6ff",
                "border": "#bfdbfe"
            },
            ...
        ]
    """
    cards = [create_metric_card(**metric) for metric in metrics]

    return html.Div(
        cards,
        style={
            "display": "grid",
            "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
            "gap": "20px",
            "marginBottom": "40px",
        },
    )


# Configuraciones de colores predefinidas para métricas
METRIC_COLORS = {
    "blue": {
        "color": "#2563eb",
        "background": "#eff6ff",
        "border": "#bfdbfe",
    },
    "green": {
        "color": "#16a34a",
        "background": "#f0fdf4",
        "border": "#bbf7d0",
    },
    "red": {
        "color": "#dc2626",
        "background": "#fef2f2",
        "border": "#fecaca",
    },
    "purple": {
        "color": "#7c3aed",
        "background": "#faf5ff",
        "border": "#e9d5ff",
    },
    "yellow": {
        "color": "#ca8a04",
        "background": "#fefce8",
        "border": "#fef08a",
    },
    "orange": {
        "color": "#ea580c",
        "background": "#fff7ed",
        "border": "#fed7aa",
    },
}


def get_metric_colors(color_name: str = "blue") -> Dict[str, str]:
    """
    Obtiene el esquema de colores para una métrica.

    Args:
        color_name: Nombre del esquema de color

    Returns:
        Dict con color, background y border
    """
    return METRIC_COLORS.get(color_name, METRIC_COLORS["blue"])
