# dataops-curso-historia

Projeto prático do curso **Engenharia de Dados: DataOps, CI/CD e Liderança Técnica** (Alura), com Bruno Corrêa.

Ao longo das aulas, um pipeline de dados de uma loja (pedidos, clientes e produtos) sai do nível 1 de maturidade, com scripts que funcionam mas sem testes nem automação, e chega a um projeto com testes, CI/CD, padrões de código e métricas.

## O caso

Na reunião de resultados, o relatório mostrou um faturamento de outubro diferente do que o financeiro fechou, e ninguém soube explicar de onde veio o número. Você é o engenheiro de dados da loja: ao longo das aulas, vai investigar o erro, corrigir e garantir que ele não volte.

## Comandos da Aula 4 · Padrões técnicos e code review

Roteiro da aula: copie um bloco de cada vez (botão de copiar no canto do bloco), cole no terminal do Codespace e confira o resultado.

Na reunião, ninguém soube explicar a regra do faturamento: ela só existia no código. Nesta aula, o time combina padrões, revisa o código em todo pull request e escreve as decisões em ADRs.

### 4.1 · Padrões técnicos do time

**1. Criar a branch e ver o histórico.** O `git log --oneline` mostra um commit por linha, com os prefixos `feat`, `fix`, `test` e `ci`.

```bash
git switch -c padroes/pre-commit
git log --oneline
```

**2. Trazer os ADRs.** O primeiro registra por que o time escolheu o dbt. O segundo escreve a regra do faturamento, a que ninguém soube explicar na reunião.

```bash
git checkout origin/aula-04-padroes -- docs/adr/0001-escolha-do-dbt.md docs/adr/0002-regra-do-faturamento.md
code docs/adr/0001-escolha-do-dbt.md
code docs/adr/0002-regra-do-faturamento.md
```

### 4.2 · Automatizando com pre-commit

**1. Trazer a configuração.** O `.pre-commit-config.yaml` tem os hooks de higiene, o ruff e o sqlfluff. O `.sqlfluff` diz que o SQL é DuckDB e usa o dbt.

```bash
git checkout origin/aula-04-padroes -- .pre-commit-config.yaml .sqlfluff
code .pre-commit-config.yaml
code .sqlfluff
```

**2. Ativar e rodar em todos os arquivos.** O `install` liga o pre-commit nos commits. O `run --all-files` roda as verificações agora.

```bash
pre-commit install
pre-commit run --all-files
```

Resultado esperado: na primeira vez ele instala as ferramentas (alguns minutos), e o `ruff format` mostra `Failed` com `4 files reformatted`.

**3. Ver o que ele arrumou.**

```bash
git diff
```

**4. Rodar de novo.**

```bash
git add .
pre-commit run --all-files
```

Resultado esperado: tudo `Passed`.

**5. Trazer o CI que roda o pre-commit.**

```bash
git checkout origin/aula-04-padroes -- .github/workflows/ci.yml
```

### 4.3 · Code review eficaz

**1. Trazer o template de pull request e o CODEOWNERS.**

```bash
git checkout origin/aula-04-padroes -- .github/pull_request_template.md .github/CODEOWNERS
code .github/pull_request_template.md
code .github/CODEOWNERS
```

**2. Enviar para o GitHub.** Repare que o pre-commit roda sozinho no commit.

```bash
git add .
git commit -m "chore: padroes automatizados com pre-commit"
git push -u origin padroes/pre-commit
```

**3. Revisar o pull request.** Abra o pull request: a descrição já vem com o template. Na aba **Files changed**, revise seguindo a ordem: correção, impacto em dados, testes, performance, segurança e legibilidade.

**4. Merge e aprovação.** Com o check verde: **Merge pull request**, depois **Actions → Review deployments → Approve and deploy**.

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
├── scripts/           faturamento, consultas e deploy
├── docs/              documentação do time
├── dbt_project.yml
├── profiles.yml
└── requirements.txt
```
