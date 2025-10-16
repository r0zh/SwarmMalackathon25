from dash import Dash, html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Inicializar la app con hojas de estilo personalizadas
app = Dash(__name__, assets_folder='assets')

# Crear datos de ejemplo
df_sales = pd.DataFrame({
    'Mes': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
    'Ventas': [4500, 5200, 4800, 6100, 5800, 6500],
    'Gastos': [3200, 3400, 3100, 3800, 3600, 4000]
})

df_categories = pd.DataFrame({
    'Categoría': ['Electrónica', 'Ropa', 'Alimentos', 'Hogar', 'Deportes'],
    'Valor': [35, 28, 18, 12, 7]
})

# Layout de la aplicación con HTML personalizado
app.layout = html.Div([
    # Header
    html.Header([
        html.H1("Dashboard Malackathon 2025", className="header-title"),
        html.P("Panel de análisis interactivo con Dash y Plotly", className="subtitle")
    ], className="header"),
    
    # Tarjetas de métricas
    html.Div([
        html.Div([
            html.Div("💰", className="metric-icon"),
            html.H3("Ventas Totales"),
            html.H2(f"${df_sales['Ventas'].sum():,}", className="metric-value"),
            html.P("↑ 15% vs mes anterior", className="metric-change positive")
        ], className="metric-card sales"),
        
        html.Div([
            html.Div("📊", className="metric-icon"),
            html.H3("Gastos Totales"),
            html.H2(f"${df_sales['Gastos'].sum():,}", className="metric-value"),
            html.P("↓ 5% vs mes anterior", className="metric-change negative")
        ], className="metric-card expenses"),
        
        html.Div([
            html.Div("📈", className="metric-icon"),
            html.H3("Beneficio Neto"),
            html.H2(f"${df_sales['Ventas'].sum() - df_sales['Gastos'].sum():,}", className="metric-value"),
            html.P("↑ 28% vs mes anterior", className="metric-change positive")
        ], className="metric-card profit"),
    ], className="metrics-grid"),
    
    # Gráficos principales
    html.Div([
        html.Div([
            html.H3("Ventas y Gastos Mensuales", className="chart-title"),
            dcc.Graph(
                id='grafico-barras',
                figure=px.bar(
                    df_sales, 
                    x='Mes', 
                    y=['Ventas', 'Gastos'],
                    barmode='group',
                    color_discrete_sequence=['#10b981', '#ef4444']
                ).update_layout(
                    plot_bgcolor='#fafafa',
                    paper_bgcolor='white',
                    font={'size': 12, 'family': 'Segoe UI, sans-serif'},
                    margin=dict(l=50, r=30, t=30, b=50),
                    xaxis_title='Mes',
                    yaxis_title='Valor ($)',
                    showlegend=True
                )
            )
        ], className="chart-card large"),
        
        html.Div([
            html.H3("Distribución por Categoría", className="chart-title"),
            dcc.Graph(
                id='grafico-pie',
                figure=px.pie(
                    df_categories, 
                    values='Valor', 
                    names='Categoría',
                    hole=0.4,
                    color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b']
                ).update_layout(
                    paper_bgcolor='white',
                    font={'family': 'Segoe UI, sans-serif'},
                    margin=dict(l=20, r=20, t=20, b=20),
                    showlegend=True
                )
            )
        ], className="chart-card small"),
    ], className="charts-grid"),
    
    # Gráfico de líneas con selector
    html.Div([
        html.H3("Tendencia de Ventas", className="chart-title"),
        html.Div([
            html.Label("Selecciona métrica:", className="control-label"),
            dcc.Dropdown(
                id='dropdown-metrica',
                options=[
                    {'label': 'Ventas', 'value': 'Ventas'},
                    {'label': 'Gastos', 'value': 'Gastos'}
                ],
                value='Ventas',
                className="dropdown-select"
            ),
        ], className="controls"),
        dcc.Graph(id='grafico-lineas')
    ], className="chart-card full"),
    
    # Footer
    html.Footer([
        html.P("© 2025 Malackathon Dashboard | Creado con Dash y Plotly")
    ], className="footer")
    
], className="container")

# Callback para actualizar el gráfico de líneas
@callback(
    Output('grafico-lineas', 'figure'),
    Input('dropdown-metrica', 'value')
)
def actualizar_grafico(metrica_seleccionada):
    color = '#10b981' if metrica_seleccionada == 'Ventas' else '#ef4444'
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_sales['Mes'],
        y=df_sales[metrica_seleccionada],
        mode='lines+markers',
        name=metrica_seleccionada,
        line=dict(color=color, width=3),
        marker=dict(size=10, color=color)
    ))
    
    fig.update_layout(
        xaxis_title='Mes',
        yaxis_title='Valor ($)',
        plot_bgcolor='#fafafa',
        paper_bgcolor='white',
        font={'family': 'Segoe UI, sans-serif'},
        hovermode='x unified',
        margin=dict(l=50, r=30, t=30, b=50)
    )
    
    return fig

if __name__ == "__main__":
    app.run(debug=True)
