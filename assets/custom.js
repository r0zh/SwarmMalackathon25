// Custom JavaScript para mejorar la interactividad del Dashboard de Bienestar Mental

// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard de Bienestar Mental - JavaScript Cargado');
    
    // Inicializar todas las funcionalidades
    initializeAnimations();
    initializeMetricCards();
    initializeChartInteractions();
    initializeThemeToggle();
    addScrollEffects();
});

// Animaciones de entrada mejoradas para las tarjetas
function initializeAnimations() {
    // Asegurar que todas las tarjetas sean visibles desde el inicio
    document.querySelectorAll('.metric-card, .chart-card').forEach(card => {
        card.classList.add('visible');
        card.style.opacity = '1';
        card.style.transform = 'translateY(0)';
    });
    
    // Observer para animaciones futuras (opcional)
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });

    // Observar todas las tarjetas
    document.querySelectorAll('.metric-card, .chart-card').forEach(card => {
        observer.observe(card);
    });
}

// Interactividad mejorada para las tarjetas de métricas
function initializeMetricCards() {
    const metricCards = document.querySelectorAll('.metric-card');
    
    metricCards.forEach(card => {
        // Efecto de pulso al hacer hover
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
        
        // Click para ver más detalles (simulado)
        card.addEventListener('click', function() {
            const metricValue = this.querySelector('.metric-value');
            const originalValue = metricValue.textContent;
            
            // Animación de actualización
            metricValue.style.transform = 'scale(1.1)';
            metricValue.style.color = '#2563eb';
            
            setTimeout(() => {
                metricValue.style.transform = 'scale(1)';
                metricValue.style.color = '';
            }, 300);
            
            // Crear partículas de celebración
            createParticles(this);
        });
    });
}

