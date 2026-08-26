import streamlit as st

# ---------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Sistema Especialista de Decisão Zootécnica & Lucro Bovino",
    page_icon="🐂",
    layout="wide",
)

st.title("🐂 Sistema Especialista de Decisão Zootécnica & Lucro")
st.caption(
    "Determinação matemática de dieta, análise de ágio, recomendação de ração e projeção de carcaça."
)

# ---------------------------------------------------------
# 1. ENTRADAS: LOCALIZAÇÃO, MERCADO, ANIMAL E PESO
# ---------------------------------------------------------
st.sidebar.header("📍 Localização & Época")
estado = st.sidebar.selectbox(
    "Estado:",
    [
        "Goiás (GO)",
        "Mato Grosso (MT)",
        "Mato Grosso do Sul (MS)",
        "Minas Gerais (MG)",
        "São Paulo (SP)",
    ],
)
epoca_ano = st.sidebar.radio("Época do Ano:", ["Seca / Transição", "Águas (Chuva)"])

st.sidebar.divider()
st.sidebar.header("💵 Mercado & Cotações (R$)")
preco_arroba_compra = st.sidebar.number_input(
    "Preço da Arroba de COMPRA (Magro/Bezerro) - R$:", value=280.0, step=5.0
)
preco_arroba_venda = st.sidebar.number_input(
    "Preço da Arroba de VENDA (Gordo Projetado) - R$:", value=245.0, step=5.0
)

st.header("1. Informações do Animal")

c_raca, c_peso, c_qtd = st.columns(3)

with c_raca:
    raca = st.selectbox(
        "Selecione a Raça ou Cruzamento:",
        [
            "Nelore (Zebuíno)",
            "Cruzamento Industrial (Angus x Nelore)",
            "Cruzamento Industrial (Senepol / Brangus)",
            "Anelorado / Comercial",
            "Misto / Leiteiro",
        ],
    )

with c_peso:
    peso_atual = st.number_input(
        "Peso Atual do Animal (kg/cabeça):",
        min_value=100.0,
        max_value=750.0,
        value=320.0,
        step=5.0,
    )

with c_qtd:
    qtd_cabecas = st.number_input(
        "Tamanho do Lote (Cabeças):", min_value=1, value=100, step=10
    )

st.divider()

# ---------------------------------------------------------
# 2. MOTOR DE DECISÃO ZOOTÉCNICA (100% LÓGICO E DETERMINÍSTICO)
# ---------------------------------------------------------

# A) Definição Automática da Fase e Estratégia de Alimentação pelo Peso
if peso_atual < 260.0:
    fase_atual = "Desmama / Recria Inicial"
    tipo_alimento = (
        "Proteinado de Seca (0,25% PV)"
        if "Seca" in epoca_ano
        else "Proteinado Energético de Águas (0,35% PV)"
    )
elif 260.0 <= peso_atual < 390.0:
    fase_atual = "Recria Intermediária / Crescimento"
    tipo_alimento = (
        "Proteinado Energético (0,5% PV)"
        if "Seca" in epoca_ano
        else "Suplemento de Recria Intensiva (0,8% PV)"
    )
else:
    fase_atual = "Terminação / Engorda"
    tipo_alimento = "Ração de Confinamento / TIP (1,5% a 2,0% PV)"

# B) Definição de Ganho Médio Diário (GMD), Rendimento e Peso de Abate pela Raça
if "Angus" in raca:
    fator_gmd = 1.18
    rend_carcaca = 55.5
    peso_abate_ideal = 560.0
elif "Senepol" in raca or "Brangus" in raca:
    fator_gmd = 1.10
    rend_carcaca = 54.5
    peso_abate_ideal = 540.0
elif "Nelore" in raca:
    fator_gmd = 1.00
    rend_carcaca = 54.0
    peso_abate_ideal = 530.0
