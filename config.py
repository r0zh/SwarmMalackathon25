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


# Validar configuración al importar el módulo
Config.validate()
