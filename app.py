import streamlit as st
import pandas as pd
import os
import datetime
from streamlit_gsheets import GSheetsConnection

# Estilo basado en el póster de la FNA32
st.markdown("""
    <style>
    /* Fondo principal en Negro */
    .stApp {
        background-color: #000000;
        max-width: 100% !important;
    }
    
    /* Asegurar que todo el contenido tenga max-width 100% */
    .main .block-container {
        max-width: 100% !important;
    }
    
    /* Títulos en Blanco con acento en Rojo - Centrados */
    h1 {
        color: #FFFFFF !important;
        font-family: 'Orbitron', sans-serif; /* Tipografía tipo carrera */
        border-bottom: 5px solid #E30613; /* Línea roja debajo del título */
        padding-bottom: 10px;
        text-align: center !important;
        font-size: clamp(1.5rem, 5vw, 2.5rem); /* Tamaño adaptable */
        letter-spacing: 0.5px !important; /* Look moderno */
    }
    
    /* Subtítulos y headers centrados */
    h2 {
        text-align: center !important;
        font-size: clamp(1.2rem, 4vw, 2rem); /* Tamaño adaptable */
        text-wrap: balance !important; /* Reparte palabras equilibradamente */
    }
    
    h3 {
        text-align: center !important;
        font-size: clamp(0.9rem, 3.5vw, 1.5rem); /* Tamaño adaptable con clamp */
        margin: 0 !important; /* Eliminar márgenes por defecto */
        line-height: 1.1 !important;
    }
    
    /* Headers de Streamlit centrados */
    .stHeader {
        text-align: center !important;
    }
    
    /* Banner unificado - Fiesta Nacional del Automovilismo */
    .banner-title {
        text-align: center !important;
        font-size: clamp(1.2rem, 4vw, 1.8rem) !important;
        color: #FFFFFF !important;
        margin-bottom: 8px !important;
        letter-spacing: 0.8px !important; /* Look moderno y premium */
    }
    
    /* Subtítulo 33ª Edición dentro del banner */
    .banner-subtitle {
        margin-top: -20px !important;
        display: block !important;
        font-size: 0.8em !important;
        opacity: 0.8 !important;
        color: #FFFFFF !important;
    }
    
    /* Mensaje de sorteo - texto rojo y negrita */
    .sorteo-mensaje {
        color: #E30613 !important;
        text-align: center !important;
        font-weight: bold !important;
        font-size: clamp(0.95rem, 2.5vw, 1.1rem) !important;
        margin: 12px 0 8px 0 !important;
        padding: 0 !important;
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
        border-radius: 10px !important;
        border: none;
        font-weight: bold !important;
        width: 100%;
        max-width: 100% !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        background-color: #C00510 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(227, 6, 19, 0.4) !important;
    }
    
    .stButton>button:active {
        transform: translateY(0) !important;
    }
    
    /* Optimización de imágenes y logos */
    img {
        max-width: 100% !important;
        height: auto !important;
    }
    
    /* Padding dinámico y ajustes para móviles */
    @media screen and (max-width: 768px) {
        /* Reducir márgenes laterales en pantallas pequeñas */
        .stApp {
            padding-left: 10px !important;
            padding-right: 10px !important;
        }
        
        /* Ajustar padding de contenedores principales */
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        /* Título de bienvenida: mantiene sierras juntas */
        h1 {
            font-size: clamp(1.2rem, 6vw, 2rem) !important;
            border-bottom-width: 3px !important;
            padding-bottom: 6px !important;
            margin-bottom: 10px !important;
            white-space: nowrap !important;
        }
        
        /* Título del formulario: compacto en móviles */
        h2 {
            font-size: clamp(1rem, 3.5vw, 1.4rem) !important;
            margin-top: 10px !important;
            margin-bottom: 5px !important;
            line-height: 1.1 !important;
            text-wrap: balance !important;
        }
        
        .banner-title {
            font-size: clamp(1rem, 3.8vw, 1.5rem) !important;
            margin-bottom: 6px !important;
        }
        
        .banner-subtitle {
            margin-top: -18px !important;
            font-size: 0.75em !important;
        }
        
        /* Mensaje de sorteo en móviles */
        .sorteo-mensaje {
            margin: 10px 0 6px 0 !important;
            font-size: clamp(0.85rem, 2.2vw, 1rem) !important;
        }
        
        /* Botón con ancho completo en móviles para fácil toque */
        .stButton>button {
            width: 100% !important;
            min-height: 44px !important;
            font-size: 1rem !important;
        }
    }
    
    /* Ajustes adicionales para pantallas muy pequeñas */
    @media screen and (max-width: 480px) {
        h1 {
            font-size: clamp(1rem, 5.5vw, 1.8rem) !important;
            padding-bottom: 5px !important;
            margin-bottom: 8px !important;
            white-space: nowrap !important;
        }
        
        h2 {
            font-size: clamp(0.9rem, 3.2vw, 1.2rem) !important;
            margin-top: 8px !important;
            margin-bottom: 3px !important;
            line-height: 1.1 !important;
            text-wrap: balance !important;
        }
        
        .banner-title {
            font-size: clamp(0.9rem, 3.5vw, 1.3rem) !important;
            margin-bottom: 5px !important;
        }
        
        .banner-subtitle {
            margin-top: -15px !important;
            font-size: 0.7em !important;
        }
        
        .sorteo-mensaje {
            margin: 8px 0 5px 0 !important;
            font-size: clamp(0.8rem, 2vw, 0.95rem) !important;
        }
        
        .main .block-container {
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
            padding-top: 0.5rem !important;
        }
    }
    
    /* Escalado proporcional de paddings para pantallas menores a 400px */
    @media screen and (max-width: 400px) {
        .stApp {
            padding-left: 5px !important;
            padding-right: 5px !important;
        }
        
        .main .block-container {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
            padding-top: 0.5rem !important;
            padding-bottom: 0.75rem !important;
        }
        
        h1 {
            padding-bottom: 4px !important;
            margin-bottom: 6px !important;
            font-size: clamp(0.9rem, 5vw, 1.6rem) !important;
        }
        
        h2 {
            margin-top: 6px !important;
            margin-bottom: 2px !important;
            font-size: clamp(0.85rem, 3vw, 1.1rem) !important;
            line-height: 1.1 !important;
        }
        
        .banner-title {
            font-size: clamp(0.85rem, 3.2vw, 1.2rem) !important;
            margin-bottom: 4px !important;
        }
        
        .banner-subtitle {
            margin-top: -12px !important;
            font-size: 0.65em !important;
        }
        
        .sorteo-mensaje {
            margin: 6px 0 4px 0 !important;
            font-size: clamp(0.75rem, 1.8vw, 0.9rem) !important;
        }
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

# --- Conexión a Google Sheets ---
conn = st.connection("gsheets", type=GSheetsConnection)

# Cargamos los datos existentes para contar los cupones
try:
    df_gsheet = conn.read(worksheet="Hoja 1")
except:
    df_gsheet = pd.DataFrame()

# --- Encabezado de la App ---
st.markdown("""
    <div style="text-align: center; padding: 0px;">
        <h2 style="margin-bottom: 0px; font-size: 28px;">⛰️ ¡Bienvenido a Balcarce!</h2>
        <h1 style="margin-top: 0px; margin-bottom: 5px; font-size: 22px; color: #E30613;">Fiesta Nacional del Automovilismo 🏎️</h1>
        <p style="margin-top: -10px; font-size: 18px; font-weight: bold; opacity: 0.9;">33ª Edición</p>
    </div>
    <hr style="margin-top: 5px; margin-bottom: 20px; border: 1px solid #E30613;">
""", unsafe_allow_html=True)

# --- Formulario de Registro ---
st.markdown("<h2>Boxes de Información: Contanos sobre vos</h2>", unsafe_allow_html=True)

with st.form(key='registro_form'):
    ciudad = st.text_input("¿Desde qué ciudad nos visitás?").strip().upper()
    
    intereses = st.multiselect(
        "¿Qué es lo que más te interesa de la fiesta?",
        options=["Automovilismo", "Gastronomía", "Shows", "Feria de Artesanos", "Museo Fangio", "Productores Locales"],
        default=None,
        placeholder="Seleccioná una o más opciones",
        help="Podés elegir todas las opciones que quieras"
    )

    grupo = st.number_input("¿Cuántos integran tu grupo?", min_value=1, value=1, step=1)
    
    whatsapp = st.text_input("WhatsApp de contacto *", placeholder="Ej: 2266554433", help="Número con código de país para el sorteo")

    # Mensaje de sorteo
    st.markdown('<div class="sorteo-mensaje">🏆 ¡Registrate y participá del sorteo oficial de la FNA33!</div>', unsafe_allow_html=True)
    
    submit_button = st.form_submit_button(label='Terminar 🏁 ')

    if submit_button:
        # Validar campos obligatorios
        whatsapp_clean = whatsapp.strip() if whatsapp else ""
        if ciudad and intereses and whatsapp_clean:
            try:
                # 1. Preparar los datos
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                intereses_str = ", ".join(intereses)
                
                # Creamos una lista con el orden exacto de tus columnas en el Excel
                # Timestamp, Ciudad, Intereses, Grupo, WhatsApp
                nueva_fila = [timestamp, ciudad, intereses_str, grupo, whatsapp_clean]
                
                # 2. ENVIAR A GOOGLE SHEETS
                conn.append_row(nueva_fila, worksheet="Hoja 1")
                
                # 3. Obtener el número de cupón contando la nube
                # Volvemos a leer para tener el número exacto
                df_conteo = conn.read(worksheet="Hoja 1")
                numero_cupon = len(df_conteo)
                
                st.success(f"¡Ya estás participando! Tu número de cupón es el #{numero_cupon} 🎉")
                st.balloons()
                
            except Exception as e:
                st.error(f"Error al conectar con la planilla: {e}")
        else:
            if not ciudad:
                st.error("Por favor, completá tu ciudad.")
            elif not intereses:
                st.error("Por favor, seleccioná al menos un interés.")
            elif not whatsapp_clean:
                st.error("Por favor, completá tu WhatsApp para el sorteo.")

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
