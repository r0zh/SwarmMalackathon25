"""
Funciones para aplicar temas (claro/oscuro) a los gráficos de Plotly
"""

import plotly.graph_objects as go


# Definición de colores para cada tema
THEME_COLORS = {
    "dark": {
        "background": "rgba(0,0,0,0)",
        "plot_bg": "rgba(0,0,0,0.02)",
        "text": "#e2e8f0",
        "title": "#f1f5f9",
        "grid": "#334155",
    },
    "light": {
        "background": "rgba(255,255,255,0)",
        "plot_bg": "rgba(248,250,252,0.5)",
        "text": "#1e293b",
        "title": "#0f172a",
        "grid": "#e2e8f0",
    },
}


def get_theme_colors(theme: str = "dark") -> dict:
    """
    Obtiene los colores para un tema específico.

    Args:
        theme: "dark" o "light"

    Returns:
        dict: Diccionario con los colores del tema
    """
    return THEME_COLORS.get(theme, THEME_COLORS["dark"])


def apply_theme(fig: go.Figure, theme: str = "dark") -> go.Figure:
    """
    Aplica el tema (claro/oscuro) consistente a las figuras de Plotly.

    Args:
        fig: Figura de Plotly
        theme: "dark" o "light" (default: "dark")

    Returns:
        fig: Figura con el tema aplicado
    """
    colors = get_theme_colors(theme)
    template = "plotly_dark" if theme == "dark" else "plotly"

    fig.update_layout(
        template=template,
        paper_bgcolor=colors["background"],
        plot_bgcolor=colors["plot_bg"],
        font=dict(color=colors["text"], family="Inter, system-ui, sans-serif"),
        title_font=dict(color=colors["title"], size=16),
    )

    return fig


def apply_dark_theme(fig: go.Figure) -> go.Figure:
    """
    Aplica el tema oscuro a una figura de Plotly.
    Función de conveniencia para mantener compatibilidad con código existente.

    Args:
        fig: Figura de Plotly

    Returns:
        fig: Figura con el tema oscuro aplicado
    """
    return apply_theme(fig, theme="dark")


def apply_light_theme(fig: go.Figure) -> go.Figure:
    """
    Aplica el tema claro a una figura de Plotly.
    Función de conveniencia para mantener compatibilidad con código existente.

    Args:
        fig: Figura de Plotly

    Returns:
        fig: Figura con el tema claro aplicado
    """
    return apply_theme(fig, theme="light")
