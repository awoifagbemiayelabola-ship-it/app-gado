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

st.title("🐂 Sistema Especialista de Recria & Confinamento Bovino")
st.caption(
    "Planejamento Zootécnico, Nutricional e Econômico (Análise de Ágio e Viabilidade)"
)

# ---------------------------------------------------------
# 1. LOCALIZAÇÃO E EPOCA DO ANO
# ---------------------------------------------------------
st.sidebar.header("📍 Localização & Clima")

estado = st.sidebar.selectbox("Estado:", ["Goiás (GO)", "Mato Grosso (MT)", "Mato Grosso do Sul (MS)", "Minas Gerais (MG)", "São Paulo (SP)"])

cidades_go = ["Goiânia", "Rio Verde", "Jataí", "Itumbiara", "Cristalina", "Porangatu", "Anápolis", "Luziânia"]
cidade = st.sidebar.selectbox("Cidade / Município:", cidades_go if "Goiás" in estado else ["Capital / Polo Regional"])

epoca_ano = st.sidebar.radio("Época do Ano:", ["Seca / Transição", "Águas (Chuva)"])

st.sidebar.divider()
st.sidebar.header("💵 Mercado & Cotações")
preco_arroba_magro = st.sidebar.number_input("Preço da Arroba do Boi Magro/Bezerro (R$):", value=280.0, step=5.0)
preco_arroba_gordo = st.sidebar.number_input("Preço da Arroba do Boi Gordo (R$):", value=245.0, step=5.0)

# ---------------------------------------------------------
# 2. SELEÇÃO DA SISTEMA E RAÇA
# ---------------------------------------------------------
st.header("1. Seleção do Sistema, Raça e Categoria")

col_sis, col_raca, col_qtd = st.columns(3)

with col_sis:
    fase_sistema = st.selectbox(
        "Fase / Sistema de Produção:",
        [
            "Recria a Pasto Intensificada (Suplementação)",
            "Recria Confinada / Sequestro de Bezerros",
            "Confinamento Tradicional (Grão Moído + Volumoso)",
            "Confinamento Sem Volumoso / PFT (Grão Moído + Pellet)",
            "Terminação Intensiva a Pasto (TIP)",
        ]
    )

with col_raca:
    raca = st.selectbox(
        "Raça ou Cruzamento:",
        [
            "Nelore (Zebuíno) - Rústico e Adaptado",
            "Cruzamento Industrial (Angus x Nelore) - Precoce / Alta Eficiência",
            "Cruzamento Industrial (Senepol / Brangus)",
            "Anelorado / Anelorado Comercial",
            "Gado Misto / Leiteiro",
        ]
    )

with col_qtd:
    qtd_animais = st.number_input("Tamanho do Lote (Cabeças):", min_value=1, max_value=10000, value=100, step=10)

# Parâmetros de desempenho ajustados por Raça
if "Angus" in raca or "Senepol" in raca:
    fator_gmd = 1.15  # +15% de desempenho potencial
    rendimento_carcaca_est = 55.5
elif "Nelore" in raca:
    fator_gmd = 1.00
    rendimento_carcaca_est = 54.0
else:
    fator_gmd = 0.88
    rendimento_carcaca_est = 51.5

st.divider()

# ---------------------------------------------------------
# 3. PESOS, METAS E ANÁLISE DE ÁGIO
# ---------------------------------------------------------
st.header("2. Metas de Pesos, Permanência e Análise de Ágio")

# Sugestões de entrada e saída por sistema
if "Recria" in fase_sistema:
    peso_in_default = 210.0  # Entrada bezerro desmamado
    peso_out_default = 390.0 # Saída garrote para terminação
    gmd_base = 0.750
elif "Confinamento" in fase_sistema or "TIP" in fase_sistema:
    peso_in_default = 410.0  # Entrada boi magro
    peso_out_default = 560.0 # Saída boi gordo (18 a 20 arrobas)
    gmd_base = 1.500

col_p1, col_p2, col_p3 = st.columns(3)

with col_p1:
    peso_entrada = st.number_input("Peso Inicial de Entrada (kg/cab):", value=peso_in_default, step=5.0)
    
