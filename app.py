import streamlit as st

# Configuração visual e layout
st.set_page_config(page_title="Gestão & Viabilidade Pecuária", layout="wide")

st.title("🐄 Sistema Avançado de Viabilidade Pecuária")
st.caption("Análise de compra, projeção de GMD, estratégias nutricionais e protocolos de manejo.")

# --- FORMULÁRIO DE ENTRADA ---
st.header("📋 1. Dados do Lote e Aquisição")

col_fase, col_tipo = st.columns(2)
with col_fase:
    manejo = st.radio("Selecione o Sistema de Manejo:", ["RECRIA", "CONFINAMENTO"], horizontal=True)
with col_tipo:
    tipo_animal = st.selectbox(
        "Tipo de Animal:",
        ["Nelore", "Cruzamento Industrial (Angus/Nelore)", "Anelorado / Anelorado Misto", "Macho LB (Livre de Bruto)", "Fêmea / Novilha"]
    )

st.markdown("---")

col_a, col_b, col_c = st.columns(3)

with col_a:
    qtd_animais = st.number_input("Quantidade de Animais (cabeças)", min_value=1, value=100, step=1)
    peso_entrada_kg = st.number_input("Peso Médio de Entrada por Cabeça (kg)", min_value=50.0, value=330.0, step=5.0)

with col_b:
    valor_compra_cabeca = st.number_input("Valor de Compra por Cabeça (R$)", min_value=1.0, value=3200.0, step=50.0)
    preco_arroba_mercado = st.number_input("Preço de Referência da @ no Mercado (R$)", min_value=1.0, value=280.0, step=5.0)

with col_c:
    arrobas_entrada = st.number_input("Quantidade de Arrobas (@) por Cabeça", min_value=1.0, value=11.0, step=0.5)
    preco_arroba_paga = st.number_input("Valor da @ Pago na Compra (R$)", min_value=1.0, value=290.90, step=1.0)

st.markdown("---")

