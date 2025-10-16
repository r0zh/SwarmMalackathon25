"""
Componente de encabezado del dashboard
"""

from dash import html


def create_header() -> html.Div:
    """
    Crea el encabezado del dashboard con título y skip link para accesibilidad.

    Returns:
        html.Div: Componente contenedor con encabezado
    """
    return html.Div(
        [
            # Skip to main content link (para navegación por teclado)
            html.A(
                "Saltar al contenido principal",
                href="#main-content",
                className="skip-link",
                tabIndex="1",
                style={
                    "position": "absolute",
                    "left": "-9999px",
                    "zIndex": "999",
                    "padding": "1em",
                    "backgroundColor": "#2563eb",
                    "color": "white",
                    "textDecoration": "none",
                    "fontWeight": "bold",
                },
            ),
            # Header
            html.Header(
                [
                    html.H1(
                        "Dashboard de Análisis Hospitalario",
                        className="header-title",
                    ),
                    html.P(
                        "Análisis de datos hospitalarios y métricas de estancia",
                        className="subtitle",
                    ),
                    html.P(
                        "Datos en tiempo real · Análisis · Insights",
                        className="subtitle",
                        style={
                            "fontSize": "0.9rem",
                            "marginTop": "15px",
                            "opacity": "0.85",
                            "fontStyle": "italic",
                        },
                    ),
                ],
                className="header",
            ),
        ]
    )


def create_footer() -> html.Footer:
    """
    Crea el pie de página del dashboard.

    Returns:
        html.Footer: Componente de pie de página
    """
    return html.Footer(
        [html.P("© 2025 Dashboard de Análisis Hospitalario | Datos en tiempo real")],
        className="footer",
    )
