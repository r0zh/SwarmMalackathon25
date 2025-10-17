// Custom JavaScript para mejorar la interactividad del Dashboard de Bienestar Mental

// Esperar a que el DOM esté completamente cargado
document.addEventListener("DOMContentLoaded", function () {
  console.log("Dashboard de Bienestar Mental - JavaScript Cargado");

  // Inicializar todas las funcionalidades
  initializeAnimations();
  initializeMetricCards();
  initializeChartInteractions();
  addScrollEffects();
  initializeAccessibilityPanel();
});

// Animaciones de entrada mejoradas para las tarjetas
function initializeAnimations() {
  // Asegurar que todas las tarjetas sean visibles desde el inicio
  document.querySelectorAll(".metric-card, .chart-card").forEach((card) => {
    card.classList.add("visible");
    card.style.opacity = "1";
    card.style.transform = "translateY(0)";
  });

  // Observer para animaciones futuras (opcional)
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          entry.target.style.opacity = "1";
          entry.target.style.transform = "translateY(0)";
        }
      });
    },
    {
      threshold: 0.1,
    }
  );

  // Observar todas las tarjetas
  document.querySelectorAll(".metric-card, .chart-card").forEach((card) => {
    observer.observe(card);
  });
}

// Interactividad mejorada para las tarjetas de métricas
function initializeMetricCards() {
  const metricCards = document.querySelectorAll(".metric-card");

  metricCards.forEach((card) => {
    // Efecto de pulso al hacer hover
    card.addEventListener("mouseenter", function () {
      this.style.transform = "translateY(-8px) scale(1.02)";
    });

    card.addEventListener("mouseleave", function () {
      this.style.transform = "translateY(0) scale(1)";
    });

    // Click para ver más detalles (simulado)
    card.addEventListener("click", function () {
      const metricValue = this.querySelector(".metric-value");
      const originalValue = metricValue.textContent;

      // Animación de actualización
      metricValue.style.transform = "scale(1.1)";
      metricValue.style.color = "#2563eb";

      setTimeout(() => {
        metricValue.style.transform = "scale(1)";
        metricValue.style.color = "";
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
    const particle = document.createElement("div");
    particle.className = "particle";
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

    particle.animate(
      [
        { transform: "translate(0, 0)", opacity: 1 },
        { transform: `translate(${tx}px, ${ty}px)`, opacity: 0 },
      ],
      {
        duration: 1000,
        easing: "cubic-bezier(0, .9, .57, 1)",
      }
    ).onfinish = () => particle.remove();
  }
}

// Mejorar interacciones con gráficos de Plotly
function initializeChartInteractions() {
  // Esperar a que Plotly cargue los gráficos
  const checkPlotly = setInterval(() => {
    const graphs = document.querySelectorAll(".js-plotly-plot");
    if (graphs.length > 0) {
      clearInterval(checkPlotly);

      graphs.forEach((graph) => {
        // Establecer altura consistente sin forzar demasiado
        const parentCard = graph.closest(".chart-card");
        if (parentCard && parentCard.classList.contains("full")) {
          graph.style.height = "350px";
        } else if (parentCard) {
          graph.style.height = "380px";
        }

        // Añadir efecto de brillo al hacer hover (sin cambiar tamaño)
        graph.addEventListener("mouseenter", function () {
          this.closest(".chart-card").style.boxShadow =
            "0 8px 24px rgba(37, 99, 235, 0.2)";
        });

        graph.addEventListener("mouseleave", function () {
          this.closest(".chart-card").style.boxShadow =
            "0 1px 3px rgba(0, 0, 0, 0.1)";
        });
      });
    }
  }, 100);

  // Limpiar el intervalo después de 5 segundos
  setTimeout(() => clearInterval(checkPlotly), 5000);
}

// Efectos de scroll
function addScrollEffects() {
  let lastScroll = 0;
  const header = document.querySelector(".header");
  const isMobile = window.innerWidth <= 768;

  window.addEventListener("scroll", () => {
    const currentScroll = window.pageYOffset;

    // Efecto parallax en el header (reducido en móvil)
    if (header) {
      const parallaxSpeed = isMobile ? 0.3 : 0.5;
      const maxScroll = isMobile ? 300 : 500;
      header.style.transform = `translateY(${
        Math.min(currentScroll, maxScroll) * parallaxSpeed
      }px)`;
      header.style.opacity = Math.max(0.3, 1 - currentScroll / maxScroll);
    }

    lastScroll = currentScroll;
  });

  // Reajustar en cambio de tamaño de ventana
  window.addEventListener("resize", () => {
    const newIsMobile = window.innerWidth <= 768;
    if (newIsMobile !== isMobile) {
      location.reload(); // Recargar si cambia entre móvil y escritorio
    }
  });
}

// Inicializar panel de accesibilidad
function initializeAccessibilityPanel() {
  // Crear botón de accesibilidad (abre el panel) - LADO IZQUIERDO
  const colorblindButton = document.createElement("button");
  colorblindButton.id = "accessibility-toggle";
  colorblindButton.innerHTML = "🎨";
  colorblindButton.title = "Configuración de accesibilidad";
  colorblindButton.style.cssText = `
        position: fixed;
        bottom: 30px;
        left: 30px;
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
  const panel = document.createElement("div");
  panel.className = "accessibility-panel";
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
        
        <div class="panel-section">
            <label>Tamaño de Letra</label>
            <div class="font-size-selector">
                <div class="size-option" data-size="small">
                    <span class="size-icon" style="font-size: 14px;">A</span>
                    <span class="size-label">Pequeño</span>
                </div>
                <div class="size-option active" data-size="normal">
                    <span class="size-icon" style="font-size: 18px;">A</span>
                    <span class="size-label">Normal</span>
                </div>
                <div class="size-option" data-size="large">
                    <span class="size-icon" style="font-size: 22px;">A</span>
                    <span class="size-label">Grande</span>
                </div>
                <div class="size-option" data-size="xlarge">
                    <span class="size-icon" style="font-size: 26px;">A</span>
                    <span class="size-label">Muy Grande</span>
                </div>
            </div>
            <p class="info-text">Ajusta el tamaño del texto para mejorar la legibilidad</p>
        </div>
    `;

  colorblindButton.addEventListener("mouseenter", function () {
    this.style.transform = "scale(1.1) rotate(15deg)";
  });

  colorblindButton.addEventListener("mouseleave", function () {
    this.style.transform = "scale(1) rotate(0deg)";
  });

  colorblindButton.addEventListener("click", function () {
    panel.classList.toggle("visible");

    // Animación de transición
    this.style.transform = "scale(0.9) rotate(180deg)";
    setTimeout(() => {
      this.style.transform = "scale(1) rotate(0deg)";
    }, 300);

    // Manage focus trap
    if (panel.classList.contains("visible")) {
      setupFocusTrap(panel);
    } else {
      removeFocusTrap();
    }
  });

  // Close panel with Escape key
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && panel.classList.contains("visible")) {
      panel.classList.remove("visible");
      colorblindButton.focus(); // Return focus to trigger button
    }
  });

  document.body.appendChild(colorblindButton);
  document.body.appendChild(panel);

  // Configurar interacciones del panel
  setupAccessibilityPanel();
}

// Configurar el panel de accesibilidad
function setupAccessibilityPanel() {
  const colorblindToggle = document.getElementById("colorblind-toggle");
  const colorblindOptions = document.getElementById("colorblind-options");
  const highContrastToggle = document.getElementById("highcontrast-toggle");
  const highContrastOptions = document.getElementById("highcontrast-options");
  const typeOptions = document.querySelectorAll(".type-option");
  const intensitySlider = document.getElementById("intensity-slider");
  const intensityDisplay = document.getElementById("intensity-display");
  const contrastSlider = document.getElementById("contrast-slider");
  const contrastDisplay = document.getElementById("contrast-display");
  const sizeOptions = document.querySelectorAll(".size-option");

  let isColorblindMode = false;
  let isHighContrastMode = false;
  let currentType = "protanopia";
  let currentIntensity = 70;
  let currentContrast = 80;
  let currentFontSize = "normal";

  // Toggle del modo daltónico
  colorblindToggle.addEventListener("click", function () {
    const activeElement = document.activeElement;

    this.classList.toggle("active");
    isColorblindMode = !isColorblindMode;

    if (isColorblindMode) {
      colorblindOptions.style.display = "block";
      applyColorblindMode(currentType, currentIntensity);
    } else {
      colorblindOptions.style.display = "none";
      removeColorblindMode();
    }

    // Restore focus
    setTimeout(() => {
      if (activeElement && activeElement !== document.body) {
        activeElement.focus();
      }
    }, 50);
  });

  // Toggle del modo alto contraste
  highContrastToggle.addEventListener("click", function () {
    const activeElement = document.activeElement;

    this.classList.toggle("active");
    isHighContrastMode = !isHighContrastMode;

    if (isHighContrastMode) {
      highContrastOptions.style.display = "block";
      applyHighContrastMode(currentContrast);
    } else {
      highContrastOptions.style.display = "none";
      removeHighContrastMode();
    }

    // Restore focus
    setTimeout(() => {
      if (activeElement && activeElement !== document.body) {
        activeElement.focus();
      }
    }, 50);
  });

  // Selección de tipo de daltonismo
  typeOptions.forEach((option) => {
    option.addEventListener("click", function () {
      typeOptions.forEach((opt) => opt.classList.remove("active"));
      this.classList.add("active");
      currentType = this.dataset.type;

      if (isColorblindMode) {
        applyColorblindMode(currentType, currentIntensity);
      }
    });
  });

  // Slider de intensidad daltonismo
  intensitySlider.addEventListener("input", function () {
    currentIntensity = parseInt(this.value);
    intensityDisplay.textContent = currentIntensity + "%";

    // Actualizar el fondo del slider
    this.style.setProperty("--slider-value", currentIntensity + "%");

    if (isColorblindMode) {
      applyColorblindMode(currentType, currentIntensity);
    }
  });

  // Inicializar el valor del slider
  intensitySlider.style.setProperty("--slider-value", "70%");

  // Slider de intensidad alto contraste
  contrastSlider.addEventListener("input", function () {
    currentContrast = parseInt(this.value);
    contrastDisplay.textContent = currentContrast + "%";

    // Actualizar el fondo del slider
    this.style.setProperty("--slider-value", currentContrast + "%");

    if (isHighContrastMode) {
      applyHighContrastMode(currentContrast);
    }
  });

  // Inicializar el valor del slider
  contrastSlider.style.setProperty("--slider-value", "80%");

  // Selección de tamaño de letra
  sizeOptions.forEach((option) => {
    option.addEventListener("click", function () {
      sizeOptions.forEach((opt) => opt.classList.remove("active"));
      this.classList.add("active");
      currentFontSize = this.dataset.size;
      applyFontSize(currentFontSize);
    });
  });
}

// Aplicar modo daltónico con tipo e intensidad
function applyColorblindMode(type, intensity) {
  // Remover clases previas
  document.body.classList.remove(
    "colorblind-protanopia",
    "colorblind-deuteranopia",
    "colorblind-tritanopia",
    "colorblind-achromatopsia"
  );

  // Añadir clase específica
  document.body.classList.add("colorblind-mode", `colorblind-${type}`);

  // Aplicar intensidad mediante CSS filters
  const intensityValue = intensity / 100; // Convertir de 0-100 a 0-1
  const charts = document.querySelectorAll(".js-plotly-plot, .chart-card");

  charts.forEach((chart) => {
    // Calcular valores de filtro basados en el tipo y la intensidad
    let filterValue = "";

    switch (type) {
      case "protanopia":
      case "deuteranopia":
        // Rojo-Verde: ajustar contraste y saturación
        const contrast = 1 + 0.2 * intensityValue;
        const saturate = 1 + 0.3 * intensityValue;
        filterValue = `contrast(${contrast}) saturate(${saturate})`;
        break;

      case "tritanopia":
        // Azul-Amarillo: ajustar contraste y brillo
        const contrastT = 1 + 0.3 * intensityValue;
        const brightness = 1 + 0.1 * intensityValue;
        filterValue = `contrast(${contrastT}) brightness(${brightness})`;
        break;

      case "achromatopsia":
        // Sin color: escala de grises con contraste
        const grayscale = 0.7 * intensityValue;
        const contrastA = 1 + 0.4 * intensityValue;
        filterValue = `grayscale(${grayscale}) contrast(${contrastA})`;
        break;
    }

    chart.style.filter = filterValue;
  });

  // Actualizar colores de gráficos si es posible
  updateChartsForColorblind(type, intensity);

  console.log(`✓ Modo daltónico activado: ${type} al ${intensity}%`);
}

// Remover modo daltónico
function removeColorblindMode() {
  document.body.classList.remove(
    "colorblind-mode",
    "colorblind-protanopia",
    "colorblind-deuteranopia",
    "colorblind-tritanopia",
    "colorblind-achromatopsia"
  );

  // Remover filtros aplicados
  const charts = document.querySelectorAll(".js-plotly-plot, .chart-card");
  charts.forEach((chart) => {
    chart.style.filter = "";
  });

  resetChartColors();
  console.log("✓ Modo daltónico desactivado");
}

// Actualizar colores de gráficos para modo daltónico
function updateChartsForColorblind(type, intensity) {
  // Define color palettes for each type
  const colorPalettes = {
    protanopia: ["#0077bb", "#ee7733", "#009988", "#cc3311", "#33bbee"],
    deuteranopia: ["#0077bb", "#ee7733", "#009988", "#cc3311", "#33bbee"],
    tritanopia: ["#cc3311", "#009988", "#0077bb", "#ee7733", "#33bbee"],
    achromatopsia: ["#1e293b", "#64748b", "#334155", "#0f172a", "#475569"],
  };

  const colors = colorPalettes[type];
  const graphs = document.querySelectorAll(".js-plotly-plot");

  graphs.forEach((graph, index) => {
    if (graph && graph.data) {
      try {
        // Intentar actualizar con Plotly si está disponible
        if (window.Plotly) {
          const update = {
            "marker.color": colors,
            "line.color": colors[0],
          };
          window.Plotly.restyle(graph, update);
        }
      } catch (e) {
        console.log("Gráfico se actualizará en la próxima interacción");
      }
    }
  });
}

// Restablecer colores originales
function resetChartColors() {
  console.log("✓ Colores originales restaurados");
}

// Aplicar modo alto contraste
function applyHighContrastMode(intensity) {
  document.body.classList.add("high-contrast-mode");

  // Aplicar intensidad mediante CSS filters
  const intensityValue = intensity / 100;
  const contrast = 1 + 0.8 * intensityValue; // De 1.0 a 1.8
  const brightness = 1 + 0.15 * intensityValue; // De 1.0 a 1.15
  const saturate = 1 + 0.25 * intensityValue; // De 1.0 a 1.25

  const container = document.querySelector(".container");
  if (container) {
    container.style.filter = `contrast(${contrast}) brightness(${brightness}) saturate(${saturate})`;
  }

  console.log(`✓ Modo alto contraste activado: ${intensity}%`);
}

// Remover modo alto contraste
function removeHighContrastMode() {
  document.body.classList.remove("high-contrast-mode");

  // Remover filtros aplicados
  const container = document.querySelector(".container");
  if (container) {
    container.style.filter = "";
  }

  console.log("✓ Modo alto contraste desactivado");
}

// Aplicar tamaño de letra
function applyFontSize(size) {
  // Remover clases previas
  document.body.classList.remove(
    "font-small",
    "font-normal",
    "font-large",
    "font-xlarge"
  );

  // Añadir nueva clase
  document.body.classList.add(`font-${size}`);

  console.log(`✓ Tamaño de letra ajustado: ${size}`);
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
        if (node.classList && node.classList.contains("js-plotly-plot")) {
          // Asegurar que el gráfico sea visible
          node.style.opacity = "1";
          node.style.transform = "translateY(0)";

          // Aplicar tema oscuro si está activado
          if (document.body.classList.contains("dark-mode")) {
            setTimeout(() => {
              updateAllChartsTheme("dark");
            }, 100);
          }
        }
      });
    }
  });
});

