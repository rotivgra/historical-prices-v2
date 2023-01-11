import mysql.connector
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

class App(tk.Tk):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.frame_product()

    def frame_product(self):
        # FRAME consult
        self.frame_consult = tk.LabelFrame(self, text="CONSULT PRODUCTS: ")
        self.frame_consult.place(x=10, y=5, height=50, width=1000)

        # ENTRY consult
        self.entry_product = tk.Entry(self.frame_consult, width=32)
        self.entry_product.grid(row=0,column=0, padx=10)
        
        # SELECT products
        select_product = "SELECT * FROM produtos ORDER BY codigo DESC;"
        all_products = self.db.cursor()
        all_products.execute(select_product)
        table_product = all_products.fetchall()
        all_products.close()

        # TABLE products 
        self.trv_pro = ttk.Treeview(self, selectmode ="browse")
        self.trv_pro.bind("<ButtonRelease>", self.id_per_click)
        self.trv_pro.bind("<KeyRelease>", self.id_per_click)
        self.trv_pro.place(x=10, y=70)
        self.trv_pro["columns"] = ("1",)
        self.trv_pro["show"] = "headings"
        self.trv_pro.column("1", width = 190, anchor ="c")
        self.trv_pro.heading("1", text ="CODIGO")
        for id_counter, list_product in enumerate(table_product):
            self.trv_pro.insert("","end", text=str(id_counter), values=(list_product[1]))

        def consult_product():            
            # SELECT consult DB
            store_product = self.entry_product.get()                 
            select_consult = f"SELECT * FROM produtos WHERE codigo LIKE '%{store_product}%';"
            all_consult = self.db.cursor()
            all_consult.execute(select_consult)
            result_consult = all_consult.fetchall()
            all_consult.close()

            # TABLE consult
            self.trv_pro = ttk.Treeview(self, selectmode ='browse')
            self.trv_pro.bind("<ButtonRelease>", self.id_per_click)
            self.trv_pro.bind("<KeyRelease>", self.id_per_click)
            self.trv_pro.place(x=10, y=70)
            self.trv_pro["columns"] = ("1")
            self.trv_pro['show'] = 'headings'
            self.trv_pro.column("1", width = 190, anchor ='c')
            self.trv_pro.heading("1", text ="Codigo")
            for id_counter_v3, data_consult in enumerate (result_consult):
                self.trv_pro.insert('','end', text=str(id_counter_v3), values=(data_consult[1]))
                self.entry_product.delete(0, 'end')

        # BUTTON consult
        self.button_consult = tk.Button(self.frame_consult, text="CONSULT", command=consult_product)
        self.button_consult.grid(row=0,column=1, padx=10)
            
   
    def id_per_click(self, event):
        # GET code at Widget
        self.curItem = self.trv_pro.focus()
        self.get_code_item = self.trv_pro.item(self.curItem)['values'][0]

        # SELECT id at BD
        select_id = "SELECT id FROM produtos WHERE codigo = %(codigo)s"        
        all_id = self.db.cursor()
        all_id.execute(select_id, { "codigo": self.get_code_item})
        consult = all_id.fetchall()
        ref_id = consult[0][0]
        all_id.close()

        # SELECT historical prices        
        select_his = f"SELECT eu.id_produtos, p.codigo, eu.data, eu.preco FROM produtos AS p, precoeuro AS eu WHERE p.id = eu.id_produtos AND eu.id_produtos=%(eu.id_produtos)s ORDER BY p.codigo, eu.data ASC;"
        historic_by_id = self.db.cursor()
        historic_by_id.execute(select_his, { "eu.id_produtos": ref_id })
        result_historic = historic_by_id.fetchall()
        historic_by_id.close()

            
        # TABLE historical prices
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

        # SELECT average        
        select_average = f"SELECT eu.id_produtos, ROUND(SUM(eu.preco)/COUNT(*), 1) AS media FROM precoeuro AS eu WHERE eu.id_produtos=%(eu.id_produtos)s;"
        all_average = self.db.cursor()
        all_average.execute(select_average, { "eu.id_produtos": ref_id })
        bd_med = all_average.fetchall()
        all_average.close()
        
        # TABLE average
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

        # SELECT date
        select_horizontal = f"SELECT eu.data FROM precoeuro AS eu WHERE eu.id_produtos=%(eu.id_produtos)s ORDER BY eu.data ASC;"
        all_date = self.db.cursor()
        all_date.execute(select_horizontal, {"eu.id_produtos": ref_id})
        result_date = all_date.fetchall()
        all_date.close()

        # SELECT prices
        select_vertical = f"SELECT eu.preco FROM precoeuro AS eu WHERE eu.id_produtos=%(eu.id_produtos)s ORDER BY eu.data ASC;"
        all_prices = self.db.cursor()
        all_prices.execute(select_vertical, {"eu.id_produtos": ref_id})
        result_prices = all_prices.fetchall()
        all_prices.close()

        # GRAPHIC historical prices
        fig = plt.figure(figsize=(19, 7), dpi = 50)
        plt.plot(result_date, result_prices, 'k--')
        plt.plot(result_date, result_prices, 'go')
        canvas = FigureCanvasTkAgg(fig, master = self)   
        canvas.draw() 
        canvas.get_tk_widget().place(x=35, y=300)  

if __name__ == "__main__":
    db_connection = mysql.connector.connect(host="localhost", user="root", password="root", database="flutuacoes")
    app = App(db_connection)
    app.mainloop()
