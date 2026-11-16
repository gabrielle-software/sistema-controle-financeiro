"""Sistema de Controle Financeiro Pessoal.

Aplicação de linha de comando com persistência em SQLite.
"""
from contextlib import contextmanager
from datetime import date, datetime
import math
from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).with_name("financeiro.db")
TIPOS_VALIDOS = {"receita", "despesa"}


@contextmanager
def conectar(db_path=DB_PATH):
    """Abre uma conexão e garante seu fechamento ao terminar a operação."""
    conexao = sqlite3.connect(db_path)
    try:
        yield conexao
        conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.close()


def inicializar_banco(db_path=DB_PATH):
    """Cria a tabela de lançamentos caso ainda não exista."""
    with conectar(db_path) as conexao:
        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS lancamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL CHECK(tipo IN ('receita', 'despesa')),
                descricao TEXT NOT NULL,
                categoria TEXT NOT NULL,
                valor REAL NOT NULL CHECK(valor > 0),
                data TEXT NOT NULL
            )
            """
        )


def validar_lancamento(tipo, descricao, categoria, valor, data_lancamento):
    """Valida os campos de um lançamento e retorna o valor numérico."""
    if tipo not in TIPOS_VALIDOS:
        raise ValueError("Tipo deve ser 'receita' ou 'despesa'.")
    if not isinstance(descricao, str) or not descricao.strip():
        raise ValueError("A descrição é obrigatória.")
    if not isinstance(categoria, str) or not categoria.strip():
        raise ValueError("A categoria é obrigatória.")
    try:
        valor = float(valor)
    except (TypeError, ValueError):
        raise ValueError("O valor deve ser numérico.") from None
    if not math.isfinite(valor):
        raise ValueError("O valor deve ser um número finito.")
    if valor <= 0:
        raise ValueError("O valor deve ser maior que zero.")
    try:
        datetime.strptime(data_lancamento, "%Y-%m-%d")
    except (TypeError, ValueError):
        raise ValueError("A data deve estar no formato AAAA-MM-DD.") from None
    return valor


def adicionar_lancamento(tipo, descricao, categoria, valor, data_lancamento=None, db_path=DB_PATH):
    """Cadastra uma receita ou despesa e retorna o ID criado."""
    data_lancamento = data_lancamento or date.today().isoformat()
    valor = validar_lancamento(tipo, descricao, categoria, valor, data_lancamento)
    with conectar(db_path) as conexao:
        cursor = conexao.execute(
            """INSERT INTO lancamentos (tipo, descricao, categoria, valor, data)
               VALUES (?, ?, ?, ?, ?)""",
            (tipo, descricao.strip(), categoria.strip(), valor, data_lancamento),
        )
        return cursor.lastrowid


def editar_lancamento(lancamento_id, tipo, descricao, categoria, valor, data_lancamento, db_path=DB_PATH):
    """Atualiza um lançamento existente; retorna True se encontrou o ID."""
    valor = validar_lancamento(tipo, descricao, categoria, valor, data_lancamento)
    with conectar(db_path) as conexao:
        cursor = conexao.execute(
            """UPDATE lancamentos
               SET tipo = ?, descricao = ?, categoria = ?, valor = ?, data = ?
               WHERE id = ?""",
            (tipo, descricao.strip(), categoria.strip(), valor, data_lancamento, lancamento_id),
        )
        return cursor.rowcount > 0


def excluir_lancamento(lancamento_id, db_path=DB_PATH):
    """Exclui um lançamento e informa se ele existia."""
    with conectar(db_path) as conexao:
        cursor = conexao.execute("DELETE FROM lancamentos WHERE id = ?", (lancamento_id,))
        return cursor.rowcount > 0


def listar_lancamentos(db_path=DB_PATH):
    """Retorna todos os lançamentos ordenados da data mais recente."""
    with conectar(db_path) as conexao:
        linhas = conexao.execute(
            """SELECT id, tipo, descricao, categoria, valor, data
               FROM lancamentos ORDER BY data DESC, id DESC"""
        ).fetchall()
    return [
        {"id": linha[0], "tipo": linha[1], "descricao": linha[2],
         "categoria": linha[3], "valor": linha[4], "data": linha[5]}
        for linha in linhas
    ]


def calcular_saldo(db_path=DB_PATH):
    """Calcula receitas menos despesas."""
    with conectar(db_path) as conexao:
        receitas = conexao.execute(
            "SELECT COALESCE(SUM(valor), 0) FROM lancamentos WHERE tipo = 'receita'"
        ).fetchone()[0]
        despesas = conexao.execute(
            "SELECT COALESCE(SUM(valor), 0) FROM lancamentos WHERE tipo = 'despesa'"
        ).fetchone()[0]
    return receitas - despesas


def relatorio_mensal(ano, mes, db_path=DB_PATH):
    """Retorna totais de receitas, despesas e saldo para um mês."""
    if not 1 <= int(mes) <= 12:
        raise ValueError("Mês deve estar entre 1 e 12.")
    prefixo = f"{int(ano):04d}-{int(mes):02d}-"
    with conectar(db_path) as conexao:
        receitas = conexao.execute(
            "SELECT COALESCE(SUM(valor), 0) FROM lancamentos WHERE tipo='receita' AND data LIKE ?",
            (prefixo + "%",),
        ).fetchone()[0]
        despesas = conexao.execute(
            "SELECT COALESCE(SUM(valor), 0) FROM lancamentos WHERE tipo='despesa' AND data LIKE ?",
            (prefixo + "%",),
        ).fetchone()[0]
    return {"receitas": receitas, "despesas": despesas, "saldo": receitas - despesas}


def exibir_menu():
    print("\n=== SISTEMA DE CONTROLE FINANCEIRO ===")
    print("1. Cadastrar receita")
    print("2. Cadastrar despesa")
    print("3. Listar lançamentos")
    print("4. Consultar saldo")
    print("5. Relatório mensal")
    print("6. Editar lançamento")
    print("7. Excluir lançamento")
    print("0. Sair")


def executar():
    inicializar_banco()
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()
        try:
            if opcao in {"1", "2"}:
                tipo = "receita" if opcao == "1" else "despesa"
                descricao = input("Descrição: ")
                categoria = input("Categoria: ")
                valor = input("Valor: ").replace(",", ".")
                data_lancamento = input("Data (AAAA-MM-DD, vazio para hoje): ").strip() or None
                novo_id = adicionar_lancamento(tipo, descricao, categoria, valor, data_lancamento)
                print(f"Lançamento cadastrado com ID {novo_id}.")
            elif opcao == "3":
                for item in listar_lancamentos():
                    print(f"#{item['id']} | {item['data']} | {item['tipo']} | "
                          f"{item['descricao']} | {item['categoria']} | R$ {item['valor']:.2f}")
            elif opcao == "4":
                print(f"Saldo atual: R$ {calcular_saldo():.2f}")
            elif opcao == "5":
                ano = int(input("Ano (AAAA): "))
                mes = int(input("Mês (1-12): "))
                relatorio = relatorio_mensal(ano, mes)
                print(f"Receitas: R$ {relatorio['receitas']:.2f}")
                print(f"Despesas: R$ {relatorio['despesas']:.2f}")
                print(f"Saldo do mês: R$ {relatorio['saldo']:.2f}")
            elif opcao == "6":
                lancamento_id = int(input("ID do lançamento: "))
                descricao = input("Nova descrição: ")
                categoria = input("Nova categoria: ")
                tipo = input("Tipo (receita/despesa): ").strip().lower()
                valor = input("Novo valor: ").replace(",", ".")
                data_lancamento = input("Nova data (AAAA-MM-DD): ").strip()
                if editar_lancamento(lancamento_id, tipo, descricao, categoria, valor, data_lancamento):
                    print("Lançamento atualizado.")
                else:
                    print("Lançamento não encontrado.")
            elif opcao == "7":
                lancamento_id = int(input("ID do lançamento: "))
                if excluir_lancamento(lancamento_id):
                    print("Lançamento excluído.")
                else:
                    print("Lançamento não encontrado.")
            elif opcao == "0":
                print("Até logo!")
                break
            else:
                print("Opção inválida.")
        except (ValueError, sqlite3.Error) as erro:
            print(f"Não foi possível concluir a operação: {erro}")


if __name__ == "__main__":
    executar()
