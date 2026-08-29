import streamlit as st

# Configuração visual e layout
st.set_page_config(page_title="Gestão & Viabilidade Pecuária", layout="wide")

st.title("🐄 Sistema Avançado de Viabilidade Pecuária")
st.caption("Preencha os dados do lote para obter o diagnóstico financeiro, metas e recomendações de manejo.")

# --- FORMULÁRIO DE ENTRADA STRICTO ---
st.header("📋 Preenchimento dos Dados do Lote")

# 1. Opção de Recria e Confinamento (Marcação)
manejo = st.radio("Selecione o Sistema de Manejo:", ["RECRIA", "CONFINAMENTO"], horizontal=True)

col_1, col_2 = st.columns(2)

with col_1:
    # 2. Quantidade de animais
    qtd_animais = st.number_input("Quantidade de Animais", min_value=1, value=50, step=1)
    
    # 3. Valor do lote (R$)
    valor_total_lote = st.number_input("Valor do Lote (R$ Total de Compra)", min_value=1.0, value=150000.0, step=1000.0)
    
    # 4. Quantas @ tem os animais (Total do lote ou por cabeça)
    tipo_arroba_input = st.radio("A quantidade de @ informada abaixo é:", ["Por Cabeça (individual)", "Total do Lote"], horizontal=True)
    arrobas_input = st.number_input("Quantidade de Arrobas (@)", min_value=1.0, value=11.0, step=0.5)

with col_2:
    # 5. Valor da @ de mercado (R$)
    preco_arroba_mercado = st.number_input("Valor da @ de Mercado (R$)", min_value=1.0, value=280.0, step=5.0)
    
    # 6. Tipo de animal (Preenchido por texto)
    tipo_animal = st.text_input("Tipo de Animal (ex: Nelore, Cruzado Industrial, Anelorado, Novilhas)", value="Nelore Macho")

st.markdown("---")

