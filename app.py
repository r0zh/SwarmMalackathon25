"""
Dashboard de Análisis Hospitalario - Aplicación Principal
Versión 2.0 - Arquitectura Refactorizada
"""

import logging
from dash import Dash, html

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Importar módulos de la aplicación
from src.utils.config import Config
from src.data import get_data_loader
from src.layouts import (
    create_header,
    create_footer,
    create_main_metrics,
    create_diagnostics_section,
    create_gender_analysis_section,
    create_severity_section,
    create_weight_stay_section,
    create_insights_section,
)
from src.callbacks import register_callbacks

# Configuración de la aplicación
logger.info("Initializing Hospital Analytics Dashboard v2.0...")

# Inicializar la app con hojas de estilo y scripts personalizados
app = Dash(__name__, assets_folder="assets")
server = app.server

# Configurar el título de la página y meta tags
app.title = "Dashboard de Análisis Hospitalario"
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
        <meta name="description" content="Dashboard interactivo de análisis de datos hospitalarios">
        <meta name="theme-color" content="#1e293b">
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <!-- Google reCAPTCHA v3 -->
        <script src="https://www.google.com/recaptcha/api.js?render=6LeHfuwrAAAAAE-FOdiuq6iB9Wdbh5VRbWGBlwxK"></script>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

# Cargar datos al iniciar la aplicación
logger.info("Loading data from ORDS...")
data_loader = get_data_loader()

try:
    data = data_loader.fetch_all_data()
    df_peso_estancia = data["peso_estancia"]
    df_diagnosticos = data["diagnosticos"]
    df_diagnostico_sexo = data["diagnostico_sexo"]
    df_severidad_mortalidad = data["severidad_mortalidad"]

    logger.info(f"Data loaded successfully:")
    logger.info(f"  - Peso/Estancia: {len(df_peso_estancia)} records")
    logger.info(f"  - Diagnósticos: {len(df_diagnosticos)} records")
    logger.info(f"  - Diagnóstico/Sexo: {len(df_diagnostico_sexo)} records")
    logger.info(f"  - Severidad/Mortalidad: {len(df_severidad_mortalidad)} records")

    data_load_error = None

except Exception as e:
    logger.error(f"Error loading data: {e}")
    data_load_error = str(e)
    # Crear DataFrames vacíos en caso de error
    import pandas as pd

    df_peso_estancia = pd.DataFrame()
    df_diagnosticos = pd.DataFrame()
    df_diagnostico_sexo = pd.DataFrame()
    df_severidad_mortalidad = pd.DataFrame()

# Configurar tema por defecto
THEME = Config.DEFAULT_THEME

# Construir el layout de la aplicación
logger.info("Building application layout...")

app.layout = html.Div(
    [
        # Header
        create_header(),
        # Error notification (if any)
        html.Div(
            (
                [
                    html.Div(
                        [
                            html.Span(
                                "⚠️ ",
                                style={"fontSize": "1.5rem", "marginRight": "10px"},
                            ),
                            html.Span("Error al cargar datos: "),
                            html.Span(
                                data_load_error or "Error desconocido",
                                style={"fontWeight": "bold"},
                            ),
                            html.Br(),
                            html.Span(
                                "Mostrando dashboard con datos vacíos. Por favor, verifica la conexión a la base de datos.",
                                style={"fontSize": "0.9rem", "opacity": "0.9"},
                            ),
                        ],
                        style={
                            "backgroundColor": "#fef2f2",
                            "border": "2px solid #fecaca",
                            "borderLeft": "6px solid #dc2626",
                            "borderRadius": "8px",
                            "padding": "20px",
                            "margin": "0 24px 24px 24px",
                            "color": "#991b1b",
                            "boxShadow": "0 4px 12px rgba(220, 38, 38, 0.1)",
                        },
                        role="alert",
                    )
                ]
                if data_load_error
                else []
            ),
        ),
        # Main content container
        html.Div(
            [
                # KPIs principales
                create_main_metrics(
                    df_diagnosticos=df_diagnosticos,
                    df_peso_estancia=df_peso_estancia,
                    df_severidad=df_severidad_mortalidad,
                ),
                # Sección 1: Diagnósticos y Demografía
                create_diagnostics_section(df=df_diagnosticos, theme=THEME),
                # Sección 2: Análisis por Sexo
                create_gender_analysis_section(df=df_diagnostico_sexo, theme=THEME),
                # Sección 3: Severidad y Mortalidad
                create_severity_section(df=df_severidad_mortalidad, theme=THEME),
                # Sección 4: Peso y Estancia
                create_weight_stay_section(df=df_peso_estancia, theme=THEME),
                # Sección 5: Insights
                create_insights_section(
                    df_diagnosticos=df_diagnosticos,
                    df_severidad=df_severidad_mortalidad,
                    df_peso=df_peso_estancia,
                ),
            ],
            className="container",
        ),
        # Footer
        create_footer(),
    ]
)

# Registrar callbacks
register_callbacks(app)

logger.info("Application initialization complete!")

# Punto de entrada para ejecución
if __name__ == "__main__":
    logger.info(f"Starting server on {Config.HOST}:{Config.PORT}...")
    app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)
