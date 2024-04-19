import requests
from PIL import Image
import uuid
import io
from config import IMAGE_GENERATION_TOKEN

API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
headers = {"Authorization": "Bearer " + IMAGE_GENERATION_TOKEN}

client = requests.Session()

def query(query, path):
	try:
		response = client.post(API_URL, headers=headers, json={"inputs": query})
		p = path + str(uuid.uuid4()) + ".jpg"
		Image.open(io.BytesIO(response.content)).save(p)
		return p

	except Exception as e:
		print(e)
		return None
	
def close():
	client.close()