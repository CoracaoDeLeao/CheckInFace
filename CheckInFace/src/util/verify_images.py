from pathlib import Path
from src.service.conexao.conn import importar_imagens
from src.classifier.scripts.model_loader import get_model
import os


# Obtém o caminho da raiz
path_parent = Path(__file__).resolve().parent.parent
path_images = path_parent / 'classifier' / 'images'

def verify_images():
    if not os.path.exists(str(path_images)):
        importar_imagens()
        get_model()
        print(" > Término de imports de imagens")