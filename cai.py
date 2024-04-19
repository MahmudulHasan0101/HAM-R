import tls_client
import json
from config import CAI_TOKEN

class caiAPIError(Exception):
    pass

class ServerError(caiAPIError):
    pass

class LabelError(caiAPIError):
    pass

class AuthError(caiAPIError):
    pass

class PostTypeError(caiAPIError):
    pass


AI_PUBLIC_IDs = {
    "Default"     : "YntB_ZeqRq2l_aVf2gWDCZl4oBttQzDvhj9cXafWcF8",
    "Assistant"   : "_nZnN3nSjh5iPHx3X62kpstpuS_QF6a-JOehZeL6oUk",
    "Doctor"      : "A84TZGxGy7PWIp7kuPkmZzC9j-PJnwEJASjGqCy_cPQ",
    "Astrophysicst": "L2x_xNQwUmUfaimIiwvaoirLpa0Aw9PZXimLqKkb6wA",
    "Teacher"     : "NrvAmvd7qjuVQ7ofsGNfS9yKOHiL9zPpCn064KYY3HU"
}

token = CAI_TOKEN

session = tls_client.Session(
    client_identifier='firefox_120'
)

tgt = ""
id = ""


setattr(session, 'url', f'https://beta.character.ai/')
setattr(session, 'token', token)


def handle_error(data):
    if str(data).startswith("{'detail': 'Auth"):
        raise AuthError('Invalid token')
    elif str(data).startswith("{'status': 'Error"):
        raise ServerError(data['status'])
    elif str(data).startswith("{'error'"):
        raise ServerError(data['error'])


def get(
    url: str, session: tls_client.Session, split: bool = False,
):
    link = f'{session.url}{url}'

    headers = {'Authorization': f'Token {session.token}'}

    response = session.get(link, headers=headers)
    print("GET: ", response)
    
    try:
        if split:
            data = json.loads(response.text.split('\n')[-2])
        else:
            data = response.json()
            
        handle_error(data)
        return data
        
    except Exception as e:
        print(e)


def post(
    url: str, session: tls_client.Session, data: dict = None, split: bool = False
):
    link = f'{session.url}{url}'

    headers = {'Authorization': f'Token {session.token}'}

    response = session.post(link, headers=headers, json=data)
    print("POST: ", response)
    
    try:
        if split:
            data = json.loads(response.text.split('\n')[-2])
        else:
            data = response.json()
        
        handle_error(data)
        return data
        
    except Exception as e:
        print(e)



def create_charecter(
    greeting: str,   
    identifier: str,
    name: str, *, 
    copyable: bool = True, 
    definition: str = '',
    description: str = '',
    title: str = '',
    img_gen_enabled: bool = False,
    visibility: str = 'PUBLIC', 
    **kwargs
):
    return post(
            url = '../chat/character/create/',
            session = session,
            data={
                'greeting': greeting,
                'identifier': identifier,
                'name': name,
                'copyable': copyable,
                'definition': definition,
                'description': description,
                'img_gen_enabled': img_gen_enabled,
                'title': title,
                'visibility': visibility,
                **kwargs
            }
        )



def update_charecter(
    public_id: str,
    greeting: str,
    name: str,
    title: str = '',
    definition: str = '',
    copyable: bool = True, 
    description: str = '',
    visibility: str = 'PUBLIC', 
    **kwargs
):
    return post(
        url = '../chat/character/update/', 
        session = session,
        data={
            'external_id': public_id,
            'name': name,
            'title': title,
            'visibility': visibility,
            'copyable': copyable,
            'description': description,
            'greeting': greeting,
            'definition': definition,
            **kwargs
        }
    )


def charecter_info(
    char: str, *,
    token: str = None,
):
    return post(
        url = 'chat/character/', 
        session = session,
        data = {
            'external_id': char
    }
)


def get_chat(
    public_id: str = None
):
    return post(
        url = 'chat/history/continue/', 
        session = session,
        data={
            'character_external_id': public_id,
        }
    )


def set_mode(mode):
    chat = get_chat(AI_PUBLIC_IDs[mode])
    print("CHAT: ", chat)
    participants = chat['participants']

    if not participants[0]['is_human']:
        tgt = participants[0]['user']['username']
    else:
        tgt = participants[1]['user']['username']

    id = chat['external_id']
    print("ID: ", id)
    

def message(text : str):
    data = send_message(id, tgt, text)
    print("DATA: ", data)
    
    try:
        replay = data['replies'][0]['text']
        return replay
        
    except Exception as e:
        print(e)
        return "Sorry couldn't reach you at the moment, would you please say again?"


def send_message(
    history_id: str, tgt: str, text: str,
    **kwargs
):
    return post(
        url = 'chat/streaming/', 
        session = session,
        split = True,
        data = {
            'history_external_id': history_id,
            'tgt': tgt,
            'text': text,
            **kwargs
        }
    )


def new_chat(
    public_id: str
):
    return post(
        url = 'chat/history/create/', 
        session = session,
        data = {
            'character_external_id': public_id
        }
    )


new_chat("Default")
set_mode("Default")