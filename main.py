from parser import parse_address
from geocoder import get_coordinates
from database import create_database, save_location, get_locations


create_database()


address = "Opposite Ganesh temple, near Sai bakery, Ramalingapuram, Tenali"


parsed = parse_address(address)


clean_address = (
    parsed["locality"] +
    ", " +
    parsed["city"] +
    ", Andhra Pradesh, India"
)


location = get_coordinates(clean_address)


save_location(address, parsed, location)


print("Stored Successfully")


print("\nDatabase Records:")

for row in get_locations():
    print(row)