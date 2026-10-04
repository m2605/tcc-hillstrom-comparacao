# -*- coding: utf-8 -*-
"""Leitura dos dados e gravação das previsões, comum aos scripts da parte NRA.
Os modelos ficam nos scripts de cada caderno, copiados do código dos autores."""
import os
import sys
import warnings

warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, os.path.join(R, "upstream", "nra", "dependances"))
SAIDA = os.path.join(R, "resultados", "nra", "predicoes")
os.makedirs(SAIDA, exist_ok=True)

treino = pd.read_csv(os.path.join(R, "dados", "nra", "treino.csv"))
teste = pd.read_csv(os.path.join(R, "dados", "nra", "teste.csv"))
COV = [c for c in treino.columns if c not in ("T", "Y")]


def grava(nome, uplift):
    """Efeito previsto de cada tratamento contra o controle, colunas '1' (Mens), '2' (Womens)."""
    u = np.asarray(uplift, dtype=float)
    assert u.shape == (len(teste), 2) and np.isfinite(u).all(), (nome, u.shape)
    pd.DataFrame(u, columns=["1", "2"]).to_csv(os.path.join(SAIDA, f"{nome}.csv"), index=False)
    print(f"  {nome}: gravado ({u.shape[0]} x {u.shape[1]})")
