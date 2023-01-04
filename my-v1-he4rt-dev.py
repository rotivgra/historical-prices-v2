import mysql.connector
import tkinter as tk
from tkinter import ttk

"""
        Este algoritimo deve permitir que o úsuario consulte o histórico de preços de cotações feitas em euro!

        Para isso eu criei uma Widget:
            self.trv_pro = ttk.Treeview            /para apresentar ao úsuario todos os códigos do BD flutuacoes Tabela PRODUTOS

        Feito o Widget eu uso uma função do mysql.connector que é a cursor.execute para realizar consults no BD,
            e salvo o resultado destas consult em uma variavel utilizando o metodo cursor.fetchall(),
            essa variavel possui o resultado da consult que retorna uma lista contendo tuplas com o ID e o Código de tudo cadastrado na Tabela PRODUTOS

        Para apresentar os dados destas consults eu faço um loop for onde defino uma variavel = 0 para representar o ID da Tabela consultda,
            e para cada item dentro da variavel que salva o resultado da consult eu insiro as informações retornadas,
            utilizando o metodo self.trv_pro.insert

        Para cada Código apresentado em self.trv_pro o usuario deve poder navegar pelos códigos da Widget utilizando o teclado ou o mouse,
            e para cada clique ou navegação por teclado eu tive que fazer uma função que retornasse o ID do produto pois o ID da tabela PRODUTOS
            possui relação com a Tabela PRECOEURO do mesmo BD,

        Para capturar o ID de cada interação feita pelo usuario eu criei a função que recebe um evento do metodo bind:
            def id_per_click(self, event):

        Para capturar a interação do usuario por mouse ou teclado eu utilizei o metodo bind do Treeview:
            self.trv_pro.bind("<ButtonRelease>", self.id_per_click)            / Permite a interação por mouse
            self.trv_pro.bind("<KeyRelease>", self.id_per_click)               / Permite a interação por teclado

        Com isso para cada inteiração por mouse ou teclado na Widget self.trv_pro,
            eu capturo o ID do produto pela função def id_per_click(self, event): e salvo o ID em uma variavel chamada pros,
            e acabo utilizando essa variavel pros para fazer consults atraves do ID na Tabela PRECOEURO, retornando todo histórico de preços no Widget:
                self.trv_his = ttk.Treeview,
            e retorno para cada inteiração do usuario uma média no Widget:
                self.trv_med = ttk.Treeview
                
        
"""

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.frame_product()

    def frame_product(self):
        select_product = ("select * from produtos order by codigo DESC;")
        cursor.execute(select_product)
        table_product = cursor.fetchall()

        # Table 1
        self.trv_pro = ttk.Treeview(self, selectmode ='browse')
        self.trv_pro.bind("<ButtonRelease>", self.id_per_click)
        self.trv_pro.bind("<KeyRelease>", self.id_per_click)
        self.trv_pro.place(x=10, y=70)
        self.trv_pro["columns"] = ("1")
        self.trv_pro['show'] = 'headings'
        self.trv_pro.column("1", width = 190, anchor ='c')
        self.trv_pro.heading("1", text ="Codigo")
        ndl = 0
        for p in table_product:
            self.trv_pro.insert('','end', text=str(ndl), values=(p[1]))
            ndl += 1 

    def id_per_click(self, event):
        self.curItem = self.trv_pro.focus()
        self.a = self.trv_pro.item(self.curItem).items()
        self.b = list(self.a)[2][1]
        for clique in self.b:
            
            select_id = ("SELECT id FROM produtos WHERE codigo = %(codigo)s")
            cursor.execute(select_id, { 'codigo': self.b[0] })
            consult = cursor.fetchall()
            pros = consult[0][0]

            select_his = (f"select eu.id_produtos, p.codigo, eu.data, eu.preco from produtos as p, precoeuro as eu where p.id = eu.id_produtos AND eu.id_produtos=%(eu.id_produtos)s order by p.codigo, eu.data ASC;")
            cursor.execute(select_his, { 'eu.id_produtos': pros })
            form = cursor.fetchall()
            
        # Table 2
        self.trv_his = ttk.Treeview(self, selectmode ='browse')
        self.trv_his.place(x=250, y=70)
        self.trv_his["columns"] = ("1", "2", "3")
        self.trv_his['show'] = 'headings'
        self.trv_his.column("1", width = 200, anchor ='c')
        self.trv_his.column("2", width = 200, anchor ='c')
        self.trv_his.column("3", width = 200, anchor ='c')
        self.trv_his.heading("1", text ="Produto")
        self.trv_his.heading("2", text ="Data")
        self.trv_his.heading("3", text ="Custo")
        cpt = 0
        for l in form:
            try:
                self.trv_his.insert('', 'end', text=str(cpt), values=(l[1], l[2], l[3]))
                cpt += 1
            except tk.TclError:
                print("Não possui histórico")

        # # Table 3
        cursor.execute(f"SELECT eu.id_produtos, ROUND(SUM(eu.preco)/COUNT(*), 1) AS media FROM precoeuro AS eu WHERE eu.id_produtos='{pros}';")
        bd_med = cursor.fetchall()      
        self.trv_med = ttk.Treeview(self, selectmode ='browse')
        self.trv_med.place(x=926, y= 70)
        self.trv_med["columns"] = ("1")
        self.trv_med['show'] = 'headings'
        self.trv_med.column("1", width = 80, anchor ='c')
        self.trv_med.heading("1", text ="Média")
        mpt = 0
        for me in bd_med:
            try:
                self.trv_med.insert('', 'end', text=str(cpt), values=(me[1]))
                mpt += 1
            except tk.TclError:
                print("Não possui histórico")

if __name__ == '__main__':
    db_connection = mysql.connector.connect(host='localhost', user='root', password='root', database='flutuacoes')
    cursor = db_connection.cursor()
    app = App()
    app.mainloop()
