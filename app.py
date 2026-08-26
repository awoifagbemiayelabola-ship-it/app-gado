import requests
import streamlit as st

# ---------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Sistema Integrado de Recria e Confinamento Bovino",
    page_icon="🐂",
    layout="wide",
)

st.title("🐂 Sistema Inteligente de Predição de Ganho de Peso & Nutrição")
st.caption(
    "Calculadora zootécnica com estimativa automática de GMD, Peso Ideal de Abate e Formulação de Ração."
)

# ---------------------------------------------------------
# 1. LOCALIZAÇÃO E ÉPOCA DO ANO
# ---------------------------------------------------------
st.sidebar.header("📍 Localização & Clima")

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

cidades_go = [
    "Goiânia",
    "Rio Verde",
    "Jataí",
    "Itumbiara",
    "Cristalina",
    "Porangatu",
    "Anápolis",
    "Luziânia",
]
cidade = st.sidebar.selectbox(
    "Cidade / Município:",
    cidades_go if "Goiás" in estado else ["Capital / Polo Regional"],
)

epoca_ano = st.sidebar.radio("Época do Ano:", ["Seca / Transição", "Águas (Chuva)"])

st.sidebar.divider()
st.sidebar.header("💵 Mercado & Cotações")
preco_arroba_magro = st.sidebar.number_input(
    "Preço da Arroba do Boi Magro/Bezerro (R$):", value=280.0, step=5.0
)
preco_arroba_gordo = st.sidebar.number_input(
    "Preço da Arroba do Boi Gordo (R$):", value=245.0, step=5.0
)

# ---------------------------------------------------------
# 2. ENTRADAS DO USUÁRIO (PESO INICIAL, RAÇA, SISTEMA, PASTO)
# ---------------------------------------------------------
st.header("1. Parâmetros do Lote e Sistema")

col_p_in, col_qtd, col_raca = st.columns(3)

with col_p_in:
    peso_entrada = st.number_input(
        "Peso Inicial de Entrada (kg/cabeça):",
        min_value=100.0,
        max_value=700.0,
        value=380.0,
        step=5.0,
    )

with col_qtd:
    qtd_animais = st.number_input(
        "Tamanho do Lote (Cabeças):",
        min_value=1,
        max_value=10000,
        value=100,
        step=10,
    )

with col_raca:
    raca = st.selectbox(
        "Raça ou Cruzamento:",
        [
            "Nelore (Zebuíno)",
            "Cruzamento Industrial (Angus x Nelore)",
            "Cruzamento Industrial (Senepol / Brangus)",
            "Anelorado Comercial",
            "Misto / Leiteiro",
        ],
    )

col_sis, col_pasto = st.columns(2)

with col_sis:
    fase_sistema = st.selectbox(
        "Estratégia Nutricional / Alimentação:",
        [
            "Sal Mineral Linha Branca (0,03% PV)",
            "Proteinado de Seca (0,25% PV)",
            "Proteinado Energético de Águas (0,35% PV)",
            "Recria Intensiva a Pasto (0,8% PV)",
            "Terminação Intensiva a Pasto - TIP (1,2% PV)",
            "Confinamento Tradicional com Volumoso (1,8% PV)",
            "Confinamento Grão Inteiro / PFT sem Volumoso (2,1% PV)",
        ],
    )

with col_pasto:
    if (
        "Confinamento" in fase_sistema
        and "TIP" not in fase_sistema
        and "PFT" not in fase_sistema
    ):
        pasto_tipo = "Confinamento (Sem Pasto)"
        st.info("Pasto desativado para Confinamento Fechado.")
    else:
        pasto_tipo = st.selectbox(
            "Capim / Qualidade do Pasto:",
            [
                "Brachiaria Marandu (Braviariao) - Bom Manejo",
                "Panicum Mombaça / Zuri / Quênia - Intensivo",
                "Brachiaria Decumbens - Pasto Degradado / Fraco",
                "Palhada de Milho / Braquiária Seca",
            ],
        )

st.divider()

# ---------------------------------------------------------
# 3. ENGINE ZOOTÉCNICA: CÁLCULO AUTOMÁTICO DE GMD E PESO IDEAL
# ---------------------------------------------------------
st.header("2. Resultados do Cálculo Automático (GMD e Peso Ideal)")


