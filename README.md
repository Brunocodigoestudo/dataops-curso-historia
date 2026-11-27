# dataops-curso-historia

Projeto prático do curso **Engenharia de Dados: DataOps, CI/CD e Liderança Técnica** (Alura), com Bruno Corrêa.

Ao longo das aulas, um pipeline de dados de uma loja (pedidos, clientes e produtos) sai do nível 1 de maturidade, com scripts que funcionam mas sem testes nem automação, e chega a um projeto com testes, CI/CD, padrões de código e métricas.

## O caso

Na reunião de resultados, o relatório mostrou um faturamento de outubro diferente do que o financeiro fechou, e ninguém soube explicar de onde veio o número. Você é o engenheiro de dados da loja: ao longo das aulas, vai investigar o erro, corrigir e garantir que ele não volte.

## Comandos da Aula 2 · Testes automatizados

Roteiro da aula: copie um bloco de cada vez (botão de copiar no canto do bloco), cole no terminal do Codespace e confira o resultado. Você começa da branch `aula-01-inicio` e traz os arquivos desta branch com `git checkout`. Na Aula 2 você trabalha direto na `main`.

Na Aula 1 você achou a causa: o pedido estornado entrou no faturamento, e nenhum teste avisou. Agora os testes provam o erro, a regra é corrigida e o projeto passa a barrar status desconhecidos antes do relatório.

### 2.1 · A pirâmide de testes

**1. Trazer a regra de negócio e os testes unitários.** Copia só estes arquivos da branch `aula-02-testes` para o seu projeto.

```bash
git checkout origin/aula-02-testes -- src/transformacoes.py tests/__init__.py tests/test_transformacoes.py
```

**2. Ler a regra e os testes.** A regra é uma função pura: recebe uma lista e devolve uma lista. São quatro testes, e o `parametrize` roda o mesmo teste com vários cenários. O `test_remove_pedidos_estornados` é o erro da reunião virando teste.

```bash
code src/transformacoes.py
code tests/test_transformacoes.py
```

**3. Rodar os testes.** O `pytest` procura os testes da pasta `tests/` e roda um por um. O `-v` mostra o nome de cada teste.

```bash
pytest -v
```

Resultado esperado: `6 passed`.

**4. Ver o teste falhar, de propósito.** Em `src/transformacoes.py`, troque `round(p["quantidade"] * p["preco_unitario"], 2)` por `p["quantidade"] * p["preco_unitario"]`, salve e rode:

```bash
pytest -v
```

Resultado esperado: `1 failed`, com o valor `0.30000000000000004`. Desfaça com **Ctrl+Z**, salve e rode `pytest -v` de novo: `6 passed`.

### 2.2 · Integração e idempotência

**1. Trazer o pipeline e o teste de integração.** O pipeline lê do banco, aplica a regra e grava o resultado.

```bash
git checkout origin/aula-02-testes -- src/pipeline.py tests/test_integracao.py
code src/pipeline.py
code tests/test_integracao.py
```

**2. Rodar os testes.** A fixture cria um DuckDB em memória: um banco real, mas descartável.

```bash
pytest -v
```

Resultado esperado: `8 passed`.

**3. Ver a idempotência quebrar, de propósito.** Em `src/pipeline.py`, troque `CREATE OR REPLACE TABLE` por `CREATE TABLE IF NOT EXISTS`, salve e rode:

```bash
pytest -v
```

Resultado esperado: `1 failed`, com `assert 2 == 1`. O pedido apareceu duas vezes. Desfaça com **Ctrl+Z**, salve e rode `pytest -v` de novo: `8 passed`.

### 2.3 · Testando dados com dbt

**1. Trazer os testes de dados.** Testes do staging, unit tests do mart e o teste singular. A regra do `fct_pedidos` ainda é a antiga, a mesma que gerou o número errado.

```bash
git checkout origin/aula-02-testes -- models/staging/_staging.yml models/marts/_marts.yml tests/assert_valor_total_positivo.sql
code models/staging/_staging.yml
code models/marts/_marts.yml
code tests/assert_valor_total_positivo.sql
```

No `_staging.yml`, o `accepted_values` lista os status que a loja conhece. No `_marts.yml`, o unit test `valor_total_ignora_estornados` diz o que o faturamento deveria fazer com um estorno.

**2. Rodar modelos e testes juntos.** O primeiro comando carrega os CSVs. O `dbt build` roda os modelos e os testes na ordem do grafo.

