from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import io
import os  # <-- Añade esta línea
import re

app = Flask(__name__)

# Configuración de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'  # Ahora funcionará

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)