from causalml.inference.tree import UpliftRandomForestClassifier
import pandas as pd
import numpy as np
import os

# Hillstrom: caminhos a partir da raiz do repositorio
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
SAIDA = os.path.join(R, "resultados", "lbcf", "predicoes")

train = pd.read_csv(os.path.join(R, "dados", "lbcf", "rct_training.csv"))
test = pd.read_csv(os.path.join(R, "dados", "lbcf", "rct_test.csv"))
train.exp_group = train.exp_group.astype(str)
features = ['recency', 'history', 'mens', 'womens', 'newbie',
   'zip_Rural', 'zip_Surburban', 'zip_Urban',
   'channel_Multichannel', 'channel_Phone', 'channel_Web']


Chi_uplift_model = UpliftRandomForestClassifier(n_estimators=300, evaluationFunction = "Chi", 
                                        max_depth = 5,min_samples_leaf=100, 
                                        min_samples_treatment=50,n_reg=100,control_name='0', n_jobs=1,normalization=True,
                                        random_state=42)  # DIVERGENCIAS L5
Chi_uplift_model.fit(X=train[features].values, treatment=train['exp_group'].values, y=train['label'].values)
Chi_pred = Chi_uplift_model.predict(test[features].values)
Chi_test_result = pd.DataFrame(Chi_pred,columns=[c for c in Chi_uplift_model.classes_ if c != Chi_uplift_model.control_name])  # DIVERGENCIAS A3
Chi_test_result.to_csv(os.path.join(SAIDA, 'Chi.csv'))

ED_uplift_model = UpliftRandomForestClassifier(n_estimators=300, evaluationFunction = "ED", 
                                        max_depth = 5,min_samples_leaf=100, 
                                        min_samples_treatment=50,n_reg=100,control_name='0', n_jobs=1,normalization=True,
                                        random_state=42)  # DIVERGENCIAS L5
ED_uplift_model.fit(X=train[features].values, treatment=train['exp_group'].values, y=train['label'].values)
ED_pred = ED_uplift_model.predict(test[features].values)
ED_test_result = pd.DataFrame(ED_pred,columns=[c for c in ED_uplift_model.classes_ if c != ED_uplift_model.control_name])  # DIVERGENCIAS A3
ED_test_result.to_csv(os.path.join(SAIDA, 'ED.csv'))

CTS_uplift_model = UpliftRandomForestClassifier(n_estimators=300, evaluationFunction = "CTS", 
                                        max_depth = 5,min_samples_leaf=100, 
                                        min_samples_treatment=50,n_reg=100,control_name='0', n_jobs=1,normalization=True,
                                        random_state=42)  # DIVERGENCIAS L5
CTS_uplift_model.fit(X=train[features].values, treatment=train['exp_group'].values, y=train['label'].values)
CTS_pred = CTS_uplift_model.predict(test[features].values)
CTS_test_result = pd.DataFrame(CTS_pred,columns=[c for c in CTS_uplift_model.classes_ if c != CTS_uplift_model.control_name])  # DIVERGENCIAS A3
CTS_test_result.to_csv(os.path.join(SAIDA, 'CTS.csv'))
    
    
    