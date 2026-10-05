# -*- coding: utf-8 -*-
"""Compara Chi, ED e CTS nas duas configurações de hiperparâmetros (DIVERGENCIAS X4).

Para cada critério:
  - configuração LBCF pelo script dos autores do LBCF  (resultados/lbcf/predicoes)
  - configuração LBCF pelo pipeline do NRA             (resultados/nra/experimento_hiper_lbcf)
  - configuração NRA pelo pipeline do NRA              (resultados/nra/predicoes)

Valor da política: expected_outcome do código do NRA (conferida contra a média das
contribuições individuais, Eq. 2.3 de Zhao et al., 2017). Grava
resultados/nra/experimento_hiper_lbcf/comparacao.md.
"""
import importlib
import os
import sys
import warnings

warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, os.path.join(R, "upstream", "nra", "dependances"))
ava = importlib.import_module("évaluation")

teste = pd.read_csv(os.path.join(R, "dados", "lbcf", "rct_test.csv"))
t = teste["exp_group"].to_numpy()
y = teste["label"].to_numpy(dtype=float)
n = len(teste)
p = teste["exp_group"].value_counts(normalize=True).to_dict()


def contribuicoes(pol):
    casa = pol == t
    z = np.zeros(n)
    z[casa] = y[casa] / np.array([p[k] for k in t[casa]])
    return z


def valor(pol):
    eo = ava.expected_outcome(teste, "exp_group", "label", list(pol))
    assert abs(contribuicoes(pol).mean() - eo) < 1e-12
    return eo


linhas = []
for crit in ("Chi", "ED", "CTS"):
    u_lbcf = pd.read_csv(os.path.join(R, "resultados", "lbcf", "predicoes", f"{crit}.csv"),
                         index_col=0)[["1", "2"]].to_numpy()
    u_cruz = pd.read_csv(os.path.join(R, "resultados", "nra", "experimento_hiper_lbcf",
                                      f"{crit}.csv"))[["1", "2"]].to_numpy()
    u_nra = pd.read_csv(os.path.join(R, "resultados", "nra", "predicoes",
                                     f"{crit}.csv"))[["1", "2"]].to_numpy()
    pol_lbcf, pol_cruz, pol_nra = (ava.uplift_to_policy(u) for u in (u_lbcf, u_cruz, u_nra))
    linhas.append(dict(
        crit=crit,
        lbcf=100 * valor(pol_lbcf), cruz=100 * valor(pol_cruz), nra=100 * valor(pol_nra),
        dif_pipeline=np.abs(u_lbcf - u_cruz).max()))

out = os.path.join(R, "resultados", "nra", "experimento_hiper_lbcf", "comparacao.md")
with open(out, "w", encoding="utf-8") as f:
    f.write("Desfecho `conversion`, conjunto de teste (n = 19.200). Resposta esperada pela "
            "`expected_outcome` do código do NRA.\n\n")
    f.write("| critério | hiper. LBCF, script LBCF | hiper. LBCF, pipeline NRA | "
            "dif. máx. das previsões | hiper. NRA, pipeline NRA |\n|---|---|---|---|---|\n")
    for r in linhas:
        dif = "0 (idênticas)" if r["dif_pipeline"] == 0 else f"{r['dif_pipeline']:.0e}"
        f.write(f"| {r['crit']} | {r['lbcf']:.3f} % | {r['cruz']:.3f} % | {dif} | "
                f"{r['nra']:.3f} % |\n")
print(open(out, encoding="utf-8").read())
