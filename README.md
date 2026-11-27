# dataops-curso-historia

Projeto prático do curso **Engenharia de Dados: DataOps, CI/CD e Liderança Técnica** (Alura), com Bruno Corrêa.

Ao longo das aulas, um pipeline de dados de uma loja (pedidos, clientes e produtos) sai do nível 1 de maturidade, com scripts que funcionam mas sem testes nem automação, e chega a um projeto com testes, CI/CD, padrões de código e métricas.

## O caso

Na reunião de resultados, o relatório mostrou um faturamento de outubro diferente do que o financeiro fechou, e ninguém soube explicar de onde veio o número. Você é o engenheiro de dados da loja: ao longo das aulas, vai investigar o erro, corrigir e garantir que ele não volte.

## Comandos da Aula 1 · Princípios de DataOps

Roteiro da aula: copie um bloco de cada vez (botão de copiar no canto do bloco), cole no terminal do Codespace e confira o resultado. O comando `code` abre o arquivo no editor.

### 1.4 · O ambiente no Codespaces

**1. Criar o ambiente.** No GitHub, escolha a branch `aula-01-inicio` e clique em **Code → Codespaces → Create codespace**. Espere o terminal aparecer.

**2. Ver a receita do ambiente.** Mostra a imagem com Python 3.12, o comando que instala as dependências e a variável que faz o dbt achar o `profiles.yml`.

```bash
code .devcontainer/devcontainer.json
```

**3. Ver as versões fixadas.** Cada ferramenta tem a versão travada, para todo mundo ter o mesmo resultado.

```bash
code requirements.txt
```

**4. Conferir as versões instaladas.** Mostra a versão do Python e do dbt que o ambiente instalou.

```bash
python --version
dbt --version
```

Resultado esperado: `Python 3.12` e `dbt 1.12.6`. Se aparecer um aviso de versão mais nova, tudo bem: a versão foi fixada de propósito.

**5. Ao terminar de estudar.** Pare o codespace no menu **Codespaces → Stop**, para não gastar a cota gratuita.

### 1.5 · Régua de maturidade

O faturamento chegou errado na reunião e ninguém sabe por quê. Antes de mexer em qualquer coisa, o engenheiro de dados investiga, nesta ordem: o número, os arquivos, o banco, a regra e os testes.

**1. Reproduzir o problema.** O primeiro comando carrega os CSVs no banco. O segundo constrói os modelos do dbt. O terceiro mostra o faturamento que foi para o relatório.

```bash
python -m src.ingestao
dbt run
python scripts/faturamento.py
```

Resultado esperado: `3`, `3` e `6` linhas carregadas, `PASS=3` no dbt e `Faturamento de outubro: R$ 153,00 em 5 pedidos`. O pipeline roda sem erro, mas o financeiro fechou `R$ 63,10`.

**2. Olhar os arquivos.** O que chegou da origem: seis pedidos. Repare no status do pedido 6.

```bash
code data/pedidos.csv
```

**3. Olhar o banco.** Conta os pedidos de cada status na camada `raw`, do jeito que chegaram.

```bash
python scripts/consultar.py "select status, count(*) as pedidos from raw.pedidos group by status order by status"
```

Resultado esperado: aberto 1, cancelado 1, estornado 1 e pago 3. Os seis pedidos chegaram inteiros, então o problema não está na ingestão. Existe um status que ninguém conhecia: `estornado`.

**4. Seguir o caminho do dado.** A ingestão lê cada CSV e grava na camada `raw`. O staging padroniza: converte a data e deixa o status em minúsculo.

```bash
code src/ingestao.py
code models/staging/stg_pedidos.sql
```

**5. Olhar a regra de negócio.** Valor total é quantidade vezes preço, e só o pedido cancelado sai do faturamento. A regra não sabe o que é estorno.

```bash
code models/marts/fct_pedidos.sql
```

**6. Confirmar a suspeita.** Mostra os pedidos que entraram no faturamento.

```bash
python scripts/consultar.py "select id_pedido, valor_total from main.fct_pedidos order by id_pedido"
```

Resultado esperado: o pedido 6, de `89.9`, está no faturamento. É exatamente a diferença entre `R$ 153,00` e `R$ 63,10`: um dinheiro que voltou para o cliente foi somado.

**7. Olhar os testes.** Procura a pasta de testes do projeto.

```bash
ls tests
```

Resultado esperado: `No such file or directory`. Não existe nenhum teste, por isso nada avisou antes da reunião.

**8. Avaliar na régua.** A avaliação é feita nos slides da aula: volte para a apresentação.

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
