from processamento_dados import Dados

# ------------------------------------------------------------------ #
#  Caminhos das fontes de dados                                        #
# ------------------------------------------------------------------ #

caminho_json = 'data_raw/dados_empresaA.json'
caminho_csv  = 'data_raw/dados_empresaB.csv'

# ------------------------------------------------------------------ #
#  EXTRACT — leitura das fontes brutas                                 #
# ------------------------------------------------------------------ #

fonte_empresa_a = Dados(caminho_json, 'json')
print("Empresa A — colunas:", fonte_empresa_a.colunas)
print("Empresa A — total de registros:", fonte_empresa_a.total_linhas)

fonte_empresa_b = Dados(caminho_csv, 'csv')
print("Empresa B — colunas:", fonte_empresa_b.colunas)
print("Empresa B — total de registros:", fonte_empresa_b.total_linhas)

# ------------------------------------------------------------------ #
#  TRANSFORM — padronização e combinação                               #
# ------------------------------------------------------------------ #

mapeamento_colunas = {
    'Nome do Item'             : 'Nome do Produto',
    'Classificação do Produto' : 'Categoria do Produto',
    'Valor em Reais (R$)'      : 'Preço do Produto (R$)',
    'Quantidade em Estoque'    : 'Quantidade em Estoque',
    'Nome da Loja'             : 'Filial',
    'Data da Venda'            : 'Data da Venda',
}

fonte_empresa_b.renomear_colunas(mapeamento_colunas)
print("Empresa B após padronização — colunas:", fonte_empresa_b.colunas)

catalogo_unificado = Dados.unir(fonte_empresa_a, fonte_empresa_b)
print("Dataset unificado — colunas:", catalogo_unificado.colunas)
print("Dataset unificado — total de registros:", catalogo_unificado.total_linhas)

# ------------------------------------------------------------------ #
#  LOAD — exportação do dataset consolidado                            #
# ------------------------------------------------------------------ #

caminho_saida = 'data_processed/dados_combinados.csv'
catalogo_unificado.exportar_csv(caminho_saida)
print(f"Arquivo exportado com sucesso: {caminho_saida}")
