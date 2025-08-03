# 🪪 Reconocimiento de DNI con OCR y Comparación Facial

Este proyecto permite extraer automáticamente el texto de un DNI usando OCR y comparar si el rostro en el documento coincide con otro proporcionado, utilizando reconocimiento facial con Python.

## 📸 ¿Qué hace esta app?

- Extrae datos del documento de identidad (DNI) usando OCR (`pytesseract`)
- Detecta y compara rostros en dos imágenes (DNI y selfie) usando `face_recognition`
- Expone dos endpoints REST con Flask:
  - `/ocr`: para procesar imágenes y comparar rostros
  - (Opcional) `/extract-text`: para extraer el texto del DNI

---

## ⚙️ Tecnologías utilizadas

- Python 3.10.10
- Flask
- face_recognition
- OpenCV
- Pillow
- pytesseract
- dlib (preinstalado con `.whl` para compatibilidad en Windows)

---

## 🚀 Instalación

1. **Clona el repositorio:**

```bash
git clone https://github.com/JHAMILCALI/flask-ocr.git
cd reconocimiento-dni-flask
```
- Crea un entorno virtual (opcional pero recomendado):

```bash
python -m venv venv
venv\Scripts\activate
```
- Instala las dependencias:

```bash
pip install -r requirements.txt
```
- Nota: En Windows, instala dlib manualmente con:
```bash
pip install C:\Users\ASUS\Downloads\dlib-19.22.99-cp310-cp310-win_amd64.whl
```
despues
```bash
pip install face_recognition
```
## 🧪 Cómo probar
Usando Postman o cURL
- Endpoint para obtener No. identidad
```bash
http://127.0.0.1:5000/ocr
```
- Endpoint para carnet y Imagen
```bash
http://127.0.0.1:5000/compare-faces
```
Método: POST
Tipo de cuerpo: form-data
Campos:

- image1: imagen del rostro en el DNI
![carnet](./Img%20prubas/carnet2.png)
- image2: imagen del rostro externo (selfie)
![IMG](./Img%20prubas/John-Cena.jpg)
Respuesta esperada:

```json
{
  "match": true
}
```
o

```json
{
  "error": "No se detectaron rostros en una o ambas imágenes"
}
```
## 📝 Estructura del proyecto
```bash
Reconocimiento-de-DNI-con-Python/
│
├── app.py                  # Servidor Flask
├── requirements.txt        # Dependencias
├── venv/                   # Entorno virtual
└── README.md               # Este archivo
```
## 📦 Requisitos del sistema
- Windows 10/11 (o Linux/Mac compatible con dlib)

- Python 3.10+ (recomendado 3.10.5)

- Tesseract OCR instalado:

- Descárgalo desde: https://github.com/tesseract-ocr/tesseract

- Asegúrate de agregar tesseract.exe al PATH

