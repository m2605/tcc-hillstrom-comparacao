# -*- coding: utf-8 -*-
"""Dados da parte NRA: os mesmos treino e teste da parte LBCF (DIVERGENCIAS L1, N4),
com as colunas renomeadas para o formato dos cadernos do NRA: 'T' (tratamento) e 'Y'
(desfecho). Exige ter rodado antes lbcf/01_dados/prep_hillstrom.py."""
import os
import pandas as pd

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
ORIGEM = os.path.join(R, "dados", "lbcf")
DESTINO = os.path.join(R, "dados", "nra")
os.makedirs(DESTINO, exist_ok=True)
for origem, destino in (("rct_training.csv", "treino.csv"), ("rct_test.csv", "teste.csv")):
    d = pd.read_csv(os.path.join(ORIGEM, origem)).rename(columns={"exp_group": "T", "label": "Y"})
    d = d[[c for c in d.columns if c not in ("T", "Y")] + ["T", "Y"]]
    d.to_csv(os.path.join(DESTINO, destino), index=False)
    print(f"{destino}: {len(d):,} linhas, colunas {list(d.columns)}")
