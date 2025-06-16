import cv2
import numpy as np
import os
import pickle
from PIL import Image
from pathlib import Path


# Obtém o caminho da raiz
path_parent = Path(__file__).resolve().parent.parent

# Configura os caminhos usados
path_classifier = path_parent / "lbph_classifier.yml"
path_images = path_parent / "images/alunos/treinamento"
path_pickle_file = path_parent / "face_names.pickle"


# Começo do Treino
print(" > Começando treino")


# Função 
def get_image_data(path_data):
    subdirs = [os.path.join(path_data, f) for f in os.listdir(path_data)]
    faces = []
    ids = []

    face_names = {}
    id = 1   #  (starting id)
    ra = -1 # (starting RA)

    for subdir in subdirs:
        name = os.path.split(subdir)[1]
        images_list = [os.path.join(subdir, f) for f in os.listdir(subdir)]

        for path in images_list:
            try:
                image = Image.open(path).convert('L')
                face = np.array(image, 'uint8')
                face = cv2.resize(face, (90, 120))

                ids.append(id)
                faces.append(face)

                ra = os.path.basename(path).split('.')[0]
                # Log
                print(str(id) + " <-- " + path)
            except Exception as e:
                print(f'Erro ao tentar processar imagem de treino: {e}')

        face_names[id] = {'RA': ra, 'nome': name}
        id += 1
    return np.array(ids), faces, face_names

ids, faces, face_names = get_image_data(path_images)


print(face_names)


# store names and ids in a pickle file
with open(path_pickle_file, "wb") as f:
  pickle.dump(face_names, f)


# Treino
lbph = cv2.face.LBPHFaceRecognizer_create()
lbph.train(faces, ids)
lbph.write(path_classifier)


# Fim do Treino
print(" > Fim do treino")