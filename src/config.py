import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
_ = load_dotenv(find_dotenv())

hf_api_key = os.getenv('HF_API_KEY')
TTI_ENDPOINT = os.getenv('HF_API_TTI_BASE')
ITT_ENDPOINT = os.getenv('HF_API_ITT_BASE')
