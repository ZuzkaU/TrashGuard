from flask import Flask, request, render_template
import overpy
import database

def getMap():
    lat, lon = 48.11004353217281, 11.587360738996582
    area = 1000

    id_counter = 0
    markers = ''
    
    api = overpy.Overpass()
    
    show_waste_baskets = True
    show_waste_disposal = True
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
            markers += "var {idd} = L.marker([{latitude}, {longitude}], {{icon: recycling_icon}});\
                        {idd}.addTo(map).bindPopup('{name}');".format(idd=idd, latitude=node.lat,\
                        longitude=node.lon,
                        name='Recycling')
    
    if show_active_requests:
        active_requests = database.get_active_requests()
        for node in active_requests:
            idd = node[3] + str(id_counter)
            id_counter += 1
            markers += "var {idd} = L.marker([{latitude}, {longitude}]);\
                        {idd}.addTo(map).bindPopup('{name}');".format(idd=idd, latitude=node[1],\
                        longitude=node[2],
                        name=node[4])
    

    # Render the page with the map
    return render_template('map.html', markers=markers, lat=lat, lon=lon)
    
