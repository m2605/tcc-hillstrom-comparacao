# -*- coding: utf-8 -*-
"""Figura da avaliação do benchmark NRA (cópia de lbcf/03_avaliacao/figura.py) a partir de avaliacao.csv e curvas.csv (gerados por avalia.py)."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
RES = os.path.join(R, "resultados", "nra")
tab = pd.read_csv(os.path.join(RES, "avaliacao.csv"))
cur = pd.read_csv(os.path.join(RES, "curvas.csv"))

SURF, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
MODELOS = ["X-Learner RF", "X-Learner XGB", "S-Learner XGB", "T-Learner XGB", "Chi", "ED", "CTS"]
COR = dict(zip(MODELOS, ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7"]))
mens = tab.loc[tab.modelo == "Mens para todos", "resposta_esperada"].item()


def limpa(ax):
    ax.set_facecolor(SURF)
    ax.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(AXIS)
    ax.tick_params(colors=MUTED, labelsize=8.5)


fig, (a, b) = plt.subplots(1, 2, figsize=(13.5, 5.6), facecolor=SURF,
                           gridspec_kw={"width_ratios": [1, 1.25]})

# painel A: resposta esperada com IC 95 %
ordem = ["Nenhum e-mail", "Womens para todos", "Mens para todos"] + MODELOS
for i, nome in enumerate(ordem[::-1]):
    r = tab[tab.modelo == nome].iloc[0]
    cor = COR.get(nome, MUTED)
    a.plot([r.ic_inf, r.ic_sup], [i, i], color=cor, lw=2, alpha=0.5, solid_capstyle="round")
    a.plot([r.resposta_esperada], [i], "o", ms=8, color=cor, mec=SURF, mew=1.5, zorder=3)
    txt = "referência" if nome == "Mens para todos" else f"{r.vs_mens_pp:+.3f} pp (z = {r.z_pareado:+.2f})"
    if r.tipo == "modelo" or nome == "Mens para todos":
        a.annotate(txt, (r.ic_sup, i), xytext=(6, 0), textcoords="offset points",
                   va="center", fontsize=8, color=INK2)
a.axvline(mens, color=MUTED, lw=1.2, ls=(0, (1, 2.5)))
a.set_yticks(range(len(ordem)))
a.set_yticklabels(ordem[::-1], fontsize=9.5, color=INK2)
a.set_xlim(0.3, 2.05)
limpa(a)
a.set_xlabel("resposta esperada (%) · IC 95 %", fontsize=9, color=INK2)
a.set_title("Valor de cada política no teste", loc="left", fontsize=10.5, color=INK)

# painel B: curvas de uplift modificadas
for nome in MODELOS:
    b.plot(cur.fracao_tratada, cur[nome], color=COR[nome], lw=1.7, label=nome)
b.axhline(mens, color=MUTED, lw=1.2, ls=(0, (1, 2.5)), label="Mens para todos")
limpa(b)
b.set_xlim(0, 1)
b.set_xlabel("fração da população tratada (ordenada pelo efeito previsto)", fontsize=9, color=INK2)
b.set_ylabel("resposta esperada (%)", fontsize=9, color=INK2)
b.set_title("Curva de uplift modificada (Zhao et al., 2017, §4.2)", loc="left", fontsize=10.5, color=INK)
b.legend(frameon=False, fontsize=8.5, labelcolor=INK2, loc="lower right", ncol=2)

fig.suptitle("Modelos do benchmark NRA na Hillstrom — desfecho conversion, conjunto de teste (n = 19.200)",
             x=0.008, ha="left", fontsize=12.5, color=INK)
fig.text(0.008, 0.905, "Resposta esperada pela expected_outcome do código do NRA. IC 95 %, z pareado "
         "e curvas são acréscimo nosso. Modelos e hiperparâmetros do código dos autores do NRA.", fontsize=8.5, color=INK2, ha="left")
fig.tight_layout(rect=[0, 0, 1, 0.89])
fig.savefig(os.path.join(RES, "avaliacao_nra.png"), dpi=200, facecolor=SURF)
print("gravado: resultados/nra/avaliacao_nra.png")
