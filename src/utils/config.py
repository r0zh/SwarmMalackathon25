"""
Configuración centralizada para la aplicación.
Carga y valida las variables de entorno necesarias.
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class Config:
    """Clase de configuración para la aplicación"""

    # Oracle ORDS Configuration
    ORDS_BASE_URL = os.getenv("ORDS_BASE_URL")
    ORDS_USERNAME = os.getenv("ORDS_USERNAME")
    ORDS_PASSWORD = os.getenv("ORDS_PASSWORD")

    # App Configuration
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8050"))

    # Data Configuration
    DEFAULT_LIMIT = int(os.getenv("DEFAULT_LIMIT", "20000"))
    CACHE_TIMEOUT = int(os.getenv("CACHE_TIMEOUT", "300"))  # 5 minutes default

    # Theme Configuration
    DEFAULT_THEME = os.getenv("DEFAULT_THEME", "dark")  # "dark" or "light"

    @classmethod
    def validate(cls):
        """Valida que todas las variables de entorno requeridas estén configuradas"""
        required_vars = ["ORDS_BASE_URL", "ORDS_USERNAME", "ORDS_PASSWORD"]
        missing_vars = []

        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)

        if missing_vars:
            raise ValueError(
                f"Faltan las siguientes variables de entorno requeridas: {', '.join(missing_vars)}\n"
                f"Por favor, copia .env.example a .env y configura las variables necesarias."
            )

    @classmethod
    def get_ords_config(cls):
        """Retorna la configuración de Oracle ORDS como diccionario"""
        return {
            "base_url": cls.ORDS_BASE_URL,
            "username": cls.ORDS_USERNAME,
            "password": cls.ORDS_PASSWORD,
        }


# Validar configuración al importar el módulo
Config.validate()
