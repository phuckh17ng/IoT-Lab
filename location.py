from geopy.geocoders import Photon
import geocoder

#initialize the Nominatim object
Nomi_locator = Photon(user_agent="My App")

my_location= geocoder.ip('me')

#my latitude and longitude coordinates
latitude= my_location.geojson['features'][0]['properties']['lat']
longitude = my_location.geojson['features'][0]['properties']['lng']

#get the location
location = Nomi_locator.reverse(f"{latitude}, {longitude}")
print(latitude,' ',longitude)