// Observar el documento para nuevos gráficos
graphObserver.observe(document.body, {
  childList: true,
  subtree: true,
});

// Añadir tooltips informativos
function addTooltips() {
  const tipCards = document.querySelectorAll(".tip-card");

  tipCards.forEach((card) => {
    card.addEventListener("mouseenter", function () {
      this.style.transform = "translateX(8px) scale(1.02)";
    });

    card.addEventListener("mouseleave", function () {
      this.style.transform = "translateX(0) scale(1)";
    });
  });
}

// Ejecutar tooltips después de que el DOM se cargue
setTimeout(addTooltips, 500);

// Setup external dark mode toggle button
function setupDarkModeButton() {
  const darkModeBtn = document.getElementById("dark-mode-toggle-btn");
  if (!darkModeBtn) {
    console.log("Dark mode button not found, retrying...");
    return;
  }

  let isDarkMode = false;

  // Update button icon based on theme
  function updateButtonIcon() {
    darkModeBtn.textContent = isDarkMode ? "☀️" : "🌙";
    darkModeBtn.title = isDarkMode
      ? "Cambiar a modo claro"
      : "Cambiar a modo oscuro";
  }

  // Toggle dark mode
  darkModeBtn.addEventListener("click", function (e) {
    e.preventDefault();
    e.stopPropagation();

    isDarkMode = !isDarkMode;

    if (isDarkMode) {
      applyDarkMode();
    } else {
      removeDarkMode();
    }

    updateButtonIcon();

    console.log("✓ Dark mode toggled:", isDarkMode ? "ON" : "OFF");
  });

  // Initialize icon
  updateButtonIcon();

  console.log("✓ Dark mode button initialized");
}

