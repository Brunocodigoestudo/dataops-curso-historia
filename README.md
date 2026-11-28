# dataops-curso-historia

Projeto prático do curso **Engenharia de Dados: DataOps, CI/CD e Liderança Técnica** (Alura), com Bruno Corrêa.

Ao longo das aulas, um pipeline de dados de uma loja (pedidos, clientes e produtos) sai do nível 1 de maturidade, com scripts que funcionam mas sem testes nem automação, e chega a um projeto com testes, CI/CD, padrões de código e métricas.

## O caso

Na reunião de resultados, o relatório mostrou um faturamento de outubro diferente do que o financeiro fechou, e ninguém soube explicar de onde veio o número. Você é o engenheiro de dados da loja: ao longo das aulas, vai investigar o erro, corrigir e garantir que ele não volte.

## Comandos da Aula 2 · Testes automatizados

Roteiro da aula: copie um bloco de cada vez (botão de copiar no canto do bloco), cole no terminal do Codespace e confira o resultado. Nesta aula você trabalha na própria branch `aula-02-testes`. Ela começa do jeito que estava no dia da reunião: a regra do faturamento ainda soma os estornos e não existe nenhum teste. Você cria os testes, eles mostram o erro, você corrige uma linha e os testes confirmam a correção.

### Antes de começar · entrar na branch e ver o número errado

**1. Trocar para a branch da Aula 2.** Se você está no Codespace da Aula 1, troque de branch. Se preferir, abra um Codespace novo direto na branch `aula-02-testes`.

```bash
# git switch: troca para outra branch. Aqui, a branch da Aula 2
git switch aula-02-testes
```

Resultado esperado: `Switched to a new branch 'aula-02-testes'` (ou `Switched to branch`). Se aparecer um erro dizendo que arquivos seriam sobrescritos, rode `git reset --hard` e tente de novo.

**2. Rodar o pipeline e ver o número da reunião.**

```bash
# Roda a ingestão: lê os CSVs da pasta data/ e grava no banco DuckDB
# na camada raw, que guarda o dado bruto, do jeito que chegou
python -m src.ingestao
# dbt run: monta as tabelas do dbt: o staging (dado padronizado)
# e o fct_pedidos (a tabela do faturamento)
dbt run
# Mostra o faturamento do mês: soma o valor dos pedidos do fct_pedidos,
# o mesmo número que vai para o relatório da diretoria
python scripts/faturamento.py
```

Resultado esperado: `1000`, `1000` e `3000` linhas carregadas, `PASS=3` e `Faturamento de outubro: R$ 333.739,80 em 2546 pedidos`. É o número errado da reunião: o financeiro fechou `R$ 315.488,80`.

### 2.1 · A pirâmide de testes · prática 1 de 2

**1. Ler a regra do faturamento em Python.** A função recebe uma lista de pedidos e devolve só os que entram no faturamento. Repare que ela só tira os cancelados.

```bash
# code: abre um arquivo no editor.
# transformacoes.py: a regra do faturamento escrita em Python
code src/transformacoes.py
```

**2. Criar a pasta de testes.** O `mkdir` cria a pasta `tests`. O `touch` cria o arquivo vazio `__init__.py`, que avisa o Python que a pasta faz parte do projeto.

```bash
# mkdir: cria uma pasta. Aqui, a pasta tests, onde ficam os testes.
# O -p evita erro se a pasta já existir
mkdir -p tests
# touch: cria um arquivo vazio.
# __init__.py: marca a pasta tests como um pacote do Python. Com ele, o pytest
# consegue achar o código da pasta src/. Sem ele, o teste dá erro de import
touch tests/__init__.py
```

**3. Criar o arquivo de testes.** O comando abre um arquivo novo no editor. Cole o código abaixo, já comentado, e salve com **Ctrl+S**.

```bash
# code: como o arquivo ainda não existe, cria e abre ele no editor.
# test_transformacoes.py: os testes da regra do faturamento.
# Cole o código e salve com Ctrl+S
code tests/test_transformacoes.py
```

```python
# Testes da regra de faturamento (src/transformacoes.py).
# Cada teste monta pedidos de exemplo, passa pela regra
# e confere se o resultado é o esperado.

from src.transformacoes import calcular_valor_total


def test_calcula_valor_total():
    # Um pedido pago: 2 unidades de R$ 10,50.
    pedidos = [{"quantidade": 2, "preco_unitario": 10.5, "status": "pago"}]
    resultado = calcular_valor_total(pedidos)
    # O valor total tem que ser quantidade x preço: R$ 21,00.
    assert resultado[0]["valor_total"] == 21.0


def test_remove_pedidos_cancelados():
    # Pedido cancelado não é venda: não pode entrar no faturamento.
    pedidos = [{"quantidade": 1, "preco_unitario": 5, "status": "cancelado"}]
    # A lista vazia mostra que a regra tirou o pedido.
    assert calcular_valor_total(pedidos) == []


def test_remove_pedidos_estornados():
    # O ERRO DA REUNIÃO: o estorno é dinheiro que voltou para o cliente.
    # A regra antiga somava o estorno, e o faturamento foi para mais.
    # Este teste garante que o erro não volta.
    pedidos = [{"quantidade": 1, "preco_unitario": 89.9, "status": "estornado"}]
    assert calcular_valor_total(pedidos) == []
```

**4. Rodar os testes.** O `pytest` procura os testes da pasta `tests/` e roda um por um. O `-v` mostra o nome de cada teste.

```bash
# pytest: procura os arquivos test_*.py da pasta tests e roda cada teste.
# O -v (verbose) mostra o nome de cada teste e se passou ou falhou
pytest -v
```

