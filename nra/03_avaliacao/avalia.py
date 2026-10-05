# -*- coding: utf-8 -*-
"""Avalia os sete modelos do benchmark NRA no conjunto de teste.

Cópia de lbcf/03_avaliacao/avalia.py: mesma métrica, mesma referência, mesmos acréscimos;
mudam só a lista de modelos e a leitura das previsões.

Origem de cada peça (ACORDOS 2):
  previsão -> recomendação   uplift_to_policy, código do NRA (dependances/évaluation.py)
  valor da política          expected_outcome, código do NRA, sem alteração
  referências                expected_outcome com política constante (Zhao et al. 2017, §4.2)
  intervalo de confiança     calculado a partir da contribuição de cada cliente (Eq. 2.3 de
                             Zhao); o Teorema 2.1 de Zhao indica que o IC pode ser obtido assim.
                             A média é conferida contra a expected_outcome do NRA
  curva de uplift modificada ACRÉSCIMO NOSSO (Zhao §4.2), conferida em pontos contra a
                             expected_outcome do NRA

Gera resultados/nra/avaliacao.csv, avaliacao.md e curvas.csv.
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
ava = importlib.import_module("évaluation")          # código do NRA, sem alteração
expected_outcome, uplift_to_policy = ava.expected_outcome, ava.uplift_to_policy

PRED = os.path.join(R, "resultados", "nra", "predicoes")
SAIDA = os.path.join(R, "resultados", "nra")
MODELOS = ["X-Learner RF", "X-Learner XGB", "S-Learner XGB", "T-Learner XGB", "Chi", "ED", "CTS"]
Z975 = 1.959963984540054

teste = pd.read_csv(os.path.join(R, "dados", "lbcf", "rct_test.csv"))   # = dados/nra/teste.csv
t = teste["exp_group"].to_numpy()
y = teste["label"].to_numpy(dtype=float)
n = len(teste)
# mesma proporção que a expected_outcome do NRA usa: value_counts(normalize=True)
p = teste["exp_group"].value_counts(normalize=True).to_dict()


def le_previsoes():
    """Matriz (n, 2): efeito previsto de Mens e de Womens contra o controle."""
    prev = {m: pd.read_csv(os.path.join(PRED, f"{m}.csv"))[["1", "2"]].to_numpy() for m in MODELOS}
    for nome, u in prev.items():
        assert u.shape == (n, 2) and np.isfinite(u).all(), nome
    return prev


def contribuicoes(politica):
    """z_i de Zhao (Eq. 2.3): y_i / p_t se a política coincide com o sorteio, senão 0."""
    politica = np.asarray(politica)
    casa = politica == t
    z = np.zeros(n)
    z[casa] = y[casa] / np.array([p[k] for k in t[casa]])
    return z


def linha(nome, tipo, politica):
    eo_nra = expected_outcome(teste, "exp_group", "label", list(politica))
    z = contribuicoes(politica)
    assert abs(z.mean() - eo_nra) < 1e-12, (nome, z.mean(), eo_nra)   # confere com o NRA
    ep = z.std(ddof=1) / np.sqrt(n)
    return dict(modelo=nome, tipo=tipo, resposta_esperada=100 * eo_nra,
                ic_inf=100 * (eo_nra - Z975 * ep), ic_sup=100 * (eo_nra + Z975 * ep))


def curva(u, pontos=101):
    """Curva de uplift modificada (Zhao §4.2): os p% com maior diferença entre o tratamento
    ótimo previsto e o controle recebem o ótimo previsto; os demais, o controle."""
    otimo = uplift_to_policy(u)
    ganho = np.where(otimo > 0, u.max(axis=1), 0.0)
    ordem = np.argsort(-ganho, kind="stable")
    z_otimo = contribuicoes(otimo)
    z_ctrl = contribuicoes(np.zeros(n, dtype=int))
    acum = np.concatenate([[0.0], np.cumsum((z_otimo - z_ctrl)[ordem])])
    fr = np.linspace(0, 1, pontos)
    k = np.round(fr * n).astype(int)
    valores = (z_ctrl.sum() + acum[k]) / n
    # conferência: três pontos recalculados com a expected_outcome do NRA
    for kk in (k[25], k[50], k[100]):
        pol = np.zeros(n, dtype=int)
        pol[ordem[:kk]] = otimo[ordem[:kk]]
        eo = expected_outcome(teste, "exp_group", "label", list(pol))
        assert abs(eo - (z_ctrl.sum() + acum[kk]) / n) < 1e-12
    return fr, valores


prev = le_previsoes()
linhas = [linha(rot, "tratamento único", np.full(n, k))
          for rot, k in (("Nenhum e-mail", 0), ("Mens para todos", 1), ("Womens para todos", 2))]
curvas = {}
for nome in MODELOS:
    linhas.append(linha(nome, "modelo", uplift_to_policy(prev[nome])))
    fr, curvas[nome] = curva(prev[nome])

tab = pd.DataFrame(linhas)
tab.to_csv(os.path.join(SAIDA, "avaliacao.csv"), index=False, float_format="%.6f")
pd.DataFrame({"fracao_tratada": fr, **{k: 100 * v for k, v in curvas.items()}}).to_csv(
    os.path.join(SAIDA, "curvas.csv"), index=False, float_format="%.6f")

with open(os.path.join(SAIDA, "avaliacao.md"), "w", encoding="utf-8") as f:
    f.write(f"Desfecho `conversion`, conjunto de teste (n = {n:,}). Resposta esperada pela "
            "`expected_outcome` do código do NRA; IC 95 % a partir das contribuições individuais "
            "(Zhao et al., 2017, Teorema 2.1).\n\n")
    f.write("| política | resposta esperada | IC 95 % |\n|---|---|---|\n")
    for r in linhas:
        f.write(f"| {r['modelo']} | {r['resposta_esperada']:.3f} % | "
                f"[{r['ic_inf']:.3f}; {r['ic_sup']:.3f}] |\n")
print(open(os.path.join(SAIDA, "avaliacao.md"), encoding="utf-8").read())
