# Estrutura dos dados: [Nome, ID, Prioridade, Peso(kg), Combustível(%), Horário]
energia = ["Energia", 1, "Vital", 8500, 95, "08:00"]
habitacao = ["Habitação", 2, "Vital", 12000, 90, "8:30"]
suporteMedico = ["Suporte Médico", 3, "Médio", 5000, 85, "8:15"]
logistica = ["Logística", 4, "Baixo", 15000, 80, "9:00"]
laboratorio = ["Laboratório", 5, "Baixo", 7200, 92, "10:00"]

modulos = [suporteMedico, laboratorio, energia, logistica, habitacao]

print("="*80)
print("Análise para o pouso em Marte")
print("="*80)

# --- Identificação do Módulo com Menor Combustível ---
menorCombustivel = modulos[0]

for c in modulos[1:]:
    if c[4] <= menorCombustivel[4]:
        menorCombustivel = c

print(f"O Módulo {menorCombustivel[0]} tem a menor quantidade de combustível: {menorCombustivel[4]}%")
print("="*80)

# --- Ordenação e Exibição por Peso (Crescente) ---
ordenados = sorted(modulos, key=lambda x: x[3])
print("Lista de peso:\n")
for i, lista in enumerate(ordenados):
    nome, peso = lista[0], lista[3]
    
    if i == 0:
        print(f"- {nome} ({peso}kg) [MENOR]")
    elif i == len(ordenados) - 1:
        print(f"- {nome} ({peso}kg) [MAIOR]")
    else:
        print(f"- {nome} ({peso}kg)")
print("="*80)

# --- Algoritmo de Ordenação: Insertion Sort (Ordena pelo ID - index 1) ---
def insertionSort(array):
    n = len(array)
    if n <= 1:
        return
    for i in range(1, n):
        key = array[i]
        j = i - 1
        while j >= 0 and key[1] < array[j][1]:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key

# Função auxiliar para gerenciar a entrada em filas (FIFO)
def fila_enqueue(fila, item):
    fila.append(item)

# --- Lógica de Validação para Pouso ---
def checar_pouso(modulo):
    """
    Verifica se o módulo atende aos critérios:
    - Prioridade: Vital ou Médio
    - Peso: Até 15.000kg
    - Combustível: Mínimo 30%
    """
    prioridade_ok = modulo[2] in ["Vital", "Médio"]
    peso_ok = modulo[3] <= 15000
    combustivel_ok = modulo[4] >= 30
    
    return prioridade_ok and peso_ok and combustivel_ok

# --- Processamento e Categorização dos Módulos ---
autorizacaoPouso = []
esperaOrbita = []
emergencia = []

# Criamos uma cópia da lista original para ordenar sem afetar os dados brutos
modulosOrdenados = list(modulos)
insertionSort(modulosOrdenados)

for i in modulosOrdenados:
    # Condição Crítica: Emergência imediata
    if i[4] <= 15 or i[3] > 15000:
        print(f"ALERTA: Módulo {i[0]} em EMERGÊNCIA!")
        fila_enqueue(emergencia, i)
    
    # Condição Operacional: Autorização de Pouso
    elif checar_pouso(i):
        print(f"{i[0]}: Pronto para pouso.")
        fila_enqueue(autorizacaoPouso, i)
    
    # Condição de Espera: Baixa prioridade ou critérios não atingidos
    else:
        print(f"{i[0]}: Em espera orbital.")
        fila_enqueue(esperaOrbita, i)

print("="*80)
print(f"RESUMO DA MISSÃO:")
print(f"- Emergência: {len(emergencia)}")
print(f"- Autorizados: {len(autorizacaoPouso)}")
print(f"- Em Órbita:   {len(esperaOrbita)}")