import numpy as np
import cv2
from src.util.detect_face_ssd import detect_face_ssd

def detect_face(orig_frame, network, face_classifier, face_names, conf_min=0.7, threshold = 10e2, show_conf=True):
    frame, face_roi = detect_face_ssd(orig_frame, network, conf_min=conf_min, show_conf=show_conf)

    if face_roi is None:
        return orig_frame, None, "Not identified", -1
    

    # Converte para escala de cinza e redimensiona
    face_roi_gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
    face_roi_gray = cv2.resize(face_roi_gray, (90, 120))  # mesma dimensão usada no treino

    # Reconhecimento
    prediction, conf = face_classifier.predict(face_roi_gray)
    pred_aluno = face_names[prediction] if conf <= threshold else "Not identified"
    
    # Escreve nome e confiança na imagem
    if pred_aluno is "Not identified":
        return frame, face_roi, "Not identified", -1

    nome = pred_aluno["nome"]
    if nome is not None and show_conf:
        nome_formatado = nome.replace('_', ' ').title()
        text = "{}".format(nome_formatado)
        cv2.putText(frame, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    return frame, face_roi, nome, pred_aluno['RA']