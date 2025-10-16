from dash import Dash, html, dcc, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from ords_utils import (
    fetch_peso_estancia_data,
    fetch_diagnosticos_data,
    fetch_diagnostico_sexo_data,
    fetch_severidad_mortalidad_data,
)


# Función helper para aplicar tema oscuro a los gráficos
def apply_dark_theme(fig):
    """
    Aplica el tema oscuro consistente a todas las figuras de Plotly.
    Nota: Este tema se aplica en la carga inicial. Los cambios posteriores
    se manejan con CSS.
    """
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",  # Transparente para que CSS lo controle
        plot_bgcolor="rgba(0,0,0,0.02)",
        font=dict(color="#e2e8f0", family="Inter, system-ui, sans-serif"),
        title_font=dict(color="#f1f5f9", size=16),
    )
    return fig


def apply_light_theme(fig):
    """
    Aplica el tema claro consistente a todas las figuras de Plotly.
    Nota: Este tema se aplica en la carga inicial. Los cambios posteriores
    se manejan con CSS.
    """
    fig.update_layout(
        template="plotly",
        paper_bgcolor="rgba(255,255,255,0)",  # Transparente para que CSS lo controle
        plot_bgcolor="rgba(248,250,252,0.5)",
        font=dict(color="#1e293b", family="Inter, system-ui, sans-serif"),
        title_font=dict(color="#0f172a", size=16),
    )
    return fig


# Inicializar la app con hojas de estilo y scripts personalizados
app = Dash(__name__, assets_folder="assets")

# Obtener datos reales al inicio
df_peso_estancia = fetch_peso_estancia_data()
df_diagnosticos = fetch_diagnosticos_data()
df_diagnostico_sexo = fetch_diagnostico_sexo_data()
df_severidad_mortalidad = fetch_severidad_mortalidad_data()

# Configurar el título de la página y meta tags para responsividad
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

