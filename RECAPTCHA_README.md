# 🔐 Integración de reCAPTCHA Enterprise

## ✅ Estado Actual

**reCAPTCHA Enterprise está integrado en el frontend** y listo para usar.

### Archivos Modificados/Creados:

1. **`app.py`** - Script de reCAPTCHA añadido en el `<head>`
2. **`assets/recaptcha.js`** - Lógica de reCAPTCHA en el frontend
3. **`recaptcha_backend.py`** - Código de verificación del backend (opcional)

---

## 🚀 Uso Actual (Solo Frontend)

El reCAPTCHA ya está funcionando automáticamente:

### Acciones Monitoreadas:
- ✅ **PAGE_LOAD** - Al cargar la página
- ✅ **METRIC_CARD_CLICK** - Al hacer clic en tarjetas de métricas
- ✅ **DROPDOWN_INTERACTION** - Al usar el dropdown
- ✅ **ACCESSIBILITY_TOGGLE** - Al abrir panel de accesibilidad
- ✅ **THEME_TOGGLE** - Al cambiar tema oscuro/claro

### Verificar que funciona:
1. Ejecuta la aplicación: `uv run python app.py`
2. Abre la consola del navegador (F12)
3. Deberías ver mensajes como:
   ```
   ✅ reCAPTCHA Enterprise cargado correctamente
   ✅ reCAPTCHA token generado para acción: PAGE_LOAD
   ```

---

## 🔧 Configuración Backend (Opcional)

Si quieres **verificar los tokens en el servidor**, sigue estos pasos:

### 1. Instalar Dependencias

```bash
pip install google-cloud-recaptcha-enterprise
# o con uv:
uv add google-cloud-recaptcha-enterprise
```

### 2. Configurar Google Cloud

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea o selecciona un proyecto
3. Habilita **reCAPTCHA Enterprise API**
4. Ve a **Credenciales** → **Crear credenciales** → **Cuenta de servicio**
5. Descarga el archivo JSON de credenciales

### 3. Configurar Variables de Entorno

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/ruta/a/tu/credenciales.json"
export GOOGLE_CLOUD_PROJECT_ID="tu-proyecto-id"
```

En Windows (PowerShell):
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\ruta\a\tu\credenciales.json"
$env:GOOGLE_CLOUD_PROJECT_ID="tu-proyecto-id"
```

### 4. Integrar Backend en app.py

Añade esto al final de tu `app.py`:

```python
from recaptcha_backend import setup_recaptcha_routes

# Después de crear la app
app = Dash(__name__, assets_folder="assets")
server = app.server

# Configurar rutas de verificación
setup_recaptcha_routes(server)
```

### 5. Activar Verificación en Frontend

En `assets/recaptcha.js`, descomenta la línea en la función `executeRecaptcha`:

```javascript
// Cambiar:
// Por ejemplo: await sendTokenToBackend(token, action);

// A:
await sendTokenToBackend(token, action);
```

---

## 📊 Entender los Scores

reCAPTCHA asigna un score de 0.0 a 1.0:

| Score | Interpretación |
|-------|---------------|
| 0.0 - 0.3 | 🤖 Bot probable |
| 0.3 - 0.5 | ⚠️ Sospechoso |
| 0.5 - 0.7 | ✅ Normal |
| 0.7 - 1.0 | ⭐ Usuario confiable |

**Score mínimo recomendado: 0.5**

---

## 🔍 Testing

### Verificar en Consola del Navegador:

```javascript
// Obtener un token manualmente
const token = await window.getRecaptchaToken('TEST_ACTION');
console.log('Token:', token);
```

### Verificar en Backend:

```bash
curl -X POST http://localhost:8050/api/verify-recaptcha \
  -H "Content-Type: application/json" \
  -d '{"token":"TOKEN_AQUI","action":"PAGE_LOAD"}'
```

---

## 📝 Personalización

### Añadir Nueva Acción:

En `assets/recaptcha.js`:

```javascript
// Ejemplo: Verificar al enviar un formulario
document.getElementById('mi-formulario').addEventListener('submit', async function(e) {
    e.preventDefault();
    const token = await executeRecaptcha('FORM_SUBMIT');
    
    if (token) {
        // Enviar formulario con el token
        this.submit();
    }
});
```

### Cambiar Score Mínimo:

En `recaptcha_backend.py`, método `verify_token`:

```python
result = recaptcha.verify_token(
    token=token,
    recaptcha_action=action,
    min_score=0.7  # Cambiar aquí (0.0 - 1.0)
)
```

---

## 🛡️ Seguridad

### ⚠️ Importante:

1. **NUNCA** expongas tu **Secret Key** en el código del cliente
2. La **Site Key** (6LeHfuwrAAAAAE-FOdiuq6iB9Wdbh5VRbWGBlwxK) es pública y está bien en el frontend
3. **SIEMPRE** verifica los tokens en el backend para producción
4. No confíes solo en la verificación del frontend

### Para Producción:

- Habilita verificación backend
- Configura límites de tasa (rate limiting)
- Monitorea los scores en Google Cloud Console
- Ajusta el score mínimo según tus necesidades

---

## 📚 Recursos

- [Documentación reCAPTCHA Enterprise](https://cloud.google.com/recaptcha-enterprise/docs)
- [Mejores prácticas](https://cloud.google.com/recaptcha-enterprise/docs/best-practices)
- [Interpretar scores](https://cloud.google.com/recaptcha-enterprise/docs/interpret-assessment)

---

## ✨ Resumen Rápido

**Ya funciona en frontend:**
- ✅ Script cargado en `<head>`
- ✅ Tokens generándose automáticamente
- ✅ Múltiples acciones monitoreadas
- ✅ Consola con logs informativos

**Para producción (opcional):**
1. Instalar `google-cloud-recaptcha-enterprise`
2. Configurar credenciales de Google Cloud
3. Integrar `recaptcha_backend.py`
4. Activar verificación en `recaptcha.js`

---

¿Necesitas ayuda? Revisa la consola del navegador para ver los logs de reCAPTCHA.
