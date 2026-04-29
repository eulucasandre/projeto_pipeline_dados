import json
import csv


class Dados:
    """
    Classe responsável por encapsular os dados brutos de uma fonte (JSON ou CSV),
    oferecendo métodos para leitura, transformação e persistência.
    """

    def __init__(self, origem, formato):
        self.origem = origem
        self.formato = formato
        self.registros = self._carregar_registros()
        self.colunas = self._extrair_colunas()
        self.total_linhas = self._contar_linhas()

    # ------------------------------------------------------------------ #
    #  Leitura                                                             #
    # ------------------------------------------------------------------ #

    def _ler_json(self):
        with open(self.origem, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)

    def _ler_csv(self):
        registros = []
        with open(self.origem, 'r', encoding='utf-8') as arquivo:
            leitor = csv.DictReader(arquivo, delimiter=',')
            for linha in leitor:
                registros.append(linha)
        return registros

    def _carregar_registros(self):
        if self.formato == 'csv':
            return self._ler_csv()
        elif self.formato == 'json':
            return self._ler_json()
        elif self.formato == 'lista':
            dados = self.origem
            self.origem = 'lista_em_memoria'
            return dados
        return []

    # ------------------------------------------------------------------ #
    #  Metadados                                                           #
    # ------------------------------------------------------------------ #

    def _extrair_colunas(self):
        return list(self.registros[-1].keys())

    def _contar_linhas(self):
        return len(self.registros)

    # ------------------------------------------------------------------ #
    #  Transformação                                                       #
    # ------------------------------------------------------------------ #

    def renomear_colunas(self, mapeamento):
        """Renomeia as colunas de acordo com um dicionário de mapeamento."""
        novos_registros = []
        for registro_antigo in self.registros:
            registro_novo = {
                mapeamento[chave]: valor
                for chave, valor in registro_antigo.items()
            }
            novos_registros.append(registro_novo)

        self.registros = novos_registros
        self.colunas = self._extrair_colunas()

    def _converter_para_tabela(self):
        """Converte a lista de dicionários em uma tabela (lista de listas)."""
        tabela = [self.colunas]
        for registro in self.registros:
            linha = [
                registro.get(coluna, 'Indisponível')
                for coluna in self.colunas
            ]
            tabela.append(linha)
        return tabela

    # ------------------------------------------------------------------ #
    #  Operações entre instâncias                                          #
    # ------------------------------------------------------------------ #

    @staticmethod
    def unir(fonte_a, fonte_b):
        """Combina os registros de duas instâncias de Dados em uma nova."""
        registros_unidos = []
        registros_unidos.extend(fonte_a.registros)
        registros_unidos.extend(fonte_b.registros)
        return Dados(registros_unidos, 'lista')

    # ------------------------------------------------------------------ #
    #  Persistência                                                        #
    # ------------------------------------------------------------------ #

    def exportar_csv(self, caminho_destino):
        """Salva os dados em um arquivo CSV no caminho informado."""
        tabela = self._converter_para_tabela()
        with open(caminho_destino, 'w', encoding='utf-8', newline='') as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerows(tabela)
