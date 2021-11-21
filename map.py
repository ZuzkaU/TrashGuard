from flask import Flask, request, render_template
import overpy
import requests, json
import database

def getMap():
    area = 10000
    
    url = 'https://api.freegeoip.app/json/{}?apikey=a7428a00-4a36-11ec-8912-ef59e2b118f7'.format(request.remote_addr)
    response = requests.get(url)
    location = json.loads(response.text)
    lat = location['latitude']
    lon = location['longitude']
    lat, lon = 48.1431647, 11.5747058

    id_counter = 0
    
    api = overpy.Overpass()

    baskets = ''
    waste_baskets_query = """(node["amenity"="waste_basket"](around:{area},{lat},{lon}););out;""".format(area=area, lat=lat, lon=lon)
    waste_baskets = api.query(waste_baskets_query)
    for node in waste_baskets.nodes:
        baskets += "baskets.addLayer(L.marker([{latitude}, {longitude}], {{icon: waste_basket_icon}}).bindPopup('{name}'));".format(latitude=node.lat, longitude=node.lon, name='Waste basket');

    disposal = ''
    waste_disposal_query = """(node["amenity"="waste_disposal"](around:{area},{lat},{lon}););out;""".format(area=area, lat=lat, lon=lon)
    waste_disposal = api.query(waste_disposal_query)
    for node in waste_disposal.nodes:
        disposal += "disposal.addLayer(L.marker([{latitude}, {longitude}], {{icon: waste_disposal_icon}}).bindPopup('{name}'));".format(latitude=node.lat, longitude=node.lon, name='Waste disposal');

    recycling = ''
    recycling_query = """(node["amenity"="recycling"](around:{area},{lat},{lon}););out;""".format(area=area, lat=lat, lon=lon)
    recycling_results = api.query(recycling_query)
    for node in recycling_results.nodes:
        recycling += "recycling.addLayer(L.marker([{latitude}, {longitude}], {{icon: recycling_icon}}).bindPopup('{name}'));".format(latitude=node.lat, longitude=node.lon, name='Recycling');

    reported = ''
    active_requests = database.get_active_requests()
    for node in active_requests:
        reported += "reported.addLayer(L.marker([{latitude}, {longitude}]).bindPopup('{name}'));".format(latitude=node[1], longitude=node[2], name='Reported trash<br>'+node[4]);
    
    
    # Render the page with the map
    return render_template('map.html', baskets=baskets, disposal=disposal, recycling=recycling, reported=reported, lat=lat, lon=lon)
    
