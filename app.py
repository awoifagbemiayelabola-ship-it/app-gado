import streamlit as st

st.set_page_config(page_title="Calculadora Pecuária", layout="wide")

st.title("🐂 Calculadora Pecuária - Boi Gordo")
st.write("Simulador de recria e confinamento para bezerros, bezerras, garrotes e novilhas.")

# Abas para navegar entre Recria e Confinamento
aba_recria, aba_confinamento = st.tabs(["🌾 1. Recria (Pasto)", "🥩 2. Confinamento"])

# ==========================================
# ABA 1: RECRIA
# ==========================================
with aba_recria:
    st.header("Simulador de Recria")
    
    col1, col2 = st.columns(2)
    with col1:
        peso_ini_recria = st.number_input("Peso Inicial (kg)", value=200, step=10, key="rec_p_ini")
        peso_fim_recria = st.number_input("Peso Final Projetado (kg)", value=350, step=10, key="rec_p_fim")
        dias_recria = st.number_input("Dias de Recria", value=300, step=10, key="rec_dias")
        custo_aquisicao = st.number_input("Custo de Aquisição (R$)", value=2200.0, step=50.0, key="rec_aq")

    with col2:
        custo_diario_pasto = st.number_input("Custo Diário - Pasto/Suplemento (R$)", value=2.50, step=0.5, key="rec_diario")
        custo_outros_recria = st.number_input("Outros Custos - Sanidade/Frete (R$)", value=150.0, step=10.0, key="rec_outros")
        rend_recria = st.number_input("Rendimento Carcaça Estimado (%)", value=52.0, step=0.5, key="rec_rend")

    if st.button("Calcular Recria", type="primary"):
        # Cálculos
        gmd = (peso_fim_recria - peso_ini_recria) / dias_recria if dias_recria > 0 else 0
        @_iniciais = (peso_ini_recria * (rend_recria / 100)) / 15
        @_finais = (peso_fim_recria * (rend_recria / 100)) / 15
        @_ganhas = @_finais - @_iniciais
        
        custo_nutricao = custo_diario_pasto * dias_recria
        custo_total = custo_aquisicao + custo_nutricao + custo_outros_recria
        custo_arroba_ganha = (custo_nutricao + custo_outros_recria) / @_ganhas if @_ganhas > 0 else 0
        break_even = custo_total / @_finais if @_finais > 0 else 0

        st.markdown("---")
        st.subheader("Resultados da Recria")
        res1, res2, res3 = st.columns(3)
        res1.metric("GMD Médio", f"{gmd:.3f} kg/dia")
        res2.metric("Arrobas Ganhas", f"{@_ganhas:.2f} @")
        res3.metric("Custo Total / Cabeça", f"R$ {custo_total:.2f}")

        res4, res5 = st.columns(2)
        res4.metric("Custo da @ Ganha", f"R$ {custo_arroba_ganha:.2f}")
        res5.metric("Ponto de Equilíbrio (Break-Even)", f"R$ {break_even:.2f} / @")

# ==========================================
# ABA 2: CONFINAMENTO
# ==========================================
with aba_confinamento:
    st.header("Simulador de Confinamento")
    
    col1, col2 = st.columns(2)
    with col1:
        peso_entrada_conf = st.number_input("Peso de Entrada (kg)", value=380, step=10, key="conf_p_ent")
        peso_meta_conf = st.number_input("Peso Meta Abate (kg)", value=540, step=10, key="conf_p_meta")
        gmd_conf = st.number_input("GMD Esperado (kg/dia)", value=1.50, step=0.1, key="conf_gmd")
        valor_animal_conf = st.number_input("Valor de Entrada do Animal (R$)", value=3500.0, step=50.0, key="conf_val")

    with col2:
        custo_dieta = st.number_input("Custo Diário da Dieta (R$)", value=14.50, step=0.5, key="conf_dieta")
        custo_operacional = st.number_input("Custo Diário Operacional (R$)", value=2.00, step=0.5, key="conf_op")
        rend_conf = st.number_input("Rendimento Carcaça Abate (%)", value=54.0, step=0.5, key="conf_rend")

    if st.button("Calcular Confinamento", type="primary"):
        # Cálculos
        ganho_peso = peso_meta_conf - peso_entrada_conf
        dias_cocho = ganho_peso / gmd_conf if gmd_conf > 0 else 0
        custo_diario_total = custo_dieta + custo_operacional
        custo_cocho = custo_diario_total * dias_cocho
        custo_total_conf = valor_animal_conf + custo_cocho
        @_finais_conf = (peso_meta_conf * (rend_conf / 100)) / 15
        break_even_conf = custo_total_conf / @_finais_conf if @_finais_conf > 0 else 0

        st.markdown("---")
        st.subheader("Resultados do Confinamento")
        c1, c2, c3 = st.columns(3)
        c1.metric("Dias de Cocho", f"{int(dias_cocho)} dias")
        c2.metric("Custo Total do Cocho", f"R$ {custo_cocho:.2f}")
        c3.metric("@ Finais de Carcaça", f"{@_finais_conf:.2f} @")

        st.metric("Ponto de Equilíbrio Mínimo (Break-Even)", f"R$ {break_even_conf:.2f} / @")
