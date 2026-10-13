# Exercício Computacional para P2 (2 Questao) - Capítulo 6

def mva_exato(demandas, n_query, n_update):
    # demandas[i] = [Query, Update] no dispositivo i
    estados = {}
    for q in range(n_query + 1):
        for u in range(n_update + 1):
            if q == 0 and u == 0:
                estados[(0, 0)] = [[0.0, 0.0] for _ in range(3)]
                continue

            R = [0.0, 0.0]
            X = [0.0, 0.0]
            for c in range(2):
                qtd = [q, u][c]
                if qtd > 0:
                    ant = estados[(q - 1, u)] if c == 0 else estados[(q, u - 1)]
                    for i in range(3):
                        R[c] += demandas[i][c] * (1 + ant[i][0] + ant[i][1])
                    X[c] = qtd / R[c]

            fila = [[0.0, 0.0] for _ in range(3)]
            for i in range(3):
                for c in range(2):
                    qtd = [q, u][c]
                    if qtd > 0:
                        ant = estados[(q - 1, u)] if c == 0 else estados[(q, u - 1)]
                        fila[i][c] = X[c] * demandas[i][c] * (1 + ant[i][0] + ant[i][1])
            estados[(q, u)] = fila

    return R, X, estados[(n_query, n_update)]


def mostrar(titulo, demandas):
    R, X, fila = mva_exato(demandas, 3, 1)
    print(titulo)
    print(f"Tempo de resposta Query: {R[0]:.4f} s")
    print(f"Tempo de resposta Update: {R[1]:.4f} s")
    print(f"Vazão Query: {X[0]:.4f} trans/s")
    print(f"Vazão Update: {X[1]:.4f} trans/s")
    print("Tamanho médio das filas:")
    for nome, f in zip(["CPU", "Disco 1", "Disco 2"], fila):
        print(f"  {nome}: {f[0] + f[1]:.4f}")
    print()


# [Query, Update] em CPU, Disco 1 e Disco 2
atual = [[0.105, 0.375], [0.180, 0.480], [0.000, 0.240]]
balanceado = [[0.105, 0.375], [0.090, 0.480], [0.090, 0.240]]

mostrar("=== SITUAÇÃO ATUAL ===", atual)
mostrar("=== QUERY BALANCEADA ENTRE OS DISCOS ===", balanceado)