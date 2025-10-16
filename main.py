from dash import Dash, html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Inicializar la app con hojas de estilo personalizadas
app = Dash(__name__, assets_folder='assets')

# Datos de ejemplo - Niveles de Bienestar Mental (escala 1-10)
df_bienestar = pd.DataFrame({
    'Mes': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
    'Bienestar_Emocional': [6.5, 7.2, 6.8, 7.5, 7.8, 8.1],
    'Nivel_Estrés': [6.8, 6.2, 6.5, 5.8, 5.5, 5.2],
    'Horas_Sueño': [6.2, 6.5, 6.8, 7.0, 7.2, 7.5],
    'Actividad_Fisica': [3.5, 4.0, 4.2, 4.8, 5.2, 5.5]
})

# Distribución de factores que afectan la salud mental
df_factores = pd.DataFrame({
    'Factor': ['Trabajo/Estudios', 'Relaciones Sociales', 'Salud Física', 'Finanzas', 'Otros'],
    'Porcentaje': [35, 25, 20, 15, 5]
})

# Datos de actividades de autocuidado realizadas por semana
df_autocuidado = pd.DataFrame({
    'Actividad': ['Meditación', 'Ejercicio', 'Tiempo Social', 'Hobbies', 'Terapia'],
    'Frecuencia_Semanal': [4, 3, 5, 6, 1]
})

# Layout de la aplicación con HTML personalizado
app.layout = html.Div([
    # Header
    html.Header([
        html.H1("Dashboard de Bienestar Mental", className="header-title"),
        html.P("Monitoreo y seguimiento de tu salud emocional", className="subtitle")
    ], className="header"),
    
    # Tarjetas de métricas
    html.Div([
        html.Div([
            html.Div("🧠", className="metric-icon"),
            html.H3("Bienestar Emocional"),
            html.H2(f"{df_bienestar['Bienestar_Emocional'].iloc[-1]:.1f}/10", className="metric-value"),
            html.P("↑ +0.3 vs mes anterior", className="metric-change positive")
        ], className="metric-card mental"),
        
        html.Div([
            html.Div("�", className="metric-icon"),
            html.H3("Nivel de Estrés"),
            html.H2(f"{df_bienestar['Nivel_Estrés'].iloc[-1]:.1f}/10", className="metric-value"),
            html.P("↓ -0.3 mejorando", className="metric-change positive")
        ], className="metric-card stress"),
        
        html.Div([
            html.Div("�", className="metric-icon"),
            html.H3("Horas de Sueño"),
            html.H2(f"{df_bienestar['Horas_Sueño'].iloc[-1]:.1f}h", className="metric-value"),
            html.P("↑ +0.3h vs mes anterior", className="metric-change positive")
        ], className="metric-card sleep"),
    ], className="metrics-grid"),
    
    # Gráficos principales
    html.Div([
        html.Div([
            html.H3("Evolución del Bienestar y Estrés", className="chart-title"),
            dcc.Graph(
                id='grafico-bienestar',
                figure=go.Figure([
                    go.Scatter(
                        x=df_bienestar['Mes'],
                        y=df_bienestar['Bienestar_Emocional'],
                        mode='lines+markers',
                        name='Bienestar Emocional',
                        line=dict(color='#2563eb', width=3),
                        marker=dict(size=8)
                    ),
                    go.Scatter(
                        x=df_bienestar['Mes'],
                        y=df_bienestar['Nivel_Estrés'],
                        mode='lines+markers',
                        name='Nivel de Estrés',
                        line=dict(color='#1e293b', width=3),
                        marker=dict(size=8)
                    )
                ]).update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font={'size': 12, 'family': 'Segoe UI, sans-serif', 'color': '#1e293b'},
                    margin=dict(l=50, r=30, t=30, b=50),
                    xaxis_title='Mes',
                    yaxis_title='Nivel (1-10)',
                    yaxis=dict(range=[0, 10]),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    hovermode='x unified',
                    height=400
                )
            )
        ], className="chart-card chart-large"),
        
        html.Div([
            html.H3("Factores de Estrés", className="chart-title"),
            dcc.Graph(
                id='grafico-factores',
                figure=px.pie(
                    df_factores, 
                    values='Porcentaje', 
                    names='Factor',
                    hole=0.4,
                    color_discrete_sequence=['#2563eb', '#3b82f6', '#60a5fa', '#93c5fd', '#dbeafe']
                ).update_layout(
                    paper_bgcolor='white',
                    font={'family': 'Segoe UI, sans-serif', 'color': '#1e293b'},
                    margin=dict(l=20, r=20, t=20, b=20),
                    showlegend=True,
                    height=400
                )
            )
        ], className="chart-card chart-small"),
    ], className="charts-grid"),
    
    # Gráfico de actividades de autocuidado
    html.Div([
        html.H3("Actividades de Autocuidado Semanales", className="chart-title"),
        dcc.Graph(
            id='grafico-autocuidado',
            figure=px.bar(
                df_autocuidado,
                x='Actividad',
                y='Frecuencia_Semanal',
                color='Frecuencia_Semanal',
                color_continuous_scale=['#dbeafe', '#93c5fd', '#60a5fa', '#3b82f6', '#2563eb'],
                labels={'Frecuencia_Semanal': 'Veces por semana'}
            ).update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font={'family': 'Segoe UI, sans-serif', 'color': '#1e293b'},
                margin=dict(l=50, r=30, t=30, b=50),
                xaxis_title='Actividad',
                yaxis_title='Frecuencia (veces/semana)',
                showlegend=False,
                height=350
            )
        )
    ], className="chart-card full"),
    
    # Gráfico interactivo con selector
    html.Div([
        html.H3("Seguimiento Personalizado", className="chart-title"),
        html.Div([
            html.Label("Selecciona métrica:", className="control-label"),
            dcc.Dropdown(
                id='dropdown-metrica',
                options=[
                    {'label': '🧠 Bienestar Emocional', 'value': 'Bienestar_Emocional'},
                    {'label': '😌 Nivel de Estrés', 'value': 'Nivel_Estrés'},
                    {'label': '😴 Horas de Sueño', 'value': 'Horas_Sueño'},
                    {'label': '🏃 Actividad Física', 'value': 'Actividad_Fisica'}
                ],
                value='Bienestar_Emocional',
                className="dropdown-select"
            ),
        ], className="controls"),
        dcc.Graph(id='grafico-tendencia')
    ], className="chart-card full"),
    
    # Sección de consejos
    html.Div([
        html.H3("💡 Recomendaciones para tu Bienestar", className="chart-title"),
        html.Div([
            html.Div([
                html.H4("🧘 Mindfulness"),
                html.P("Practica 10 minutos de meditación al día para reducir el estrés"),
            ], className="tip-card"),
            html.Div([
                html.H4("💪 Ejercicio"),
                html.P("La actividad física regular mejora el estado de ánimo"),
            ], className="tip-card"),
            html.Div([
                html.H4("😴 Sueño"),
                html.P("Mantén un horario regular de sueño de 7-8 horas"),
            ], className="tip-card"),
            html.Div([
                html.H4("👥 Conexión Social"),
                html.P("Mantén contacto regular con amigos y seres queridos"),
            ], className="tip-card"),
        ], className="tips-grid")
    ], className="chart-card full tips-section"),
    
    # Footer
    html.Footer([
        html.P("© 2025 Dashboard de Bienestar Mental | Tu salud mental importa 💚")
    ], className="footer")
    
], className="container")

