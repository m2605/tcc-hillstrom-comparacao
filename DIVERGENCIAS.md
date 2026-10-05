# Divergências em relação aos autores

Toda diferença entre o que este repositório faz e o que o artigo ou o código dos autores
faz. Registrada no momento em que é decidida (acordo 6).

Não entram aqui as adaptações de entrada que os próprios autores autorizam
(*"you can modify the input data as you like"*, README de `UDCF_RCT` e de `MBCF_RCT`):
caminhos de arquivo, índices de colunas e número de tratamentos.

## Parte LBCF

| # | o quê | autores | este trabalho | motivo |
|---|---|---|---|---|
| L1 | proporção treino/teste | não informada (artigo, apêndice A.3) | 70/30, estratificada por tratamento × desfecho, semente 42 | escolha necessária; a mesma do benchmark NRA, para os dois trabalhos usarem o mesmo teste |
| L2 | desfecho | duração de engajamento, contínua (§5.2) | `conversion` da Hillstrom, 0/1 | é a base deste trabalho; decisão de 03/10/2026 |
| L3 | `imbalance_penalty` do UDCF | 0.01 (`default_options`, `ForestTestUtilities.cpp:38`) | **UDCF default** = 0.01; **UDCF** = 0 | combinado (ACORDOS §4) |
| L4 | ablação | não existe no código | `udcf_trainer(..., false)`: `stabilize_splits = false`, `imbalance_penalty = 0` | combinado (ACORDOS §4); `stabilize_splits` é parâmetro da própria função dos autores |
| L5 | semente do Chi, ED e CTS | sem `random_state` (`Chi_ED_CTS_train_and_predict-RCT.py:12,20,28`) | `random_state = 42` | reprodutibilidade: mesmos resultados em cada execução; não altera o método nem os hiperparâmetros. Decisão de 03/10/2026 |
| L6 | métrica | PMG com orçamento (Eq. 2; `Code/Evaluation/Offline_test.py`) | `expected_outcome` do código do NRA, sem orçamento | sem custo e sem orçamento a etapa de otimização não se aplica; a objeção do LBCF à *expected outcome* é só sobre orçamento (§3, p. 2312). Combinado (ACORDOS §2) |

## Ambiente de compilação (não altera código nem método)

| # | o quê | autores | este trabalho | motivo |
|---|---|---|---|---|
| A1 | versão mínima do CMake | `cmake_minimum_required(VERSION 2.0)` no `CMakeLists.txt` | arquivo intocado; configurado com `cmake -DCMAKE_POLICY_VERSION_MINIMUM=3.5 ..` | o CMake 4 recusa versões mínimas abaixo de 3.5; a opção de linha de comando é a que o próprio CMake indica e não muda o código |
| A2 | executável pré-compilado no zip | `UDCF_RCT/core/build/UDCF` (compilado em 2021) | descartado; recompilado do código-fonte, seguindo o README (`rm -r *`, `cmake ..`, `make`) | garantir que o executável corresponde ao código; o alvo do `CMakeLists.txt` gera `UDCF_RCT` (o README cita `./UDCF`) |
| A3 | nomes das colunas na saída do Chi, ED e CTS | `pd.DataFrame(pred, columns=model.classes_)` (`Chi_ED_CTS_train_and_predict-RCT.py:17,25,33`); versão da CausalML não fixada pelos autores | `columns=` `classes_` sem o controle | na CausalML 0.17.0, `classes_` inclui o controle e `predict` devolve só os tratamentos, e a linha original quebra; o arquivo de resultado publicado pelos autores (`Chi_ED_CTS/5Chiresult`) tem colunas só dos tratamentos (`1,2,3`), formato que esta mudança reproduz. Só muda o nome das colunas; os valores são os do `predict` |

## Acréscimos (não existem no código dos autores)

| # | o quê | como | conferência |
|---|---|---|---|
| X1 | intervalo de confiança de 95 % da resposta esperada | contribuição de cada cliente pela Eq. 2.3 de Zhao et al. (2017), cujo Teorema 2.1 indica que o IC pode ser calculado; IC normal pelo erro-padrão da média (`lbcf/03_avaliacao/avalia.py`). Até 05/10/2026 incluía também um teste z pareado contra Mens para todos, a diferença em p.p. e a distribuição das recomendações; foram retirados por não terem apoio em nenhum dos artigos de referência | a média das contribuições é igual à `expected_outcome` do NRA em todas as políticas (diferença < 1e-12, verificada por `assert`) |
| X2 | curva de uplift modificada | Zhao et al. (2017), §4.2: os p % com maior diferença prevista entre o tratamento ótimo e o controle recebem o ótimo; os demais, o controle | três pontos por modelo recalculados com a `expected_outcome` do NRA (`assert`) |
| X3 | regras de tratamento único (nenhum, Mens, Womens para todos) | `expected_outcome` do NRA com política constante (Zhao et al., 2017, Fig. 3 e §4.2) | Mens para todos = taxa observada do grupo Mens no teste (1,252 %) |
| X4 | experimento: Chi, ED e CTS pelo pipeline do NRA com os hiperparâmetros do LBCF | entradas como nos cadernos do NRA; hiperparâmetros de `Chi_ED_CTS_train_and_predict-RCT.py:12-14`; semente 42 e `n_jobs` padrão, como no NRA (`nra/04_experimento_hiper_lbcf/roda.py`) | comparação das previsões com as da parte LBCF, que usa `n_jobs = 1`. Isola o efeito dos hiperparâmetros: decisão de 04/10/2026 |

## Parte NRA

| # | o quê | autores | este trabalho | motivo |
|---|---|---|---|---|
| N1 | Chi | linhas comentadas em `execution_chi_ed.ipynb` | descomentadas, sem outra mudança | decisão de 03/10/2026 |
| N2 | TARNet | descrito no artigo (§3.1.3; 5º de 12 na Tabela 2), ausente do código | não entra | decisão de 03/10/2026: é o único método sem código dos autores; rodá-lo exigiria escolher arquitetura, treino e validação sem especificação no artigo. Sem ele, tudo o que roda na parte NRA é código dos autores |
| N3 | R-Learner, DR-Learner, S-Learner LR, T-Learner LR | na Tabela 2; R/DR no código com nomes trocados; S/T-LR não executados | não entram | decisão de 03/10/2026 |
| N4 | dados e métrica | sintéticos com viés NRA; RMSE e *expected outcome* | Hillstrom (experimento aleatorizado, sem viés a induzir), mesma divisão da parte LBCF (L1); só *expected outcome* | RMSE exige o uplift verdadeiro, inexistente em dado real |
