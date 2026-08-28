<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Calculadora de Gado - Viabilidade do Lote</title>
  <!-- Tailwind CSS via CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- FontAwesome Ícones -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen py-6 px-4">

  <div class="max-w-4xl mx-auto space-y-6">
    
    <!-- Cabeçalho -->
    <header class="flex flex-col sm:flex-row items-center justify-between bg-slate-800 p-6 rounded-2xl border border-slate-700 shadow-lg gap-4">
      <div class="flex items-center gap-3">
        <div class="bg-emerald-500/20 p-3 rounded-xl text-emerald-400">
          <i class="fa-solid font-bold fa-calculator text-2xl"></i>
        </div>
        <div>
          <h1 class="text-2xl font-bold text-white">Calculadora de Gado</h1>
          <p class="text-slate-400 text-sm">Simulador de Lucratividade e Recria/Engorda</p>
        </div>
      </div>
      <!-- Status Online/Offline -->
      <div id="status-badge" class="flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 px-3 py-1.5 rounded-full text-sm font-medium">
        <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
        <span id="status-text">Online & Conectado</span>
      </div>
    </header>

    <!-- Formulário de Entrada -->
    <div class="bg-slate-800 p-6 rounded-2xl border border-slate-700 shadow-lg space-y-6">
      <h2 class="text-lg font-semibold text-emerald-400 border-b border-slate-700 pb-2 flex items-center gap-2">
        <i class="fa-solid fa-pen-to-square"></i> Dados do Lote
      </h2>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        
        <!-- Descrição -->
        <div class="col-span-1 md:col-span-2 lg:col-span-3">
          <label class="block text-xs text-slate-400 mb-1">Descrição do Lote</label>
          <input type="text" id="descricao" value="Lote 24 Cabeças Nelore" placeholder="Ex: Garrotes Nelore do Sítio" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-emerald-500">
        </div>

        <!-- Quantidade de Animais -->
        <div>
          <label class="block text-xs text-slate-400 mb-1">Qtd. de Animais (cabeças)</label>
          <input type="number" id="qtdAnimais" value="24" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-emerald-500">
        </div>

        <!-- Valor Compra / Cabeça -->
        <div>
          <label class="block text-xs text-slate-400 mb-1">Valor de Aquisição / Cabeça (R$)</label>
          <input type="number" id="valorAquisicao" value="2300" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-emerald-500">
        </div>

        <!-- Peso Inicial -->
        <div>
          <label class="block text-xs text-slate-400 mb-1">Peso Inicial / Cabeça (kg)</label>
          <input type="number" id="pesoInicial" value="285" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-emerald-500">
        </div>

        <!-- Peso Final -->
        <div>
          <label class="block text-xs text-slate-400 mb-1">Peso Final Esperado / Cabeça (kg)</label>
          <input type="number" id="pesoFinal" value="540" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-emerald-500">
        </div>

        <!-- GMD -->
        <div>
          <label class="block text-xs text-slate-400 mb-1">GMD - Ganho Médio Diário (kg)</label>
          <input type="number" step="0.01" id="gmd" value="0.75" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-emerald-500">
        </div>

        <!-- Valor Pasto -->
        <div>
          <label class="block text-xs text-slate-400 mb-1">Custo Pasto/Mês por Cabeça (R$)</label>
          <input type="number" id="valorPasto" value="60" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-emerald-500">
        </div>

        <!-- Rendimento Carcaça -->
        <div>
          <label class="block text-xs text-slate-400 mb-1">Rendimento de Carcaça (%)</label>
          <input type="number" step="0.1" id="rendimento" value="53" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-emerald-500">
        </div>

        <!-- Cotação Boi Gordo -->
        <div>
          <label class="block text-xs text-slate-400 mb-1">Cotação Boi Gordo Venda (R$/@)</label>
          <input type="number" id="cotacaoBoiGordo" value="330" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-emerald-500">
        </div>

      </div>
    </div>

    <!-- Resultados -->
    <div id="resultado-card" class="bg-slate-800 p-6 rounded-2xl border border-slate-700 shadow-lg space-y-6">
      
      <!-- Cabeçalho do Veredito -->
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center border-b border-slate-700 pb-4 gap-4">
        <div>
          <h2 class="text-xl font-bold text-white" id="res-descricao">Resultados do Lote</h2>
          <p class="text-slate-400 text-sm" id="res-dias-permanencia">Tempo estimado: 0 dias</p>
        </div>
        <div id="badge-lucro" class="px-4 py-2 rounded-xl text-lg font-bold flex items-center gap-2">
          <!-- Dinâmico via JS -->
        </div>
      </div>

      <!-- Grid de Métricas Principais -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        
        <div class="bg-slate-900 p-4 rounded-xl border border-slate-700/50">
          <span class="text-xs text-slate-400">Ágio na Compra</span>
          <p class="text-xl font-bold mt-1" id="res-agio">0%</p>
          <span class="text-[10px] text-slate-500">vs Boi Gordo</span>
        </div>

        <div class="bg-slate-900 p-4 rounded-xl border border-slate-700/50">
          <span class="text-xs text-slate-400">R$ / @ Entrada</span>
          <p class="text-xl font-bold text-white mt-1" id="res-arroba-entrada">R$ 0,00</p>
          <span class="text-[10px] text-slate-500" id="res-arrobas-inicial">0 @/cab</span>
        </div>

        <div class="bg-slate-900 p-4 rounded-xl border border-slate-700/50">
          <span class="text-xs text-slate-400">R$ / @ Saída Esperada</span>
          <p class="text-xl font-bold text-white mt-1" id="res-arroba-saida">R$ 0,00</p>
          <span class="text-[10px] text-slate-500" id="res-arrobas-final">0 @/cab</span>
        </div>

        <div class="bg-slate-900 p-4 rounded-xl border border-slate-700/50">
          <span class="text-xs text-slate-400">Lucro Total do Lote</span>
          <p class="text-xl font-bold text-emerald-400 mt-1" id="res-lucro-total">R$ 0,00</p>
          <span class="text-[10px] text-slate-500" id="res-lucro-cabeca">R$ 0,00 / cab</span>
        </div>

      </div>

      <!-- Resumo Financeiro Detalhado -->
      <div class="bg-slate-900/60 p-4 rounded-xl border border-slate-700 space-y-2 text-sm">
        <h3 class="font-semibold text-slate-300 border-b border-slate-700/50 pb-2">Resumo Financeiro e Custo de Manejo</h3>
        <div class="flex justify-between text-slate-400">
          <span>Investimento Inicial em Animais:</span>
          <span class="font-medium text-white" id="res-total-compra">R$ 0,00</span>
        </div>
        <div class="flex justify-between text-slate-400">
          <span>Custo Total de Pastagem/Manejo:</span>
          <span class="font-medium text-white" id="res-total-pasto">R$ 0,00</span>
        </div>
        <div class="flex justify-between text-slate-400">
          <span>Custo Total do Lote (Entrada + Pasto):</span>
          <span class="font-medium text-white" id="res-custo-total">R$ 0,00</span>
        </div>
        <div class="flex justify-between text-slate-400">
          <span>Faturamento Bruto Previsto:</span>
          <span class="font-medium text-emerald-400" id="res-faturamento-total">R$ 0,00</span>
        </div>
        <div class="flex justify-between text-slate-400 font-bold border-t border-slate-700/50 pt-2">
          <span>Retorno sobre Investimento (ROI):</span>
          <span class="text-emerald-400" id="res-roi">0%</span>
        </div>
      </div>

    </div>

  </div>

  <!-- JavaScript do Aplicativo -->
  <script>
    // Seleção dos elementos do DOM
    <script>
    const inputs = ['descricao', 'qtdAnimais', 'valorAquisicao', 'pesoInicial', 'pesoFinal', 'gmd', 'valorPasto', 'rendimento', 'cotacaoBoiGordo'];
    
    // Função principal de cálculo
    function calcular() {
      const desc = document.getElementById('descricao').value || 'Lote sem nome';
      const qtd = parseFloat(document.getElementById('qtdAnimais').value) || 0;
      const vlrAquisicao = parseFloat(document.getElementById('valorAquisicao').value) || 0;
      const pInicial = parseFloat(document.getElementById('pesoInicial').value) || 0;
      const pFinal = parseFloat(document.getElementById('pesoFinal').value) || 0;
      const gmd = parseFloat(document.getElementById('gmd').value) || 0.01;
      const vlrPastoMes = parseFloat(document.getElementById('valorPasto').value) || 0;
      const rend = (parseFloat(document.getElementById('rendimento').value) || 50) / 100;
      const cotacaoGordo = parseFloat(document.getElementById('cotacaoBoiGordo').value) || 0;

      // 1. Cálculos de Arrobas e Entrada
      const arrobasEntradaCabeca = (pInicial * 0.50) / 15; // Bezerro/Garrote usa 50% padrão de carcaça
      const valorArrobaEntrada = arrobasEntradaCabeca > 0 ? (vlrAquisicao / arrobasEntradaCabeca) : 0;
      
      // 2. Ágio (%)
      const agio = cotacaoGordo > 0 ? (((valorArrobaEntrada / cotacaoGordo) - 1) * 100) : 0;

      // 3. Tempo e Custos de Pasto
      const ganhoPesoNecessario = Math.max(0, pFinal - pInicial);
      const diasPermanencia = Math.ceil(ganhoPesoNecessario / gmd);
      const mesesPermanencia = diasPermanencia / 30;
      const custoPastoCabeca = mesesPermanencia * vlrPastoMes;
      const custoPastoTotal = custoPastoCabeca * qtd;

      // 4. Faturamento e Arrobas na Saída
      const arrobasSaidaCabeca = (pFinal * rend) / 15;
      const faturamentoCabeca = arrobasSaidaCabeca * cotacaoGordo;
      const faturamentoTotal = faturamentoCabeca * qtd;

      // 5. Totais e Margem
      const investimentoCompraTotal = vlrAquisicao * qtd;
      const custoTotalLote = investimentoCompraTotal + custoPastoTotal;
      const lucroTotal = faturamentoTotal - custoTotalLote;
      const lucroPorCabeca = lucroTotal / (qtd || 1);
      const roi = custoTotalLote > 0 ? ((lucroTotal / custoTotalLote) * 100) : 0;

      // Update do DOM
      document.getElementById('res-descricao').innerText = desc;
      document.getElementById('res-dias-permanencia').innerText = `Tempo estimado: ${diasPermanencia} dias (~${mesesPermanencia.toFixed(1)} meses)`;
      
      // Card do Ágio
      const elAgio = document.getElementById('res-agio');
      elAgio.innerText = `${agio.toFixed(1)}%`;
      elAgio.className = `text-xl font-bold mt-1 ${agio <= 0 ? 'text-emerald-400' : 'text-amber-400'}`;

      // Valores de Arroba
      document.getElementById('res-arroba-entrada').innerText = `R$ ${valorArrobaEntrada.toFixed(2)}`;
      document.getElementById('res-arrobas-inicial').innerText = `${arrobasEntradaCabeca.toFixed(2)} @/cab`;
      document.getElementById('res-arroba-saida').innerText = `R$ ${cotacaoGordo.toFixed(2)}`;
      document.getElementById('res-arrobas-final').innerText = `${arrobasSaidaCabeca.toFixed(2)} @/cab`;

      // Resumo Financeiro
      document.getElementById('res-total-compra').innerText = `R$ ${investimentoCompraTotal.toLocaleString('pt-BR', {minimumFractionDigits: 2})}`;
      document.getElementById('res-total-pasto').innerText = `R$ ${custoPastoTotal.toLocaleString('pt-BR', {minimumFractionDigits: 2})}`;
      document.getElementById('res-custo-total').innerText = `R$ ${custoTotalLote.toLocaleString('pt-BR', {minimumFractionDigits: 2})}`;
      document.getElementById('res-faturamento-total').innerText = `R$ ${faturamentoTotal.toLocaleString('pt-BR', {minimumFractionDigits: 2})}`;
      document.getElementById('res-lucro-total').innerText = `R$ ${lucroTotal.toLocaleString('pt-BR', {minimumFractionDigits: 2})}`;
      document.getElementById('res-lucro-cabeca').innerText = `R$ ${lucroPorCabeca.toLocaleString('pt-BR', {minimumFractionDigits: 2})} / cab`;
      document.getElementById('res-roi').innerText = `${roi.toFixed(1)}%`;

      // Badge Veredito
      const badge = document.getElementById('badge-lucro');
      if (lucroTotal > 0) {
        badge.className = 'px-4 py-2 rounded-xl text-lg font-bold flex items-center gap-2 bg-emerald-500/20 text-emerald-400 border border-emerald-500/30';
        badge.innerHTML = `<i class="fa-solid fa-circle-check"></i> BOM NEGÓCIO (LUCRO)`;
      } else {
        badge.className = 'px-4 py-2 rounded-xl text-lg font-bold flex items-center gap-2 bg-red-500/20 text-red-400 border border-red-500/30';
        badge.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> PREJUÍZO PREVISTO`;
      }
    }

    // Monitorar digitação em tempo real
    inputs.forEach(id => {
      document.getElementById(id).addEventListener('input', calcular);
    });

    // Monitorar conexão com a internet
    function atualizarStatusConexao() {
      const badge = document.getElementById('status-badge');
      const text = document.getElementById('status-text');
      
      if (navigator.onLine) {
        badge.className = "flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 px-3 py-1.5 rounded-full text-sm font-medium";
        text.innerText = "Online & Conectado";
      } else {
        badge.className = "flex items-center gap-2 bg-amber-500/10 border border-amber-500/30 text-amber-400 px-3 py-1.5 rounded-full text-sm font-medium";
        text.innerText = "Modo Offline (Dados Locais)";
      }
    }

    window.addEventListener('online', atualizarStatusConexao);
    window.addEventListener('offline', atualizarStatusConexao);

    // Inicializar na carga da página
    calcular();
    atualizarStatusConexao();
  </script>
</body>
</html>
