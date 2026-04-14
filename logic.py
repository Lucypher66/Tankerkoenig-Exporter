import requests

def prometheus_escape(value):
    value = str(value)
    value = value.replace("\\", "\\\\")
    value = value.replace("\n", "\\n")
    value = value.replace('"', '\\"')
    return value

def request_data(request):
    r = requests.get(request, timeout=10)
    r.raise_for_status()

    try:
        payload = r.json()
    except ValueError:
        return {"raw": r.text}

    if isinstance(payload, dict):
        return payload

    return {"data": payload}

def build_request(station_id,api_key):
    request = f'https://creativecommons.tankerkoenig.de/json/detail.php?id={station_id}&apikey={api_key}'
    return request