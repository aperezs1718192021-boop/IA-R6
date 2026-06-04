# 🎯 R6 Siege AI — Estrategias Tácticas

App en **Streamlit + Python** que usa IA (Claude de Anthropic) para generar estrategias de ataque y defensa personalizadas por mapa en Rainbow Six Siege.

---

## 🚀 Instalación local (VS Code)

### 1. Clona el repositorio
```bash
git clone https://github.com/TU_USUARIO/r6-siege-ai.git
cd r6-siege-ai
```

### 2. Crea un entorno virtual
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Instala las dependencias
```bash
pip install -r requirements.txt
```

### 4. Añade tu API Key de Anthropic
Edita el archivo `.streamlit/secrets.toml` y pon tu clave:
```toml
ANTHROPIC_API_KEY = "sk-ant-XXXXXXXXXX"
```
Consigue tu clave en: https://console.anthropic.com

### 5. Ejecuta la app
```bash
streamlit run app.py
```

Se abrirá automáticamente en `http://localhost:8501`

---

## ☁️ Desplegar en Streamlit Cloud (gratis)

1. Sube el proyecto a GitHub (sin el `secrets.toml` con tu clave real)
2. Ve a [share.streamlit.io](https://share.streamlit.io) e inicia sesión con GitHub
3. Selecciona tu repositorio → `app.py` como archivo principal
4. En **Settings → Secrets**, añade:
   ```
   ANTHROPIC_API_KEY = "sk-ant-XXXXXXXXXX"
   ```
5. ¡Despliega!

---

## 🗺️ Mapas disponibles

### 🏆 Ranked
Club House, Banco, Estudio de Grabación, Faro, Consulado, Kafe Dostoyevski, Jardín Japonés, Villa, Frontera, Vertigo

### 🎮 Casual
Casa, Cafetería, Presidio, Avión, Yate, Parque de Atracciones, Costa, Minas de Kanal

### 🌍 Operaciones Especiales
Favela, Montaña

---

## 🛠️ Tecnologías

- **Python 3.10+**
- **Streamlit** — interfaz web
- **Anthropic Claude** — generación de estrategias con IA

---

## ⚠️ Importante

Nunca subas tu `secrets.toml` con la API Key real a GitHub. El `.gitignore` ya lo excluye automáticamente.
