import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from util.base64 import image_to_base64
from service.conexao import saveFirestore

class TelaCadastro(ctk.CTkToplevel):
    def __init__(self, parent, callback_sucesso):
        super().__init__(parent)
        self.parent = parent
        self.callback_sucesso = callback_sucesso
        self.fotos_selecionadas = []
        
        # Configurar tema
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        self.title("Cadastro de aluno")
        self.geometry("350x450")
        self.resizable(False, False)
        
        # Configurar grid principal
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Frame principal responsivo
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Configurar grid do frame principal
        self.main_frame.grid_rowconfigure(4, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Elementos da interface
        self.criar_campos()
        self.criar_botoes()
        self.criar_lista_fotos()
        
        # Centralizar inicialmente
        self.centralizar_janela()
    
    def centralizar_janela(self):
        self.update_idletasks()
        largura_janela = self.winfo_width()
        altura_janela = self.winfo_height()
        
        # Calcular posição
        x = (self.winfo_screenwidth() - largura_janela) // 2
        y = (self.winfo_screenheight() - altura_janela) // 2
        
        # Aplicar geometria
        self.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

    def criar_campos(self):
        # Frame para campos de entrada
        campos_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        campos_frame.grid(row=0, column=0, pady=10, sticky="ew")
        
        # Configurar grid dos campos
        campos_frame.grid_columnconfigure(0, weight=0)
        campos_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            master=campos_frame,
            text="Cadastrar aluno",
            font=("Helvetica", 14, "bold"),
            justify="center"
        ).grid(
            row=0, column=1,
            pady=5,
            sticky="ew"
        )
        
        self.nome_entry = ctk.CTkEntry(campos_frame, width=200, placeholder_text="Nome")
        self.nome_entry.grid(row=1, column=1, pady=5, padx=15, sticky="ew")
        
        self.ra_entry = ctk.CTkEntry(campos_frame, width=200, placeholder_text="RA (Registro Acadêmico)")
        self.ra_entry.grid(row=2, column=1, pady=5, padx=15, sticky="ew")

    def criar_botoes(self):
        # Botão para selecionar fotos
        btn_fotos = ctk.CTkButton(
            self.main_frame, 
            text="ANEXAR FOTOS", 
            font=("Helvetica", 14, "bold"),
            command=self.selecionar_fotos
        )
        btn_fotos.grid(row=2, column=0, columnspan=2, padx=80, pady=5, sticky="ew")
        
        # Botão de salvar
        btn_salvar = ctk.CTkButton(
            self.main_frame,
            text="CADASTRAR",
            font=("Helvetica", 14, "bold"),
            command=self.salvar_cadastro
        )
        btn_salvar.grid(row=4, column=0, columnspan=2, padx=100, pady=5, sticky="ew")

    def criar_lista_fotos(self):
        # Lista de fotos
        self.lista_fotos = ctk.CTkTextbox(
            self.main_frame, 
            width=400, 
            height=150, 
            state="disabled"
        )
        self.lista_fotos.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

    def selecionar_fotos(self):
        arquivos = filedialog.askopenfilenames(
            title="Selecione as fotos",
            filetypes=(("Arquivos de imagem", "*.jpg *.jpeg *.png *.bmp"), ("Todos os arquivos", "*.*"))
        )
        
        if arquivos:
            self.fotos_selecionadas.extend(arquivos)
            self.atualizar_lista_fotos()

    def atualizar_lista_fotos(self):
        self.lista_fotos.configure(state="normal")
        self.lista_fotos.delete("1.0", "end")
        for foto in self.fotos_selecionadas:
            self.lista_fotos.insert("end", os.path.basename(foto) + "\n")
        self.lista_fotos.configure(state="disabled")

    def validar_campos(self):
        nome = self.nome_entry.get().strip()
        ra = self.ra_entry.get().strip()
        
        if not nome:
            messagebox.showerror("Erro", "Por favor, insira o nome")
            return False
        
        if not ra.isdigit():
            messagebox.showerror("Erro", "RA deve conter apenas números")
            return False
        
        if len(ra) != 14:
            messagebox.showerror("Erro", "RA deve conter exatamente 14 dígitos")
            return False
        
        if not self.fotos_selecionadas:
            messagebox.showerror("Erro", "Por favor, selecione pelo menos uma foto")
            return False
            
        return True

    def salvar_cadastro(self):
        if not self.validar_campos():
            return
        
        try:
            fotos = [image_to_base64(foto) for foto in self.fotos_selecionadas]
            nome = self.nome_entry.get().strip()
            ra = self.ra_entry.get().strip()

            saveFirestore(nome, ra, fotos)
            self.callback_sucesso(nome, ra)
            self.destroy()
            messagebox.showinfo("Sucesso", "Cadastro salvo com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar: {str(e)}")

    def limpar_campos(self):
        self.nome_entry.delete(0, "end")
        self.ra_entry.delete(0, "end")
        self.fotos_selecionadas = []
        self.atualizar_lista_fotos()

def main():
    root = ctk.CTk(fg_color="#e0e0e0")
    app = TelaCadastro(root)
    root.resizable(False, False) 
    root.mainloop()

if __name__ == "__main__":
    main()