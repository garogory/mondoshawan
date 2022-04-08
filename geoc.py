from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="mytestapplication")
HOME = "19 chemin de la chapelle 78114 Magny Les Hameaux France" 
NEW_HOME = "14 rue des Sablons, Forges Les Bains" 
location = geolocator.geocode(NEW_HOME)
print(location.address)
print(location.latitude, location.longitude)
