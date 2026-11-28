# dataops-curso-historia

Projeto prático do curso **Engenharia de Dados: DataOps, CI/CD e Liderança Técnica** (Alura), com Bruno Corrêa.

Ao longo das aulas, um pipeline de dados de uma loja (pedidos, clientes e produtos) sai do nível 1 de maturidade, com scripts que funcionam mas sem testes nem automação, e chega a um projeto com testes, CI/CD, padrões de código e métricas.

## O caso

Na reunião de resultados, o relatório mostrou um faturamento de outubro diferente do que o financeiro fechou, e ninguém soube explicar de onde veio o número. Você é o engenheiro de dados da loja: ao longo das aulas, vai investigar o erro, corrigir e garantir que ele não volte.

## Comandos da Aula 2 · Testes automatizados

Roteiro da aula: copie um bloco de cada vez (botão de copiar no canto do bloco), cole no terminal do Codespace e confira o resultado. Nesta aula você trabalha na própria branch `aula-02-testes`, que já tem a regra corrigida e os testes prontos. Para mostrar o erro, você traz de volta, de propósito, a regra antiga da Aula 1.

Na Aula 1 você achou a causa: o pedido estornado entrou no faturamento, e nenhum teste avisou. Agora os testes provam o erro e mostram a correção.

### Antes de começar · entrar na branch da aula

**1. Trocar para a branch da Aula 2.** Se você está no Codespace da Aula 1, troque de branch. Se preferir, abra um Codespace novo direto na branch `aula-02-testes`.

```bash
git switch aula-02-testes
```

Resultado esperado: `Switched to a new branch 'aula-02-testes'` (ou `Switched to branch`). Se aparecer um erro dizendo que arquivos seriam sobrescritos, rode `git reset --hard` e tente de novo: ele descarta as mudanças que ficaram da aula anterior.

**2. Carregar os dados no banco.**

```bash
python -m src.ingestao
```

Resultado esperado: `1000`, `1000` e `3000` linhas carregadas.

### 2.1 · A pirâmide de testes · prática 1 de 2

**1. Ler a regra e o teste do estorno.** A regra é uma função pura: recebe uma lista de pedidos e devolve só os que entram no faturamento. O `test_remove_pedidos_estornados` é o erro da reunião virando teste.

```bash
code src/transformacoes.py
code tests/test_transformacoes.py
```

**2. Rodar os testes.** O `pytest` procura os testes da pasta `tests/` e roda um por um. O `-v` mostra o nome de cada teste.

```bash
pytest -v
```

Resultado esperado: `6 passed`.

**3. Ver o teste pegar o erro da reunião, de propósito.** Em `src/transformacoes.py`, troque `not in ("cancelado", "estornado")` por `!= "cancelado"`, que é a regra antiga da Aula 1. Salve e rode:

```bash
pytest -v
```

Resultado esperado: `1 failed`, no `test_remove_pedidos_estornados`. Desfaça com **Ctrl+Z**, salve e rode `pytest -v` de novo: `6 passed`.

### 2.2 · Integração e idempotência · prática-relâmpago

**1. Rodar a ingestão duas vezes seguidas.** Se o pipeline não fosse idempotente, a segunda vez somaria os pedidos de novo.

```bash
python -m src.ingestao
python -m src.ingestao
```

Resultado esperado: `raw.pedidos: 3000 linhas` nas duas vezes. Nada duplicou.

### 2.3 · Testando dados com dbt · prática 2 de 2

**1. Ler os testes de dados.** No `_staging.yml`, o `accepted_values` lista os status que a loja conhece. No `_marts.yml`, o unit test `valor_total_ignora_estornados` diz o que o faturamento deveria fazer com um estorno.

```bash
code models/staging/_staging.yml
code models/marts/_marts.yml
```

**2. Trazer de volta a regra antiga, a da reunião.** O primeiro comando copia o `fct_pedidos` da Aula 1, que só tira os cancelados. O segundo roda os modelos e os testes na ordem do grafo.

```bash
git checkout origin/aula-01-inicio -- models/marts/fct_pedidos.sql
dbt build
```

Resultado esperado: `FAIL 1` no unit test `valor_total_ignora_estornados` e `ERROR=1`. O teste pegou o erro da reunião: o pedido estornado entrou no faturamento.

**3. Voltar a regra corrigida e conferir o faturamento.** O primeiro comando devolve o `fct_pedidos` desta branch, que tira cancelados e estornados.

```bash
git checkout HEAD -- models/marts/fct_pedidos.sql
code models/marts/fct_pedidos.sql
dbt build
python scripts/faturamento.py
```

Resultado esperado: `PASS=12` e `Faturamento de outubro: R$ 315.488,80 em 2411 pedidos`. O número agora bate com o financeiro.

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