# --- BOTÃO DE PROCESSAMENTO ---
if st.button("🚀 Processar Análise e Ver Resultados", type="primary", use_container_width=True):

    # --- CÁLCULOS DERIVADOS ---
    # Normalização do total de arrobas por cabeça
    if tipo_arroba_input == "Total do Lote":
        arrobas_por_cabeca = arrobas_input / qtd_animais
        arrobas_totais_lote = arrobas_input
    else:
        arrobas_por_cabeca = arrobas_input
        arrobas_totais_lote = arrobas_input * qtd_animais

    # Valor pago por cabeça e valor pago por @
    valor_por_cabeca = valor_total_lote / qtd_animais
    valor_arroba_paga = valor_por_cabeca / arrobas_por_cabeca if arrobas_por_cabeca > 0 else 0

    # Estimativa de Peso Vivo Inicial em KG (Considerando 50% de rendimento na compra se for garrote/boi)
    peso_inicial_kg = arrobas_por_cabeca * 30  # Conversão padrão em pé

    # Cálculo do Ágio de Compra (%)
    # Ágio = ((Valor da @ Paga / Valor da @ Mercado) - 1) * 100
    agio_pct = ((valor_arroba_paga - preco_arroba_mercado) / preco_arroba_mercado) * 100

    # --- DEFINIÇÃO DE METAS E PARÂMETROS ZOOTÉCNICOS ---
    if manejo == "CONFINAMENTO":
        dias_meta_min, dias_meta_max = 75, 100
        dias_projetados = 90
        peso_meta_final = 530.0
        rc_estimado = 55.5  # Rendimento de carcaça
        custo_diario_estimado = 12.00  # Custo da diária de cocho
    else:  # RECRIA
        dias_projetados = 180  # Giro rápido
        peso_meta_final = 430.0
        rc_estimado = 52.0
        custo_diario_estimado = 3.50  # Custo de pasto + suplementação

    # Cálculo do GMD Necessário
    ganho_peso_necessario = max(0.0, peso_meta_final - peso_inicial_kg)
    gmd_necessario = ganho_peso_necessario / dias_projetados if dias_projetados > 0 else 0.0

    # Financeiro Projetado
    arrobas_finais_cabeca = (peso_meta_final * (rc_estimado / 100)) / 15
    faturamento_cabeca = arrobas_finais_cabeca * preco_arroba_mercado
    custo_operacional_cabeca = custo_diario_estimado * dias_projetados
    custo_total_cabeca = valor_por_cabeca + custo_operacional_cabeca

    lucro_cabeca = faturamento_cabeca - custo_total_cabeca
    lucro_total_lote = lucro_cabeca * qtd_animais
    margem_lucro = (lucro_cabeca / faturamento_cabeca * 100) if faturamento_cabeca > 0 else 0.0

    # --- PAINEL DE RESULTADOS ---
    st.subheader(f"📊 Resumo Financeiro e Indicadores do Lote ({tipo_animal})")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Valor Pago por Cabeça", f"R$ {valor_por_cabeca:,.2f}", f"R$ {valor_arroba_paga:.2f} / @")
    c2.metric("Ágio da Compra", f"{agio_pct:.2f}%", delta=f"{agio_pct:.1f}% vs Mercado", delta_color="inverse")
    c3.metric("GMD Necessário", f"{gmd_necessario:.3f} kg/dia", f"Meta: {dias_projetados} dias")
    c4.metric("Lucro Líquido do Lote", f"R$ {lucro_total_lote:,.2f}", delta=f"{margem_lucro:.1f}% Margem")

    st.markdown("---")

    # --- AVALIAÇÃO DE VIABILIDADE ---
    st.subheader("💡 Avaliação do Negócio")
    
    if lucro_total_lote > 0 and agio_pct <= 15:
        st.success("🟢 **BOM NEGÓCIO!** O ágio de compra está em níveis adequados e o lote apresenta projeção de margem positiva.")
    elif lucro_total_lote > 0 and agio_pct > 15:
        st.warning(f"🟡 **ATENÇÃO AO ÁGIO ({agio_pct:.1f}%):** O negócio gera lucro, porém você pagou um valor por arroba elevado na compra. Exige cumprimento rigoroso do GMD.")
    else:
        st.error("🔴 **ALERTA DE RISCO / PREJUÍZO:** A operação apresenta margem negativa com base nos custos estimados. Avalie renegociar o valor da compra.")

    st.markdown("---")

    # --- ORIENTAÇÕES E ESTRATÉGIAS DE MANEJO ---
    col_dir1, col_dir2 = st.columns(2)

    with col_dir1:
        if manejo == "CONFINAMENTO":
            st.subheader("🎯 Estratégia para Confinamento (75 a 100 Dias)")
            st.markdown(f"""
            * **Janela de Abate:** Planejado para encerramento entre **{dias_meta_min} e {dias_meta_max} dias** para otimizar conversão alimentar.
            * **Manejo de Cocho e Adaptação:**
              * *Adaptação (14 dias):* Transição com aumento gradual de concentrado (iniciar com 1,0% do Peso Vivo e evoluir até a dieta total).
              * *Fase de Terminação:* Leitura diária de cocho para evitar acidose e garantir consumo máximo constante.
            """)
        else:
            st.subheader("🚀 Estratégia para Recria (Giro Rápido)")
            st.markdown("""
            * **Foco em Eficiência:** Giro rápido para maximizar ganho em estrutura óssea e muscular sem acúmulo precoce de gordura.
            * **Manejo de Pastagem:** Lotação ajustada para manter oferta de massa foliar de alta qualidade durante todo o ciclo.
            * **Estratégia Nutricional:**
              * *Águas:* Suplementação Proteico Energética (0,3% a 0,5% do Peso Vivo).
              * *Seca:* Suplementação com maior aporte proteico/energético para manter GMD mínimo de 0,700 kg/dia.
            """)

    with col_dir2:
        st.subheader("🌾 Recomendação Nutricional")
        if manejo == "CONFINAMENTO":
            st.markdown("""
            * **Tipo de Ração:** Dietas de alto grão ou ração total misturada (TMR) com **1,8% a 2,2% do Peso Vivo** em concentrado.
            * **Aditivos Essenciais:** Uso indispensável de **Monensina Sódica** ou **Virginiamicina** para segurança ruminal e melhora de ganho em peso.
            """)
        else:
            st.markdown("""
            * **Tipo de Ração:** Proteinado 0,2% (manutenção/ganho moderado) ou Proteico Energético 0,5% (para acelerar ganho diário).
            * **Objetivo:** Estimular a população de bactérias fibrolíticas no rúmen.
            """)

    st.markdown("---")

    # --- TRATAMENTOS SANITÁRIOS E PROTOCOLO TIP ---
    st.subheader("💉 Tratamentos Sanitários & Protocolos de TIP")
    st.markdown("""
    * **Protocolo de Recepção / Entrada do Lote:**
      * **Vermifugação:** Aplicação de endectocida de alta concentração (ex: Eprinomectina ou Ivermectina 3,5%) na chegada.
      * **Vacinação:** Imunização contra clostridioses (com reforço) e vacina respiratória (pneumonias).
      * **Mineralização:** Aplicação injetável de complexo vitamínico ADE e minerais (Cobre, Zinco, Fósforo).
    * **Instruções para TIP (Terminação Intensiva a Pasto):**
      * Espaçamento de cocho recomendado: **40 a 50 cm por cabeça**.
      * Fornecimento diário de concentrado na proporção de **1,2% a 1,5% do Peso Vivo**.
      * Adaptação contínua nos primeiros 12 dias aumentando o volume fornecido gradativamente.
    """)