elif "Anelorado" in raca:
    fator_gmd = 0.92
    rend_carcaca = 52.5
    peso_abate_ideal = 510.0
else:  # Misto / Leiteiro
    fator_gmd = 0.80
    rend_carcaca = 50.5
    peso_abate_ideal = 480.0

# Ajuste de GMD pelo Tipo de Alimentação Recomendado
if "Sal Mineral" in tipo_alimento:
    gmd_base = 0.350
elif "Proteinado de Seca" in tipo_alimento:
    gmd_base = 0.500
elif "Proteinado Energético" in tipo_alimento:
    gmd_base = 0.800
elif "Recria Intensiva" in tipo_alimento:
    gmd_base = 1.050
else:  # Confinamento / TIP
    gmd_base = 1.450

gmd_calculado = round(gmd_base * fator_gmd, 3)

# Se o animal já estiver em terminação, a meta é o peso ideal de abate; na recria, é a transição
if peso_atual >= 390.0:
    peso_saida_meta = max(peso_abate_ideal, peso_atual + 60.0)
else:
    peso_saida_meta = 410.0  # Meta para finalizar a recria e entrar na engorda

ganho_necessario = peso_saida_meta - peso_atual
dias_necessarios = (
    ganho_necessario / gmd_calculado if gmd_calculado > 0 else 0
)

# ---------------------------------------------------------
# 3. ANÁLISE ECONÔMICA, ÁGIO E VALOR DE REVENDA
# ---------------------------------------------------------
arrobas_entrada = peso_atual / 30.0
custo_aquisicao_cabeca = arrobas_entrada * preco_arroba_compra

arrobas_saida = (peso_saida_meta * (rend_carcaca / 100.0)) / 15.0
receita_bruta_cabeca = arrobas_saida * preco_arroba_venda

agio_reais = preco_arroba_compra - preco_arroba_venda
agio_pct = ((preco_arroba_compra / preco_arroba_venda) - 1) * 100

if agio_pct <= 10.0:
    status_agio = "🟢 EXCELENTE COMPENSAÇÃO (Margem Alta)"
    diagnostico_viabilidade = "COMPENSA MUITO! O custo da arroba comprada está alinhado com o preço de venda. O ganho de peso gerará lucro rápido."
elif 10.0 < agio_pct <= 18.0:
    status_agio = "🟡 COMPENSA COM EFICIÊNCIA (Margem Moderada)"
    diagnostico_viabilidade = "COMPENSA, desde que você utilize a ração de alta performance formulada abaixo para diluir o ágio no ganho de arrobas no pasto/cocho."
else:
    status_agio = "🔴 ALTO ÁGIO (Risco Elevado)"
    diagnostico_viabilidade = "NÃO COMPENSA COMPRAR NESTE PREÇO sem negociação de desconto, pois o valor pago na carcaça de entrada exige um custo de ração extremamente baixo para não dar prejuízo."

# Exibição do Diagnóstico
st.header("2. Diagnóstico de Viabilidade, Ágio e Retorno Financeiro")

st.markdown(f"### **Status:** {status_agio}")
st.write(f"👉 **Parecer Técnico:** {diagnostico_viabilidade}")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Ágio da Arroba (%)", f"{agio_pct:.1f}%")
m2.metric("Valor Estimado de Compra", f"R$ {custo_aquisicao_cabeca:.2f}")
m3.metric("Arrobas Finais (@)", f"{arrobas_saida:.2f} @")
m4.metric("Valor de Revenda Projetado", f"R$ {receita_bruta_cabeca:.2f}")

st.divider()

# ---------------------------------------------------------
# 4. PRESCRIÇÃO NUTRICIONAL E FORMULAÇÃO DA MELHOR RAÇÃO
# ---------------------------------------------------------
st.header("3. Prescrição de Nutrição e Formulação Própria da Ração")

st.info(
    f"📌 **Fase Detectada:** {fase_atual} | **Estratégia Recomendada:** {tipo_alimento}"
)


