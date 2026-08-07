import re


def parse_address(address):

    result = {
        "landmark": [],
        "locality": "",
        "city": ""
    }

    address = address.lower()

    # Find landmarks
    if "opposite" in address:
        part = address.split("opposite")[1]
        landmark = part.split(",")[0]
        result["landmark"].append(landmark.strip())

    if "near" in address:
        part = address.split("near")[1]
        landmark = part.split(",")[0]
        result["landmark"].append(landmark.strip())


    # Split remaining parts
    parts = [x.strip() for x in address.split(",")]


    if len(parts) >= 2:
        result["locality"] = parts[-2]

        result["city"] = parts[-1]


    return result