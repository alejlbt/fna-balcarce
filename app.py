import streamlit as st
import pandas as pd
import os
import datetime

# Estilo basado en el póster de la FNA32
st.markdown("""
    <style>
    /* Fondo principal en Negro */
    .stApp {
        background-color: #000000;
    }
    
    /* Títulos en Blanco con acento en Rojo - Centrados */
    h1 {
        color: #FFFFFF !important;
        font-family: 'Orbitron', sans-serif; /* Tipografía tipo carrera */
        border-bottom: 5px solid #E30613; /* Línea roja debajo del título */
        padding-bottom: 10px;
        text-align: center !important;
    }
    
    /* Subtítulos y headers centrados */
    h2, h3 {
        text-align: center !important;
    }
    
    /* Headers de Streamlit centrados */
    .stHeader {
        text-align: center !important;
    }
    
    /* Espaciado después del banner de la 33ª edición */
    .banner-spacing {
        margin-bottom: 35px !important;
    }
    
    /* Textos y etiquetas en Blanco */
    label, p, .stMarkdown {
        color: #FFFFFF !important;
    }

    /* Inputs (cajas de texto) con borde rojo FNA para coherencia visual */
    .stTextInput>div>div>input {
        background-color: #1A1A1A;
        color: white;
        border: 1px solid #E30613 !important;
    }
    
    /* Selectores múltiples también con borde rojo */
    .stMultiSelect>div>div {
        border: 1px solid #E30613 !important;
    }
    
    /* Input numérico también con borde rojo */
    .stNumberInput>div>div>input {
        border: 1px solid #E30613 !important;
    }

    /* Botón estilo FNA: Fondo Rojo Sólido, Letra Blanca en Negrita */
    .stButton>button {
        background-color: #E30613 !important;
        color: white !important;
        border-radius: 5px;
        border: none;
        font-weight: bold !important;
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: #C00510 !important;
        border: 1px solid white;
    }
    </style>
    """, unsafe_allow_html=True)


# --- Configuración de la página ---
st.set_page_config(
    page_title="Fiesta Nacional del Automovilismo - Balcarce",
    page_icon="🏎️",
    layout="centered"
)

# --- Rutas de archivos ---
DATA_FILE = "visitantes_fna.csv"
ADMIN_PASSWORD = "balcarce2026"

# --- Cargar o crear el DataFrame ---
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Timestamp", "Ciudad", "Intereses", "Grupo"])

df = load_data()

# --- Encabezado de la App ---
st.markdown("<h1>⛰️ ¡Bienvenido a Balcarce! ⛰️</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='banner-spacing'>🏎️ 33ª Edición - Fiesta Nacional del Automovilismo 🏁</h3>", unsafe_allow_html=True)

# --- Formulario de Registro ---
st.markdown("<h2 style='text-align: center; margin-top: 35px;'>Boxes de Información: Contanos sobre vos</h2>", unsafe_allow_html=True)

with st.form(key='registro_form'):
    ciudad = st.text_input("¿Desde qué ciudad nos visitás?").strip().upper() # .strip() y .upper() aquí
    
    intereses = st.multiselect(
        "¿Qué es lo que más te interesa de la fiesta?",
        options=["Automovilismo", "Gastronomía", "Shows", "Feria de Artesanos", "Museo Fangio", "Productores Locales"],
        default=None,
        placeholder="Seleccioná una o más opciones",
        help="Podés elegir todas las opciones que quieras"
    )

    grupo = st.number_input("¿Cuántos integran tu grupo?", min_value=1, value=1, step=1)

    submit_button = st.form_submit_button(label='Terminar 🏁 ')

    if submit_button:
        if ciudad and intereses: # Asegurarse de que no estén vacíos
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Convertir la lista de intereses a un string separado por comas
            intereses_str = ", ".join(intereses)
            
            new_entry = pd.DataFrame([{"Timestamp": timestamp, "Ciudad": ciudad, "Intereses": intereses_str, "Grupo": grupo}])
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success(f"¡Gracias! Ya registramos tu visita desde {ciudad}. 🎉")
            st.balloons() # ¡Los globos de festejo!
        else:
            st.error("Por favor, completá tu ciudad y al menos un interés.")

st.markdown("---")

# --- Sección de Administración ---
st.sidebar.title("Acceso Administrador")
admin_input = st.sidebar.text_input("Contraseña")

if admin_input == ADMIN_PASSWORD:
    st.sidebar.success("Acceso Concedido")
    st.header("Estadísticas y Reportes (Admin)")

    total_registros = len(df)
    total_visitantes = df['Grupo'].sum()

    st.write(f"**Total de registros:** {total_registros}")
    st.write(f"**Total de visitantes (personas):** {total_visitantes}")

    if not df.empty:
        # Gráfico de Ciudades
        st.subheader("Visitantes por Ciudad")
        ciudad_counts = df['Ciudad'].value_counts().reset_index()
        ciudad_counts.columns = ['Ciudad', 'Cantidad']
        st.bar_chart(ciudad_counts.set_index('Ciudad'))

        # Gráfico de Intereses (manejar múltiples selecciones)
        st.subheader("Intereses de los Visitantes")
        # Split y explode para contar cada interés individualmente
        all_intereses = df['Intereses'].str.split(', ').explode()
        intereses_counts = all_intereses.value_counts().reset_index()
        intereses_counts.columns = ['Interés', 'Cantidad']
        st.bar_chart(intereses_counts.set_index('Interés'))

        # Tabla de datos crudos
        st.subheader("Detalle de Registros")
        st.dataframe(df)

        # Botón para descargar datos
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar Datos en CSV",
            data=csv_data,
            file_name="reporte_visitantes_fna.csv",
            mime="text/csv",
            help="Descargá el archivo CSV con todos los registros."
        )
    else:
        st.info("Aún no hay registros de visitantes para mostrar estadísticas.")
elif admin_input: # Si ingresó algo pero no es la contraseña correcta
    st.sidebar.error("Contraseña incorrecta")