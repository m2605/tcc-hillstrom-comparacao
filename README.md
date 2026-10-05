# Comparação de modelos de uplift multi-tratamento na Hillstrom

Experimentos do TCC (MBA em Data Science e Analytics). Dois conjuntos de modelos, cada um
rodado **com o código publicado pelos próprios autores**, aplicados à base Hillstrom
(desfecho `conversion`) e avaliados pela mesma métrica, no mesmo conjunto de teste.

| parte | artigo | modelos |
|---|---|---|
| **LBCF** | Ai et al. (2022), *LBCF: A Large-Scale Budget-Constrained Causal Forest Algorithm*, WWW '22 | UDCF, UDCF default, UDCF sem intra-split, MBCF, Chi, ED, CTS |
| **NRA** | Le Boudec et al. (2026), *Multi-treatment uplift evaluation on non-random assignment biased data*, DKE 163 | X-Learner RF, X-Learner XGB, S-Learner XGB, T-Learner XGB, Chi, ED, CTS |

**Métrica:** *expected outcome* de Zhao, Fang & Simchi-Levi (2017), pela função
`expected_outcome` do código do NRA. **Referência:** o melhor tratamento único
(Mens E-Mail para todos).

## Documentos

| arquivo | conteúdo |
|---|---|
| `ACORDOS.md` | regras de trabalho deste repositório |
| `PROTOCOLO_LBCF.md`, `PROTOCOLO_NRA.md` | o que cada artigo e cada código fazem, com página e arquivo:linha |
| `DIVERGENCIAS.md` | toda diferença em relação aos autores, e os acréscimos nossos |
| `HIPERPARAMETROS.md` | origem dos hiperparâmetros, valores de cada modelo e o experimento cruzado |

## Resultados

| parte | tabela | figura |
|---|---|---|
| LBCF | `resultados/lbcf/avaliacao.md` | `resultados/lbcf/avaliacao_lbcf_resposta.png` e `_curva.png` |
| NRA | `resultados/nra/avaliacao.md` | `resultados/nra/avaliacao_nra_resposta.png` e `_curva.png` |

As previsões de cada modelo no teste estão em `resultados/<parte>/predicoes/`.

## Como reproduzir

Código dos autores, obtido dos repositórios originais (não versionado aqui):

```bash
git clone https://github.com/www2022paper/WWW-2022-PAPER-SUPPLEMENTARY-MATERIALS.git upstream/lbcf   # commit 569bc94
git clone https://github.com/Nathpreums/Uplift_Multitreatment_Benchmark_NRA.git upstream/nra        # commit dbbd725
```

Ambiente usado: Python 3.12 (Windows) com `causalml` 0.17.0, `xgboost`, `scikit-learn`,
`pandas`, `matplotlib` e as dependências importadas por `upstream/nra/dependances/évaluation.py`;
WSL2/Ubuntu com `g++` 15.2 e `cmake` 4.2 para os modelos em C++.

Na raiz do repositório, em ordem:

```bash
python lbcf/01_dados/prep_hillstrom.py                         # baixa a Hillstrom; divisão 70/30
bash   lbcf/02_modelos/udcf/roda_udcf.sh                       # no WSL: UDCF, UDCF default, UDCF sem intra-split
bash   lbcf/02_modelos/mbcf/roda_mbcf.sh                       # no WSL: MBCF
python lbcf/02_modelos/chi_ed_cts/Chi_ED_CTS_train_and_predict-RCT.py
python lbcf/03_avaliacao/avalia.py && python lbcf/03_avaliacao/figura.py

python nra/01_dados/prep_nra.py                                # mesmos treino e teste
cd nra/02_modelos && python roda_xgb.py && python roda_xl.py && python roda_chi_ed.py && python roda_cts.py && cd ../..
python nra/03_avaliacao/avalia.py && python nra/03_avaliacao/figura.py
```

Todas as execuções usam semente fixa; o UDCF e o MBCF foram conferidos bit a bit em duas
execuções.
