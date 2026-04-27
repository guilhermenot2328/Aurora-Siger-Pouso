# Estrutura dos dados: [Nome, ID, Prioridade, Criticidade, Peso(kg), Combustível(%), Horário]
energia        = ["Energia",        1, 1, "Vital", 8500,  95, "08:00"]
habitacao      = ["Habitação",      2, 2, "Vital", 12000, 90, "08:30"]
suporteMedico  = ["Suporte Médico", 3, 3, "Alta",  5000,  85, "08:15"]
logistica      = ["Logística",      4, 4, "Alta",  15000, 80, "09:00"]
laboratorio    = ["Laboratório",    5, 5, "Média", 7200,  92, "10:00"]

modulos = [suporteMedico, laboratorio, energia, logistica, habitacao]

print("=" * 80)
print("Análise para o pouso em Marte")
print("=" * 80)

# --- Identificação do Módulo com Menor Combustível ---
menorCombustivel = modulos[0]

for c in modulos[1:]:
    if c[5] < menorCombustivel[5]:
        menorCombustivel = c

print(f"O Módulo {menorCombustivel[0]} tem a menor quantidade de combustível: {menorCombustivel[5]}%")
print("=" * 80)

# --- Ordenação e Exibição por Peso (Crescente) ---
ordenados = sorted(modulos, key=lambda x: x[4])
print("Lista de peso:\n")
for i, lista in enumerate(ordenados):
    nome, peso = lista[0], lista[4]

    if i == 0:
        print(f"- {nome} ({peso}kg) [MENOR]")
    elif i == len(ordenados) - 1:
        print(f"- {nome} ({peso}kg) [MAIOR]")
    else:
        print(f"- {nome} ({peso}kg)")
print("=" * 80)


# --- Algoritmo de Ordenação: Insertion Sort (ordena pela Prioridade - index 2) ---
def insertionSort(array):
    n = len(array)
    if n <= 1:
        return
    for i in range(1, n):
        key = array[i]
        j = i - 1
        while j >= 0 and key[2] < array[j][2]:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key


# --- Algoritmo de Busca Linear (Item 3 do enunciado) ---
def busca_linear(array, indice_campo, valor):
    """
    Retorna o primeiro módulo cujo campo (na posição 'indice_campo') seja
    igual a 'valor'. Retorna None se não encontrar.
    Exemplo: busca_linear(modulos, 3, "Vital") -> retorna o módulo Energia.
    """
    for item in array:
        if item[indice_campo] == valor:
            return item
    return None


# Função auxiliar para gerenciar a entrada em filas (FIFO)
def fila_enqueue(fila, item):
    fila.append(item)


# Função auxiliar para gerenciar a entrada em pilhas (LIFO)
def pilha_push(pilha, item):
    pilha.append(item)


def pilha_pop(pilha):
    """Remove e retorna o último item empilhado (LIFO). None se vazia."""
    if not pilha:
        return None
    return pilha.pop()


# ==============================================================================
# ITEM 2 -- PORTAS LÓGICAS
# Implementação direta das portas do diagrama (pág. 4 do relatório). Cada porta
# é uma função de uma linha, espelhando a tabela-verdade.
# ==============================================================================
def AND(*args):  return int(all(args))
def OR(*args):   return int(any(args))
def NOT(a):      return int(not a)
def NAND(*args): return NOT(AND(*args))
def NOR(*args):  return NOT(OR(*args))
def XOR(a, b):   return int(a != b)
def XNOR(a, b):  return int(a == b)


# --- Expressão booleana final do MGPEB (pág. 6 do relatório) ---
def autorizar_pouso(C, A, P, H, S1, S2, Kb, KB, E, Mm, Mr):
    """
    Reproduz a expressão booleana final do circuito do Item 2:
        S      = (S1 == S2)                  -> XNOR (sensores concordam)
        HS_OK  = (Kb == KB)                  -> XNOR (códigos de handshake)
        N      = C · A · P · H · S · HS_OK   -> AND  (pouso nominal)
        Em     = E · P · S                   -> AND  (rota de emergência)
        AUTORIZAR_POUSO = N + Em             -> OR
        BLOQUEIO        = ¬ AUTORIZAR_POUSO  -> NOT
        ALARM_ABORT     = ¬ (C · P)          -> NAND
        LIBERA_EVA      = ¬ (Mm + Mr)        -> NOR
    """
    S      = XNOR(S1, S2)
    HS_OK  = XNOR(Kb, KB)
    N      = AND(C, A, P, H, S, HS_OK)
    Em     = AND(E, P, S)
    autoriza    = OR(N, Em)
    bloqueio    = NOT(autoriza)
    alarm_abort = NAND(C, P)
    libera_eva  = NOR(Mm, Mr)
    return {
        "N": N, "Em": Em, "S": S, "HS_OK": HS_OK,
        "AUTORIZAR_POUSO": autoriza,
        "BLOQUEIO": bloqueio,
        "ALARM_ABORT": alarm_abort,
        "LIBERA_EVA": libera_eva,
    }


