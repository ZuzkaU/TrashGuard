from flask import Flask, request, render_template
import overpy

def getMap():
    lat, lon = 48.11004353217281, 11.587360738996582

    id_counter = 0
    markers = ''
    api = overpy.Overpass()
    # Define the query
    query = """(node["shop"](around:500,{lat},{lon});
            node["building"="retail"](around:500,{lat},{lon});
            node["building"="supermarket"](around:500,{lat},{lon});
            node["healthcare"="pharmacy"](around:500,{lat},{lon});
            );out;""".format(lat=lat, lon=lon)

    # Call the API
    shops = api.query(query)


    for node in shops.nodes:

            # Create unique ID for each marker
            idd = 'shop' + str(id_counter)
            id_counter += 1

            # Check if shops have name and website in OSM
            try:
                shop_brand = node.tags['brand']
            except:
                shop_brand = 'null'

            try:
                shop_website = node.tags['website']
            except:
                shop_website = 'null'

            # Create the marker and its pop-up for each shop
            markers += "var {idd} = L.marker([{latitude}, {longitude}]);\
                        {idd}.addTo(map).bindPopup('{brand}<br>{website}');".format(idd=idd, latitude=node.lat,\
                                                                                     longitude=node.lon,
                                                                                     brand=shop_brand,\
                                                                                     website=shop_website)

    # Render the page with the map
    return render_template('map.html', markers=markers, lat=lat, lon=lon)
