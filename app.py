import requests
import streamlit as st

# ---------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Especialista Zootécnico - Nutrição de Grão Moído (Goiás)",
    page_icon="🐂",
    layout="wide",
)

st.title("🐂 Especialista em Nutrição Bovina & Carcaça (Grão Moído)")
st.caption(
    "Formulador profissional de rações concentradas à base de Milho/Sorgo Moído e Proteínas para Goiás."
)

# ---------------------------------------------------------
# 1. CLIMA EM TEMPO REAL (OPEN-METEO - SEM NECESSIDADE DE API KEY)
# ---------------------------------------------------------
st.sidebar.header("📍 Localização & Clima em Goiás")

municipios_go = {
    "Goiânia": {"lat": -16.6869, "lon": -49.2648},
    "Rio Verde": {"lat": -17.7924, "lon": -50.9189},
    "Jataí": {"lat": -17.8814, "lon": -51.7144},
    "Itumbiara": {"lat": -18.4194, "lon": -49.2158},
    "Cristalina": {"lat": -16.7686, "lon": -47.6136},
    "Porangatu": {"lat": -13.4414, "lon": -49.1486},
    "Anápolis": {"lat": -16.3267, "lon": -48.9528},
}

cidade_sel = st.sidebar.selectbox(
    "Selecione o Município:", list(municipios_go.keys())
)
coords = municipios_go[cidade_sel]


