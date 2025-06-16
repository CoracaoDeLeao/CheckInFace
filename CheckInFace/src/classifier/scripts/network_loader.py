import cv2
from pathlib import Path


# Obtém o caminho da raiz
path_parent = Path(__file__).resolve().parent.parent

# Configura os caminhos usados
path_deploy = path_parent / "deploy.prototxt.txt"
path_caffemodel = path_parent / "res10_300x300_ssd_iter_140000.caffemodel"

def get_network():
    network = cv2.dnn.readNetFromCaffe(path_deploy, path_caffemodel)
    return network