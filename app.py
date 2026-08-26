import streamlit as st

# ---------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Estratégia Perfeita de Recria e Engorda Bovino",
    page_icon="🐂",
    layout="wide",
)

st.title("🐂 Sistema Especialista de Matriz Nutricional (Seca vs. Águas)")
st.caption(
    "Planejamento Zootécnico e Econômico Infalível por Peso, Raça e Estação do Ano"
)

# ---------------------------------------------------------
# 1. PAINEL LATERAL: ENTRADAS OBRIGATÓRIAS
# ---------------------------------------------------------
st.sidebar.header("🗓️ 1. Estação do Ano (Determinante)")
epoca_ano = st.sidebar.radio(
    "Selecione a Época do Ano Atual/Planejada:",
    ["Seca / Transição (Capim Seco)", "Águas (Capim Verde e Nutritivo)"],
)

st.sidebar.divider()
st.sidebar.header("🧪 2. Perfil dos Insumos")
nucleo_com_ureia = st.sidebar.checkbox(
    "O Núcleo/Concentrado que utilizo JÁ TEM UREIA?",
    value=False,
    help="Se ativado, cancela a inclusão de ureia extra para evitar intoxicação.",
)

st.sidebar.divider()
st.sidebar.header("💵 3. Mercado & Arroba (R$)")
preco_arroba_compra = st.sidebar.number_input(
    "Preço da Arroba de COMPRA (R$):", value=280.0, step=5.0
)
preco_arroba_venda = st.sidebar.number_input(
    "Preço da Arroba de VENDA (R$):", value=245.0, step=5.0
)

# ---------------------------------------------------------
# 2. INFORMÇÕES DO ANIMAL
# ---------------------------------------------------------
st.header("1. Perfil do Rebanho e Peso Atual")

col_raca, col_peso, col_qtd = st.columns(3)

with col_raca:
    raca = st.selectbox(
        "Raça ou Cruzamento:",
        [
            "Nelore (Zebuíno)",
            "Cruzamento Industrial (Angus x Nelore)",
            "Cruzamento Industrial (Senepol / Brangus)",
            "Anelorado / Comercial",
            "Misto / Leiteiro",
        ],
    )

with col_peso:
    peso_atual = st.number_input(
        "Peso Atual do Animal (kg/cabeça):",
        min_value=120.0,
        max_value=750.0,
        value=320.0,
        step=5.0,
    )

with col_qtd:
    qtd_cabecas = st.number_input(
        "Tamanho do Lote (Cabeças):", min_value=1, value=100, step=10
    )

st.divider()

# ---------------------------------------------------------
# 3. MATRIZ INFALÍVEL DE ESTRATÉGIA (SECA VS ÁGUAS X PESO)
# ---------------------------------------------------------

eh_seca = "Seca" in epoca_ano

# Define Fase Zootécnica, Estratégia Recomendada e Taxa de Consumo (% do Peso Vivo)
if peso_atual < 260.0:
    fase_atual = "Desmama / Recria Inicial (Bezerro)"
    if eh_seca:
        estrategia_nome = "Proteinado de Seca (0,25% PV)"
        tx_pv = 0.0025
        gmd_base = 0.500
    else:
        estrategia_nome = "Proteinado Energético de Águas (0,35% PV)"
        tx_pv = 0.0035
        gmd_base = 0.850
    peso_meta = 390.0

elif 260.0 <= peso_atual < 390.0:
    fase_atual = "Recria Intermediária (Garrote/Boi Magro)"
    if eh_seca:
        estrategia_nome = "Proteinado Energético de Seca (0,5% PV)"
        tx_pv = 0.0050
        gmd_base = 0.750
    else:
        estrategia_nome = "Recria Intensiva a Pasto - TIP Recria (0,8% PV)"
        tx_pv = 0.0080
        gmd_base = 1.100
    peso_meta = 420.0

else:
    fase_atual = "Terminação / Engorda Final"
    if eh_seca:
        estrategia_nome = "Confinamento Tradicional ou PFT (1,8% a 2,1% PV)"
        tx_pv = 0.0190
        gmd_base = 1.500
    else:
        estrategia_nome = "Terminação Intensiva a Pasto - TIP (1,2% a 1,5% PV)"
        tx_pv = 0.0135
        gmd_base = 1.350
    peso_meta = 540.0 if "Nelore" in raca else 570.0

# Eficiência da Raça
if "Angus" in raca:
    fator_raca, rend_carcaca = 1.18, 55.5
elif "Senepol" in raca or "Brangus" in raca:
    fator_raca, rend_carcaca = 1.10, 54.5
elif "Nelore" in raca:
    fator_raca, rend_carcaca = 1.00, 54.0
elif "Anelorado" in raca:
    fator_raca, rend_carcaca = 0.92, 52.5
else:
    fator_raca, rend_carcaca = 0.80, 50.5

gmd_final = round(gmd_base * fator_raca, 3)
ganho_necessario = peso_meta - peso_atual
dias_permanencia = round(
    ganho_necessario / gmd_final if gmd_final > 0 else 0
)

# ---------------------------------------------------------
# 4. DIAGNÓSTICO FINANCEIRO & ANÁLISE DE ÁGIO
# ---------------------------------------------------------
arrobas_entrada = peso_atual / 30.0
custo_compra_cab = arrobas_entrada * preco_arroba_compra
arrobas_saida = (peso_meta * (rend_carcaca / 100.0)) / 15.0
receita_venda_cab = arrobas_saida * preco_arroba_venda

