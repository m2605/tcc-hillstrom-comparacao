# -*- coding: utf-8 -*-
"""ED e Chi, como em Exécution/execution_chi_ed.ipynb (célula 2). Chi: linhas 220-221,
comentadas no original, descomentadas aqui (DIVERGENCIAS N1)."""
from comum import COV, treino, teste, grava
from causalml.inference.tree import UpliftRandomForestClassifier

# entradas, como nas linhas 175-180 e 202 do caderno
X_train = treino[COV]
treatment_train = treino['T']
y_train = treino['Y']
X_test = teste[COV]
treatment_train = treatment_train.astype(str)

# ED  -- linhas 206-209 do caderno
ED = UpliftRandomForestClassifier(control_name='0', n_estimators=50,max_depth=50,random_state=42,evaluationFunction = 'ED')
ED.fit(X=X_train.values, treatment=treatment_train.values, y=y_train.values)
uplift_S_learner_XGB = ED.predict(X=X_test.values)
grava("ED", uplift_S_learner_XGB)

# Chi  -- linhas 220-221 do caderno, descomentadas; previsão como a do ED (linha 209)
Chi = UpliftRandomForestClassifier(control_name='0', n_estimators=50,max_depth=50,random_state=42,evaluationFunction = 'Chi')
Chi.fit(X=X_train.values, treatment=treatment_train.values, y=y_train.values)
uplift_Chi = Chi.predict(X=X_test.values)
grava("Chi", uplift_Chi)