def buscar_clima(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m"
        r = requests.get(url, timeout=4)
        if r.status_code == 200:
            d = r.json()["current"]
            return d["temperature_2m"], d["relative_humidity_2m"]
    except Exception:
        pass
    return None, None


temp, umidade = buscar_clima(coords["lat"], coords["lon"])

if temp is not None:
    st.sidebar.metric(f"Temperatura ({cidade_sel})", f"{temp} °C")
    st.sidebar.metric("Umidade Relativa", f"{umidade}%")
    estacao_sugerida = "Águas (Chuva)" if umidade > 55 else "Seca / Transição"
    st.sidebar.info(f"Época Detectada: **{estacao_sugerida}**")
else:
    st.sidebar.warning("Buscando dados do clima...")
    estacao_sugerida = "Águas (Chuva)"

# ---------------------------------------------------------
# 2. CONFIGURAÇÃO DE CATEGORIA ANIMAL & PESO
# ---------------------------------------------------------
st.header("⚙️ Perfil do Rebanho e Categoria Animal")

col_cat, col_peso, col_qtd = st.columns(3)

with col_cat:
    categoria = st.selectbox(
        "Categoria Animal:",
        [
            "Bezerro / Bezerra (Mamando - Creep Feeding)",
            "Garrote / Novilha (Recria / Crescimento)",
            "Boi Magro (Engorda / Terminação)",
            "Vaca de Descarte / Matriz (Recuperação de Carcaça)",
        ],
    )

with col_peso:
    # Faixas de peso automáticas por categoria
    if "Bezerro" in categoria:
        peso_padrao = 160.0
    elif "Garrote" in categoria:
        peso_padrao = 320.0
    elif "Boi Magro" in categoria:
        peso_padrao = 450.0
    else:
        peso_padrao = 480.0

    peso_medio = st.number_input(
        "Peso Médio Atual (kg/cabeça):",
        min_value=50.0,
        max_value=900.0,
        value=peso_padrao,
        step=5.0,
    )

with col_qtd:
    quantidade_cabecas = st.number_input(
        "Número de Animais no Lote:",
        min_value=1,
        max_value=10000,
        value=100,
        step=10,
    )

st.divider()

# ---------------------------------------------------------
# 3. ESCOLHA DA DIETA COM GRÃO MOÍDO
# ---------------------------------------------------------
st.header("🥣 Formulação Nutricional à Base de Grão Moído")

# Seleção de dietas adequadas para a categoria
if "Bezerro" in categoria:
    opcoes_dieta = [
        "Creep-Feeding Inicial (Grão Moído + Soja 18% PB) - 0,5% PV",
        "Creep-Feeding Acelerado (Grão Moído + Soja 20% PB) - 1,0% PV",
    ]
elif "Garrote" in categoria:
    opcoes_dieta = [
        "Proteinado de Seca com Grão Moído e Ureia - 0,2% PV",
        "Proteinado Energético de Águas com Grão Moído - 0,3% PV",
        "Ração de Recria Intensiva a Pasto (Grão Moído) - 0,5% a 0,8% PV",
    ]
elif "Boi Magro" in categoria:
    opcoes_dieta = [
        "Proteinado de Seca para Terminação a Pasto - 0,3% PV",
        "Terminação Intensiva a Pasto (TIP Grão Moído) - 1,2% PV",
        "Confinamento Total com Grão Moído + Volumoso/Silagem - 1,8% PV",
    ]
else:
    opcoes_dieta = [
        "Proteinado para Recuperação de Vaca Magra - 0,3% PV",
        "Engorda Rápida de Vaca (TIP Grão Moído) - 1,2% PV",
    ]

estrategia = st.selectbox(
    "Selecione o Protocolo de Alimentação de Grão Moído:", opcoes_dieta
)

# ---------------------------------------------------------
# 4. ENGINE ZOOTÉCNICA DE CÁLCULO DE RAÇÃO
# ---------------------------------------------------------


def calcular_mistura_grao_moido(peso, qtd, est):
    # Definindo consumos e percentuais da mistura para 100 kg
    if "Creep-Feeding Inicial" in est:
        tx_consumo = 0.005  # 0.5% PV
        gmd = "0,750 a 0,950 kg/dia"
        mistura = {
            "Milho Moído Fino (ou Sorgo Moído)": 68.0,
            "Farelo de Soja 46%": 25.0,
            "Núcleo Mineral Creep-Feeding (com Virginiamicina)": 7.0,
        }
        obs = "Sem adição de Ureia. Ideal para desenvolvimento do rúmen do bezerro."

    elif "Creep-Feeding Acelerado" in est:
        tx_consumo = 0.010  # 1.0% PV
        gmd = "0,950 a 1,200 kg/dia"
        mistura = {
            "Milho Moído Fino": 60.0,
            "Farelo de Soja 46%": 32.0,
            "Núcleo Mineral/Vit. Creep": 8.0,
        }
        obs = "Acelera a desmama gerando bezerros pesados (acima de 210 kg)."

    elif "Proteinado de Seca" in est:
        tx_consumo = 0.002  # 0.2% PV
        gmd = "0,350 a 0,550 kg/dia"
        mistura = {
            "Milho Moído Fino (Energia)": 42.0,
            "Farelo de Soja (Proteína)": 28.0,
            "Ureia Pecuária + Sulfato de Amônio (9:1)": 8.0,
            "Sal Mineral / Núcleo Proteinado": 22.0,
        }
        obs = "Evita a perda de peso na seca e mantém o ganho contínuo no pasto."

    elif "Proteinado Energético de Águas" in est:
        tx_consumo = 0.003  # 0.3% PV
        gmd = "0,700 a 0,900 kg/dia"
        mistura = {
            "Milho Moído Fino": 68.0,
            "Farelo de Soja": 20.0,
            "Núcleo Mineral com Monensina Sódica": 12.0,
        }
        obs = "Aproveita o capim verde das águas com energia rápida do milho moído."

    elif "Recria Intensiva" in est:
        tx_consumo = 0.007  # 0.7% PV
        gmd = "0,900 a 1,150 kg/dia"
        mistura = {
            "Milho Moído Fino": 70.0,
            "Farelo de Soja": 22.0,
            "Núcleo Mineral/Aditivo com Tampão": 6.0,
            "Ureia + Sulfato de Amônio (9:1)": 2.0,
        }
        obs = "Encurta a recria para o garrote entrar magro e forte na terminação."

    elif "TIP Grão Moído" in est or "Engorda Rápida" in est:
        tx_consumo = 0.012  # 1.2% PV
        gmd = "1,350 a 1,750 kg/dia"
        mistura = {
            "Milho Moído Fino (Fubá/Xerém)": 72.0,
            "Farelo de Soja 46% (ou Algodão 38%)": 21.0,
            "Núcleo Confinamento/TIP (com Tampão/Bicarbonato e Virginiamicina)": 5.0,
            "Ureia Pecuária + Sulfato de Amônio (9:1)": 2.0,
        }
        obs = "Alta energia para depósito rápido de gordura e acabamento de carcaça no pasto."

    else:  # Confinamento Total com Volumoso
        tx_consumo = 0.018  # 1.8% PV (Concentrado)
        gmd = "1,500 a 1,900 kg/dia"
        mistura = {
            "Milho Moído Fino": 75.0,
            "Farelo de Soja": 18.0,
            "Núcleo Confinamento com Monensina + Virginiamicina": 5.0,
            "Ureia Pecuária + Sulfato de Amônio (9:1)": 2.0,
        }
        obs = "Acompanhar com 15% a 20% de volumoso (Silagem de milho ou bagaço de cana)."

    consumo_cabeca = peso * tx_consumo
    consumo_lote_dia = consumo_cabeca * qtd
    consumo_lote_mes = (consumo_lote_dia * 30) / 1000

    return consumo_cabeca, consumo_lote_dia, consumo_lote_mes, gmd, mistura, obs


c_cab, c_lote_d, c_lote_m, gmd_est, receita, observacao = (
    calcular_mistura_grao_moido(peso_medio, quantidade_cabecas, estrategia)
)

# Exibição de Métricas
c1, c2, c3 = st.columns(3)
c1.metric("Consumo Diário por Cabeça", f"{c_cab:.2f} kg/dia")
c2.metric("Consumo Diário Total do Lote", f"{c_lote_d:.1f} kg/dia")
c3.metric("Ganho Médio Diário Esperado (GMD)", gmd_est)

st.info(f"💡 **Diretriz Técnica:** {observacao}")

st.subheader("📋 Receita da Mistura (Proporção Exata para 100 kg de Ração)")

col_rec, col_dem = st.columns([1.3, 1])

with col_rec:
    for ingrediente, pct in receita.items():
        kg_dia_lote = (c_lote_d * pct) / 100
        st.write(
            f"• **{ingrediente}**: `{pct}%` — **{kg_dia_lote:.1f} kg/dia para o lote todo**"
        )

with col_dem:
    st.success(
        f"📦 **Demanda Mensal Estimada do Lote:** `{c_lote_m:.2f} Toneladas/mês`"
    )

st.divider()

# ---------------------------------------------------------
# 5. MANEJO TÉCNICO DE PASTAGEM EM GOIÁS
# ---------------------------------------------------------
st.header("🌱 Manejo de Pastagens para Suplementação com Grão Moído")

pasto_tipo = st.selectbox(
    "Selecione o Capim Predominante na Sua Área:",
    [
        "Brachiaria brizantha (Marandu / Braquiariao)",
        "Panicum maximum (Mombaça)",
        "Panicum maximum (Zuri)",
        "Panicum maximum (Quênia)",
        "Brachiaria decumbens",
    ],
)

tabela_pastos = {
    "Brachiaria brizantha (Marandu / Braquiariao)": {
        "entrada": "25 a 30 cm",
        "saida": "15 cm",
        "dica": "Ideal para recria e engorda. Evite passar de 35 cm para não talar e perder proteína.",
    },
    "Panicum maximum (Mombaça)": {
        "entrada": "85 a 90 cm",
        "saida": "40 a 50 cm",
        "dica": "Exige alta adubação nas águas. Não baixar de 40 cm no pastejo rotacionado.",
    },
    "Panicum maximum (Zuri)": {
        "entrada": "70 a 75 cm",
        "saida": "30 a 35 cm",
        "dica": "Excelente folhagem. Responde com altíssima conversão de carcaça com grão moído.",
    },
    "Panicum maximum (Quênia)": {
        "entrada": "60 a 70 cm",
        "saida": "30 cm",
        "dica": "Facilidade de manejo e alta digestibilidade para garrotes e novilhas.",
    },
    "Brachiaria decumbens": {
        "entrada": "20 a 25 cm",
        "saida": "10 a 12 cm",
        "dica": "Rústica e bem adaptada aos solos fracos do cerrado goiano.",
    },
}

p_info = tabela_pastos[pasto_tipo]

cp1, cp2, cp3 = st.columns(3)
cp1.metric("Altura de Entrada (Colocar gado)", p_info["entrada"])
cp2.metric("Altura de Saída (Tirar gado)", p_info["saida"])
cp3.info(f"📌 **Manejo:** {p_info['dica']}")

st.warning(
    "⚠️ **Protocolo Obrigatório de Adaptação de Ureia com Grão Moído:** Durante os primeiros 14 dias, forneça metade da dose da ração para evitar acidose ruminal e intoxicação por ureia no lote."
)
