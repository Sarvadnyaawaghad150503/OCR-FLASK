# main_script.py
from ocr_module import request_ocr, ENDPOINT_URL, api_key, img_loc, process_ocr_result

result = request_ocr(ENDPOINT_URL, api_key, img_loc)

if result.status_code != 200 or result.json().get('error'):
    print("Error")
else:
    result = result.json()['responses'][0]['textAnnotations']
    process_ocr_result(result)