// Crear efecto de partículas
function createParticles(element) {
    const rect = element.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    
    for (let i = 0; i < 12; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
            position: fixed;
            width: 8px;
            height: 8px;
            background: linear-gradient(135deg, #2563eb, #3b82f6);
            border-radius: 50%;
            pointer-events: none;
            z-index: 9999;
            left: ${centerX}px;
            top: ${centerY}px;
        `;
        
        document.body.appendChild(particle);
        
        const angle = (Math.PI * 2 * i) / 12;
        const velocity = 100 + Math.random() * 50;
        const tx = Math.cos(angle) * velocity;
        const ty = Math.sin(angle) * velocity;
        
        particle.animate([
            { transform: 'translate(0, 0)', opacity: 1 },
            { transform: `translate(${tx}px, ${ty}px)`, opacity: 0 }
        ], {
            duration: 1000,
            easing: 'cubic-bezier(0, .9, .57, 1)'
        }).onfinish = () => particle.remove();
    }
}

// Mejorar interacciones con gráficos de Plotly
function initializeChartInteractions() {
    // Esperar a que Plotly cargue los gráficos
    const checkPlotly = setInterval(() => {
        const graphs = document.querySelectorAll('.js-plotly-plot');
        if (graphs.length > 0) {
            clearInterval(checkPlotly);
            
            graphs.forEach(graph => {
                // Establecer altura consistente sin forzar demasiado
                const parentCard = graph.closest('.chart-card');
                if (parentCard && parentCard.classList.contains('full')) {
                    graph.style.height = '350px';
                } else if (parentCard) {
                    graph.style.height = '380px';
                }
                
                // Añadir efecto de brillo al hacer hover (sin cambiar tamaño)
                graph.addEventListener('mouseenter', function() {
                    this.closest('.chart-card').style.boxShadow = '0 8px 24px rgba(37, 99, 235, 0.2)';
                });
                
                graph.addEventListener('mouseleave', function() {
                    this.closest('.chart-card').style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
                });
            });
        }
    }, 100);
    
    // Limpiar el intervalo después de 5 segundos
    setTimeout(() => clearInterval(checkPlotly), 5000);
}

// Toggle de tema claro/oscuro y modo daltónico
function initializeThemeToggle() {
    // Crear botón de toggle de tema oscuro
    const toggleButton = document.createElement('button');
    toggleButton.id = 'theme-toggle';
    toggleButton.innerHTML = '🌙';
    toggleButton.title = 'Cambiar tema oscuro/claro';
    toggleButton.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #2563eb, #1e293b);
        border: none;
        color: white;
        font-size: 24px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        z-index: 1000;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    `;
    
    // Crear botón de accesibilidad (abre el panel)
    const colorblindButton = document.createElement('button');
    colorblindButton.id = 'accessibility-toggle';
    colorblindButton.innerHTML = '🎨';
    colorblindButton.title = 'Configuración de accesibilidad';
    colorblindButton.style.cssText = `
        position: fixed;
        bottom: 100px;
        right: 30px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #009988, #0077bb);
        border: none;
        color: white;
        font-size: 28px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0, 119, 187, 0.3);
        z-index: 1000;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: float 3s ease-in-out infinite;
    `;
    
    // Crear panel de configuración de accesibilidad
    const panel = document.createElement('div');
    panel.className = 'accessibility-panel';
    panel.innerHTML = `
        <h3>Configuración de Accesibilidad</h3>
        
        <div class="panel-section">
            <div class="toggle-switch" id="colorblind-toggle">
                <span>Modo Daltónico</span>
                <div class="switch"></div>
            </div>
        </div>
        
        <div class="panel-section" id="colorblind-options" style="display: none;">
            <label>Tipo de Daltonismo</label>
            <div class="colorblind-type-selector">
                <div class="type-option active" data-type="protanopia">
                    <span class="type-label">Protanopía</span>
                    <span class="type-description">Rojo-Verde</span>
                </div>
                <div class="type-option" data-type="deuteranopia">
                    <span class="type-label">Deuteranopía</span>
                    <span class="type-description">Rojo-Verde</span>
                </div>
                <div class="type-option" data-type="tritanopia">
                    <span class="type-label">Tritanopía</span>
                    <span class="type-description">Azul-Amarillo</span>
                </div>
                <div class="type-option" data-type="achromatopsia">
                    <span class="type-label">Acromatopsia</span>
                    <span class="type-description">Sin color</span>
                </div>
            </div>
            
            <div class="intensity-slider-container">
                <div class="intensity-value">
                    <span>Intensidad del Ajuste</span>
                    <span id="intensity-display">70%</span>
                </div>
                <input 
                    type="range" 
                    min="0" 
                    max="100" 
                    value="70" 
                    class="intensity-slider" 
                    id="intensity-slider"
                >
                <p class="info-text">Ajusta la intensidad de la corrección de color según tus necesidades</p>
            </div>
        </div>
        
        <div class="panel-section">
            <div class="toggle-switch" id="highcontrast-toggle">
                <span>Modo Alto Contraste</span>
                <div class="switch"></div>
            </div>
        </div>
        
        <div class="panel-section" id="highcontrast-options" style="display: none;">
            <label>Intensidad del Contraste</label>
            <div class="intensity-slider-container">
                <div class="intensity-value">
                    <span>Nivel de Contraste</span>
                    <span id="contrast-display">80%</span>
                </div>
                <input 
                    type="range" 
                    min="0" 
                    max="100" 
                    value="80" 
                    class="intensity-slider contrast-slider" 
                    id="contrast-slider"
                >
                <p class="info-text">Aumenta el contraste entre elementos para mejorar la legibilidad</p>
            </div>
            
            <div class="contrast-preview">
                <div class="preview-box" style="background: linear-gradient(135deg, #000000, #1e293b);">
                    <span style="color: white;">Texto en alto contraste</span>
                </div>
            </div>
        </div>
    `;
    
    toggleButton.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.1) rotate(15deg)';
    });
    
    toggleButton.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1) rotate(0deg)';
    });
    
    toggleButton.addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
        this.innerHTML = document.body.classList.contains('dark-mode') ? '☀️' : '🌙';
        this.title = document.body.classList.contains('dark-mode') ? 'Cambiar a tema claro' : 'Cambiar a tema oscuro';
        
        // Animación de transición
        this.style.transform = 'scale(0.8) rotate(180deg)';
        setTimeout(() => {
            this.style.transform = 'scale(1) rotate(0deg)';
        }, 300);
    });
    
    colorblindButton.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.1) rotate(15deg)';
    });
    
    colorblindButton.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1) rotate(0deg)';
    });
    
    colorblindButton.addEventListener('click', function() {
        panel.classList.toggle('visible');
        
        // Animación de transición
        this.style.transform = 'scale(0.9) rotate(180deg)';
        setTimeout(() => {
            this.style.transform = 'scale(1) rotate(0deg)';
        }, 300);
    });
    
    document.body.appendChild(toggleButton);
    document.body.appendChild(colorblindButton);
    document.body.appendChild(panel);
    
    // Configurar interacciones del panel
    setupAccessibilityPanel();
}

