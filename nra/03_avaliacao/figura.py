# -*- coding: utf-8 -*-
"""Figura da avaliação, no formato de Zhao, Fang & Simchi-Levi (2017):
(a) barras da resposta esperada, políticas de tratamento único em cinza e modelos em cor
    (como as Figs. 3 e 4 do artigo), com o intervalo de confiança de 95 %;
(b) curva de uplift modificada (como as Figs. 2 e 5), com a política de tratamento único de
    maior resposta esperada como linha de referência (como a Fig. 1).
Uso: python figura.py <lbcf|nra>
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MultipleLocator
import pandas as pd

PARTE = sys.argv[1] if len(sys.argv) > 1 else "nra"
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
RES = os.path.join(R, "resultados", PARTE)
tab = pd.read_csv(os.path.join(RES, "avaliacao.csv"))
cur = pd.read_csv(os.path.join(RES, "curvas.csv"))

if PARTE == "lbcf":
    MODELOS = ["UDCF", "UDCF default", "UDCF sem intra-split", "MBCF", "Chi", "ED", "CTS"]
    TITULO = "Modelos de Ai et al. (2022)"
    SAIDA = "avaliacao_lbcf.png"
else:
    MODELOS = ["X-Learner RF", "X-Learner XGB", "S-Learner XGB", "T-Learner XGB", "Chi", "ED", "CTS"]
    TITULO = "Modelos do benchmark de Le Boudec et al. (2026)"
    SAIDA = "avaliacao_nra.png"
NOME = {"Nenhum e-mail": "Nenhum envio\n(todos)", "Womens para todos": "E-mail feminino\n(todos)",
        "Mens para todos": "E-mail masculino\n(todos)"}
ROTULO = lambda m: NOME.get(m, m.replace("-Learner", "-learner"))

SURF, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
CINZA = "#c3c2b7"
COR = dict(zip(MODELOS, ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7"]))
virgula = FuncFormatter(lambda v, _: f"{v:.1f}".replace(".", ","))
virgula2 = FuncFormatter(lambda v, _: f"{v:.2f}".replace(".", ","))


def limpa(ax):
    ax.set_facecolor(SURF)
    ax.grid(True, axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(AXIS)
    ax.tick_params(colors=MUTED, labelsize=8.5)


fig, (a, b) = plt.subplots(1, 2, figsize=(13.5, 5.6), facecolor=SURF,
                           gridspec_kw={"width_ratios": [1.15, 1]})

# (a) barras da resposta esperada
ordem = ["Nenhum e-mail", "Womens para todos", "Mens para todos"] + MODELOS
for i, nome in enumerate(ordem):
    r = tab[tab.modelo == nome].iloc[0]
    cor = COR.get(nome, CINZA)
    a.bar(i, r.resposta_esperada, width=0.62, color=cor, zorder=2)
    a.plot([i, i], [r.ic_inf, r.ic_sup], color=INK2, lw=1.1, zorder=3)
    a.plot([i - 0.12, i + 0.12], [r.ic_inf] * 2, color=INK2, lw=1.1, zorder=3)
    a.plot([i - 0.12, i + 0.12], [r.ic_sup] * 2, color=INK2, lw=1.1, zorder=3)
    a.text(i, r.ic_sup + 0.03, f"{r.resposta_esperada:.3f}".replace(".", ","),
           ha="center", va="bottom", fontsize=7.8, color=INK)
a.set_xticks(range(len(ordem)))
a.set_xticklabels([ROTULO(m) for m in ordem], rotation=45, ha="right", fontsize=8.3, color=INK2)
a.set_ylim(0, 2.0)
a.yaxis.set_major_locator(MultipleLocator(0.2))
a.yaxis.set_major_formatter(virgula)
limpa(a)
a.set_ylabel("resposta esperada (%)", fontsize=9, color=INK2)
a.set_title("(a) Resposta esperada, com intervalo de confiança de 95%", loc="left",
            fontsize=10.5, color=INK)

# (b) curvas de uplift modificadas
mens = tab.loc[tab.modelo == "Mens para todos", "resposta_esperada"].item()
for nome in MODELOS:
    b.plot(cur.fracao_tratada, cur[nome], color=COR[nome], lw=1.7, label=ROTULO(nome))
b.axhline(mens, color=MUTED, lw=1.2, ls=(0, (1, 2.5)), label="E-mail masculino (todos)")
limpa(b)
b.grid(True, axis="x", color=GRID, lw=0.6)
b.set_xlim(0, 1)
b.xaxis.set_major_formatter(virgula)
b.yaxis.set_major_formatter(virgula2)
b.set_xlabel("fração da população tratada", fontsize=9, color=INK2)
b.set_ylabel("resposta esperada (%)", fontsize=9, color=INK2)
b.set_title("(b) Curva de uplift modificada", loc="left", fontsize=10.5, color=INK)
b.legend(frameon=False, fontsize=8.3, labelcolor=INK2, loc="lower right", ncol=2)

fig.suptitle(f"{TITULO}: desfecho conversão, conjunto de teste (n = 19.200)",
             x=0.008, ha="left", fontsize=12, color=INK)
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(os.path.join(RES, SAIDA), dpi=200, facecolor=SURF)
print("gravado:", os.path.join("resultados", PARTE, SAIDA))
