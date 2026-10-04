# Protocolo dos autores do LBCF

Levantado do artigo, dos READMEs e do código, antes de qualquer execução (passo 1).
Cada ponto traz a fonte. Repositório: <https://github.com/www2022paper/WWW-2022-PAPER-SUPPLEMENTARY-MATERIALS>.
Caminhos abaixo são relativos à raiz desse repositório.

> Ai, M. et al. (2022). *LBCF: A Large-Scale Budget-Constrained Causal Forest Algorithm.*
> WWW '22, pp. 2310–2319. doi:10.1145/3485447.3512103

## 1. O que o artigo propõe

- **LBCF = UDCF + DGB.** Duas etapas: (i) estimar o CATE de cada usuário com um único
  modelo; (ii) escolher o tratamento resolvendo um problema com restrição de orçamento.
  *Artigo, §4.2, p. 2314: "We break BTS problem into two steps".*
- **Sem custo e sem orçamento, a etapa (ii) não se aplica.** Neste trabalho fica só o
  estimador, a etapa (i).
- **UDCF** = floresta causal do GRF com uma nova regra de divisão em duas etapas:
  Inter split (Eq. 3) seleciona `m` candidatas e Intra split (Eq. 4) escolhe a melhor.
  *Artigo, §4.2.1, p. 2314.* *README raiz, "Implementation Details" 1: "implemented by
  directly modifying the C++ source code of GRF ... with a new splitting criterion".*
- **Baselines** (§5.1, p. 2316): ED, Chi e CTS da CausalML; CT.ST e CF.DT de Tu et al.
  *README raiz, item 3: ED/Chi/CTS "are all directly imported from CausalML package".*
  **CF.DT usa o MBCF** como estimador: *§5.3, p. 2317: "CF is actually the MBCF model".*

## 2. Como dividem os dados

- **Treino e teste separados.**
  - *Apêndice A.3, p. 2319: "RCT Data Folder contains real-world RCT data which has been
    split into training and testing."*
  - *`Data/README.md`: idem; os sintéticos vêm em arquivos Training e Test.*
- **A proporção não é informada** no artigo nem nos READMEs.
- Os dados reais publicados são uma amostra de ~2.000 linhas criptografadas, *"NOT FOR
  REPRODUCE THE RESULT"* (`README.md` raiz, §5.2; `Data/RCT_data/README.md`).

## 3. Formato dos arquivos de entrada (dados reais)

Todos sem cabeçalho, separados por espaço, exceto `rct_*.csv`.

| arquivo | colunas | usado por |
|---|---|---|
| `Data/RCT_data/rct_training.csv` / `rct_test.csv` | `c0..c13`, `label`, `exp_group` (CSV com cabeçalho) | Chi, ED, CTS |
| `Data/RCT_data/train_data_UDCF.csv` | 14 covariáveis · desfecho (índice 14) · 7 colunas 0/1, uma por tratamento (índices 15–21); controle = todas zero | UDCF (treino) |
| `Data/RCT_data/test_data_UDCF.csv` | 14 covariáveis · desfecho (14) · `exp_group` (15) | UDCF (previsão) |
| `Data/RCT_data/MBCF_train_k.csv`, k = 1..7 | 14 covariáveis · desfecho (14) · tratamento 0/1 (15); só controle + braço k | MBCF (treino) |
| `Data/RCT_data/test_data_MBCF.csv` | igual a `test_data_UDCF.csv` | MBCF (previsão) |

Conferido nos arquivos publicados (2.000 linhas cada):

- `train_data_UDCF.csv` tem as mesmas covariáveis e desfecho de `rct_training.csv`, com
  `exp_group` (0–7) convertido em 7 colunas 0/1;
- `test_data_UDCF.csv` é igual a `rct_test.csv`;
- `MBCF_train_1.csv` tem exatamente as linhas de controle e do braço 1 do treino (507).

Ou seja, os três modelos treinam e são avaliados nas mesmas linhas.

## 4. Os modelos, como estão no código

### UDCF — `Code/Model/LBCF/LBCF_RCT.zip` → `UDCF_RCT/core/main.cpp`

