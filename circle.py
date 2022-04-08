import os
import folium
import gpxpy
import numpy as np
import webbrowser as wb
from geopy.geocoders import Nominatim

PAPOU_NANOU = "55 rue Honoré de Balzac, 86530, Naintré"
CATHY = "3 rue des Tamaris, 17450 Fouras"
NANA = '4 rue du Pech, Issus'
TONY = 'Route de préseau, Marly'
MAMY = "6 rue Pierre Loti, 62330 Isbergues" 
HOME = "19 chemin de la chapelle 78114 Magny Les Hameaux France"
NEW_HOME = "14 rue des Sablons, Forges Les Bains"

DATA = {'cathy': CATHY,
        'ntgt' : PAPOU_NANOU,
        'nana' : NANA,
        'tony' : TONY,
        'mamay': MAMY,
        'home' : HOME,
        'newhome' : NEW_HOME}
RADIUS = 20000 # 1000

def print_data(data):
    for item in data:
        print(item, ' : ', data[item])

def get_lat_long(address):

     geolocator = Nominatim(user_agent="mytestapplication")
     location = geolocator.geocode(address)
     return location.address, location.latitude, location.longitude

def build_map(add, lati, longi):
    m = folium.Map(
            location=[lati, longi])
    
    folium.Circle(
        radius=RADIUS,
        location=[lati, longi],
        popup='The Waterfront',
        color='crimson',
        fill=False,
    ).add_to(m)
    
    folium.Marker([lati, longi], 
                  popup=add,
                  icon=folium.Icon(color='blue', icon='info-sign')).add_to(m)
    return m

def generate_all():
    for item in DATA: 
        add, lati, longi = get_lat_long(DATA[item])
        print(item, add)
        m = folium.Map(
            location=[lati, longi],
        #    tiles='Stamen Toner',
        #    zoom_start=13
        )
        
        folium.Circle(
            radius=RADIUS,
            location=[lati, longi],
            popup='The Waterfront',
            color='crimson',
            fill=False,
        ).add_to(m)
        
        folium.Marker([lati, longi], 
                      popup=add,
                      icon=folium.Icon(color='blue', icon='info-sign')).add_to(m)
        
        name = item
        m.save(name + '.html')

def show_my_map(inputfile):
    inputfile2 = os.path.abspath(inputfile)
    wb.open('file://'+inputfile2)

def main():
    counter = 0
    print_data(DATA)
    while True:
        counter += 1
        address = input("Type an address or a name to see the correspondng map with 20 km circle\n" )
        if address in DATA:
            address2 = DATA[address]
        else:
            address2 = address
        add, lati, longi = get_lat_long(address2)
        mymap = build_map(add, lati, longi)
        name = str(counter) + '.html' 
        mymap.save(name)
        show_my_map(name)
if __name__ == "__main__":
    main()

