import customtkinter as ctk
from ..cadastro.main import TelaCadastro
from ..scanner.main import JanelaWebCam

# Configuração inicial do tema
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Chamada Escolar")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        self.all_check_vars = []
        self.create_widgets()
        self.centralizar_janela()

    def centralizar_janela(self):
        self.root.update_idletasks()
        largura_janela = self.root.winfo_width()
        altura_janela = self.root.winfo_height()

        x = (self.root.winfo_screenwidth() - largura_janela) // 2
        y = (self.root.winfo_screenheight() - altura_janela) // 2

        self.root.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

    def create_widgets(self):
        # Frame superior para título e botão
        top_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        top_frame.pack(side="top", fill="x", padx=20, pady=10)

        # Configurar colunas para centralização exata
        top_frame.grid_columnconfigure(0, weight=1, uniform="cols_espacadoras")  # Coluna esquerda
        top_frame.grid_columnconfigure(1, weight=0, uniform="cols_espacadoras")  # Coluna central
        top_frame.grid_columnconfigure(2, weight=1, uniform="cols_espacadoras")  # Coluna direita

        # Título
        ctk.CTkLabel(
            top_frame, 
            text="Controle de Frequência",
            font=("Arial", 18, "bold"),
        ).grid(row=0, column=1, padx=0, pady=0)

        # Botão Cadastrar
        ctk.CTkButton(
            top_frame,
            text="Cadastrar",
            width=100,
            font=("Arial", 14, "bold"),
            command=self.abrir_janela_cadastro
        ).grid(row=0, column=2, sticky="e")

        # Botão Cadastrar
        ctk.CTkButton(
            top_frame,
            text="Scanear",
            width=100,
            font=("Arial", 14, "bold"),
            command=JanelaWebCam
        ).grid(row=0, column=0, sticky="w")

        # Frame principal para a tabela
        table_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=0, pady=10)
        
        # Divisória horizontal antes do cabeçalho
        self.create_row_divider(table_frame, 0)

        headers = ["Aluno", "RA", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"]

        # Configuração das colunas da tabela
        for col in range(15):  # 8 colunas de conteúdo + 7 divisórias
            if col % 2 == 0:
                table_frame.columnconfigure(col, 
                    weight=1,
                    minsize=120 if col < 4 else 80
                )
            else:
                table_frame.columnconfigure(col, 
                    weight=0, 
                    minsize=2
                )

        table_frame.rowconfigure(0, weight=0)  # divisória
        table_frame.rowconfigure(1, weight=0, minsize=40)  # cabeçalho
        
        for r in (2,3,4,5,6):
            table_frame.rowconfigure(r, weight=0)
        
        # Cabeçalhos
        for idx, header in enumerate(headers):
            col = idx * 2
            # 1) Cria um frame azul que vai ocupar 100% da célula:
            header_bg = ctk.CTkFrame(
                table_frame,
                #fg_color="#2600ff",
                fg_color="transparent",
                corner_radius=0
            )
            header_bg.grid(row=1, column=col, sticky="nsew", padx=0, pady=0)

            # 2) Coloca o texto dentro, com fundo transparente:
            ctk.CTkLabel(
                header_bg,
                text=header,
                font=("Arial", 14, "bold"),
                fg_color="transparent"
            ).pack(expand=True, fill="both")

            # 3) Continua criando as divisórias verticais:
            if idx > 0:
                self.create_column_divider(table_frame, col-1)

        # Conteúdo principal
        self.create_row_divider(table_frame, 2)
        self.create_student_row(table_frame, 3, "Isaac da Cunha Carvalho", "12345671234567")
        self.create_row_divider(table_frame, 4)

    def create_student_row(self, parent, row, nome="", ra=""):
        # Nome do Aluno
        nome_entry = ctk.CTkEntry(
            parent,
            width=170,
            border_width=0, 
            fg_color="transparent", 
            justify="center",
        )
        nome_entry.insert(0, nome)
        nome_entry.configure(state="readonly")
        nome_entry.grid(row=row, column=0, padx=0, pady=0, sticky="nsew")

        # RA
        ra_entry = ctk.CTkEntry(
            parent,
            width=120,
            border_width=0,
            fg_color="transparent", 
            justify="center"
        )
        ra_entry.insert(0, ra)
        ra_entry.configure(state="readonly")
        ra_entry.grid(row=row, column=2, padx=0, pady=0, sticky="nsew")

        # Checkboxes
        check_vars = []
        for idx, col in enumerate(range(4, 16, 2)):
            var = ctk.BooleanVar()
            
            # Container principal
            main_frame = ctk.CTkFrame(
                parent,
                width=80,
                height=20,
                fg_color="transparent"
            )
            main_frame.grid_propagate(False)
            main_frame.grid(row=row, column=col, padx=0, pady=0, sticky="nsew")

            # Checkbox centralizado
            checkbox = ctk.CTkCheckBox(
                main_frame,
                text="",
                variable=var,
                width=24,
                height=24,
                border_width=2
            )
            checkbox.place(relx=0.5, rely=0.5, anchor="center")

            check_vars.append(var)
            if idx < 4:
                self.create_column_divider(parent, col+1)

        self.all_check_vars.append(check_vars)

    def create_row_divider(self, parent, row):
        """Divisória horizontal entre linhas"""
        divider = ctk.CTkFrame(
            parent,
            height=2,
            fg_color="#d0d0d0",
            corner_radius=0
        )
        divider.grid(row=row, column=0, columnspan=15, sticky="ew", pady=0)

    def create_column_divider(self, parent, col):
        """Divisória vertical entre colunas"""
        divider = ctk.CTkFrame(
            parent,
            width=2,
            fg_color="#d0d0d0",
            corner_radius=0
        )
        divider.grid(row=0, column=col, rowspan=5, sticky="ns")

    def abrir_janela_cadastro(self):
        if not hasattr(self, 'janela_cadastro') or not self.janela_cadastro.winfo_exists():
            self.janela_cadastro = TelaCadastro(
                parent=self.root,
                callback_sucesso=self.atualizar_tabela
            )
            self.janela_cadastro.grab_set()
    
    def atualizar_tabela(self, nome, ra):
        table_frame = self.root.winfo_children()[2]
        ultima_linha = len(self.all_check_vars) * 2 + 2

        self.create_student_row(table_frame, ultima_linha + 1, nome, ra)
        self.create_row_divider(table_frame, ultima_linha + 2)
        self.all_check_vars.append([ctk.BooleanVar() for _ in range(6)])

def main():
    root = ctk.CTk()
    app = AttendanceApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()