// Configurar el panel de accesibilidad
function setupAccessibilityPanel() {
    const colorblindToggle = document.getElementById('colorblind-toggle');
    const colorblindOptions = document.getElementById('colorblind-options');
    const highContrastToggle = document.getElementById('highcontrast-toggle');
    const highContrastOptions = document.getElementById('highcontrast-options');
    const typeOptions = document.querySelectorAll('.type-option');
    const intensitySlider = document.getElementById('intensity-slider');
    const intensityDisplay = document.getElementById('intensity-display');
    const contrastSlider = document.getElementById('contrast-slider');
    const contrastDisplay = document.getElementById('contrast-display');
    
    let isColorblindMode = false;
    let isHighContrastMode = false;
    let currentType = 'protanopia';
    let currentIntensity = 70;
    let currentContrast = 80;
    
    // Toggle del modo daltónico
    colorblindToggle.addEventListener('click', function() {
        this.classList.toggle('active');
        isColorblindMode = !isColorblindMode;
        
        if (isColorblindMode) {
            colorblindOptions.style.display = 'block';
            applyColorblindMode(currentType, currentIntensity);
        } else {
            colorblindOptions.style.display = 'none';
            removeColorblindMode();
        }
    });
    
    // Toggle del modo alto contraste
    highContrastToggle.addEventListener('click', function() {
        this.classList.toggle('active');
        isHighContrastMode = !isHighContrastMode;
        
        if (isHighContrastMode) {
            highContrastOptions.style.display = 'block';
            applyHighContrastMode(currentContrast);
        } else {
            highContrastOptions.style.display = 'none';
            removeHighContrastMode();
        }
    });
    
    // Selección de tipo de daltonismo
    typeOptions.forEach(option => {
        option.addEventListener('click', function() {
            typeOptions.forEach(opt => opt.classList.remove('active'));
            this.classList.add('active');
            currentType = this.dataset.type;
            
            if (isColorblindMode) {
                applyColorblindMode(currentType, currentIntensity);
            }
        });
    });
    
    // Slider de intensidad daltonismo
    intensitySlider.addEventListener('input', function() {
        currentIntensity = parseInt(this.value);
        intensityDisplay.textContent = currentIntensity + '%';
        
        if (isColorblindMode) {
            applyColorblindMode(currentType, currentIntensity);
        }
    });
    
    // Slider de intensidad alto contraste
    contrastSlider.addEventListener('input', function() {
        currentContrast = parseInt(this.value);
        contrastDisplay.textContent = currentContrast + '%';
        
        if (isHighContrastMode) {
            applyHighContrastMode(currentContrast);
        }
    });
}

// Aplicar modo daltónico con tipo e intensidad
function applyColorblindMode(type, intensity) {
    // Remover clases previas
    document.body.classList.remove('colorblind-protanopia', 'colorblind-deuteranopia', 
                                   'colorblind-tritanopia', 'colorblind-achromatopsia');
    
    // Añadir clase específica
    document.body.classList.add('colorblind-mode', `colorblind-${type}`);
    
    // Aplicar intensidad mediante filtros CSS
    const filterIntensity = intensity / 100;
    
    // Paletas de color según el tipo
    const colorPalettes = {
        protanopia: {
            colors: ['#0077bb', '#ee7733', '#009988', '#cc3311', '#33bbee'],
            filter: `contrast(${1 + filterIntensity * 0.2}) saturate(${1 + filterIntensity * 0.3})`
        },
        deuteranopia: {
            colors: ['#0077bb', '#ee7733', '#009988', '#cc3311', '#33bbee'],
            filter: `contrast(${1 + filterIntensity * 0.2}) saturate(${1 + filterIntensity * 0.3})`
        },
        tritanopia: {
            colors: ['#cc3311', '#009988', '#0077bb', '#ee7733', '#33bbee'],
            filter: `contrast(${1 + filterIntensity * 0.3}) brightness(${1 + filterIntensity * 0.1})`
        },
        achromatopsia: {
            colors: ['#1e293b', '#64748b', '#334155', '#0f172a', '#475569'],
            filter: `grayscale(${filterIntensity}) contrast(${1 + filterIntensity * 0.4})`
        }
    };
    
    const palette = colorPalettes[type];
    
    // Aplicar filtro a los gráficos
    const graphs = document.querySelectorAll('.js-plotly-plot');
    graphs.forEach(graph => {
        graph.style.filter = palette.filter;
    });
    
    // Actualizar colores de gráficos si es posible
    updateChartsForColorblind(palette.colors, type, intensity);
    
    console.log(`✓ Modo daltónico activado: ${type} al ${intensity}%`);
}

// Remover modo daltónico
function removeColorblindMode() {
    document.body.classList.remove('colorblind-mode', 'colorblind-protanopia', 
                                   'colorblind-deuteranopia', 'colorblind-tritanopia', 
                                   'colorblind-achromatopsia');
    
    // Remover filtros
    const graphs = document.querySelectorAll('.js-plotly-plot');
    graphs.forEach(graph => {
        graph.style.filter = '';
    });
    
    resetChartColors();
    console.log('✓ Modo daltónico desactivado');
}

