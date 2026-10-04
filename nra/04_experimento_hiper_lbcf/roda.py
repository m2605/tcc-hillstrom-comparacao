# -*- coding: utf-8 -*-
"""Experimento à parte (DIVERGENCIAS X4): Chi, ED e CTS pelo pipeline do benchmark NRA
(entradas como em execution_chi_ed.ipynb / execution_cts.ipynb, linhas 175-180 e 202),
mas com os hiperparâmetros do script dos autores do LBCF
(Chi_ED_CTS_train_and_predict-RCT.py, linhas 12-14). Semente 42, como nos cadernos do NRA;
n_jobs no padrão da CausalML, como nos cadernos do NRA.

Pergunta: com os mesmos hiperparâmetros, o pipeline do NRA reproduz as previsões da parte
LBCF? Grava em resultados/nra/experimento_hiper_lbcf/ e compara."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "02_modelos"))
from comum import COV, R, treino, teste
import numpy as np
import pandas as pd
from causalml.inference.tree import UpliftRandomForestClassifier

SAIDA = os.path.join(R, "resultados", "nra", "experimento_hiper_lbcf")
os.makedirs(SAIDA, exist_ok=True)

# entradas, como nos cadernos do NRA
X_train = treino[COV]
treatment_train = treino['T'].astype(str)
y_train = treino['Y']
X_test = teste[COV]

# hiperparâmetros do LBCF (Chi_ED_CTS_train_and_predict-RCT.py:12-14)
LBCF = dict(n_estimators=300, max_depth=5, min_samples_leaf=100,
            min_samples_treatment=50, n_reg=100, normalization=True)

for crit in ("Chi", "ED", "CTS"):
    m = UpliftRandomForestClassifier(control_name='0', random_state=42,
                                     evaluationFunction=crit, **LBCF)
    m.fit(X=X_train.values, treatment=treatment_train.values, y=y_train.values)
    u = m.predict(X=X_test.values)
    pd.DataFrame(u, columns=["1", "2"]).to_csv(os.path.join(SAIDA, f"{crit}.csv"), index=False)
    ref = pd.read_csv(os.path.join(R, "resultados", "lbcf", "predicoes", f"{crit}.csv"),
                      index_col=0)[["1", "2"]].to_numpy()
    print(f"{crit:4s} diferença máxima para a parte LBCF: {np.abs(u - ref).max():.1e}", flush=True)
