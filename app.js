// ══════════════════════════════════════════════
//  R6 SIEGE AI STRATEGY HUB — app.js
// ══════════════════════════════════════════════

// ── CONFIGURACIÓN ──────────────────────────────
// Reemplaza con tu API Key de Anthropic
// IMPORTANTE: En producción nunca expongas la clave en el frontend.
// Para uso local en VS Code está bien; para publicar online usa un backend.
const API_KEY = "TU_API_KEY_AQUI";
const API_URL = "https://api.anthropic.com/v1/messages";
const MODEL   = "claude-sonnet-4-20250514";

// ── DATOS DE MAPAS ─────────────────────────────
const MAPS = [
  { name: "Bank",               type: "Urban",      category: "RANKED" },
  { name: "Border",             type: "Military",   category: "RANKED" },
  { name: "Chalet",             type: "Alpine",     category: "RANKED" },
  { name: "Clubhouse",          type: "Biker",      category: "RANKED" },
  { name: "Coastline",          type: "Coastal",    category: "RANKED" },
  { name: "Consulate",          type: "Diplomatic", category: "RANKED" },
  { name: "Kafe Dostoyevsky",   type: "Restaurant", category: "RANKED" },
  { name: "Oregon",             type: "Ranch",      category: "RANKED" },
  { name: "Skyscraper",         type: "Urban",      category: "RANKED" },
  { name: "Nighthaven Labs",    type: "Facility",   category: "RANKED" },
  { name: "Stadium Bravo",      type: "Stadium",    category: "RANKED" },
  { name: "Villa",              type: "Estate",     category: "RANKED" },
  { name: "Lair",               type: "Underground",category: "RANKED" },
  { name: "Emerald Plains",     type: "Manor",      category: "RANKED" },
  { name: "Fortress",           type: "Desert",     category: "RANKED" },
  { name: "House",              type: "Residential",category: "CASUAL" },
  { name: "Plane",              type: "Aircraft",   category: "CASUAL" },
  { name: "Hereford Base",      type: "Military",   category: "CASUAL" },
];

// ── ESTADO ────────────────────────────────────
let selectedMap  = null;
let selectedMode = null;
let isLoading    = false;

// ── REFERENCIAS DOM ───────────────────────────
const mapListEl       = document.getElementById("mapList");
const mapSearchEl     = document.getElementById("mapSearch");
const mapHeaderArea   = document.getElementById("mapHeaderArea");
const mapTitleDisplay = document.getElementById("mapTitleDisplay");
const mapSubtitle     = document.getElementById("mapSubtitleDisplay");
const strategyPanel   = document.getElementById("strategyPanel");
const tabAtk          = document.getElementById("tabAtk");
const tabDef          = document.getElementById("tabDef");
const customQuestion  = document.getElementById("customQuestion");
const askBtn          = document.getElementById("askBtn");

// ── EVENTOS ───────────────────────────────────
mapSearchEl.addEventListener("input", () => renderMapList(mapSearchEl.value));
tabAtk.addEventListener("click", () => selectMode("atk"));
tabDef.addEventListener("click", () => selectMode("def"));
askBtn.addEventListener("click", askCustomQuestion);
customQuestion.addEventListener("keydown", (e) => {
  if (e.key === "Enter") askCustomQuestion();
});

// ── RENDER LISTA DE MAPAS ────────────────────
function renderMapList(filter = "") {
  const filtered = MAPS.filter(m =>
    m.name.toLowerCase().includes(filter.toLowerCase())
  );
  const categories = [...new Set(filtered.map(m => m.category))];

  mapListEl.innerHTML = "";

  categories.forEach(cat => {
    const catDiv = document.createElement("div");
    catDiv.className = "map-category";
    catDiv.textContent = `// ${cat}`;
    mapListEl.appendChild(catDiv);

    filtered
      .filter(m => m.category === cat)
      .forEach(m => {
        const item = document.createElement("div");
        item.className = "map-item" + (selectedMap === m.name ? " active" : "");
        item.innerHTML = `
          <div class="map-dot"></div>
          <div class="map-name">${m.name}</div>
          <div class="map-type">${m.type}</div>
        `;
        item.addEventListener("click", () => selectMap(m.name, m.type));
        mapListEl.appendChild(item);
      });
  });
}

// ── SELECCIONAR MAPA ─────────────────────────
function selectMap(name, type) {
  selectedMap  = name;
  selectedMode = null;

  mapHeaderArea.style.display = "flex";
  mapTitleDisplay.textContent = name.toUpperCase();
  mapSubtitle.textContent     = `// ${type.toUpperCase()} — SELECCIONA MODO`;

  tabAtk.className = "tab-btn";
  tabDef.className = "tab-btn";

  renderMapList(mapSearchEl.value);

  showPanel(`
    <div class="welcome-state">
      <div class="welcome-hex">◈</div>
      <div class="welcome-title">${name.toUpperCase()}</div>
      <div class="welcome-sub">
        Selecciona <strong>ATAQUE</strong> o <strong>DEFENSA</strong>
        para que la IA genere estrategias para este mapa.
      </div>
    </div>
  `);

  askBtn.disabled = false;
}

