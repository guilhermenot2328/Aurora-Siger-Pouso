# ==============================================================================
# POUSO EM MARTE -- Estruturas Lineares, Busca, Ordenação e Autorização
# ==============================================================================
# Estrutura: [Nome, ID, Prioridade, Criticidade, Peso(kg), Combustível(%), Horário]

energia        = ["Energia",        1, 1, "Vital", 8500,  95, "08:00"]
habitacao      = ["Habitação",      2, 2, "Vital", 12000, 90, "08:30"]
suporteMedico  = ["Suporte Médico", 3, 3, "Alta",  5000,  85, "08:15"]
logistica      = ["Logística",      4, 4, "Alta",  15000, 80, "09:00"]
laboratorio    = ["Laboratório",    5, 5, "Média", 7200,  92, "10:00"]

# LISTA  -- todos os módulos cadastrados
modulos = [suporteMedico, laboratorio, energia, logistica, habitacao]

# FILA   (FIFO) -- ordem de autorização para pouso
autorizacaoPouso = [energia, habitacao, suporteMedico]

# LISTA  -- módulos em standby na órbita
esperaOrbita = [logistica, laboratorio]

# LISTA  -- módulos em estado de alerta
emergencia = []

# PILHA  (LIFO) -- histórico de pousos (último a pousar fica no topo)
historicoPouso = []


# ==============================================================================
# OPERAÇÕES DE FILA E PILHA
# ==============================================================================
def fila_enqueue(fila, item):       # entra no fim
    fila.append(item)

def fila_dequeue(fila):             # sai do início (FIFO)
    return fila.pop(0) if fila else None

def pilha_push(pilha, item):        # empilha no topo
    pilha.append(item)

def pilha_pop(pilha):               # desempilha do topo (LIFO)
    return pilha.pop() if pilha else None


# ==============================================================================
# ALGORITMOS DE BUSCA
# ==============================================================================
def busca_menor_combustivel(array):
    """Retorna o módulo com o MENOR valor de combustível (índice 5)."""
    menor = array[0]
    for m in array[1:]:
        if m[5] < menor[5]:
            menor = m
    return menor


def busca_maior_prioridade(array):
    """Retorna o módulo de MAIOR prioridade (menor número em índice 2)."""
    maior = array[0]
    for m in array[1:]:
        if m[2] < maior[2]:
            maior = m
    return maior


def busca_por_carga(array, criticidade):
    """Busca linear: primeiro módulo com a criticidade indicada (índice 3)."""
    for m in array:
        if m[3] == criticidade:
            return m
    return None


# ==============================================================================
# ALGORITMOS DE ORDENAÇÃO
# ==============================================================================
def insertion_sort_prioridade(array):
    """Ordena IN-PLACE pela prioridade (índice 2). Insertion sort clássico."""
    for i in range(1, len(array)):
        chave = array[i]
        j = i - 1
        while j >= 0 and chave[2] < array[j][2]:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = chave


def ordenar_por_peso(array):
    """Retorna nova lista ordenada por peso (índice 4) crescente."""
    return sorted(array, key=lambda m: m[4])


# ==============================================================================
# AUTORIZAÇÃO DE POUSO
# IF/ELIF/ELSE refletindo a expressão booleana modelada no Item 2:
#   N           = C · A · P · H · (S1 XNOR S2) · (Kb XNOR KB)
#   Em          = E · P · (S1 XNOR S2)
#   AUTORIZA    = N + Em
#   ALARM_ABORT = NAND(C, P)
# ==============================================================================
def autorizar_pouso(C, A, P, H, S1, S2, Kb, KB, E):
    sensores_ok  = (S1 == S2)        # XNOR dos altímetros redundantes
    handshake_ok = (Kb == KB)        # XNOR do código base/módulo
    nominal      = C and A and P and H and sensores_ok and handshake_ok
    rota_emerg   = E and P and sensores_ok

    if not (C and P):                # NAND(C,P)=1  -> aborto
        return "ABORT"
    elif nominal or rota_emerg:      # N + Em = 1   -> autoriza
        return "OK"
    else:                            # bloqueio    -> mantém em espera
        return "HOLD"


# ==============================================================================
# EXECUÇÃO
# ==============================================================================
print("=" * 60)
print("Análise para o pouso em Marte")
print("=" * 60)

# --- BUSCAS ---
mc    = busca_menor_combustivel(modulos)
mp    = busca_maior_prioridade(modulos)
vital = busca_por_carga(modulos, "Vital")

print(f"Menor combustível:    {mc[0]} ({mc[5]}%)")
print(f"Maior prioridade:     {mp[0]} (P{mp[2]})")
print(f"1ª carga Vital:       {vital[0]}")
print("=" * 60)

# --- ORDENAÇÕES ---
print("Ordenação por peso (crescente):")
for m in ordenar_por_peso(modulos):
    print(f"  {m[0]:<16} {m[4]} kg")
print()

insertion_sort_prioridade(autorizacaoPouso)
print("Fila de autorização ordenada por prioridade (insertion sort):")
for m in autorizacaoPouso:
    print(f"  P{m[2]}: {m[0]}")
print("=" * 60)

# --- SIMULAÇÃO DA AUTORIZAÇÃO DE POUSO ---
print("Estado inicial:")
print(f"  Fila:       {[m[0] for m in autorizacaoPouso]}")
print(f"  Em órbita:  {[m[0] for m in esperaOrbita]}")
print()

print("Processando fila de autorização:")
pendentes = []
while autorizacaoPouso:
    modulo = fila_dequeue(autorizacaoPouso)            # FIFO
    C = 1 if modulo[5] >= 15 else 0                    # combustível mínimo
    decisao = autorizar_pouso(C=C, A=1, P=1, H=1, S1=1, S2=1, Kb=1, KB=1, E=0)

    if decisao == "ABORT":
        fila_enqueue(emergencia, modulo)
        print(f"  [ABORT] {modulo[0]}")
    elif decisao == "OK":
        pilha_push(historicoPouso, modulo)             # LIFO
        print(f"  [OK]    {modulo[0]}")
    else:
        pendentes.append(modulo)
        print(f"  [HOLD]  {modulo[0]}")

autorizacaoPouso.extend(pendentes)                     # devolve os HOLD à fila
print("=" * 60)

# --- RESUMO ---
print("RESUMO DA MISSÃO:")
print(f"  Pousos concluídos: {len(historicoPouso)} -> {[m[0] for m in historicoPouso]}")
print(f"  Em emergência:     {len(emergencia)}")
print(f"  Em órbita:         {len(esperaOrbita)}")
if historicoPouso:
    print(f"  Topo da pilha (último a pousar): {historicoPouso[-1][0]}")
