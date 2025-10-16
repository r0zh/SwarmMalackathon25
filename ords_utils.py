"""
Utilidades para interactuar con la API de Oracle ORDS.
"""

import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from config import Config


def fetch_ords_data(endpoint: str, limit: int = 1000) -> pd.DataFrame:
    """
    Función genérica para obtener datos desde Oracle ORDS con soporte para paginación.

    Args:
        endpoint: El endpoint de la API (ej: "peso_vs_estancia")
        limit: Número de registros por petición (default: 1000, máximo recomendado por ORDS)

    Returns:
        DataFrame con todos los datos obtenidos, o DataFrame vacío si hay error
    """
    base_url = f"{Config.ORDS_BASE_URL}/{endpoint}/"
    all_items = []
    offset = 0
    has_more = True

    try:
        print(f"Obteniendo datos de {endpoint}...")

        while has_more:
            # Construir URL con parámetros de paginación
            url = f"{base_url}?limit={limit}&offset={offset}"

            response = requests.get(
                url,
                auth=HTTPBasicAuth(Config.ORDS_USERNAME, Config.ORDS_PASSWORD),
                headers={"Content-Type": "application/json"},
            )

            if response.status_code == 200:
                data = response.json()

                # Verificar si hay items en la respuesta
                if "items" in data and len(data["items"]) > 0:
                    all_items.extend(data["items"])
                    print(
                        f"  → Obtenidos {len(data['items'])} registros (Total acumulado: {len(all_items)})"
                    )

                    # Verificar si hay más datos
                    has_more = data.get("hasMore", False)

                    if has_more:
                        offset += limit
                    else:
                        print(
                            f"✓ Completado: Total de {len(all_items)} registros obtenidos de {endpoint}"
                        )
                else:
                    # No hay más items
                    has_more = False
                    if len(all_items) == 0:
                        print(
                            f"No se encontraron 'items' en la respuesta de {endpoint}"
                        )
                    else:
                        print(
                            f"✓ Completado: Total de {len(all_items)} registros obtenidos de {endpoint}"
                        )
            else:
                print(f"Error al obtener datos de {endpoint}: {response.status_code}")
                print(f"Respuesta: {response.text}")
                has_more = False

        # Convertir todos los items a DataFrame
        if all_items:
            df = pd.DataFrame(all_items)
            return df
        else:
            return pd.DataFrame()

    except Exception as e:
        print(f"Excepción al obtener datos de {endpoint}: {e}")
        return pd.DataFrame()


def fetch_peso_estancia_data() -> pd.DataFrame:
    """
    Obtiene datos de peso vs estancia desde Oracle ORDS.

    Returns:
        DataFrame con columnas: peso_espanol_apr, estancia_dias
    """
    df = fetch_ords_data("peso_vs_estancia")

    if not df.empty:
        # Convertir tipos de datos
        df["peso_espanol_apr"] = pd.to_numeric(df["peso_espanol_apr"], errors="coerce")
        df["estancia_dias"] = pd.to_numeric(df["estancia_dias"], errors="coerce")
        # Eliminar filas con valores nulos
        df = df.dropna()

    return df


def fetch_diagnosticos_data() -> pd.DataFrame:
    """
    Obtiene datos de diagnósticos, edad y mes de ingreso desde Oracle ORDS.

    Returns:
        DataFrame con columnas: nombre_enc, rango_de_edad, diagnostico_principal, mes_de_ingreso
    """
    df = fetch_ords_data("vista_muy_interesante")

    if not df.empty:
        # Limpiar datos si es necesario
        df = df.dropna(
            subset=["rango_de_edad", "diagnostico_principal", "mes_de_ingreso"]
        )

    return df


def fetch_diagnostico_sexo_data() -> pd.DataFrame:
    """
    Obtiene datos de diagnósticos principales vs sexo desde Oracle ORDS.

    Returns:
        DataFrame con columnas: diagnostico_principal, sexo, sexo_label
    """
    df = fetch_ords_data("diagnostico principal vs sexo")

    if not df.empty:
        # Convertir sexo a numérico y luego a categorías descriptivas
        df["sexo"] = pd.to_numeric(df["sexo"], errors="coerce")
        # Mapear 1=Masculino, 2=Femenino (según la convención común en bases de datos médicas)
        df["sexo_label"] = df["sexo"].map({1: "Masculino", 2: "Femenino"})
        # Eliminar filas con valores nulos
        df = df.dropna(subset=["diagnostico_principal", "sexo"])

    return df
