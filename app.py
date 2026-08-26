import streamlit as st
import requests

# Configuração da página
st.set_page_config(page_title="Calculadora Pecuária - Ágio & Viabilidade", page_icon="🐂", layout="centered")

# --- BUSCA DA COTAÇÃO AUTOMÁTICA DA @ DO BOI GORDO ---
@st.cache_data(ttl=3600)  # Atualiza a cotação a cada 1 hora
def obter_cotacao_boi():
    try:
        # Tenta buscar via API AgroDoc / CEPEA
        response = requests.get("https://agrodocai.com.br/api/cotacao/boi", timeout=5)
        if response.status_code == 200:
            dados = response.json()
            return float(dados.get("preco", 340.00))
    except Exception:
        pass
    # Valor padrão de fallback caso a API falhe
    return 340.00 

cotacao_boi_hoje = obter_cotacao_boi()

# --- INTERFACE DO APLICATIVO ---
st.title("🐂 Calculadora Pecuária de Ágio e Viabilidade")
st.markdown("Avalie a compra de animais, ágio sobre a arroba e viabilidade do investimento.")

st.sidebar.header("📊 Cotação de Referência")
preco_boi_gordo = st.sidebar.number_input(
    "Cotação do Boi Gordo HOJE (R$/@):", 
    value=cotacao_boi_hoje, 
    step=1.00,
    help="Atualizado automaticamente do mercado. Você pode alterar se necessário."
)
st.sidebar.caption("💡 Atualizado automaticamente com mercado físico/CEPEA.")

st.divider()

# --- ENTRADA DE DADOS PELO USUÁRIO ---
st.subheader("1. Identificação e Dados da Compra")

col1, col2 = st.columns(2)

with col1:
    tipo_animal = st.text_input("Tipo de Animal (ex: Bezerro, Garrote, Novilha):", value="Bezerro Nelore")
    sistema = st.selectbox("Sistema de Destino:", ["Recria", "Confinamento"])
    peso_kg = st.number_input("Peso do Animal (em kg):", min_value=1.0, value=200.0, step=5.0)

with col2:
    rendimento_carcaca = st.number_input("Rendimento de Carcaça estimado (%):", min_value=40.0, max_value=65.0, value=50.0, step=0.5)
    preco_total_cabeca = st.number_input("Valor Pago por Cabeça (R$):", min_value=1.0, value=2800.0, step=50.0)

# --- CÁLCULOS MATEMÁTICOS ---
# Arrobas brutas do animal (relação peso vivo / 30)
arrobas_vivas = peso_kg / 30.0

# Arrobas de carcaça (considerando o rendimento)
arrobas_carcaca = (peso_kg * (rendimento_carcaca / 100)) / 15.0

# Valor pago por @ comprada
preco_pago_por_arroba = preco_total_cabeca / arrobas_carcaca

# Cálculo do Ágio
agio_reais = preco_pago_por_arroba - preco_boi_gordo
agio_percentual = ((preco_pago_por_arroba / preco_boi_gordo) - 1) * 100

st.divider()

# --- RESULTADOS DO ÁGIO ---
st.subheader("2. Análise do Ágio Pago")

c1, c2, c3 = st.columns(3)
c1.metric("Arrobas (@ Carcaça)", f"{arrobas_carcaca:.2f} @")
c2.metric("Valor Pago por @", f"R$ {preco_pago_por_arroba:.2f}")
c3.metric("Ágio da @", f"{agio_percentual:.1f}%", delta=f"R$ {agio_reais:.2f}/@", delta_color="inverse")

# --- ANÁLISE DE VIABILIDADE ---
st.subheader(f"3. Viabilidade para {sistema}")

if sistema == "Recria":
    ganho_peso_esperado = st.number_input("Ganho de peso estimado até a venda (em kg):", value=180.0, step=10.0)
    custo_mes_cabeca = st.number_input("Custo de Pastagem/Manejo por mês (R$/cabeça):", value=60.0, step=5.0)
    meses_recria = st.number_input("Tempo de Recria (meses):", value=10, step=1)
    
    # Cálculos Recria
    custo_total_manejo = custo_mes_cabeca * meses_recria
    peso_final_kg = peso_kg + ganho_peso_esperado
    arrobas_finais = (peso_final_kg * (rendimento_carcaca / 100)) / 15.0
    
    receita_estimada = arrobas_finais * preco_boi_gordo
    custo_total = preco_total_cabeca + custo_total_manejo
    lucro_estimado = receita_estimada - custo_total
    margem = (lucro_estimado / custo_total) * 100

elif sistema == "Confinamento":
    dias_confinamento = st.number_input("Dias de Cocho:", value=90, step=5)
    ganho_diario_kg = st.number_input("Ganho de Peso Diário (kg/dia):", value=1.5, step=0.1)
    custo_diaria_cocho = st.number_input("Custo da Diária do Cocho (R$/dia):", value=14.0, step=0.5)
    
    # Cálculos Confinamento
    ganho_peso_esperado = ganho_diario_kg * dias_confinamento
    custo_total_manejo = custo_diaria_cocho * dias_confinamento
    peso_final_kg = peso_kg + ganho_peso_esperado
    
    # No confinamento o rendimento costuma subir
    rendimento_final = rendimento_carcaca + 4.0 if rendimento_carcaca <= 52.0 else rendimento_carcaca
    arrobas_finais = (peso_final_kg * (rendimento_final / 100)) / 15.0
    
    receita_estimada = arrobas_finais * preco_boi_gordo
    custo_total = preco_total_cabeca + custo_total_manejo
    lucro_estimado = receita_estimada - custo_total
    margem = (lucro_estimado / custo_total) * 100

# --- PARECER FINAL ---
st.markdown("### 📋 Diagnóstico da Operação")

if lucro_estimado > 0:
    st.success(f"""
    **COMPENSA A COMPRA!** ✅  
    * **Investimento Total:** R$ {custo_total:,.2f}  
    * **Faturamento Estimado na Venda:** R$ {receita_estimada:,.2f}  
    * **Lucro Estimado por Cabeça:** **R$ {lucro_estimado:,.2f}** (Margem de **{margem:.1f}%**)
    """)
else:
    st.error(f"""
    **NÃO COMPENSA (Risco de Prejuízo)** ⚠️  
    * **Investimento Total:** R$ {custo_total:,.2f}  
    * **Faturamento Estimado na Venda:** R$ {receita_estimada:,.2f}  
    * **Prejuízo Estimado por Cabeça:** **R$ {lucro_estimado:,.2f}** (Margem de **{margem:.1f}%**)  
    * *Dica:* O ágio pago de **{agio_percentual:.1f}%** está muito alto para a margem de ganho informada.
    """)

