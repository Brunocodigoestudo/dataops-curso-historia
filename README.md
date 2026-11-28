# dataops-curso-historia

Projeto prático do curso **Engenharia de Dados: DataOps, CI/CD e Liderança Técnica** (Alura), com Bruno Corrêa.

Ao longo das aulas, um pipeline de dados de uma loja (pedidos, clientes e produtos) sai do nível 1 de maturidade, com scripts que funcionam mas sem testes nem automação, e chega a um projeto com testes, CI/CD, padrões de código e métricas.

## O caso

Na reunião de resultados, o relatório mostrou um faturamento de outubro diferente do que o financeiro fechou, e ninguém soube explicar de onde veio o número. Você é o engenheiro de dados da loja: ao longo das aulas, vai investigar o erro, corrigir e garantir que ele não volte.

## Comandos da Aula 2 · Testes automatizados

Roteiro da aula: copie um bloco de cada vez (botão de copiar no canto do bloco), cole no terminal do Codespace e confira o resultado. Você começa da branch `aula-01-inicio` e traz os arquivos desta branch com `git checkout`. Na Aula 2 você trabalha direto na `main`.

Na Aula 1 você achou a causa: o pedido estornado entrou no faturamento, e nenhum teste avisou. Agora os testes provam o erro, a regra é corrigida e o projeto passa a barrar status desconhecidos antes do relatório.

### 2.1 · A pirâmide de testes · prática 1 de 2

**1. Trazer a regra de negócio e os testes em Python.** Copia de uma vez os arquivos de Python e de testes da branch `aula-02-testes` para o seu projeto.

```bash
git checkout origin/aula-02-testes -- src/transformacoes.py src/pipeline.py tests/__init__.py tests/test_transformacoes.py tests/test_integracao.py tests/test_ingestao.py
```

**2. Ler a regra e o teste do estorno.** A regra é uma função pura: recebe uma lista de pedidos e devolve só os que entram no faturamento. O `test_remove_pedidos_estornados` é o erro da reunião virando teste.

```bash
code src/transformacoes.py
code tests/test_transformacoes.py
```

**3. Rodar os testes.** O `pytest` procura os testes da pasta `tests/` e roda um por um. O `-v` mostra o nome de cada teste.

```bash
pytest -v
```

Resultado esperado: `9 passed`.

**4. Ver o teste pegar o erro da reunião, de propósito.** Em `src/transformacoes.py`, troque `not in ("cancelado", "estornado")` por `!= "cancelado"`, que é a regra antiga da Aula 1. Salve e rode:

```bash
pytest -v
```

Resultado esperado: `1 failed`, no `test_remove_pedidos_estornados`. Desfaça com **Ctrl+Z**, salve e rode `pytest -v` de novo: `9 passed`.

### 2.2 · Integração e idempotência

O vídeo 2.2 é só de slides, sem comandos.

### 2.3 · Testando dados com dbt · prática 2 de 2

**1. Trazer os testes de dados.** Testes do staging, unit tests do mart e o teste singular. A regra do `fct_pedidos` ainda é a antiga, a mesma que gerou o número errado.

```bash
git checkout origin/aula-02-testes -- models/staging/_staging.yml models/marts/_marts.yml tests/assert_valor_total_positivo.sql
code models/staging/_staging.yml
code models/marts/_marts.yml
```

No `_staging.yml`, o `accepted_values` lista os status que a loja conhece. No `_marts.yml`, o unit test `valor_total_ignora_estornados` diz o que o faturamento deveria fazer com um estorno.

**2. Rodar modelos e testes juntos.** O primeiro comando carrega os CSVs. O `dbt build` roda os modelos e os testes na ordem do grafo.

```bash
python -m src.ingestao
dbt build
```

Resultado esperado: `FAIL 1` no unit test `valor_total_ignora_estornados`, `ERROR=1` e `SKIP=3`. O teste reproduziu o erro da reunião: o pedido estornado apareceu no resultado, somado ao faturamento.

**3. Corrigir a regra e conferir o faturamento.** Traz o `fct_pedidos` corrigido: cancelados e estornados ficam fora do faturamento.

```bash
git checkout origin/aula-02-testes -- models/marts/fct_pedidos.sql
code models/marts/fct_pedidos.sql
dbt build
python scripts/faturamento.py
```

Resultado esperado: `PASS=12` e `Faturamento de outubro: R$ 315.488,80 em 2411 pedidos`. O número agora bate com o financeiro.

**4. Salvar a aula no Git.** Prepara os arquivos, registra o commit e envia para o GitHub.

```bash
git add .
git commit -m "fix: estornado fora do faturamento, com testes"
git push
```

### 2.4 · Cobertura de testes

O vídeo 2.4 é só de slides, sem comandos.

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
