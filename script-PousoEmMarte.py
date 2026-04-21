# Definimos os dados de cada módulo

energia = [1, "Vital", 8500, 95, "08:00"]
habitacao = [2, "Vital", 12000, 90, "8:30"]
suporteMedico = [3, "Alta", 5000, 85, "8:15"]
logistica = [4, "Alta", 15000, 80, "9:00"]
laboratorio = [5, "Médio", 7200, 92, "10:00"]

modulos = [energia, habitacao, suporteMedico, logistica, laboratorio]

def insertionSort(combustivel):
    for c in combustivel:
        combustivel = c[3]
        n = len(combustivel)
        
        if n <= 1:
            return
        for i in range(1, n):
            key = combustivel[i]         
            j = i - 1
            while j >= 0 and key < combustivel[j]: 
                combustivel[j + 1] = combustivel[j]
                j -= 1
            combustivel[j + 1] = key
            print(combustivel)   

insertionSort(modulos)
print(modulos)





'''
menorCombustivel = modulos[0]

for c in modulos[1:]:
    combustivel = c[3]
    if combustivel <= menorCombustivel[3]:
        menorCombustivel = c

print(str(menorCombustivel[0]) + " " + str(menorCombustivel[3]))


def binary_search(arr, x):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = low + (high - low) // 2

        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid - 1
        else:
            return mid
    return -1

# Criamos uma estrutura de dados para saber em que estado cada módulo está atualmente

autorizacaoPouso = [energia, habitacao, suporteMedico]
esperaOrbita = [logistica, laboratorio]
emergencia = []

'''
