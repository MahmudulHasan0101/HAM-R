from g4f.client import Client

client = Client()

setting = "(You name is HAM-R, created by two students, you are a assistant, you main goal is to assist people)"

def message(promt : str):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role" : "user", "content" : setting}, {"role": "user", "content": promt}]
        )   
        return response.choices[0].message.content

    except Exception as e:
        print(e)
        return "Extreamly sorry, couldn't connect to you at the moment"


def set_mode(mode : str):
    global setting
    setting = f"(You name is HAM-R, created by two students, you are a {mode}, you main goal is to assist people)"