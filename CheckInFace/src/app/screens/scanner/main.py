import cv2
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image


def JanelaWebCam():
    """
    Abre uma nova janela CTkToplevel que captura e exibe o feed da webcam em tempo real.
    """
    # Cria a janela filha
    nova_janela = ctk.CTkToplevel()
    nova_janela.title("Scanner - Webcam")
    nova_janela.geometry("640x480")
    nova_janela.minsize(640, 480)
    nova_janela.grab_set()

    # Label para exibir o vídeo
    video_label = ctk.CTkLabel(nova_janela, text="")
    video_label.pack(fill="both", expand=True, padx=10, pady=10)

    # Inicializa captura da webcam (0 = padrão)
    captura = cv2.VideoCapture(0)

    if not captura.isOpened():
        ctk.messagebox.showerror(
            title="Erro",
            message="Não foi possível acessar a webcam. Verifique se está conectada."
        )
        nova_janela.destroy()
        return

    def atualizar_frame():
        if not nova_janela.winfo_exists():
            captura.release()
            return

        ret, frame = captura.read()
        if not ret:
            captura.release()
            nova_janela.destroy()
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(frame_rgb)

        # Criar CTkImage com o tamanho desejado
        img_ctk = CTkImage(light_image=img_pil, size=(640, 480))

        video_label.configure(image=img_ctk)
        video_label.image = img_ctk  # Manter referência para evitar coleta de lixo

        video_label.after(15, atualizar_frame)

    # Inicia loop de vídeo
    atualizar_frame()
    centralizar_janela(nova_janela)

    # Libera recursos ao fechar
    def on_close():
        captura.release()
        nova_janela.destroy()

    nova_janela.protocol("WM_DELETE_WINDOW", on_close)

def centralizar_janela(janela):
    janela.update_idletasks()
    largura_janela = janela.winfo_reqwidth()
    altura_janela = janela.winfo_reqheight()

    x = (janela.winfo_screenwidth() - largura_janela) // 2
    y = (janela.winfo_screenheight() - altura_janela) // 2

    janela.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")