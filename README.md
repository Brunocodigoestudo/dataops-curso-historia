# dataops-curso-historia

Projeto prático do curso **Engenharia de Dados: DataOps, CI/CD e Liderança Técnica** (Alura), com Bruno Corrêa.

Ao longo das aulas, um pipeline de dados de uma loja (pedidos, clientes e produtos) sai do nível 1 de maturidade, com scripts que funcionam mas sem testes nem automação, e chega a um projeto com testes, CI/CD, padrões de código e métricas.

## O caso

Na reunião de resultados, o relatório mostrou um faturamento de outubro diferente do que o financeiro fechou, e ninguém soube explicar de onde veio o número. Você é o engenheiro de dados da loja: ao longo das aulas, vai investigar o erro, corrigir e garantir que ele não volte.

## Comandos da Aula 3 · CI/CD para pipelines de dados

Roteiro da aula: copie um bloco de cada vez (botão de copiar no canto do bloco), cole no terminal do Codespace e confira o resultado. Nesta aula você trabalha na própria branch `aula-03-ci-cd`, que já tem o CI e o deploy prontos.

O faturamento foi corrigido na Aula 2, mas nada impede que alguém traga a regra antiga de volta sem rodar os testes. Nesta aula, o GitHub passa a rodar os testes sozinho e a barrar esse erro antes da produção.

Para o aluno: para rodar o CI e mexer nas configurações, você precisa de uma cópia do repositório na sua conta. Clique em **Fork**, desmarque **Copy the main branch only** (para vir com todas as branches) e, na aba **Actions** da sua cópia, habilite os workflows.

### Antes de começar · entrar na branch da aula

Na Aula 2 você criou os testes e corrigiu a regra no seu Codespace. A branch da Aula 3 já começa com tudo isso pronto. O `git reset --hard` descarta as correções feitas à mão, e o `git clean -fd` apaga os arquivos de teste criados na aula, para a troca de branch funcionar.

```bash
# git reset --hard: descarta as mudanças feitas nos arquivos e volta ao que está salvo no Git
git reset --hard
# git clean -fd: apaga os arquivos e pastas novos que o Git ainda não conhece
git clean -fd
# git switch: troca para outra branch. Aqui, a branch da Aula 3
git switch aula-03-ci-cd
# Roda a ingestão: lê os CSVs da pasta data/ e grava no banco (camada raw)
python -m src.ingestao
```

Resultado esperado: `Switched to a new branch 'aula-03-ci-cd'` e `1000`, `1000` e `3000` linhas carregadas.

O vídeo 3.1 é só de slides, sem comandos.

### 3.2 · Os blocos de um workflow

**1. Ler o workflow.** Leia de cima para baixo: `on` (quando roda), `jobs` e `runs-on` (o que roda e em qual máquina), `steps` (a sequência de passos).

```bash
# code: abre o workflow do CI, as instruções que o GitHub segue em todo pull request
code .github/workflows/ci.yml
```

**2. Criar uma branch de trabalho e trazer o erro da reunião, de propósito.** O `git switch -c` cria uma branch nova a partir da branch da aula. O `git checkout` traz a regra antiga do faturamento, da Aula 1.

```bash
# git switch -c: cria uma branch nova e já entra nela
git switch -c ci/regra-antiga
# git checkout ... --: copia um arquivo de outra branch. Aqui, a regra antiga da Aula 1
git checkout origin/aula-01-inicio -- models/marts/fct_pedidos.sql
# git commit -am: salva no Git todas as mudanças, com uma mensagem
git commit -am "test: regra antiga do faturamento de volta"
# git push: envia a branch para o GitHub. O -u liga a branch local à do GitHub
git push -u origin ci/regra-antiga
```

**3. Abrir o pull request.** No GitHub, clique em **Compare & pull request**. Em **base**, escolha `aula-03-ci-cd` (no fork, escolha também o seu repositório em **base repository**) e clique em **Create pull request**.

