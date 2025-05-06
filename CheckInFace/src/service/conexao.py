import firebase_admin
from firebase_admin import credentials, firestore
import os
from pathlib import Path

# Caminho para o arquivo JSON da chave
current_dir = Path(__file__).parent  # Pasta do arquivo conexao.py
project_root = current_dir.parent.parent  # Sobe 2 níveis até a raiz do projeto
json_path = project_root / "checkinface-private_key-adminsdk.json"

cred = credentials.Certificate(json_path)

# Inicializa o app só se ainda não foi inicializado (evita erro em importações múltiplas)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Conecta com o Firestore
db = firestore.client()

def saveFirestore(nome, RA, b64_data):
    try:
        doc_ref = db.collection("alunos").document()
        doc_ref.set({
            "nome": nome,
            "RA": RA,
            "base64": b64_data,
        })
        return True
    except Exception as e:
        print(f"Erro ao salvar: {str(e)}")
        return False

# def getFirestore():
#     doc_ref = db.collection("alunos").document("BASE64_TOP")
#     doc = doc_ref.get()
    
#     if doc.exists:
#         data = doc.to_dict()
#         return data["base64"], data["format"]
#     else:
#         raise ValueError("Documento não encontrado")