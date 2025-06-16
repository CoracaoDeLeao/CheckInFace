import cv2
import customtkinter as ctk
from tkinter import messagebox
from customtkinter import CTkImage
from PIL import Image

from src.classifier.scripts.model_loader import get_model
from src.classifier.scripts.network_loader import get_network
from src.util.detect_face import detect_face

def JanelaWebCam(on_press, on_press_key="q", show_conf=True):
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

    # Inicializa classificador
    face_classifier, face_names = get_model()
    network = get_network()

    # Inicializa captura da webcam (0 = padrão)
    captura = cv2.VideoCapture(0)    

    # 
    reg_aluno = {}
    reg_frame = [None, None]

    if not captura.isOpened():
        messagebox.showerror(
            title="Erro",
            message="Não foi possível acessar a webcam. Verifique se está conectada."
        )
        nova_janela.destroy()
        return    

    # Evento de clique:
    def event_on_press(event):
        if event.char == on_press_key and reg_frame[0] is not None:
            action = on_press(reg_frame[0], reg_frame[1], reg_aluno[0])

            if action == 'close':
                on_close()

    # Atualização do frame:
    def atualizar_frame():
        if not nova_janela.winfo_exists():
            captura.release()
            return

        ret, frame = captura.read()
        if not ret:
            captura.release()
            nova_janela.destroy()
            return

        # Desenha informação de detecção facial
        frame, face_roi, nome, id = detect_face(frame, network, face_classifier, face_names, threshold = 10e1, show_conf=show_conf)
        reg_frame[0] = frame
        reg_frame[1] = face_roi if face_roi is not None else None
        
        if nome is not None:
            reg_aluno[0] = id
        else:
            reg_aluno[0] = {}

        # Criar CTkImage com o tamanho desejado
        img_rgb_final = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil_final = Image.fromarray(img_rgb_final)
        img_ctk = CTkImage(light_image=img_pil_final, size=(640, 480))

        video_label.configure(image=img_ctk)
        video_label.image = img_ctk  # Manter referência para evitar coleta de lixo

        video_label.after(15, atualizar_frame)

    # Inicia loop de vídeo
    atualizar_frame()
    centralizar_janela(nova_janela)

    # Registra evento de clique
    nova_janela.bind(f'<KeyPress-{on_press_key}>', event_on_press)

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