# -*- coding: utf-8 -*-
"""Prepara a Hillstrom nos formatos de entrada do código dos autores do LBCF.

Formatos copiados dos arquivos publicados em upstream/lbcf/Data/RCT_data/
(ver PROTOCOLO_LBCF.md, seção 3):

  rct_training.csv / rct_test.csv   CSV com cabeçalho: covariáveis, label, exp_group
                                    -> Chi, ED, CTS
  train_data_UDCF.csv               sem cabeçalho, separado por espaço:
                                    covariáveis, desfecho, uma coluna 0/1 por tratamento
                                    -> UDCF (treino)
  test_data_UDCF.csv                covariáveis, desfecho, exp_group -> UDCF (previsão)
  MBCF_train_k.csv                  só controle + braço k: covariáveis, desfecho, 0/1
                                    -> MBCF (treino), k = 1, 2
  test_data_MBCF.csv                igual a test_data_UDCF.csv -> MBCF (previsão)

Tratamento: 0 = No E-Mail, 1 = Mens E-Mail, 2 = Womens E-Mail.
Desfecho: conversion.
Divisão 70/30, estratificada por tratamento x desfecho, semente 42 (DIVERGENCIAS L1).
"""
import io
import os
import urllib.request

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(AQUI, "..", "..", "dados", "lbcf")
URL = ("http://www.minethatdata.com/"
       "Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv")
SEMENTE = 42
FRACAO_TESTE = 0.30
DESFECHO = "conversion"

os.makedirs(DADOS, exist_ok=True)
with urllib.request.urlopen(URL, timeout=180) as r:
    bruto = pd.read_csv(io.BytesIO(r.read()))
print(f"base: {len(bruto):,} linhas")

# covariáveis: as numéricas e binárias como estão; zip_code e channel em colunas 0/1.
# history_segment fica de fora: é a própria history agrupada em faixas.
X = bruto[["recency", "history", "mens", "womens", "newbie"]].astype(float)
X = pd.concat([X,
               pd.get_dummies(bruto["zip_code"], prefix="zip", dtype=float),
               pd.get_dummies(bruto["channel"], prefix="channel", dtype=float)], axis=1)
COV = list(X.columns)

d = X.copy()
d["exp_group"] = bruto["segment"].map(
    {"No E-Mail": 0, "Mens E-Mail": 1, "Womens E-Mail": 2}).astype(int)
d["label"] = bruto[DESFECHO].astype(int)
assert d["exp_group"].notna().all()

estratos = d["exp_group"].astype(str) + "_" + d["label"].astype(str)
treino, teste = train_test_split(d, test_size=FRACAO_TESTE, random_state=SEMENTE,
                                 stratify=estratos)
treino = treino.reset_index(drop=True)
teste = teste.reset_index(drop=True)


def grava(df, nome, **kw):
    df.to_csv(os.path.join(DADOS, nome), index=False, **kw)


# Chi, ED, CTS
grava(treino[COV + ["label", "exp_group"]], "rct_training.csv")
grava(teste[COV + ["label", "exp_group"]], "rct_test.csv")

# UDCF
u = treino[COV + ["label"]].copy()
u["T1"] = (treino["exp_group"] == 1).astype(int)
u["T2"] = (treino["exp_group"] == 2).astype(int)
grava(u, "train_data_UDCF.csv", header=False, sep=" ")
grava(teste[COV + ["label", "exp_group"]], "test_data_UDCF.csv", header=False, sep=" ")

# MBCF: um arquivo por braço, só controle + aquele braço
for k in (1, 2):
    m = treino[treino["exp_group"].isin([0, k])]
    m = m[COV + ["label"]].assign(T=(m["exp_group"] == k).astype(int))
    grava(m, f"MBCF_train_{k}.csv", header=False, sep=" ")
grava(teste[COV + ["label", "exp_group"]], "test_data_MBCF.csv", header=False, sep=" ")

print(f"covariáveis ({len(COV)}): {COV}")
print(f"índices: desfecho = {len(COV)}, tratamentos UDCF = {{{len(COV)}+1, {len(COV)}+2}}, "
      f"tratamento MBCF = {len(COV)}+1")
for nome, parte in (("treino", treino), ("teste", teste)):
    print(f"{nome}: {len(parte):,} linhas")
    for k, rot in ((0, "No E-Mail"), (1, "Mens"), (2, "Womens")):
        s = parte[parte["exp_group"] == k]
        print(f"   {k} {rot:<9} n={len(s):>6,}  {DESFECHO}={100 * s['label'].mean():.3f}%")
print(f"gravado em {os.path.normpath(DADOS)}")
