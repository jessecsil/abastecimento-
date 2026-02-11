import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Controle de Combustível", layout="centered")

st.title("⛽ Abastecimento 2026")

# Conectando com a planilha (Google Sheets)
conn = st.connection("gsheets", type=GSheetsConnection)

# Lendo os dados existentes
df = conn.read(ttl="0")

# Interface de entrada
with st.form(key="abastecimento_form"):
    data = st.date_input("Data")
    gnv = st.number_input("Valor GNV (R$)", min_value=0.0)
    gas = st.number_input("Valor GAS (R$)", min_value=0.0)
    
    submit_button = st.form_submit_button(label="Registrar Abastecimento")

    if submit_button:
        total = gnv + gas
        # Criando a nova linha
        nova_linha = pd.DataFrame([{
            "Data": data.strftime("%d/%m/%Y"),
            "GNV": gnv,
            "GAS": gas,
            "VALOR TOTAL": total
        }])
        
        # Adicionando ao DataFrame atual
        df_atualizado = pd.concat([df, nova_linha], ignore_index=True)
        
        # Salvando de volta na planilha
        conn.update(worksheet="Fevereiro", data=df_atualizado)
        st.success("Dados salvos com sucesso!")
        st.cache_data.clear() # Limpa o cache para mostrar o dado novo

# Exibição da Tabela
st.subheader("Histórico de Gastos")
st.dataframe(df)

# Cálculos Totais
st.divider()
total_geral = df["VALOR TOTAL"].sum()
st.metric(label="SOMA TOTAL", value=f"R$ {total_geral:.2f}")
