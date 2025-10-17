// Google reCAPTCHA Enterprise Integration
// Site Key: 6LeHfuwrAAAAAE-FOdiuq6iB9Wdbh5VRbWGBlwxK

// Inicializar reCAPTCHA cuando la página carga
document.addEventListener("DOMContentLoaded", function () {
  console.log("reCAPTCHA Enterprise inicializando...");

  // Verificar que grecaptcha esté disponible
  if (typeof grecaptcha !== "undefined") {
    console.log("✅ grecaptcha disponible");
    initializeRecaptcha();
  } else {
    console.warn("⚠️ Esperando a que reCAPTCHA se cargue...");
    // Reintentar cada 500ms hasta que se cargue
    const checkInterval = setInterval(function () {
      if (typeof grecaptcha !== "undefined") {
        clearInterval(checkInterval);
        console.log("✅ grecaptcha cargado correctamente");
        initializeRecaptcha();
      }
    }, 500);
  }
});

// Inicializar reCAPTCHA
function initializeRecaptcha() {
  // Ejecutar reCAPTCHA automáticamente al cargar la página
  executeRecaptcha("PAGE_LOAD");

  // Añadir listeners a elementos interactivos
  setupRecaptchaListeners();
}

// Configurar listeners para diferentes acciones
function setupRecaptchaListeners() {
  // Detectar clics en tarjetas de métricas
  const metricCards = document.querySelectorAll(".metric-card");
  metricCards.forEach(function (card) {
    card.addEventListener("click", function (e) {
      executeRecaptcha("METRIC_CARD_CLICK");
    });
  });

  // Detectar cambios en el dropdown
  const dropdown = document.getElementById("dropdown-metrica");
  if (dropdown) {
    const dropdownContainer = dropdown.parentElement;
    if (dropdownContainer) {
      dropdownContainer.addEventListener("click", function (e) {
        executeRecaptcha("DROPDOWN_INTERACTION");
      });
    }
  }

  // Detectar clics en botones de accesibilidad
  const accessibilityButton = document.getElementById("accessibility-toggle");
  if (accessibilityButton) {
    accessibilityButton.addEventListener("click", function (e) {
      executeRecaptcha("ACCESSIBILITY_TOGGLE");
    });
  }
}

// Función principal para ejecutar reCAPTCHA
function executeRecaptcha(action) {
  try {
    if (typeof grecaptcha === "undefined") {
      console.warn("reCAPTCHA no está disponible aún");
      return null;
    }

    grecaptcha.ready(function () {
      grecaptcha
        .execute("6LeHfuwrAAAAAE-FOdiuq6iB9Wdbh5VRbWGBlwxK", {
          action: action,
        })
        .then(function (token) {
          console.log("✅ reCAPTCHA token generado para acción: " + action);
          console.log("Token: " + token.substring(0, 50) + "...");

          // Aquí puedes enviar el token a tu backend para verificación
          // Por ejemplo: sendTokenToBackend(token, action);

          return token;
        })
        .catch(function (error) {
          console.error("❌ Error generando token:", error);
        });
    });
  } catch (error) {
    console.error("❌ Error ejecutando reCAPTCHA:", error);
    return null;
  }
}

// Función opcional para enviar el token al backend
function sendTokenToBackend(token, action) {
  fetch("/api/verify-recaptcha", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      token: token,
      action: action,
    }),
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (result) {
      console.log("Respuesta del servidor:", result);
      return result;
    })
    .catch(function (error) {
      console.error("Error enviando token al backend:", error);
      return null;
    });
}

// Función para manejar clics con reCAPTCHA
function onClick(e) {
  e.preventDefault();
  grecaptcha.ready(function () {
    grecaptcha
      .execute("6LeHfuwrAAAAAE-FOdiuq6iB9Wdbh5VRbWGBlwxK", {
        action: "LOGIN",
      })
      .then(function (token) {
        console.log(
          "Token de LOGIN generado: " + token.substring(0, 50) + "..."
        );
      });
  });
}

// Hacer la función onClick disponible globalmente
window.onClickWithRecaptcha = onClick;

// Función para obtener un token bajo demanda
window.getRecaptchaToken = function (action) {
  action = action || "CUSTOM_ACTION";
  return new Promise(function (resolve, reject) {
    grecaptcha.ready(function () {
      grecaptcha
        .execute("6LeHfuwrAAAAAE-FOdiuq6iB9Wdbh5VRbWGBlwxK", {
          action: action,
        })
        .then(resolve)
        .catch(reject);
    });
  });
};

console.log("📋 reCAPTCHA Enterprise script cargado. Acciones disponibles:");
console.log("   - PAGE_LOAD: Al cargar la página");
console.log("   - METRIC_CARD_CLICK: Al hacer clic en tarjetas");
console.log("   - DROPDOWN_INTERACTION: Al usar el dropdown");
console.log("   - ACCESSIBILITY_TOGGLE: Al cambiar accesibilidad");
console.log("   - LOGIN: Para autenticación (use onClick)");
