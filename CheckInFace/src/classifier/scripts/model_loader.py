from pathlib import Path
import subprocess
import cv2
import pickle


# Obtém o caminho da raiz
path_parent = Path(__file__).resolve().parent

# Configura os caminhos usados
path_train_script = path_parent / "train_model.py"
path_classifier = path_parent.parent / "lbph_classifier.yml"
path_pickle_file = path_parent.parent / "face_names.pickle"

def get_model(parse=False):    
    # Verify if file exists
    if not path_classifier.is_file() or parse:
        try:
            subprocess.run(['python', str(path_train_script)], check=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f'[ERROR : Erro ao executar treino de modelo]')
            raise

        if not path_classifier.is_file():
            raise FileNotFoundError("[ERROR : Modelo não foi criado]")
    
    # read model
    face_classifier = cv2.face.LBPHFaceRecognizer_create()
    face_classifier.read(str(path_classifier))

    # load names from pickle file
    face_names = {}
    with open(path_pickle_file, "rb") as f:
        original_labels = pickle.load(f)
        # [ID] : Nome e RA
        face_names = {id_ : {'nome': info['nome'], 'RA': info['RA']} for id_, info in original_labels.items()}
        
        

    return face_classifier, face_names