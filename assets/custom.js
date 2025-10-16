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

// Toggle de tema claro/oscuro
function initializeThemeToggle() {
    // Crear botón de toggle
    const toggleButton = document.createElement('button');
    toggleButton.id = 'theme-toggle';
    toggleButton.innerHTML = '🌙';
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
    
    toggleButton.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.1) rotate(15deg)';
    });
    
    toggleButton.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1) rotate(0deg)';
    });
    
    toggleButton.addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
        this.innerHTML = document.body.classList.contains('dark-mode') ? '☀️' : '🌙';
        
        // Animación de transición
        this.style.transform = 'scale(0.8) rotate(180deg)';
        setTimeout(() => {
            this.style.transform = 'scale(1) rotate(0deg)';
        }, 300);
    });
    
    document.body.appendChild(toggleButton);
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
