import streamlit as st
import anthropic

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="R6 Siege AI Estrategias",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS personalizado ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Share+Tech+Mono&display=swap');

html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
    background-color: #0a0c0f;
    color: #e0e0e0;
}

/* Fondo general */
.stApp { background-color: #0a0c0f; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #10141a;
    border-right: 1px solid #ff6b00;
}
section[data-testid="stSidebar"] * { color: #e0e0e0 !important; }

/* Títulos */
h1 { color: #ff6b00 !important; font-family: 'Rajdhani', sans-serif !important; letter-spacing: 3px; }
h2, h3 { color: #ffa040 !important; font-family: 'Rajdhani', sans-serif !important; }

/* Botones */
.stButton > button {
    background: linear-gradient(135deg, #ff6b00, #cc4400);
    color: white;
    border: none;
    border-radius: 4px;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 16px;
    letter-spacing: 2px;
    padding: 10px 24px;
    width: 100%;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #ff8c00, #ff6b00);
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(255,107,0,0.4);
}

/* Selectbox y inputs */
.stSelectbox > div > div {
    background-color: #1a1f2a !important;
    border: 1px solid #ff6b00 !important;
    color: #e0e0e0 !important;
    border-radius: 4px;
}
.stTextArea textarea {
    background-color: #1a1f2a !important;
    border: 1px solid #444 !important;
    color: #e0e0e0 !important;
    font-family: 'Share Tech Mono', monospace !important;
}
.stTextArea textarea:focus { border-color: #ff6b00 !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background-color: #10141a;
    border-bottom: 2px solid #ff6b00;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background-color: #1a1f2a;
    color: #888 !important;
    border-radius: 4px 4px 0 0;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 16px;
    letter-spacing: 2px;
    padding: 10px 24px;
    border: 1px solid #333;
}
.stTabs [aria-selected="true"] {
    background-color: #ff6b00 !important;
    color: white !important;
    border-color: #ff6b00 !important;
}

/* Cajas de estrategia */
.strategy-box {
    background: linear-gradient(135deg, #12161e, #1a1f2a);
    border: 1px solid #ff6b00;
    border-left: 4px solid #ff6b00;
    border-radius: 6px;
    padding: 20px;
    margin: 12px 0;
    box-shadow: 0 4px 20px rgba(255,107,0,0.1);
}
.strategy-title {
    color: #ff6b00;
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 8px;
}
.strategy-desc { color: #ccc; line-height: 1.6; }

/* Chips de operadores */
.op-chip {
    display: inline-block;
    background-color: #1e2a1e;
    border: 1px solid #4caf50;
    color: #4caf50;
    border-radius: 3px;
    padding: 3px 10px;
    margin: 3px;
    font-size: 13px;
    font-family: 'Share Tech Mono', monospace;
}
.op-chip.attack {
    background-color: #2a1e1e;
    border-color: #ff6b00;
    color: #ff6b00;
}

/* Cajas info */
.info-box {
    background-color: #12161e;
    border: 1px solid #333;
    border-radius: 6px;
    padding: 16px;
    margin: 10px 0;
}
.info-label {
    color: #ff6b00;
    font-size: 12px;
    letter-spacing: 2px;
    font-weight: 700;
    margin-bottom: 6px;
}
.info-value { color: #e0e0e0; font-size: 15px; }

/* Header banner */
.header-banner {
    background: linear-gradient(135deg, #12161e 0%, #1a1f2a 50%, #12161e 100%);
    border: 1px solid #ff6b00;
    border-radius: 8px;
    padding: 24px;
    text-align: center;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.header-banner::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #ff6b00, transparent);
}

/* Divider naranja */
.orange-divider {
    height: 2px;
    background: linear-gradient(90deg, #ff6b00, transparent);
    margin: 16px 0;
    border: none;
}

/* Scroll de respuesta */
.response-container {
    max-height: 70vh;
    overflow-y: auto;
    padding-right: 8px;
}
.response-container::-webkit-scrollbar { width: 4px; }
.response-container::-webkit-scrollbar-thumb { background: #ff6b00; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ── Datos de mapas ───────────────────────────────────────────────────────────
MAPAS = {
    "🏆 Competitivo": {
        "Banco": {"en": "Bank", "descripcion": "Edificio bancario urbano con bóveda subterránea, vestíbulo principal y múltiples zonas de oficinas en dos plantas"},
        "Frontera": {"en": "Border", "descripcion": "Puesto fronterizo con almacén de armas, sala de inmigración y pasillos estrechos ideales para el control de zonas"},
        "Chalet": {"en": "Chalet", "descripcion": "Lujoso chalet de montaña con garaje, cocina y zonas de estar distribuidas en tres plantas con acceso exterior nevado"},
        "Club": {"en": "Club House", "descripcion": "Cuartel de la banda de moteros con bar, sala de billar, armería y acceso por sótano; tres plantas con rutas verticales"},
        "Consulado": {"en": "Consulate", "descripcion": "Edificio consular de alta seguridad en entorno urbano, con sala de visas, oficinas y múltiples puntos de entrada exteriores"},
        "Café Dostoyevsky": {"en": "Kafe Dostoyevski", "descripcion": "Elegante café ruso de tres plantas con cocina industrial, comedor principal, bar y sala VIP; muchas roturas de suelo"},
        "Guarida": {"en": "Lair", "descripcion": "Base subterránea secreta con laboratorios, sala de servidores y zonas industriales; diseño vertical complejo"},
        "Laboratorios Nighthaven": {"en": "Nighthaven Labs", "descripcion": "Instalación científica de alta tecnología sobre el agua, con laboratorios, sala de control y zonas acristaladas"},
        "Rascacielos": {"en": "Skyscraper", "descripcion": "Piso ejecutivo japonés en las alturas con jardín zen en la azotea, sala de reuniones y diseño abierto"},
    },
    "🎮 No Competitivo": {
        "Avión Presidencial": {"en": "Presidential Plane", "descripcion": "Avión presidencial de lujo con cabina, zona VIP, cola y compartimento de carga; espacios muy estrechos"},
        "Casa": {"en": "House", "descripcion": "Casa residencial de dos plantas ideal para aprender mecánicas básicas; diseño sencillo con jardín y garaje"},
        "Torre": {"en": "Tower", "descripcion": "Torre de comunicaciones con varios pisos, sala de control y zonas de acceso por escaleras exteriores"},
        "Yate": {"en": "Yacht", "descripcion": "Lujoso yate privado con camarotes, sala de máquinas, cubierta superior y zonas de entretenimiento"},
        "Base de Hereford": {"en": "Hereford Base", "descripcion": "Base militar clásica con bunker subterráneo, hangares y múltiples rutas de entrada en exterior abierto"},
        "Favela": {"en": "Favela", "descripcion": "Barrio densamente poblado de Río de Janeiro con rutas verticales, huecos en paredes y pasillos laberínticos"},
        "Fortaleza": {"en": "Fortress", "descripcion": "Fortaleza militar en el desierto con murallas exteriores, patio central y varios edificios interiores conectados"},
        "Canal": {"en": "Kanal", "descripcion": "Instalación industrial con dos edificios separados por un canal de agua; control del puente central es clave"},
        "Outback": {"en": "Outback", "descripcion": "Motel australiano en el desierto con piscina exterior, habitaciones, bar y zonas de servicio interconectadas"},
        "Estadio Alfa / Estadio Bravo": {"en": "Stadium Bravo", "descripcion": "Estadio deportivo con vestuarios, palcos VIP, pasillos interiores y zona de campo con visibilidad extrema"},
        "Close Quarter": {"en": "Close Quarter", "descripcion": "Mapa de combate extremadamente cerrado diseñado para partidas rápidas e intensas en espacios muy reducidos"},
        "Emerald Plains": {"en": "Emerald Plains", "descripcion": "Mansión irlandesa con jardines exteriores, biblioteca, sala de billar y múltiples pasillos interiores"},
    }
}

# Lista plana de mapas para el selector
def get_all_maps():
    maps = {}
    for categoria, mapas in MAPAS.items():
        for nombre_es, datos in mapas.items():
            maps[f"{nombre_es}"] = {"categoria": categoria, **datos}
    return maps

TODOS_LOS_MAPAS = get_all_maps()

# ── Cliente Anthropic ────────────────────────────────────────────────────────
def get_client():
    try:
        return anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    except Exception:
        st.error("❌ Falta la API Key. Añade ANTHROPIC_API_KEY en `.streamlit/secrets.toml`")
        st.stop()

# ── Generador de estrategias ─────────────────────────────────────────────────
def generar_estrategia(mapa_es: str, mapa_en: str, modo: str, pregunta_libre: str = "") -> str:
    client = get_client()

    if pregunta_libre:
        prompt = f"""Eres un experto táctico en Rainbow Six Siege. El jugador está en el mapa "{mapa_es}" ({mapa_en} en inglés) y tiene esta pregunta específica:

"{pregunta_libre}"

Responde en español de forma clara, táctica y detallada. Incluye operadores recomendados, posicionamiento y consejos prácticos."""
    else:
        modo_texto = "ATAQUE" if modo == "Ataque" else "DEFENSA"
        prompt = f"""Eres un experto táctico en Rainbow Six Siege. Genera estrategias completas para el mapa "{mapa_es}" (conocido en inglés como "{mapa_en}") en modo {modo_texto}.

Responde ÚNICAMENTE en español. Estructura tu respuesta así (usa exactamente estos encabezados):

## 📋 RESUMEN TÁCTICO
[2-3 frases describiendo la filosofía general del mapa en este modo]

## 🎯 OBJETIVO PRINCIPAL
[Qué debe priorizar el equipo]

## 👥 OPERADORES RECOMENDADOS
[Lista 5-6 operadores ideales para este modo en este mapa, con una frase explicando por qué cada uno]

## ⚔️ ESTRATEGIA 1: [NOMBRE EN MAYÚSCULAS]
[Descripción detallada de la estrategia, con posicionamiento y ejecución]

## ⚔️ ESTRATEGIA 2: [NOMBRE EN MAYÚSCULAS]
[Descripción detallada de la estrategia, con posicionamiento y ejecución]

## ⚔️ ESTRATEGIA 3: [NOMBRE EN MAYÚSCULAS]
[Descripción detallada de la estrategia, con posicionamiento y ejecución]

## 💡 CONSEJOS CLAVE
[3-5 consejos tácticos específicos para este mapa]

## ❌ ERRORES COMUNES
[3 errores frecuentes a evitar]

Sé específico con nombres de salas y zonas del mapa. Responde siempre en español."""

    with st.spinner("🔄 Analizando mapa y generando estrategias..."):
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=2500,
            messages=[{"role": "user", "content": prompt}]
        )

    return response.content[0].text

# ── INTERFAZ PRINCIPAL ───────────────────────────────────────────────────────

# Header
st.markdown("""
<div class="header-banner">
    <h1 style="margin:0; font-size:2.4em; letter-spacing:6px;">🎯 R6 SIEGE AI</h1>
    <p style="color:#888; letter-spacing:3px; margin:8px 0 0 0; font-size:14px;">SISTEMA DE ANÁLISIS TÁCTICO · RAINBOW SIX SIEGE</p>
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🗺️ SELECCIONAR MAPA")
    st.markdown('<hr class="orange-divider">', unsafe_allow_html=True)

    # Selector de categoría
    categoria_sel = st.selectbox(
        "Categoría",
        list(MAPAS.keys()),
        label_visibility="collapsed"
    )

    # Badge dinámico según categoría
    if "Competitivo" in categoria_sel:
        st.markdown("""
    <div style="background:#1a1200; border:1px solid #ff6b00; border-radius:4px; padding:8px 12px; margin-bottom:12px; font-size:12px; letter-spacing:1px; color:#ffa040;">
        🏆 POOL COMPETITIVO OFICIAL · Ranked · Pro League
    </div>
    """, unsafe_allow_html=True)
    else:
        st.markdown("""
    <div style="background:#0d1a0d; border:1px solid #4a9eff; border-radius:4px; padding:8px 12px; margin-bottom:12px; font-size:12px; letter-spacing:1px; color:#4a9eff;">
        🎮 MAPAS NO COMPETITIVOS · Casual · Arcade
    </div>
    """, unsafe_allow_html=True)

    # Selector de mapa dentro de la categoría
    mapas_lista = list(MAPAS[categoria_sel].keys())
    mapa_sel = st.selectbox(
        "Mapa",
        mapas_lista,
        label_visibility="collapsed"
    )

    datos_mapa = MAPAS[categoria_sel][mapa_sel]

    st.markdown(f"""
    <div class="info-box" style="margin-top:16px;">
        <div class="info-label">📍 MAPA SELECCIONADO</div>
        <div class="info-value" style="font-size:18px; font-weight:700; color:#ff6b00;">{mapa_sel}</div>
        <div style="color:#666; font-size:12px; margin-top:4px; font-style:italic;">"{datos_mapa['en']}" en inglés</div>
        <hr style="border-color:#333; margin:10px 0;">
        <div class="info-label">📖 DESCRIPCIÓN</div>
        <div class="info-value" style="font-size:13px; color:#aaa;">{datos_mapa['descripcion']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="orange-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div style="color:#555; font-size:11px; text-align:center; letter-spacing:1px;">
        POWERED BY CLAUDE AI<br>ANTHROPIC · 2025
    </div>
    """, unsafe_allow_html=True)

# ── CONTENIDO PRINCIPAL ───────────────────────────────────────────────────────
col_main, col_chat = st.columns([3, 1])

with col_main:
    tab_ataque, tab_defensa = st.tabs(["⚔️  ATAQUE", "🛡️  DEFENSA"])

    for tab, modo in [(tab_ataque, "Ataque"), (tab_defensa, "Defensa")]:
        with tab:
            icono = "⚔️" if modo == "Ataque" else "🛡️"
            color = "#ff6b00" if modo == "Ataque" else "#4a9eff"

            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
                <span style="font-size:2em;">{icono}</span>
                <div>
                    <div style="color:{color}; font-size:20px; font-weight:700; letter-spacing:3px;">{modo.upper()} — {mapa_sel.upper()}</div>
                    <div style="color:#555; font-size:12px; letter-spacing:2px;">{datos_mapa['en']} · {categoria_sel}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            btn_key = f"btn_{modo}_{mapa_sel}"
            if st.button(f"🎯 GENERAR ESTRATEGIAS DE {modo.upper()}", key=btn_key):
                resultado = generar_estrategia(mapa_sel, datos_mapa['en'], modo)
                st.session_state[f"resultado_{modo}_{mapa_sel}"] = resultado

            # Mostrar resultado si existe
            key_resultado = f"resultado_{modo}_{mapa_sel}"
            if key_resultado in st.session_state:
                st.markdown('<hr class="orange-divider">', unsafe_allow_html=True)
                st.markdown(st.session_state[key_resultado])

with col_chat:
    st.markdown("### 💬 PREGUNTA LIBRE")
    st.markdown('<hr class="orange-divider">', unsafe_allow_html=True)
    st.markdown(f"<div style='color:#888; font-size:12px; margin-bottom:8px;'>Mapa activo: <span style='color:#ff6b00;'>{mapa_sel}</span></div>", unsafe_allow_html=True)

    pregunta = st.text_area(
        "Pregunta",
        placeholder="Ej: ¿Cómo defender la sala del servidor? ¿Qué hacer si nos flanquean por el sótano?",
        height=120,
        label_visibility="collapsed"
    )

    if st.button("🔍 CONSULTAR IA", key="btn_pregunta"):
        if pregunta.strip():
            respuesta = generar_estrategia(mapa_sel, datos_mapa['en'], "", pregunta)
            st.session_state["respuesta_libre"] = respuesta
            st.session_state["pregunta_libre"] = pregunta
        else:
            st.warning("Escribe una pregunta primero.")

    if "respuesta_libre" in st.session_state:
        st.markdown('<hr class="orange-divider">', unsafe_allow_html=True)
        st.markdown(f"<div style='color:#555; font-size:11px; margin-bottom:8px;'>❓ {st.session_state.get('pregunta_libre','')}</div>", unsafe_allow_html=True)
        st.markdown(st.session_state["respuesta_libre"])
