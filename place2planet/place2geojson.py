import json
import requests
import shapely
import shapely.geometry as geom
from shapely.geometry import Point, box, Polygon, MultiPoint

def search(place,local):
    if (',') in place:
        place.split(',')
        real=''.join(place)
        r=requests.get('https://nominatim.openstreetmap.org/search?q='+real+'&format=jsonv2')
        response=r.json()
        for things in response:
            try:
                if len(response)>1 and things['importance']>=0.7:
                    lat=things['lat']
                    lon=things['lon']
                    center=Point(float(lon),float(lat)).buffer(0.11)
                    poly=center.simplify(4)
                    features = json.dumps(shapely.geometry.mapping(poly))
                    with open(local, 'w') as outfile:
                      outfile.write(features)
                    print('GeoJSON Exported to: '+str(local))
                else:
                    lat=things['lat']
                    lon=things['lon']
                    center=Point(float(lon),float(lat)).buffer(0.11)
                    poly=center.simplify(4)
                    features = json.dumps(shapely.geometry.mapping(poly))
                    with open(local, 'w') as outfile:
                      outfile.write(features)
                    print('GeoJSON Exported to: '+str(local))
            except Exception as e:
                print(e)
    else:
        r=requests.get('https://nominatim.openstreetmap.org/search?q='+place+'&format=jsonv2')
        response=r.json()
        for things in response:
            if len(response)>1 and things['importance']>=0.7:
                lat=things['lat']
                lon=things['lon']
                center=Point(float(lon),float(lat)).buffer(0.11)
                poly=center.simplify(4)
                features = json.dumps(shapely.geometry.mapping(poly))
                with open(local, 'w') as outfile:
                  outfile.write(features)
                print('GeoJSON Exported to: '+str(local))
            elif things['importance']>=0.7:
                lat=things['lat']
                lon=things['lon']
                center=Point(float(lon),float(lat)).buffer(0.11)
                poly=center.simplify(4)
                features = json.dumps(shapely.geometry.mapping(poly))
                with open(local, 'w') as outfile:
                  outfile.write(features)
                print('GeoJSON Exported to: '+str(local))
#search(place="Bangalore,India",local=r"C:\planet_demo\bangalore.geojson")
