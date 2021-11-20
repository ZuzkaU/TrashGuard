from flask import Flask, request, render_template
import overpy
import requests, json
import database

def getMap():
    area = 5000
    
    url = 'https://api.freegeoip.app/json/{}?apikey=a7428a00-4a36-11ec-8912-ef59e2b118f7'.format(request.remote_addr)
    response = requests.get(url)
    location = json.loads(response.text)
    lat = location['latitude']
    lon = location['longitude']
    lat, lon = 48.11004353217281, 11.587360738996582

    id_counter = 0
    markers = ''
    
    api = overpy.Overpass()


    waste_baskets_query = """(node["amenity"="waste_basket"](around:{area},{lat},{lon}););out;""".format(area=area, lat=lat, lon=lon)
    waste_baskets = api.query(waste_baskets_query)
    for node in waste_baskets.nodes:
        markers += "markers.addLayer(L.marker([{latitude}, {longitude}], {{icon: waste_basket_icon}}).bindPopup('{name}'));".format(latitude=node.lat, longitude=node.lon, name='Waste basket');


    waste_disposal_query = """(node["amenity"="waste_disposal"](around:{area},{lat},{lon}););out;""".format(area=area, lat=lat, lon=lon)
    waste_disposal = api.query(waste_disposal_query)
    for node in waste_disposal.nodes:
        markers += "markers.addLayer(L.marker([{latitude}, {longitude}], {{icon: waste_disposal_icon}}).bindPopup('{name}'));".format(latitude=node.lat, longitude=node.lon, name='Waste disposal');


    recycling_query = """(node["amenity"="recycling"](around:{area},{lat},{lon}););out;""".format(area=area, lat=lat, lon=lon)
    recycling = api.query(recycling_query)
    for node in recycling.nodes:
        markers += "markers.addLayer(L.marker([{latitude}, {longitude}], {{icon: recycling_icon}}).bindPopup('{name}'));".format(latitude=node.lat, longitude=node.lon, name='Recycling');


    active_requests = database.get_active_requests()
    for node in active_requests:
        markers += "markers.addLayer(L.marker([{latitude}, {longitude}]).bindPopup('{name}'));".format(latitude=node[1], longitude=node[2], name='Reported trash<br>'+node[4]);
    
    
    # Render the page with the map
    return render_template('map.html', markers=markers, lat=lat, lon=lon)
    
