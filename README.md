# 🎮 R6 Siege — AI Strategy Hub

Aplicación web que usa la IA de Anthropic (Claude) para generar estrategias de ataque y defensa para cada mapa de Rainbow Six Siege.

---

## 📁 Estructura del proyecto

```
r6-strategy-ai/
├── index.html     → Estructura HTML de la app
├── styles.css     → Estilos y diseño visual
├── app.js         → Lógica, lista de mapas y llamadas a la IA
└── README.md      → Este archivo
```

---

## 🚀 Instalación y uso

### 1. Clona o descarga el repositorio

```bash
git clone https://github.com/TU_USUARIO/r6-strategy-ai.git
cd r6-strategy-ai
```

### 2. Consigue tu API Key de Anthropic

1. Ve a [https://console.anthropic.com](https://console.anthropic.com)
2. Regístrate o inicia sesión
3. Ve a **API Keys** y crea una nueva clave

### 3. Introduce tu API Key en el proyecto

Abre `app.js` y reemplaza la línea:

```js
const API_KEY = "TU_API_KEY_AQUI";
```

por tu clave real:

```js
const API_KEY = "sk-ant-xxxxxxxxxxxxxxxxx";
```

### 4. Abre el proyecto en VS Code

```bash
code .
```

### 5. Lanza con Live Server

1. Instala la extensión **Live Server** en VS Code (si no la tienes)
   - Busca `Live Server` de Ritwick Dey en el panel de extensiones
2. Click derecho sobre `index.html` → **"Open with Live Server"**
3. La app se abrirá en tu navegador en `http://127.0.0.1:5500`

---

## 🎯 Cómo usar la app

1. **Selecciona un mapa** de la lista lateral (puedes buscar por nombre)
2. Pulsa **ATAQUE** o **DEFENSA** para generar estrategias con IA
3. La IA generará:
   - Resumen estratégico
   - Zona de spawn / posicionamiento inicial
   - Objetivo clave de la ronda
   - Operadores recomendados (meta actual)
   - 3 estrategias con nombre y descripción
   - Consejos tácticos
   - Errores comunes a evitar
4. Usa la **barra inferior** para hacer preguntas específicas sobre el mapa

---

## ⚠️ Advertencia de seguridad

> **No subas tu API Key a GitHub.**
> 
> Si vas a hacer el repositorio público, asegúrate de que `app.js` tenga `TU_API_KEY_AQUI` en lugar de tu clave real antes de hacer commit.

Para evitar exponer la clave accidentalmente puedes añadir al `.gitignore`:

```
# Si usas un archivo separado de config
config.js
.env
```

O crear un archivo `config.js` separado (ignorado por git) que exporte la clave.

---

## 🗺️ Mapas disponibles

### Ranked
Bank · Border · Chalet · Clubhouse · Coastline · Consulate · Kafe Dostoyevsky · Oregon · Skyscraper · Nighthaven Labs · Stadium Bravo · Villa · Lair · Emerald Plains · Fortress

### Casual
House · Plane · Hereford Base

---

## 🛠️ Tecnologías

- **HTML5** — estructura semántica
- **CSS3** — diseño táctico con variables CSS, animaciones y diseño responsivo
- **JavaScript (Vanilla)** — sin frameworks, sin dependencias
- **Anthropic Claude API** — modelo `claude-sonnet-4-20250514`
- **Google Fonts** — Rajdhani + Share Tech Mono + Inter

---

## 📝 Personalización

### Añadir más mapas
En `app.js`, añade entradas al array `MAPS`:

```js
{ name: "Nuevo Mapa", type: "Tipo", category: "RANKED" },
```

### Cambiar el modelo de IA
En `app.js`, modifica la constante `MODEL`:

```js
const MODEL = "claude-opus-4-5"; // más potente pero más lento
```

### Cambiar colores
En `styles.css`, edita las variables CSS en `:root`:

```css
:root {
  --orange: #ff781e;  /* color de acento principal */
  --bg:     #0a0c0f;  /* fondo principal */
}
```

---

## 📄 Licencia

MIT — libre para uso personal y educativo.
