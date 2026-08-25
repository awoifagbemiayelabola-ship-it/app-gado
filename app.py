import streamlit as st

# Configuração da página com ícone personalizado de Boi
st.set_page_config(
    page_title="BoiCria - Viabilidade, Ágio & Nutrição",
    page_icon="🐂",
    layout="wide"
)

st.title("🐂 BoiCria - Calculadora de Viabilidade, Ágio & Nutrição")
st.markdown("---")

# --- SEÇÃO 1: CATEGORIA E DADOS DE COMPRA ---
st.subheader("1. Categoria & Dados da Compra")

col_cat, col_price = st.columns(2)

with col_cat:
    categoria = st.selectbox(
        "Tipo / Categoria do Animal",
        ["Bezerro", "Garrote", "Novilha", "Boi Gordo"]
    )

# Definir parâmetros padrão baseados na categoria
if categoria == "Bezerro":
    peso_abate_padrao = 510.0
    rendimento_padrao = 50.0
    gmd_alvo_padrao = 1.0
    agio_teto_recomendado = 18.0 # % máximo recomendado para bezerro
elif categoria == "Garrote":
    peso_abate_padrao = 530.0
    rendimento_padrao = 52.0
    gmd_alvo_padrao = 1.1
    agio_teto_recomendado = 12.0 # % máximo recomendado para garrote
elif categoria == "Novilha":
    peso_abate_padrao = 450.0
    rendimento_padrao = 52.0
    gmd_alvo_padrao = 0.9
    agio_teto_recomendado = 15.0 # % máximo para novilha
else: # Boi Gordo
    peso_abate_padrao = 550.0
    rendimento_padrao = 54.0
    gmd_alvo_padrao = 1.2
    agio_teto_recomendado = 5.0

preco_compra = st.number_input("Preço de Compra do Animal (R$)", value=2500.0, step=50.0)
peso_atual = st.number_input("Peso Atual do Animal (kg)", value=190.0, step=5.0)
cotacao_arroba = st.number_input("Cotação Atual da @ do Boi Gordo (R$)", value=332.0, step=1.0)

rendimento = st.slider("Rendimento de Carcaça Estimado (%)", min_value=48.0, max_value=56.0, value=rendimento_padrao, step=0.5)

st.markdown("---")

# --- SEÇÃO 2: CÁLCULOS ZOOTÉCNICOS E FINANCEIROS ---
# Arrobas atuais do animal
arrobas_atuais = (peso_atual * (rendimento / 100)) / 15.0
valor_arroba_seca = arrobas_atuais * cotacao_arroba

# Cotação paga na @ magra
valor_arroba_paga = preco_compra / arrobas_atuais if arrobas_atuais > 0 else 0.0

# Cálculo do Ágio
diferenca_agio = preco_compra - valor_arroba_seca
percentual_agio = ((preco_compra - valor_arroba_seca) / valor_arroba_seca) * 100 if valor_arroba_seca > 0 else 0.0

# Preço justo recomendado (com teto de ágio seguro)
preco_justo = valor_arroba_seca * (1 + (agio_teto_recomendado / 100))

# --- SEÇÃO 3: ANÁLISE DETALHADA DO ÁGIO ---
st.subheader("2. Análise Profunda do Ágio")

col_a1, col_a2, col_a3 = st.columns(3)
col_a1.metric("Cotação da @ Paga no Animal Magro", f"R$ {valor_arroba_paga:.2f}")
col_a2.metric("Ágio em R$ (sobre a @ gorda)", f"R$ {diferenca_agio:.2f}")
col_a3.metric("Porcentagem de Ágio Paga", f"{percentual_agio:.1f}%")

if percentual_agio <= 0:
    st.success(f"💎 **COMPRA EXCELENTE (SEM ÁGIO)!** Você está pagando abaixo da cotação seca da arroba. O animal vale R$ {valor_arroba_seca:.2f} na arroba seca e você está pagando R$ {preco_compra:.2f}.")
elif percentual_agio <= agio_teto_recomendado:
    st.info(f"✅ **ÁGIO ACEITÁVEL E VIÁVEL.** Você está pagando {percentual_agio:.1f}% de ágio. Para a categoria **{categoria}**, um ágio de até {agio_teto_recomendado}% é considerado dentro da margem de segurança.")
else:
    st.error(f"⚠️ **ÁGIO ALTO / RISCO NA COMPRA!** Você está pagando {percentual_agio:.1f}% de ágio. O recomendado para **{categoria}** é pagar no máximo **{agio_teto_recomendado}%** de ágio.")

# Sugestão de Preço Justo
st.warning(f"💡 **Sugestão de Preço Justo / Negociação:** Tente negociar a compra deste {categoria} por **R$ {preco_justo:.2f}** (teto de {agio_teto_recomendado}% de ágio).")

st.markdown("---")

# --- SEÇÃO 4: METAS DE ENGORDA & RESULTADOS ---
st.subheader("3. Estimativa de Desempenho & Lucro")

peso_meta = peso_abate_padrao
ganho_necessario_kg = max(0.0, peso_meta - peso_atual)
dias_estimados = int(ganho_necessario_kg / gmd_alvo_padrao) if gmd_alvo_padrao > 0 else 0

# Estimativa de receita final
arrobas_finais = (peso_meta * (rendimento / 100)) / 15.0
receita_estimada = arrobas_finais * cotacao_arroba
lucro_bruto = receita_estimada - preco_compra

col1, col2, col3 = st.columns(3)
col1.metric("Arrobas Atuais", f"{arrobas_atuais:.2f} @")
col2.metric("Meta de Peso Abate", f"{peso_meta:.0f} kg ({arrobas_finais:.1f} @)")
col3.metric("Lucro Bruto Estimado", f"R$ {lucro_bruto:.2f}")

st.markdown("---")

# --- SEÇÃO 5: MANEJO NUTRICIONAL ---
st.subheader("4. Planejamento Nutricional & GMD Diário")

c_gmd, c_dias = st.columns(2)
c_gmd.metric("GMD Diário Alvo", f"{gmd_alvo_padrao:.2f} kg/dia")
c_dias.metric("Tempo de Permanência Estimado", f"{dias_estimados} dias")

consumo_materia_seca = peso_atual * 0.025 # 2.5% do peso vivo
racao_concentrado = peso_atual * 0.01 # 1% do peso vivo

st.info(f"""
* **Consumo Total Estimado:** ~{consumo_materia_seca:.1f} kg/dia por cabeça (Matéria Seca).
* **Ração Recomendada (1% PV):** ~{racao_concentrado:.2f} kg/dia por cabeça (com 18% a 22% de Proteína Bruta).
* **Estratégia:** Garantir ótimo consumo de pasto para diluir o custo do ágio ao longo dos {dias_estimados} dias.
""")