Resultado esperado: `1 failed, 2 passed`. O teste que falhou é o `test_remove_pedidos_estornados`: o teste provou o erro da reunião.

**5. Corrigir a regra.** Em `src/transformacoes.py`, troque a linha

```python
        if p["status"] != "cancelado"
```

por

```python
        if p["status"] not in ("cancelado", "estornado")
```

Salve e rode os testes de novo.

```bash
# pytest: procura os arquivos test_*.py da pasta tests e roda cada teste.
# O -v (verbose) mostra o nome de cada teste e se passou ou falhou
pytest -v
```

Resultado esperado: `3 passed`. A regra foi corrigida, e o teste confirma.

### 2.2 · Integração e idempotência · prática-relâmpago

**1. Rodar a ingestão duas vezes seguidas.** Se o pipeline não fosse idempotente, a segunda vez somaria os pedidos de novo.

```bash
# Roda a ingestão: lê os CSVs da pasta data/ e grava no banco DuckDB
# na camada raw, que guarda o dado bruto, do jeito que chegou
python -m src.ingestao
# Roda a ingestão de novo: se o número de linhas não dobrar,
# o pipeline é idempotente
python -m src.ingestao
```

Resultado esperado: `raw.pedidos: 3000 linhas` nas duas vezes. Nada duplicou.

### 2.3 · Testando dados com dbt · prática 2 de 2

**1. Criar o teste da regra do faturamento no dbt.** Abre um arquivo novo. Cole o código abaixo e salve com **Ctrl+S**. Cada unit test inventa alguns pedidos e confere o que o `fct_pedidos` devolve.

```bash
# code: cria e abre o arquivo no editor.
# _marts.yml: os unit tests da regra do faturamento no dbt.
# Cole o código e salve com Ctrl+S
code models/marts/_marts.yml
```

```yaml
# Testes da regra do faturamento no dbt (unit tests).
# Cada teste inventa alguns pedidos, roda o fct_pedidos com eles
# e confere se o resultado é o esperado.
version: 2

unit_tests:
  # Pedido cancelado não é venda: só o pedido pago pode aparecer.
  - name: valor_total_ignora_cancelados
    model: fct_pedidos
    given:
      - input: ref('stg_pedidos')
        rows:
          - {id_pedido: 1, quantidade: 2, preco_unitario: 10.0, status: 'pago'}
          - {id_pedido: 2, quantidade: 1, preco_unitario: 5.0, status: 'cancelado'}
    expect:
      rows:
        - {id_pedido: 1, valor_total: 20.0}

  # O ERRO DA REUNIÃO: o estorno é dinheiro que voltou para o cliente.
  # Só o pedido pago pode aparecer no faturamento.
  - name: valor_total_ignora_estornados
    model: fct_pedidos
    given:
      - input: ref('stg_pedidos')
        rows:
          - {id_pedido: 1, quantidade: 2, preco_unitario: 10.0, status: 'pago'}
          - {id_pedido: 6, quantidade: 1, preco_unitario: 89.9, status: 'estornado'}
    expect:
      rows:
        - {id_pedido: 1, valor_total: 20.0}
```

**2. Criar o teste do dado real.** Abre outro arquivo novo. Cole o código abaixo e salve com **Ctrl+S**. Ele confere os pedidos que chegaram: sem repetidos, sem vazios e só com os status que a loja conhece.

```bash
# code: cria e abre o arquivo no editor.
# _staging.yml: os testes do dado real, que conferem os pedidos que chegaram.
# Cole o código e salve com Ctrl+S
code models/staging/_staging.yml
```

```yaml
# Testes do dado real (data tests): conferem os pedidos que chegaram
# toda vez que o pipeline roda.
version: 2

models:
  - name: stg_pedidos
    columns:
      # Cada pedido aparece uma vez só e nunca fica vazio.
      - name: id_pedido
        data_tests:
          - unique
          - not_null
      # O porteiro: só entram os status que a loja conhece.
      - name: status
        data_tests:
          - accepted_values:
              arguments:
                values: ['aberto', 'pago', 'cancelado', 'estornado']
```

**3. Rodar modelos e testes juntos.** O `dbt build` roda os modelos e os testes na ordem certa.

```bash
# dbt build: monta as tabelas e roda os testes, na ordem certa.
# Se um teste falha, o dbt não monta o que depende dele (SKIP)
dbt build
```

Resultado esperado: `FAIL 1` no unit test `valor_total_ignora_estornados` e `ERROR=1`. O teste pegou o erro da reunião: o pedido estornado entrou no faturamento.

**4. Corrigir a regra do faturamento no dbt.** Abra o `fct_pedidos.sql`:

```bash
# code: abre um arquivo no editor.
# fct_pedidos.sql: a regra do faturamento escrita em SQL, no dbt
code models/marts/fct_pedidos.sql
```

Troque a linha

```sql
where status != 'cancelado'
```

por

```sql
where status not in ('cancelado', 'estornado')
```

Salve e rode de novo:

```bash
# dbt build: monta as tabelas e roda os testes, na ordem certa.
# Se um teste falha, o dbt não monta o que depende dele (SKIP)
dbt build
# Mostra o faturamento do mês: soma o valor dos pedidos do fct_pedidos,
# o mesmo número que vai para o relatório da diretoria
python scripts/faturamento.py
```

Resultado esperado: `PASS=8` e `Faturamento de outubro: R$ 315.488,80 em 2411 pedidos`. O número agora bate com o financeiro.

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
