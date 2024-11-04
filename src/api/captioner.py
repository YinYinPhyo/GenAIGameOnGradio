import io
import requests
import json
from ..config import ITT_ENDPOINT, hf_api_key
from ..utils.image_utils import image_to_base64_str
import logging

logger = logging.getLogger(__name__)

def get_completion(image_bytes, prompt, api_url, is_json=True):
    headers = {
        "Authorization": f"Bearer {hf_api_key}"
    }
    if is_json:
        headers["Content-Type"] = "application/json"
        data = {"inputs": prompt, "image": image_to_base64_str(image_bytes)}
    else:
        data = image_bytes

    response = requests.post(api_url, headers=headers, json=data if is_json else None, data=None if is_json else data)
    response.raise_for_status()
    
    return response.json() if is_json else response.content

def captioner(image):
    if image is None:
        raise ValueError("No image provided")
    
    # Convert PIL Image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    if ITT_ENDPOINT is None:
        raise ValueError("ITT_ENDPOINT is not set in the environment variables")

    try:
        result = get_completion(img_byte_arr, None, ITT_ENDPOINT, is_json=False)
        logger.debug(f"Captioner API response: {result}")
        
        # Decode the JSON string
        decoded_result = json.loads(result.decode('utf-8'))
        
        if not decoded_result or not isinstance(decoded_result, list) or len(decoded_result) == 0:
            raise ValueError(f"Unexpected response structure from captioner API: {decoded_result}")
        
        return decoded_result[0]['generated_text']
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error communicating with the captioner API: {str(e)}")
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        raise ValueError(f"Error parsing captioner API response: {str(e)}")
    except Exception as e:
        raise ValueError(f"An unexpected error occurred during captioning: {str(e)}")
