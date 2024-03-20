import tkinter as tk
import sqlite3
from tkinter import messagebox, simpledialog

class StockManagementApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestão de Estoque")
        self.master.geometry("600x400")

        self.conn = sqlite3.connect('stock.db')
        self.create_table()

        self.create_widgets()
        self.generate_html()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            quantity INTEGER,
                            description TEXT)''')
        self.conn.commit()

    def create_widgets(self):
        self.label_product_name = tk.Label(self.master, text="Nome do Produto:", font=("Arial", 14))
        self.label_product_name.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        self.entry_product_name = tk.Entry(self.master, font=("Arial", 12))
        self.entry_product_name.grid(row=0, column=1, padx=10, pady=10)

        self.label_quantity = tk.Label(self.master, text="Quantidade:", font=("Arial", 14))
        self.label_quantity.grid(row=1, column=0, sticky="w", padx=10, pady=10)

        self.entry_quantity = tk.Entry(self.master, font=("Arial", 12))
        self.entry_quantity.grid(row=1, column=1, padx=10, pady=10)

        self.label_description = tk.Label(self.master, text="Descrição:", font=("Arial", 14))
        self.label_description.grid(row=2, column=0, sticky="w", padx=10, pady=10)

        self.entry_description = tk.Text(self.master, font=("Arial", 12), height=5, width=30)
        self.entry_description.grid(row=2, column=1, padx=10, pady=10)

        self.add_button = tk.Button(self.master, text="Adicionar Produto", font=("Arial", 12), command=self.add_product)
        self.add_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        self.edit_button = tk.Button(self.master, text="Editar Produto", font=("Arial", 12), command=self.edit_product)
        self.edit_button.grid(row=3, column=1, padx=10, pady=10, sticky="e")

        self.stock_frame = tk.Frame(self.master, bd=2, relief=tk.GROOVE)
        self.stock_frame.grid(row=0, column=2, rowspan=4, padx=10, pady=10, sticky="nsew")

        self.stock_listbox = tk.Listbox(self.stock_frame, font=("Arial", 12), height=15, width=40)
        self.stock_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.stock_listbox.bind("<Double-Button-1>", self.edit_product)

    def generate_html(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, quantity, description FROM products")
        rows = cursor.fetchall()

        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Gestão de Estoque</title>
        </head>
        <body>
            <h1>Gestão de Estoque</h1>
            <table border="1">
                <tr>
                    <th>Nome do Produto</th>
                    <th>Quantidade</th>
                    <th>Descrição</th>
                </tr>
        """

        for row in rows:
            html_content += f"""
                <tr>
                    <td>{row[0]}</td>
                    <td>{row[1]}</td>
                    <td>{row[2]}</td>
                </tr>
            """

        html_content += """
            </table>
        </body>
        </html>
        """

        with open("stock_management.html", "w") as file:
            file.write(html_content)

            print("Arquivo HTML gerado com sucesso: stock_management.html")

    def add_product(self):
        product_name = self.entry_product_name.get()
        quantity = self.entry_quantity.get()
        description = self.entry_description.get("1.0", tk.END).strip()

        if product_name and quantity:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO products (name, quantity, description) VALUES (?, ?, ?)",
                           (product_name, int(quantity), description))
            self.conn.commit()
            self.stock_listbox.insert(tk.END, f"{product_name}: {quantity} - {description}")
            self.entry_product_name.delete(0, tk.END)
            self.entry_quantity.delete(0, tk.END)
            self.entry_description.delete("1.0", tk.END)
        else:
            messagebox.showwarning("Aviso", "Por favor, preencha o nome do produto e a quantidade.")

    def edit_product(self, event=None):
        selected_index = self.stock_listbox.curselection()

        if selected_index:
            product_name = self.stock_listbox.get(selected_index).split(":")[0]
            cursor = self.conn.cursor()
            cursor.execute("SELECT quantity, description FROM products WHERE name=?", (product_name,))
            row = cursor.fetchone()
            old_quantity = row[0]
            old_description = row[1]

            new_quantity = simpledialog.askinteger("Editar Produto", f"Nova quantidade para {product_name}:",
                                                   initialvalue=old_quantity)
            if new_quantity is not None:
                new_description = simpledialog.askstring("Editar Produto", f"Nova descrição para {product_name}:",
                                                         initialvalue=old_description)
                cursor.execute("UPDATE products SET quantity=?, description=? WHERE name=?",
                               (new_quantity, new_description, product_name))
                self.conn.commit()
                self.stock_listbox.delete(selected_index)
                self.stock_listbox.insert(selected_index, f"{product_name}: {new_quantity} - {new_description}")
        else:
            messagebox.showwarning("Aviso", "Selecione um produto para editar.")

def main():
    root = tk.Tk()
    app = StockManagementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
