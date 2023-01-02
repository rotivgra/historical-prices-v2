import mysql.connector

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler

db_connection = mysql.connector.connect(host='localhost', user='root', password='root', database='flutuacoes')
cursor = db_connection.cursor() # Guia para utilizar funções do BD
cursor.execute("select eu.id_produtos, p.codigo, eu.data, eu.preco from produtos as p, precoeuro as eu where p.id = eu.id_produtos order by p.codigo, eu.data ASC;")
myresult = cursor.fetchall() # Necessário para formatar a saída do BD
cursor.execute("select * from produtos order by codigo DESC;")
produtos = cursor.fetchall()


class App(tk.Tk):
    # Torax do meu app
    def __init__(self):
        super().__init__()
        # Criando tabelas
        self.trv_pro = ttk.Treeview(self, selectmode ='browse')
        self.trv_pro.bind("<ButtonRelease>", self.seleciona_por_clique)
        self.trv_pro.bind("<KeyRelease>", self.seleciona_por_clique)

        self.title('MeuApp')
        
        self.trv_pro.place(x=10, y=70)
        self.trv_pro["columns"] = ("1")
        self.trv_pro['show'] = 'headings'
        self.trv_pro.column("1", width = 190, anchor ='c')
        self.trv_pro.heading("1", text ="Codigo")
        ndl = 0
        for p in produtos:
            self.trv_pro.insert('','end', text=str(ndl), values=(p[1]))
            ndl += 1      

    def seleciona_por_clique(self, event):
        self.curItem = self.trv_pro.focus()
        self.a = self.trv_pro.item(self.curItem).items()
        self.b = list(self.a)[2][1]
        for clique in self.b:
            cursor.execute(f"SELECT id FROM produtos WHERE codigo='{self.b[0]}';")
            consulta = cursor.fetchall()
            pros = consulta[0][0]
            cursor.execute(f"select eu.id_produtos, p.codigo, eu.data, eu.preco from produtos as p, precoeuro as eu where p.id = eu.id_produtos AND eu.id_produtos='{pros}' order by p.codigo, eu.data ASC;")
            form = cursor.fetchall()            
       
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

        # Tabela3
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

        #def pesquisar():
            

if __name__ == "__main__":
  app = App()
  app.mainloop()
