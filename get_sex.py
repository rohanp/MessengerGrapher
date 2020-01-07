from requests import get

def get_sex(name):
    """
    Guess the gender of the sender based on gender-api.
    """
    if len(name.split(" ")) != 1:
        name = name.split(" ")[0]

    url = "https://gender-api.com/get?key=" + API_KEY + "&name=" + name

    try:
        response = get(url)
        data = response.json()

        return data["gender"]
    except Exception:
        return "unknown"