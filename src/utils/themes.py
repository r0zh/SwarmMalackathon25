"""
Funciones para aplicar temas (claro/oscuro) a los gráficos de Plotly
"""

import plotly.graph_objects as go


# Definición de colores para cada tema
THEME_COLORS = {
    "dark": {
        "background": "rgba(30, 41, 59, 0)",  # Transparent dark
        "plot_bg": "rgba(15, 23, 42, 0.3)",  # Dark blue-gray
        "text": "#cbd5e1",  # Light gray text
        "title": "#f1f5f9",  # Very light gray for titles
        "grid": "rgba(71, 85, 105, 0.3)",  # Subtle dark grid
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


def apply_theme(fig: go.Figure, theme: str = "light") -> go.Figure:
    """
    Aplica el tema (claro/oscuro) consistente a las figuras de Plotly.

    Args:
        fig: Figura de Plotly
        theme: "dark" o "light" (default: "light")

    Returns:
        fig: Figura con el tema aplicado
    """
    colors = get_theme_colors(theme)
    template = "plotly_dark" if theme == "dark" else "plotly_white"

    fig.update_layout(
        template=template,
        paper_bgcolor=colors["background"],
        plot_bgcolor=colors["plot_bg"],
        font=dict(
            color=colors["text"], family="system-ui, -apple-system, sans-serif", size=11
        ),
        title_font=dict(
            color=colors["title"],
            size=14,
            family="system-ui, -apple-system, sans-serif",
        ),
        hoverlabel=dict(
            bgcolor="#1e293b" if theme == "dark" else "white",
            font_color="#e2e8f0" if theme == "dark" else "#1e293b",
            font_size=11,
            font_family="system-ui, -apple-system, sans-serif",
        ),
        xaxis=dict(
            gridcolor=colors["grid"],
            color=colors["text"],
        ),
        yaxis=dict(
            gridcolor=colors["grid"],
            color=colors["text"],
        ),
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
