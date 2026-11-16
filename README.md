# Sistema de Controle Financeiro | Personal Finance Management System

[![Testes automatizados](https://github.com/gabrielle-software/sistema-controle-financeiro/actions/workflows/tests.yml/badge.svg)](https://github.com/gabrielle-software/sistema-controle-financeiro/actions/workflows/tests.yml)

Aplicação de linha de comando desenvolvida em **Python** para registrar receitas e despesas, acompanhar o saldo e consultar relatórios mensais. O projeto demonstra práticas de organização de código, persistência com SQLite, validação de dados, precisão monetária e testes automatizados.

> **Status:** os 24 testes automatizados passaram na execução mais recente do GitHub Actions em 16/11/2026.

## 🇧🇷 Português

### Funcionalidades

- Cadastro de receitas e despesas.
- Listagem de lançamentos por data.
- Edição e exclusão de lançamentos.
- Organização por descrição e categoria.
- Registro de valores e datas.
- Cálculo automático do saldo (receitas menos despesas).
- Relatório mensal com totais de receitas, despesas e saldo.
- Persistência local dos dados em banco SQLite.
- Validação de campos, datas e valores informados.
- Migração de bancos legados para o armazenamento monetário em centavos inteiros.
- Testes automatizados e integração contínua com GitHub Actions.

### Tecnologias e conceitos

- **Python 3.12** — lógica da aplicação e regras de negócio.
- **SQLite** — armazenamento persistente.
- **Decimal** — tratamento preciso de valores monetários.
- **unittest** — testes automatizados.
- **Git e GitHub** — versionamento e hospedagem do código.
- **GitHub Actions** — execução automatizada dos testes.

### Como executar

**Pré-requisito:** Python 3.12 ou superior.

1. Clone o repositório:

   ```bash
   git clone https://github.com/gabrielle-software/sistema-controle-financeiro.git
   ```

2. Acesse a pasta do projeto:

   ```bash
   cd sistema-controle-financeiro
   ```

3. Inicie a aplicação:

   ```bash
   python main.py
   ```

O arquivo `financeiro.db` será criado automaticamente na pasta do projeto na primeira execução.

### Como executar os testes

Na pasta do projeto, execute:

```bash
python -m unittest -v
```

Os testes utilizam bancos de dados temporários, mantendo os dados financeiros locais separados dos dados usados na validação automatizada.

### Estrutura do projeto

```text
sistema-controle-financeiro/
├── .github/
│   └── workflows/
│       └── tests.yml
├── main.py
├── test_main.py
└── README.md
```

### Decisões técnicas

- Os valores monetários são armazenados como **centavos inteiros**, evitando imprecisões comuns em operações com ponto flutuante.
- A conversão e validação de valores utilizam `Decimal`.
- As operações com SQLite utilizam parâmetros nas consultas e garantem o encerramento das conexões.
- O projeto inclui migração de dados de uma estrutura antiga para o formato atual de centavos inteiros.
- O GitHub Actions executa a suíte de testes a cada atualização enviada ao repositório.

### Testes e integração contínua

A suíte é executada com `unittest`. Na última execução verificada, **24 testes foram executados e aprovados**.

[Consultar execuções do GitHub Actions](https://github.com/gabrielle-software/sistema-controle-financeiro/actions)

### Objetivo de aprendizagem

Este projeto foi criado para consolidar conhecimentos práticos de Python e Engenharia de Software, especialmente CRUD, persistência de dados, validação, tratamento de valores monetários, migração de banco de dados, testes e integração contínua.

---

## 🇺🇸 English

### Overview

A Python command-line application for recording income and expenses, tracking the current balance, and generating monthly reports. The project demonstrates software engineering practices including code organization, SQLite persistence, input validation, monetary precision, database migration, and automated testing.

### Features

- Add income and expense transactions.
- List transactions by date.
- Edit and delete transactions.
- Organize records by description and category.
- Store transaction dates and amounts.
- Automatically calculate the balance (income minus expenses).
- Generate monthly income, expense, and balance reports.
- Persist data locally with SQLite.
- Validate input fields, dates, and monetary amounts.
- Migrate legacy databases to integer-cent storage.
- Run automated tests through GitHub Actions.

### Technologies

- **Python 3.12**
- **SQLite**
- **Decimal**
- **unittest**
- **Git and GitHub**
- **GitHub Actions**

### Requirements

Python 3.12 or newer.

### Run the application

1. Clone the repository:

   ```bash
   git clone https://github.com/gabrielle-software/sistema-controle-financeiro.git
   ```

2. Navigate to the project directory:

   ```bash
   cd sistema-controle-financeiro
   ```

3. Run the application:

   ```bash
   python main.py
   ```

The `financeiro.db` database file is automatically created in the project directory on first run.

### Run the tests

```bash
python -m unittest -v
```

Tests use temporary databases to keep test data separate from the application's local financial records.

### Technical notes

- Monetary amounts are stored as **integer cents** to avoid floating-point precision issues.
- `Decimal` is used to convert and validate monetary values.
- SQLite operations use parameterized queries and safely close database connections.
- The application includes a migration path from the legacy database format to integer-cent storage.
- GitHub Actions runs the automated test suite whenever changes are pushed to the repository.

### Continuous integration

The latest verified workflow run executed and passed **24 automated tests**.

[View GitHub Actions runs](https://github.com/gabrielle-software/sistema-controle-financeiro/actions)

### Learning goals

This project supports hands-on learning in Python and software engineering, with a focus on CRUD operations, data persistence, validation, monetary calculations, database migration, automated testing, and continuous integration.

---

**Repository:** https://github.com/gabrielle-software/sistema-controle-financeiro
