# -*- coding: utf-8 -*-
"""CTS, como em Exécution/execution_cts.ipynb (célula 2)."""
from comum import COV, treino, teste, grava
from causalml.inference.tree import UpliftRandomForestClassifier

# entradas, como nas linhas 175-180 e 202 do caderno
X_train = treino[COV]
treatment_train = treino['T']
y_train = treino['Y']
X_test = teste[COV]
treatment_train = treatment_train.astype(str)

# CTS  -- linhas 206-211 do caderno
cts = UpliftRandomForestClassifier(control_name='0', n_estimators=70,max_depth=70,random_state=42,evaluationFunction = 'CTS')
cts.fit(X=X_train.values, treatment=treatment_train.values, y=y_train.values)
uplift_S_learner_XGB = cts.predict(X=X_test.values)
grava("CTS", uplift_S_learner_XGB)