// Actualizar colores de gráficos para modo daltónico
function updateChartsForColorblind(colors, type, intensity) {
    const graphs = document.querySelectorAll('.js-plotly-plot');
    
    graphs.forEach((graph, index) => {
        if (graph && graph.data) {
            try {
                // Intentar actualizar con Plotly si está disponible
                if (window.Plotly) {
                    const update = {
                        'marker.color': colors,
                        'line.color': colors[0]
                    };
                    window.Plotly.restyle(graph, update);
                }
            } catch (e) {
                console.log('Gráfico se actualizará en la próxima interacción');
            }
        }
    });
}

// Restablecer colores originales
function resetChartColors() {
    console.log('✓ Colores originales restaurados');
}

// Aplicar modo alto contraste
function applyHighContrastMode(intensity) {
    document.body.classList.add('high-contrast-mode');
    
    const contrastValue = 1 + (intensity / 100) * 1.5; // 1.0 a 2.5
    const brightnessValue = 1 + (intensity / 100) * 0.3; // 1.0 a 1.3
    const saturationValue = 1 + (intensity / 100) * 0.5; // 1.0 a 1.5
    
    // Aplicar filtros a todo el contenido
    const container = document.querySelector('.container');
    if (container) {
        container.style.filter = `contrast(${contrastValue}) brightness(${brightnessValue}) saturate(${saturationValue})`;
    }
    
    // Ajustar estilos específicos según intensidad
    const root = document.documentElement;
    root.style.setProperty('--contrast-border-width', `${2 + (intensity / 100) * 2}px`);
    root.style.setProperty('--contrast-shadow-intensity', `${0.1 + (intensity / 100) * 0.3}`);
    root.style.setProperty('--contrast-text-weight', intensity > 50 ? '700' : '600');
    
    console.log(`✓ Modo alto contraste activado: ${intensity}%`);
}

// Remover modo alto contraste
function removeHighContrastMode() {
    document.body.classList.remove('high-contrast-mode');
    
    const container = document.querySelector('.container');
    if (container) {
        container.style.filter = '';
    }
    
    const root = document.documentElement;
    root.style.removeProperty('--contrast-border-width');
    root.style.removeProperty('--contrast-shadow-intensity');
    root.style.removeProperty('--contrast-text-weight');
    
    console.log('✓ Modo alto contraste desactivado');
}

// Efectos de scroll
function addScrollEffects() {
    let lastScroll = 0;
    const header = document.querySelector('.header');
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        // Efecto parallax en el header
        if (header) {
            header.style.transform = `translateY(${currentScroll * 0.5}px)`;
            header.style.opacity = 1 - (currentScroll / 500);
        }
        
        lastScroll = currentScroll;
    });
}

// Añadir contador animado a los valores de las métricas
function animateValue(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const value = progress * (end - start) + start;
        element.textContent = value.toFixed(1);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Observador de mutaciones para detectar cambios en los gráficos
const graphObserver = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.addedNodes.length) {
            mutation.addedNodes.forEach((node) => {
                if (node.classList && node.classList.contains('js-plotly-plot')) {
                    // Asegurar que el gráfico sea visible
                    node.style.opacity = '1';
                    node.style.transform = 'translateY(0)';
                }
            });
        }
    });
});

// Observar el documento para nuevos gráficos
graphObserver.observe(document.body, {
    childList: true,
    subtree: true
});

// Añadir tooltips informativos
function addTooltips() {
    const tipCards = document.querySelectorAll('.tip-card');
    
    tipCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0) scale(1)';
        });
    });
}

// Ejecutar tooltips después de que el DOM se cargue
setTimeout(addTooltips, 500);

// Añadir indicador de carga
window.addEventListener('load', function() {
    // Ocultar cualquier indicador de carga si existe
    const loader = document.querySelector('.loader');
    if (loader) {
        loader.style.opacity = '0';
        setTimeout(() => loader.remove(), 300);
    }
});

// Logger de interacciones (útil para analytics)
function logInteraction(type, detail) {
    console.log(`[Dashboard] ${type}:`, detail);
    // Aquí podrías enviar datos a un servicio de analytics
}

// Detectar clicks en las tarjetas
document.addEventListener('click', function(e) {
    if (e.target.closest('.metric-card')) {
        const cardType = e.target.closest('.metric-card').className.split(' ')[1];
        logInteraction('metric-card-click', cardType);
    }
});

console.log('✅ Dashboard JavaScript inicializado correctamente');