// ── SELECCIONAR MODO ─────────────────────────
function selectMode(mode) {
  if (!selectedMap) return;
  selectedMode = mode;

  tabAtk.className = "tab-btn" + (mode === "atk" ? " active-atk" : "");
  tabDef.className = "tab-btn" + (mode === "def" ? " active-def" : "");

  const modeLabel = mode === "atk" ? "ATAQUE" : "DEFENSA";
  mapSubtitle.textContent = `// ${selectedMap.toUpperCase()} — ${modeLabel}`;

  fetchStrategies(selectedMap, mode);
}

// ── HELPERS DOM ───────────────────────────────
function showPanel(html) {
  strategyPanel.innerHTML = html;
}

function showLoading(map, mode) {
  const label = mode === "atk" ? "ATAQUE" : "DEFENSA";
  showPanel(`
    <div class="loading-state">
      <div class="loading-bar"></div>
      <div class="loading-text">// ANALIZANDO ${map.toUpperCase()} — ${label}...</div>
      <div class="loading-bar"></div>
      <div class="loading-text" style="color:var(--text-dim)">// GENERANDO ESTRATEGIAS CON IA...</div>
    </div>
  `);
}

// ── LLAMADA A LA API ─────────────────────────
async function callClaude(systemPrompt, userPrompt, maxTokens = 2048) {
  const res = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type":         "application/json",
      "x-api-key":            API_KEY,
      "anthropic-version":    "2023-06-01",
      "anthropic-dangerous-direct-browser-access": "true"
    },
    body: JSON.stringify({
      model:      MODEL,
      max_tokens: maxTokens,
      system:     systemPrompt,
      messages:   [{ role: "user", content: userPrompt }]
    })
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err?.error?.message || `HTTP ${res.status}`);
  }

  const data = await res.json();
  return data.content.map(c => c.text || "").join("");
}

// ── PARSEO SEGURO DE JSON ────────────────────
function safeParseJSON(raw) {
  let clean = raw.replace(/```json|```/g, "").trim();
  try {
    return JSON.parse(clean);
  } catch {
    // Intenta reparar JSON truncado
    const lastComma = clean.lastIndexOf(",");
    const lastBrace = clean.lastIndexOf("}");
    if (lastComma > lastBrace) clean = clean.substring(0, lastComma);

    const openBrackets = (clean.match(/\[/g) || []).length - (clean.match(/\]/g) || []).length;
    const openBraces   = (clean.match(/\{/g) || []).length - (clean.match(/\}/g) || []).length;
    for (let i = 0; i < openBrackets; i++) clean += "]";
    for (let i = 0; i < openBraces;   i++) clean += "}";

    return JSON.parse(clean);
  }
}

// ── FETCH ESTRATEGIAS ─────────────────────────
async function fetchStrategies(map, mode) {
  if (isLoading) return;
  isLoading = true;
  showLoading(map, mode);

  const systemPrompt = `Eres un experto en Rainbow Six Siege con miles de horas de experiencia.
Conoces todos los mapas, mecánicas, operadores y el meta actual.
Responde SOLO en JSON válido, sin backticks ni markdown.
Sé conciso en cada campo (máximo 2 frases por descripción).
La estructura debe ser exactamente:
{
  "fase": "string",
  "resumen": "string",
  "entrada_principal": "string",
  "objetivo_clave": "string",
  "operadores_recomendados": ["op1","op2","op3","op4","op5"],
  "estrategias": [
    {"titulo":"string","descripcion":"string"},
    {"titulo":"string","descripcion":"string"},
    {"titulo":"string","descripcion":"string"}
  ],
  "consejos": ["string","string","string","string"],
  "errores_comunes": ["string","string","string"]
}`;

  const userPrompt = mode === "atk"
    ? `Dame estrategias completas de ATAQUE para el mapa ${map} en Rainbow Six Siege. Incluye operadores meta, estrategias con nombre, consejos y errores comunes.`
    : `Dame estrategias completas de DEFENSA para el mapa ${map} en Rainbow Six Siege. Incluye operadores meta, estrategias con nombre, consejos y errores comunes.`;

  try {
    const raw    = await callClaude(systemPrompt, userPrompt, 2048);
    const parsed = safeParseJSON(raw);
    renderStrategies(parsed, map, mode);
  } catch (e) {
    showPanel(`
      <div class="error-msg">
        // ERROR AL CONECTAR CON LA IA<br>
        // Comprueba que tu API Key es correcta en app.js<br><br>
        ${e.message}
      </div>
    `);
  }

  isLoading = false;
}