with col_p2:
    peso_saida = st.number_input("Peso Meta de Saída (kg/cab):", value=peso_out_default, step=5.0)

with col_p3:
    gmd_projetado = st.number_input("Ganho Médio Diário Esperado (kg/dia):", value=round(gmd_base * fator_gmd, 3), step=0.05)

# Cálculos Zootécnicos e de Tempo
ganho_total_kg = peso_saida - peso_entrada
dias_permanencia = ganho_total_kg / gmd_projetado if gmd_projetado > 0 else 0
arrobas_entrada = peso_entrada / 30.0
arrobas_saida = (peso_saida * (rendimento_carcaca_est / 100)) / 15.0

# Cálculo do Ágio da Arroba
agio_valor = preco_arroba_magro - preco_arroba_gordo
agio_percentual = ((preco_arroba_magro / preco_arroba_gordo) - 1) * 100

st.subheader("📊 Indicadores de Desempenho e Ágio da Compra")

c_res1, c_res2, c_res3, c_res4 = st.columns(4)
c_res1.metric("Tempo de Permanência", f"{dias_permanencia:.0f} Dias")
c_res2.metric("Ganho de Peso Total", f"{ganho_total_kg:.1f} kg")
c_res3.metric("Arrobas Finais Estimadas", f"{arrobas_saida:.2f} @")

# Avaliação do Ágio
if agio_percentual <= 10:
    status_agio = "🟢 EXCELENTE (Ágio Baixo - Margem Favorável)"
elif agio_percentual <= 18:
    status_agio = "🟡 MODERADO (Exige bom ganho na terminação para compensar)"
else:
    status_agio = "🔴 ALTO ÁGIO (Risco Aumentado - Exige máxima eficiência alimentar)"

c_res4.metric("Ágio Pago na Arroba", f"{agio_percentual:.1f}%", help=f"Diferença de R$ {agio_valor:.2f}/@ entre o magro e o gordo")
st.info(f"📌 **Status do Ágio na Compra:** {status_agio}")

st.divider()

# ---------------------------------------------------------
# 4. FORMULAÇÃO DA RAÇÃO FEITA NA FAZENDA
# ---------------------------------------------------------
st.header("3. Ração e Nutrição (Fabricada na Fazenda com Grão Moído)")

def gerar_receita(fase, epoca, peso):
    if "Recria a Pasto" in fase:
        if "Seca" in epoca:
            taxa_pv = 0.0025 # 0.25% PV
            formula = {
                "Milho Moído (Fubá/Xerém)": 55.0,
                "Farelo de Soja 46%": 25.0,
                "Ureia Pecuária + Sulfato de Amônio (9:1)": 5.0,
                "Sal Mineral / Núcleo Proteinado": 15.0
            }
            desc = "Proteinado de Seca. Mantém o gado ganhando peso na palhada."
        else:
            taxa_pv = 0.003 # 0.3% PV
            formula = {
                "Milho Moído Fino": 68.0,
                "Farelo de Soja 46%": 18.0,
                "Núcleo Mineral com Monensina Sódica": 14.0
            }
            desc = "Proteinado Energético das Águas. Potencializa o capim verde."

    elif "Recria Confinada" in fase:
        taxa_pv = 0.012 # 1.2% PV
        formula = {
            "Milho Moído Fino": 62.0,
            "Farelo de Soja 46%": 22.0,
            "Casca de Soja / Polpa Cítrica": 10.0,
            "Núcleo Confinamento / Tampão": 4.0,
            "Ureia + Sulfato (9:1)": 2.0
        }
        desc = "Ração de Crescimento e Estruturação Óssea (sem acúmulo precoce de gordura)."

    elif "Confinamento Tradicional" in fase:
        taxa_pv = 0.018 # 1.8% PV (Concentrado)
        formula = {
            "Milho Moído Fino": 74.0,
            "Farelo de Soja 46% ou Algodão 38%": 18.0,
            "Núcleo Mineral com Tampão, Monensina e Virginiamicina": 6.0,
            "Ureia Pecuária + Sulfato (9:1)": 2.0
        }
        desc = "Confinamento de Alto Rendimento. Acompanhar com 15% a 20% de Silagem/Volumoso na MS."

    elif "Confinamento Sem Volumoso" in fase:
        taxa_pv = 0.021 # 2.1% PV
        formula = {
            "Milho Moído Fino / Triturado": 70.0,
            "Pellet Proteico / Mineral Específico sem Volumoso": 30.0
        }
        desc = "Sistema PFT / Dieta Total sem necessidade de picar silagem ou capim."

    else: # TIP
        taxa_pv = 0.012 # 1.2% PV
        formula = {
            "Milho Moído Fino (Fubá/Xerém)": 72.0,
            "Farelo de Soja 46%": 21.0,
            "Núcleo TIP (Tampão + Virginiamicina)": 5.0,
            "Ureia Pecuária + Sulfato (9:1)": 2.0
        }
        desc = "Terminação Intensiva a Pasto. Elimina a necessidade de estrutura de confinamento."

    consumo_cabeca = peso * taxa_pv
    consumo_lote_dia = consumo_cabeca * qtd_animais
    consumo_lote_total_periodo = (consumo_lote_dia * dias_permanencia) / 1000 # Toneladas

    return consumo_cabeca, consumo_lote_dia, consumo_lote_total_periodo, formula, desc

