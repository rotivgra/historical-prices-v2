# historical-prices-v2
frame_product:
		Apresenta os produtos cadastrado no BD através de uma Widget

consult_product:
		Utiliza a sintax de filtragem SQL para pesquisar produtos com códigos relacionado ao digitado em self.entry_product

id_per_click:
		Atraves de um conjunto de ferramentas do Tkinter + SQL pega o ID do produto no BD e utiliza este mesmo ID para apresentar o histórico de preços,
		a média do histórico e também é utilizado para apresentar um grafico com variação de preços ao longo do tempo

ERROS / EXCEÇÕES:
		Caso as consultas pelo ID não encontre o histórico de preço do produto, é jogada uma printado no console uma exceção
