import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ============================
# Configuración inicial
# ============================
st.set_page_config(
    page_title="💰 Personal Finance Manager",
    page_icon="💰",
    layout="wide"
)

# ============================
# Traducciones
# ============================
translations = {
    "en": {
        "title": "💰 Personal Finance Manager",
        "upload": "📂 Upload your Excel or CSV file",
        "add": "🧾 Add a transaction manually",
        "type": "Type",
        "amount": "Amount",
        "date": "Date",
        "add_btn": "Add Transaction",
        "overview": "📊 Transactions Overview",
        "total_income": "💵 Total Income",
        "total_expense": "💸 Total Expense",
        "chart_title": "Income vs Expense",
        "upload_info": "Please upload a file or add transactions manually to see results.",
        "success_add": "✅ Added {type} of {amount}{currency} on {date}"
    },
    "es": {
        "title": "💰 Gestor de Finanzas Personales",
        "upload": "📂 Sube tu archivo Excel o CSV",
        "add": "🧾 Añadir una transacción manualmente",
        "type": "Tipo",
        "amount": "Monto",
        "date": "Fecha",
        "add_btn": "Agregar Transacción",
        "overview": "📊 Resumen de Transacciones",
        "total_income": "💵 Ingresos Totales",
        "total_expense": "💸 Gastos Totales",
        "chart_title": "Ingresos vs Gastos",
        "upload_info": "Por favor, sube un archivo o añade transacciones manualmente para ver los resultados.",
        "success_add": "✅ Se agregó {type} de {amount}{currency} el {date}"
    }
}

# ============================
# Selector de idioma y moneda
# ============================
col_lang, col_currency = st.columns([2, 1])

with col_lang:
    lang = st.selectbox("🌐 Language / Idioma", ["English", "Español"])
    lang_code = "en" if lang == "English" else "es"

with col_currency:
    currency = st.selectbox("💱 Currency", ["USD", "EUR", "COP", "GBP", "MXN"])

t = translations[lang_code]

# ============================
# Título
# ============================
st.title(t["title"])
st.markdown("---")

# ============================
# Variables de sesión
# ============================
if "manual_data" not in st.session_state:
    st.session_state.manual_data = pd.DataFrame(columns=["Type", "Amount", "Date"])

# ============================
# Subida de archivo
# ============================
st.subheader(t["upload"])
uploaded_file = st.file_uploader("📎", type=["xlsx", "csv"])

# ============================
# Formulario manual
# ============================
st.subheader(t["add"])

with st.form("manual_entry_form"):
    col1, col2, col3 = st.columns(3)
    tipo = col1.selectbox(t["type"], ["Income", "Expense"] if lang_code == "en" else ["Ingreso", "Gasto"])
    monto = col2.number_input(t["amount"], min_value=0.0, step=0.1)
    fecha = col3.date_input(t["date"], datetime.today())

    submitted = st.form_submit_button(t["add_btn"])

if submitted:
    type_en = "Income" if tipo in ["Income", "Ingreso"] else "Expense"
    new_data = pd.DataFrame([{"Type": type_en, "Amount": monto, "Date": fecha}])
    st.session_state.manual_data = pd.concat(
        [st.session_state.manual_data, new_data], ignore_index=True
    )
    st.success(t["success_add"].format(type=tipo, amount=monto, currency=currency, date=fecha))

# ============================
# Procesar archivo subido
# ============================
df = pd.DataFrame()

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        st.success("📄 File uploaded successfully!" if lang_code == "en" else "📄 Archivo cargado con éxito!")
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")

# ============================
# Combinar datos
# ============================
if not df.empty or not st.session_state.manual_data.empty:
    combined_df = pd.concat([df, st.session_state.manual_data], ignore_index=True)

    st.markdown(f"### {t['overview']}")
    st.dataframe(combined_df, use_container_width=True)

    if "Type" in combined_df.columns and "Amount" in combined_df.columns:
        df_summary = combined_df.groupby("Type")["Amount"].sum().reset_index()

        col1, col2 = st.columns(2)
        with col1:
            st.metric(t["total_income"], f"{df_summary[df_summary['Type'] == 'Income']['Amount'].sum():,.2f} {currency}")
        with col2:
            st.metric(t["total_expense"], f"{df_summary[df_summary['Type'] == 'Expense']['Amount'].sum():,.2f} {currency}")

        # ============================
        # Gráfico de barras
        # ============================
        fig = px.bar(
            df_summary,
            x="Type",
            y="Amount",
            color="Type",
            title=t["chart_title"],
            text_auto=True,
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(size=14),
            title_font=dict(size=20)
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info(t["upload_info"])

# ============================
# Pie de página
# ============================streamlit run app.py

st.markdown("---")
st.caption(f"📅 {datetime.today().date()} | Created by Ghosty ❤️ Powered by Streamlit")
