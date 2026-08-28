import streamlit as st

# Configuração da página
st.set_page_config(page_title="Calculadora Pecuária", layout="centered")

st.title("🐄 Calculadora de Viabilidade Pecuária")
st.caption("Preencha os campos abaixo para analisar o lucro e a viabilidade do lote.")

# --- FORMULÁRIO DE ENTRADA (TELA PRINCIPAL) ---

st.header("1. Identificação e Manejo")
lote = st.text_input("Identificação do Lote", value="Lote 01")
qtd_animais = st.number_input("Quantidade de Animais", min_value=1, value=50, step=1)
fase = st.radio("Opção de Fase", ["RECRIA", "ENGORDA"], horizontal=True)

st.header("2. Pesos e Desempenho")
col_p1, col_p2 = st.columns(2)
with col_p1:
    peso_inicial = st.number_input("Peso Inicial por Cabeça (kg)", min_value=1.0, value=300.0, step=5.0)
    gmd = st.number_input("GMD - Ganho Médio Diário (kg)", min_value=0.01, value=0.80, step=0.05)
with col_p2:
    peso_final = st.number_input("Peso Final por Cabeça (kg)", min_value=1.0, value=520.0, step=5.0)
    rendimento_carcaca = st.number_input("Rendimento de Carcaça (%)", min_value=40.0, max_value=65.0, value=54.0, step=0.5)

st.header("3. Custos e Valores de Mercado")
col_v1, col_v2 = st.columns(2)
with col_v1:
    valor_aquisicao = st.number_input("Valor de Aquisição por Cabeça (R$)", min_value=0.0, value=3000.0, step=50.0)
    valor_pasto = st.number_input("Valor de Pasto por Cabeça/Mês (R$)", min_value=0.0, value=60.0, step=5.0)
with col_v2:
    preco_arroba_compra = st.number_input("Preço da @ de Compra na Região (R$)", min_value=1.0, value=280.0, step=5.0)
    preco_arroba_venda = st.number_input("Preço Estimado da @ na Venda (R$)", min_value=1.0, value=300.0, step=5.0)

st.header("4. Suplementação")
tipo_suplemento = st.selectbox(
    "Tipo de Suplementação",
    [
        "Proteínado 0,1%",
        "Proteínado 0,2%",
        "Proteico energético 0,3%",
        "Proteico energético 0,4%",
        "Proteico energético 0,5%",
        "Concentrado engorda 1%",
        "Concentrado engorda 1,5%",
        "Concentrado engorda 2%"
    ]
)
custo_suplemento_dia = st.number_input("Custo da Suplementação/Dia por Cabeça (R$)", min_value=0.0, value=2.50, step=0.10)

st.markdown("---")

# --- BOTÃO PARA EXIBIR RESULTADOS EM BAIXO ---
if st.button("📊 Calcular Resultado e Ver Conselhos", type="primary", use_container_width=True):
    
    # --- CÁLCULOS PRINCIPAIS ---
    ganho_peso_total = max(0.0, peso_final - peso_inicial)
    dias_necessarios = int(ganho_peso_total / gmd) if gmd > 0 else 0
    meses = dias_necessarios / 30.0

    # Ágio (%)
    arrobas_compra = (peso_inicial * (rendimento_carcaca / 100)) / 15
    valor_arroba_paga = valor_aquisicao / arrobas_compra if arrobas_compra > 0 else 0
    agio_pct = ((valor_arroba_paga - preco_arroba_compra) / preco_arroba_compra) * 100

    # Custos
    custo_pasto_total_cabeca = (valor_pasto / 30) * dias_necessarios
    custo_suplemento_total_cabeca = custo_suplemento_dia * dias_necessarios
    custo_operacional_cabeca = valor_aquisicao + custo_pasto_total_cabeca + custo_suplemento_total_cabeca
    custo_total_lote = custo_operacional_cabeca * qtd_animais

    # Receita e Lucro
    arrobas_venda_cabeca = (peso_final * (rendimento_carcaca / 100)) / 15
    receita_cabeca = arrobas_venda_cabeca * preco_arroba_venda
    receita_total_lote = receita_cabeca * qtd_animais

    lucro_cabeca = receita_cabeca - custo_operacional_cabeca
    lucro_total_lote = receita_total_lote - custo_total_lote
    margem_lucro = (lucro_total_lote / receita_total_lote * 100) if receita_total_lote > 0 else 0

    # --- EXIBIÇÃO EM BAIXO ---
    st.markdown("## 📈 Resultados da Análise")
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.metric("Tempo Estimado (Dias)", f"{dias_necessarios} dias", f"~{meses:.1f} meses")
        st.metric("Ágio da Compra (%)", f"{agio_pct:.2f}%")
        st.metric("Custo Total por Cabeça", f"R$ {custo_operacional_cabeca:,.2f}")
    
    with col_r2:
        st.metric("Faturamento do Lote", f"R$ {receita_total_lote:,.2f}")
        st.metric("Lucro Líquido do Lote", f"R$ {lucro_total_lote:,.2f}", delta=f"{margem_lucro:.1f}% Margem")
        st.metric("Lucro por Cabeça", f"R$ {lucro_cabeca:,.2f}")

    st.markdown("---")
    
    # --- CONSELHOS E DIAGNÓSTICO ---
    st.subheader("💡 Conselhos e Avaliação do Negócio")
    
    if lucro_total_lote > 0:
        if margem_lucro >= 15:
            st.success("🟢 **EXCELENTE NEGÓCIO!** A margem estimada está acima de 15%. A operação apresenta ótima viabilidade financeira.")
        else:
            st.warning("🟡 **NEGÓCIO REGULAR.** O lote gera lucro, mas a margem é estreita (< 15%). Qualquer variação no preço da arroba pode comprometer o resultado.")
    else:
        st.error("🔴 **NEGÓCIO ARRISCADO / PREJUÍZO!** O projeto apresenta resultado negativo. Verifique se o valor de aquisição está alto ou se o período de permanência está longo demais.")

    # Alertas adicionais
    if agio_pct > 20:
        st.info(f"⚠️ **Alerta de Ágio Elevado ({agio_pct:.1f}%):** O valor pago por arroba na compra está consideravelmente acima do valor de mercado.")
    if gmd < 0.5 and fase == "ENGORDA":
        st.info("⚠️ **Desempenho Baixo:** Um GMD abaixo de 0.500 kg/dia na fase de engorda aumenta muito o tempo de cocho e o custo total.")
