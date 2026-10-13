# Exercício Computacional para P2 (2 Questao) - Capítulo 6

taxa_query = 7368 / 1800

d_cpu_up = 0.375
d_d1_up = 0.480
d_d2_up = 0.240

def calcular(d1_query, d2_query):
    d_q = [0.105, d1_query, d2_query]
    d_u = [d_cpu_up, d_d1_up, d_d2_up]
    
    d_efetiva = []
    for i in range(3):
        u_q = taxa_query * d_q[i]
        d_efetiva.append(d_u[i] / (1 - u_q))
        
    r_update = sum(d_efetiva)
    x_update = 1 / r_update
    
    fila_u = [x_update * d_efetiva[i] for i in range(3)]
        
    r_query = 0.0
    fila_q = []
    for i in range(3):
        u_q = taxa_query * d_q[i]
        r_dev = (d_q[i] * (1 + fila_u[i])) / (1 - u_q)
        r_query += r_dev
        fila_q.append(taxa_query * r_dev)
        
    print(f"Tempo de resposta Query: {r_query:.4f} s")
    print(f"Vazão Query: {taxa_query:.4f} trans/s")
    print(f"Tempo de resposta Update: {r_update:.4f} s")
    print(f"Vazão Update: {x_update:.4f} trans/s")
    
    print("Tamanho médio das filas:")
    nomes = ["CPU", "Disco 1", "Disco 2"]
    for i in range(3):
        print(f"  {nomes[i]}: {fila_u[i] + fila_q[i]:.4f}")

print("=== SITUAÇÃO ATUAL ===")
calcular(0.180, 0.000)

print("\n=== QUERY BALANCEADA ENTRE OS DISCOS ===")
calcular(0.090, 0.090)