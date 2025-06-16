import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import cv2
import random
from src.util.base64 import image_to_base64
from src.service.conexao.conn import saveFirestore
from src.app.screens.scanner.main import JanelaWebCam
from src.util.detect_face_ssd import detect_face_ssd
from src.classifier.scripts.network_loader import get_network
from src.classifier.scripts.model_loader import get_model
from src.classifier.scripts.image_saver import save_image


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
        # Botão para abrir scan de fotos
        btn_webcam = ctk.CTkButton(
            self.main_frame,
            text="Escanear Webcam",
            font=("Helvetica", 14, "bold"),
            command=self.escanear_webcam
        )
        btn_webcam.grid(row=3, column=0, columnspan=2, padx=80, pady=5, sticky="ew")
        
        # Botão de salvar
        btn_salvar = ctk.CTkButton(
            self.main_frame,
            text="CADASTRAR",
            font=("Helvetica", 14, "bold"),
            command=self.salvar_cadastro
        )
        btn_salvar.grid(row=5, column=0, columnspan=2, padx=100, pady=5, sticky="ew")

    def criar_lista_fotos(self):
        # Lista de fotos
        self.lista_fotos = ctk.CTkTextbox(
            self.main_frame, 
            width=400, 
            height=150, 
            state="disabled"
        )
        self.lista_fotos.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

    # Webcam:
    def salvar_imagem_webcam(self, frame, face_roi, aluno): 
        if face_roi is None:
            return
        
        rnd_nome = "foto_" + str(random.randint(10**13, 10**14 - 1)) + ".jpg"

        self.fotos_selecionadas.append((face_roi.copy(), rnd_nome))
        self.atualizar_lista_fotos()
    
    def escanear_webcam(self): 
        JanelaWebCam(self.salvar_imagem_webcam, show_conf=False)


    def atualizar_lista_fotos(self):
        self.lista_fotos.configure(state="normal")
        self.lista_fotos.delete("1.0", "end")

        for _, nome in self.fotos_selecionadas:
            self.lista_fotos.insert("end", nome + "\n")

        self.lista_fotos.configure(state="disabled")

    def validar_campos(self):
        nome = self.nome_entry.get().strip()
        ra = self.ra_entry.get().strip()
        
        if not nome:
            messagebox.showerror("Erro", "Por favor, insira o nome", parent=self)
            return False
        
        if not ra.isdigit():
            messagebox.showerror("Erro", "RA deve conter apenas números", parent=self)
            return False
        
        if len(ra) != 14:
            messagebox.showerror("Erro", "RA deve conter exatamente 14 dígitos", parent=self)
            return False
        
        if not self.fotos_selecionadas:
            messagebox.showerror("Erro", "Por favor, selecione pelo menos uma foto", parent=self)
            return False
            
        return True

    def salvar_cadastro(self):
        if not self.validar_campos():
            return
        
        try:
            fotos = [image_to_base64(foto) for foto,_ in self.fotos_selecionadas]
            nome = self.nome_entry.get().strip()
            ra = self.ra_entry.get().strip()

            saveFirestore(nome, ra, fotos)

            # Atualiza modelo de treinamento
            sample = 1
            for foto, _ in self.fotos_selecionadas:
                save_image(nome, ra, foto, sample)
                sample += 1

            get_model(parse=True)
            
            self.callback_sucesso()
            self.limpar_campos()


            messagebox.showinfo("Sucesso", "Cadastro salvo com sucesso!", parent=self)
            self.focus_force()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar: {str(e)}", parent=self)
            self.focus_force()

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