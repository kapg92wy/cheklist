import streamlit as st
from PIL import Image
import io
import base64
from datetime import datetime
import json
import os

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Checklist Mini Garra",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# ESTILOS CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&family=Nunito:wght@400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Rajdhani', sans-serif;
        letter-spacing: 1px;
    }

    .main { background-color: #0f0f1a; color: #e8e8f0; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 2px solid #e94560;
    }
    section[data-testid="stSidebar"] .stRadio label {
        color: #e8e8f0 !important;
        font-size: 15px;
        font-weight: 600;
    }

    /* Tarjetas de casilla */
    .casilla-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #1f2040 100%);
        border: 1px solid #2a2a4a;
        border-left: 4px solid #e94560;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 18px;
        box-shadow: 0 4px 20px rgba(233,69,96,0.12);
    }

    .casilla-header {
        background: linear-gradient(90deg, #e94560, #c23152);
        color: white;
        padding: 10px 18px;
        border-radius: 8px;
        font-family: 'Rajdhani', sans-serif;
        font-size: 20px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 16px;
        display: inline-block;
    }

    .seccion-titulo {
        color: #e94560;
        font-family: 'Rajdhani', sans-serif;
        font-size: 17px;
        font-weight: 700;
        letter-spacing: 1px;
        border-bottom: 1px solid #2a2a4a;
        padding-bottom: 4px;
        margin: 14px 0 8px 0;
        text-transform: uppercase;
    }

    .maquina-banner {
        background: linear-gradient(90deg, #0f3460, #16213e);
        border: 2px solid #e94560;
        border-radius: 14px;
        padding: 18px 28px;
        margin: 16px 0 24px 0;
        text-align: center;
    }
    .maquina-banner h2 {
        color: #e94560;
        font-size: 28px;
        margin: 0;
        letter-spacing: 3px;
    }
    .maquina-banner p {
        color: #a0a0c0;
        margin: 4px 0 0 0;
        font-size: 14px;
    }

    .resumen-box {
        background: #1a1a2e;
        border: 1px solid #2a2a4a;
        border-top: 3px solid #e94560;
        border-radius: 10px;
        padding: 16px 20px;
        margin: 10px 0;
    }

    .stat-chip {
        display: inline-block;
        background: #e94560;
        color: white;
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 13px;
        font-weight: 700;
        margin: 2px 4px;
    }

    .prueba-box {
        background: linear-gradient(135deg, #1a2e1a 0%, #1f401f 100%);
        border: 1px solid #2a4a2a;
        border-left: 4px solid #4caf50;
        border-radius: 10px;
        padding: 16px;
        margin-top: 12px;
    }

    /* Inputs */
    .stTextInput > div > input,
    .stNumberInput > div > input {
        background: #0f0f1a !important;
        color: #e8e8f0 !important;
        border: 1px solid #2a2a4a !important;
        border-radius: 8px !important;
    }

    .stCheckbox label { color: #e8e8f0 !important; }

    .stSelectbox > div { background: #1a1a2e; }

    div[data-testid="stFileUploader"] {
        background: #1a1a2e;
        border: 1px dashed #e94560 !important;
        border-radius: 10px;
    }

    .stButton > button {
        background: linear-gradient(90deg, #e94560, #c23152) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        letter-spacing: 1px !important;
        padding: 10px 28px !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(233,69,96,0.4) !important;
    }

    .footer-logo {
        text-align: center;
        color: #444466;
        font-family: 'Rajdhani', sans-serif;
        font-size: 13px;
        margin-top: 40px;
        letter-spacing: 2px;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def foto_input(label, key):
    """Subida de foto con previsualización compacta."""
    uploaded = st.file_uploader(f"📷 {label}", type=["jpg","jpeg","png","webp"], key=key)
    if uploaded:
        img = Image.open(uploaded)
        st.image(img, use_column_width=True, caption=label)
        return uploaded
    return None


def casilla_form(maquina_id: str, casilla_num: int):
    """Renderiza el formulario completo de una casilla."""
    key_prefix = f"m{maquina_id}_c{casilla_num}"

    st.markdown(f'<div class="casilla-header">⬡ CASILLA {casilla_num}</div>', unsafe_allow_html=True)

    # ── Número de serie ──────────────────────
    st.markdown('<p class="seccion-titulo">📋 Identificación</p>', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        serie = st.text_input("Número de serie", key=f"{key_prefix}_serie",
                              placeholder="Ej. SN-20241001-A")
    with col2:
        foto_input("Foto del número de serie", f"{key_prefix}_foto_serie")

    # ── Vitrina ──────────────────────────────
    st.markdown('<p class="seccion-titulo">🪟 Vitrina</p>', unsafe_allow_html=True)
    foto_input("Foto de vitrina lista", f"{key_prefix}_foto_vitrina")

    # ── Peluches ────────────────────────────
    st.markdown('<p class="seccion-titulo">🧸 Peluches</p>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        peluches_deje = st.number_input("¿Cuántos peluches dejé?", min_value=0, step=1,
                                        key=f"{key_prefix}_deje")
    with col_b:
        peluches_traje = st.number_input("¿Cuántos peluches traje?", min_value=0, step=1,
                                         key=f"{key_prefix}_traje")

    # ── Foto general ─────────────────────────
    st.markdown('<p class="seccion-titulo">📸 Foto General de la Máquina</p>', unsafe_allow_html=True)
    foto_input("Foto general de la máquina", f"{key_prefix}_foto_general")

    # ── Contadores de premios ─────────────────
    st.markdown('<p class="seccion-titulo">🏆 Contador de Premios</p>', unsafe_allow_html=True)
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("**Mecánico**")
        premios_mec = st.number_input("Contador premios mecánico", min_value=0, step=1,
                                      key=f"{key_prefix}_premios_mec")
        foto_input("Foto contador premios mecánico", f"{key_prefix}_foto_premios_mec")
    with col_p2:
        st.markdown("**Digital**")
        premios_dig = st.number_input("Contador premios digital", min_value=0, step=1,
                                      key=f"{key_prefix}_premios_dig")
        foto_input("Foto contador premios digital", f"{key_prefix}_foto_premios_dig")

    # ── Contadores de monedas ─────────────────
    st.markdown('<p class="seccion-titulo">🪙 Contador de Monedas</p>', unsafe_allow_html=True)
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("**Mecánico**")
        monedas_mec = st.number_input("Contador monedas mecánico", min_value=0, step=1,
                                      key=f"{key_prefix}_monedas_mec")
        foto_input("Foto contador monedas mecánico", f"{key_prefix}_foto_monedas_mec")
    with col_m2:
        st.markdown("**Digital**")
        monedas_dig = st.number_input("Contador monedas digital", min_value=0, step=1,
                                      key=f"{key_prefix}_monedas_dig")
        foto_input("Foto contador monedas digital", f"{key_prefix}_foto_monedas_dig")

    # ── Pruebas (opcional) ───────────────────
    st.markdown('<p class="seccion-titulo">🔧 Pruebas (Opcional)</p>', unsafe_allow_html=True)
    hacer_prueba = st.checkbox("¿Se realizaron pruebas en esta casilla?",
                               key=f"{key_prefix}_prueba_check")

    if hacer_prueba:
        st.markdown('<div class="prueba-box">', unsafe_allow_html=True)
        st.markdown("#### Datos de prueba")
        col_pr1, col_pr2 = st.columns(2)
        with col_pr1:
            st.markdown("**ANTES de prueba**")
            monedas_antes = st.number_input("Contador monedas ANTES de prueba", min_value=0, step=1,
                                            key=f"{key_prefix}_antes")
            foto_input("Foto contador ANTES de prueba", f"{key_prefix}_foto_antes")
        with col_pr2:
            st.markdown("**DESPUÉS de prueba**")
            monedas_despues = st.number_input("Contador monedas DESPUÉS de prueba", min_value=0, step=1,
                                              key=f"{key_prefix}_despues")
            foto_input("Foto contador DESPUÉS de prueba", f"{key_prefix}_foto_despues")

        if hacer_prueba:
            diferencia = monedas_despues - monedas_antes
            st.info(f"💡 Monedas consumidas en prueba: **{diferencia}**")
        st.markdown('</div>', unsafe_allow_html=True)

    # Resumen rápido de la casilla
    st.markdown('<div class="resumen-box">', unsafe_allow_html=True)
    st.markdown(f"""
    <b>Resumen Casilla {casilla_num}</b><br>
    <span class="stat-chip">Serie: {serie if serie else '—'}</span>
    <span class="stat-chip">Dejé: {peluches_deje} 🧸</span>
    <span class="stat-chip">Traje: {peluches_traje} 🧸</span>
    <span class="stat-chip">Premios Mec: {premios_mec}</span>
    <span class="stat-chip">Premios Dig: {premios_dig}</span>
    <span class="stat-chip">Monedas Mec: {monedas_mec}</span>
    <span class="stat-chip">Monedas Dig: {monedas_dig}</span>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()


# ─────────────────────────────────────────────
# SIDEBAR – NAVEGACIÓN
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 10px 0 20px 0;">
        <div style="font-family:'Rajdhani',sans-serif; font-size:28px; color:#e94560; font-weight:700; letter-spacing:3px;">
            🎮 MINI GARRA
        </div>
        <div style="color:#a0a0c0; font-size:12px; letter-spacing:2px;">CHECKLIST DE MÁQUINAS</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📍 Selecciona Máquina")
    maquina_sel = st.radio(
        "",
        options=["🏬 Cinepolis Galerías", "🏪 Cinepolis Forum Tlaquepaque"],
        key="maquina_radio"
    )

    st.divider()
    st.markdown("### 📅 Fecha")
    fecha = st.date_input("Fecha de revisión", value=datetime.today(), key="fecha_global")
    hora = st.time_input("Hora", value=datetime.now().time(), key="hora_global")

    st.divider()
    st.markdown("### 👤 Técnico")
    tecnico = st.text_input("Nombre del técnico", key="tecnico", placeholder="Tu nombre")

    st.divider()
    st.caption("v1.0 · Mini Garra Checklist")


# ─────────────────────────────────────────────
# HEADER PRINCIPAL
# ─────────────────────────────────────────────
maquina_id = "galerias" if "Galerías" in maquina_sel else "forum"
ubicacion_nombre = "Cinepolis Galerías" if maquina_id == "galerias" else "Cinepolis Forum Tlaquepaque"
icono = "🏬" if maquina_id == "galerias" else "🏪"

st.markdown(f"""
<div class="maquina-banner">
    <h2>{icono} {ubicacion_nombre.upper()}</h2>
    <p>Fecha: {fecha.strftime('%d/%m/%Y')} · Técnico: {tecnico if tecnico else '—'}</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"### 🎮 Checklist — Mini Garra 4 Casillas")
st.caption("Completa todos los campos para cada casilla. Las fotos son opcionales pero recomendadas.")

# ─────────────────────────────────────────────
# TABS POR CASILLA
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "  Casilla 1  ",
    "  Casilla 2  ",
    "  Casilla 3  ",
    "  Casilla 4  ",
])

with tab1:
    st.markdown('<div class="casilla-card">', unsafe_allow_html=True)
    casilla_form(maquina_id, 1)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="casilla-card">', unsafe_allow_html=True)
    casilla_form(maquina_id, 2)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="casilla-card">', unsafe_allow_html=True)
    casilla_form(maquina_id, 3)
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="casilla-card">', unsafe_allow_html=True)
    casilla_form(maquina_id, 4)
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# BOTÓN DE GUARDAR / EXPORTAR
# ─────────────────────────────────────────────
st.divider()
st.markdown("### 💾 Guardar Checklist")

col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    if st.button("✅ GUARDAR CHECKLIST COMPLETO", use_container_width=True):
        resumen = {
            "maquina": ubicacion_nombre,
            "fecha": str(fecha),
            "hora": str(hora),
            "tecnico": tecnico,
            "timestamp": datetime.now().isoformat(),
        }
        resumen_json = json.dumps(resumen, ensure_ascii=False, indent=2)
        st.success(f"✅ Checklist guardado correctamente para **{ubicacion_nombre}**")
        st.download_button(
            label="⬇️ Descargar resumen JSON",
            data=resumen_json,
            file_name=f"checklist_{maquina_id}_{fecha}.json",
            mime="application/json",
            use_container_width=True
        )

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer-logo">
    🎮 MINI GARRA CHECKLIST · CINEPOLIS JALISCO · 2024
</div>
""", unsafe_allow_html=True)