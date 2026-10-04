# -*- coding: utf-8 -*-
"""S-Learner XGB e T-Learner XGB, como em Exécution/execution_xgb.ipynb (célula 2)."""
from comum import COV, treino, teste, grava
import xgboost as xgb
from modèles import S_Learner, T_Learner          # classes ativas: modèles.py linhas 92 e 191

# entradas, como nas linhas 131-139 do caderno
X_train = treino[COV + ["T"]]
X_train_t = treino[COV + ["T", "Y"]]
X_test = teste[COV + ["T"]]
y_train = treino[["Y"]]

#S learner (XGB)  -- linhas 173-175 do caderno
s_learner_model_XGB  = S_Learner(xgb.XGBClassifier(random_state=42))
s_learner_model_XGB.fit(X_train, y_train,'T')
uplift_S_learner_XGB = s_learner_model_XGB .predict_uplift(X_test)
grava("S-Learner XGB", uplift_S_learner_XGB)

#T learner (XGB)  -- linhas 185-187 do caderno
t_learner_model_XGB = T_Learner(xgb.XGBClassifier(random_state=42))
t_learner_model_XGB.fit(X_train_t,'T','Y')
uplift_T_learner_XGB = t_learner_model_XGB.predict_uplift(X_test)
grava("T-Learner XGB", uplift_T_learner_XGB)