# ==============================================================================
# ITEM 4 -- FUNÇÕES MATEMÁTICAS APLICADAS AO POUSO
# ==============================================================================
def altura(t, h0=2000, v0=-50, g=3.71):
    """
    h(t) = h0 + v0*t - 0.5*g*t^2
    Modelo da descida controlada em Marte (antes da desaceleração ativa).
    """
    return h0 + v0 * t - 0.5 * g * t ** 2


def velocidade(t, v0=-50, g=3.71):
    """v(t) = v0 - g*t  (taxa de variação de h em relação a t)."""
    return v0 - g * t


def consumo(v, k=0.05):
    """
    C(v) = k * v^2  (kg de combustível para dissipar a energia cinética).
    Forma quadrática: pequenos atrasos -> grandes aumentos no consumo.
    """
    return k * v ** 2


def sinal_H(t):
    """
    Sinal binário H que alimenta o circuito do Item 2.
    H = 1 quando h(t) está dentro do envelope de retrofoguete (500m a 1500m).
    """
    h = altura(t)
    return int(500 <= h <= 1500)


# --- Pré-filtro alternativo (validação operacional simples do módulo) ---
def checar_pouso(modulo):
    """
    Pré-filtro independente das condições atmosféricas:
    - Criticidade: Vital ou Alta
    - Peso: até 15.000kg
    - Combustível: mínimo 30%
    """
    criticidade_ok  = modulo[3] in ["Vital", "Alta"]
    peso_ok         = modulo[4] <= 15000
    combustivel_ok  = modulo[5] >= 30
    return criticidade_ok and peso_ok and combustivel_ok


# ==============================================================================
# ESTADO INICIAL CONFORME RELATÓRIO (pág. 3)
#   FILA    (autorização): [Energia, Habitação, Suporte Médico]
#   STANDBY (em órbita):   [Logística, Laboratório]
#   ALERTA  (emergência):  []
# ==============================================================================
autorizacaoPouso = [energia, habitacao, suporteMedico]   # FILA  (FIFO)
esperaOrbita     = [logistica, laboratorio]              # LISTA (standby)
emergencia       = []                                    # LISTA (alerta)
historicoPouso   = []                                    # PILHA (LIFO)

# Garante que a fila esteja em ordem de prioridade (insertion sort).
insertionSort(autorizacaoPouso)

# Demonstra o insertion sort também em uma cópia da lista geral (fora de ordem).
modulosOrdenados = list(modulos)
insertionSort(modulosOrdenados)
print("Módulos ordenados por prioridade (insertion sort):")
for m in modulosOrdenados:
    print(f"  P{m[2]}: {m[0]}")
print("=" * 80)

print("Estado inicial:")
print(f"  Fila de autorização: {[m[0] for m in autorizacaoPouso]}")
print(f"  Espera em órbita:    {[m[0] for m in esperaOrbita]}")
print(f"  Emergência:          {[m[0] for m in emergencia]}")
print("=" * 80)


# ==============================================================================
# SIMULAÇÃO DE POUSO USANDO O CIRCUITO BOOLEANO (Item 3 + Item 2)
# ==============================================================================
def simular_pouso(modulo, t_descida, sensores=None):
    """
    Aplica o circuito booleano do Item 2 ao módulo na altura h(t_descida).
    'sensores' permite sobrescrever os sinais (C, A, P, S1, S2, Kb, KB, E,
    Mm, Mr); por padrão assume condições nominais (todos OK, sem emergência).
    """
    pad = {
        "C": 1 if modulo[5] >= 15 else 0,   # combustível mínimo de operação
        "A": 1, "P": 1,
        "S1": 1, "S2": 1,
        "Kb": 1, "KB": 1,
        "E": 0, "Mm": 0, "Mr": 0,
    }
    if sensores:
        pad.update(sensores)

    H = sinal_H(t_descida)
    return autorizar_pouso(
        pad["C"], pad["A"], pad["P"], H,
        pad["S1"], pad["S2"], pad["Kb"], pad["KB"],
        pad["E"], pad["Mm"], pad["Mr"],
    )


