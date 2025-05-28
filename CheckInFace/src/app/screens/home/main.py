import customtkinter as ctk
from datetime import datetime, timezone

from src.app.screens.cadastro.main import TelaCadastro
from src.app.screens.scanner.main import JanelaWebCam
from src.service.conexao.conn import getFirestore

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Chamada Escolar")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        self.all_check_vars = []
        self.table_frame = None
        self.create_widgets()
        self.centralizar_janela()
        self.atualizar_tabela()
        self.agendar_atualizacoes()

    def centralizar_janela(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        top_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        top_frame.pack(side="top", fill="x", padx=20, pady=10)

        top_frame.grid_columnconfigure(0, weight=1, uniform="cols_espacadoras")
        top_frame.grid_columnconfigure(1, weight=0, uniform="cols_espacadoras")
        top_frame.grid_columnconfigure(2, weight=1, uniform="cols_espacadoras")

        ctk.CTkLabel(
            top_frame, 
            text="Controle de Frequência",
            font=("Arial", 18, "bold"),
        ).grid(row=0, column=1)

        self._create_button(top_frame, "Cadastrar", self.abrir_janela_cadastro, 2, "e")
        self._create_button(top_frame, "Scanear", JanelaWebCam, 0, "w")

        self.table_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.table_frame.pack(fill="both", expand=True, padx=0, pady=10)

        for col in range(15):
            if col % 2 == 0:
                minsize = 200 if col == 0 else (150 if col == 2 else 80)
                self.table_frame.columnconfigure(col, weight=1, minsize=minsize)
            else:
                self.table_frame.columnconfigure(col, weight=0, minsize=2)

        for r in range(50):  # permitir várias linhas de aluno sem erro
            self.table_frame.rowconfigure(r, weight=0, minsize=40 if r % 2 != 0 else 2)

        self.criar_cabecalhos()
        self.create_row_divider(self.table_frame, 0)

    def _create_button(self, parent, text, command, column, sticky):
        btn = ctk.CTkButton(
            parent,
            text=text,
            width=100,
            font=("Arial", 14, "bold"),
            command=command
        )
        btn.grid(row=0, column=column, sticky=sticky)
        return btn

    def criar_cabecalhos(self):
        headers = ["Aluno", "RA", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"]
        for idx, header in enumerate(headers):
            col = idx * 2
            self.table_frame.columnconfigure(col, weight=1, minsize=150 if idx < 2 else 80)

            # Frame externo com cor de fundo
            header_bg = ctk.CTkFrame(self.table_frame, fg_color="transparent", corner_radius=0)
            header_bg.grid(row=1, column=col, sticky="ew")

            # Frame interno para o label
            header_inner = ctk.CTkFrame(header_bg, fg_color="transparent")
            header_inner.pack(expand=True, fill="both", padx=1, pady=1)

            ctk.CTkLabel(
                header_inner,
                text=header,
                font=("Arial", 14, "bold")
            ).pack(expand=True, fill="both")

            if idx > 0:
                self.create_column_divider(self.table_frame, col - 1)

    def create_student_row(self, parent, row, nome="", ra=""):
        aluno_frame = ctk.CTkFrame(parent, fg_color="transparent")
        aluno_frame.grid(row=row, column=0, sticky="ew", padx=5, pady=5)

        ctk.CTkLabel(
            aluno_frame,
            text=nome,
            anchor="center"
        ).pack(expand=True, fill="both")

        ra_frame = ctk.CTkFrame(parent, fg_color="transparent")
        ra_frame.grid(row=row, column=2, sticky="ew", padx=5, pady=5)

        ctk.CTkLabel(
            ra_frame,
            text=ra,
            anchor="center"
        ).pack(expand=True, fill="both")

        check_vars = []
        for idx, col in enumerate(range(4, 16, 2)):
            var = ctk.BooleanVar()
            main_frame = ctk.CTkFrame(parent, width=80, height=20, fg_color="transparent")
            main_frame.grid(row=row, column=col, sticky="nsew")

            ctk.CTkCheckBox(
                main_frame,
                text="",
                variable=var,
                width=24,
                height=24,
                border_width=2
            ).place(relx=0.5, rely=0.5, anchor="center")

            check_vars.append(var)
            if idx < 4:
                self.create_column_divider(parent, col + 1)

        self.all_check_vars.append(check_vars)

    def create_divider(self, parent, **kwargs):
        return ctk.CTkFrame(
            parent,
            fg_color="#d0d0d0",
            corner_radius=0,
            **kwargs
        )

    def create_column_divider(self, parent, col):
        self.create_divider(parent, width=2).grid(
            row=0, column=col, rowspan=1000, sticky="ns"
        )
        
    def create_row_divider(self, parent, row):
        self.create_divider(parent, height=2).grid(
            row=row, column=0, columnspan=15, sticky="ew", pady=0
        )

    def abrir_janela_cadastro(self):
        if not hasattr(self, 'janela_cadastro') or not self.janela_cadastro.winfo_exists():
            self.janela_cadastro = TelaCadastro(
                parent=self.root,
                callback_sucesso=self.atualizar_tabela
            )
            self.janela_cadastro.grab_set()

    def atualizar_tabela(self):
        loading = ctk.CTkLabel(self.root, text="Carregando dados...", font=("Arial", 16))
        loading.place(relx=0.5, rely=0.5, anchor="center")
        self.root.update_idletasks()

        for widget in self.table_frame.winfo_children():
            if int(widget.grid_info().get('row', 0)) > 1:
                widget.destroy()

        self.all_check_vars = []
        current_row = 2
        
        for aluno in getFirestore():
            self.create_row_divider(self.table_frame, current_row)
            self.create_student_row(self.table_frame, current_row + 1, aluno['nome'], aluno['RA'])

            if self.all_check_vars:
                self.marcar_presencas(self.all_check_vars[-1], aluno.get('presencas', []))

            current_row += 2

        self.create_row_divider(self.table_frame, current_row)
        loading.destroy()

    def marcar_presencas(self, check_vars, presencas):
        dias_presentes = set()
        data_atual = datetime.now(timezone.utc).astimezone()
        ano_atual, semana_atual, _ = data_atual.isocalendar()

        for presenca in presencas:
            try:
                data_local = presenca['data'].astimezone()
                ano_presenca, semana_presenca, _ = data_local.isocalendar()

                if ano_presenca == ano_atual and semana_presenca == semana_atual:
                    dias_presentes.add(data_local.weekday())
            except Exception as e:
                print(f"Erro ao processar data: {e}")

        for idx, var in enumerate(check_vars[:6]):
            var.set(idx in dias_presentes)

    def agendar_atualizacoes(self):
        self.atualizar_tabela()
        self.root.after(100000, self.agendar_atualizacoes)

def main():
    root = ctk.CTk()
    AttendanceApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