// ── RENDER ESTRATEGIAS ────────────────────────
function renderStrategies(data, map, mode) {
  const isAtk     = mode === "atk";
  const badgeClass = isAtk ? "atk"      : "def";
  const chipClass  = isAtk ? "atk-chip" : "def-chip";
  const modeLabel  = isAtk ? "ATAQUE"   : "DEFENSA";

  const ops = (data.operadores_recomendados || [])
    .map(op => `<span class="op-chip ${chipClass}">${op}</span>`)
    .join("");

  const estrategias = (data.estrategias || [])
    .map(s => `
      <div class="tip-row">
        <div class="tip-num">▸</div>
        <div>
          <strong style="color:var(--text);font-family:var(--font-head);font-size:13px;letter-spacing:0.5px">
            ${s.titulo}
          </strong><br>
          <span style="color:var(--text-muted);font-size:13px">${s.descripcion}</span>
        </div>
      </div>
    `).join("");

  const consejos = (data.consejos || [])
    .map((c, i) => `
      <div class="tip-row">
        <div class="tip-num">0${i + 1}</div>
        <div style="font-size:13px">${c}</div>
      </div>
    `).join("");

  const errores = (data.errores_comunes || [])
    .map(e => `
      <div class="tip-row">
        <div class="tip-num" style="color:var(--red)">✕</div>
        <div style="font-size:13px">${e}</div>
      </div>
    `).join("");

  showPanel(`
    <div class="strategy-header">
      <span class="mode-badge ${badgeClass}">${modeLabel}</span>
      <span class="strategy-map-label">// ${map.toUpperCase()}</span>
    </div>

    <div class="strategy-block">
      <div class="block-title">Resumen Estratégico</div>
      <div class="block-content">${data.resumen || "—"}</div>
    </div>

    <div class="strategy-block">
      <div class="block-title">${isAtk ? "Zona de Spawn / Entrada" : "Posicionamiento Inicial"}</div>
      <div class="block-content">${data.entrada_principal || "—"}</div>
    </div>

    <div class="strategy-block">
      <div class="block-title">Objetivo Clave</div>
      <div class="block-content">${data.objetivo_clave || "—"}</div>
    </div>

    <div class="strategy-block">
      <div class="block-title">Operadores Recomendados</div>
      <div class="op-chips">${ops}</div>
    </div>

    <div class="strategy-block">
      <div class="block-title">Estrategias</div>
      ${estrategias}
    </div>

    <div class="strategy-block">
      <div class="block-title">Consejos Tácticos</div>
      ${consejos}
    </div>

    <div class="strategy-block">
      <div class="block-title">Errores Comunes</div>
      ${errores}
    </div>
  `);
}

// ── PREGUNTA LIBRE ────────────────────────────
async function askCustomQuestion() {
  const q = customQuestion.value.trim();
  if (!q || !selectedMap || isLoading) return;

  isLoading       = true;
  askBtn.disabled = true;

  const modeCtx = selectedMode
    ? `(modo actual: ${selectedMode === "atk" ? "ATAQUE" : "DEFENSA"})`
    : "";

  // Añade el bloque de carga al final sin borrar lo anterior
  const loadingEl = document.createElement("div");
  loadingEl.className = "strategy-block";
  loadingEl.style.marginTop = "0.5rem";
  loadingEl.innerHTML = `
    <div class="block-title" style="color:var(--blue)">Analizando...</div>
    <div class="loading-bar" style="margin-top:8px"></div>
  `;
  strategyPanel.appendChild(loadingEl);
  strategyPanel.scrollTop = strategyPanel.scrollHeight;

  const systemPrompt = `Eres un experto en Rainbow Six Siege. 
Responde en español de forma concisa y táctica.
Usa párrafos cortos y consejos prácticos.`;

  const userPrompt = `Sobre el mapa ${selectedMap} en Rainbow Six Siege ${modeCtx}: ${q}`;

  try {
    const answer = await callClaude(systemPrompt, userPrompt, 1500);
    loadingEl.innerHTML = `
      <div class="block-title" style="color:var(--blue)">Respuesta // ${selectedMap}</div>
      <div style="font-family:var(--font-mono);font-size:11px;color:var(--text-muted);margin-bottom:0.5rem;letter-spacing:1px">${q}</div>
      <div class="block-content">${answer.replace(/\n/g, "<br>")}</div>
    `;
  } catch (e) {
    loadingEl.innerHTML = `
      <div class="error-msg">// ERROR: ${e.message}</div>
    `;
  }

  customQuestion.value = "";
  askBtn.disabled      = false;
  isLoading            = false;
  strategyPanel.scrollTop = strategyPanel.scrollHeight;
}

// ── INIT ──────────────────────────────────────
renderMapList();