// Añadir indicador de carga
window.addEventListener("load", function () {
  // Ocultar cualquier indicador de carga si existe
  const loader = document.querySelector(".loader");
  if (loader) {
    loader.style.opacity = "0";
    setTimeout(() => loader.remove(), 300);
  }
});

// Logger de interacciones (útil para analytics)
function logInteraction(type, detail) {
  console.log(`[Dashboard] ${type}:`, detail);
  // Aquí podrías enviar datos a un servicio de analytics
}

// Detectar clicks en las tarjetas
document.addEventListener("click", function (e) {
  if (e.target.closest(".metric-card")) {
    const cardType = e.target.closest(".metric-card").className.split(" ")[1];
    logInteraction("metric-card-click", cardType);
  }
});

// Focus trap management for accessibility panel
function setupFocusTrap(panel) {
  const focusableElements = panel.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );

  if (focusableElements.length === 0) return;

  const firstElement = focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];

  // Store for cleanup
  panel._focusTrapHandler = function (e) {
    if (e.key !== "Tab") return;

    if (e.shiftKey) {
      if (document.activeElement === firstElement) {
        e.preventDefault();
        lastElement.focus();
      }
    } else {
      if (document.activeElement === lastElement) {
        e.preventDefault();
        firstElement.focus();
      }
    }
  };

  panel.addEventListener("keydown", panel._focusTrapHandler);

  // Focus first element
  setTimeout(() => firstElement.focus(), 100);
}

