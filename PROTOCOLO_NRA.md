# Protocolo dos autores do benchmark NRA

Levantado do artigo, do README e do código antes de qualquer execução.
Repositório: <https://github.com/Nathpreums/Uplift_Multitreatment_Benchmark_NRA>,
commit `dbbd725` (10/12/2024). Caminhos relativos à raiz desse repositório.

> Le Boudec, N., Voisine, N., Crémilleux, B. (2026). *Multi-treatment uplift evaluation on
> non-random assignment biased data.* Data & Knowledge Engineering 163, 102565.
> doi:10.1016/j.datak.2026.102565

## 1. O que o artigo faz

- Compara métodos de uplift multi-tratamento sob viés de atribuição não aleatória, em
  **dados sintéticos** (§4.4–4.5, p. 5–6).
- Treino e teste independentes. *§4.4, p. 6: "we generated test datasets independent of the
  training datasets, with 15,000 individuals per treatment group."*
- Métricas: **RMSE** (exige o uplift verdadeiro, que só existe em dado sintético) e
  **expected outcome** de Zhao et al. (§2.2, p. 2; ref. [9]).
- Métodos (§3.1, p. 3; Tabela 2, p. 9): **12 linhas** na Tabela 2.
- **O artigo não informa hiperparâmetros.** Eles só aparecem no código.

## 2. Os 12 métodos da Tabela 2 contra o código

| método (Tabela 2) | no código? | onde / observação |
|---|---|---|
| X-Learner RF | **sim** | `Exécution/execution_XL.ipynb`: `BaseXClassifier` (CausalML) com `RandomForestClassifier`/`RandomForestRegressor(random_state=42)` |
| X-Learner XGB | **sim** | idem, com `XGBClassifier`/`XGBRegressor(random_state=42)` |
| S-Learner XGB | **sim** | `execution_xgb.ipynb`: `S_Learner(xgb.XGBClassifier(random_state=42))` de `dependances/modèles.py` |
| T-Learner XGB | **sim** | idem: `T_Learner(xgb.XGBClassifier(random_state=42))` |
| ED | **sim** | `execution_chi_ed.ipynb`: `UpliftRandomForestClassifier(n_estimators=50, max_depth=50, random_state=42, evaluationFunction='ED')` |
| CTS | **sim** | `execution_cts.ipynb`: idem com `n_estimators=70, max_depth=70, evaluationFunction='CTS'` |
| **Chi** | **comentado** | `execution_chi_ed.ipynb`: as linhas do Chi existem, mas estão comentadas (`#Chi = ...`, `#Chi.fit(...)`) |
| **S-Learner LR** | **não** | nenhum caderno o executa. A classe `S_Learner` aceita qualquer classificador, mas a chamada com regressão logística não existe |
| **T-Learner LR** | **não** | idem. O caderno `execution_lr.ipynb` existe, mas o código dele é o do CTS (igual a `execution_cts.ipynb`, exceto uma linha de exclusão de arquivo) |
| **TARNet** | **não** | nenhum arquivo menciona TARNet. `modèles.py:367` tem uma `NeuralNetworkClassifier` que não é TARNet (rede de 2 camadas, sem a representação compartilhada com uma "cabeça" por tratamento descrita em §3.1.3), não é usada por nenhum caderno e, como está, não funciona: o construtor usa uma variável `model` que não existe naquele ponto |
| **R-Learner** e **DR-Learner** | **sim, com nomes trocados** | `execution_r_dr_xgb.ipynb`: `R_L = BaseDRRegressor(XGBRegressor(), control_name='0')` e `DR_L = BaseRRegressor(XGBRegressor(), control_name='0')`. A variável chamada R guarda o DR, e vice-versa. Não dá para saber, só pelo código, se as linhas R e DR da Tabela 2 saíram trocadas |

## 3. Outros pontos do código

- `modèles.py` define `S_Learner` duas vezes (linhas 92 e 147) e `T_Learner` duas vezes
  (191 e 262). As segundas estão dentro de blocos `'''` (linhas 145–189 e 260–314), ou seja,
  são texto, não código. **As versões ativas são as das linhas 92 e 191.**
- Recomendação: `get_max_index` nos cadernos e `uplift_to_policy` em `évaluation.py`
  (mesma regra: maior uplift previsto; se todos ≤ 0, controle).
- Métrica: `expected_outcome` em `dependances/évaluation.py:45`, a mesma usada na parte LBCF.
- `execution_xgb.ipynb` roda também uma `MeanPredictor` ("Baseline average"), que não está
  na Tabela 2.
- RMSE e `true_expected_outcome` dependem do uplift verdadeiro e **não se aplicam à
  Hillstrom**.

## 4. Decisões (03/10/2026)

| item | decisão |
|---|---|
| Chi | descomentar as linhas dos autores |
| S-Learner LR, T-Learner LR, R-Learner, DR-Learner | não entram |
| TARNet | não entra: sem código dos autores (ver DIVERGENCIAS N2) |

Modelos da parte NRA: X-Learner RF, X-Learner XGB, S-Learner XGB, T-Learner XGB, ED, CTS e Chi.
