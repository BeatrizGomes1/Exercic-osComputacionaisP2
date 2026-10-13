
# Exercicio Computacional 1 - Capitulo 6
# Modelo de duas classes: Query e Update

demandas = [
    [0.105, 0.375],  # CPU
    [0.180, 0.480],  # Disco 1
    [0.000, 0.240]   # Disco 2
]

dispositivos = ["CPU", "Disco 1", "Disco 2"]
classes = ["Query", "Update"]


# MVA aproximado
def mva_aproximado(n_query, n_update):
    n = [n_query, n_update]

    fila = [[0.0, 0.0] for i in range(3)]
    diferenca = 1
    iteracoes = 0

    while diferenca > 0.001:
        fila_antiga = [[fila[i][j] for j in range(2)]
                       for i in range(3)]

        resposta = [0.0, 0.0]
        vazao = [0.0, 0.0]

        for c in range(2):
            if n[c] > 0:
                for i in range(3):
                    total_fila = fila_antiga[i][0] + fila_antiga[i][1]
                    resposta[c] += demandas[i][c] * (
                        1 + total_fila - fila_antiga[i][c] / n[c]
                    )

                vazao[c] = n[c] / resposta[c]

        for i in range(3):
            for c in range(2):
                fila[i][c] = vazao[c] * demandas[i][c] * (
                    1 + fila_antiga[i][0] + fila_antiga[i][1]
                    - fila_antiga[i][c] / n[c]
                ) if n[c] > 0 else 0.0

        diferenca = 0

        for i in range(3):
            for c in range(2):
                valor = abs(fila[i][c] - fila_antiga[i][c])
                if valor > diferenca:
                    diferenca = valor

        iteracoes += 1

    return resposta, vazao, fila, iteracoes


# MVA exato
def mva_exato(n_query, n_update):
    filas = {}

    resposta = [0.0, 0.0]
    vazao = [0.0, 0.0]

    for q in range(n_query + 1):
        for u in range(n_update + 1):

            if q == 0 and u == 0:
                filas[(q, u)] = [[0.0, 0.0] for i in range(3)]
                continue

            n = [q, u]
            resposta = [0.0, 0.0]
            vazao = [0.0, 0.0]

            for c in range(2):
                if n[c] > 0:
                    if c == 0:
                        fila_anterior = filas[(q - 1, u)]
                    else:
                        fila_anterior = filas[(q, u - 1)]

                    for i in range(3):
                        total_fila = (
                            fila_anterior[i][0] + fila_anterior[i][1]
                        )
                        resposta[c] += demandas[i][c] * (1 + total_fila)

                    vazao[c] = n[c] / resposta[c]

            fila_atual = [[0.0, 0.0] for i in range(3)]

            for i in range(3):
                for c in range(2):
                    if n[c] > 0:
                        if c == 0:
                            fila_anterior = filas[(q - 1, u)]
                        else:
                            fila_anterior = filas[(q, u - 1)]

                        fila_atual[i][c] = (
                            vazao[c] * demandas[i][c]
                            * (1 + fila_anterior[i][0]
                               + fila_anterior[i][1])
                        )

            filas[(q, u)] = fila_atual

    # Calcula os resultados do estado final
    fila_final = filas[(n_query, n_update)]
    resposta = [0.0, 0.0]
    vazao = [0.0, 0.0]

    for c in range(2):
        n = [n_query, n_update][c]

        if n > 0:
            if c == 0:
                fila_anterior = filas[(n_query - 1, n_update)]
            else:
                fila_anterior = filas[(n_query, n_update - 1)]

            for i in range(3):
                total_fila = (
                    fila_anterior[i][0] + fila_anterior[i][1]
                )
                resposta[c] += demandas[i][c] * (1 + total_fila)

            vazao[c] = n / resposta[c]

    return resposta, vazao, fila_final, len(filas)


# Exibe os resultados
def mostrar_resultados(titulo, resultado):
    resposta, vazao, fila, quantidade = resultado

    print("\n", titulo)
    print("-" * 45)

    for c in range(2):
        print(classes[c])
        print("Tempo de resposta:", round(resposta[c], 4), "segundos")
        print("Vazao:", round(vazao[c], 4), "transacoes/segundo")

    print("\nTamanho medio das filas:")

    for i in range(3):
        total = fila[i][0] + fila[i][1]
        print(dispositivos[i], ":", round(total, 4))

    print("Estados/iteracoes:", quantidade)


# Parte 1: MVA aproximado com os niveis originais
resultado1 = mva_aproximado(3, 1)
mostrar_resultados("MVA aproximado - niveis originais", resultado1)

# Parte 2: nivel de Update triplicado
resultado2 = mva_exato(3, 3)
mostrar_resultados("MVA exato - Update triplicado", resultado2)

resultado3 = mva_aproximado(3, 3)
mostrar_resultados("MVA aproximado - Update triplicado", resultado3)

print("\nComparacao do esforco computacional")
print("Iteracoes do aproximado:", resultado3[3])
print("Estados calculados pelo exato:", resultado2[3])
