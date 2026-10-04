# Hiperparâmetros: origem, valores usados e experimento cruzado

Texto de apoio para a seção de metodologia do TCC. Cada afirmação traz a fonte.

## 1. Origem dos hiperparâmetros nos dois artigos

**Nenhum dos dois artigos relata como os hiperparâmetros foram escolhidos, e nenhum dos dois
repositórios contém procedimento de ajuste** (busca em grade, validação cruzada ou equivalente).
Os valores estão fixados diretamente no código, sem comentário que os justifique.

**LBCF (Ai et al., 2022).**
- No texto, "hyperparameter" aparece duas vezes, nenhuma sobre os modelos: o DGB *"requires no
  additional hyperparameter tuning"* (p. 2311), e o *"uncertainty weight hyperparameter"*, que
  controla o ruído na geração dos dados sintéticos (p. 2316).
- Não há menção a profundidade das árvores, número de árvores, regularização ou validação
  cruzada.
- No código, os valores do Chi, ED e CTS são **idênticos no experimento sintético**
  (`Code/Model/Chi_ED_CTS/Chi_ED_CTS.py`) **e no de dados reais**
  (`Chi_ED_CTS_train_and_predict-RCT.py`): não foram reajustados por base, ao menos não de forma
  registrada.
- Os do UDCF e do MBCF vêm da função `ForestTestUtilities::default_options`
  (`src/utilities/ForestTestUtilities.cpp`, linhas 29–47), um utilitário de testes do código-base
  do GRF usado pelos autores como configuração.

**NRA (Le Boudec et al., 2026).**
- No texto, "hyperparameter" não aparece. "Parameter" aparece apenas para o contraste e a
  complexidade dos dados sintéticos (p. 5).
- No código, os valores das florestas estão fixados nos cadernos de `Exécution/`; nos
  meta-learners, os modelos internos usam os padrões das bibliotecas, apenas com
  `random_state = 42`.
- O histórico do repositório (outubro a dezembro de 2024) não contém script de ajuste.

**Contraste.** Zhao, Fang & Simchi-Levi (2017), de onde vem a métrica, descrevem o ajuste no
apêndice: por exemplo, o `min_split` do CTS escolhido por validação cruzada de 5 dobras,
avaliada pela própria *expected outcome*.

**Ressalva.** A ausência de registro não prova que os autores não tenham testado valores; prova
apenas que o processo não está documentado no texto nem no código.

**Decisão deste trabalho.** Usam-se os valores publicados, sem ajuste, para preservar a
fidelidade aos protocolos originais.

## 2. Valores usados em cada modelo

Versões: CausalML 0.17.0, XGBoost 3.4.1, scikit-learn 1.9.0; UDCF e MBCF compilados do
código-fonte dos autores. Em *itálico*, valores que não estão escritos no código dos autores e
vêm do padrão da biblioteca.

### Parte LBCF

| modelo | hiperparâmetros | fonte |
|---|---|---|
| **UDCF** | 300 árvores, `sample_fraction` 0,5, `mtry` 3, `min_node_size` 50, honestidade (fração 0,5, com poda), `alpha` 0,05, **`imbalance_penalty` 0**, `stabilize_splits` = true, semente 42 | `default_options(true,1)` com `imbalance_penalty` trocado (DIVERGENCIAS L3) |
| **UDCF default** | idem, **`imbalance_penalty` 0,01** | `default_options(true,1)`, valores dos autores |
| **Ablação** | idem ao UDCF, `imbalance_penalty` 0, **`stabilize_splits` = false** | DIVERGENCIAS L4 |
| **MBCF** | uma floresta instrumental por braço, `reduced_form_weight` 0, `stabilize_splits` = false, opções de `default_options(true,1)` (inclui `imbalance_penalty` 0,01), semente 42 | `MBCF_RCT/core/main.cpp` dos autores |
| **Chi, ED, CTS** | `n_estimators` 300, `max_depth` 5, `min_samples_leaf` 100, `min_samples_treatment` 50, `n_reg` 100, `normalization` = True, `n_jobs` 1, *`max_features` 10*, `random_state` 42 | `Chi_ED_CTS_train_and_predict-RCT.py:12-14`; semente acrescentada (DIVERGENCIAS L5) |

### Parte NRA