print("Simulando pousos (t = 8s, dentro do envelope de paraquedas):")
fila_pendente = []
while autorizacaoPouso:
    modulo = autorizacaoPouso.pop(0)            # remove da FILA (FIFO)
    sinais = simular_pouso(modulo, t_descida=8)

    # IF / ELIF / ELSE refletindo a expressão booleana final
    if sinais["ALARM_ABORT"] == 1:
        # NAND(C, P) = 1 -> aborto, módulo vai à lista de alerta
        fila_enqueue(emergencia, modulo)
        print(f"  [ABORT] {modulo[0]:<16} -> ALARM_ABORT=1 (NAND C,P)")
    elif sinais["AUTORIZAR_POUSO"] == 1:
        # AUTORIZAR_POUSO = N + Em -> pousa, vai à PILHA (LIFO)
        pilha_push(historicoPouso, modulo)
        print(f"  [OK]    {modulo[0]:<16} -> N={sinais['N']}, Em={sinais['Em']}, AUTORIZA=1")
    else:
        # BLOQUEIO = 1 -> volta para a fila pendente
        fila_pendente.append(modulo)
        print(f"  [HOLD]  {modulo[0]:<16} -> AUTORIZA=0, BLOQUEIO=1")

# Devolve à fila os módulos que ficaram em hold (mantém FIFO).
autorizacaoPouso.extend(fila_pendente)
print("=" * 80)


# ==============================================================================
# CENÁRIOS DE TESTE -- exercitando portas individuais do circuito
# ==============================================================================
print("Cenários de falha (validam portas isoladas do circuito):\n")

# XOR: divergência entre altímetros redundantes (S1 != S2)
falha = simular_pouso(energia, t_descida=8, sensores={"S1": 1, "S2": 0})
print(f"  Divergência S1≠S2:  S=XNOR={falha['S']}  AUTORIZA={falha['AUTORIZAR_POUSO']}")

# NAND: combustível crítico (C=0) com pista livre (P=1)
critico = simular_pouso(energia, t_descida=8, sensores={"C": 0})
print(f"  Combustível baixo:  ALARM_ABORT=NAND(C,P)={critico['ALARM_ABORT']}  AUTORIZA={critico['AUTORIZAR_POUSO']}")

# NOR: alerta de meteoro impede liberação de EVA
meteoro = simular_pouso(energia, t_descida=8, sensores={"Mm": 1})
print(f"  Alerta de meteoro:  LIBERA_EVA=NOR(Mm,Mr)={meteoro['LIBERA_EVA']}")

# OR: emergência libera pouso mesmo sem N (rota Em = E·P·S)
emerg = simular_pouso(energia, t_descida=30, sensores={"E": 1})  # t=30 -> H=0
print(f"  Reentrada forçada:  N={emerg['N']}, Em={emerg['Em']}, AUTORIZA={emerg['AUTORIZAR_POUSO']}")
print("=" * 80)


# --- Demonstração da Busca Linear ---
vital = busca_linear(modulos, 3, "Vital")
print(f"Busca por criticidade 'Vital' -> primeiro módulo encontrado: {vital[0]}")
print("=" * 80)


# --- Demonstração das funções h(t), v(t) e C(v) (Item 4) ---
print("Funções aplicadas (Item 4):")
print(f"  h(0)  = {altura(0):>7.1f} m   v(0)  = {velocidade(0):>7.2f} m/s")
print(f"  h(8)  = {altura(8):>7.1f} m   v(8)  = {velocidade(8):>7.2f} m/s   (paraquedas)")
print(f"  h(18) = {altura(18):>7.1f} m   v(18) = {velocidade(18):>7.2f} m/s   (retrofoguetes)")
print(f"  Consumo a v=116.8 m/s: C = {consumo(116.8):.1f} kg")
print(f"  Consumo a v=124.2 m/s: C = {consumo(124.2):.1f} kg  (atraso de 2s -> +{consumo(124.2)-consumo(116.8):.1f} kg)")
print("=" * 80)


# --- Resumo da missão ---
print("RESUMO DA MISSÃO:")
print(f"- Emergência:        {len(emergencia)}  -> {[m[0] for m in emergencia]}")
print(f"- Em Órbita:         {len(esperaOrbita)}  -> {[m[0] for m in esperaOrbita]}")
print(f"- Pousos concluídos: {len(historicoPouso)}")
print(f"  Último a pousar (topo da pilha): {historicoPouso[-1][0] if historicoPouso else '-'}")
