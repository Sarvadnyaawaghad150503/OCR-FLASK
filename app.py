# app.py
from flask import Flask, render_template, request, jsonify
from ocr_module import request_ocr, ENDPOINT_URL, api_key, process_ocr_result

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"})

    # Save the uploaded file (you may want to store it in a more secure way)
    file.save("uploaded_image.jpg")

    # Perform OCR
    img_loc = "uploaded_image.jpg"
    result = request_ocr(ENDPOINT_URL, api_key, img_loc)

    # Process OCR result
    processed_result = process_ocr_result(result)

    return jsonify({"result": processed_result})

if __name__ == "__main__":
    app.run(debug=True)
