import requests
from config import BLACKBOX_API_KEY

headers = {
    'Content-Type': 'application/json',
    'key': BLACKBOX_API_KEY,  # Replace with your actual API key
}



url = "https://blackbox.ai/api/inference"
client = requests.Session()

def talk(query):
    data = {
    "messages": [
        {
            "role": "user",
            "content": query
        }
    ]
    }
    
    try:
        response = client.post(url, headers=headers, json=data)
        print(response)
        return response.json()["message"]["content"]
        
    except Exception as e:
        print (e)
        return "Sorry couldn't reach you at the moment, would you please say again?"
    

def close():
    client.close()
