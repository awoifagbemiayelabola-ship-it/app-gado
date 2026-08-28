import streamlit as st

# Configuração da página
st.set_page_config(page_title="Calculadora Pecuária", layout="wide")

st.title("🐄 Calculadora de Viabilidade Pecuária")
st.caption("Aplicações sempre conectadas para análise de lucro e viabilidade.")

# --- FORMULÁRIO DE ENTRADA ---
with st.sidebar:
    st.header("📋 Dados do Lote")
    lote = st.text_input("Identificação do Lote", value="Lote 01")
    qtd_animais = st.number_input("Quantidade de Animais", min_value=1, value=50, step=1)
    fase = st.selectbox("Fase do Manejo", ["RECRIA", "ENGORDA"])
    
    st.header("⚖️ Pesos e Desempenho")
    peso_inicial = st.number_input("Peso Inicial por Cabeça (kg)", min_value=1.0, value=300.0, step=5.0)
    peso_final = st.number_input("Peso Final Desejado por Cabeça (kg)", min_value=1.0, value=520.0, step=5.0)
    gmd = st.number_input("GMD - Ganho Médio Diário (kg/dia)", min_value=0.1, value=0.8, step=0.05)
    rendimento_carcaca = st.number_input("Rendimento de Carcaça (%)", min_value=40.0, max_value=65.0, value=54.0, step=0.5)

    st.header("💰 Custos e Valores")
    valor_aquisicao = st.number_input("Valor de Aquisição por Cabeça (R$)", min_value=0.0, value=3000.0, step=50.0)
    valor_pasto = st.number_input("Valor do Pasto por Cabeça/Mês (R$)", min_value=0.0, value=60.0, step=5.0)
    preco_arroba_compra = st.number_input("Preço da @ de Compra na Região (R$)", min_value=1.0, value=280.0, step=5.0)
    preco_arroba_venda = st.number_input("Preço Estimado da @ na Venda (R$)", min_value=1.0, value=300.0, step=5.0)

    st.header("🌾 Suplementação")
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
    custo_suplemento_dia = st.number_input("Custo Estimado da Suplementação/Dia por Cabeça (R$)", min_value=0.0, value=2.50, step=0.10)

# --- CÁLCULOS PRINCIPAIS ---

# 1. Tempo necessário
ganho_peso_total = max(0.0, peso_final - peso_inicial)
dias_necessarios = int(ganho_peso_total / gmd) if gmd > 0 else 0
meses = dias_necessarios / 30.0

# 2. Ágio (%)
# Ágio = ((Valor Pago por @ na Compra / Preço de Mercado da @) - 1) * 100
arrobas_compra = (peso_inicial * (rendimento_carcaca / 100)) / 15
valor_arroba_paga = valor_aquisicao / arrobas_compra if arrobas_compra > 0 else 0
agio_pct = ((valor_arroba_paga - preco_arroba_compra) / preco_arroba_compra) * 100

# 3. Custos Individuais e do Lote
custo_pasto_total_cabeca = (valor_pasto / 30) * dias_necessarios
custo_suplemento_total_cabeca = custo_suplemento_dia * dias_necessarios
custo_operacional_cabeca = valor_aquisicao + custo_pasto_total_cabeca + custo_suplemento_total_cabeca

custo_total_lote = custo_operacional_cabeca * qtd_animais

# 4. Receita e Lucro
arrobas_venda_cabeca = (peso_final * (rendimento_carcaca / 100)) / 15
receita_cabeca = arrobas_venda_cabeca * preco_arroba_venda
receita_total_lote = receita_cabeca * qtd_animais

lucro_cabeca = receita_cabeca - custo_operacional_cabeca
lucro_total_lote = receita_total_lote - custo_total_lote
margem_lucro = (lucro_total_lote / receita_total_lote * 100) if receita_total_lote > 0 else 0

# --- PAINEL DE RESULTADOS ---

st.subheader(f"📊 Resumo do Lote: {lote} ({fase})")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Tempo Estimado", f"{dias_necessarios} dias", f"~{meses:.1f} meses")
col2.metric("Ágio da Compra", f"{agio_pct:.2f}%")
col3.metric("Custo Total por Cabeça", f"R$ {custo_operacional_cabeca:,.2f}")
col4.metric("Lucro Líquido do Lote", f"R$ {lucro_total_lote:,.2f}", delta=f"{margem_lucro:.1f}% Margem")

st.markdown("---")

# Detalhamento Visual
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("💵 Custos e Receitas por Cabeça")
    st.write(f"* **Aquisição:** R$ {valor_aquisicao:,.2f}")
    st.write(f"* **Custo de Pasto ({dias_necessarios} dias):** R$ {custo_pasto_total_cabeca:,.2f}")
    st.write(f"* **Custo de Suplementação ({tipo_suplemento}):** R$ {custo_suplemento_total_cabeca:,.2f}")
    st.write(f"* **@ Produzida na Venda:** {arrobas_venda_cabeca:.2f} @")
    st.write(f"* **Faturamento Estimado:** R$ {receita_cabeca:,.2f}")

with col_right:
    st.subheader("💡 Conselhos & Diagnóstico do Negócio")
    
    if lucro_total_lote > 0:
        if margem_lucro >= 15:
            st.success("🟢 **ÓTIMO NEGÓCIO!** A margem estimada está acima de 15%. A operação apresenta excelente viabilidade financeira.")
        else:
            st.warning("🟡 **NEGÓCIO REGULAR.** O lote gera lucro, mas a margem é estreita (< 15%). Fique atento a oscilações no preço da arroba ou custos de insumos.")
    else:
        st.error("🔴 **NEGÓCIO ARRISCADO / PREJUÍZO!** As projeções indicam resultado negativo. Revise o preço de compra, reduza o custo de suplementação ou melhore o GMD.")

    # Alertas específicos sobre Ágio e GMD
    if agio_pct > 20:
        st.info("⚠️ **Atenção ao Ágio:** Você está pagando um ágio alto (> 20%) na compra do animal. Garanta que o ganho de peso compensará esse custo inicial.")
    if gmd < 0.5 e fase == "ENGORDA":
        st.info("⚠️ **GMD Baixo para Engorda:** O ganho médio diário está baixo para a fase de engorda. Considere aumentar a oferta nutricional.")
