"""
Componentes de tablas reutilizables usando dash_table
"""

from dash import dash_table
import pandas as pd
from typing import Optional, List, Dict, Any, Literal, cast


def create_data_table(
    df: pd.DataFrame,
    columns: Optional[List[Dict[str, Any]]] = None,
    page_size: int = 10,
    sort_action: Literal["native", "custom", "none"] = "native",
    filter_action: Literal["native", "custom", "none"] = "native",
    style_table: Optional[Dict[str, Any]] = None,
    style_header: Optional[Dict[str, Any]] = None,
    style_cell: Optional[Dict[str, Any]] = None,
    style_data: Optional[Dict[str, Any]] = None,
    style_data_conditional: Optional[List[Dict[str, Any]]] = None,
    **kwargs: Any,
) -> dash_table.DataTable:
    """
    Crea una tabla de datos interactiva.

    Args:
        df: DataFrame con los datos
        columns: Lista de diccionarios con definición de columnas
        page_size: Número de filas por página
        sort_action: Tipo de ordenamiento ('native', 'custom', None)
        filter_action: Tipo de filtro ('native', 'custom', None)
        style_table: Estilos para la tabla completa
        style_header: Estilos para el encabezado
        style_cell: Estilos para las celdas
        style_data: Estilos para los datos
        style_data_conditional: Estilos condicionales
        **kwargs: Argumentos adicionales para DataTable

    Returns:
        dash_table.DataTable: Tabla de datos
    """
    # Columnas por defecto si no se especifican
    if columns is None:
        columns = [{"name": col, "id": col} for col in df.columns]

    # Estilos por defecto
    default_style_table = {
        "overflowX": "auto",
        "overflowY": "auto",
        "maxHeight": "400px",
    }

    default_style_cell = {
        "textAlign": "center",
        "padding": "12px",
        "fontFamily": "Segoe UI, sans-serif",
        "fontSize": "14px",
        "border": "1px solid #e2e8f0",
    }

    default_style_header = {
        "backgroundColor": "#6366f1",
        "color": "white",
        "fontWeight": "bold",
        "textAlign": "center",
        "border": "1px solid #4f46e5",
    }

    default_style_data = {
        "backgroundColor": "white",
        "color": "#1e293b",
    }

    default_style_data_conditional = [
        {
            "if": {"row_index": "odd"},
            "backgroundColor": "#f8fafc",
        },
        {
            "if": {"state": "active"},
            "backgroundColor": "#dbeafe",
            "border": "1px solid #2563eb",
        },
    ]

    # Combinar estilos
    final_style_table = {**default_style_table, **(style_table or {})}
    final_style_cell = {**default_style_cell, **(style_cell or {})}
    final_style_header = {**default_style_header, **(style_header or {})}
    final_style_data = {**default_style_data, **(style_data or {})}
    final_style_data_conditional = (
        style_data_conditional
        if style_data_conditional is not None
        else default_style_data_conditional
    )

    return dash_table.DataTable(
        columns=columns,  # type: ignore[arg-type]
        data=df.to_dict("records") if not df.empty else [],  # type: ignore[arg-type]
        page_size=page_size,
        sort_action=sort_action,
        sort_mode="multi",
        filter_action=filter_action,
        style_table=final_style_table,
        style_cell=final_style_cell,
        style_header=final_style_header,
        style_data=final_style_data,
        style_data_conditional=final_style_data_conditional,  # type: ignore[arg-type]
        **kwargs,
    )


def create_comparison_table(
    df: pd.DataFrame,
    index_col: str,
    value_col: str,
    pivot_col: str,
    top_n: int = 20,
    header_color: str = "#6366f1",
    **kwargs,
) -> dash_table.DataTable:
    """
    Crea una tabla comparativa con pivot.

    Args:
        df: DataFrame original
        index_col: Columna para usar como índice
        value_col: Columna con los valores
        pivot_col: Columna para hacer pivot
        top_n: Número de filas superiores a mostrar
        header_color: Color del encabezado
        **kwargs: Argumentos adicionales

    Returns:
        dash_table.DataTable: Tabla comparativa
    """
    if df.empty:
        return create_data_table(pd.DataFrame())

    # Crear tabla pivot
    pivot_df = df.groupby(index_col)[value_col].value_counts().unstack(fill_value=0)

    # Añadir columna total
    pivot_df["Total"] = pivot_df.sum(axis=1)

    # Ordenar y tomar top N
    pivot_df = pivot_df.sort_values("Total", ascending=False).head(top_n).reset_index()

    # Definir columnas
    columns = [{"name": col, "id": col} for col in pivot_df.columns]

    # Estilos personalizados
    style_header = {
        "backgroundColor": header_color,
        "color": "white",
        "fontWeight": "bold",
        "textAlign": "center",
        "border": f"1px solid {header_color}",
    }

    style_data_conditional = [
        {
            "if": {"row_index": "odd"},
            "backgroundColor": "#f8fafc",
        },
        {
            "if": {"column_id": "Total"},
            "backgroundColor": "#fee2e2",
            "fontWeight": "bold",
        },
    ]

    return create_data_table(
        df=pivot_df,
        columns=columns,
        style_header=style_header,
        style_data_conditional=style_data_conditional,
        **kwargs,
    )


def create_crosstab_table(
    df: pd.DataFrame,
    row_col: str,
    col_col: str,
    margins: bool = True,
    margins_name: str = "Total",
    **kwargs,
) -> dash_table.DataTable:
    """
    Crea una tabla de tabulación cruzada (crosstab).

    Args:
        df: DataFrame original
        row_col: Columna para las filas
        col_col: Columna para las columnas
        margins: Incluir totales marginales
        margins_name: Nombre para los totales
        **kwargs: Argumentos adicionales

    Returns:
        dash_table.DataTable: Tabla de tabulación cruzada
    """
    if df.empty:
        return create_data_table(pd.DataFrame())

    # Crear crosstab
    crosstab_df = pd.crosstab(
        df[row_col], df[col_col], margins=margins, margins_name=margins_name
    )

    # Resetear índice para tener como columna
    crosstab_df = crosstab_df.rename_axis("index").reset_index().fillna(0)

    # Convertir a int si es posible
    for col in crosstab_df.columns:
        if col != "index":
            crosstab_df[col] = crosstab_df[col].astype(int)

    # Definir columnas
    columns = [
        {"name": f"{row_col} \\ {col_col}" if col == "index" else col, "id": col}
        for col in crosstab_df.columns
    ]

    # Estilos condicionales
    style_data_conditional = [
        {
            "if": {"row_index": "odd"},
            "backgroundColor": "#fef2f2",
        },
        {
            "if": {"column_id": margins_name},
            "backgroundColor": "#fee2e2",
            "fontWeight": "bold",
        },
        {
            "if": {"filter_query": f"{{index}} = '{margins_name}'"},
            "backgroundColor": "#fee2e2",
            "fontWeight": "bold",
        },
    ]

    style_header = {
        "backgroundColor": "#dc2626",
        "color": "white",
        "fontWeight": "bold",
        "textAlign": "center",
        "border": "1px solid #b91c1c",
    }

    return create_data_table(
        df=crosstab_df,
        columns=columns,
        style_header=style_header,
        style_data_conditional=style_data_conditional,
        page_size=20,
        **kwargs,
    )
