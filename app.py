import streamlit as st

st.title("Calculadora de Gado")

# Entradas de dados com valores padrão seguros
peso_ini = st.number_input("Peso inicial (kg):", min_value=0.0, value=300.0)
peso_fim = st.number_input("Peso final (kg):", min_value=0.0, value=500.0)
dias = st.number_input("Total de dias:", min_value=1, value=90)
consumo_dia = st.number_input("Consumo médio por dia (kg):", min_value=0.0, value=10.0)

# Botão para disparar o cálculo apenas quando acionado
if st.button("Calcular Desempenho"):
    ganho_total = peso_fim - peso_ini
    gmd = ganho_total / dias if dias > 0 else 0
    conversao = consumo_dia / gmd if gmd > 0 else 0

    st.subheader("Resultados:")
    st.write(f"**Ganho de Peso Total:** {ganho_total:.2f} kg")
    st.write(f"**Ganho Médio Diário (GMD):** {gmd:.3f} kg/dia")
    st.write(f"**Conversão Alimentar:** {conversao:.2f} kg de alimento/kg ganho")