| linha | conteúdo |
|---|---|
| 39–42 | treino: `train_data_UDCF.csv`, desfecho 14, tratamentos `{15..21}` |
| 47–52 | teste: `test_data_UDCF.csv`, desfecho 14, tratamento `{15}` |
| 55 | `udcf_trainer(num_treatments, 1, true)`: o `true` é `stabilize_splits`, a regra do UDCF |
| 56 | `ForestTestUtilities::default_options(true, 1)` |
| 58–59 | `udcf_predictor(1, num_treatments, 1)` e `predictor.predict(forest, data, data2, false)`: **treina no treino e prevê no teste** |

`default_options(true, 1)` (`src/utilities/ForestTestUtilities.cpp`, linhas 29–47):
`num_trees=300`, `sample_fraction=0.5`, `mtry=3`, `min_node_size=50`, `honesty=true`,
`honesty_fraction=0.5`, `prune=true`, `alpha=0.05`, `imbalance_penalty=0.01`,
`num_threads=40`, `seed=42`.

README do `UDCF_RCT`: *"main entrance for this c++ project: /core/main.cpp — you can
modify the input data as you like."*

### MBCF (CF.DT) — `Code/Model/CF_DT/CF_DT_RCT.zip` → `MBCF_RCT/core/main.cpp`

- Laço `for i = 1..7`: uma floresta binária por tratamento, treinada em `MBCF_train_i.csv`.
- `instrumental_trainer(0.0, false)`, com instrumento = tratamento (índice 15), e
  `default_options(true, 1)`.
- Previsão: `instrumental_predictor(5)` e
  **`predictor.predict(forest, data2, data2, false)`**, com o arquivo de teste passado nas
  duas posições.
- As 7 saídas são juntadas por `Code/Model/CF_DT/data_merging.py` (parte RCT) numa
  tabela `exp_group, predict_1..predict_7`.
- O README do `MBCF_RCT` repete *"you can modify the input data as you like."*

### Chi, ED, CTS — `Code/Model/Chi_ED_CTS/Chi_ED_CTS_train_and_predict-RCT.py`

```python
UpliftRandomForestClassifier(n_estimators=300, evaluationFunction=<"Chi"|"ED"|"CTS">,
    max_depth=5, min_samples_leaf=100, min_samples_treatment=50, n_reg=100,
    control_name='0', n_jobs=1, normalization=True)
.fit(X=train[features], treatment=train['exp_group'], y=train['label'])   # rct_training.csv
.predict(test[features])                                                   # rct_test.csv
```

- Sem `random_state`.
- A versão da CausalML não é fixada em nenhum arquivo.

## 5. Como avaliam

- **Dados reais: PMG** (Eq. 2, §3, p. 2313), calculado em `Code/Evaluation/Offline_test.py`
  sobre as políticas com orçamento.
- O artigo critica a *expected outcome* de Zhao et al. só pelo **orçamento**:
  *§3, p. 2312: "the evaluated users is not the whole RCT users ... which causes the
  consumed budget change with different treatment selection policies. Two policies with
  different consumed budgets are not comparable."*
  - **Sem orçamento, essa objeção não se aplica.** O PMG estima
    `E[Y(T = π)] − E[Y(T = 0)]`, normalizado pela média do controle (§3, p. 2313:
    *"the PMG is a plug-in estimator of the quantity E[Y(T=πB) − Y(T=0)]/E[Y(T=0)]"*).
  - O termo `E[Y | T = π]` é o mesmo que a *expected outcome* estima.

## 6. O que isso fixa para este trabalho

| ponto | dos autores | neste trabalho |
|---|---|---|
| divisão | treino e teste, proporção não informada | 70/30 estratificada, semente 42 (escolha nossa, declarada) |
| UDCF | `main.cpp` acima, `imbalance_penalty = 0.01` | **UDCF default** = igual; **UDCF** = `imbalance_penalty = 0` (combinado) |
| ablação | não existe no código | `stabilize_splits = false`, `imbalance_penalty = 0` (combinado) |
| MBCF | laço do `main.cpp` acima, inclusive `predict(forest, data2, data2, false)` | igual, com 2 braços em vez de 7 |
| Chi, ED, CTS | script acima | igual |
| métrica | PMG com orçamento | `expected_outcome` do NRA, sem orçamento (combinado) |