# --- BOTÃO DE PROCESSAMENTO ---
if st.button("🚀 Processar Análise de Viabilidade e Recomendações", type="primary", use_container_width=True):

    # --- CÁLCULOS TÉCNICOS ---
    # 1. Cálculo do Ágio (%)
    # Ágio = ((Valor da @ paga / Valor da @ mercado) - 1) * 100
    agio_porcentagem = ((preco_arroba_paga - preco_arroba_mercado) / preco_arroba_mercado) * 100
    
    # 2. Definição de Metas de Acordo com o Manejo
    if manejo == "CONFINAMENTO":
        dias_meta_min = 75
        dias_meta_max = 100
        dias_projetados = 90  # Média padrão de ciclo
        peso_meta_final = 540.0 if "Cruzamento" in tipo_animal else 520.0
        rc_estimado = 55.5  # Rendimento de Carcaça médio em confinamento (%)
    else:  # RECRIA
        dias_projetados = 180  # Meta para giro rápido
        peso_meta_final = 420.0 if "Fêmea" in tipo_animal else 450.0
        rc_estimado = 52.0  # Rendimento de Carcaça médio na recria (%)

    # 3. Ganho Médio Diário (GMD) Necessário
    ganho_peso_necessario = max(0.0, peso_meta_final - peso_entrada_kg)
    gmd_necessario = ganho_peso_necessario / dias_projetados if dias_projetados > 0 else 0.0

    # 4. Projeção de Faturamento e Lucratividade Estimada
    arrobas_finais = (peso_meta_final * (rc_estimado / 100)) / 15
    faturamento_cabeca = arrobas_finais * preco_arroba_mercado
    
    # Estimativa de custos operacionais (Pasto/Cocho + Nutrição + Sanidade)
    custo_diario_estimado = 11.50 if manejo == "CONFINAMENTO" else 3.80
    custo_operacional_total = custo_diario_estimado * dias_projetados
    custo_total_cabeca = valor_compra_cabeca + custo_operacional_total
    
    lucro_cabeca = faturamento_cabeca - custo_total_cabeca
    lucro_lote_total = lucro_cabeca * qtd_animais
    margem_lucro = (lucro_cabeca / faturamento_cabeca) * 100 if faturamento_cabeca > 0 else 0.0

    # --- EXIBIÇÃO DOS RESULTADOS ---
    
    st.subheader("📊 Diagnóstico Financeiro e Desempenho Projetado")

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Ágio Pago na Compra", f"{agio_porcentagem:.2f}%", delta=f"{agio_porcentagem:.1f}% vs Mercado", delta_color="inverse")
    col_m2.metric("GMD Necessário", f"{gmd_necessario:.3f} kg/dia", f"{dias_projetados} dias de ciclo")
    col_m3.metric("Lucro Est. por Cabeça", f"R$ {lucro_cabeca:,.2f}")
    col_m4.metric("Lucro Líquido do Lote", f"R$ {lucro_lote_total:,.2f}", delta=f"{margem_lucro:.1f}% Margem")

    st.markdown("---")

    # --- AVALIAÇÃO DE VIABILIDADE DO NEGÓCIO ---
    st.subheader("💡 Avaliação Técnica do Negócio")

    if lucro_cabeca > 0 and agio_porcentagem <= 15:
        st.success("🟢 **EXCELENTE OPORTUNIDADE:** O ágio de compra está dentro do limite operacional aceitável e a projeção indica boa margem de lucro.")
    elif lucro_cabeca > 0 and agio_porcentagem > 15:
        st.warning("🟡 **NEGÓCIO VIÁVEL, MAS REQUER ATENÇÃO:** O ágio pago na compra é elevado. O lucro dependerá do cumprimento rigoroso das metas de GMD.")
    else:
        st.error("🔴 **ALERTA DE RISCO ELEVADO:** Operação com margem negativa ou nula. O custo total supera a receita projetada com base no preço de venda atual.")

    st.markdown("---")

    # --- INSTRUÇÕES E ESTRATÉGIAS DE MANEJO ---
    col_esq, col_dir = st.columns(2)

    with col_esq:
        if manejo == "CONFINAMENTO":
            st.subheader("🎯 Diretrizes para Confinamento (75 a 100 Dias)")
            st.markdown(f"""
            * **Meta de Ciclo:** Finalização rigorosa entre **{dias_meta_min} e {dias_meta_max} dias** para evitar queda na eficiência alimentar.
            * **Meta de Peso Final:** {peso_meta_final:.0f} kg com rendimento de carcaça projetado em **{rc_estimado}%**.
            * **Estratégia de Adaptação (Primeiros 14 dias):**
              * *Dias 1 a 7:* Dieta com 60% de volumoso e 40% de concentrado.
              * *Dias 8 a 14:* Dieta com 40% de volumoso e 60% de concentrado.
              * *Dia 15 em diante:* Dieta de Terminação (80% a 85% de concentrado).
            """)
        else:
            st.subheader("🚀 Diretrizes para Recria de Giro Rápido")
            st.markdown(f"""
            * **Objetivo principal:** Maximizar o ganho em carcaça no menor tempo possível para antecipar a entrada na terminação.
            * **Lotação e Pastagem:** Manejo rotacionado garantindo oferta de forragem com alta relação folha/caule.
            * **Suplementação Estratégica:**
              * *Período das Águas:* Proteico energétic0 0,3% a 0,5% do Peso Vivo (PV).
              * *Período da Seca:* Proteico energétic0 0,5% a 1,0% do PV para manter GMD acima de 0,700 kg/dia.
            """)

    with col_dir:
        st.subheader("🌾 Nutrição Recomendada de Alta Performance")
        if manejo == "CONFINAMENTO":
            st.markdown("""
            * **Formulação Indicada:** Concentrado de Engorda de **1,5% a 2,0% do Peso Vivo (PV)** + Fonte de fibra de alta qualidade (Silagem de milho ou Bagaço de cana).
            * **Uso de Aditivos:** Inclusão obrigatória de **Monensina Sódica** ou **Virginiamicina** para controle de acidose ruminal e otimização da conversão alimentar.
            """)
        else:
            st.markdown("""
            * **Formulação Indicada:** Suplemento Proteico Energético (0,3% a 0,5% do PV) no período chuvoso e Concentrado (1% do PV) no período de transição.
            * **Objetivo Nutricional:** Potencializar a microbiota ruminal para maior aproveitamento da fibra do pasto.
            """)

    st.markdown("---")

    # --- SANIDADE E MANEJO DE TIP / TRATAMENTOS ---
    st.subheader("💉 Protocolos Sanitários e Manejo de TIP (Terminação Intensiva a Pasto)")
    
    st.markdown("""
    * **Protocolo de Entrada (Recepção do Lote):**
      * **Vermifugação Estratégica:** Aplicação de eprinomectina ou ivermectina 3,5% de longa ação na chegada.
      * **Vacinação:** Imunização contra clostridioses (dose e reforço após 30 dias) e vacinas respiratórias (BRD).
      * **Suplementação Mineral/Injetável:** Aplicação de complexos vitamínicos (ADE) e minerais injetáveis (Fósforo/Cobre/Zinco) no desembarque.
    * **Ajustes para TIP (caso opte por engorda a pasto sem cocho de confinamento):**
      * Cocho com metragem linear mínima de **40 a 50 cm por cabeça**.
      * Fornecimento diário de concentrado na proporção de **1,2% a 1,5% do PV**.
      * Adaptação contínua de 10 a 12 dias aumentando gradativamente a dose do concentrado no pasto.
    """)
