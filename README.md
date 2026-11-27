# dataops-curso-historia

Projeto prático do curso **Engenharia de Dados: DataOps, CI/CD e Liderança Técnica** (Alura), com Bruno Corrêa.

Ao longo das aulas, um pipeline de dados de uma loja (pedidos, clientes e produtos) sai do nível 1 de maturidade, com scripts que funcionam mas sem testes nem automação, e chega a um projeto com testes, CI/CD, padrões de código e métricas.

## O caso

Na reunião de resultados, o relatório mostrou um faturamento de outubro diferente do que o financeiro fechou, e ninguém soube explicar de onde veio o número. Você é o engenheiro de dados da loja: ao longo das aulas, vai investigar o erro, corrigir e garantir que ele não volte.

## Comandos da Aula 3 · CI/CD para pipelines de dados

Roteiro da aula: copie um bloco de cada vez (botão de copiar no canto do bloco), cole no terminal do Codespace e confira o resultado. A partir daqui, toda mudança vai por branch e pull request.

O faturamento foi corrigido na Aula 2, mas nada impede que alguém traga a regra antiga de volta sem rodar os testes. Nesta aula, o GitHub passa a rodar os testes sozinho e a barrar esse erro antes da produção.

Antes de começar: para rodar o CI e mexer nas configurações, você precisa de uma cópia do repositório na sua conta. Clique em **Fork**, desmarque **Copy the main branch only** (para vir com todas as branches) e, na aba **Actions** da sua cópia, habilite os workflows.

O vídeo 3.1 é só de slides, sem comandos.

### 3.2 · Os blocos de um workflow

**1. Criar a branch e trazer o workflow.** O `git switch -c` cria uma branch nova e já entra nela.

```bash
git switch -c ci/primeiro-workflow
git checkout origin/aula-03-ci-cd -- .github/workflows/ci.yml
code .github/workflows/ci.yml
```

Leia de cima para baixo: `on` (quando roda), `jobs` e `runs-on` (o que roda e em qual máquina), `steps` (a sequência de passos).

**2. Enviar a branch para o GitHub.**

```bash
git add .
git commit -m "ci: workflow de qualidade"
git push -u origin ci/primeiro-workflow
```

**3. Abrir o pull request.** No GitHub, clique em **Compare & pull request → Create pull request** e espere o check `qualidade` ficar verde.

**4. Ver o CI ficar vermelho, de propósito.** O primeiro comando traz de volta a regra antiga do faturamento, da Aula 1, a que gerou o número errado da reunião. Os outros enviam a mudança.

```bash
git checkout origin/aula-01-inicio -- models/marts/fct_pedidos.sql
git commit -am "test: regra antiga do faturamento de volta"
git push
```

Resultado esperado: o check fica vermelho no pull request. No log, o step **Build e testes do dbt** mostra o `FAIL` do unit test `valor_total_ignora_estornados`. O erro da reunião foi barrado antes da produção.

**5. Desfazer.** O `git revert` cria um commit que desfaz o anterior.

```bash
git revert HEAD --no-edit
git push
```

Resultado esperado: o check volta a ficar verde. Não faça o merge ainda.

### 3.3 · Environments, secrets e aprovação

**1. Criar os ambientes e o secret no GitHub.** Em **Settings** do seu repositório:

- **Environments → New environment:** `staging` → **Configure environment**.
- **Environments → New environment:** `production` → marque **Required reviewers**, adicione o seu usuário → **Save protection rules**.
- **Secrets and variables → Actions → New repository secret:** nome `EXEMPLO_SECRET`, valor `ensaio123`.

**2. Trazer os arquivos do deploy.** Um banco por ambiente, o script de deploy e o workflow de CD.

```bash
git checkout origin/aula-03-ci-cd -- profiles.yml scripts/deploy.sh .github/workflows/cd.yml
code profiles.yml
code scripts/deploy.sh
code .github/workflows/cd.yml
```

**3. Testar o deploy no Codespace.** Roda o deploy simulado no ambiente de staging.

```bash
EXEMPLO_SECRET=teste bash scripts/deploy.sh staging
```

Resultado esperado: `PASS=12` e `Deploy em staging concluído`.

**4. Enviar para o GitHub.**

```bash
git add .
git commit -m "ci: deploy com aprovacao"
git push
```

**5. Fazer o merge e aprovar a produção.** No pull request, com o check verde: **Merge pull request → Confirm merge**. Depois vá em **Actions → Deploy do pipeline**, clique em **Review deployments → production → Approve and deploy**. No log, o secret aparece como `***`.

**6. Voltar para a main atualizada.**

```bash
git switch main
git pull
```

### 3.4 · Protegendo a main

**1. Criar a regra de proteção.** Em **Settings → Branches → Add classic branch protection rule**:

- **Branch name pattern:** `main`.
- Marque **Require a pull request before merging** e desmarque **Require approvals**.
- Marque **Require status checks to pass before merging** e escolha `qualidade`.
- Marque **Do not allow bypassing the above settings**.
- Clique em **Create**.

**2. Criar uma branch de teste.**

```bash
git switch -c teste/ci-vermelho
```

**3. Quebrar de propósito e enviar.** Traz de novo a regra antiga do faturamento e envia a branch.

```bash
git checkout origin/aula-01-inicio -- models/marts/fct_pedidos.sql
git commit -am "test: merge bloqueado"
git push -u origin teste/ci-vermelho
```

**4. Ver o merge bloqueado.** Abra o pull request no GitHub: com o CI vermelho, o botão de merge não libera. Depois clique em **Close pull request**.

**5. Limpar.** Volta para a main e apaga a branch de teste.

```bash
git switch main
git branch -D teste/ci-vermelho
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
├── scripts/           faturamento, consultas e deploy
├── dbt_project.yml
├── profiles.yml
└── requirements.txt
```
