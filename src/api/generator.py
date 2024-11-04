import io
import requests
import json
from PIL import Image
from ..config import TTI_ENDPOINT, hf_api_key
import logging
import base64

logger = logging.getLogger(__name__)

def generate(prompt):
    if not prompt:
        raise ValueError("No prompt provided")
    
    if TTI_ENDPOINT is None:
        raise ValueError("TTI_ENDPOINT is not set in the environment variables")

    try:
        response = requests.post(TTI_ENDPOINT, headers={
            "Authorization": f"Bearer {hf_api_key}",
            "Content-Type": "application/json"
        }, json={"inputs": prompt})
        
        response.raise_for_status()
        
        # Check if the response is JSON
        content_type = response.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            output = response.json()
            logger.debug(f"Image generation API JSON response: {output}")
            if isinstance(output, dict) and 'error' in output:
                raise ValueError(f"Error from API: {output['error']}")
            # Assuming the JSON response contains the image data in base64 format
            image_data = output.get('image', '')
            if not image_data:
                raise ValueError("No image data in the API response")
            image_bytes = base64.b64decode(image_data)
        else:
            # If it's not JSON, it might be the image data directly
            logger.debug(f"Image generation API response content type: {content_type}")
            image_bytes = response.content
        
        # Try to convert the output to an image
        try:
            return Image.open(io.BytesIO(image_bytes))
        except Exception as e:
            logger.error(f"Failed to convert API response to image: {str(e)}")
            raise ValueError(f"Invalid image data received from API")

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        raise ValueError(f"Error communicating with the image generation API: {str(e)}")
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        logger.error(f"Response content: {response.content[:1000]}")  # Log the first 1000 characters of the response
        raise ValueError(f"Error decoding JSON response from the image generation API: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise ValueError(f"An unexpected error occurred during image generation: {str(e)}")
