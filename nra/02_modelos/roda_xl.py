# -*- coding: utf-8 -*-
"""X-Learner XGB e X-Learner RF, como em Exécution/execution_XL.ipynb (célula 2)."""
from comum import COV, treino, teste, grava
from xgboost import XGBClassifier, XGBRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from causalml.inference.meta import BaseXClassifier

# entradas, como nas linhas 175-180 do caderno
X_train = treino[COV]
treatment_train = treino['T']
y_train = treino['Y']
X_test = teste[COV]

#X Learner (XGB)  -- linhas 205-214 do caderno
x_learner = BaseXClassifier(treatment_outcome_learner=XGBClassifier(random_state=42), 
                        treatment_effect_learner=XGBRegressor(random_state=42),
                        control_outcome_learner=XGBClassifier(random_state=42),
                        control_effect_learner=XGBRegressor(random_state=42),
                        control_name=0)
x_learner.fit(X_train, treatment_train, y_train)
uplift_S_learner_XGB = x_learner.predict(X_test)
grava("X-Learner XGB", uplift_S_learner_XGB)

#X learner (RandomForest)  -- linhas 226-236 do caderno
x_learner = BaseXClassifier(
treatment_outcome_learner=RandomForestClassifier(random_state=42),
treatment_effect_learner=RandomForestRegressor(random_state=42),
control_outcome_learner=RandomForestClassifier(random_state=42),
control_effect_learner=RandomForestRegressor(random_state=42),
control_name=0)
x_learner.fit(X_train, treatment_train, y_train)
uplift_T_learner_XGB = x_learner.predict(X_test)
grava("X-Learner RF", uplift_T_learner_XGB)