c_cabeca, c_lote_dia, c_lote_total, receita_dict, descricao_nutri = gerar_receita(fase_sistema, epoca_ano, peso_entrada)

st.subheader(f"🥣 Formulação para {fase_sistema}")
st.write(f"💡 **Diretriz Tática:** {descricao_nutri}")

col_n1, col_n2, col_n3 = st.columns(3)
col_n1.metric("Consumo Diário por Cabeça", f"{c_cabeca:.2f} kg/dia")
col_n2.metric("Consumo Diário do Lote", f"{c_lote_dia:.1f} kg/dia")
col_n3.metric("Ração Total no Período", f"{c_lote_total:.2f} Toneladas")

st.markdown("#### 📦 Mistura e Nutrientes para 100 kg de Ração")

col_ing, col_tot = st.columns([1.3, 1])

with col_ing:
    for item, pct in receita_dict.items():
        kg_mistura_dia = (c_lote_dia * pct) / 100.0
        st.write(f"• **{item}**: `{pct}%` — **{kg_mistura_dia:.1f} kg/dia no batidão do lote**")

with col_tot:
    st.success(f"""
    **Nutrientes Principais Inclusos:**
    * **Energia (NDT):** Amido do Milho Moído
    * **Proteína Bruta (PB):** Farelo de Soja / Algodão e Ureia Pecuária
    * **Promotores de Crescimento:** Virginiamicina / Monensina Sódica
    * **Tamponantes:** Bicarbonato de Sódio / Óxido de Magnésio (Evita Acidose)
    """)

st.divider()

# ---------------------------------------------------------
# 5. MANEJO DE PASTAGENS (QUANDO APLICÁVEL)
# ---------------------------------------------------------
if "Pasto" in fase_sistema:
    st.header("🌱 Manejo do Pasto na Recria / TIP")
    capim = st.selectbox("Capim Predominante:", ["Brachiaria brizantha (Marandu / Braquiariao)", "Panicum maximum (Mombaça)", "Panicum maximum (Zuri)", "Panicum maximum (Quênia)"])
    
    tabela_alturas = {
        "Brachiaria brizantha (Marandu / Braquiariao)": ("25 - 30 cm", "15 cm"),
        "Panicum maximum (Mombaça)": ("85 - 90 cm", "40 - 50 cm"),
        "Panicum maximum (Zuri)": ("70 - 75 cm", "30 - 35 cm"),
        "Panicum maximum (Quênia)": ("60 - 70 cm", "30 cm")
    }
    
    h_in, h_out = tabela_alturas[capim]
    m1, m2 = st.columns(2)
    m1.metric("Altura de Entrada do Gado", h_in)
    m2.metric("Altura de Saída (Resíduo)", h_out)

st.warning("⚠️ **Adaptação Obrigatória de Ureia e Amido:** Durante os primeiros 14 dias de transição para dietas de alta energia/ureia, forneça apenas 50% da dose recomendada para evitar acidose ruminal e intoxicação.")
