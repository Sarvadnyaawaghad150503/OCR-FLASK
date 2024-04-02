# ocr_module.py

import json
import requests
from base64 import b64encode

def make_image_data(imgpath):
    with open(imgpath, 'rb') as f:
        ctxt = b64encode(f.read()).decode()
        img_req = {
            'image': {
                'content': ctxt
            },
            'features': [{
                'type': 'DOCUMENT_TEXT_DETECTION',
                'maxResults': 1
            }]
        }
    return json.dumps({"requests": img_req}).encode()

def request_ocr(url, api_key, imgpath):
    imgdata = make_image_data(imgpath)
    response = requests.post(url,
                             data=imgdata,
                             params={'key': api_key},
                             headers={'Content-Type': 'application/json'})
    return response

def process_ocr_result(response):
    if response.status_code != 200 or response.json().get('error'):
        return "Error in OCR request"

    result = response.json().get('responses', [])
    if not result:
        return "No OCR result found"

    ocr_annotations = result[0].get('textAnnotations', [])

    if not ocr_annotations:
        return "No text annotations found"

    # Extract lines with standalone integers and their font sizes
    lines_with_integers = [(annotation.get('description', '').strip(), annotation.get('fontSize', 0))
                           for annotation in ocr_annotations
                           if annotation.get('description', '').replace('.', '', 1).isdigit()
                           and not any(char.isalpha() for char in annotation.get('description', ''))]

    if lines_with_integers:
        # Return the line with the largest font size
        largest_font_line = max(lines_with_integers, key=lambda x: x[1])
        return largest_font_line[0]
    else:
        return "No line with standalone integer found in the text annotations"

# Example additional constant
ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'
# api_key = 'AIzaSyBmQjVFEudXg7RPKFzYUPSJdWnzr5JcSEI'
api_key = 'AIzaSyC410uHETKEYonXSmxh4yl5sHVdtdiuX34'
img_loc = r"C:\Users\ameya\OneDrive\Desktop\WhatsApp Image 2023-11-29 at 08.28.38.jpeg"