def calcular_desempenho_zootecnico(
    peso_in, raca_sel, alimento_sel, pasto_sel, epoca
):
    # A) Base do GMD pelo alimento/ração
    if "Linha Branca" in alimento_sel:
        gmd_base = 0.150 if "Seca" in epoca else 0.450
        rendimento = 52.0
    elif "Proteinado de Seca" in alimento_sel:
        gmd_base = 0.450
        rendimento = 52.5
    elif "Proteinado Energético" in alimento_sel:
        gmd_base = 0.750
        rendimento = 53.0
    elif "Recria Intensiva" in alimento_sel:
        gmd_base = 0.950
        rendimento = 53.5
    elif "TIP" in alimento_sel:
        gmd_base = 1.350
        rendimento = 54.5
    elif "Confinamento Tradicional" in alimento_sel:
        gmd_base = 1.500
        rendimento = 55.0
    else:  # Confinamento Grão Inteiro
        gmd_base = 1.600
        rendimento = 55.5

    # B) Fator de Raça (Eficiência Alimentar e Peso Ideal de Abate)
    if "Angus" in raca_sel:
        fator_raca = 1.15
        rendimento += 1.5
        peso_ideal_abate = 570.0  # Peso ideal para acabamento de gordura
    elif "Senepol" in raca_sel:
        fator_raca = 1.10
        rendimento += 1.0
        peso_ideal_abate = 550.0
    elif "Nelore" in raca_sel:
        fator_raca = 1.00
        peso_ideal_abate = 540.0
    elif "Anelorado" in raca_sel:
        fator_raca = 0.95
        peso_ideal_abate = 520.0
    else:  # Misto/Leiteiro
        fator_raca = 0.85
        rendimento -= 2.0
        peso_ideal_abate = 490.0

    # C) Ajuste pelo Pasto (se aplicável)
    fator_pasto = 1.0
    if "Confinamento (Sem Pasto)" not in pasto_sel:
        if "Mombaça" in pasto_sel or "Zuri" in pasto_sel:
            fator_pasto = 1.10
        elif "Marandu" in pasto_sel:
            fator_pasto = 1.00
        elif "Decumbens" in pasto_sel:
            fator_pasto = 0.88
        elif "Palhada" in pasto_sel:
            fator_pasto = 0.80

    # Se o animal ainda for muito leve (recria), o peso de saída meta da fase ajusta
    if peso_in < 300.0 and "Confinamento" not in alimento_sel:
        peso_meta_calculado = 420.0  # Meta de saída da recria para ir pro confinamento/TIP
    else:
        peso_meta_calculado = max(peso_ideal_abate, peso_in + 80.0)

    gmd_final = round(gmd_base * fator_raca * fator_pasto, 3)

    return gmd_final, peso_meta_calculado, rendimento


gmd_calculado, peso_saida_ideal, rendimento_est = (
    calcular_desempenho_zootecnico(
        peso_entrada, raca, fase_sistema, pasto_tipo, epoca_ano
    )
)

# Cálculos de tempo e ganho
ganho_peso_total = peso_saida_ideal - peso_entrada
dias_permanencia = (
    ganho_peso_total / gmd_calculado if gmd_calculado > 0 else 0
)
arrobas_saida = (peso_saida_ideal * (rendimento_est / 100.0)) / 15.0

# Análise de Ágio
agio_valor = preco_arroba_magro - preco_arroba_gordo
agio_percentual = ((preco_arroba_magro / preco_arroba_gordo) - 1) * 100

if agio_percentual <= 10:
    status_agio = "🟢 EXCELENTE (Ágio Baixo - Operação Muito Favorável)"
elif agio_percentual <= 18:
    status_agio = (
        "🟡 MODERADO (Exige bom ganho diário na engorda para compensar)"
    )
else:
    status_agio = "🔴 ALTO ÁGIO (Exige máxima eficiência alimentar no lote)"

# Exibição dos cards de resultados
res1, res2, res3, res4 = st.columns(4)
res1.metric(
    "Ganho Médio Diário (GMD)",
    f"{gmd_calculado:.3f} kg/dia",
    help="Calculado combinando Raça + Alimentação + Pasto",
)
res2.metric(
    "Peso Ideal de Saída",
    f"{peso_saida_ideal:.0f} kg",
    help="Peso recomendado para acabamento ideal de carcaça",
)
res3.metric(
    "Tempo de Permanência",
    f"{dias_permanencia:.0f} Dias",
    help="Dias necessários para atingir o peso meta",
)
res4.metric("Arrobas Finais Estimadas", f"{arrobas_saida:.2f} @")

st.info(
    f"📌 **Avaliação do Ágio na Compra:** {status_agio} (Ágio de **{agio_percentual:.1f}%** / R$ {agio_valor:.2f} por @)"
)

st.divider()

# ---------------------------------------------------------
# 4. FORMULAÇÃO DA RAÇÃO FEITA NA FAZENDA
# ---------------------------------------------------------
st.header("3. Ração e Mistura Recomendada (Fabricada na Fazenda)")


