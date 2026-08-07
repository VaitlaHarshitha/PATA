import requests
import certifi


def get_coordinates(address):

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": address,
        "format": "json"
    }

    response = requests.get(
        url,
        params=params,
        headers={"User-Agent": "PATA-App"},
        verify=certifi.where()
    )

    data = response.json()

    if data:
        return {
            "latitude": data[0]["lat"],
            "longitude": data[0]["lon"],
            "display_name": data[0]["display_name"],
            "accuracy": "Exact"
        }


    # fallback search
    parts = [x.strip() for x in address.split(",")]

    city = parts[-3]

    params["q"] = city + ", Andhra Pradesh, India"

    response = requests.get(
        url,
        params=params,
        headers={"User-Agent": "PATA-App"},
        verify=certifi.where()
    )

    data = response.json()

    if data:
        return {
            "latitude": data[0]["lat"],
            "longitude": data[0]["lon"],
            "display_name": data[0]["display_name"],
            "accuracy": "City level"
        }


    return None