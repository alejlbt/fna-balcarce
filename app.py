import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection

# --- REGLA DE ORO: st.set_page_config debe ser la primera línea ejecutable después de imports ---
st.set_page_config(
    page_title="FNA Balcarce - Registro",
    page_icon="🏎️",
    layout="centered"
)

# --- CONEXIÓN Y DESTINO DE DATOS ---
ADMIN_PASSWORD = "balcarce2026"
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ESTILOS VISUALES (FNA Balcarce) ---
st.markdown("""
    <style>
    /* Fondo negro sólido */
    .stApp {
        background-color: #000000;
        max-width: 100% !important;
    }
    
    /* Títulos en blanco con acento rojo */
    h1 {
        color: #FFFFFF !important;
        text-align: center !important;
        border-bottom: 5px solid #E30613 !important;
        padding-bottom: 10px;
        font-size: clamp(1.5rem, 5vw, 2.5rem);
        letter-spacing: 0.5px;
    }
    
    h2 {
        color: #FFFFFF !important;
        text-align: center !important;
        font-size: clamp(1.2rem, 4vw, 2rem);
        text-wrap: balance !important;
    }
    
    /* Banner unificado */
    .banner-title {
        text-align: center !important;
        font-size: clamp(1.2rem, 4vw, 1.8rem) !important;
        color: #FFFFFF !important;
        margin-bottom: 8px !important;
        letter-spacing: 0.8px !important;
    }
    
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
    
    /* Textos y etiquetas en blanco */
    label, p, .stMarkdown {
        color: #FFFFFF !important;
    }
    
    /* Inputs con borde rojo FNA */
    .stTextInput>div>div>input {
        background-color: #1A1A1A !important;
        color: white !important;
        border: 1px solid #E30613 !important;
    }
    
    .stMultiSelect>div>div {
        border: 1px solid #E30613 !important;
    }
    
    .stNumberInput>div>div>input {
        border: 1px solid #E30613 !important;
    }
    
    /* Botón: Rojo sólido, texto blanco, negrita, ancho completo */
    .stButton>button {
        background-color: #E30613 !important;
        color: white !important;
        font-weight: bold !important;
        width: 100% !important;
        border-radius: 10px !important;
        border: none !important;
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
    
    /* Optimización mobile */
    @media screen and (max-width: 768px) {
        .stApp {
            padding-left: 10px !important;
            padding-right: 10px !important;
        }
        
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 100% !important;
        }
        
        h1 {
            font-size: clamp(1.2rem, 6vw, 2rem) !important;
            padding-bottom: 6px !important;
            margin-bottom: 10px !important;
        }
        
        h2 {
            font-size: clamp(1rem, 3.5vw, 1.4rem) !important;
            margin-top: 10px !important;
            margin-bottom: 5px !important;
        }
        
        .banner-title {
            font-size: clamp(1rem, 3.8vw, 1.5rem) !important;
            margin-bottom: 6px !important;
        }
        
        .banner-subtitle {
            margin-top: -18px !important;
            font-size: 0.75em !important;
        }
        
        .sorteo-mensaje {
            margin: 10px 0 6px 0 !important;
            font-size: clamp(0.85rem, 2.2vw, 1rem) !important;
        }
        
        .stButton>button {
            min-height: 44px !important;
            font-size: 1rem !important;
        }
    }
    
    @media screen and (max-width: 480px) {
        .banner-title {
            font-size: clamp(0.9rem, 3.5vw, 1.3rem) !important;
            margin-bottom: 5px !important;
        }
        
        .banner-subtitle {
            margin-top: -15px !important;
            font-size: 0.7em !important;
        }
        
        .main .block-container {
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
            padding-top: 0.5rem !important;
        }
    }
    
    @media screen and (max-width: 400px) {
        .stApp {
            padding-left: 5px !important;
            padding-right: 5px !important;
        }
        
        .main .block-container {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
            padding-top: 0.5rem !important;
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


# --- ENCABEZADO OPTIMIZADO PARA MÓVIL ---
st.markdown("""
    <div style="text-align: center; padding: 10px 0px;">
        <h1 style="color: #E30613; line-height: 1.1; margin-bottom: 10px; font-family: 'Orbitron', sans-serif;">
            <span style="font-size: 2.2rem; display: block;">FIESTA NACIONAL</span>
            <span style="font-size: 1.8rem; display: block; opacity: 0.9;">del</span>
            <span style="font-size: 2.2rem; display: block;">AUTOMOVILISMO</span>
        </h1>
        <p style="margin-top: 0px; font-size: 1.5rem; font-weight: bold; color: #FFFFFF; letter-spacing: 3px; border-top: 2px solid #E30613; display: inline-block; padding-top: 5px;">
            33ª EDICIÓN
        </p>
    </div>
""", unsafe_allow_html=True)

# --- FORMULARIO DE REGISTRO ---
st.markdown("<h2>Boxes de Información: Contanos sobre vos</h2>", unsafe_allow_html=True)

with st.form(key='registro_form'):
    # Campos del formulario
    ciudad = st.text_input("¿Desde qué ciudad nos visitás?").strip().upper()
    
    intereses = st.multiselect(
        "¿Qué es lo que más te interesa de la fiesta?",
        options=["Automovilismo", "Gastronomía", "Shows", "Feria de Artesanos", "Museo Fangio", "Productos Locales"],
        default=None,
        placeholder="Seleccioná una o más opciones"
    )
    
    grupo = st.number_input("¿Cuántos integran tu grupo?", min_value=1, value=1, step=1)
    
    whatsapp = st.text_input("WhatsApp de contacto *", placeholder="Ej: 2266554433", help="Número con código de país para el sorteo")

    # Mensaje de sorteo
    st.markdown('<div class="sorteo-mensaje">🏆 ¡Registrate y participá del sorteo oficial de la FNA33!</div>', unsafe_allow_html=True)
    
    submit_button = st.form_submit_button(label='Terminar 🏁')

    if submit_button:
        # Validación: Solo disparar guardado si Ciudad, Intereses y WhatsApp no están vacíos
        whatsapp_clean = whatsapp.strip() if whatsapp else ""
        
        if ciudad and intereses and whatsapp_clean:
            try:
                # LÓGICA DE GUARDADO (sin append_row):
                # 1. Leer la hoja con conn.read(worksheet="Hoja 1", ttl=0)
                df_existente = conn.read(worksheet="Hoja 1", ttl=0)
                
                # 2. Crear un DataFrame con el nuevo registro
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                nueva_fila = pd.DataFrame([{
                    "Timestamp": timestamp,
                    "Ciudad": ciudad,
                    "Intereses": ", ".join(intereses),
                    "Grupo": int(grupo),
                    "WhatsApp": whatsapp_clean
                }])
                
                # 3. Concatenar con pd.concat
                df_final = pd.concat([df_existente, nueva_fila], ignore_index=True)
                
                # 4. Guardar todo el DataFrame actualizado usando conn.update(worksheet="Hoja 1", data=df_final)
                conn.update(worksheet="Hoja 1", data=df_final)
                
                # Éxito: Limpiar formulario (se limpia automáticamente en Streamlit), # --- Animación de Banderas a Cuadros --- y mostrar mensaje
                st.markdown("""
                    <div class="flags-container">
                        <div class="checker-flag">🏁</div><div class="checker-flag">🏁</div>
                        <div class="checker-flag">🏁</div><div class="checker-flag">🏁</div>
                        <div class="checker-flag">🏁</div><div class="checker-flag">🏁</div>
                        <div class="checker-flag">🏁</div><div class="checker-flag">🏁</div>
                    </div>
                    <style>
                        .checker-flag {
                            position: fixed;
                            top: -50px;
                            font-size: 45px;
                            z-index: 9999;
                            animation: fall 3s linear forwards;
                        }
                        @keyframes fall {
                            to {
                                transform: translateY(110vh) rotate(720deg);
                            }
                        }
                        .checker-flag:nth-child(1) { left: 5%; animation-delay: 0s; }
                        .checker-flag:nth-child(2) { left: 20%; animation-delay: 0.4s; }
                        .checker-flag:nth-child(3) { left: 35%; animation-delay: 0.2s; }
                        .checker-flag:nth-child(4) { left: 50%; animation-delay: 0.8s; }
                        .checker-flag:nth-child(5) { left: 65%; animation-delay: 0.3s; }
                        .checker-flag:nth-child(6) { left: 80%; animation-delay: 0.6s; }
                        .checker-flag:nth-child(7) { left: 90%; animation-delay: 1.1s; }
                        .checker-flag:nth-child(8) { left: 15%; animation-delay: 0.5s; }
                    </style>
                """, unsafe_allow_html=True)
                numero_cupon = len(df_final)
                st.success(f"¡REGISTRO EXITOSO! Tu número de cupón es: #{numero_cupon}")
                
            except Exception as e:
                st.error(f"Error al guardar en Google Sheets: {e}")
        else:
            # Mensajes de validación específicos
            if not ciudad:
                st.error("Por favor, completá tu ciudad.")
            elif not intereses:
                st.error("Por favor, seleccioná al menos un interés.")
            elif not whatsapp_clean:
                st.error("Por favor, completá tu número de WhatsApp para participar del sorteo.")

# --- PANEL DE ADMINISTRACIÓN ---
st.sidebar.title("Acceso Administrador")
admin_input = st.sidebar.text_input("Contraseña", type="password")

if admin_input == ADMIN_PASSWORD:
    st.sidebar.success("Acceso Concedido")
    st.header("Estadísticas y Reportes (Admin)")
    
    try:
        # Leer datos de la Hoja 1
        df_admin = conn.read(worksheet="Hoja 1", ttl=0)
        
        if not df_admin.empty:
            # Mostrar total de registros
            total_registros = len(df_admin)
            st.write(f"**Total de registros:** {total_registros}")
            
            # Mostrar la tabla completa de datos de la Hoja 1
            st.subheader("Tabla completa de registros")
            st.dataframe(df_admin, use_container_width=True)
            
            # Gráficos opcionales
            if "Ciudad" in df_admin.columns:
                st.subheader("Visitantes por Ciudad")
                ciudad_counts = df_admin['Ciudad'].value_counts().reset_index()
                ciudad_counts.columns = ['Ciudad', 'Cantidad']
                st.bar_chart(ciudad_counts.set_index('Ciudad'))
                
        else:
            st.info("Aún no hay registros en la planilla 'Hoja 1'.")
            
    except Exception as e:
        st.error(f"Error al leer datos de Google Sheets: {e}")
        
elif admin_input:  # Si ingresó algo pero no es la contraseña correcta
    st.sidebar.error("Contraseña incorrecta")






