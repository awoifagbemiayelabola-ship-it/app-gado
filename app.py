# ==========================================
# CÁLCULO DE PONTUAÇÃO / DESEMPENHO DO GADO
# ==========================================

def calcular_desempenho_gado(peso_inicial, peso_final, dias_confiamento, consumo_diario_kg):
    """
    Calcula o ganho de peso total, ganho médio diário (GMD) 
    e a conversão alimentar do lote.
    """
    # Ganho de peso total (kg)
    ganho_peso_total = peso_final - peso_inicial
    
    # Ganho Médio Diário - GMD (kg/dia)
    if dias_confiamento > 0:
        gmd = ganho_peso_total / dias_confiamento
    else:
        gmd = 0.0

    # Conversão Alimentar (kg de alimento / kg de peso ganho)
    if ganho_peso_total > 0:
        conversion_alimentar = consumo_diario_kg / gmd
    else:
        conversion_alimentar = 0.0

    return {
        "ganho_peso_total_kg": round(ganho_peso_total, 2),
        "gmd_kg_dia": round(gmd, 3),
        "conversao_alimentar": round(conversion_alimentar, 2)
    }

# ==========================================
# EXEMPLO DE USO / ENTRADA DE DADOS
# ==========================================

if __name__ == "__main__":
    print("--- CALCULADORA DE GADO ---")
    
    # Entradas mantidas
    peso_ini = float(input("Peso inicial do animal/lote (kg): "))
    peso_fim = float(input("Peso final do animal/lote (kg): "))
    dias = int(input("Total de dias em confinamento/pasto: "))
    consumo_dia = float(input("Consumo médio de ração/pasto por dia (kg): "))

    # Processamento
    resultado = calcular_desempenho_gado(peso_ini, peso_fim, dias, consumo_dia)

    # Exibição dos resultados
    print("\n--- RESULTADOS ---")
    print(f"Ganho de Peso Total: {resultado['ganho_peso_total_kg']} kg")
    print(f"Ganho Médio Diário (GMD): {resultado['gmd_kg_dia']} kg/dia")
    print(f"Conversão Alimentar: {resultado['conversao_alimentar']} kg de alimento/kg ganho")
