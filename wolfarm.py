import wolframalpha

def wolframalpha_get(query, app_id = 'QXP9AK-TV9K6E3HUY'):
    client = wolframalpha.Client(app_id)
    try:
        result = client.query(query)

        for pod in result.pods:
            if pod.title == "Result":
                return pod.text
        else:
            return None
        
    except Exception as e:
        print(f"Error: {e}")

