# dataops-curso-historia

Projeto prático do curso **Engenharia de Dados: DataOps, CI/CD e Liderança Técnica** (Alura), com Bruno Corrêa.

Ao longo das aulas, um pipeline de dados de uma loja (pedidos, clientes e produtos) sai do nível 1 de maturidade, com scripts que funcionam mas sem testes nem automação, e chega a um projeto com testes, CI/CD, padrões de código e métricas.

## O caso

Na reunião de resultados, o relatório mostrou um faturamento de outubro diferente do que o financeiro fechou, e ninguém soube explicar de onde veio o número. Você é o engenheiro de dados da loja: ao longo das aulas, vai investigar o erro, corrigir e garantir que ele não volte.

## Comandos da Aula 6 · Medindo a transformação DataOps

Roteiro da aula: copie um bloco de cada vez (botão de copiar no canto do bloco), cole no terminal do Codespace e confira o resultado.

A diretoria quer saber o que aconteceu com o faturamento e se o time melhorou. Nesta aula, o incidente vira um postmortem e as entregas viram métricas.

Antes de começar, no GitHub: **Issues → Labels → New label**, nome `incidente` → **Create label**.

### 6.1 · Postmortem sem culpados

**1. Abrir a issue do incidente.** No GitHub: **Issues → New issue**, título `Faturamento de outubro divergente na reunião`, label `incidente` → **Submit new issue**. A hora de abertura vira o "detectado" das métricas.

**2. Criar a branch e trazer o postmortem.** Conta a história da reunião, sem culpados: o que aconteceu, a causa raiz e as ações.

```bash
git switch main
git pull
git switch -c incidente/faturamento-divergente
git checkout origin/aula-06-metricas -- docs/postmortems/2026-11-faturamento-divergente.md
code docs/postmortems/2026-11-faturamento-divergente.md
```

Repare na lista de ações: cada causa virou um teste, uma automação ou um documento, e quase tudo já foi feito nas aulas anteriores.

**3. Enviar para o GitHub.**

```bash
git add .
git commit -m "docs: postmortem do faturamento divergente"
git push -u origin incidente/faturamento-divergente
```

**4. Publicar e fechar a issue.** Pull request, check verde, merge, aprovação da produção e, por fim, feche a issue do incidente.

### 6.2 · Métricas DORA

**1. Criar a branch e trazer o script.**

```bash
git switch main
git pull
git switch -c metricas/dora
git checkout origin/aula-06-metricas -- scripts/metricas_dora.py
code scripts/metricas_dora.py
```

**2. Apontar para o seu repositório.** Na linha do `REPO`, coloque o nome do seu repositório, no formato `usuario/repositorio`.

**3. Rodar o script.** Busca os dados na API do GitHub e calcula os deploys por semana e o lead time.

```bash
python scripts/metricas_dora.py
```

Com poucas semanas de histórico o número é pequeno. O que importa é acompanhar a tendência.

### 6.3 · Tempo de recuperação (MTTR)

**1. Ver a função do MTTR.** No mesmo `scripts/metricas_dora.py`, veja a função `recuperacao_horas`. Depois, no GitHub, abra a issue do faturamento divergente e compare com o tempo de recuperação que o script mostrou no terminal.

**2. Fechar a história.** Roda o pipeline inteiro de novo e mostra o faturamento do relatório.

```bash
python -m src.ingestao
dbt build
python scripts/faturamento.py
```

Resultado esperado: `PASS=12` e `Faturamento de outubro: R$ 63,10 em 4 pedidos`. O número do relatório bate com o do financeiro.

**3. Trazer o README final.**

```bash
git checkout origin/aula-06-metricas -- README.md
```

**4. Enviar para o GitHub.**

```bash
git add .
git commit -m "feat: metricas DORA"
git push -u origin metricas/dora
```

**5. Publicar.** Pull request, check verde, merge e aprovação da produção.

### 6.4 · A régua, antes e depois

Só slides, sem comandos.

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

## Documentação do time

- **Modelos e linhagem:** `dbt docs generate` e depois `dbt docs serve --no-browser`. No codespace, abra a porta 8080.
- **Quando um número chegar errado ou o pipeline falhar:** [docs/runbooks/incidente-de-dados.md](docs/runbooks/incidente-de-dados.md).
- **Decisões técnicas:** [docs/adr/](docs/adr/).

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
├── .devcontainer/          ambiente do Codespaces
├── .github/
│   ├── workflows/          ci.yml · cd.yml
│   ├── pull_request_template.md
│   └── CODEOWNERS
├── data/                   CSVs de origem
├── src/                    ingestao.py · transformacoes.py · pipeline.py
├── tests/                  testes pytest e teste singular do dbt
├── models/                 staging/ · marts/ (dbt)
├── scripts/                faturamento.py · consultar.py · deploy.sh · metricas_dora.py
├── docs/                   adr/ · runbooks/ · postmortems/
├── .pre-commit-config.yaml
├── .sqlfluff
├── dbt_project.yml
├── profiles.yml
└── requirements.txt
```
