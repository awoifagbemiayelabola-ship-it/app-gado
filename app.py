import streamlit as st

# Configuração da página
st.set_page_config(page_title="Calculadora de Gado", page_icon="🐮", layout="wide")

st.title("🐮 Calculadora de Viabilidade de Gado")
st.markdown("Simulador de lucratividade para recria e engorda.")

st.divider()

# Formulário de Entradas
st.subheader("📝 Dados do Lote")

col1, col2, col3 = st.columns(3)

with col1:
    descricao = st.text_input("Descrição do Lote", value="Lote 24 Cabeças Nelore")
    qtd_animais = st.number_input("Quantidade de Animais (cabeças)", min_value=1, value=24, step=1)
    valor_aquisicao = st.number_input("Valor de Aquisição / Cabeça (R$)", min_value=0.0, value=2300.0, step=50.0)

with col2:
    peso_inicial = st.number_input("Peso Inicial / Cabeça (kg)", min_value=0.0, value=285.0, step=5.0)
    peso_final = st.number_input("Peso Final Esperado / Cabeça (kg)", min_value=0.0, value=540.0, step=5.0)
    gmd = st.number_input("GMD - Ganho Médio Diário (kg)", min_value=0.01, value=0.75, step=0.05)

with col3:
    valor_pasto = st.number_input("Custo Pasto/Mês por Cabeça (R$)", min_value=0.0, value=60.0, step=5.0)
    rendimento = st.number_input("Rendimento de Carcaça (%)", min_value=0.0, max_value=100.0, value=53.0, step=0.5)
    cotacao_boi_gordo = st.number_input("Cotação Boi Gordo Venda (R$/@)", min_value=0.0, value=330.0, step=5.0)

st.divider()

# --- CÁLCULOS ---
# 1. Arrobas na entrada (padrão 50% carcaça para bezerro/garrote)
arrobas_entrada_cabeca = (peso_inicial * 0.50) / 15.0
valor_arroba_entrada = (valor_aquisicao / arrobas_entrada_cabeca) if arrobas_entrada_cabeca > 0 else 0.0

# 2. Ágio (%)
agio = (((valor_arroba_entrada / cotacao_boi_gordo) - 1) * 100) if cotacao_boi_gordo > 0 else 0.0

# 3. Permanência e Pasto
ganho_peso = max(0.0, peso_final - peso_inicial)
dias_permanencia = int(ganho_peso / gmd) if gmd > 0 else 0
meses_permanencia = dias_permanencia / 30.0
custo_pasto_cabeca = meses_permanencia * valor_pasto
custo_pasto_total = custo_pasto_cabeca * qtd_animais

# 4. Faturamento na Saída
arrobas_saida_cabeca = (peso_final * (rendimento / 100.0)) / 15.0
faturamento_cabeca = arrobas_saida_cabeca * cotacao_boi_gordo
faturamento_total = faturamento_cabeca * qtd_animais

# 5. Totais e Margem
investimento_compra = valor_aquisicao * qtd_animais
custo_total_lote = investimento_compra + custo_pasto_total
lucro_total = faturamento_total - custo_total_lote
lucro_cabeca = lucro_total / qtd_animais
roi = ((lucro_total / custo_total_lote) * 100) if custo_total_lote > 0 else 0.0

# --- RESULTADOS ---
st.subheader(f"📊 Resultados: {descricao}")
st.caption(f"Tempo estimado de permanência: **{dias_permanencia} dias** (~{meses_permanencia:.1f} meses)")

# Métricas Principais
m1, m2, m3, m4 = st.columns(4)

m1.metric(
    label="Ágio na Compra", 
    value=f"{agio:.1f}%", 
    delta="Desconto (Bom)" if agio <= 0 else "Ágio Positivo",
    delta_color="normal" if agio <= 0 else "inverse"
)

m2.metric(
    label="R$ / @ Entrada", 
    value=f"R$ {valor_arroba_entrada:.2f}",
    help=f"Arrobas por cabeça na entrada: {arrobas_entrada_cabeca:.2f} @"
)

m3.metric(
    label="R$ / @ Saída Esperada", 
    value=f"R$ {cotacao_boi_gordo:.2f}",
    help=f"Arrobas por cabeça na saída: {arrobas_saida_cabeca:.2f} @"
)

m4.metric(
    label="Lucro Total Previsto", 
    value=f"R$ {lucro_total:,.2f}",
    delta=f"R$ {lucro_cabeca:,.2f} / cab"
)

# Veredito Visual
if lucro_total > 0:
    st.success(f"✅ **BOM NEGÓCIO!** O lote apresenta previsão de **LUCRO** com Retorno sobre Investimento (ROI) de **{roi:.1f}%**.")
else:
    st.error(f"⚠️ **ATENÇÃO!** Nas condições preenchidas, o lote apresenta previsão de **PREJUÍZO**.")

# Resumo Detalhado
with st.expander("🔎 Ver Resumo Financeiro Completo"):
    st.write(f"- **Investimento Inicial em Animais:** R$ {investimento_compra:,.2f}")
    st.write(f"- **Custo Total de Pasto ({dias_permanencia} dias):** R$ {custo_pasto_total:,.2f}")
    st.write(f"- **Custo Total Acumulado (Entrada + Pasto):** R$ {custo_total_lote:,.2f}")
    st.write(f"- **Faturamento Bruto Previsto:** R$ {faturamento_total:,.2f}")
    st.write(f"- **Lucro Líquido Final:** R$ {lucro_total:,.2f}")
