import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# --- Configuración inicial ---
st.set_page_config(page_title="Gestor Financiero", page_icon="💰", layout="centered")

# Inicializar datos en la sesión
if "movimientos" not in st.session_state:
    st.session_state["movimientos"] = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Monto"])

# --- Configuración de moneda en el sidebar ---
st.sidebar.header("⚙️ Configuración")
moneda = st.sidebar.selectbox("Selecciona la moneda", ["USD ($)", "EUR (€)", "ARS ($)", "MXN ($)", "CLP ($)"])
simbolos = {"USD ($)": "$", "EUR (€)": "€", "ARS ($)": "$", "MXN ($)": "$", "CLP ($)": "$","COP ($)": "$"}
simbolo = simbolos[moneda]

st.title("💰 Mi Gestor Financiero")

# --- Opción para cargar archivo ---
st.header("📂 Cargar movimientos desde archivo")
archivo = st.file_uploader("Sube un archivo Excel (.xlsx) o CSV", type=["xlsx", "csv"])

if archivo:
    try:
        if archivo.name.endswith(".csv"):
            df = pd.read_csv(archivo)
        else:
            df = pd.read_excel(archivo)

        # Si no tiene columna "Fecha", asignar la fecha de hoy
        if "Fecha" not in df.columns:
            df["Fecha"] = date.today()

        # Verificar que tenga las columnas necesarias
        if set(["Tipo", "Categoría", "Monto"]).issubset(df.columns):
            st.session_state["movimientos"] = pd.concat(
                [st.session_state["movimientos"], df], ignore_index=True
            )
            st.success("✅ Movimientos cargados desde archivo")
        else:
            st.error("❌ El archivo debe tener las columnas: Tipo, Categoría, Monto (y opcionalmente Fecha)")
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")

# --- Formulario de ingreso manual ---
st.header("➕ Registrar movimiento manual")

fecha = st.date_input("Fecha", date.today())
tipo = st.selectbox("Tipo", ["Ingreso", "Egreso"])
categoria = st.text_input("Categoría (ej: comida, salario, ocio)")
monto = st.number_input("Monto", min_value=0.0, step=0.1)

if st.button("Agregar manualmente"):
    nuevo = {"Fecha": fecha, "Tipo": tipo, "Categoría": categoria, "Monto": monto}
    st.session_state["movimientos"] = pd.concat(
        [st.session_state["movimientos"], pd.DataFrame([nuevo])],
        ignore_index=True
    )
    st.success("Movimiento agregado ✅")

# --- Mostrar tabla de movimientos ---
st.header("📋 Historial de movimientos")
st.dataframe(st.session_state["movimientos"], width="stretch")

# --- Mostrar gráficos y métricas ---
if not st.session_state["movimientos"].empty:
    st.header("📊 Visualización")

    resumen = st.session_state["movimientos"].groupby("Tipo")["Monto"].sum()

    fig, ax = plt.subplots()
    resumen.plot(kind="bar", ax=ax, color=["green", "red"])
    ax.set_ylabel(f"Monto total ({simbolo})")
    ax.set_title("Ingresos vs Egresos")
    st.pyplot(fig)

    balance = resumen.get("Ingreso", 0) - resumen.get("Egreso", 0)
    st.metric("Balance actual", f"{simbolo}{balance:,.2f}")

    # --- Nuevo: gráfico por fechas ---
    st.subheader("📆 Movimientos en el tiempo")
    fig2, ax2 = plt.subplots()
    st.session_state["movimientos"].groupby("Fecha")["Monto"].sum().plot(ax=ax2, marker="o")
    ax2.set_ylabel(f"Monto ({simbolo})")
    ax2.set_xlabel("Fecha")
    ax2.set_title("Evolución de movimientos")
    st.pyplot(fig2)

else:
    st.info("Todavía no has registrado movimientos.")

    import streamlit as st

# Diccionario de traducciones
translations = {
    "en": {
        "title": "Personal Finance App",
        "welcome": "Welcome to your personal finance dashboard!",
        "balance": "Your balance is:",
        "expenses": "Expenses",
        "income": "Income",
    },
    "es": {
        "title": "Aplicación de Finanzas Personales",
        "welcome": "¡Bienvenido a tu panel de finanzas personales!",
        "balance": "Tu saldo es:",
        "expenses": "Gastos",
        "income": "Ingresos",
    }
}

# --- Selección de idioma ---
lang = st.sidebar.selectbox("Choose your language", ["en", "es"])

# Función para traducir textos
def t(key):
    return translations[lang].get(key, key)

# --- Interfaz principal ---
st.title(t("title"))
st.write(t("welcome"))

# Ejemplo de datos
balance = 1200
expenses = 500
income = 1700

# Mostrar métricas
st.metric(t("balance"), f"${balance}")
st.subheader(t("expenses"))
st.write(f"${expenses}")

st.subheader(t("income"))
st.write(f"${income}")
