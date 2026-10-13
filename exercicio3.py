
# Exercício Computacional para P2 (3ª Questão) - Capítulo 6

import io
from contextlib import redirect_stdout
from line_solver import *
import pandas as pd
import matplotlib.pyplot as plt


# Demandas de serviço (s) em CPU, D1 e D2 (Tabela 6.12)
demandas = {
    'Q': (0.06, 0.030, 0.06),
    'U': (0.10, 0.030, 0.09),
    'I': (0.09, 0.045, 0.00)
}


def montar_modelo(
    lamQ=3.0,
    lamU=1.5,
    terminais=50,
    Z=15.0,
    vel_cpu=1.0,
    vel_d1=1.0
):
    modelo = Network('Questao3')

    fonte = Source(modelo, 'Source')
    cpu = Queue(modelo, 'CPU', SchedStrategy.PS)
    d1 = Queue(modelo, 'D1', SchedStrategy.PS)
    d2 = Queue(modelo, 'D2', SchedStrategy.PS)
    think = Delay(modelo, 'Think')
    saida = Sink(modelo, 'Sink')

    # Q e U são classes abertas; I é classe fechada
    Q = OpenClass(modelo, 'Q')
    U = OpenClass(modelo, 'U')
    I = ClosedClass(modelo, 'I', terminais, think, 0)

    fonte.setArrival(Q, Exp(lamQ))
    fonte.setArrival(U, Exp(lamU))

    # Configuração dos tempos de serviço
    for classe, nome in [(Q, 'Q'), (U, 'U'), (I, 'I')]:
        d_cpu, d_d1, d_d2 = demandas[nome]

        cpu.setService(
            classe,
            Exp.fitMean(d_cpu / vel_cpu)
        )

        d1.setService(
            classe,
            Exp.fitMean(d_d1 / vel_d1)
        )

        if d_d2 > 0:
            d2.setService(
                classe,
                Exp.fitMean(d_d2)
            )

    think.setService(I, Exp.fitMean(Z))

    # Definição das rotas
    rotas = modelo.initRoutingMatrix()

    # Classes abertas: Source -> CPU -> D1 -> D2 -> Sink
    for classe in (Q, U):
        rotas.set(classe, classe, fonte, cpu, 1.0)
        rotas.set(classe, classe, cpu, d1, 1.0)
        rotas.set(classe, classe, d1, d2, 1.0)
        rotas.set(classe, classe, d2, saida, 1.0)

    # Classe fechada: Think -> CPU -> D1 -> Think
    rotas.set(I, I, think, cpu, 1.0)
    rotas.set(I, I, cpu, d1, 1.0)
    rotas.set(I, I, d1, think, 1.0)

    modelo.link(rotas)

    return modelo


def tempo_resposta(modelo):
    # Oculta mensagens do solucionador no terminal
    with redirect_stdout(io.StringIO()):
        tabela = MVA(modelo).getAvgTable()

    # Exclui Source e Think do tempo de resposta
    tabela = tabela[
        ~tabela['Station'].isin(['Source', 'Think'])
    ]

    # Soma os tempos de resposta dos dispositivos por classe
    return tabela.groupby('JobClass')['RespT'].sum()


def titulo(texto):
    print("\n" + "=" * 55)
    print(texto.center(55))
    print("=" * 55)


def mostrar_resultados(texto, resultados):
    titulo(texto)

    print(f"{'Classe':<18}{'Tempo de resposta (s)':>25}")
    print("-" * 43)

    for classe, valor in resultados.items():
        print(f"{classe:<18}{valor:>25.4f}")

    print("-" * 43)


def mostrar_percentuais(texto, resultados):
    titulo(texto)

    print(f"{'Classe':<18}{'Variação (%)':>20}")
    print("-" * 38)

    for classe, valor in resultados.items():
        print(f"{classe:<18}{valor:>20.1f}")

    print("-" * 38)


# ==========================================================
# (a) CENÁRIO BASE
# ==========================================================

base = tempo_resposta(montar_modelo())

mostrar_resultados("(a) CENÁRIO BASE", base)


# ==========================================================
# (b) AUMENTO DE 95% NA TAXA DE CHEGADA DE Q
# ==========================================================

lamQ_novo = 3.0 * 1.95

cen_b = tempo_resposta(
    montar_modelo(lamQ=lamQ_novo)
)

mostrar_resultados("(b) CHEGADAS DE Q +95%", cen_b)

aumento = ((cen_b / base - 1) * 100).round(1)

mostrar_percentuais(
    "(b) AUMENTO DO TEMPO DE RESPOSTA",
    aumento
)


# ==========================================================
# (c) COMPARAÇÃO DAS MELHORIAS DE HARDWARE
# ==========================================================

cen_d1 = tempo_resposta(
    montar_modelo(
        lamQ=lamQ_novo,
        vel_d1=2.0
    )
)

cen_cpu = tempo_resposta(
    montar_modelo(
        lamQ=lamQ_novo,
        vel_cpu=2.0
    )
)

mostrar_resultados(
    "(c) D1 DUAS VEZES MAIS RÁPIDO",
    cen_d1
)

mostrar_resultados(
    "(c) CPU DUAS VEZES MAIS RÁPIDA",
    cen_cpu
)

reducao = pd.DataFrame({
    'D1 2x': (1 - cen_d1 / cen_b) * 100,
    'CPU 2x': (1 - cen_cpu / cen_b) * 100
}).round(1)

titulo("(c) REDUÇÃO DO TEMPO DE RESPOSTA (%)")

print(
    f"{'Classe':<18}"
    f"{'D1 2x (%)':>16}"
    f"{'CPU 2x (%)':>16}"
)
print("-" * 50)

for classe, linha in reducao.iterrows():
    print(
        f"{classe:<18}"
        f"{linha['D1 2x']:>16.1f}"
        f"{linha['CPU 2x']:>16.1f}"
    )

print("-" * 50)


# ==========================================================
# (d) GRÁFICO E MÁXIMO DE TERMINAIS
# ==========================================================

terminais = list(range(50, 251, 5))
resp_I = []

for n in terminais:
    r = tempo_resposta(
        montar_modelo(
            lamQ=lamQ_novo,
            vel_cpu=2.0,
            terminais=n
        )
    )

    resp_I.append(r['I'])


# Procura o maior número de terminais com R_I < 1,5 s
n = 250

while tempo_resposta(
    montar_modelo(
        lamQ=lamQ_novo,
        vel_cpu=2.0,
        terminais=n + 1
    )
)['I'] < 1.5:
    n += 1


titulo("(d) LIMITE DE TERMINAIS")

print(f"{'Taxa de chegada de Q:':<30}{lamQ_novo:.2f} transações/s")
print(f"{'Velocidade da CPU:':<30}2x mais rápida")
print(f"{'Tempo limite:':<30}1,5 s")
print(f"{'Máximo de terminais:':<30}{n}")
print("=" * 55)


# Gráfico
plt.figure(figsize=(9, 5))

plt.plot(
    terminais,
    resp_I,
    marker='o',
    label='Tempo de resposta de I'
)

plt.axhline(
    1.5,
    linestyle='--',
    color='r',
    label='Limite de 1,5 s'
)

plt.xlabel('Número de terminais')
plt.ylabel('Tempo de resposta interativo (s)')
plt.title(
    'Tempo de resposta vs. terminais '
    '(CPU 2x, λ_Q = 5,85)'
)

plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig('grafico_d.png', dpi=150)
plt.show()
