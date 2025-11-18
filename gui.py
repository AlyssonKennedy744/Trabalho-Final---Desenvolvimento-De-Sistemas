import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from db import Database

class MovieApp:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.title("CineManager - Sistema de Filmes")
        self.root.geometry("950x650")
        
        # --- Cabeçalho ---
        header_frame = ttk.Frame(root, padding=20)
        header_frame.pack(fill=X)
        
        lbl_title = ttk.Label(
            header_frame, 
            text="Gerenciamento de Filmes", 
            font=("Helvetica", 24, "bold"),
            bootstyle="primary"
        )
        lbl_title.pack(side=LEFT)

        lbl_subtitle = ttk.Label(
            header_frame, 
            text="Controle seu catálogo pessoal", 
            font=("Helvetica", 12),
            bootstyle="secondary"
        )
        lbl_subtitle.pack(side=LEFT, padx=15, pady=(10, 0))

        # --- Área de Cadastro (Card) ---
        input_frame = ttk.Labelframe(root, text=" Novo Registro ", padding=20, bootstyle="info")
        input_frame.pack(fill=X, padx=20, pady=10)

        # Grid Configuration
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(3, weight=1)

        # Linha 1
        ttk.Label(input_frame, text="Título do Filme:").grid(row=0, column=0, sticky=W, pady=5)
        self.entry_titulo = ttk.Entry(input_frame)
        self.entry_titulo.grid(row=0, column=1, sticky=EW, padx=(5, 20), pady=5)

        ttk.Label(input_frame, text="Diretor:").grid(row=0, column=2, sticky=W, pady=5)
        self.entry_diretor = ttk.Entry(input_frame)
        self.entry_diretor.grid(row=0, column=3, sticky=EW, padx=5, pady=5)

        # Linha 2
        ttk.Label(input_frame, text="Ano de Lançamento:").grid(row=1, column=0, sticky=W, pady=5)
        self.entry_ano = ttk.Entry(input_frame)
        self.entry_ano.grid(row=1, column=1, sticky=EW, padx=(5, 20), pady=5)

        ttk.Label(input_frame, text="Categoria:").grid(row=1, column=2, sticky=W, pady=5)
        
        # Carregar categorias
        cats = self.db.get_categorias()
        self.cat_dict = {c[1]: c[0] for c in cats}
        self.combo_cat = ttk.Combobox(input_frame, values=list(self.cat_dict.keys()), state="readonly")
        self.combo_cat.grid(row=1, column=3, sticky=EW, padx=5, pady=5)

        # --- Área de Botões ---
        btn_frame = ttk.Frame(root, padding=10)
        btn_frame.pack(fill=X, padx=20)

        self.btn_add = ttk.Button(btn_frame, text="Adicionar Filme", command=self.add_filme, bootstyle=SUCCESS, width=20)
        self.btn_add.pack(side=LEFT, padx=(0, 10))

        self.btn_update = ttk.Button(btn_frame, text="Atualizar Selecionado", command=self.update_filme, bootstyle=WARNING, width=20)
        self.btn_update.pack(side=LEFT, padx=10)

        self.btn_delete = ttk.Button(btn_frame, text="Excluir Filme", command=self.delete_filme, bootstyle=DANGER, width=20)
        self.btn_delete.pack(side=RIGHT)

        # --- Listagem (Tabela) ---
        tree_frame = ttk.Frame(root, padding=20)
        tree_frame.pack(fill=BOTH, expand=True)

        scroll = ttk.Scrollbar(tree_frame)
        scroll.pack(side=RIGHT, fill=Y)

        columns = ("ID", "Título", "Diretor", "Ano", "Categoria")
        self.tree = ttk.Treeview(
            tree_frame, 
            columns=columns, 
            show='headings', 
            yscrollcommand=scroll.set,
            bootstyle="primary"
        )
        
        scroll.config(command=self.tree.yview)
        
        # Configuração das colunas (CORRIGIDO: removido weight, usado width)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Título", text="Título do Filme")
        self.tree.heading("Diretor", text="Diretor")
        self.tree.heading("Ano", text="Ano")
        self.tree.heading("Categoria", text="Gênero")
        
        self.tree.column("ID", width=50, anchor=CENTER)
        self.tree.column("Título", width=300)  # Aumentei a largura
        self.tree.column("Diretor", width=200) # Aumentei a largura
        self.tree.column("Ano", width=80, anchor=CENTER)
        self.tree.column("Categoria", width=120, anchor=CENTER)

        self.tree.pack(fill=BOTH, expand=True)
        
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.load_data()

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in self.db.get_filmes():
            self.tree.insert("", "end", values=row)

    def add_filme(self):
        try:
            cat_name = self.combo_cat.get()
            if not cat_name: raise ValueError("Selecione uma categoria")
            cat_id = self.cat_dict[cat_name]
            
            self.db.add_filme(
                self.entry_titulo.get(),
                self.entry_diretor.get(),
                int(self.entry_ano.get()),
                cat_id
            )
            self.flash_message("Filme adicionado com sucesso!", "success")
            self.load_data()
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir: {e}")

    def delete_filme(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um item na lista abaixo")
            return
        
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este filme?"):
            item = self.tree.item(selected[0])
            id_filme = item['values'][0]
            self.db.delete_filme(id_filme)
            self.flash_message("Filme removido!", "danger")
            self.load_data()
            self.clear_entries()

    def update_filme(self):
        selected = self.tree.selection()
        if not selected: return
        
        try:
            id_filme = self.tree.item(selected[0])['values'][0]
            cat_id = self.cat_dict[self.combo_cat.get()]
            
            self.db.update_filme(
                id_filme,
                self.entry_titulo.get(),
                self.entry_diretor.get(),
                int(self.entry_ano.get()),
                cat_id
            )
            self.flash_message("Registro atualizado!", "info")
            self.load_data()
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected: return
        values = self.tree.item(selected[0])['values']
        
        self.entry_titulo.delete(0, tk.END)
        self.entry_titulo.insert(0, values[1])
        self.entry_diretor.delete(0, tk.END)
        self.entry_diretor.insert(0, values[2])
        self.entry_ano.delete(0, tk.END)
        self.entry_ano.insert(0, values[3])
        self.combo_cat.set(values[4])

    def clear_entries(self):
        self.entry_titulo.delete(0, tk.END)
        self.entry_diretor.delete(0, tk.END)
        self.entry_ano.delete(0, tk.END)
        self.combo_cat.set('')

    def flash_message(self, msg, type):
        # Como não temos uma barra de status, imprimimos no console para debug
        print(f"LOG [{type}]: {msg}")