# Layout de la aplicación con HTML personalizado
app.layout = html.Div(
    [
        # Skip to main content link (para navegación por teclado)
        html.A(
            "Saltar al contenido principal",
            href="#main-content",
            className="skip-link",
            style={
                "position": "absolute",
                "left": "-9999px",
                "zIndex": "999",
                "padding": "1em",
                "backgroundColor": "#2563eb",
                "color": "white",
                "textDecoration": "none",
                "fontWeight": "bold",
            },
            **{
                "data-skip-link": "true",
                "tabIndex": "1",
            },
        ),
        # Header
        html.Header(
            [
                html.H1(
                    "Dashboard de Análisis Hospitalario",
                    className="header-title",
                    **{
                        "aria-label": "Dashboard de Análisis Hospitalario - Página principal",
                        "role": "banner",
                    },
                ),
                html.P(
                    "Análisis de datos hospitalarios y métricas de estancia",
                    className="subtitle",
                    **{
                        "aria-label": "Descripción: Análisis de datos hospitalarios y métricas de estancia"
                    },
                ),
                html.P(
                    "Datos en tiempo real · Análisis · Insights",
                    className="subtitle",
                    style={
                        "fontSize": "0.9rem",
                        "marginTop": "15px",
                        "opacity": "0.85",
                        "fontStyle": "italic",
                    },
                    **{
                        "aria-label": "Características: Datos en tiempo real, Análisis e Insights"
                    },
                ),
            ],
            className="header",
            **{"role": "banner"},
        ),
        # Main content empieza aquí - Resumen Ejecutivo
        html.Div(
            id="main-content",
            children=[
                # KPIs principales
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    "📊",
                                    className="metric-icon",
                                    style={"fontSize": "2.5rem"},
                                ),
                                html.H3("Total de Casos"),
                                html.H2(
                                    f"{len(df_diagnosticos):,}"
                                    if not df_diagnosticos.empty
                                    else "N/A",
                                    className="metric-value",
                                    style={"color": "#2563eb"},
                                ),
                                html.P(
                                    "Registros analizados",
                                    style={"fontSize": "0.9rem", "opacity": "0.7"},
                                ),
                            ],
                            className="metric-card",
                            style={
                                "backgroundColor": "#eff6ff",
                                "border": "2px solid #bfdbfe",
                                "borderRadius": "12px",
                                "padding": "20px",
                                "textAlign": "center",
                            },
                        ),
                        html.Div(
                            [
                                html.Div(
                                    "⚕️",
                                    className="metric-icon",
                                    style={"fontSize": "2.5rem"},
                                ),
                                html.H3("Estancia Media"),
                                html.H2(
                                    f"{df_peso_estancia['estancia_dias'].mean():.1f}"
                                    if not df_peso_estancia.empty
                                    else "N/A",
                                    className="metric-value",
                                    style={"color": "#16a34a"},
                                ),
                                html.P(
                                    "Días promedio",
                                    style={"fontSize": "0.9rem", "opacity": "0.7"},
                                ),
                            ],
                            className="metric-card",
                            style={
                                "backgroundColor": "#f0fdf4",
                                "border": "2px solid #bbf7d0",
                                "borderRadius": "12px",
                                "padding": "20px",
                                "textAlign": "center",
                            },
                        ),
                        html.Div(
                            [
                                html.Div(
                                    "🔴",
                                    className="metric-icon",
                                    style={"fontSize": "2.5rem"},
                                ),
                                html.H3("Casos Graves"),
                                html.H2(
                                    f"{((df_severidad_mortalidad['nivel_severidad_apr'] >= 3).sum() if not df_severidad_mortalidad.empty else 0):,}"
                                    if not df_severidad_mortalidad.empty
                                    else "N/A",
                                    className="metric-value",
                                    style={"color": "#dc2626"},
                                ),
                                html.P(
                                    "Severidad grave/extrema",
                                    style={"fontSize": "0.9rem", "opacity": "0.7"},
                                ),
                            ],
                            className="metric-card",
                            style={
                                "backgroundColor": "#fef2f2",
                                "border": "2px solid #fecaca",
                                "borderRadius": "12px",
                                "padding": "20px",
                                "textAlign": "center",
                            },
                        ),
                        html.Div(
                            [
                                html.Div(
                                    "🏥",
                                    className="metric-icon",
                                    style={"fontSize": "2.5rem"},
                                ),
                                html.H3("Diagnósticos"),
                                html.H2(
                                    f"{df_diagnosticos['diagnostico_principal'].nunique():,}"
                                    if not df_diagnosticos.empty
                                    else "N/A",
                                    className="metric-value",
                                    style={"color": "#7c3aed"},
                                ),
                                html.P(
                                    "Condiciones únicas",
                                    style={"fontSize": "0.9rem", "opacity": "0.7"},
                                ),
                            ],
                            className="metric-card",
                            style={
                                "backgroundColor": "#faf5ff",
                                "border": "2px solid #e9d5ff",
                                "borderRadius": "12px",
                                "padding": "20px",
                                "textAlign": "center",
                            },
                        ),
                    ],
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
                        "gap": "20px",
                        "marginBottom": "40px",
                    },
                )
            ],
            className="metrics-grid",
            role="region",
            **{"aria-label": "Contenido principal"},
        ),
        # Sección 1: Análisis de Diagnósticos y Demografía
        html.Div(
            [
                html.H3(
                    "1️⃣ Análisis de Diagnósticos y Demografía",
                    className="chart-title",
                ),
                html.P(
                    "Distribución de diagnósticos principales, tendencias temporales y análisis demográfico",
                    style={
                        "textAlign": "center",
                        "color": "#64748b",
                        "marginBottom": "20px",
                        "fontSize": "0.95rem",
                    },
                ),
                # Gráficos en grid
                html.Div(
                    [
                        # Gráfico 1: Distribución por diagnóstico
                        html.Div(
                            [
                                html.H4(
                                    "Top 10 Diagnósticos Principales",
                                    style={
                                        "textAlign": "center",
                                        "marginBottom": "15px",
                                    },
                                ),
                                dcc.Graph(
                                    id="grafico-diagnosticos",
                                    config={"displayModeBar": False},
                                    figure=apply_dark_theme(
                                        px.bar(
                                            df_diagnosticos["diagnostico_principal"]
                                            .value_counts()
                                            .head(10)
                                            .reset_index()
                                            if not df_diagnosticos.empty
                                            else pd.DataFrame(),
                                            x="count",
                                            y="diagnostico_principal",
                                            orientation="h",
                                            labels={
                                                "diagnostico_principal": "Diagnóstico",
                                                "count": "Número de Casos",
                                            },
                                            color="count",
                                            color_continuous_scale="Blues",
                                        ).update_layout(
                                            margin=dict(l=100, r=30, t=30, b=50),
                                            height=400,
                                            showlegend=False,
                                        )
                                    )
                                    if not df_diagnosticos.empty
                                    else apply_dark_theme(
                                        go.Figure()
                                        .add_annotation(
                                            text="No hay datos disponibles",
                                            xref="paper",
                                            yref="paper",
                                            x=0.5,
                                            y=0.5,
                                            showarrow=False,
                                            font=dict(size=20, color="#94a3b8"),
                                        )
                                        .update_layout(
                                            height=400,
                                            xaxis=dict(visible=False),
                                            yaxis=dict(visible=False),
                                        )
                                    ),
                                ),
                            ],
                            className="chart-card chart-large",
                        ),
                        # Gráfico 2: Distribución por edad
                        html.Div(
                            [
                                html.H4(
                                    "Distribución por Rango de Edad",
                                    style={
                                        "textAlign": "center",
                                        "marginBottom": "15px",
                                    },
                                ),
                                dcc.Graph(
                                    id="grafico-edad",
                                    config={"displayModeBar": False},
                                    figure=apply_dark_theme(
                                        px.pie(
                                            df_diagnosticos["rango_de_edad"]
                                            .value_counts()
                                            .reset_index()
                                            if not df_diagnosticos.empty
                                            else pd.DataFrame(),
                                            values="count",
                                            names="rango_de_edad",
                                            hole=0.4,
                                            color_discrete_sequence=px.colors.qualitative.Set3,
                                        )
                                        .update_layout(
                                            margin=dict(l=20, r=20, t=20, b=20),
                                            showlegend=True,
                                            height=400,
                                        )
                                        .update_traces(
                                            textposition="inside",
                                            textinfo="percent+label",
                                        )
                                    )
                                    if not df_diagnosticos.empty
                                    else apply_dark_theme(
                                        go.Figure()
                                        .add_annotation(
                                            text="No hay datos disponibles",
                                            xref="paper",
                                            yref="paper",
                                            x=0.5,
                                            y=0.5,
                                            showarrow=False,
                                            font=dict(size=20, color="#94a3b8"),
                                        )
                                        .update_layout(
                                            height=400,
                                            xaxis=dict(visible=False),
                                            yaxis=dict(visible=False),
                                        )
                                    ),
                                ),
                            ],
                            className="chart-card chart-small",
                        ),
                    ],
                    className="charts-grid",
                ),
                # Gráfico de tendencia temporal
                html.Div(
                    [
                        html.H4(
                            "Ingresos por Mes",
                            style={"textAlign": "center", "marginBottom": "15px"},
                        ),
                        dcc.Graph(
                            id="grafico-temporal",
                            config={"displayModeBar": False},
                            figure=apply_dark_theme(
                                px.line(
                                    df_diagnosticos["mes_de_ingreso"]
                                    .value_counts()
                                    .sort_index()
                                    .reset_index()
                                    if not df_diagnosticos.empty
                                    else pd.DataFrame(),
                                    x="mes_de_ingreso",
                                    y="count",
                                    labels={
                                        "mes_de_ingreso": "Mes de Ingreso",
                                        "count": "Número de Ingresos",
                                    },
                                    markers=True,
                                )
                                .update_layout(
                                    margin=dict(l=50, r=30, t=30, b=100),
                                    height=350,
                                    xaxis=dict(tickangle=-45),
                                )
                                .update_traces(
                                    line=dict(color="#60a5fa", width=3),
                                    marker=dict(size=8, color="#60a5fa"),
                                )
                            )
                            if not df_diagnosticos.empty
                            else apply_dark_theme(
                                go.Figure()
                                .add_annotation(
                                    text="No hay datos disponibles",
                                    xref="paper",
                                    yref="paper",
                                    x=0.5,
                                    y=0.5,
                                    showarrow=False,
                                    font=dict(size=20, color="#94a3b8"),
                                )
                                .update_layout(
                                    height=350,
                                    xaxis=dict(visible=False),
                                    yaxis=dict(visible=False),
                                )
                            ),
                        ),
                    ],
                    style={"marginTop": "20px"},
                ),
                # Mapa de calor: Diagnóstico vs Edad
                html.Div(
                    [
                        html.H4(
                            "Mapa de Calor: Diagnósticos más frecuentes por Rango de Edad",
                            style={"textAlign": "center", "marginBottom": "15px"},
                        ),
                        dcc.Graph(
                            id="grafico-heatmap",
                            config={"displayModeBar": False},
                            figure=apply_dark_theme(
                                px.density_heatmap(
                                    df_diagnosticos
                                    if not df_diagnosticos.empty
                                    else pd.DataFrame(),
                                    x="rango_de_edad",
                                    y="diagnostico_principal",
                                    color_continuous_scale="YlOrRd",
                                    labels={
                                        "rango_de_edad": "Rango de Edad",
                                        "diagnostico_principal": "Diagnóstico",
                                    },
                                ).update_layout(
                                    margin=dict(l=150, r=30, t=30, b=100),
                                    height=600,
                                    xaxis=dict(tickangle=-45),
                                )
                            )
                            if not df_diagnosticos.empty
                            else apply_dark_theme(
                                go.Figure()
                                .add_annotation(
                                    text="No hay datos disponibles",
                                    xref="paper",
                                    yref="paper",
                                    x=0.5,
                                    y=0.5,
                                    showarrow=False,
                                    font=dict(size=20, color="#94a3b8"),
                                )
                                .update_layout(
                                    height=600,
                                    xaxis=dict(visible=False),
                                    yaxis=dict(visible=False),
                                )
                            ),
                        ),
                    ],
                    style={"marginTop": "20px"},
                ),
                # Estadísticas resumen
                html.Div(
                    [
                        html.Div(
                            [
                                html.H4(
                                    "📊 Estadísticas Generales",
                                    style={"marginBottom": "15px"},
                                ),
                                html.P(
                                    f"Total de registros: {len(df_diagnosticos)}"
                                    if not df_diagnosticos.empty
                                    else "No hay datos disponibles"
                                ),
                                html.P(
                                    f"Diagnósticos únicos: {df_diagnosticos['diagnostico_principal'].nunique()}"
                                    if not df_diagnosticos.empty
                                    else ""
                                ),
                                html.P(
                                    f"Rango de edad más común: {df_diagnosticos['rango_de_edad'].mode()[0] if not df_diagnosticos.empty and not df_diagnosticos['rango_de_edad'].mode().empty else 'N/A'}"
                                ),
                                html.P(
                                    f"Diagnóstico más frecuente: {df_diagnosticos['diagnostico_principal'].mode()[0] if not df_diagnosticos.empty and not df_diagnosticos['diagnostico_principal'].mode().empty else 'N/A'}"
                                ),
                            ],
                            style={
                                "backgroundColor": "#f0f9ff",
                                "padding": "20px",
                                "borderRadius": "8px",
                                "marginTop": "20px",
                                "border": "1px solid #bae6fd",
                            },
                        )
                    ]
                ),
            ],
            className="chart-card full",
        ),
        # Sección 2: Análisis de Diagnósticos por Sexo
        html.Div(
            [
                html.H3(
                    "2️⃣ Análisis por Sexo: Perspectiva de Género",
                    className="chart-title",
                ),
                html.P(
                    "Distribución de diagnósticos y patrones diferenciados por sexo del paciente",
                    style={
                        "textAlign": "center",
                        "color": "#64748b",
                        "marginBottom": "20px",
                        "fontSize": "0.95rem",
                    },
                ),
                # Gráficos en grid
                html.Div(
                    [
                        # Gráfico 1: Distribución general por sexo
                        html.Div(
                            [
                                html.H4(
                                    "Distribución General por Sexo",
                                    style={
                                        "textAlign": "center",
                                        "marginBottom": "15px",
                                    },
                                ),
                                dcc.Graph(
                                    id="grafico-sexo-general",
                                    config={"displayModeBar": False},
                                    figure=apply_dark_theme(
                                        px.pie(
                                            df_diagnostico_sexo["sexo_label"]
                                            .value_counts()
                                            .reset_index()
                                            if not df_diagnostico_sexo.empty
                                            else pd.DataFrame(),
                                            values="count",
                                            names="sexo_label",
                                            hole=0.4,
                                            color="sexo_label",
                                            color_discrete_map={
                                                "Masculino": "#3b82f6",
                                                "Femenino": "#ec4899",
                                            },
                                        )
                                        .update_layout(
                                            font={
                                                "family": "Segoe UI, sans-serif",
                                                "color": "#e2e8f0",
                                            },
                                            margin=dict(l=20, r=20, t=20, b=20),
                                            showlegend=True,
                                            height=400,
                                        )
                                        .update_traces(
                                            textposition="inside",
                                            textinfo="percent+label",
                                            textfont_size=14,
                                        )
                                    )
                                    if not df_diagnostico_sexo.empty
                                    else apply_dark_theme(
                                        go.Figure()
                                        .add_annotation(
                                            text="No hay datos disponibles",
                                            xref="paper",
                                            yref="paper",
                                            x=0.5,
                                            y=0.5,
                                            showarrow=False,
                                            font=dict(size=20, color="#94a3b8"),
                                        )
                                        .update_layout(
                                            height=400,
                                            xaxis=dict(visible=False),
                                            yaxis=dict(visible=False),
                                        )
                                    ),
                                ),
                            ],
                            className="chart-card chart-small",
                        ),
                        # Gráfico 2: Top diagnósticos por sexo
                        html.Div(
                            [
                                html.H4(
                                    "Top 10 Diagnósticos por Sexo",
                                    style={
                                        "textAlign": "center",
                                        "marginBottom": "15px",
                                    },
                                ),
                                dcc.Graph(
                                    id="grafico-diagnosticos-sexo",
                                    config={"displayModeBar": False},
                                    figure=apply_dark_theme(
                                        px.histogram(
                                            df_diagnostico_sexo[
                                                df_diagnostico_sexo[
                                                    "diagnostico_principal"
                                                ].isin(
                                                    df_diagnostico_sexo[
                                                        "diagnostico_principal"
                                                    ]
                                                    .value_counts()
                                                    .head(10)
                                                    .index
                                                )
                                            ]
                                            if not df_diagnostico_sexo.empty
                                            else pd.DataFrame(),
                                            x="diagnostico_principal",
                                            color="sexo_label",
                                            barmode="group",
                                            labels={
                                                "diagnostico_principal": "Diagnóstico",
                                                "count": "Número de Casos",
                                                "sexo_label": "Sexo",
                                            },
                                            color_discrete_map={
                                                "Masculino": "#3b82f6",
                                                "Femenino": "#ec4899",
                                            },
                                        ).update_layout(
                                            font={
                                                "family": "Segoe UI, sans-serif",
                                                "color": "#e2e8f0",
                                            },
                                            margin=dict(l=50, r=30, t=30, b=100),
                                            height=400,
                                            xaxis=dict(tickangle=-45),
                                        )
                                    )
                                    if not df_diagnostico_sexo.empty
                                    else apply_dark_theme(
                                        go.Figure()
                                        .add_annotation(
                                            text="No hay datos disponibles",
                                            xref="paper",
                                            yref="paper",
                                            x=0.5,
                                            y=0.5,
                                            showarrow=False,
                                            font=dict(size=20, color="#94a3b8"),
                                        )
                                        .update_layout(
                                            height=400,
                                            xaxis=dict(visible=False),
                                            yaxis=dict(visible=False),
                                        )
                                    ),
                                ),
                            ],
                            className="chart-card chart-large",
                        ),
                    ],
                    className="charts-grid",
                ),
                # Gráfico de barras apiladas - Proporción de sexo por diagnóstico
                html.Div(
                    [
                        html.H4(
                            "Proporción de Sexo en Diagnósticos Principales",
                            style={"textAlign": "center", "marginBottom": "15px"},
                        ),
                        dcc.Graph(
                            id="grafico-proporcion-sexo",
                            config={"displayModeBar": False},
                            figure=apply_dark_theme(
                                px.histogram(
                                    df_diagnostico_sexo[
                                        df_diagnostico_sexo[
                                            "diagnostico_principal"
                                        ].isin(
                                            df_diagnostico_sexo["diagnostico_principal"]
                                            .value_counts()
                                            .head(15)
                                            .index
                                        )
                                    ]
                                    if not df_diagnostico_sexo.empty
                                    else pd.DataFrame(),
                                    y="diagnostico_principal",
                                    color="sexo_label",
                                    barmode="stack",
                                    orientation="h",
                                    labels={
                                        "diagnostico_principal": "Diagnóstico",
                                        "count": "Número de Casos",
                                        "sexo_label": "Sexo",
                                    },
                                    color_discrete_map={
                                        "Masculino": "#3b82f6",
                                        "Femenino": "#ec4899",
                                    },
                                ).update_layout(
                                    font={
                                        "family": "Segoe UI, sans-serif",
                                        "color": "#e2e8f0",
                                    },
                                    margin=dict(l=100, r=30, t=30, b=50),
                                    height=500,
                                )
                            )
                            if not df_diagnostico_sexo.empty
                            else apply_dark_theme(
                                go.Figure()
                                .add_annotation(
                                    text="No hay datos disponibles",
                                    xref="paper",
                                    yref="paper",
                                    x=0.5,
                                    y=0.5,
                                    showarrow=False,
                                    font=dict(size=20, color="#94a3b8"),
                                )
                                .update_layout(
                                    height=500,
                                    xaxis=dict(visible=False),
                                    yaxis=dict(visible=False),
                                )
                            ),
                        ),
                    ],
                    style={"marginTop": "20px"},
                ),
                # Tabla comparativa
                html.Div(
                    [
                        html.H4(
                            "Tabla Comparativa: Diagnósticos por Sexo",
                            style={"textAlign": "center", "marginBottom": "15px"},
                        ),
                        dash_table.DataTable(
                            id="tabla-diagnostico-sexo",
                            columns=[
                                {
                                    "name": "Diagnóstico",
                                    "id": "diagnostico_principal",
                                },
                                {"name": "Masculino", "id": "Masculino"},
                                {"name": "Femenino", "id": "Femenino"},
                                {"name": "Total", "id": "Total"},
                            ],
                            data=df_diagnostico_sexo.groupby("diagnostico_principal")[
                                "sexo_label"
                            ]
                            .value_counts()
                            .unstack(fill_value=0)
                            .assign(Total=lambda x: x.sum(axis=1) if not x.empty else 0)
                            .reset_index()
                            .sort_values("Total", ascending=False)
                            .head(20)
                            .to_dict("records")
                            if not df_diagnostico_sexo.empty
                            else [],
                            style_table={
                                "overflowX": "auto",
                                "overflowY": "auto",
                                "maxHeight": "400px",
                            },
                            style_cell={
                                "textAlign": "center",
                                "padding": "12px",
                                "fontFamily": "Segoe UI, sans-serif",
                                "fontSize": "14px",
                                "border": "1px solid #e2e8f0",
                            },
                            style_header={
                                "backgroundColor": "#6366f1",
                                "color": "white",
                                "fontWeight": "bold",
                                "textAlign": "center",
                                "border": "1px solid #4f46e5",
                            },
                            style_data={
                                "backgroundColor": "white",
                                "color": "#1e293b",
                            },
                            style_data_conditional=[
                                {
                                    "if": {"row_index": "odd"},
                                    "backgroundColor": "#f8fafc",
                                },
                                {
                                    "if": {"state": "active"},
                                    "backgroundColor": "#dbeafe",
                                    "border": "1px solid #2563eb",
                                },
                                {
                                    "if": {"column_id": "Masculino"},
                                    "backgroundColor": "#eff6ff",
                                },
                                {
                                    "if": {"column_id": "Femenino"},
                                    "backgroundColor": "#fdf2f8",
                                },
                            ],
                            page_size=10,
                            sort_action="native",
                            sort_mode="multi",
                            filter_action="native",
                        ),
                    ],
                    style={"marginTop": "30px"},
                ),
                # Estadísticas resumen
                html.Div(
                    [
                        html.Div(
                            [
                                html.H4(
                                    "📊 Estadísticas por Sexo",
                                    style={"marginBottom": "15px"},
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.H5(
                                                    "👨 Masculino",
                                                    style={"color": "#3b82f6"},
                                                ),
                                                html.P(
                                                    f"Total casos: {len(df_diagnostico_sexo[df_diagnostico_sexo['sexo_label'] == 'Masculino'])}"
                                                    if not df_diagnostico_sexo.empty
                                                    else "N/A"
                                                ),
                                                html.P(
                                                    f"Diagnósticos únicos: {df_diagnostico_sexo[df_diagnostico_sexo['sexo_label'] == 'Masculino']['diagnostico_principal'].nunique()}"
                                                    if not df_diagnostico_sexo.empty
                                                    else "N/A"
                                                ),
                                            ],
                                            style={
                                                "flex": "1",
                                                "padding": "15px",
                                                "backgroundColor": "#eff6ff",
                                                "borderRadius": "8px",
                                                "border": "2px solid #bfdbfe",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                html.H5(
                                                    "👩 Femenino",
                                                    style={"color": "#ec4899"},
                                                ),
                                                html.P(
                                                    f"Total casos: {len(df_diagnostico_sexo[df_diagnostico_sexo['sexo_label'] == 'Femenino'])}"
                                                    if not df_diagnostico_sexo.empty
                                                    else "N/A"
                                                ),
                                                html.P(
                                                    f"Diagnósticos únicos: {df_diagnostico_sexo[df_diagnostico_sexo['sexo_label'] == 'Femenino']['diagnostico_principal'].nunique()}"
                                                    if not df_diagnostico_sexo.empty
                                                    else "N/A"
                                                ),
                                            ],
                                            style={
                                                "flex": "1",
                                                "padding": "15px",
                                                "backgroundColor": "#fdf2f8",
                                                "borderRadius": "8px",
                                                "border": "2px solid #fbcfe8",
                                            },
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "gap": "20px",
                                        "marginTop": "15px",
                                    },
                                ),
                            ],
                            style={
                                "backgroundColor": "#f8fafc",
                                "padding": "20px",
                                "borderRadius": "8px",
                                "marginTop": "20px",
                                "border": "1px solid #e2e8f0",
                            },
                        )
                    ]
                ),
            ],
            className="chart-card full",
        ),
        # Sección 3: Análisis de Severidad vs Mortalidad APR
        html.Div(
            [
                html.H3(
                    "3️⃣ Severidad y Riesgo de Mortalidad APR",
                    className="chart-title",
                ),
                html.P(
                    "Evaluación de la gravedad clínica y correlación con el riesgo de mortalidad",
                    style={
                        "textAlign": "center",
                        "color": "#64748b",
                        "marginBottom": "20px",
                        "fontSize": "0.95rem",
                    },
                ),
                # Gráficos en grid
                html.Div(
                    [
                        # Gráfico 1: Distribución de Severidad
                        html.Div(
                            [
                                html.H4(
                                    "Distribución de Niveles de Severidad",
                                    style={
                                        "textAlign": "center",
                                        "marginBottom": "15px",
                                    },
                                ),
                                dcc.Graph(
                                    id="grafico-severidad-dist",
                                    config={"displayModeBar": False},
                                    figure=apply_dark_theme(
                                        px.pie(
                                            df_severidad_mortalidad["severidad_label"]
                                            .value_counts()
                                            .reset_index()
                                            if not df_severidad_mortalidad.empty
                                            else pd.DataFrame(),
                                            values="count",
                                            names="severidad_label",
                                            hole=0.4,
                                            color="severidad_label",
                                            color_discrete_map={
                                                "Leve": "#22c55e",
                                                "Moderado": "#eab308",
                                                "Grave": "#f97316",
                                                "Extremo": "#dc2626",
                                            },
                                            category_orders={
                                                "severidad_label": [
                                                    "Leve",
                                                    "Moderado",
                                                    "Grave",
                                                    "Extremo",
                                                ]
                                            },
                                        )
                                        .update_layout(
                                            font={
                                                "family": "Segoe UI, sans-serif",
                                                "color": "#e2e8f0",
                                            },
                                            margin=dict(l=20, r=20, t=20, b=20),
                                            showlegend=True,
                                            height=400,
                                        )
                                        .update_traces(
                                            textposition="inside",
                                            textinfo="percent+label",
                                            textfont_size=13,
                                        )
                                    )
                                    if not df_severidad_mortalidad.empty
                                    else apply_dark_theme(
                                        go.Figure()
                                        .add_annotation(
                                            text="No hay datos disponibles",
                                            xref="paper",
                                            yref="paper",
                                            x=0.5,
                                            y=0.5,
                                            showarrow=False,
                                            font=dict(size=20, color="#94a3b8"),
                                        )
                                        .update_layout(
                                            height=400,
                                            xaxis=dict(visible=False),
                                            yaxis=dict(visible=False),
                                        )
                                    ),
                                ),
                            ],
                            className="chart-card chart-small",
                        ),
                        # Gráfico 2: Distribución de Mortalidad
                        html.Div(
                            [
                                html.H4(
                                    "Distribución de Riesgo de Mortalidad",
                                    style={
                                        "textAlign": "center",
                                        "marginBottom": "15px",
                                    },
                                ),
                                dcc.Graph(
                                    id="grafico-mortalidad-dist",
                                    config={"displayModeBar": False},
                                    figure=apply_dark_theme(
                                        px.pie(
                                            df_severidad_mortalidad["mortalidad_label"]
                                            .value_counts()
                                            .reset_index()
                                            if not df_severidad_mortalidad.empty
                                            else pd.DataFrame(),
                                            values="count",
                                            names="mortalidad_label",
                                            hole=0.4,
                                            color="mortalidad_label",
                                            color_discrete_map={
                                                "Bajo": "#22c55e",
                                                "Moderado": "#eab308",
                                                "Alto": "#f97316",
                                                "Extremo": "#dc2626",
                                            },
                                            category_orders={
                                                "mortalidad_label": [
                                                    "Bajo",
                                                    "Moderado",
                                                    "Alto",
                                                    "Extremo",
                                                ]
                                            },
                                        )
                                        .update_layout(
                                            font={
                                                "family": "Segoe UI, sans-serif",
                                                "color": "#e2e8f0",
                                            },
                                            margin=dict(l=20, r=20, t=20, b=20),
                                            showlegend=True,
                                            height=400,
                                        )
                                        .update_traces(
                                            textposition="inside",
                                            textinfo="percent+label",
                                            textfont_size=13,
                                        )
                                    )
                                    if not df_severidad_mortalidad.empty
                                    else apply_dark_theme(
                                        go.Figure()
                                        .add_annotation(
                                            text="No hay datos disponibles",
                                            xref="paper",
                                            yref="paper",
                                            x=0.5,
                                            y=0.5,
                                            showarrow=False,
                                            font=dict(size=20, color="#94a3b8"),
                                        )
                                        .update_layout(
                                            height=400,
                                            xaxis=dict(visible=False),
                                            yaxis=dict(visible=False),
                                        )
                                    ),
                                ),
                            ],
                            className="chart-card chart-small",
                        ),
                    ],
                    className="charts-grid",
                ),
                # Mapa de calor: Severidad vs Mortalidad
                html.Div(
                    [
                        html.H4(
                            "Mapa de Calor: Correlación Severidad vs Mortalidad",
                            style={"textAlign": "center", "marginBottom": "15px"},
                        ),
                        dcc.Graph(
                            id="grafico-severidad-mortalidad-heatmap",
                            config={"displayModeBar": False},
                            figure=apply_dark_theme(
                                px.density_heatmap(
                                    df_severidad_mortalidad
                                    if not df_severidad_mortalidad.empty
                                    else pd.DataFrame(),
                                    x="severidad_label",
                                    y="mortalidad_label",
                                    color_continuous_scale="RdYlGn_r",
                                    labels={
                                        "severidad_label": "Nivel de Severidad APR",
                                        "mortalidad_label": "Riesgo de Mortalidad APR",
                                    },
                                    category_orders={
                                        "severidad_label": [
                                            "Leve",
                                            "Moderado",
                                            "Grave",
                                            "Extremo",
                                        ],
                                        "mortalidad_label": [
                                            "Bajo",
                                            "Moderado",
                                            "Alto",
                                            "Extremo",
                                        ],
                                    },
                                ).update_layout(
                                    font={
                                        "family": "Segoe UI, sans-serif",
                                        "color": "#e2e8f0",
                                    },
                                    margin=dict(l=100, r=30, t=30, b=100),
                                    height=500,
                                )
                            )
                            if not df_severidad_mortalidad.empty
                            else apply_dark_theme(
                                go.Figure()
                                .add_annotation(
                                    text="No hay datos disponibles",
                                    xref="paper",
                                    yref="paper",
                                    x=0.5,
                                    y=0.5,
                                    showarrow=False,
                                    font=dict(size=20, color="#94a3b8"),
                                )
                                .update_layout(
                                    height=500,
                                    xaxis=dict(visible=False),
                                    yaxis=dict(visible=False),
                                )
                            ),
                        ),
                    ],
                    style={"marginTop": "20px"},
                ),
                # Gráfico de barras agrupadas
                html.Div(
                    [
                        html.H4(
                            "Distribución Combinada: Severidad y Mortalidad",
                            style={"textAlign": "center", "marginBottom": "15px"},
                        ),
                        dcc.Graph(
                            id="grafico-severidad-mortalidad-bars",
                            config={"displayModeBar": False},
                            figure=apply_dark_theme(
                                px.histogram(
                                    df_severidad_mortalidad
                                    if not df_severidad_mortalidad.empty
                                    else pd.DataFrame(),
                                    x="severidad_label",
                                    color="mortalidad_label",
                                    barmode="group",
                                    labels={
                                        "severidad_label": "Nivel de Severidad APR",
                                        "mortalidad_label": "Riesgo de Mortalidad",
                                        "count": "Número de Casos",
                                    },
                                    color_discrete_map={
                                        "Bajo": "#22c55e",
                                        "Moderado": "#eab308",
                                        "Alto": "#f97316",
                                        "Extremo": "#dc2626",
                                    },
                                    category_orders={
                                        "severidad_label": [
                                            "Leve",
                                            "Moderado",
                                            "Grave",
                                            "Extremo",
                                        ],
                                        "mortalidad_label": [
                                            "Bajo",
                                            "Moderado",
                                            "Alto",
                                            "Extremo",
                                        ],
                                    },
                                ).update_layout(
                                    font={
                                        "family": "Segoe UI, sans-serif",
                                        "color": "#e2e8f0",
                                    },
                                    margin=dict(l=50, r=30, t=30, b=50),
                                    height=450,
                                )
                            )
                            if not df_severidad_mortalidad.empty
                            else apply_dark_theme(
                                go.Figure()
                                .add_annotation(
                                    text="No hay datos disponibles",
                                    xref="paper",
                                    yref="paper",
                                    x=0.5,
                                    y=0.5,
                                    showarrow=False,
                                    font=dict(size=20, color="#94a3b8"),
                                )
                                .update_layout(
                                    height=450,
                                    xaxis=dict(visible=False),
                                    yaxis=dict(visible=False),
                                )
                            ),
                        ),
                    ],
                    style={"marginTop": "20px"},
                ),
                # Tabla de contingencia
                html.Div(
                    [
                        html.H4(
                            "Tabla de Contingencia: Severidad vs Mortalidad",
                            style={"textAlign": "center", "marginBottom": "15px"},
                        ),
                        dash_table.DataTable(
                            id="tabla-severidad-mortalidad",
                            columns=[
                                {"name": "Severidad \\ Mortalidad", "id": "index"},
                                {"name": "Bajo", "id": "Bajo"},
                                {"name": "Moderado", "id": "Moderado"},
                                {"name": "Alto", "id": "Alto"},
                                {"name": "Extremo", "id": "Extremo"},
                                {"name": "Total", "id": "Total"},
                            ],
                            data=pd.crosstab(
                                df_severidad_mortalidad["severidad_label"],
                                df_severidad_mortalidad["mortalidad_label"],
                                margins=True,
                                margins_name="Total",
                            )
                            .rename_axis("index")
                            .reset_index()
                            .fillna(0)
                            .to_dict("records")
                            if not df_severidad_mortalidad.empty
                            else [],
                            style_table={
                                "overflowX": "auto",
                            },
                            style_cell={
                                "textAlign": "center",
                                "padding": "12px",
                                "fontFamily": "Segoe UI, sans-serif",
                                "fontSize": "14px",
                                "border": "1px solid #e2e8f0",
                            },
                            style_header={
                                "backgroundColor": "#dc2626",
                                "color": "white",
                                "fontWeight": "bold",
                                "textAlign": "center",
                                "border": "1px solid #b91c1c",
                            },
                            style_data={
                                "backgroundColor": "white",
                                "color": "#1e293b",
                            },
                            style_data_conditional=[
                                {
                                    "if": {"row_index": "odd"},
                                    "backgroundColor": "#fef2f2",
                                },
                                {
                                    "if": {"column_id": "Total"},
                                    "backgroundColor": "#fee2e2",
                                    "fontWeight": "bold",
                                },
                                {
                                    "if": {
                                        "filter_query": "{index} = 'Total'",
                                    },
                                    "backgroundColor": "#fee2e2",
                                    "fontWeight": "bold",
                                },
                            ],
                        ),
                    ],
                    style={"marginTop": "30px"},
                ),
                # Estadísticas resumen
                html.Div(
                    [
                        html.Div(
                            [
                                html.H4(
                                    "📊 Análisis Estadístico",
                                    style={"marginBottom": "15px"},
                                ),
                                html.P(
                                    f"Total de casos: {len(df_severidad_mortalidad)}"
                                    if not df_severidad_mortalidad.empty
                                    else "No hay datos disponibles"
                                ),
                                html.P(
                                    f"Severidad más común: {df_severidad_mortalidad['severidad_label'].mode()[0] if not df_severidad_mortalidad.empty and not df_severidad_mortalidad['severidad_label'].mode().empty else 'N/A'}"
                                ),
                                html.P(
                                    f"Riesgo de mortalidad más común: {df_severidad_mortalidad['mortalidad_label'].mode()[0] if not df_severidad_mortalidad.empty and not df_severidad_mortalidad['mortalidad_label'].mode().empty else 'N/A'}"
                                ),
                                html.P(
                                    f"Casos de severidad extrema: {len(df_severidad_mortalidad[df_severidad_mortalidad['severidad_label'] == 'Extremo']) if not df_severidad_mortalidad.empty else 0}"
                                ),
                                html.P(
                                    f"Casos de mortalidad extrema: {len(df_severidad_mortalidad[df_severidad_mortalidad['mortalidad_label'] == 'Extremo']) if not df_severidad_mortalidad.empty else 0}"
                                ),
                            ],
                            style={
                                "backgroundColor": "#fef2f2",
                                "padding": "20px",
                                "borderRadius": "8px",
                                "marginTop": "20px",
                                "border": "2px solid #fecaca",
                            },
                        )
                    ]
                ),
            ],
            className="chart-card full",
        ),
        # Sección 4: Análisis de Peso APR-GRD y Estancia Hospitalaria
        html.Div(
            [
                html.H3(
                    "4️⃣ Peso APR-GRD y Estancia Hospitalaria",
                    className="chart-title",
                ),
                html.P(
                    "Correlación entre el peso APR-GRD español y los días de estancia hospitalaria",
                    style={
                        "textAlign": "center",
                        "color": "#64748b",
                        "marginBottom": "20px",
                        "fontSize": "0.95rem",
                    },
                ),
                # Gráfico de dispersión
                dcc.Graph(
                    id="grafico-peso-estancia",
                    config={"displayModeBar": False},
                    figure=apply_dark_theme(
                        px.scatter(
                            df_peso_estancia
                            if not df_peso_estancia.empty
                            else pd.DataFrame(),
                            x="peso_espanol_apr",
                            y="estancia_dias",
                            title="Relación entre Peso APR-GRD y Estancia Hospitalaria",
                            labels={
                                "peso_espanol_apr": "Peso APR-GRD Español",
                                "estancia_dias": "Días de Estancia",
                            },
                            color="estancia_dias",
                            size="peso_espanol_apr",
                            color_continuous_scale="Viridis",
                            hover_data={
                                "peso_espanol_apr": ":.3f",
                                "estancia_dias": True,
                            },
                        ).update_layout(
                            font={"family": "Segoe UI, sans-serif", "color": "#e2e8f0"},
                            margin=dict(l=50, r=30, t=60, b=50),
                            height=400,
                        )
                    )
                    if not df_peso_estancia.empty
                    else apply_dark_theme(
                        go.Figure()
                        .add_annotation(
                            text="No hay datos disponibles",
                            xref="paper",
                            yref="paper",
                            x=0.5,
                            y=0.5,
                            showarrow=False,
                            font=dict(size=20, color="#94a3b8"),
                        )
                        .update_layout(
                            height=400,
                            xaxis=dict(visible=False),
                            yaxis=dict(visible=False),
                        )
                    ),
                    style={"marginBottom": "30px"},
                ),
                # Tabla de datos
                dash_table.DataTable(
                    id="tabla-peso-estancia",
                    columns=[
                        {"name": "Peso APR-GRD Español", "id": "peso_espanol_apr"},
                        {"name": "Estancia (días)", "id": "estancia_dias"},
                    ],
                    data=df_peso_estancia.to_dict("records")
                    if not df_peso_estancia.empty
                    else [],
                    style_table={
                        "overflowX": "auto",
                        "overflowY": "auto",
                        "maxHeight": "400px",
                    },
                    style_cell={
                        "textAlign": "center",
                        "padding": "12px",
                        "fontFamily": "Segoe UI, sans-serif",
                        "fontSize": "14px",
                        "border": "1px solid #e2e8f0",
                    },
                    style_header={
                        "backgroundColor": "#2563eb",
                        "color": "white",
                        "fontWeight": "bold",
                        "textAlign": "center",
                        "border": "1px solid #1e40af",
                    },
                    style_data={
                        "backgroundColor": "white",
                        "color": "#1e293b",
                    },
                    style_data_conditional=[
                        {
                            "if": {"row_index": "odd"},
                            "backgroundColor": "#f8fafc",
                        },
                        {
                            "if": {"state": "active"},
                            "backgroundColor": "#dbeafe",
                            "border": "1px solid #2563eb",
                        },
                    ],
                    page_size=10,
                    sort_action="native",
                    sort_mode="multi",
                    filter_action="native",
                ),
                # Estadísticas resumen
                html.Div(
                    [
                        html.Div(
                            [
                                html.H4(
                                    "📈 Estadísticas", style={"marginBottom": "15px"}
                                ),
                                html.P(
                                    f"Total de registros: {len(df_peso_estancia)}"
                                    if not df_peso_estancia.empty
                                    else "No hay datos disponibles"
                                ),
                                html.P(
                                    f"Peso promedio: {df_peso_estancia['peso_espanol_apr'].mean():.3f}"
                                    if not df_peso_estancia.empty
                                    else ""
                                ),
                                html.P(
                                    f"Estancia promedio: {df_peso_estancia['estancia_dias'].mean():.1f} días"
                                    if not df_peso_estancia.empty
                                    else ""
                                ),
                                html.P(
                                    f"Estancia máxima: {df_peso_estancia['estancia_dias'].max()} días"
                                    if not df_peso_estancia.empty
                                    else ""
                                ),
                                html.P(
                                    f"Estancia mínima: {df_peso_estancia['estancia_dias'].min()} días"
                                    if not df_peso_estancia.empty
                                    else ""
                                ),
                            ],
                            style={
                                "backgroundColor": "#f0f9ff",
                                "padding": "20px",
                                "borderRadius": "8px",
                                "marginTop": "20px",
                                "border": "1px solid #bae6fd",
                            },
                        )
                    ]
                ),
            ],
            className="chart-card full",
        ),
        # Sección 5: Insights y Conclusiones
        html.Div(
            [
                html.H3("5️⃣ Insights Clave y Conclusiones", className="chart-title"),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H4("🎯 Diagnósticos"),
                                html.P(
                                    f"Los {df_diagnosticos['diagnostico_principal'].nunique() if not df_diagnosticos.empty else 0} diagnósticos únicos muestran una alta diversidad en condiciones de salud mental"
                                    if not df_diagnosticos.empty
                                    else "Datos no disponibles"
                                ),
                            ],
                            className="tip-card",
                        ),
                        html.Div(
                            [
                                html.H4("⚕️ Severidad"),
                                html.P(
                                    f"El {((df_severidad_mortalidad['nivel_severidad_apr'] >= 3).sum() / len(df_severidad_mortalidad) * 100):.1f}% de casos presentan severidad grave o extrema"
                                    if not df_severidad_mortalidad.empty
                                    else "Datos no disponibles"
                                ),
                            ],
                            className="tip-card",
                        ),
                        html.Div(
                            [
                                html.H4("� Demografía"),
                                html.P(
                                    f"Rango de edad predominante: {df_diagnosticos['rango_de_edad'].mode()[0] if not df_diagnosticos.empty and not df_diagnosticos['rango_de_edad'].mode().empty else 'N/A'} años"
                                    if not df_diagnosticos.empty
                                    else "Datos no disponibles"
                                ),
                            ],
                            className="tip-card",
                        ),
                        html.Div(
                            [
                                html.H4("� Estancia"),
                                html.P(
                                    f"Estancia promedio: {df_peso_estancia['estancia_dias'].mean():.1f} días con correlación al peso APR-GRD"
                                    if not df_peso_estancia.empty
                                    else "Datos no disponibles"
                                ),
                            ],
                            className="tip-card",
                        ),
                    ],
                    className="tips-grid",
                ),
            ],
            className="chart-card full tips-section",
        ),
        # Footer
        html.Footer(
            [
                html.P(
                    "© 2025 Dashboard de Análisis Hospitalario | Datos en tiempo real"
                )
            ],
            className="footer",
        ),
    ],
    className="container",
)

server = app.server

if __name__ == "__main__":
    app.run(debug=True)