| modelo | hiperparâmetros | fonte |
|---|---|---|
| **ED, Chi** | `n_estimators` 50, `max_depth` 50, `random_state` 42; *`min_samples_leaf` 100, `min_samples_treatment` 10, `n_reg` 10, `normalization` = True, `max_features` 10, `n_jobs` −1* | `execution_chi_ed.ipynb` (Chi comentado no original, DIVERGENCIAS N1) |
| **CTS** | `n_estimators` 70, `max_depth` 70, `random_state` 42; demais *como acima* | `execution_cts.ipynb` |
| **S-Learner XGB, T-Learner XGB** | `XGBClassifier(random_state=42)`; *`n_estimators` 100, `max_depth` 6, `learning_rate` 0,3* | `execution_xgb.ipynb`; classes `S_Learner`/`T_Learner` de `modèles.py` |
| **X-Learner XGB** | `BaseXClassifier` com `XGBClassifier`/`XGBRegressor(random_state=42)` nos quatro aprendizes; *propensão estimada internamente pela CausalML (`ElasticNetPropensityModel`)* | `execution_XL.ipynb` |
| **X-Learner RF** | idem, com `RandomForestClassifier`/`RandomForestRegressor(random_state=42)`; *`n_estimators` 100, `max_depth` sem limite, `min_samples_leaf` 1* | `execution_XL.ipynb` |

### Chi, ED e CTS nas duas configurações, lado a lado

| | LBCF | NRA |
|---|---|---|
| `max_depth` | 5 | 50 (Chi, ED) / 70 (CTS) |
| `n_estimators` | 300 | 50 / 70 |
| `n_reg` | 100 | 10 |
| `min_samples_treatment` | 50 | 10 |
| `min_samples_leaf` | 100 | 100 |
| `normalization` | True | True |

## 3. Experimento cruzado

Chi, ED e CTS são os únicos métodos presentes nos dois repositórios, com a mesma
implementação (`UpliftRandomForestClassifier`, CausalML) e hiperparâmetros diferentes. Para
separar o efeito dos hiperparâmetros do efeito de cada pipeline, rodaram-se:

1. com os hiperparâmetros do LBCF, pelo script dos autores do LBCF (parte LBCF);
2. com os hiperparâmetros do NRA, pelo pipeline dos autores do NRA (parte NRA);
3. **com os hiperparâmetros do LBCF, pelo pipeline do NRA** (experimento X4).

Os três usam os mesmos treino e teste, a mesma semente (42) e a mesma métrica.

| critério | hiper. LBCF, script LBCF | hiper. LBCF, pipeline NRA | diferença das previsões | hiper. NRA, pipeline NRA | LBCF − NRA | z pareado |
|---|---|---|---|---|---|---|
| Chi | 1,283 % | 1,283 % | 0 (idênticas) | 1,110 % | +0,172 pp | +1,72 |
| ED | 1,345 % | 1,345 % | 0 (idênticas) | 1,063 % | +0,282 pp | +2,66 |
| CTS | 1,235 % | 1,235 % | 0 (idênticas) | 1,079 % | +0,157 pp | +1,51 |

**Leitura.**
- Com os mesmos hiperparâmetros, os dois pipelines produzem previsões **idênticas**. A
  diferença entre as partes LBCF e NRA nesses três métodos deve-se, portanto,
  **exclusivamente aos hiperparâmetros**.
- A configuração do LBCF é melhor nos três critérios. A diferença é significativa no ED
  (z = 2,66, acima também do limite de Bonferroni para três comparações, ≈ 2,39) e não
  significativa no Chi e no CTS.
- **Mecanismo:** com árvores de profundidade 50–70 e pouca regularização, as estimativas
  por folha refletem ruído; as políticas mudam a recomendação de 36–42 % dos clientes e se
  afastam do melhor tratamento único (Mens E-Mail). Com profundidade 5 e `n_reg` 100, as
  estimativas são puxadas para a média e a política fica perto da referência.
- **Alcance:** o resultado vale para estas duas configurações nesta base; não é um juízo
  sobre os métodos. Como os quatro hiperparâmetros mudam juntos, não se identificou qual
  deles responde pela diferença.

**Reprodução:** `nra/04_experimento_hiper_lbcf/roda.py` (execução) e `compara.py` (tabela),
resultado em `resultados/nra/experimento_hiper_lbcf/comparacao.md`.
