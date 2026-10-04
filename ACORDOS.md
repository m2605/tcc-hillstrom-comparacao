# Acordos de trabalho

Regras deste repositório, combinadas antes de qualquer código (03/10/2026).
Valem para todos os passos. Mudar um acordo exige combinar de novo e registrar aqui.

## 1. O código dos autores não se altera

O código dos autores é usado tal como publicado: hiperparâmetros, linhas de previsão,
ausência de semente onde não há semente. As únicas mudanças permitidas:

- adaptar a Hillstrom ao formato de entrada que o código deles espera
  (caminhos de arquivo, índices de colunas, número de tratamentos);
- na ablação, `stabilize_splits = false` no lugar de `true`.

O código dos autores não é versionado aqui (os repositórios de origem não declaram
licença); obtém-se do repositório original e fica em pastas ignoradas pelo git.

## 2. Acréscimos só em arquivos separados

- **Métrica:** a função `expected_outcome` do repositório do benchmark NRA
  (Le Boudec et al., 2026), usada diretamente, sem reimplementação.
- **Curva de uplift modificada** (Zhao, Fang & Simchi-Levi, 2017, §4.2): não existe no
  código do NRA. É acréscimo nosso, construído chamando a `expected_outcome` deles.

## 3. Protocolo: treino e teste, como os autores

O artigo do LBCF (apêndice A.3) e o código deles dividem os dados em treino e teste.
A proporção não é informada no artigo; a nossa escolha, declarada como tal:
**70/30, estratificada por tratamento × desfecho, semente 42.**

## 4. Modelos

Do artigo do LBCF, apenas:

| modelo | o que é |
|---|---|
| **UDCF** | UDCF com `imbalance_penalty = 0` |
| **UDCF default** | UDCF com `imbalance_penalty = 0.01`, o valor do código dos autores |
| **Ablação** | UDCF com `stabilize_splits = false` e `imbalance_penalty = 0` (mesmo valor do UDCF, para isolar a regra de divisão) |
| **MBCF** | baseline CF.DT dos autores (uma floresta por braço) |
| **Chi, ED, CTS** | baselines da CausalML, com os hiperparâmetros do script dos autores |

Os demais (CT.ST, S-learner, T-learner etc.) não entram.

**Benchmark NRA** (Le Boudec et al., 2026): também neste repositório, como trabalho à parte,
com o código dos autores do NRA sob as mesmas regras. Modelos (decisão de 03/10/2026, ver
`PROTOCOLO_NRA.md`):

| modelo | origem |
|---|---|
| X-Learner RF, X-Learner XGB | `execution_XL.ipynb` dos autores |
| S-Learner XGB, T-Learner XGB | `execution_xgb.ipynb` dos autores |
| ED, CTS | `execution_chi_ed.ipynb` e `execution_cts.ipynb` dos autores |
| Chi | linhas comentadas no `execution_chi_ed.ipynb`, descomentadas |

R-Learner, DR-Learner, S-Learner LR, T-Learner LR e TARNet não entram.

## 5. Cada passo é combinado antes e relatado depois

Antes: qual arquivo, o que muda, por quê. Depois: o resultado e a origem de cada peça
(artigo, código dos autores ou acréscimo nosso).

## 6. Divergências registradas no momento

Toda divergência em relação ao artigo ou ao código dos autores vai para
`DIVERGENCIAS.md` quando acontece, com citação e página do artigo ou arquivo:linha do
código deles.

## 7. Só fontes primárias

Toda afirmação se apoia no artigo (texto, figuras e apêndice), no código, README e
considerações dos autores, ou na saída de uma execução. Notas de trabalhos anteriores
não servem como prova.

## 8. Commits e publicação

Um commit por passo, só após aprovação. Repositório privado no GitHub até decisão
em contrário.
