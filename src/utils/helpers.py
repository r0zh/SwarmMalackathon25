"""
Funciones de utilidad general para el dashboard
"""

import pandas as pd
from typing import Any, Optional


def format_number(
    value: Any, decimals: int = 0, prefix: str = "", suffix: str = ""
) -> str:
    """
    Formatea un número con separadores de miles y decimales.

    Args:
        value: Valor a formatear
        decimals: Número de decimales (default: 0)
        prefix: Prefijo a añadir (ej: "$", "€")
        suffix: Sufijo a añadir (ej: "%", "días")

    Returns:
        str: Número formateado
    """
    try:
        num = float(value)
        if decimals == 0:
            formatted = f"{num:,.0f}"
        else:
            formatted = f"{num:,.{decimals}f}"
        return f"{prefix}{formatted}{suffix}"
    except (ValueError, TypeError):
        return "N/A"


def safe_division(numerator: Any, denominator: Any, default: Any = 0) -> float:
    """
    Realiza una división segura, manejando división por cero.

    Args:
        numerator: Numerador
        denominator: Denominador
        default: Valor por defecto si hay división por cero

    Returns:
        float: Resultado de la división o valor por defecto
    """
    try:
        num = float(numerator)
        den = float(denominator)
        if den == 0:
            return default
        return num / den
    except (ValueError, TypeError):
        return default


def get_mode_value(series: pd.Series, default: str = "N/A") -> str:
    """
    Obtiene el valor más común (moda) de una Serie de pandas de forma segura.

    Args:
        series: Serie de pandas
        default: Valor por defecto si no hay moda

    Returns:
        str: Valor de la moda o valor por defecto
    """
    try:
        if series.empty:
            return default
        mode = series.mode()
        if mode.empty:
            return default
        return str(mode[0])
    except Exception:
        return default


def calculate_percentage(value: Any, total: Any, decimals: int = 1) -> str:
    """
    Calcula un porcentaje de forma segura.

    Args:
        value: Valor parcial
        total: Valor total
        decimals: Decimales a mostrar

    Returns:
        str: Porcentaje formateado con símbolo %
    """
    percentage = safe_division(value, total, 0) * 100
    return format_number(percentage, decimals=decimals, suffix="%")


def is_dataframe_empty(df: pd.DataFrame) -> bool:
    """
    Verifica si un DataFrame está vacío de forma segura.

    Args:
        df: DataFrame a verificar

    Returns:
        bool: True si está vacío o es None
    """
    return df is None or df.empty


def get_dataframe_summary(df: pd.DataFrame) -> dict:
    """
    Obtiene un resumen estadístico de un DataFrame.

    Args:
        df: DataFrame

    Returns:
        dict: Diccionario con estadísticas básicas
    """
    if is_dataframe_empty(df):
        return {
            "total_rows": 0,
            "total_columns": 0,
            "memory_usage": "0 KB",
        }

    return {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB",
        "columns": list(df.columns),
    }


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Trunca un texto si excede la longitud máxima.

    Args:
        text: Texto a truncar
        max_length: Longitud máxima
        suffix: Sufijo a añadir si se trunca

    Returns:
        str: Texto truncado
    """
    if not text or len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix
