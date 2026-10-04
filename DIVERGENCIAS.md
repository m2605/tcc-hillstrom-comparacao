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
