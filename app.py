from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class RacaInfo:
    nome: str
    peso_recria_ideal: float       # kg
    gmd_recria_alvo: float         # kg/dia
    peso_confinamento_ideal: float # kg
    gmd_confinamento_alvo: float   # kg/dia
    suporta_recria: bool = True

# 1. BASE DE DADOS DAS RAÇAS
BANCO_RACAS: Dict[str, RacaInfo] = {
    "nelore": RacaInfo(
        nome="Nelore",
        peso_recria_ideal=400.0,
        gmd_recria_alvo=0.700,
        peso_confinamento_ideal=550.0,
        gmd_confinamento_alvo=1.600
    ),
    "angus_f1": RacaInfo(
        nome="Angus x Nelore (F1)",
        peso_recria_ideal=420.0,
        gmd_recria_alvo=0.900,
        peso_confinamento_ideal=590.0,
        gmd_confinamento_alvo=1.850
    ),
    "guzera": RacaInfo(
        nome="Guzerá / Tabapuã",
        peso_recria_ideal=395.0,
        gmd_recria_alvo=0.680,
        peso_confinamento_ideal=545.0,
        gmd_confinamento_alvo=1.500
    ),
    "brangus": RacaInfo(
        nome="Braford / Brangus",
        peso_recria_ideal=410.0,
        gmd_recria_alvo=0.850,
        peso_confinamento_ideal=580.0,
        gmd_confinamento_alvo=1.750
    ),
    "holandes": RacaInfo(
        nome="Holandês / Cruzamento Lácteo",
        peso_recria_ideal=0.0,
        gmd_recria_alvo=0.0,
        peso_confinamento_ideal=530.0,
        gmd_confinamento_alvo=1.300,
        suporta_recria=False
    )
}

# 2. FUNÇÕES DE CÁLCULO DA REGRA DE NEGÓCIO

def calcular_agio(preco_compra_arroba: float, preco_venda_arroba: float) -> dict:
    """Calcula a porcentagem de ágio e avalia o risco."""
    agio_pct = ((preco_compra_arroba - preco_venda_arroba) / preco_venda_arroba) * 100
    
    if agio_pct <= 10.0:
        status = "EXCELENTE"
        mensagem = "Ágio baixo. Alta viabilidade financeira para o ganho de peso."
    elif 10.0 < agio_pct <= 20.0:
        status = "ATENÇÃO"
        mensagem = "Ágio moderado. Monitorar rigorosamente o custo da diária alimentar."
    else:
        status = "ALTO RISCO"
        mensagem = "Ágio elevado! O custo do GMD precisará ser muito baixo para cobrir o valor de compra."
        
    return {
        "agio_porcentagem": round(agio_pct, 2),
        "status": status,
        "mensagem": mensagem
    }

def simular_recria(raca: RacaInfo, peso_inicial: float, custo_diaria: float = 4.50) -> dict:
    """Calcula indicadores para a fase de recria."""
    if not raca.suporta_recria:
        return {"erro": f"A raça {raca.nome} não é recomendada para sistema de recria a pasto."}
    
    if peso_inicial >= raca.peso_recria_ideal:
        return {"erro": "Peso inicial já atingiu ou superou o peso ideal de revenda da recria."}
        
    ganho_necessario = raca.peso_recria_ideal - peso_inicial
    dias_recria = int(ganho_necessario / raca.gmd_recria_alvo)
    custo_total_fase = dias_recria * custo_diaria
    
    return {
        "peso_final_ideal_kg": raca.peso_recria_ideal,
        "peso_final_ideal_arrobas": round(raca.peso_recria_ideal / 30, 2), # Considera 50% rendimento base para recria
        "gmd_alvo_kg_dia": raca.gmd_recria_alvo,
        "dias_estimados": dias_recria,
        "custo_diario_estimado_rs": custo_diaria,
        "custo_total_alimentar_rs": round(custo_total_fase, 2),
        "alimentacao_recomendada": "Pastagem de boa qualidade + Suplementação Proteica (0,1% a 0,3% do PV) na seca ou Mineral Adensado nas águas."
    }

def simular_confinamento(raca: RacaInfo, peso_inicial: float, custo_diaria: float = 14.00) -> dict:
    """Calcula indicadores para a fase de confinamento total."""
    if peso_inicial >= raca.peso_confinamento_ideal:
        return {"erro": "Peso inicial já atingiu o peso ideal de abate para esta raça."}
        
    ganho_necessario = raca.peso_confinamento_ideal - peso_inicial
    dias_confinamento = int(ganho_necessario / raca.gmd_confinamento_alvo)
    custo_total_fase = dias_confinamento * custo_diaria
    
    # Rendimento padrão de carcaça em confinamento = ~54%
    arrobas_carcaca = (raca.peso_confinamento_ideal * 0.54) / 15
    
    return {
        "peso_final_abate_kg": raca.peso_confinamento_ideal,
        "arrobas_carcaca_estimadas": round(arrobas_carcaca, 2),
        "gmd_alvo_kg_dia": raca.gmd_confinamento_alvo,
        "dias_estimados": dias_confinamento,
        "custo_diario_estimado_rs": custo_diaria,
        "custo_total_alimentar_rs": round(custo_total_fase, 2),
        "alimentacao_recomendada": "Dieta TMR (80% Concentrado / 20% Volumoso): Silagem de milho/sorgo + milho moído, farelo de soja e núcleo com ureia/monensina."
    }

# 3. MOTOR PRINCIPAL DA APLICAÇÃO (SIMULADOR DE ENTRADA DO USUÁRIO)
def processar_simulacao(
    chave_raca: str,
    peso_inicial: float,
    preco_compra_arroba: float,
    preco_venda_arroba: float,
    custo_diaria_recria: float = 4.50,
    custo_diaria_confinamento: float = 14.00
) -> dict:
    
    raca = BANCO_RACAS.get(chave_raca.lower())
    if not raca:
        return {"erro": "Raça não encontrada na base de dados."}
        
    analise_agio = calcular_agio(preco_compra_arroba, preco_venda_arroba)
    dados_recria = simular_recria(raca, peso_inicial, custo_diaria_recria)
    dados_confinamento = simular_confinamento(raca, peso_inicial, custo_diaria_confinamento)
    
    return {
        "raca_selecionada": raca.nome,
        "analise_agio": analise_agio,
        "modulo_recria": dados_recria,
        "modulo_confinamento": dados_confinamento
    }


# ==========================================
# TESTE DO CÓDIGO
# ==========================================
if __name__ == "__main__":
    # Exemplo: Nelore comprado a 240 R$/@ com venda projetada a 230 R$/@ pesando 220kg
    resultado = processar_simulacao(
        chave_raca="nelore",
        peso_inicial=220.0,
        preco_compra_arroba=240.0,
        preco_venda_arroba=230.0
    )
    
    # Exibição simplificada em console
    import json
    print(json.dumps(resultado, indent=4, ensure_ascii=False))
