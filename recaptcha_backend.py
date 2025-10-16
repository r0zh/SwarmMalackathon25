"""
Backend para verificar tokens de reCAPTCHA Enterprise
Ejemplo de implementación con Flask/Dash

Para usar esto, necesitarás:
1. pip install google-cloud-recaptcha-enterprise
2. Configurar las credenciales de Google Cloud
3. Añadir los callbacks necesarios en tu app.py
"""

from google.cloud import recaptchaenterprise_v1
from google.cloud.recaptchaenterprise_v1 import Assessment
import os


class RecaptchaVerifier:
    """
    Clase para verificar tokens de reCAPTCHA Enterprise
    """
    
    def __init__(self, project_id: str, recaptcha_site_key: str):
        """
        Inicializar el verificador de reCAPTCHA
        
        Args:
            project_id: ID del proyecto de Google Cloud
            recaptcha_site_key: Clave del sitio de reCAPTCHA
        """
        self.project_id = project_id
        self.recaptcha_site_key = recaptcha_site_key
        self.client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()
    
    def create_assessment(
        self, token: str, recaptcha_action: str
    ) -> Assessment:
        """
        Crear una evaluación de reCAPTCHA
        
        Args:
            token: Token generado por reCAPTCHA en el frontend
            recaptcha_action: Acción que se está verificando
            
        Returns:
            Assessment con el resultado de la verificación
        """
        # Preparar el request
        event = recaptchaenterprise_v1.Event()
        event.site_key = self.recaptcha_site_key
        event.token = token
        event.expected_action = recaptcha_action
        
        assessment = recaptchaenterprise_v1.Assessment()
        assessment.event = event
        
        project_name = f"projects/{self.project_id}"
        
        # Crear el assessment
        request = recaptchaenterprise_v1.CreateAssessmentRequest()
        request.assessment = assessment
        request.parent = project_name
        
        response = self.client.create_assessment(request)
        
        return response
    
    def verify_token(
        self, 
        token: str, 
        recaptcha_action: str,
        min_score: float = 0.5
    ) -> dict:
        """
        Verificar un token de reCAPTCHA y devolver el resultado
        
        Args:
            token: Token de reCAPTCHA
            recaptcha_action: Acción esperada
            min_score: Score mínimo aceptable (0.0 - 1.0)
            
        Returns:
            dict con los resultados de la verificación
        """
        try:
            assessment = self.create_assessment(token, recaptcha_action)
            
            # Verificar que el token sea válido
            if not assessment.token_properties.valid:
                return {
                    'success': False,
                    'error': 'Token inválido',
                    'reason': assessment.token_properties.invalid_reason.name
                }
            
            # Verificar que la acción coincida
            if assessment.token_properties.action != recaptcha_action:
                return {
                    'success': False,
                    'error': 'Acción no coincide',
                    'expected': recaptcha_action,
                    'received': assessment.token_properties.action
                }
            
            # Obtener el score de riesgo
            score = assessment.risk_analysis.score
            
            # Verificar el score
            if score < min_score:
                return {
                    'success': False,
                    'error': 'Score muy bajo (posible bot)',
                    'score': score,
                    'min_score': min_score,
                    'reasons': [reason.name for reason in assessment.risk_analysis.reasons]
                }
            
            return {
                'success': True,
                'score': score,
                'action': assessment.token_properties.action,
                'create_time': assessment.token_properties.create_time.timestamp()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error en verificación: {str(e)}'
            }


# Ejemplo de uso con Dash
"""
from dash import Dash, Input, Output, State, html, callback
import dash

app = Dash(__name__)

# Inicializar el verificador
recaptcha = RecaptchaVerifier(
    project_id="tu-proyecto-id",
    recaptcha_site_key="6LeHfuwrAAAAAE-FOdiuq6iB9Wdbh5VRbWGBlwxK"
)

@callback(
    Output('verification-result', 'children'),
    Input('submit-button', 'n_clicks'),
    State('recaptcha-token', 'value'),
    prevent_initial_call=True
)
def verify_user_action(n_clicks, token):
    if not token:
        return "Error: No se proporcionó token"
    
    result = recaptcha.verify_token(
        token=token,
        recaptcha_action='LOGIN',
        min_score=0.5
    )
    
    if result['success']:
        return f"✅ Verificación exitosa. Score: {result['score']}"
    else:
        return f"❌ Verificación fallida: {result.get('error', 'Error desconocido')}"
"""


# Configuración para usar con Flask/Dash
def setup_recaptcha_routes(server):
    """
    Configurar rutas para verificar reCAPTCHA en un servidor Flask/Dash
    
    Args:
        server: Instancia del servidor Flask (app.server en Dash)
    """
    from flask import request, jsonify
    
    # Configurar el verificador
    recaptcha = RecaptchaVerifier(
        project_id=os.getenv('GOOGLE_CLOUD_PROJECT_ID', 'tu-proyecto-id'),
        recaptcha_site_key='6LeHfuwrAAAAAE-FOdiuq6iB9Wdbh5VRbWGBlwxK'
    )
    
    @server.route('/api/verify-recaptcha', methods=['POST'])
    def verify_recaptcha():
        """Endpoint para verificar tokens de reCAPTCHA"""
        data = request.get_json()
        
        if not data or 'token' not in data:
            return jsonify({
                'success': False,
                'error': 'Token no proporcionado'
            }), 400
        
        token = data['token']
        action = data.get('action', 'UNKNOWN')
        
        result = recaptcha.verify_token(
            token=token,
            recaptcha_action=action,
            min_score=0.5
        )
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code


# Instrucciones de uso
USAGE_INSTRUCTIONS = """
=== CÓMO USAR reCAPTCHA ENTERPRISE ===

1. INSTALACIÓN:
   pip install google-cloud-recaptcha-enterprise

2. CONFIGURACIÓN:
   - Crear proyecto en Google Cloud Console
   - Habilitar reCAPTCHA Enterprise API
   - Crear credenciales de servicio
   - Descargar el archivo JSON de credenciales
   
3. VARIABLES DE ENTORNO:
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
   export GOOGLE_CLOUD_PROJECT_ID="tu-proyecto-id"

4. INTEGRACIÓN EN app.py:
   
   from recaptcha_backend import setup_recaptcha_routes
   
   app = Dash(__name__)
   server = app.server
   
   # Configurar rutas de verificación
   setup_recaptcha_routes(server)

5. FRONTEND:
   El archivo recaptcha.js ya está configurado para:
   - Cargar reCAPTCHA automáticamente
   - Generar tokens en diferentes acciones
   - Enviar tokens al backend (descomentar sendTokenToBackend)

6. VERIFICACIÓN:
   Los tokens se generan automáticamente y se pueden verificar
   en el backend usando el endpoint /api/verify-recaptcha

=== ACCIONES CONFIGURADAS ===

- PAGE_LOAD: Al cargar la página
- METRIC_CARD_CLICK: Al hacer clic en tarjetas de métricas
- DROPDOWN_INTERACTION: Al usar el dropdown de métricas
- ACCESSIBILITY_TOGGLE: Al cambiar configuración de accesibilidad
- THEME_TOGGLE: Al cambiar el tema (claro/oscuro)
- LOGIN: Para autenticación (personalizable)

=== SCORES ===

Los scores van de 0.0 (muy probable bot) a 1.0 (muy probable humano):
- 0.0 - 0.3: Bot probable
- 0.3 - 0.5: Sospechoso
- 0.5 - 0.7: Normal
- 0.7 - 1.0: Usuario confiable

El score mínimo recomendado es 0.5
"""

if __name__ == "__main__":
    print(USAGE_INSTRUCTIONS)
