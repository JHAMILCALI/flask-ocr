from flask import Flask, request, jsonify
import pytesseract
import face_recognition
import numpy as np
from PIL import Image
import io
import os
import re

app = Flask(__name__)

# Configuración de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'image' not in request.files:
        return jsonify({'error': 'No se encontró ninguna imagen'}), 400

    file = request.files['image']
    try:
        image = Image.open(io.BytesIO(file.read()))
        text = pytesseract.image_to_string(image, lang='spa')

        # Regex para extraer el número de CI después de "No.", "N°", etc.
        priority_pattern = r'(?:No|N°|NUMERO)[\s.:]*[\$]?\s*(\d{7,8})'
        priority_match = re.search(priority_pattern, text, re.IGNORECASE)

        if priority_match:
            return jsonify({'ci': priority_match.group(1)})

        # Fallback: Busca cualquier número de 7-8 dígitos
        fallback_match = re.search(r'\b\d{7,8}\b', text)
        if fallback_match:
            return jsonify({'ci': fallback_match.group(0)})

        return jsonify({'error': 'No se encontró un número de CI válido'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/compare-faces', methods=['POST'])
def compare_faces():
    if 'image1' not in request.files or 'image2' not in request.files:
        return jsonify({"error": "Faltan imágenes"}), 400

    image1_file = request.files['image1']
    image2_file = request.files['image2']

    try:
        image1 = Image.open(io.BytesIO(image1_file.read())).convert('RGB')
        image2 = Image.open(io.BytesIO(image2_file.read())).convert('RGB')

        image1_np = np.array(image1)
        image2_np = np.array(image2)

        encodings1 = face_recognition.face_encodings(image1_np)
        encodings2 = face_recognition.face_encodings(image2_np)

        print("Encodings1:", len(encodings1))
        print("Encodings2:", len(encodings2))

        if not encodings1 or not encodings2:
            return jsonify({"error": "No se detectaron rostros en una o ambas imágenes"}), 400

        result = face_recognition.compare_faces([encodings1[0]], encodings2[0])

        return jsonify({"match": bool(result[0])})  # 👈 esta es la corrección

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Error al procesar las imágenes", "detail": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)