def calcular_formula_racao(estratégia, peso_in):
    if "Proteinado de Seca" in estratégia:
        tx_pv = 0.0025
        formula = {
            "Milho Moído Fino (Fubá/Xerém)": 50.0,
            "Farelo de Soja 46%": 28.0,
            "Ureia Pecuária + Sulfato de Amônio (9:1)": 7.0,
            "Sal Mineral / Núcleo Proteinado": 15.0,
        }
        resumo = "Proteinado concentrado para manter o ganho na seca sem perda de peso."

    elif "Proteinado Energético" in estratégia:
        tx_pv = 0.005
        formula = {
            "Milho Moído Fino": 65.0,
            "Farelo de Soja 46%": 20.0,
            "Núcleo Mineral com Monensina": 10.0,
            "Ureia Pecuária + Sulfato (9:1)": 5.0,
        }
        resumo = "Suplemento energizante para aceleração de carcaça na recria."

    elif "Recria Intensiva" in estratégia:
        tx_pv = 0.008
        formula = {
            "Milho Moído Fino": 70.0,
            "Farelo de Soja 46%": 22.0,
            "Núcleo Mineral com Tampão": 6.0,
            "Ureia Pecuária + Sulfato (9:1)": 2.0,
        }
        resumo = "Ração de alto desempenho para estruturar carcaça em tempo recorde."

    else:  # Terminação / Engorda
        tx_pv = 0.018
        formula = {
            "Milho Moído Fino": 75.0,
            "Farelo de Soja 46%": 17.0,
            "Núcleo Confinamento (Virginiamicina + Monensina + Tampão)": 6.0,
            "Ureia Pecuária + Sulfato (9:1)": 2.0,
        }
        resumo = "Ração de engorda rápida para acabamento perfeito de gordura na carcaça."

    consumo_dia_cab = peso_in * tx_pv
    consumo_dia_lote = consumo_dia_cab * qtd_cabecas
    consumo_total_periodo_ton = (consumo_dia_lote * dias_necessarios) / 1000.0

    return (
        consumo_dia_cab,
        consumo_dia_lote,
        consumo_total_periodo_ton,
        formula,
        resumo,
    )


c_cabeca, c_lote_dia, c_tot_ton, formula_dict, desc_nutri = (
    calcular_formula_racao(tipo_alimento, peso_atual)
)

r1, r2, r3, r4 = st.columns(4)
r1.metric("GMD Projetado", f"{gmd_calculado:.3f} kg/dia")
r2.metric("Tempo de Permanência", f"{dias_necessarios:.0f} Dias")
r3.metric("Consumo/Cabeça/Dia", f"{c_cabeca:.2f} kg")
r4.metric("Ração Total para o Lote", f"{c_tot_ton:.2f} Toneladas")

st.markdown("#### 🥣 Receita de Ração Magnífica para Fabricar na Fazenda (Para cada 100 kg de misturador)")

col_ing, col_metrica = st.columns([1.3, 1])

with col_ing:
    for ingrediente, porcentagem in formula_dict.items():
        kg_lote_dia = (c_lote_dia * porcentagem) / 100.0
        st.write(
            f"• **{ingrediente}**: `{porcentagem:.1f}%` — **({kg_lote_dia:.1f} kg/dia para todo o lote)**"
        )

with col_metrica:
    st.success(f"""
    **Garantia Nutricional:**
    * **Objetivo:** {desc_nutri}
    * **Rendimento de Carcaça Estimado:** `{rend_carcaca}%`
    * **Peso Ideal de Abate/Saída:** `{peso_saida_meta:.0f} kg`
    """)

st.warning(
    "⚠️ **Protocolo de Adaptação Secreto:** Nos primeiros 14 dias, forneça 50% do consumo diário previsto para adaptar os microrganismos do rume à Ureia e ao Amido do milho, evitando acidose."
)
