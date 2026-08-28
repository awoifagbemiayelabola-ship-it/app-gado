import streamlit as st

# Configuração da página
st.set_page_config(page_title="Calculadora Pecuária - Viabilidade e Nutrição", page_icon="🐂", layout="wide")

# CSS personalizado para design moderno e profissional
st.markdown("""
<style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .stApp {
        background-color: #0f172a;
    }
    .metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .metric-title {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        color: #f8fafc;
        font-size: 1.6rem;
        font-weight: 700;
        margin-top: 4px;
    }
    .advice-card {
        background-color: #1e293b;
        border-left: 4px solid #10b981;
        border-radius: 8px;
        padding: 20px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho do App
st.title("🐂 Calculadora de Viabilidade Pecuária & Nutrição")
st.markdown("Simulador completo para análise de compra, recria, engorda e suplementação técnica de gado de corte.")

st.divider()

# --- FORMULÁRIO DE ENTRADA ---
st.subheader("📋 Parâmetros do Lote e Nutrição")

col1, col2, col3 = st.columns(3)

with col1:
    descricao = st.text_input("Descrição do Lote", value="Lote 24 Cabeças Nelore")
    qtd_animais = st.number_input("Quantidade de Animais (cabeças)", min_value=1, value=24, step=1)
    valor_aquisicao = st.number_input("Valor de Aquisição / Cabeça (R$)", min_value=0.0, value=2300.0, step=50.0)
    
    fase_producao = st.radio(
        "Fase de Produção",
        options=["Recria", "Engorda"],
        index=0,
        horizontal=True,
        help="Define a finalidade e a projeção do lote"
    )

with col2:
    peso_inicial = st.number_input("Peso Inicial / Cabeça (kg)", min_value=0.0, value=285.0, step=5.0)
    peso_final = st.number_input("Peso Final Esperado / Cabeça (kg)", min_value=0.0, value=540.0, step=5.0)
    gmd = st.number_input("GMD - Ganho Médio Diário (kg/dia)", min_value=0.01, value=0.75, step=0.05)
    
    dias_fase = st.number_input(
        f"Dias em {fase_producao} (Calculado ou Personalizado)",
        min_value=1,
        value=max(1, int((max(0.0, peso_final - peso_inicial)) / (gmd if gmd > 0 else 0.75))),
        step=5,
        help="Quantidade estimada de dias até atingir o peso final projetado"
    )

with col3:
    valor_pasto = st.number_input("Valor de Pasto / Mês por Cabeça (R$)", min_value=0.0, value=60.0, step=5.0)
    rendimento = st.number_input("Rendimento de Carcaça (%)", min_value=0.0, max_value=100.0, value=53.0, step=0.5)
    agio_manual = st.number_input("Valor do Ágio Esperado/Informado (%)", min_value=-100.0, max_value=200.0, value=-26.6, step=0.5, help="Diferença percentual estimada do preço da arroba da reposição vs boi gordo")
    cotacao_boi_gordo = st.number_input("Cotação Boi Gordo Venda (R$/@)", min_value=0.0, value=330.0, step=5.0)

# Opções de Suplementação solicitadas
opcoes_suplementacao = {
    "Proteínado 0,1%": {"consumo_pct": 0.1, "custo_kg": 3.20, "desc": "Suplemento mineral proteinado para período de águas/transição"},
    "Proteínado 0,2%": {"consumo_pct": 0.2, "custo_kg": 3.00, "desc": "Proteinado de seca ou manutenção em pastos de média qualidade"},
    "Proteico Energético 0,3%": {"consumo_pct": 0.3, "custo_kg": 2.80, "desc": "Aceleração de ganho em pasto com aporte de energia"},
    "Proteico Energético 0,4%": {"consumo_pct": 0.4, "custo_kg": 2.60, "desc": "Intensificação de recria/engorda no pasto"},
    "Proteico Energético 0,5%": {"consumo_pct": 0.5, "custo_kg": 2.50, "desc": "Transição para semi-confinamento / recria turbinada"},
    "Concentrado Engorda 1%": {"consumo_pct": 1.0, "custo_kg": 2.10, "desc": "Semi-confinamento tradicional (1% do PV em ração)"},
    "Concentrado Engorda 1,5%": {"consumo_pct": 1.5, "custo_kg": 1.95, "desc": "Semi-confinamento intensivo ou confinamento com volumoso"},
    "Concentrado Engorda 2%": {"consumo_pct": 2.0, "custo_kg": 1.85, "desc": "Confinamento sem volumoso / Ração Total Grao Inteiro"}
}

st.subheader("🌾 Suplementação Nutricional")
tipo_suplem = st.selectbox("Selecione o Tipo de Suplementação", options=list(opcoes_suplementacao.keys()), index=1)

info_suplem = opcoes_suplementacao[tipo_suplem]
peso_medio_lote = (peso_inicial + peso_final) / 2.0
consumo_diario_kg = peso_medio_lote * (info_suplem["consumo_pct"] / 100.0)

col_sup1, col_sup2 = st.columns(2)
with col_sup1:
    custo_kg_suplem = st.number_input(
        f"Custo do Kg do {tipo_suplem} (R$/kg)", 
        min_value=0.0, 
        value=info_suplem["custo_kg"], 
        step=0.10
    )
with col_sup2:
    st.info(f"💡 **Consumo Estimado:** ~{consumo_diario_kg:.2f} kg/cabeça/dia (Baseado no peso médio de {peso_medio_lote:.1f} kg).\n\n*{info_suplem['desc']}*")

st.divider()

# --- CÁLCULOS TÉCNICOS E FINANCEIROS ---

# 1. Arrobas na entrada (padrão 50% rendimento de bezerro/garrote)
rendimento_entrada = 0.50
arrobas_entrada_cabeca = (peso_inicial * rendimento_entrada) / 15.0
valor_arroba_entrada = (valor_aquisicao / arrobas_entrada_cabeca) if arrobas_entrada_cabeca > 0 else 0.0

# 2. Ágio Real Calculado vs Ágio Informado
agio_calculado = (((valor_arroba_entrada / cotacao_boi_gordo) - 1) * 100) if cotacao_boi_gordo > 0 else 0.0

# 3. Custos Operacionais
meses_fase = dias_fase / 30.0
custo_pasto_cabeca = meses_fase * valor_pasto
custo_pasto_total = custo_pasto_cabeca * qtd_animais

custo_suplem_diario_cabeca = consumo_diario_kg * custo_kg_suplem
custo_suplem_cabeca_total_fase = custo_suplem_diario_cabeca * dias_fase
custo_suplem_total_lote = custo_suplem_cabeca_total_fase * qtd_animais

custo_nutricao_manejo_cabeca = custo_pasto_cabeca + custo_suplem_cabeca_total_fase
custo_nutricao_manejo_total = custo_nutricao_manejo_cabeca * qtd_animais

# 4. Faturamento na Saída
arrobas_saida_cabeca = (peso_final * (rendimento / 100.0)) / 15.0
faturamento_cabeca = arrobas_saida_cabeca * cotacao_boi_gordo
faturamento_total = faturamento_cabeca * qtd_animais

# 5. Totais do Lote e Rentabilidade
investimento_compra_total = valor_aquisicao * qtd_animais
custo_total_acumulado = investimento_compra_total + custo_nutricao_manejo_total

lucro_total = faturamento_total - custo_total_acumulado
lucro_cabeca = lucro_total / qtd_animais
roi = ((lucro_total / custo_total_acumulado) * 100) if custo_total_acumulado > 0 else 0.0
lucro_mensal_cabeca = lucro_cabeca / (meses_fase if meses_fase > 0 else 1)

# --- EXIBIÇÃO DOS RESULTADOS ---
st.subheader(f"📊 Resultados e DRE do Lote: {descricao}")
st.caption(f"Fase: **{fase_producao}** | Duração: **{dias_fase} dias** (~{meses_fase:.1f} meses) | Ganho Diário: **{gmd:.2f} kg/dia**")

# Grid de Indicadores Principais
m1, m2, m3, m4, m5 = st.columns(5)

with m1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Ágio Real (Compra)</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value" style="color: {"#10b981" if agio_calculado <= 0 else "#f59e0b"};">{agio_calculado:.1f}%</div>', unsafe_allow_html=True)
    st.markdown(f'<span style="font-size:0.75rem; color:#64748b;">Informado: {agio_manual:.1f}%</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with m2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Custo / @ Entrada</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">R$ {valor_arroba_entrada:.2f}</div>', unsafe_allow_html=True)
    st.markdown(f'<span style="font-size:0.75rem; color:#64748b;">{arrobas_entrada_cabeca:.2f} @ / cab</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with m3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">R$ / @ Saída Esperada</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">R$ {cotacao_boi_gordo:.2f}</div>', unsafe_allow_html=True)
    st.markdown(f'<span style="font-size:0.75rem; color:#64748b;">{arrobas_saida_cabeca:.2f} @ / cab</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with m4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Custo Alimentação / Cab</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">R$ {custo_nutricao_manejo_cabeca:.2f}</div>', unsafe_allow_html=True)
    st.markdown(f'<span style="font-size:0.75rem; color:#64748b;">Pasto + Suplemento</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with m5:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Lucro Líquido / Cab</div>', unsafe_allow_html=True)
    color_lucro = "#10b981" if lucro_cabeca > 0 else "#ef4444"
    st.markdown(f'<div class="metric-value" style="color: {color_lucro};">R$ {lucro_cabeca:,.2f}</div>', unsafe_allow_html=True)
    st.markdown(f'<span style="font-size:0.75rem; color:#64748b;">ROI: {roi:.1f}%</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# Status Visual de Viabilidade
if lucro_total > 0:
    st.success(f"🎉 **NEGÓCIO LUCRATIVO E RECOMENDADO!** O lote apresenta faturamento de **R$ {faturamento_total:,.2f}** e **LUCRO LÍQUIDO TOTAL de R$ {lucro_total:,.2f}** (ROI de **{roi:.1f}%**).")
else:
    st.error(f"🚨 **ALERTA DE PREJUÍZO!** O projeto nas condições atuais gera **PREJUÍZO LÍQUIDO DE R$ {abs(lucro_total):,.2f}** (-R$ {abs(lucro_cabeca):,.2f} por cabeça).")

# Resumo Detalhado em Tabela
with st.expander("📑 Detalhamento Completo do Balanço Financeiro", expanded=True):
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown("### 📥 Custos de Entrada e Nutrição")
        st.write(f"- **Investimento Inicial em Animais ({qtd_animais} cab):** R$ {investimento_compra_total:,.2f}")
        st.write(f"- **Custo Total de Pastagem ({dias_fase} dias):** R$ {custo_pasto_total:,.2f}")
        st.write(f"- **Custo de Suplementação ({tipo_suplem}):** R$ {custo_suplem_total_lote:,.2f}")
        st.write(f"- **CUSTO TOTAL ACUMULADO:** **R$ {custo_total_acumulado:,.2f}**")
    with col_d2:
        st.markdown("### 📤 Faturamento e Resultados")
        st.write(f"- **Faturamento Bruto Projetado:** R$ {faturamento_total:,.2f}")
        st.write(f"- **Lucro Por Cabeça:** R$ {lucro_cabeca:,.2f}")
        st.write(f"- **Lucro Estimado por Mês/Cabeça:** R$ {lucro_mensal_cabeca:,.2f}")
        st.write(f"- **Retorno sobre o Investimento (ROI):** **{roi:.1f}%**")

st.divider()

# --- PAINEL DE CONSELHOS TÉCNICOS E DECISÃO DE COMPRA ---
st.subheader("💡 Conselhos Técnicos e Veredito Final")

with st.container():
    if lucro_total > 0:
        if agio_calculado < -15:
            st.markdown(f"""
            <div class="advice-card" style="border-left-color: #10b981;">
                <h4 style="color: #10b981; margin-top:0;">🏆 EXCELENTE OPORTUNIDADE DE COMPRA!</h4>
                <p><strong>1. Ágio Altamente Favorável:</strong> A arroba de compra (R$ {valor_arroba_entrada:.2f}/@) está com <strong>{abs(agio_calculado):.1f}% de DESCONTO</strong> em relação ao boi gordo (R$ {cotacao_boi_gordo:.2f}/@). Essa é uma margem de segurança excepcional raramente vista no mercado.</p>
                <p><strong>2. Manejo Nutricional ({tipo_suplem}):</strong> A suplementação com {tipo_suplem} no nível de {info_suplem['consumo_pct']}% PV é plenamente viável para sustentar o GMD de {gmd:.2f} kg/dia nesta fase de {fase_producao}.</p>
                <p><strong>3. Recomendação Técnica:</strong> Garantir a conferência de peso em balança e a verificação sanitária/estutura sanitária do lote na fazenda de origem. O negócio tem excelente viabilidade financeira.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="advice-card" style="border-left-color: #3b82f6;">
                <h4 style="color: #3b82f6; margin-top:0;">👍 NEGÓCIO VIÁVEL E COMPENSATÓRIO</h4>
                <p><strong>1. Viabilidade Confirmada:</strong> O lote gera um lucro de R$ {lucro_cabeca:,.2f} por animal em {dias_fase} dias de {fase_producao}.</p>
                <p><strong>2. Atenção ao GMD:</strong> Como o ágio está em {agio_calculado:.1f}%, a lucratividade depende fundamentalmente de manter a meta de ganho de peso ({gmd:.2f} kg/dia) com a dieta de {tipo_suplem}.</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="advice-card" style="border-left-color: #ef4444;">
            <h4 style="color: #ef4444; margin-top:0;">⚠️ NÃO COMPENSA NAS CONDIÇÕES ATUAIS</h4>
            <p><strong>1. Ponto de Estrangulamento:</strong> O custo total por cabeça (R$ {custo_total_acumulado/qtd_animais:,.2f}) supera o faturamento final (R$ {faturamento_cabeca:,.2f}).</p>
            <p><strong>2. Como Reverter o Negócio:</strong></p>
            <ul>
                <li><strong>Reduzir Custo de Compra:</strong> Negocie o valor inicial por cabeça para até R$ {(faturamento_cabeca - custo_nutricao_manejo_cabeca) * 0.9:,.2f}.</li>
                <li><strong>Aumentar Desempenho (GMD):</strong> Ajuste a dieta para buscar ganhos superiores a {gmd:.2f} kg/dia para diminuir os {dias_fase} dias de permanência.</li>
                <li><strong>Reavaliar a Suplementação:</strong> Alterne o tipo de alimento para otimizar o custo por kg ganho.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
