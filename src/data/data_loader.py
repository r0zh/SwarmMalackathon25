"""
Cargador de datos con caché y procesamiento.
Obtiene datos desde ORDS y los procesa en DataFrames.
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict
import logging

from .ords_client import ORDSClient
from ..utils.config import Config

logger = logging.getLogger(__name__)


class DataLoader:
    """Gestor de carga de datos con caché en memoria"""

    def __init__(self, client: Optional[ORDSClient] = None):
        """
        Inicializa el cargador de datos.

        Args:
            client: Cliente ORDS (si no se proporciona, se crea uno nuevo)
        """
        if client is None:
            ords_config = Config.get_ords_config()
            client = ORDSClient(**ords_config)

        self.client = client
        self._cache: Dict[str, Dict] = {}
        self.cache_timeout = Config.CACHE_TIMEOUT

    def _is_cache_valid(self, key: str) -> bool:
        """
        Verifica si el caché para una clave es válido.

        Args:
            key: Clave del caché

        Returns:
            bool: True si el caché es válido
        """
        if key not in self._cache:
            return False

        cache_entry = self._cache[key]
        timestamp = cache_entry.get("timestamp")

        if timestamp is None:
            return False

        age = (datetime.now() - timestamp).total_seconds()
        return age < self.cache_timeout

    def _get_from_cache(self, key: str) -> Optional[pd.DataFrame]:
        """
        Obtiene datos del caché si están disponibles.

        Args:
            key: Clave del caché

        Returns:
            DataFrame o None si no está en caché
        """
        if self._is_cache_valid(key):
            logger.debug(f"Cache hit for {key}")
            return self._cache[key]["data"]
        return None

    def _save_to_cache(self, key: str, data: pd.DataFrame):
        """
        Guarda datos en el caché.

        Args:
            key: Clave del caché
            data: DataFrame a guardar
        """
        self._cache[key] = {"data": data.copy(), "timestamp": datetime.now()}
        logger.debug(f"Saved to cache: {key}")

    def clear_cache(self, key: Optional[str] = None):
        """
        Limpia el caché.

        Args:
            key: Clave específica a limpiar (None = limpiar todo)
        """
        if key is None:
            self._cache.clear()
            logger.info("Cleared entire cache")
        elif key in self._cache:
            del self._cache[key]
            logger.info(f"Cleared cache for: {key}")

    def _fetch_and_process(self, endpoint: str, processor_func=None) -> pd.DataFrame:
        """
        Obtiene datos de un endpoint y opcionalmente los procesa.

        Args:
            endpoint: Nombre del endpoint
            processor_func: Función para procesar el DataFrame (opcional)

        Returns:
            DataFrame procesado
        """
        # Verificar caché
        cache_key = f"endpoint_{endpoint}"
        cached_data = self._get_from_cache(cache_key)

        if cached_data is not None:
            return cached_data

        # Obtener datos desde ORDS
        items = self.client.fetch_endpoint(endpoint, limit=Config.DEFAULT_LIMIT)

        if not items:
            logger.warning(f"No data returned from {endpoint}")
            return pd.DataFrame()

        # Convertir a DataFrame
        df = pd.DataFrame(items)

        # Aplicar procesador si existe
        if processor_func is not None:
            df = processor_func(df)

        # Guardar en caché
        self._save_to_cache(cache_key, df)

        return df

    # ========== Métodos específicos para cada endpoint ==========

    def fetch_peso_estancia_data(self) -> pd.DataFrame:
        """
        Obtiene datos de peso vs estancia desde Oracle ORDS.

        Returns:
            DataFrame con columnas: peso_espanol_apr, estancia_dias
        """

        def process(df: pd.DataFrame) -> pd.DataFrame:
            if df.empty:
                return df

            # Convertir tipos de datos
            df["peso_espanol_apr"] = pd.to_numeric(
                df["peso_espanol_apr"], errors="coerce"
            )
            df["estancia_dias"] = pd.to_numeric(df["estancia_dias"], errors="coerce")

            # Eliminar filas con valores nulos
            df = df.dropna()

            return df

        return self._fetch_and_process("peso_vs_estancia", process)

    def fetch_diagnosticos_data(self) -> pd.DataFrame:
        """
        Obtiene datos de diagnósticos, edad y mes de ingreso desde Oracle ORDS.

        Returns:
            DataFrame con columnas: nombre_enc, rango_de_edad, diagnostico_principal, mes_de_ingreso
        """

        def process(df: pd.DataFrame) -> pd.DataFrame:
            if df.empty:
                return df

            # Limpiar datos eliminando filas con valores nulos en columnas críticas
            df = df.dropna(
                subset=["rango_de_edad", "diagnostico_principal", "mes_de_ingreso"]
            )

            return df

        return self._fetch_and_process("vista_muy_interesante", process)

    def fetch_diagnostico_sexo_data(self) -> pd.DataFrame:
        """
        Obtiene datos de diagnósticos principales vs sexo desde Oracle ORDS.

        Returns:
            DataFrame con columnas: diagnostico_principal, sexo, sexo_label
        """

        def process(df: pd.DataFrame) -> pd.DataFrame:
            if df.empty:
                return df

            # Convertir sexo a numérico
            df["sexo"] = pd.to_numeric(df["sexo"], errors="coerce")

            # Mapear 1=Masculino, 2=Femenino
            df["sexo_label"] = df["sexo"].map({1: "Masculino", 2: "Femenino"})

            # Eliminar filas con valores nulos
            df = df.dropna(subset=["diagnostico_principal", "sexo"])

            return df

        return self._fetch_and_process("diagnostico principal vs sexo", process)

    def fetch_severidad_mortalidad_data(self) -> pd.DataFrame:
        """
        Obtiene datos de severidad APR vs mortalidad APR desde Oracle ORDS.

        Returns:
            DataFrame con columnas: nivel_severidad_apr, riesgo_mortalidad_apr,
                                    severidad_label, mortalidad_label
        """

        def process(df: pd.DataFrame) -> pd.DataFrame:
            if df.empty:
                return df

            # Convertir a numérico
            df["nivel_severidad_apr"] = pd.to_numeric(
                df["nivel_severidad_apr"], errors="coerce"
            )
            df["riesgo_mortalidad_apr"] = pd.to_numeric(
                df["riesgo_mortalidad_apr"], errors="coerce"
            )

            # Mapear niveles a etiquetas descriptivas
            severidad_map = {1: "Leve", 2: "Moderado", 3: "Grave", 4: "Extremo"}
            df["severidad_label"] = df["nivel_severidad_apr"].map(severidad_map)

            mortalidad_map = {1: "Bajo", 2: "Moderado", 3: "Alto", 4: "Extremo"}
            df["mortalidad_label"] = df["riesgo_mortalidad_apr"].map(mortalidad_map)

            # Eliminar filas con valores nulos
            df = df.dropna(subset=["nivel_severidad_apr", "riesgo_mortalidad_apr"])

            return df

        return self._fetch_and_process("severidad_apr vs mortadilad_apr", process)

    def fetch_all_data(self) -> Dict[str, pd.DataFrame]:
        """
        Obtiene todos los datos de una vez.

        Returns:
            Dict con todos los DataFrames
        """
        logger.info("Fetching all datasets...")

        return {
            "peso_estancia": self.fetch_peso_estancia_data(),
            "diagnosticos": self.fetch_diagnosticos_data(),
            "diagnostico_sexo": self.fetch_diagnostico_sexo_data(),
            "severidad_mortalidad": self.fetch_severidad_mortalidad_data(),
        }


# Instancia global del data loader (singleton pattern)
_data_loader_instance: Optional[DataLoader] = None


def get_data_loader() -> DataLoader:
    """
    Obtiene la instancia global del DataLoader (patrón Singleton).

    Returns:
        DataLoader: Instancia del cargador de datos
    """
    global _data_loader_instance

    if _data_loader_instance is None:
        _data_loader_instance = DataLoader()

    return _data_loader_instance
