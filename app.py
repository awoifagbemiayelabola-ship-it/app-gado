import streamlit as st

# Configuração da página com ícone personalizado de Boi
st.set_page_config(
    page_title="BoiCria - Viabilidade & Nutrição",
    page_icon="🐂",
    layout="wide"
)

st.title("🐂 BoiCria - Calculadora de Viabilidade & Nutrição")
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
elif categoria == "Garrote":
    peso_abate_padrao = 530.0
    rendimento_padrao = 52.0
    gmd_alvo_padrao = 1.1
elif categoria == "Novilha":
    peso_abate_padrao = 450.0
    rendimento_padrao = 52.0
    gmd_alvo_padrao = 0.9
else: # Boi Gordo
    peso_abate_padrao = 550.0
    rendimento_padrao = 54.0
    gmd_alvo_padrao = 1.2

preco_compra = st.number_input("Preço de Compra do Animal (R$)", value=2500.0, step=50.0)
peso_atual = st.number_input("Peso Atual do Animal (kg)", value=190.0, step=5.0)
cotacao_arroba = st.number_input("Cotação Atual da @ (R$)", value=332.0, step=1.0)

rendimento = st.slider("Rendimento de Carcaça Estimado (%)", min_value=48.0, max_value=56.0, value=rendimento_padrao, step=0.5)

st.markdown("---")

# --- SEÇÃO 2: CÁLCULOS TÉCNICOS ---
# Arrobas atuais do animal
arrobas_atuais = (peso_atual * (rendimento / 100)) / 15.0
valor_real_animal = arrobas_atuais * cotacao_arroba
diferenca_compra = valor_real_animal - preco_compra

# Metas de engorda
peso_meta = peso_abate_padrao
ganho_necessario_kg = max(0.0, peso_meta - peso_atual)
dias_estimados = int(ganho_necessario_kg / gmd_alvo_padrao) if gmd_alvo_padrao > 0 else 0

# Estimativa de receita final
arrobas_finais = (peso_meta * (rendimento / 100)) / 15.0
receita_estimada = arrobas_finais * cotacao_arroba
lucro_bruto = receita_estimada - preco_compra

# --- SEÇÃO 3: RESULTADOS E VEREDITO ---
st.subheader("2. Análise de Viabilidade & Lucro")

if diferenca_compra >= 0:
    st.success(f"✅ **VALE A PENA COMPRAR!** O animal vale R$ {valor_real_animal:.2f} na @ atual e está custando R$ {preco_compra:.2f} (Economia/Folga inicial de R$ {diferenca_compra:.2f}).")
else:
    st.warning(f"⚠️ **COMPRA COM ÁGIO:** O valor comercial em @ é R$ {valor_real_animal:.2f}. Você está pagando R$ {abs(diferenca_compra):.2f} acima da cotação seca. Requer boa estratégia nutricional para lucrar.")

col1, col2, col3 = st.columns(3)
col1.metric("Arrobas Atuais", f"{arrobas_atuais:.2f} @")
col2.metric("Meta de Peso Abate", f"{peso_meta:.0f} kg")
col3.metric("Lucro Bruto Estimado", f"R$ {lucro_bruto:.2f}")

st.markdown("---")

# --- SEÇÃO 4: META DE GMD E ESTRATÉGIA NUTRICIONAL ---
st.subheader("3. Planejamento Nutricional & GMD Diário")

c_gmd, c_dias = st.columns(2)
c_gmd.metric("GMD Diário Recomendado", f"{gmd_alvo_padrao:.2f} kg/dia")
c_dias.metric("Tempo de Manejo Estimado", f"{dias_estimados} dias")

st.markdown("### 🌾 Manejo de Pasto + Ração Recomendado")

# Cálculo simplificado de consumo nutricional
consumo_materia_seca = peso_atual * 0.025 # 2.5% do peso vivo
racao_concentrado = peso_atual * 0.01 # 1% do peso vivo para ganho rápido
pasto_estimado = consumo_materia_seca - racao_concentrado

st.info(f"""
* **Consumo Total (Matéria Seca):** ~{consumo_materia_seca:.1f} kg/dia por cabeça (aprox. 2.5% do Peso Vivo).
* **Ração/Concentrado (Rendimento Rápido):** ~{racao_concentrado:.2f} kg/dia por cabeça (1.0% do Peso Vivo de ração com 18% a 22% de Proteína Bruta).
* **Entrada de Pasto:** Garantir folha verde à vontade (altura de manejo ideal para capim Br pasture/Mombaça).
* **Dica de Ouro:** Para bater a meta de **{gmd_alvo_padrao:.2f} kg/dia**, mantenha cocho coberto e água limpa à vontade.
""")
