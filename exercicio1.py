# Exercício Computacional para P2 (1 Questao) - Capítulo 6

# Demandas de serviço [CPU, Disco 1, Disco 2]
demandas = [
    [0.105, 0.375],  # CPU
    [0.180, 0.480],  # Disco 1
    [0.000, 0.240]   # Disco 2
]

print("=== PARTE 1: MVA Aproximado (3 Q, 1 U) ===")

n = [3, 1]
fila = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]
diferenca = 1.0
iteracoes_aprox1 = 0

while diferenca > 0.001:
    fila_antiga = [linha[:] for linha in fila]
    R = [0.0, 0.0]
    X = [0.0, 0.0]
    
    for c in range(2):
        if n[c] > 0:
            for i in range(3):
                total_f = fila_antiga[i][0] + fila_antiga[i][1]
                R[c] += demandas[i][c] * (1 + total_f - (fila_antiga[i][c] / n[c]))
            X[c] = n[c] / R[c]
    
    for i in range(3):
        for c in range(2):
            if n[c] > 0:
                total_f = fila_antiga[i][0] + fila_antiga[i][1]
                fila[i][c] = X[c] * demandas[i][c] * (1 + total_f - (fila_antiga[i][c] / n[c]))
            else:
                fila[i][c] = 0.0
                
    diferenca = 0.0
    for i in range(3):
        for c in range(2):
            diff = abs(fila[i][c] - fila_antiga[i][c])
            if diff > diferenca:
                diferenca = diff
                
    iteracoes_aprox1 += 1

print(f"Tempo de resposta Query: {R[0]:.4f} s")
print(f"Tempo de resposta Update: {R[1]:.4f} s")
print(f"Vazão Query: {X[0]:.4f} trans/s")
print(f"Vazão Update: {X[1]:.4f} trans/s")
print("Tamanho das filas nos dispositivos:")
print(f"  CPU: {fila[0][0] + fila[0][1]:.4f}")
print(f"  Disco 1: {fila[1][0] + fila[1][1]:.4f}")
print(f"  Disco 2: {fila[2][0] + fila[2][1]:.4f}")
print(f"Iterações até convergir: {iteracoes_aprox1}\n")


# Triplicando Update (3 Queries, 3 Updates)

print("=== PARTE 2A: MVA Exato (3 Q, 3 U) ===")

filas_exato = {}

for q in range(4):
    for u in range(4):
        if q == 0 and u == 0:
            filas_exato[(0, 0)] = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]
            continue
            
        R_ex = [0.0, 0.0]
        X_ex = [0.0, 0.0]
        
        for c in range(2):
            qtd = [q, u][c]
            if qtd > 0:
                prev = filas_exato[(q - 1, u)] if c == 0 else filas_exato[(q, u - 1)]
                for i in range(3):
                    R_ex[c] += demandas[i][c] * (1 + prev[i][0] + prev[i][1])
                X_ex[c] = qtd / R_ex[c]
                
        nova_fila = [[0.0, 0.0] for _ in range(3)]
        for i in range(3):
            for c in range(2):
                qtd = [q, u][c]
                if qtd > 0:
                    prev = filas_exato[(q - 1, u)] if c == 0 else filas_exato[(q, u - 1)]
                    nova_fila[i][c] = X_ex[c] * demandas[i][c] * (1 + prev[i][0] + prev[i][1])
                    
        filas_exato[(q, u)] = nova_fila

fila_exata_final = filas_exato[(3, 3)]

print(f"Tempo de resposta Query: {R_ex[0]:.4f} s")
print(f"Tempo de resposta Update: {R_ex[1]:.4f} s")
print(f"Vazão Query: {X_ex[0]:.4f} trans/s")
print(f"Vazão Update: {X_ex[1]:.4f} trans/s")
print("Tamanho das filas nos dispositivos:")
print(f"  CPU: {fila_exata_final[0][0] + fila_exata_final[0][1]:.4f}")
print(f"  Disco 1: {fila_exata_final[1][0] + fila_exata_final[1][1]:.4f}")
print(f"  Disco 2: {fila_exata_final[2][0] + fila_exata_final[2][1]:.4f}")
print(f"Total de estados calculados: {len(filas_exato)}\n")


print("=== PARTE 2B: MVA Aproximado (3 Q, 3 U) ===")

n_novos = [3, 3]
fila_ap = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]
diferenca = 1.0
iteracoes_aprox2 = 0

while diferenca > 0.001:
    fila_antiga = [linha[:] for linha in fila_ap]
    R_ap = [0.0, 0.0]
    X_ap = [0.0, 0.0]
    
    for c in range(2):
        for i in range(3):
            total_f = fila_antiga[i][0] + fila_antiga[i][1]
            R_ap[c] += demandas[i][c] * (1 + total_f - (fila_antiga[i][c] / n_novos[c]))
        X_ap[c] = n_novos[c] / R_ap[c]
        
    for i in range(3):
        for c in range(2):
            total_f = fila_antiga[i][0] + fila_antiga[i][1]
            fila_ap[i][c] = X_ap[c] * demandas[i][c] * (1 + total_f - (fila_antiga[i][c] / n_novos[c]))
            
    diferenca = 0.0
    for i in range(3):
        for c in range(2):
            diff = abs(fila_ap[i][c] - fila_antiga[i][c])
            if diff > diferenca:
                diferenca = diff
                
    iteracoes_aprox2 += 1

print(f"Tempo de resposta Query: {R_ap[0]:.4f} s")
print(f"Tempo de resposta Update: {R_ap[1]:.4f} s")
print(f"Vazão Query: {X_ap[0]:.4f} trans/s")
print(f"Vazão Update: {X_ap[1]:.4f} trans/s")
print("Tamanho das filas nos dispositivos:")
print(f"  CPU: {fila_ap[0][0] + fila_ap[0][1]:.4f}")
print(f"  Disco 1: {fila_ap[1][0] + fila_ap[1][1]:.4f}")
print(f"  Disco 2: {fila_ap[2][0] + fila_ap[2][1]:.4f}")
print(f"Iterações até convergir: {iteracoes_aprox2}\n")


print("=== COMPARAÇÃO DO ESFORÇO ===")
print(f"Estados calculados no MVA Exato: {len(filas_exato)}")
print(f"Iterações no MVA Aproximado: {iteracoes_aprox2}")