def gerar_receita_feita_fazenda(fase, epoca, peso, qtd_cab, dias):
    if "Linha Branca" in fase:
        tx_pv = 0.0003
        formula = {"Sal Mineral Pronto (Macrominerais + Microminerais)": 100.0}
        desc = "Sal mineral de linha branca para manutenção alimentar."
    elif "Proteinado de Seca" in fase:
        tx_pv = 0.0025
        formula = {
            "Milho Moído Fino (Fubá/Xerém)": 52.0,
            "Farelo de Soja 46%": 25.0,
            "Ureia Pecuária + Sulfato de Amônio (9:1)": 8.0,
            "Núcleo Mineral Proteinado": 15.0,
        }
        desc = "Proteinado para suprir a deficiência de proteína do capim seco."
    elif "Proteinado Energético" in fase:
        tx_pv = 0.0035
        formula = {
            "Milho Moído Fino": 68.0,
            "Farelo de Soja 46%": 18.0,
            "Sal Mineral com Monensina Sódica": 14.0,
        }
        desc = "Suplementação energética para potencializar o pasto das águas."
    elif "Recria Intensiva" in fase:
        tx_pv = 0.008
        formula = {
            "Milho Moído Fino": 70.0,
            "Farelo de Soja 46%": 22.0,
            "Núcleo Mineral com Tampão": 6.0,
            "Ureia + Sulfato (9:1)": 2.0,
        }
        desc = "Acelera a estrutura óssea e muscular no período de recria."
    elif "TIP" in fase:
        tx_pv = 0.012
        formula = {
            "Milho Moído Fino (Fubá/Xerém)": 72.0,
            "Farelo de Soja 46%": 21.0,
            "Núcleo TIP (Tampão + Virginiamicina)": 5.0,
            "Ureia + Sulfato (9:1)": 2.0,
        }
        desc = "Terminação Intensiva a Pasto. Alta energia para acabamento de gordura."
    elif "Confinamento Tradicional" in fase:
        tx_pv = 0.018
        formula = {
            "Milho Moído Fino": 74.0,
            "Farelo de Soja 46%": 18.0,
            "Núcleo Confinamento (Monensina + Tampão)": 6.0,
            "Ureia + Sulfato (9:1)": 2.0,
        }
        desc = "Dieta concentrada para confinamento. Acompanhar com 15% a 20% de volumoso."
    else:  # Grão Inteiro
        tx_pv = 0.021
        formula = {
            "Milho Grão Inteiro (Sem moer)": 85.0,
            "Pellet Proteico/Mineral Grão Inteiro": 15.0,
        }
        desc = "Dieta total sem necessidade de volumoso."

    consumo_cab_dia = peso * tx_pv
    consumo_lote_dia = consumo_cab_dia * qtd_cab
    consumo_lote_total_ton = (consumo_lote_dia * dias) / 1000.0

    return consumo_cab_dia, consumo_lote_dia, consumo_lote_total_ton, formula, desc


c_cab, c_dia, c_tot_ton, receita, desc_nutri = gerar_receita_feita_fazenda(
    fase_sistema, epoca_ano, peso_entrada, qtd_animais, dias_permanencia
)

st.write(f"💡 **Diretriz Nutricional:** {desc_nutri}")

c1, c2, c3 = st.columns(3)
c1.metric("Consumo Diário por Cabeça", f"{c_cab:.2f} kg/dia")
c2.metric("Consumo Diário do Lote", f"{c_dia:.1f} kg/dia")
c3.metric("Ração Total no Período do Lote", f"{c_tot_ton:.2f} Toneladas")

st.markdown("#### 📦 Proporção para 100 kg de Ração e Consumo do Lote")

col_f1, col_f2 = st.columns([1.3, 1])

with col_f1:
    for item, pct in receita.items():
        kg_dia = (c_dia * pct) / 100.0
        st.write(
            f"• **{item}**: `{pct}%` — **{kg_dia:.1f} kg/dia para o lote**"
        )

with col_f2:
    st.success("""
    **Principais Nutrientes Inclusos:**
    * **Energia (NDT):** Amido (Milho Moído/Grão)
    * **Proteína Bruta (PB):** Farelo de Soja + Ureia Pecuária
    * **Aditivos:** Monensina Sódica / Virginiamicina
    * **Manejo Sanitário:** Tamponantes contra acidose ruminal
    """)

# ---------------------------------------------------------
# 5. MANEJO DE PASTAGEM
# ---------------------------------------------------------
if "Confinamento (Sem Pasto)" not in pasto_tipo:
    st.divider()
    st.header("🌱 Manejo da Pastagem")
    m1, m2 = st.columns(2)
    if "Mombaça" in pasto_tipo or "Zuri" in pasto_tipo:
        m1.metric("Altura Recomendada de Entrada", "70 - 85 cm")
        m2.metric("Altura Recomendada de Saída", "35 - 40 cm")
    elif "Marandu" in pasto_tipo:
        m1.metric("Altura Recomendada de Entrada", "25 - 30 cm")
        m2.metric("Altura Recomendada de Saída", "15 cm")
    else:
        m1.metric("Altura Recomendada de Entrada", "20 - 25 cm")
        m2.metric("Altura Recomendada de Saída", "10 - 12 cm")

st.warning(
    "⚠️ **Atenção:** Em dietas com Ureia ou alto teor de amido (como TIP e Confinamento), faça adaptação gradual durante os primeiros 14 dias para evitar acidose ruminal ou intoxicação."
)