```bash
python -m src.ingestao
dbt build
```

Resultado esperado: `FAIL 1` no unit test `valor_total_ignora_estornados`, `ERROR=1` e `SKIP=2`. O teste reproduziu o erro da reunião: o pedido estornado apareceu no resultado, somado ao faturamento.

**3. Corrigir a regra.** Traz o `fct_pedidos` corrigido: cancelados e estornados ficam fora do faturamento.

```bash
git checkout origin/aula-02-testes -- models/marts/fct_pedidos.sql
code models/marts/fct_pedidos.sql
dbt build
python scripts/faturamento.py
```

Resultado esperado: `PASS=12` e `Faturamento de outubro: R$ 315.488,80 em 2411 pedidos`. O número agora bate com o financeiro.

**4. Chegar um status novo, de propósito.** Acrescenta um pedido com o status `devolvido`, que a loja ainda não conhece, carrega de novo e roda o build.

```bash
echo "3001,1,1,1,5.90,devolvido,2026-10-31" >> data/pedidos.csv
python -m src.ingestao
dbt build
```

Resultado esperado: `FAIL 1` no teste `accepted_values` do status, `ERROR=1` e `SKIP=4`. O teste funciona como um porteiro: barrou o status desconhecido antes de ele chegar ao relatório. O teste não corrige o dado, ele avisa. O que fazer com o status novo é decisão do engenheiro com o negócio.

**5. Desfazer.** Volta o CSV ao original, carrega de novo e roda o build.

```bash
git checkout data/pedidos.csv
python -m src.ingestao
dbt build
```

Resultado esperado: `PASS=12`.

### 2.4 · Cobertura de testes

**1. Medir a cobertura.** Mostra quais linhas os testes executaram. Abaixo de 80%, falha.

```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=80
```

Resultado esperado: `42%` e `FAIL`. A ingestão inteira está sem teste.

**2. Trazer o teste que falta.** O teste da ingestão roda numa pasta temporária, sem tocar nos dados reais.

```bash
git checkout origin/aula-02-testes -- tests/test_ingestao.py
code tests/test_ingestao.py
```

**3. Medir de novo.**

```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=80
```

Resultado esperado: `9 passed` e `96%`.

**4. Salvar a aula no Git.** Prepara os arquivos, registra o commit e envia para o GitHub.

```bash
git add .
git commit -m "fix: estornado fora do faturamento, com testes"
git push
```

## Como abrir o ambiente

**Pelo navegador, sem instalar nada (recomendado):**

1. Escolha a branch da aula no seletor de branches do GitHub.
2. Clique em **Code → Codespaces → Create codespace**.
3. Espere o ambiente ficar pronto. Python 3.12, dbt, DuckDB e as demais ferramentas são instalados sozinhos.
4. Ao terminar de estudar, pare o codespace (menu Codespaces → Stop) para não gastar a sua cota gratuita.

**No seu computador:** instale Python 3.12 e Git, depois rode:

```bash
python -m venv .venv
source .venv/bin/activate          # no Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
export DBT_PROFILES_DIR=.          # no Windows: $env:DBT_PROFILES_DIR = "."
```

## Primeiros comandos

```bash
python -m src.ingestao   # carrega os CSVs da pasta data/ no DuckDB
dbt run                  # constrói os modelos
```

## Uma branch por aula

Cada branch guarda o estado do projeto **ao final** da aula. Para acompanhar uma aula, comece pela branch da aula anterior.

| Branch | Estado do projeto |
| --- | --- |
| `aula-01-inicio` | Scripts funcionando, sem testes e sem CI. O faturamento chega errado na reunião |
| `aula-02-testes` | Testes com pytest, testes de dados do dbt, cobertura e a correção do faturamento |
| `aula-03-ci-cd` | CI em todo pull request barrando a regra antiga e deploy em staging e production com aprovação |
| `aula-04-padroes` | pre-commit, template de pull request, CODEOWNERS e ADRs, incluindo a regra do faturamento |
| `aula-05-lideranca` | Documentação dos modelos e runbook de incidente de dados |
| `aula-06-metricas` | Postmortem do faturamento divergente e métricas DORA |

## Estrutura

```text
dataops-curso-historia/
├── .devcontainer/     ambiente do Codespaces
├── data/              CSVs de origem
├── src/               ingestão e transformações em Python
├── models/            modelos dbt (staging e marts)
├── scripts/           faturamento e consultas ao banco
├── dbt_project.yml
├── profiles.yml
└── requirements.txt
```
