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
