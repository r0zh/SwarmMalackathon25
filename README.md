# Dashboard de Análisis Hospitalario

Dashboard interactivo para análisis de datos hospitalarios usando Dash y Oracle ORDS.

## 🚀 Configuración

### Requisitos Previos
- Python 3.13+
- UV (gestor de paquetes)

### Instalación

1. Clona el repositorio:
```bash
git clone <tu-repositorio>
cd Malackathon
```

2. Instala las dependencias:
```bash
uv sync
```

3. Configura las variables de entorno:
```bash
cp .env.example .env
```

4. Edita el archivo `.env` con tus credenciales de Oracle ORDS:
```env
ORDS_BASE_URL=https://tu-instancia.oraclecloudapps.com/ords/admin
ORDS_USERNAME=tu_usuario
ORDS_PASSWORD=tu_contraseña
```

### Ejecución

Para ejecutar la aplicación en modo desarrollo:
```bash
uv run app.py
```

O con Gunicorn en producción:
```bash
gunicorn app:server
```

La aplicación estará disponible en `http://localhost:8050`

## 📊 Características

- **Análisis en tiempo real**: Datos obtenidos directamente desde Oracle ORDS
- **Visualizaciones interactivas**: Gráficos y tablas con Plotly
- **Datos de Peso vs Estancia**: Análisis de la relación entre peso APR-GRD y días de estancia hospitalaria
- **Responsive**: Diseño adaptado para diferentes dispositivos

## 🔒 Seguridad

- Las credenciales se almacenan en variables de entorno (archivo `.env`)
- El archivo `.env` está incluido en `.gitignore` y no se sube al repositorio
- Usa `.env.example` como plantilla para configurar tu entorno local

### Cifrado de Nombres de Pacientes

Los nombres de pacientes están cifrados con **AES-256**. Se puede hacer decrypt con el nombre cifrado y la clave:

**Clave de cifrado:**
```
QwV1^-LRj-[6_YzJ$/zDOKub"!YeJjA2
```

## 📁 Estructura del Proyecto

```
.
├── app.py                 # Aplicación principal de Dash
├── config.py             # Configuración centralizada
├── ords_utils.py         # Utilidades para API de Oracle ORDS
├── .env                  # Variables de entorno (no versionado)
├── .env.example          # Plantilla de variables de entorno
├── pyproject.toml        # Dependencias del proyecto
├── gunicorn.conf.py      # Configuración de Gunicorn
├── assets/               # Archivos estáticos (CSS, JS)
│   ├── custom.js
│   ├── recaptcha.js
│   └── style.css
└── README.md            # Este archivo
```

## 🛠️ Desarrollo

### Añadir nuevas visualizaciones de datos

1. **Opción 1 - Usar la función genérica** (Recomendado):
   ```python
   from ords_utils import fetch_ords_data
   
   # Obtener datos de un nuevo endpoint
   df = fetch_ords_data("nombre_endpoint")
   ```

2. **Opción 2 - Crear función específica** en `ords_utils.py`:
   ```python
   def fetch_mi_nuevo_dato() -> pd.DataFrame:
       df = fetch_ords_data("mi_endpoint")
       # Procesar datos específicos aquí
       return df
   ```

3. Añade los componentes visuales en el layout de `app.py`

### Archivos principales

- **`config.py`**: Gestión centralizada de variables de entorno
- **`ords_utils.py`**: Funciones reutilizables para conectarse a Oracle ORDS
- **`app.py`**: Layout y lógica de la aplicación Dash

## 📝 Licencia

© 2025 Dashboard de Análisis Hospitalario
