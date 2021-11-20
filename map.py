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
    markers = 'var markers = L.markerClusterGroup();'
    
    api = overpy.Overpass()
    
    show_waste_baskets = False
    show_waste_disposal = False
    show_recycling = True
    show_active_requests = True

    if show_waste_baskets:
        waste_baskets_query = """(node["amenity"="waste_basket"](around:{area},{lat},{lon}););out;""".format(area=area, lat=lat, lon=lon)
        waste_baskets = api.query(waste_baskets_query)
        for node in waste_baskets.nodes:
            idd = 'waste_basket' + str(id_counter)
            id_counter += 1
            markers += "var {idd} = L.marker([{latitude}, {longitude}], {{icon: waste_basket_icon}});\
                        {idd}.addTo(map).bindPopup('{name}');".format(idd=idd, latitude=node.lat,\
                        longitude=node.lon,
                        name='Waste basket')


    if show_waste_disposal:
        waste_disposal_query = """(node["amenity"="waste_disposal"](around:{area},{lat},{lon}););out;""".format(area=area, lat=lat, lon=lon)
        waste_disposal = api.query(waste_disposal_query)
        for node in waste_disposal.nodes:
            idd = 'waste_disposal' + str(id_counter)
            id_counter += 1
            markers += "var {idd} = L.marker([{latitude}, {longitude}], {{icon: waste_disposal_icon}});\
                        {idd}.addTo(map).bindPopup('{name}');".format(idd=idd, latitude=node.lat,\
                        longitude=node.lon,
                        name='Waste disposal')

    if show_recycling:
        recycling_query = """(node["amenity"="recycling"](around:{area},{lat},{lon}););out;""".format(area=area, lat=lat, lon=lon)
        recycling = api.query(recycling_query)
        for node in recycling.nodes:
            idd = 'recycling' + str(id_counter)
            id_counter += 1
            markers += "markers.addLayer(L.marker([{latitude}, {longitude}], {{icon: recycling_icon}}).bindPopup('{name}'));".format(idd=idd, latitude=node.lat, longitude=node.lon, name='Recycling');


    if show_active_requests:
        active_requests = database.get_active_requests()
        for node in active_requests:
            idd = node[3] + str(id_counter)
            id_counter += 1
            markers += "var {idd} = L.marker([{latitude}, {longitude}]);\
                        {idd}.addTo(map).bindPopup('{name}');".format(idd=idd, latitude=node[1],\
                        longitude=node[2],
                        name=node[4])
    
    markers += "map.addLayer(markers);"
    # Render the page with the map
    return render_template('map.html', markers=markers, lat=lat, lon=lon)
    
