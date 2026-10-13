# Exercício Computacional para P2 (3ª Questão) - Capítulo 6

import io
from contextlib import redirect_stdout
from line_solver import *
import pandas as pd
import matplotlib.pyplot as plt

# Demandas de serviço (s) em CPU, D1 e D2 (Tabela 6.12)
demandas = {'Q': (0.06, 0.030, 0.06),
            'U': (0.10, 0.030, 0.09),
            'I': (0.09, 0.045, 0.00)}


def montar_modelo(lamQ=3.0, lamU=1.5, terminais=50, Z=15.0, vel_cpu=1.0, vel_d1=1.0):
    modelo = Network('Questao3')

    fonte = Source(modelo, 'Source')
    cpu = Queue(modelo, 'CPU', SchedStrategy.PS)
    d1 = Queue(modelo, 'D1', SchedStrategy.PS)
    d2 = Queue(modelo, 'D2', SchedStrategy.PS)
    think = Delay(modelo, 'Think')
    saida = Sink(modelo, 'Sink')

    # Q e U são abertas, I (terminais) é fechada
    Q = OpenClass(modelo, 'Q')
    U = OpenClass(modelo, 'U')
    I = ClosedClass(modelo, 'I', terminais, think, 0)

    fonte.setArrival(Q, Exp(lamQ))
    fonte.setArrival(U, Exp(lamU))

    for classe, nome in [(Q, 'Q'), (U, 'U'), (I, 'I')]:
        d_cpu, d_d1, d_d2 = demandas[nome]
        cpu.setService(classe, Exp.fitMean(d_cpu / vel_cpu))
        d1.setService(classe, Exp.fitMean(d_d1 / vel_d1))
        if d_d2 > 0:
            d2.setService(classe, Exp.fitMean(d_d2))
    think.setService(I, Exp.fitMean(Z))

    rotas = modelo.initRoutingMatrix()
    for classe in (Q, U):
        rotas.set(classe, classe, fonte, cpu, 1.0)
        rotas.set(classe, classe, cpu, d1, 1.0)
        rotas.set(classe, classe, d1, d2, 1.0)
        rotas.set(classe, classe, d2, saida, 1.0)
    rotas.set(I, I, think, cpu, 1.0)
    rotas.set(I, I, cpu, d1, 1.0)
    rotas.set(I, I, d1, think, 1.0)
    modelo.link(rotas)

    return modelo


def tempo_resposta(modelo):
    # redirect só para o LINE não encher o terminal de mensagens
    with redirect_stdout(io.StringIO()):
        tabela = MVA(modelo).getAvgTable()
    tabela = tabela[~tabela['Station'].isin(['Source', 'Think'])]
    return tabela.groupby('JobClass')['RespT'].sum()


# (a) Cenário base
base = tempo_resposta(montar_modelo())
print("(a) Cenário base")
print(base.round(4).to_string())
print()

# (b) Chegadas de Q aumentam 95%
lamQ_novo = 3.0 * 1.95
cen_b = tempo_resposta(montar_modelo(lamQ=lamQ_novo))
print("(b) Chegadas de Q +95%")
print(cen_b.round(4).to_string())
print()
print("(b) Aumento do tempo de resposta (%)")
print(((cen_b / base - 1) * 100).round(1).to_string())
print()

# (c) Upgrades (com a carga maior de Q)
cen_d1 = tempo_resposta(montar_modelo(lamQ=lamQ_novo, vel_d1=2.0))
cen_cpu = tempo_resposta(montar_modelo(lamQ=lamQ_novo, vel_cpu=2.0))
print("(c) D1 2x mais rápido")
print(cen_d1.round(4).to_string())
print()
print("(c) CPU 2x mais rápida")
print(cen_cpu.round(4).to_string())
print()
print("(c) Redução do tempo de resposta em relação ao cenário (b) (%)")
reducao = pd.DataFrame({'D1 2x': (1 - cen_d1 / cen_b) * 100,
                        'CPU 2x': (1 - cen_cpu / cen_b) * 100})
print(reducao.round(1).to_string())
print()

# (d) CPU 2x, terminais de 50 a 250
terminais = list(range(50, 251, 5))
resp_I = []
for n in terminais:
    r = tempo_resposta(montar_modelo(lamQ=lamQ_novo, vel_cpu=2.0, terminais=n))
    resp_I.append(r['I'])

n = 250
while tempo_resposta(montar_modelo(lamQ=lamQ_novo, vel_cpu=2.0, terminais=n + 1))['I'] < 1.5:
    n += 1
print(f"(d) Máximo de terminais com R < 1,5 s: {n}")

plt.plot(terminais, resp_I, marker='o')
plt.axhline(1.5, linestyle='--', color='r', label='Limite 1,5 s')
plt.xlabel('Número de terminais')
plt.ylabel('Tempo de resposta interativo (s)')
plt.title('Tempo de resposta vs. terminais (CPU 2x, λ_Q = 5,85)')
plt.legend()
plt.grid(alpha=0.3)
plt.savefig('grafico_d.png', dpi=150)
plt.show()