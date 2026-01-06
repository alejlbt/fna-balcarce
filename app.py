import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="FNA Balcarce - Registro",
    page_icon="🏎️",
    layout="centered"
)

# --- 2. CONEXIÓN A GOOGLE SHEETS ---
ADMIN_PASSWORD = "balcarce2026"
conn = st.connection("gsheets", type=GSheetsConnection)

# Intentar leer datos para el Admin
try:
    df_gsheet = conn.read(worksheet="Hoja 1", ttl=0)
except:
    df_gsheet = pd.DataFrame()

# --- 3. ESTILOS VISUALES ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    h1 { color: #FFFFFF !important; text-align: center !important; border-bottom: 5px solid #E30613; }
    h2 { text-align: center !important; color: white !important; }
    label, p { color: #FFFFFF !important; }
    .stButton>button { background-color: #E30613 !important; color: white !important; width: 100%; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ENCABEZADO ---
st.markdown("""
    <div style="text-align: center;">
        <h2 style="margin-bottom: 0px;">⛰️ ¡Bienvenido a Balcarce!</h2>
        <h1 style="margin-top: 0px;">Fiesta Nacional del Automovilismo</h1>
        <p style="font-weight: bold;">33ª Edición</p>
    </div>
""", unsafe_allow_html=True)

# --- 5. FORMULARIO DE REGISTRO ---
with st.form(key='registro_form'):
    ciudad = st.text_input("¿Desde qué ciudad nos visitás?").strip().upper()
    intereses = st.multiselect(
        "¿Qué es lo que más te interesa?",
        options=["Automovilismo", "Gastronomía", "Shows", "Feria de Artesanos", "Museo Fangio", "Productores Locales"]
    )
    grupo = st.number_input("¿Cuántos integran tu grupo?", min_value=1, value=1)
    whatsapp = st.text_input("WhatsApp de contacto *")

    st.markdown('<p style="color: #E30613; text-align: center; font-weight: bold;">🏆 ¡Participá del sorteo!</p>', unsafe_allow_html=True)
    
    submit_button = st.form_submit_button(label='Terminar 🏁')

    if submit_button:
            if ciudad and intereses and whatsapp:
                try:
                    # 1. Preparar los datos nuevos
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    nueva_fila = pd.DataFrame([{
                        "Timestamp": timestamp,
                        "Ciudad": ciudad,
                        "Intereses": ", ".join(intereses),
                        "Grupo": grupo,
                        "WhatsApp": whatsapp
                    }])

                    # 2. Combinar con los datos existentes
                    # Leemos la planilla actual
                    df_existente = conn.read(worksheet="Hoja 1", ttl=0)
                    
                    # Unimos lo viejo con lo nuevo
                    df_actualizado = pd.concat([df_existente, nueva_fila], ignore_index=True)

                    # 3. Subir TODO de nuevo (así funciona la versión nueva)
                    conn.update(worksheet="Hoja 1", data=df_actualizado)
                    
                    st.success(f"¡Registrado con éxito! Tu cupón es el #{len(df_actualizado)} 🎉")
                    st.balloons()
                except Exception as e:
                    st.error(f"Error al guardar: {e}")
    else:
        st.warning("Completá todos los campos, por favor.")

# --- 6. SECCIÓN ADMINISTRADOR (CORREGIDA) ---
st.sidebar.title("Panel Admin")
admin_input = st.sidebar.text_input("Contraseña", type="password")

if admin_input == ADMIN_PASSWORD:
    st.sidebar.success("Acceso concedido")
    st.header("Estadísticas de la FNA")
    
    if not df_gsheet.empty:
        st.write(f"**Total Registros:** {len(df_gsheet)}")
        st.dataframe(df_gsheet)
        
        st.subheader("Visitantes por Ciudad")
        st.bar_chart(df_gsheet['Ciudad'].value_counts())
    else:
        st.info("Aún no hay registros en la planilla.")

elif admin_input: # Este es el que daba error de identación
    st.sidebar.error("Contraseña incorrecta")

