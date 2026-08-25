import streamlit as st

# Título do App
st.title("🐄 BoiCerto - Calculadora de Viabilidade & Nutrição")

st.markdown("---")

# --- SEÇÃO 1: ENTRADAS DE DADOS ---
st.subheader("1. Dados da Compra")
col1, col2 = st.columns(2)

with col1:
    preco_compra = st.number_input("Preço de Compra do Animal (R$)", min_value=100.0, value=2500.0, step=50.0)
    peso_kg = st.number_input("Peso Atual do Animal (kg)", min_value=50.0, value=330.0, step=5.0)

with col2:
    # Em uma versão final, este valor vem via API automática (ex: CEPEA)
    cotacao_arroba = st.number_input("Cotação Atual da @ (R$ / Internet)", min_value=100.0, value=240.0, step=1.0)
    rendimento_carcaca = st.slider("Rendimento de Carcaça Estimado (%)", 48, 56, 52) / 100

# --- SEÇÃO 2: CÁLCULOS ZOOTÉCNICOS E FINANCEIROS ---
peso_arrobas = (peso_kg * rendimento_carcaca) / 15
custo_por_arroba_comprada = preco_compra / peso_arrobas if peso_arrobas > 0 else 0

# Meta padrão de abate: 20 @
peso_alvo_arrobas = 20.0
peso_alvo_kg = (peso_alvo_arrobas * 15) / rendimento_carcaca
ganho_necessario_kg = peso_alvo_kg - peso_kg

# Lógica de Recomendação de Dieta & GMD
if peso_kg < 300:
    fase = "Recria"
    gmd_alvo = 0.700  # 700g/dia
    dieta = "Pasto adubado + Suplementação Proteica (0,3% a 0,5% do PV)"
    custo_diario_estimado = 3.50
elif 300 <= peso_kg < 420:
    fase = "Engorda Inicial"
    gmd_alvo = 1.100  # 1,1 kg/dia
    dieta = "Semiconfinamento (Pasto + Ração a 1% do PV)"
    custo_diario_estimado = 7.50
else:
    fase = "Terminação"
    gmd_alvo = 1.500  # 1,5 kg/dia
    dieta = "Confinamento (Dieta de alto grão / Ração a 2% do PV)"
    custo_diario_estimado = 12.00

dias_ate_abate = int(ganho_necessario_kg / gmd_alvo) if gmd_alvo > 0 else 0
custo_total_nutricao = dias_ate_abate * custo_diario_estimado
valor_venda_estimado = peso_alvo_arrobas * cotacao_arroba
lucro_estimado = valor_venda_estimado - (preco_compra + custo_total_nutricao)

# --- SEÇÃO 3: RESULTADOS E DIAGNÓSTICO ---
st.markdown("---")
st.subheader("2. Análise de Viabilidade e Estratégia")

# Veredito de Compra
if lucro_estimado > 200:
    st.success(f"✅ **VALE A PENA A COMPRA!** Lucro estimado de R$ {lucro_estimado:.2f} por cabeça.")
elif lucro_estimado > 0:
    st.warning(f"⚠️ **COMPRA DE RISCO (Margem Apertada):** Lucro estimado de apenas R$ {lucro_estimado:.2f} por cabeça.")
else:
    st.error(f"❌ **NÃO COMPENSA A COMPRA!** Prejuízo estimado de R$ {abs(lucro_estimado):.2f} por cabeça.")

# Indicadores Rápidos
col_a, col_b, col_c = st.columns(3)
col_a.metric("Peso Atual (@)", f"{peso_arrobas:.2f} @")
col_b.metric("Custo da @ Comprada", f"R$ {custo_por_arroba_comprada:.2f}")
col_c.metric("Tempo para Abate (20@)", f"{dias_ate_abate} dias (~{int(dias_ate_abate/30)} meses)")

# Recomendações
st.markdown(f"""
> **📋 Planejamento Nutricional Sugerido ({fase}):**
> * **Dieta Recomendada:** {dieta}
> * **GMD Meta:** {gmd_alvo:.3f} kg/dia
> * **Ponto Otimizado de Abate/Revenda:** Vender idealmente com **{peso_alvo_arrobas:.0f} @** ({peso_alvo_kg:.0f} kg vivo). A partir desse peso, a conversão alimentar cai e o custo de manutenção aumenta.
""")
