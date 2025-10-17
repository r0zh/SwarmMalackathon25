"""
Funciones para crear gráficos de Plotly reutilizables
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Optional

from ..utils.themes import apply_theme


def create_empty_chart(
    message: str = "No hay datos disponibles", height: int = 400, theme: str = "dark"
) -> go.Figure:
    """
    Crea un gráfico vacío con un mensaje.

    Args:
        message: Mensaje a mostrar
        height: Altura del gráfico
        theme: Tema (dark/light)

    Returns:
        go.Figure: Figura vacía con mensaje
    """
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=20, color="#94a3b8"),
    )
    fig.update_layout(
        height=height,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )

    return apply_theme(fig, theme)


def create_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    orientation: str = "v",
    title: Optional[str] = None,
    labels: Optional[dict] = None,
    color: Optional[str] = None,
    color_continuous_scale: str = "Blues",
    height: int = 400,
    theme: str = "dark",
) -> go.Figure:
    """
    Crea un gráfico de barras.

    Args:
        df: DataFrame con los datos
        x: Columna para eje X
        y: Columna para eje Y
        orientation: 'v' (vertical) o 'h' (horizontal)
        title: Título del gráfico
        labels: Diccionario de etiquetas
        color: Columna para colorear
        color_continuous_scale: Escala de colores
        height: Altura del gráfico
        theme: Tema (dark/light)

    Returns:
        go.Figure: Gráfico de barras
    """
    if df.empty:
        return create_empty_chart(height=height, theme=theme)

    fig = px.bar(
        df,
        x=x,
        y=y,
        orientation=orientation,
        title=title,
        labels=labels or {},
        color=color or y if orientation == "h" else x,
        color_continuous_scale=color_continuous_scale,
    )

    fig.update_layout(
        height=height,
        showlegend=False,
        margin=dict(l=40, r=20, t=40 if title else 10, b=60),
        title_text=title,
        hovermode="closest",
    )

    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(203, 213, 225, 0.3)",
        tickfont=dict(size=10),
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(203, 213, 225, 0.3)",
        tickfont=dict(size=10),
    )

    return apply_theme(fig, theme)


def create_pie_chart(
    df: pd.DataFrame,
    values: str,
    names: str,
    title: Optional[str] = None,
    hole: float = 0.4,
    color_discrete_sequence: Optional[list] = None,
    category_orders: Optional[dict] = None,
    height: int = 400,
    theme: str = "dark",
) -> go.Figure:
    """
    Crea un gráfico de pastel/donut.

    Args:
        df: DataFrame con los datos
        values: Columna con los valores
        names: Columna con los nombres
        title: Título del gráfico
        hole: Tamaño del agujero central (0-1, 0=pastel completo)
        color_discrete_sequence: Secuencia de colores
        category_orders: Orden de categorías para la leyenda
        height: Altura del gráfico
        theme: Tema (dark/light)

    Returns:
        go.Figure: Gráfico de pastel
    """
    if df.empty:
        return create_empty_chart(height=height, theme=theme)

    fig = px.pie(
        df,
        values=values,
        names=names,
        title=title,
        hole=hole,
        color_discrete_sequence=color_discrete_sequence or px.colors.qualitative.Set3,
        category_orders=category_orders or {},
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        textfont_size=10,
        marker=dict(line=dict(color="#f8fafc", width=1.5)),
    )

    fig.update_layout(
        height=height,
        showlegend=True,
        margin=dict(l=10, r=10, t=40 if title else 10, b=10),
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            font=dict(size=9),
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#e2e8f0",
            borderwidth=1,
        ),
    )

    return apply_theme(fig, theme)


def create_line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: Optional[str] = None,
    labels: Optional[dict] = None,
    markers: bool = True,
    line_color: str = "#60a5fa",
    height: int = 350,
    theme: str = "dark",
) -> go.Figure:
    """
    Crea un gráfico de líneas.

    Args:
        df: DataFrame con los datos
        x: Columna para eje X
        y: Columna para eje Y
        title: Título del gráfico
        labels: Diccionario de etiquetas
        markers: Mostrar marcadores en los puntos
        line_color: Color de la línea
        height: Altura del gráfico
        theme: Tema (dark/light)

    Returns:
        go.Figure: Gráfico de líneas
    """
    if df.empty:
        return create_empty_chart(height=height, theme=theme)

    fig = px.line(
        df,
        x=x,
        y=y,
        title=title,
        labels=labels or {},
        markers=markers,
    )

    fig.update_traces(
        line=dict(color=line_color, width=3),
        marker=dict(size=8, color=line_color) if markers else {},
    )

    fig.update_layout(
        height=height,
        margin=dict(l=40, r=20, t=40 if title else 10, b=80),
        xaxis=dict(tickangle=-45, tickfont=dict(size=10)),
        yaxis=dict(tickfont=dict(size=10)),
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(203, 213, 225, 0.3)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(203, 213, 225, 0.3)")

    return apply_theme(fig, theme)


def create_heatmap(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: Optional[str] = None,
    labels: Optional[dict] = None,
    color_continuous_scale: str = "YlOrRd",
    category_orders: Optional[dict] = None,
    height: int = 500,
    theme: str = "dark",
) -> go.Figure:
    """
    Crea un mapa de calor.

    Args:
        df: DataFrame con los datos
        x: Columna para eje X
        y: Columna para eje Y
        title: Título del gráfico
        labels: Diccionario de etiquetas
        color_continuous_scale: Escala de colores
        category_orders: Orden de categorías
        height: Altura del gráfico
        theme: Tema (dark/light)

    Returns:
        go.Figure: Mapa de calor
    """
    if df.empty:
        return create_empty_chart(height=height, theme=theme)

    fig = px.density_heatmap(
        df,
        x=x,
        y=y,
        title=title,
        labels=labels or {},
        color_continuous_scale=color_continuous_scale,
        category_orders=category_orders or {},
    )

    fig.update_layout(
        height=height,
        margin=dict(l=40, r=20, t=40 if title else 10, b=80),
        xaxis=dict(tickangle=-45, tickfont=dict(size=9)),
        yaxis=dict(tickfont=dict(size=9)),
    )

    return apply_theme(fig, theme)


def create_scatter_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: Optional[str] = None,
    labels: Optional[dict] = None,
    color: Optional[str] = None,
    size: Optional[str] = None,
    color_continuous_scale: str = "Viridis",
    hover_data: Optional[dict] = None,
    height: int = 400,
    theme: str = "dark",
) -> go.Figure:
    """
    Crea un gráfico de dispersión.

    Args:
        df: DataFrame con los datos
        x: Columna para eje X
        y: Columna para eje Y
        title: Título del gráfico
        labels: Diccionario de etiquetas
        color: Columna para colorear puntos
        size: Columna para tamaño de puntos
        color_continuous_scale: Escala de colores
        hover_data: Datos adicionales al pasar el mouse
        height: Altura del gráfico
        theme: Tema (dark/light)

    Returns:
        go.Figure: Gráfico de dispersión
    """
    if df.empty:
        return create_empty_chart(height=height, theme=theme)

    fig = px.scatter(
        df,
        x=x,
        y=y,
        title=title,
        labels=labels or {},
        color=color,
        size=size,
        color_continuous_scale=color_continuous_scale,
        hover_data=hover_data or {},
    )

    fig.update_layout(
        height=height,
        margin=dict(l=40, r=20, t=40 if title else 10, b=60),
        xaxis=dict(tickfont=dict(size=10)),
        yaxis=dict(tickfont=dict(size=10)),
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(203, 213, 225, 0.3)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(203, 213, 225, 0.3)")

    return apply_theme(fig, theme)


def create_histogram(
    df: pd.DataFrame,
    x: str,
    color: Optional[str] = None,
    barmode: str = "group",
    title: Optional[str] = None,
    labels: Optional[dict] = None,
    color_discrete_map: Optional[dict] = None,
    category_orders: Optional[dict] = None,
    height: int = 400,
    theme: str = "dark",
) -> go.Figure:
    """
    Crea un histograma.

    Args:
        df: DataFrame con los datos
        x: Columna para eje X
        color: Columna para colorear barras
        barmode: 'group', 'stack', o 'overlay'
        title: Título del gráfico
        labels: Diccionario de etiquetas
        color_discrete_map: Mapeo de colores
        category_orders: Orden de categorías
        height: Altura del gráfico
        theme: Tema (dark/light)

    Returns:
        go.Figure: Histograma
    """
    if df.empty:
        return create_empty_chart(height=height, theme=theme)

    fig = px.histogram(
        df,
        x=x,
        color=color,
        barmode=barmode,
        title=title,
        labels=labels or {},
        color_discrete_map=color_discrete_map or {},
        category_orders=category_orders or {},
    )

    fig.update_layout(
        height=height,
        margin=dict(l=40, r=20, t=40 if title else 10, b=80),
        xaxis=dict(tickangle=-45 if barmode != "stack" else 0, tickfont=dict(size=10)),
        yaxis=dict(tickfont=dict(size=10)),
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(203, 213, 225, 0.3)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(203, 213, 225, 0.3)")

    return apply_theme(fig, theme)
