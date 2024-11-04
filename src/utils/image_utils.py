import io
import base64
from PIL import Image

def image_to_base64_str(pil_image):
    byte_arr = io.BytesIO()
    pil_image.save(byte_arr, format='PNG')
    return base64.b64encode(byte_arr.getvalue()).decode('utf-8')

def base64_to_pil(img_base64):
    base64_decoded = base64.b64decode(img_base64)
    return Image.open(io.BytesIO(base64_decoded))
