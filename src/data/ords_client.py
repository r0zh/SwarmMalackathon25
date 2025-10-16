"""
Cliente para interactuar con la API de Oracle ORDS.
Maneja la comunicación HTTP y paginación.
"""

import requests
from requests.auth import HTTPBasicAuth
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class ORDSClient:
    """Cliente para Oracle ORDS API con soporte de paginación"""

    def __init__(self, base_url: str, username: str, password: str):
        """
        Inicializa el cliente ORDS.

        Args:
            base_url: URL base de la API ORDS
            username: Usuario para autenticación
            password: Contraseña para autenticación
        """
        self.base_url = base_url.rstrip("/")
        self.auth = HTTPBasicAuth(username, password)
        self.headers = {"Content-Type": "application/json"}

    def fetch_endpoint(
        self, endpoint: str, limit: int = 20000, max_records: Optional[int] = None
    ) -> List[Dict]:
        """
        Obtiene datos de un endpoint de ORDS con paginación automática.

        Args:
            endpoint: Nombre del endpoint (ej: "peso_vs_estancia")
            limit: Registros por página (default: 20000)
            max_records: Máximo total de registros a obtener (None = todos)

        Returns:
            List[Dict]: Lista de todos los registros obtenidos
        """
        url = f"{self.base_url}/{endpoint}/"
        all_items = []
        offset = 0
        has_more = True

        logger.info(f"Fetching data from endpoint: {endpoint}")

        try:
            while has_more:
                # Construir URL con parámetros de paginación
                params_url = f"{url}?limit={limit}&offset={offset}"

                response = requests.get(
                    params_url,
                    auth=self.auth,
                    headers=self.headers,
                    timeout=30,  # 30 seconds timeout
                )

                if response.status_code != 200:
                    logger.error(
                        f"Error fetching {endpoint}: {response.status_code} - {response.text}"
                    )
                    break

                data = response.json()

                # Verificar si hay items en la respuesta
                if "items" not in data or len(data["items"]) == 0:
                    has_more = False
                    if len(all_items) == 0:
                        logger.warning(f"No items found in response from {endpoint}")
                    break

                # Añadir items
                items = data["items"]
                all_items.extend(items)

                logger.debug(
                    f"  → Fetched {len(items)} records " f"(Total: {len(all_items)})"
                )

                # Verificar si hemos alcanzado el límite
                if max_records and len(all_items) >= max_records:
                    all_items = all_items[:max_records]
                    has_more = False
                    logger.info(f"Reached max_records limit: {max_records}")
                    break

                # Verificar si hay más datos
                has_more = data.get("hasMore", False)

                if has_more:
                    offset += limit
                else:
                    logger.info(
                        f"✓ Completed: {len(all_items)} total records from {endpoint}"
                    )

        except requests.exceptions.RequestException as e:
            logger.error(f"Request exception for {endpoint}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error fetching {endpoint}: {e}")

        return all_items

    def test_connection(self) -> bool:
        """
        Prueba la conexión con el servidor ORDS.

        Returns:
            bool: True si la conexión es exitosa
        """
        try:
            response = requests.get(
                self.base_url, auth=self.auth, headers=self.headers, timeout=10
            )
            return response.status_code in [
                200,
                401,
            ]  # 401 = autenticación requerida (pero servidor accesible)
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
