"""Testes automatizados do Sistema de Controle Financeiro."""
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

    def test_rejeita_data_invalida(self):
        with self.assertRaises(ValueError):
            self.cadastrar(data="01/11/2026")

    def test_valida_lancamento(self):
        self.assertEqual(
            validar_lancamento("receita", "Extra", "Outros", "12.50", "2026-11-02"),
            12.5,
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
        self.assertAlmostEqual(calcular_saldo(self.db_path), 1650)

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