agio_pct = ((preco_arroba_compra / preco_arroba_venda) - 1) * 100

st.header("2. Veredito Estratégico & Análise Econômica")

col_v1, col_v2 = st.columns([1.5, 1])

with col_v1:
    st.subheader(f"📌 Estratégia Definida: **{estrategia_nome}**")
    st.write(f"• **Estação Detectada:** {'☀️ **SECA** (Foco em Proteína / Ureia)' if eh_seca else '🌧️ **ÁGUAS** (Foco em Amido / Energia)'}")
    st.write(f"• **Fase Zootécnica:** {fase_atual}")
    st.write(f"• **Ganho Diário Projetado (GMD):** `{gmd_final:.3f} kg/dia`")
    st.write(f"• **Tempo Exato do Lote:** `{dias_permanencia} dias` ({dias_permanencia/30:.1f} meses)")

with col_v2:
    if agio_pct <= 10.0:
        st.success(f"🟢 **ÁGIO BAIXO ({agio_pct:.1f}%):** Negócio muito rentável. O ganho de peso paga a operação rápido.")
    elif agio_pct <= 18.0:
        st.warning(f"🟡 **ÁGIO MODERADO ({agio_pct:.1f}%):** Compensa desde que mantenha a ração ajustada sem desperdício.")
    else:
        st.error(f"🔴 **ÁGIO ALTO ({agio_pct:.1f}%):** Risco elevado. Exige ganho de peso acelerado para diluir a compra.")

    st.metric("Arrobas Finais Projetadas", f"{arrobas_saida:.2f} @")
    st.metric("Faturamento Estimado/Cabeça", f"R$ {receita_venda_cab:.2f}")

st.divider()

# ---------------------------------------------------------
# 5. FORMULAÇÃO MATEMÁTICA DA RAÇÃO
# ---------------------------------------------------------
st.header("3. Receita Exata para Fabricar na Fazenda (Por 100 kg)")


def gerar_formula_perfeita(eh_seca_flag, fase, com_ureia):
    if eh_seca_flag:
        if "Desmama" in fase:
            milho, soja, ureia, nucleo = 50.0, 28.0, 7.0, 15.0
            desc = "Proteinado de Seca: Mantém o rume ativo na palhada sem perda de peso."
        elif "Recria" in fase:
            milho, soja, ureia, nucleo = 65.0, 20.0, 5.0, 10.0
            desc = "Proteinado Energético de Seca: Estimula o crescimento de carcaça na palhada seca."
        else:
            milho, soja, ureia, nucleo = 75.0, 17.0, 2.0, 6.0
            desc = "Ração de Confinamento na Seca: Alta densidade de amido para terminação rápida."
    else:  # ÁGUAS
        if "Desmama" in fase:
            milho, soja, ureia, nucleo = 72.0, 16.0, 0.0, 12.0
            desc = "Proteinado de Águas: Amido para aproveitar o excesso de proteína do capim verde."
        elif "Recria" in fase:
            milho, soja, ureia, nucleo = 78.0, 14.0, 1.0, 7.0
            desc = "Ração de TIP Recria: Impulsiona o ganho diário para antecipar o abate."
        else:
            milho, soja, ureia, nucleo = 80.0, 13.0, 1.0, 6.0
            desc = "Ração TIP Terminação nas Águas: Acabamento perfeito de gordura no pasto verde."

    if com_ureia and ureia > 0:
        soja += round(ureia * 1.5, 1)
        milho -= round(ureia * 0.5, 1)
        ureia = 0.0

    dict_f = {
        "Milho Moído Fino (Fubá)": milho,
        "Farelo de Soja 46%": soja,
    }
    if ureia > 0:
        dict_f["Ureia Pecuária + Sulfato de Amônio (9:1)"] = ureia
    dict_f["Núcleo Mineral / Tampão"] = nucleo

    return dict_f, desc


formula_dict, orientacao = gerar_formula_perfeita(
    eh_seca, fase_atual, nucleo_com_ureia
)

consumo_dia_cab = peso_atual * tx_pv
consumo_dia_lote = consumo_dia_cab * qtd_cabecas
consumo_total_ton = (consumo_dia_lote * dias_permanencia) / 1000.0

m_c1, m_c2, m_c3 = st.columns(3)
m_c1.metric("Consumo/Cabeça/Dia", f"{consumo_dia_cab:.2f} kg")
m_c2.metric("Consumo do Lote/Dia", f"{consumo_dia_lote:.1f} kg")
m_c3.metric("Ração Total no Período", f"{consumo_total_ton:.2f} Toneladas")

st.info(f"💡 **Diretriz Tática:** {orientacao}")

col_f1, col_f2 = st.columns([1.3, 1])

with col_f1:
    st.markdown("#### **Mistura em Porcentagem (Batidão de 100 kg):**")
    for ing, pct in formula_dict.items():
        kg_lote = (consumo_dia_lote * pct) / 100.0
        st.write(
            f"• **{ing}**: `{pct:.1f}%` $\\rightarrow$ **({kg_lote:.1f} kg/dia para todo o lote)**"
        )

with col_f2:
    st.success(f"""
    **Regra de Ouro da Estação:**
    * **Nas Águas:** O capim já entrega a proteína. A ração precisa ser **rica em Amido (Milho)**.
    * **Na Seca:** O capim perde proteína. A ração precisa ser **rica em Nitrogênio (Ureia/Soja)**.
    """)

