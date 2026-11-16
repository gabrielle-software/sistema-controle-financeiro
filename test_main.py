"""Testes automatizados do Sistema de Controle Financeiro."""
import sqlite3
import tempfile
import unittest
from pathlib import Path

from main import (
    adicionar_lancamento,
    calcular_saldo,
    editar_lancamento,
    excluir_lancamento,
    inicializar_banco,
    listar_lancamentos,
    relatorio_mensal,
    validar_lancamento,
    converter_para_centavos,
)


class TesteSistemaFinanceiro(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "teste.db"
        inicializar_banco(self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def cadastrar(self, tipo="receita", descricao="Salário", categoria="Trabalho",
                  valor=2500, data="2026-11-01"):
        return adicionar_lancamento(tipo, descricao, categoria, valor, data, self.db_path)

    def test_inicializa_banco_vazio(self):
        self.assertEqual(listar_lancamentos(self.db_path), [])

    def test_migra_banco_legado_para_centavos(self):
        legado = self.db_path
        with sqlite3.connect(legado) as conexao:
            conexao.execute("""
                CREATE TABLE lancamentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT NOT NULL,
                    descricao TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    valor REAL NOT NULL,
                    data TEXT NOT NULL
                )
            """)
            conexao.execute(
                """INSERT INTO lancamentos
                   (id, tipo, descricao, categoria, valor, data)
                   VALUES (7, 'receita', 'Pagamento', 'Trabalho', 123.45, '2026-10-05')"""
            )
            conexao.execute(
                """INSERT INTO lancamentos
                   (id, tipo, descricao, categoria, valor, data)
                   VALUES (8, 'despesa', 'Mercado', 'Casa', 10.99, '2026-10-06')"""
            )

        inicializar_banco(legado)

        with sqlite3.connect(legado) as conexao:
            colunas = {linha[1] for linha in conexao.execute(
                "PRAGMA table_info(lancamentos)"
            )}
            registros = conexao.execute(
                "SELECT id, valor_centavos FROM lancamentos ORDER BY id"
            ).fetchall()

        self.assertIn("valor_centavos", colunas)
        self.assertNotIn("valor", colunas)
        self.assertEqual(registros, [(7, 12345), (8, 1099)])
        itens = listar_lancamentos(legado)
        self.assertEqual([item["valor"] for item in itens], [123.45, 10.99])

    def test_migracao_pode_ser_executada_mais_de_uma_vez(self):
        legado = self.db_path
        with sqlite3.connect(legado) as conexao:
            conexao.execute("""
                CREATE TABLE lancamentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT NOT NULL,
                    descricao TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    valor REAL NOT NULL,
                    data TEXT NOT NULL
                )
            """)
            conexao.execute(
                """INSERT INTO lancamentos
                   (tipo, descricao, categoria, valor, data)
                   VALUES ('receita', 'Pagamento', 'Trabalho', 50.25, '2026-10-05')"""
            )

        inicializar_banco(legado)
        inicializar_banco(legado)

        itens = listar_lancamentos(legado)
        self.assertEqual(len(itens), 1)
        self.assertEqual(itens[0]["valor"], 50.25)

    def test_cadastra_receita(self):
        identificador = self.cadastrar()
        self.assertEqual(identificador, 1)
        self.assertEqual(len(listar_lancamentos(self.db_path)), 1)

    def test_cadastra_despesa(self):
        self.cadastrar("despesa", "Aluguel", "Moradia", 900)
        self.assertEqual(listar_lancamentos(self.db_path)[0]["tipo"], "despesa")

    def test_rejeita_tipo_invalido(self):
        with self.assertRaises(ValueError):
            self.cadastrar(tipo="transferência")

    def test_rejeita_descricao_vazia(self):
        with self.assertRaises(ValueError):
            self.cadastrar(descricao="  ")

    def test_rejeita_categoria_vazia(self):
        with self.assertRaises(ValueError):
            self.cadastrar(categoria="")

    def test_rejeita_valor_nao_numerico(self):
        with self.assertRaises(ValueError):
            self.cadastrar(valor="abc")

    def test_rejeita_valor_zero_ou_negativo(self):
        for valor in (0, -10):
            with self.subTest(valor=valor), self.assertRaises(ValueError):
                self.cadastrar(valor=valor)

    def test_rejeita_valores_nao_finitos(self):
        for valor in ("NaN", "inf", "-inf"):
            with self.subTest(valor=valor), self.assertRaises(ValueError):
                self.cadastrar(valor=valor)

    def test_converte_valores_para_centavos_exatamente(self):
        self.assertEqual(converter_para_centavos("10,99"), 1099)
        self.assertEqual(converter_para_centavos("0.10"), 10)

    def test_rejeita_mais_de_duas_casas_decimais(self):
        with self.assertRaises(ValueError):
            self.cadastrar(valor="10.999")

    def test_rejeita_data_invalida(self):
        with self.assertRaises(ValueError):
            self.cadastrar(data="01/11/2026")

    def test_valida_lancamento(self):
        self.assertEqual(
            validar_lancamento("receita", "Extra", "Outros", "12.50", "2026-11-02"),
            1250,
        )

    def test_edita_lancamento_existente(self):
        identificador = self.cadastrar()
        resultado = editar_lancamento(
            identificador, "despesa", "Conta de luz", "Casa", 180,
            "2026-11-03", self.db_path
        )
        self.assertTrue(resultado)
        item = listar_lancamentos(self.db_path)[0]
        self.assertEqual(item["descricao"], "Conta de luz")
        self.assertEqual(item["tipo"], "despesa")

    def test_edicao_de_id_inexistente(self):
        self.assertFalse(editar_lancamento(
            999, "receita", "Extra", "Outros", 50, "2026-11-03", self.db_path
        ))

    def test_exclui_lancamento(self):
        identificador = self.cadastrar()
        self.assertTrue(excluir_lancamento(identificador, self.db_path))
        self.assertEqual(listar_lancamentos(self.db_path), [])

    def test_exclusao_de_id_inexistente(self):
        self.assertFalse(excluir_lancamento(999, self.db_path))

    def test_calcula_saldo(self):
        self.cadastrar(valor=2000)
        self.cadastrar("despesa", "Mercado", "Alimentação", 350)
        self.assertEqual(calcular_saldo(self.db_path), 1650)

    def test_saldo_sem_lancamentos(self):
        self.assertEqual(calcular_saldo(self.db_path), 0)

    def test_relatorio_mensal(self):
        self.cadastrar(valor=2000, data="2026-11-01")
        self.cadastrar("despesa", "Mercado", "Alimentação", 300, "2026-11-10")
        self.cadastrar("receita", "Freelance", "Extra", 500, "2026-10-10")
        relatorio = relatorio_mensal(2026, 11, self.db_path)
        self.assertEqual(relatorio, {"receitas": 2000, "despesas": 300, "saldo": 1700})

    def test_relatorio_rejeita_mes_invalido(self):
        with self.assertRaises(ValueError):
            relatorio_mensal(2026, 13, self.db_path)

    def test_lista_lancamentos_com_campos(self):
        self.cadastrar()
        item = listar_lancamentos(self.db_path)[0]
        self.assertEqual(
            set(item),
            {"id", "tipo", "descricao", "categoria", "valor", "data"},
        )


if __name__ == "__main__":
    unittest.main()
