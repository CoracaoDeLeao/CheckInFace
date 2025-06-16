from pathlib import Path
import os
import cv2

from src.util.base64 import base64_to_image

# Obtém o caminho da raiz
path_parent = Path(__file__).resolve().parent.parent

path_images = path_parent / "images" / "alunos" / "treinamento"

def create_folders(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_image(nome, ra, face_roi, sample):
    photo_sample = sample if sample > 0 else 0

    image_name = ra + "." + str(photo_sample) + ".jpg"
    final_path = os.path.sep.join([str(path_images), nome.replace(' ', '_').lower()])
    create_folders(str(final_path))

    
    output_path = os.path.join(final_path, image_name)

    if isinstance(face_roi, str):
        base64_to_image(face_roi,output_path)
    else:
        cv2.imwrite(final_path + "/" + image_name, face_roi) 
    print("=> photo " + str(sample))