Resultado esperado: o check `qualidade` fica vermelho. No log, o step **Build e testes do dbt** mostra o `FAIL` do unit test `valor_total_ignora_estornados`. O erro da reunião foi barrado antes da produção.

**4. Desfazer.** O `git revert` cria um commit que desfaz o anterior.

```bash
# git revert: cria um commit que desfaz o último commit (HEAD)
git revert HEAD --no-edit
# git push: envia os commits para o GitHub
git push
```

Resultado esperado: o check volta a ficar verde.

**5. Fechar o pull request.** No GitHub, clique em **Close pull request**. No Codespace, volte para a branch da aula:

```bash
# git switch: troca para outra branch. Aqui, a branch da Aula 3
git switch aula-03-ci-cd
```

### 3.3 · Environments, secrets e aprovação

**1. Criar os ambientes e o secret no GitHub.** Em **Settings** do repositório:

- **Environments → New environment:** `staging` → **Configure environment**.
- **Environments → New environment:** `production` → marque **Required reviewers**, adicione o seu usuário → **Save protection rules**.
- **Secrets and variables → Actions → New repository secret:** nome `EXEMPLO_SECRET`, valor `ensaio123`.

**2. Ler os arquivos do deploy.** Um banco por ambiente, o script de deploy e o workflow de CD.

```bash
# Abre o profiles.yml: um banco para cada ambiente (dev, ci, staging e production)
code profiles.yml
# Abre o script de deploy: carrega os dados e roda o dbt build no ambiente escolhido
code scripts/deploy.sh
# Abre o workflow de deploy: testes, staging, aprovação e produção
code .github/workflows/cd.yml
```

**3. Testar o deploy no Codespace.** Roda o deploy simulado no ambiente de staging.

```bash
# Roda o deploy no staging. O EXEMPLO_SECRET faz o papel de uma senha
EXEMPLO_SECRET=teste bash scripts/deploy.sh staging
```

Resultado esperado: `PASS=12` e `Deploy em staging concluído`.

**4. Rodar o deploy no GitHub e aprovar a produção.** Na aba **Actions**, clique em **Deploy do pipeline → Run workflow**, escolha a branch `aula-03-ci-cd` e clique em **Run workflow**. Espere os testes e o staging ficarem verdes, clique em **Review deployments → production → Approve and deploy**.

Resultado esperado: os três jobs verdes. No log, o secret aparece como `***`.

### 3.4 · Protegendo a branch

**1. Criar a regra de proteção.** Em **Settings → Branches → Add classic branch protection rule**:

- **Branch name pattern:** `aula-03-ci-cd` (num projeto real, é a `main`).
- Marque **Require a pull request before merging** e desmarque **Require approvals**.
- Marque **Require status checks to pass before merging** e escolha `qualidade`.
- Marque **Do not allow bypassing the above settings**.
- Clique em **Create**.

**2. Quebrar de propósito e enviar.** Cria uma branch de teste com a regra antiga do faturamento.

```bash
# git switch -c: cria uma branch de teste e já entra nela
git switch -c teste/ci-vermelho
# git checkout ... --: copia um arquivo de outra branch. Aqui, a regra antiga da Aula 1
git checkout origin/aula-01-inicio -- models/marts/fct_pedidos.sql
# git commit -am: salva no Git todas as mudanças, com uma mensagem
git commit -am "test: merge bloqueado"
# git push: envia a branch de teste para o GitHub
git push -u origin teste/ci-vermelho
```

**3. Ver o merge bloqueado.** No GitHub, abra o pull request com **base** `aula-03-ci-cd`: com o CI vermelho, o botão de merge não libera. Depois clique em **Close pull request**.

**4. Limpar.** Volta para a branch da aula e apaga a branch de teste.

```bash
# git switch: troca para outra branch. Aqui, a branch da Aula 3
git switch aula-03-ci-cd
# git branch -D: apaga a branch de teste, que não é mais necessária
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
