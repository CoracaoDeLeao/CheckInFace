import firebase_admin
from firebase_admin import credentials, firestore
import os
from pathlib import Path
from datetime import datetime, timezone
from src.classifier.scripts.image_saver import save_image


# Caminho para o arquivo JSON da chave
current_dir = Path(__file__).parent  # Pasta do arquivo conexao.py
project_root = current_dir.parent.parent.parent  # Sobe 2 níveis até a raiz do projeto
json_path = project_root / "checkinface-private_key-adminsdk.json"

cred = credentials.Certificate(json_path)

# Inicializa o app só se ainda não foi inicializado (evita erro em importações múltiplas)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Conecta com o Firestore
db = firestore.client()

def saveFirestore(nome, ra, b64_data):
    if not b64_data:
        print(f'{nome} esta sem imagens')
        return
    
    try:
        doc_ref = db.collection("alunos").document(str(ra))
        doc_ref.set({
            "nome": nome,
            "base64": b64_data,
        })
        return True
    except Exception as e:
        print(f"Erro ao salvar: {str(e)}")
        return False

def getFirestore(ra_atual=None, limit=10):
    docs = db.collection("alunos").order_by("__name__") # Referência do documento

    if ra_atual is not None:
        print(ra_atual)
        docs = docs.start_after({"__name__": str(ra_atual)})
    
    docs = docs.limit(limit).stream()
    list_alunos = []

    for doc in docs:
        data = doc.to_dict()

        list_alunos.append({
            'nome': data["nome"],
            'RA': data.get("RA", doc.id),
            'presencas': data.get("presencas", [])
        })
        

    # if not list_alunos:
    #     raise ValueError("Documento não encontrado")
    
    return list_alunos

def salvar_presenca(ra):
    try:
        now = datetime.now(timezone.utc)

        doc_ref = db.collection("alunos").document(ra)
        doc_ref.update({
            "presencas": firestore.ArrayUnion([
                now
            ])
        })

        return True
    except Exception as e:
        return False
    
def importar_imagens(): 
    docs = db.collection("alunos").stream()
    for doc in docs:
        data = doc.to_dict()

        nome = data["nome"]
        ra = doc.id
        imgs = data["base64"]        

        if imgs is None:
            print(imgs)
            print(f'{nome} está vazio')
        else:
            sample = 1
            for img in imgs:
                save_image(nome, ra, img, sample)
                sample += 1