function removeFocusTrap() {
  const panel = document.querySelector(".accessibility-panel");
  if (panel && panel._focusTrapHandler) {
    panel.removeEventListener("keydown", panel._focusTrapHandler);
    delete panel._focusTrapHandler;
  }
}

// ===================================
// DARK MODE FUNCTIONS
// ===================================

function applyDarkMode() {
  // Aplicar clase dark-mode al body
  document.body.classList.add("dark-mode");

  // Actualizar todos los gráficos de Plotly con tema oscuro
  updateAllChartsTheme("dark");

  console.log("✓ Modo oscuro activado");
}

function removeDarkMode() {
  // Remover clase dark-mode del body
  document.body.classList.remove("dark-mode");

  // Restaurar todos los gráficos de Plotly con tema claro
  updateAllChartsTheme("light");

  console.log("✓ Modo oscuro desactivado");
}

function updateAllChartsTheme(theme) {
  const graphs = document.querySelectorAll(".js-plotly-plot");

  if (!window.Plotly) {
    console.log(
      "Plotly no está disponible aún, los gráficos se actualizarán en la próxima recarga"
    );
    return;
  }

  graphs.forEach((graph) => {
    try {
      if (graph && graph.data && graph.layout) {
        const isDark = theme === "dark";

        // Colores del tema
        const colors = {
          background: isDark ? "rgba(30, 41, 59, 0)" : "rgba(255,255,255,0)",
          plot_bg: isDark ? "rgba(15, 23, 42, 0.3)" : "rgba(248,250,252,0.5)",
          text: isDark ? "#cbd5e1" : "#1e293b",
          title: isDark ? "#f1f5f9" : "#0f172a",
          grid: isDark ? "rgba(71, 85, 105, 0.3)" : "#e2e8f0",
          legend_bg: isDark ? "rgba(30, 41, 59, 0.9)" : "rgba(255,255,255,0.9)",
          legend_border: isDark ? "#475569" : "#e2e8f0",
        };

        // Actualizar layout del gráfico
        const layoutUpdate = {
          paper_bgcolor: colors.background,
          plot_bgcolor: colors.plot_bg,
          font: {
            color: colors.text,
            family: "system-ui, -apple-system, sans-serif",
            size: 11,
          },
          title: {
            font: {
              color: colors.title,
              size: 14,
              family: "system-ui, -apple-system, sans-serif",
            },
          },
          xaxis: {
            gridcolor: colors.grid,
            color: colors.text,
          },
          yaxis: {
            gridcolor: colors.grid,
            color: colors.text,
          },
          legend: {
            bgcolor: colors.legend_bg,
            bordercolor: colors.legend_border,
            font: {
              color: colors.text,
            },
          },
          hoverlabel: {
            bgcolor: isDark ? "#1e293b" : "white",
            font: {
              color: isDark ? "#e2e8f0" : "#1e293b",
              size: 11,
              family: "system-ui, -apple-system, sans-serif",
            },
          },
        };

        // Aplicar actualización
        window.Plotly.relayout(graph, layoutUpdate);

        // Actualizar ejes si existen múltiples
        const axisUpdates = {};
        Object.keys(graph.layout).forEach((key) => {
          if (key.startsWith("xaxis") || key.startsWith("yaxis")) {
            axisUpdates[key + ".gridcolor"] = colors.grid;
            axisUpdates[key + ".color"] = colors.text;
          }
        });

        if (Object.keys(axisUpdates).length > 0) {
          window.Plotly.relayout(graph, axisUpdates);
        }
      }
    } catch (e) {
      console.log("Error actualizando gráfico:", e);
    }
  });

  console.log(`✓ ${graphs.length} gráficos actualizados al tema ${theme}`);
}

// Initialize dark mode button when DOM is ready
function initDarkModeWithRetry() {
  let attempts = 0;
  const maxAttempts = 10;

  function trySetup() {
    attempts++;
    const btn = document.getElementById("dark-mode-toggle-btn");

    if (btn) {
      setupDarkModeButton();
    } else if (attempts < maxAttempts) {
      console.log(`Waiting for dark mode button... (attempt ${attempts})`);
      setTimeout(trySetup, 200);
    } else {
      console.log("Dark mode button not found after max attempts");
    }
  }

  trySetup();
}

// Start initialization
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initDarkModeWithRetry);
} else {
  // DOM already loaded, try immediately
  setTimeout(initDarkModeWithRetry, 100);
}

console.log("✅ Dashboard JavaScript inicializado correctamente");
