import requests
import certifi

url = "https://nominatim.openstreetmap.org/search"

params = {
    "q": "Ramalingapuram, Tenali, Andhra Pradesh, India",
    "format": "json"
}

response = requests.get(
    url,
    params=params,
    headers={"User-Agent": "PATA-App"},
    verify=certifi.where()
)

print(response.json())