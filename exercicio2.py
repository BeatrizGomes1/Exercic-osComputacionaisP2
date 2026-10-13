
# Exercicio Computacional 2 - Capitulo 6

taxa_query = 7368 / 1800

demanda_cpu_query = 0.105
demanda_d1_query = 0.180
demanda_d2_query = 0.000

demanda_cpu_update = 0.375
demanda_d1_update = 0.480
demanda_d2_update = 0.240


def calcular(d1_query, d2_query):
    demandas_query = [
        demanda_cpu_query,
        d1_query,
        d2_query
    ]

    demandas_update = [
        demanda_cpu_update,
        demanda_d1_update,
        demanda_d2_update
    ]

    demanda_efetiva = []

    for i in range(3):
        utilizacao_query = taxa_query * demandas_query[i]
        demanda = demandas_update[i] / (1 - utilizacao_query)
        demanda_efetiva.append(demanda)

    resposta_update = sum(demanda_efetiva)
    vazao_update = 1 / resposta_update

    fila_update = []

    for i in range(3):
        tamanho = vazao_update * demanda_efetiva[i]
        fila_update.append(tamanho)

    resposta_query = 0.0
    fila_query = []

    for i in range(3):
        utilizacao_query = taxa_query * demandas_query[i]

        resposta_dispositivo = (
            demandas_query[i] * (1 + fila_update[i])
            / (1 - utilizacao_query)
        )

        resposta_query += resposta_dispositivo
        fila_query.append(taxa_query * resposta_dispositivo)

    print("Tempo de resposta Query:", round(resposta_query, 4), "s")
    print("Vazao Query:", round(taxa_query, 4), "trans/s")
    print("Tempo de resposta Update:", round(resposta_update, 4), "s")
    print("Vazao Update:", round(vazao_update, 4), "trans/s")

    print("Tamanho medio das filas:")

    nomes = ["CPU", "Disco 1", "Disco 2"]

    for i in range(3):
        total = fila_update[i] + fila_query[i]
        print(nomes[i], ":", round(total, 4))


print("=== SITUACAO ATUAL ===")
calcular(0.180, 0.000)

print("\n=== QUERY BALANCEADA ENTRE OS DISCOS ===")
calcular(0.090, 0.090)