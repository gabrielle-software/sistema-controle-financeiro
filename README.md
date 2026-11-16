# Sistema de Controle Financeiro

Projeto desenvolvido em Python para praticar fundamentos de Engenharia de Software, persistência de dados, organização de código e testes automatizados.

## Funcionalidades

- Cadastro de receitas e despesas
- Edição e exclusão de lançamentos
- Organização por descrição e categoria
- Registro de data e valor
- Cálculo automático do saldo (receitas menos despesas)
- Relatório mensal de receitas, despesas e saldo
- Armazenamento persistente com SQLite, guardando valores em centavos inteiros para evitar erros de arredondamento
- Testes automatizados com `unittest`
- Integração contínua com GitHub Actions

## Tecnologias

- Python 3.12
- SQLite
- unittest
- Git e GitHub
- GitHub Actions

## Como executar

1. Tenha o Python 3.12 ou superior instalado.
2. Clone este repositório:
   `git clone https://github.com/gabrielle-software/sistema-controle-financeiro.git`
3. Entre na pasta:
   `cd sistema-controle-financeiro`
4. Execute:
   `python main.py`

O banco de dados `financeiro.db` será criado automaticamente na pasta do projeto na primeira execução.

## Como executar os testes

Na pasta do projeto, execute:

```bash
python -m unittest -v
```

Os testes usam bancos temporários, sem alterar seus dados financeiros reais.

## Estrutura

```text
sistema-controle-financeiro/
├── .github/
│   └── workflows/
│       └── tests.yml
├── main.py
├── test_main.py
└── README.md
```

---

# Personal Finance Management System

A Python command-line application created to practice software engineering fundamentals, data persistence, code organization, and automated testing.

## Features

- Add income and expenses
- Edit and delete transactions
- Organize transactions by description and category
- Store dates and amounts
- Automatically calculate the balance (income minus expenses)
- Generate monthly income, expense, and balance reports
- Persistent storage with SQLite, storing amounts as integer cents to avoid rounding errors
- Automated tests with `unittest`
- Continuous integration with GitHub Actions

## Technologies

- Python 3.12
- SQLite
- unittest
- Git and GitHub
- GitHub Actions

## Run the application

1. Install Python 3.12 or newer.
2. Clone this repository:
   `git clone https://github.com/gabrielle-software/sistema-controle-financeiro.git`
3. Open the project folder:
   `cd sistema-controle-financeiro`
4. Run:
   `python main.py`

The `financeiro.db` database file is created automatically in the project folder on first run.

## Run the tests

```bash
python -m unittest -v
```

Tests use temporary databases and do not modify your personal finance data.
