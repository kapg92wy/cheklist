import streamlit as st
from PIL import Image
from datetime import datetime
import json

# ─────────────────────────────────────────────
# CONFIGURACIÓN — layout centered es mejor en móvil
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Checklist Mini Garra",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Nunito:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
    background-color: #0d0d1a;
    color: #e8e8f0;
}
h1,h2,h3,h4 { font-family: 'Rajdhani', sans-serif; letter-spacing: 1px; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#1a1a2e,#16213e);
    border-right: 2px solid #e94560;
}

.maquina-banner {
    background: linear-gradient(135deg,#0f3460,#16213e);
    border: 2px solid #e94560;
    border-radius: 14px;
    padding: 16px 20px;
    margin: 12px 0 20px 0;
    text-align: center;
}
.maquina-banner h2 { color: #e94560; font-size: 22px; margin: 0; letter-spacing: 2px; }
.maquina-banner p { color: #a0a0c0; margin: 6px 0 0 0; font-size: 13px; }

.casilla-card {
    background: linear-gradient(135deg,#1a1a2e,#1f2040);
    border: 1px solid #2a2a4a;
    border-left: 5px solid #e94560;
    border-radius: 14px;
    padding: 18px 16px;
    margin-bottom: 24px;
}

.casilla-header {
    background: linear-gradient(90deg,#e94560,#c23152);
    color: white;
    padding: 10px 20px;
    border-radius: 10px;
    font-family: 'Rajdhani', sans-serif;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 3px;
    margin-bottom: 18px;
    display: block;
    text-align: center;
}

.sec {
    color: #e94560;
    font-family: 'Rajdhani', sans-serif;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 1px;
    border-bottom: 1px solid #2a2a4a;
    padding-bottom: 4px;
    margin: 18px 0 10px 0;
    text-transform: uppercase;
}

.contador-bloque {
    background: #13132a;
    border: 1px solid #2a2a4a;
    border-radius: 10px;
    padding: 14px 14px 6px 14px;
    margin-bottom: 12px;
}
.contador-label {
    font-family: 'Rajdhani', sans-serif;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 8px;
}
.lbl-mec { color: #f4a261; }
.lbl-dig { color: #56cfe1; }

.prueba-box {
    background: linear-gradient(135deg,#1a2e1a,#1f401f);
    border: 1px solid #2a4a2a;
    border-left: 5px solid #4caf50;
    border-radius: 10px;
    padding: 14px;
    margin-top: 10px;
}

.resumen-box {
    background: #12122a;
    border: 1px solid #2a2a4a;
    border-top: 3px solid #e94560;
    border-radius: 10px;
    padding: 14px 16px;
    margin-top: 14px;
    line-height: 2.2;
}
.chip {
    display: inline-block;
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 12px;
    font-weight: 700;
    margin: 2px 3px;
    color: white;
}
.chip-red { background: #e94560; }
.chip-green { background: #2d6a4f; }
.chip-blue { background: #1d6fa4; }

/* Inputs grandes para dedo — evita zoom en iOS */
.stTextInput > div > input,
.stNumberInput > div > input {
    background: #0d0d1a !important;
    color: #e8e8f0 !important;
    border: 1px solid #3a3a5a !important;
    border-radius: 10px !important;
    font-size: 16px !important;
    padding: 10px 14px !important;
    min-height: 46px !important;
}
div[data-testid="stFileUploader"] {
    background: #1a1a2e;
    border: 1.5px dashed #e94560 !important;
    border-radius: 10px;
}
.stCheckbox > label { font-size: 15px !important; }

.stButton > button {
    background: linear-gradient(90deg,#e94560,#c23152) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    font-size: 18px !important;
    letter-spacing: 1px !important;
    padding: 14px 24px !important;
    width: 100% !important;
}

/* Tabs grandes para dedo */
.stTabs [data-baseweb="tab"] {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 20px !important;
    font-weight: 700 !important;
    letter-spacing: 3px !important;
    padding: 12px 20px !important;
}

.footer-logo {
    text-align: center;
    color: #333355;
    font-family: 'Rajdhani', sans-serif;
    font-size: 12px;
    margin-top: 36px;
    letter-spacing: 2px;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def foto_input(label: str, key: str):
    up = st.file_uploader(f"📷 {label}", type=["jpg","jpeg","png","webp"], key=key)
    if up:
        st.image(Image.open(up), use_column_width=True, caption=label)
    return up


def bloque_contador(titulo: str, clase: str, icono_str: str,
                    key_num: str, key_foto: str, casilla: str, tipo: str):
    """Bloque individual mecánico o digital, etiquetado por casilla."""
    st.markdown(
        f'<div class="contador-bloque">'
        f'<div class="contador-label {clase}">{icono_str} {titulo} — Casilla {casilla}</div>',
        unsafe_allow_html=True
    )
    val = st.number_input(
        f"Contador {tipo} {titulo.lower()} — Casilla {casilla}",
        min_value=0, step=1, key=key_num, label_visibility="collapsed"
    )
    foto_input(f"Foto {tipo} {titulo.lower()} — Casilla {casilla}", key_foto)
    st.markdown('</div>', unsafe_allow_html=True)
    return val


# ─────────────────────────────────────────────
# FORMULARIO POR CASILLA
# ─────────────────────────────────────────────
def casilla_form(maquina_id: str, letra: str):
    kp = f"m{maquina_id}_c{letra}"

    st.markdown(f'<div class="casilla-header">⬡ CASILLA {letra}</div>', unsafe_allow_html=True)

    # 1 · Número de serie
    st.markdown(f'<p class="sec">📋 Número de Serie — Casilla {letra}</p>', unsafe_allow_html=True)
    serie = st.text_input(
        f"Número de serie — Casilla {letra}",
        key=f"{kp}_serie", placeholder=f"Ej. SN-2024-{letra}"
    )
    foto_input(f"Foto del número de serie — Casilla {letra}", f"{kp}_foto_serie")

    # 2 · Vitrina
    st.markdown(f'<p class="sec">🪟 Vitrina Lista — Casilla {letra}</p>', unsafe_allow_html=True)
    foto_input(f"Foto vitrina lista — Casilla {letra}", f"{kp}_foto_vitrina")

    # 3 · Peluches
    st.markdown(f'<p class="sec">🧸 Peluches — Casilla {letra}</p>', unsafe_allow_html=True)
    p_deje  = st.number_input(f"Peluches que DEJÉ — Casilla {letra}",  min_value=0, step=1, key=f"{kp}_deje")
    p_traje = st.number_input(f"Peluches que TRAJE — Casilla {letra}", min_value=0, step=1, key=f"{kp}_traje")

    # 4 · Foto general
    st.markdown(f'<p class="sec">📸 Foto General de la Máquina — Casilla {letra}</p>', unsafe_allow_html=True)
    foto_input(f"Foto general de la máquina — Casilla {letra}", f"{kp}_foto_general")

    # 5 · Contador de premios (mecánico + digital)
    st.markdown(f'<p class="sec">🏆 Contador de Premios — Casilla {letra}</p>', unsafe_allow_html=True)
    prem_mec = bloque_contador("Mecánico", "lbl-mec", "⚙️",
                               f"{kp}_prem_mec", f"{kp}_fprem_mec", letra, "premios")
    prem_dig = bloque_contador("Digital",  "lbl-dig", "💻",
                               f"{kp}_prem_dig", f"{kp}_fprem_dig", letra, "premios")

    # 6 · Contador de monedas (mecánico + digital)
    st.markdown(f'<p class="sec">🪙 Contador de Monedas — Casilla {letra}</p>', unsafe_allow_html=True)
    mon_mec = bloque_contador("Mecánico", "lbl-mec", "⚙️",
                              f"{kp}_mon_mec", f"{kp}_fmon_mec", letra, "monedas")
    mon_dig = bloque_contador("Digital",  "lbl-dig", "💻",
                              f"{kp}_mon_dig", f"{kp}_fmon_dig", letra, "monedas")

    # 7 · Pruebas (opcional)
    st.markdown(f'<p class="sec">🔧 Pruebas (Opcional) — Casilla {letra}</p>', unsafe_allow_html=True)
    hacer_prueba = st.checkbox(f"¿Se hicieron pruebas en Casilla {letra}?", key=f"{kp}_prueba_chk")

    mon_antes = mon_despues = 0
    if hacer_prueba:
        st.markdown('<div class="prueba-box">', unsafe_allow_html=True)
        st.markdown(f"**📊 ANTES de prueba — Casilla {letra}**")
        mon_antes = st.number_input(
            f"Contador monedas ANTES de prueba — Casilla {letra}",
            min_value=0, step=1, key=f"{kp}_antes"
        )
        foto_input(f"Foto contador ANTES de prueba — Casilla {letra}", f"{kp}_foto_antes")

        st.markdown(f"**📊 DESPUÉS de prueba — Casilla {letra}**")
        mon_despues = st.number_input(
            f"Contador monedas DESPUÉS de prueba — Casilla {letra}",
            min_value=0, step=1, key=f"{kp}_despues"
        )
        foto_input(f"Foto contador DESPUÉS de prueba — Casilla {letra}", f"{kp}_foto_despues")

        diferencia = mon_despues - mon_antes
        st.success(f"💡 Monedas usadas en prueba — Casilla {letra}: **{diferencia}**")
        st.markdown('</div>', unsafe_allow_html=True)

    # Resumen rápido
    prueba_html = (
        f"<br><span class='chip chip-green'>Prueba {letra}: {mon_antes}→{mon_despues} "
        f"({mon_despues-mon_antes} monedas)</span>"
        if hacer_prueba else ""
    )
    st.markdown(f"""
    <div class="resumen-box">
        <b style="font-family:'Rajdhani',sans-serif;font-size:16px;letter-spacing:1px;">
            RESUMEN CASILLA {letra}
        </b><br>
        <span class="chip chip-red">Serie: {serie if serie else '—'}</span><br>
        <span class="chip chip-green">Dejé: {p_deje} 🧸</span>
        <span class="chip chip-green">Traje: {p_traje} 🧸</span><br>
        <span class="chip chip-red">Premios Mec {letra}: {prem_mec}</span>
        <span class="chip chip-blue">Premios Dig {letra}: {prem_dig}</span><br>
        <span class="chip chip-red">Monedas Mec {letra}: {mon_mec}</span>
        <span class="chip chip-blue">Monedas Dig {letra}: {mon_dig}</span>
        {prueba_html}
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:10px 0 20px 0;">
        <div style="font-family:'Rajdhani',sans-serif;font-size:26px;color:#e94560;font-weight:700;letter-spacing:3px;">
            🎮 MINI GARRA
        </div>
        <div style="color:#a0a0c0;font-size:11px;letter-spacing:2px;">CHECKLIST DE MÁQUINAS</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📍 Máquina")
    maquina_sel = st.radio(
        "",
        options=["🏬 Cinepolis Galerías", "🏪 Cinepolis Forum Tlaquepaque"],
        key="maquina_radio"
    )
    st.divider()
    st.markdown("### 📅 Fecha y Hora")
    fecha = st.date_input("Fecha de revisión", value=datetime.today(), key="fecha_g")
    hora  = st.time_input("Hora", value=datetime.now().time(), key="hora_g")
    st.divider()
    st.markdown("### 👤 Técnico")
    tecnico = st.text_input("Nombre", key="tecnico", placeholder="Tu nombre")
    st.divider()
    st.caption("v2.0 · Mini Garra Checklist")


# ─────────────────────────────────────────────
# HEADER PRINCIPAL
# ─────────────────────────────────────────────
maquina_id       = "galerias" if "Galerías" in maquina_sel else "forum"
ubicacion_nombre = "Cinepolis Galerías" if maquina_id == "galerias" else "Cinepolis Forum Tlaquepaque"
icono_loc        = "🏬" if maquina_id == "galerias" else "🏪"

st.markdown(f"""
<div class="maquina-banner">
    <h2>{icono_loc} {ubicacion_nombre.upper()}</h2>
    <p>{fecha.strftime('%d/%m/%Y')} &nbsp;·&nbsp; {hora.strftime('%H:%M')} &nbsp;·&nbsp; {tecnico if tecnico else '—'}</p>
</div>
""", unsafe_allow_html=True)

st.markdown("##### 🎮 Mini Garra · Casillas A · B · C · D")
st.caption("Toca cada tab para llenar la casilla. Todos los contadores y fotos son independientes por casilla.")

# ─────────────────────────────────────────────
# TABS A / B / C / D
# ─────────────────────────────────────────────
tab_a, tab_b, tab_c, tab_d = st.tabs(["  A  ", "  B  ", "  C  ", "  D  "])

with tab_a:
    casilla_form(maquina_id, "A")
with tab_b:
    casilla_form(maquina_id, "B")
with tab_c:
    casilla_form(maquina_id, "C")
with tab_d:
    casilla_form(maquina_id, "D")

# ─────────────────────────────────────────────
# GUARDAR
# ─────────────────────────────────────────────
st.divider()
st.markdown("### 💾 Guardar Checklist")

if st.button("✅ GUARDAR CHECKLIST COMPLETO", use_container_width=True):
    resumen = {
        "maquina": ubicacion_nombre,
        "fecha": str(fecha),
        "hora": str(hora),
        "tecnico": tecnico,
        "timestamp": datetime.now().isoformat(),
        "casillas": ["A", "B", "C", "D"],
    }
    resumen_json = json.dumps(resumen, ensure_ascii=False, indent=2)
    st.success(f"✅ Checklist guardado — **{ubicacion_nombre}**")
    st.download_button(
        label="⬇️ Descargar resumen JSON",
        data=resumen_json,
        file_name=f"checklist_{maquina_id}_{fecha}.json",
        mime="application/json",
        use_container_width=True,
    )

st.markdown("""
<div class="footer-logo">🎮 MINI GARRA CHECKLIST · CINEPOLIS JALISCO · 2025</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer-logo">
    🎮 MINI GARRA CHECKLIST · CINEPOLIS JALISCO · 2024
</div>
""", unsafe_allow_html=True)