# Callback para actualizar el gráfico de tendencias
@callback(
    Output('grafico-tendencia', 'figure'),
    Input('dropdown-metrica', 'value')
)
def actualizar_grafico(metrica_seleccionada):
    # Definir colores según la métrica - paleta azul y negro
    colores = {
        'Bienestar_Emocional': '#2563eb',
        'Nivel_Estrés': '#1e293b',
        'Horas_Sueño': '#3b82f6',
        'Actividad_Fisica': '#60a5fa'
    }
    
    # Nombres amigables
    nombres = {
        'Bienestar_Emocional': 'Bienestar Emocional',
        'Nivel_Estrés': 'Nivel de Estrés',
        'Horas_Sueño': 'Horas de Sueño',
        'Actividad_Fisica': 'Actividad Física (veces/semana)'
    }
    
    color = colores.get(metrica_seleccionada, '#2563eb')
    nombre = nombres.get(metrica_seleccionada, metrica_seleccionada)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_bienestar['Mes'],
        y=df_bienestar[metrica_seleccionada],
        mode='lines+markers',
        name=nombre,
        line=dict(color=color, width=3),
        marker=dict(size=10, color=color),
        fill='tozeroy',
        fillcolor=f'rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.1)'
    ))
    
    # Configurar el eje Y según la métrica
    if metrica_seleccionada in ['Bienestar_Emocional', 'Nivel_Estrés']:
        yaxis_range = [0, 10]
        yaxis_title = 'Nivel (1-10)'
    elif metrica_seleccionada == 'Horas_Sueño':
        yaxis_range = [0, 12]
        yaxis_title = 'Horas'
    else:
        yaxis_range = [0, None]
        yaxis_title = 'Veces por semana'
    
    fig.update_layout(
        xaxis_title='Mes',
        yaxis_title=yaxis_title,
        yaxis=dict(range=yaxis_range),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font={'family': 'Segoe UI, sans-serif', 'color': '#1e293b'},
        hovermode='x unified',
        margin=dict(l=50, r=30, t=30, b=50),
        height=350
    )
    
    return fig

if __name__ == "__main__":
    app.run(debug=True)
