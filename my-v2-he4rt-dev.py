import mysql.connector
import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.frame_product()

    """
    frame_product: Utiliza o mysql.connector para se conectar ao BD FLUTUACOES e retornar consultas de todos os dados cadastrados!
                   cursor.execute recebe uma string com uma sintax SQL tornado possivel que seja feitas diversas consultas diferentes no BD,
                   sendo necessário apenas alterar a sintax  dentro da Tupla para retornar o resultado desejado!
                   A variavel que recebe cursor.fetchall() salva o resultado de cursor.execute,
                   essa variavel que recebeu cursor.fetchall() possui uma lista contendo tuplas com o ID e o Código de tudo cadastrado na Tabela PRODUTOS!

                   Para apresentar esses dados utilizo a Widget ttk.Treeview, apenas configurando o cabeçalho e a quantidade de colunas!
                   Feito as configurações necessárias eu faço um laço for, para inserir os dados salvos na variavel que recebeu cursor.fetchall(),
                   na Widget ttk.Treeview através do comando self.trv_pro.insert.
                   
    """
    
    def frame_product(self):
        select_product = "SELECT * FROM produtos ORDER BY codigo DESC;"
        all_products = cursor
        all_products.execute(select_product)
        table_product = all_products.fetchall()

        # Table 1
        self.trv_pro = ttk.Treeview(self, selectmode ="browse")
        self.trv_pro.bind("<ButtonRelease>", self.id_per_click)
        self.trv_pro.bind("<KeyRelease>", self.id_per_click)
        self.trv_pro.place(x=10, y=70)
        self.trv_pro["columns"] = ("1",)
        self.trv_pro["show"] = "headings"
        self.trv_pro.column("1", width = 190, anchor ="c")
        self.trv_pro.heading("1", text ="Codigo")
        for id_counter, list_product in enumerate(table_product):
            self.trv_pro.insert("","end", text=str(id_counter), values=(list_product[1]))
    """
    id_per_click: Recebe um evento da função frame_product que é utilizado para capturar o ID de cada interação do usuario,
                  na Widget self.trv_pro através do metodo self.trv_pro.bind
                  O ID do produto capturada através de uma consulta no BD que utiliza o evento de interação do usuario por mouse ou teclado,
                  é salvo na variavel ref_id!

                  Atraves da variavel ref_id é possivel fazer diversas consultas no BD usando-a como parametro, como exemplo verifique a variavel select_his,
                  Para cada troca de linha feita no Widget self.trv_pro, o algoritimo faz a consulta, verifique a variavel select_his,
                  esta consulta é salva em result_historic e apresentada em self.trv_his!

                  É necessário apresentar ao usuario a média dos valores armazenado na Coluna PRECOEURO do BD FLUTUACOES, para isso verifique a variavel select_med,
                  o resultado desta consulta é apresentada em self.trv_med.

    ERROS/ EXEÇÕES: id_per_click: Essa função possui um laço de repetição que consulta no BD o histórico de preços referente a um ID selecionado pelo úsuario,
                                  porém nem todos os produtos cadastrados possuem histórico de preço nesse caso o sistema apresenta um erro pois não encontra,
                                  histórico para o Produto que o usuario selecionou!

                                  Para tratar esse erro é criada a uma exceção tk.TclError:
                                  Ela printa no console uma mensagem para que o usuario esteja ciente que determinado ID não possui histórico no BD
                  
    """
    def id_per_click(self, event):
        self.curItem = self.trv_pro.focus()
        self.dict_items = self.trv_pro.item(self.curItem).items()
        self.get_code_item = list(self.dict_items)[2][1]
        for code in self.get_code_item:            
            select_id = "SELECT id FROM produtos WHERE codigo = %(codigo)s"
            all_id = cursor
            all_id.execute(select_id, { "codigo": self.get_code_item[0] })
            consult = all_id.fetchall()
            ref_id = consult[0][0]

            select_his = f"SELECT eu.id_produtos, p.codigo, eu.data, eu.preco FROM produtos AS p, precoeuro AS eu WHERE p.id = eu.id_produtos AND eu.id_produtos=%(eu.id_produtos)s ORDER BY p.codigo, eu.data ASC;"
            historic_by_id = cursor
            historic_by_id.execute(select_his, { "eu.id_produtos": ref_id })
            result_historic = historic_by_id.fetchall()
            print(result_historic)
            
        # Table 2
        self.trv_his = ttk.Treeview(self, selectmode ="browse")
        self.trv_his.place(x=250, y=70)
        self.trv_his["columns"] = ("1", "2", "3")
        self.trv_his["show"] = "headings"
        self.trv_his.column("1", width = 200, anchor ="c")
        self.trv_his.column("2", width = 200, anchor ="c")
        self.trv_his.column("3", width = 200, anchor ="c")
        self.trv_his.heading("1", text ="PRODUTO")
        self.trv_his.heading("2", text ="DATA")
        self.trv_his.heading("3", text ="CUSTO")
        for id_counter_v1, line_bd in enumerate(result_historic):
            try:
                self.trv_his.insert("", "end", text=str(id_counter_v1), values=(line_bd[1], line_bd[2], line_bd[3]))
            except tk.TclError:
                print("Não possui histórico")

        # Table 3        
        select_average = f"SELECT eu.id_produtos, ROUND(SUM(eu.preco)/COUNT(*), 1) AS media FROM precoeuro AS eu WHERE eu.id_produtos=%(eu.id_produtos)s;"
        all_average = cursor
        all_average.execute(select_average, { "eu.id_produtos": ref_id })
        bd_med = all_average.fetchall()
        
        self.trv_med = ttk.Treeview(self, selectmode ="browse")
        self.trv_med.place(x=926, y= 70)
        self.trv_med["columns"] = ("1",)
        self.trv_med["show"] = "headings"
        self.trv_med.column("1", width = 80, anchor ="c")
        self.trv_med.heading("1", text ="MEDIA")
        for id_counter_v2, media in enumerate (bd_med):
            try:
                self.trv_med.insert("", "end", text=str(id_counter_v2), values=(media[1]))
            except tk.TclError:
                print("Não possui histórico")

if __name__ == "__main__":
    db_connection = mysql.connector.connect(host="localhost", user="root", password="root", database="flutuacoes")
    cursor = db_connection.cursor()
    app = App()
    app.mainloop()
