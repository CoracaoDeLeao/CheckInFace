import base64
import cv2

def image_to_base64(image):
    try:
        _, buffer = cv2.imencode('.jpg', image)
        img = base64.b64encode(buffer).decode("utf-8")
        return img
            
    except FileNotFoundError:
        raise ValueError("Arquivo de imagem não encontrado")

def base64_to_image(b64_str, output_path):
    try:
        img_data = base64.b64decode(b64_str)
        with open(output_path, "wb") as f:
            f.write(img_data)
        print(f"Imagem salva em: {output_path}")
    except Exception as e:
        print(f"Erro na decodificação: {str(e)}")