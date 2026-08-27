class CalculadoraPecuaria:
    def __init__(self):
        pass

    @staticmethod
    def kg_para_arrobas_vivas(peso_kg):
        """Converte peso vivo em kg para arrobas vivas (@)."""
        return peso_kg / 30.0

    @staticmethod
    def calcular_carcaca_kg(peso_vivo_kg, rendimento_porcentagem):
        """Calcula o peso total de carcaça em kg."""
        return peso_vivo_kg * (rendimento_porcentagem / 100.0)

    @staticmethod
    def calcular_arrobas_carcaca(peso_vivo_kg, rendimento_porcentagem):
        """Calcula a quantidade de arrobas (@) de carcaça."""
        carcaca_kg = peso_vivo_kg * (rendimento_porcentagem / 100.0)
        return carcaca_kg / 15.0

    def funcao_recria(self, 
                      peso_inicial_kg, 
                      peso_final_kg, 
                      dias_recria, 
                      custo_aquisicao, 
                      custo_diario_pasto_suplemento, 
                      custo_sanidade_outros, 
                      rendimento_carcaca_estimado=52.0):
        """
        FUNÇÃO 1: SIMULAÇÃO DE RECRIA (Pasto / Suplementação)
        """
        gmd_kg = (peso_final_kg - peso_inicial_kg) / dias_recria
        
        arrobas_iniciais = self.calcular_arrobas_carcaca(peso_inicial_kg, rendimento_carcaca_estimado)
        arrobas_finais = self.calcular_arrobas_carcaca(peso_final_kg, rendimento_carcaca_estimado)
        arrobas_ganhas = arrobas_finais - arrobas_iniciais
        
        custo_alimentacao_total = custo_diario_pasto_suplemento * dias_recria
        custo_total_recria = custo_aquisicao + custo_alimentacao_total + custo_sanidade_outros
        
        custo_por_arroba_ganha = (custo_alimentacao_total + custo_sanidade_outros) / arrobas_ganhas if arrobas_ganhas > 0 else 0
        break_even_arroba = custo_total_recria / arrobas_finais

        return {
            "dias_recria": dias_recria,
            "gmd_kg_dia": round(gmd_kg, 3),
            "arrobas_ganhas": round(arrobas_ganhas, 2),
            "custo_total_acumulado": round(custo_total_recria, 2),
            "custo_por_arroba_produzida": round(custo_por_arroba_ganha, 2),
            "break_even_arroba": round(break_even_arroba, 2)
        }

    def funcao_confinamento(self, 
                            peso_entrada_kg, 
                            peso_meta_kg, 
                            gmd_esperado_kg, 
                            custo_diario_dieta, 
                            custo_diario_operacional, 
                            valor_aquisicao_animal, 
                            rendimento_carcaca_estimado=54.0):
        """
        FUNÇÃO 2: SIMULAÇÃO DE CONFINAMENTO (Engorda Intensiva)
        """
        ganho_necessario_kg = peso_meta_kg - peso_entrada_kg
        dias_cocho = ganho_necessario_kg / gmd_esperado_kg
        
        custo_diario_total = custo_diario_dieta + custo_diario_operacional
        custo_cocho_total = custo_diario_total * dias_cocho
        custo_total_animal = valor_aquisicao_animal + custo_cocho_total
        
        arrobas_finais = self.calcular_arrobas_carcaca(peso_meta_kg, rendimento_carcaca_estimado)
        break_even_arroba = custo_total_animal / arrobas_finais

        return {
            "dias_de_cocho": int(round(dias_cocho)),
            "ganho_peso_total_kg": round(ganho_necessario_kg, 2),
            "custo_cocho_total": round(custo_cocho_total, 2),
            "custo_total_acumulado": round(custo_total_animal, 2),
            "arrobas_finais_carcaca": round(arrobas_finais, 2),
            "break_even_arroba": round(break_even_arroba, 2)
        }


# ==========================================
# EXEMPLO DE USO / TESTE DAS DUAS FUNÇÕES
# ==========================================
if __name__ == "__main__":
    calc = CalculadoraPecuaria()

    print("--- 1. TESTE DA FUNÇÃO RECRIA (Bezerro -> Garrote/Novilha) ---")
    resultado_recria = calc.funcao_recria(
        peso_inicial_kg=200,                # Peso de compra do bezerro
        peso_final_kg=350,                  # Peso final projetado na recria
        dias_recria=300,                    # Período de recria (dias)
        custo_aquisicao=2200.00,            # Preço pago no bezerro (R$)
        custo_diario_pasto_suplemento=2.50, # Custo de pasto + sal/proteinado por dia (R$)
        custo_sanidade_outros=150.00,       # Vacinas, frete, exames (R$)
        rendimento_carcaca_estimado=52.0    # 52% para recria
    )
    for chave, valor in resultado_recria.items():
        print(f"{chave}: {valor}")

    print("\n--- 2. TESTE DA FUNÇÃO CONFINAMENTO (Garrote -> Boi Gordo) ---")
    resultado_confinamento = calc.funcao_confinamento(
        peso_entrada_kg=380,                # Peso de entrada no cocho
        peso_meta_kg=540,                   # Peso final desejado no abate
        gmd_esperado_kg=1.5,                # Ganho Médio Diário no cocho (kg/dia)
        custo_diario_dieta=14.50,           # Dieta total por cabeça/dia (R$)
        custo_diario_operacional=2.00,      # Mão de obra, diesel, depreciação por dia (R$)
        valor_aquisicao_animal=3500.00,     # Custo/Avaliação do garrote ao entrar no cocho (R$)
        rendimento_carcaca_estimado=54.0    # 54% rendimento de carcaça no abate
    )
    for chave, valor in resultado_confinamento.items():
        print(f"{chave}: {valor}")
