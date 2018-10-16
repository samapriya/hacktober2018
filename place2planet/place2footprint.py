import os
import sys
import json
import requests
import shapely
import shapely.geometry as geom
from datetime import datetime, timedelta
from requests.auth import HTTPBasicAuth
from planet.api.auth import find_api_key
from shapely.geometry import Point, box, Polygon, MultiPoint
try:
    api_key = find_api_key()
    os.environ['PLANET_API_KEY'] = find_api_key()
except:
    print 'Failed to get Planet Key'
    sys.exit()

def comb_filter(geom,item,local,start,end):
  geojson_geometry = {
  "type": "GeometryFilter",
  "field_name": "geometry",
  "config": geom,
}
  date_range_filter = {
    "type": "DateRangeFilter",
    "field_name": "acquired",
    "config": {
      "gte": start+"T00:00:00.000Z",
      "lte": end+"T00:00:00.000Z"
    }
  }

  cloud_cover_filter = {
    "type": "RangeFilter",
    "field_name": "cloud_cover",
    "config": {
      "lte": 1
    }
  }
  combined_filter = {
    "type": "AndFilter",
    "config": [geojson_geometry, date_range_filter, cloud_cover_filter]
  }
  item_type = item

  search_request = {"interval": "day","item_types": [item_type],"filter": combined_filter}

  search_result =requests.post('https://api.planet.com/data/v1/quick-search',
      auth=HTTPBasicAuth(api_key, ''),
      json=search_request)
  if len(search_result.json()['features'])>0:
    print('Total assets found: '+str(len(search_result.json()['features'])))
    # for items in search_result.json()['features']:
    #   print(items['id'])
    with open(local, 'w') as outfile:
        outfile.write(json.dumps(search_result.json()))
    print('Footprints Exported as GeoJSON: '+str(local))
  else:
    print('No assets found try expanding start and end date')
  # try:
  #     with open(local) as f:
  #         contents = f.read()
  #         display(contents)
  # except Exception as e:
  #   print(e)

def fp(place,local,item,start,end):
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
                    features = shapely.geometry.mapping(poly)
                    json_string=json.dumps(features)
                    geom=json.loads(json_string)
                    comb_filter(geom=geom,item=item,local=local,start=start,end=end)
                else:
                    lat=things['lat']
                    lon=things['lon']
                    center=Point(float(lon),float(lat)).buffer(0.11)
                    poly=center.simplify(4)
                    features = shapely.geometry.mapping(poly)
                    json_string=json.dumps(features)
                    geom=json.loads(json_string)
                    comb_filter(geom=geom,item=item,local=local,start=start,end=end)
            except Exception as e:
                print('Issue Getting Geometry'+str(e))
    else:
        r=requests.get('https://nominatim.openstreetmap.org/search?q='+place+'&format=jsonv2')
        response=r.json()
        for things in response:
          try:
              if len(response)>1 and things['importance']>=0.7:
                  lat=things['lat']
                  lon=things['lon']
                  center=Point(float(lon),float(lat)).buffer(0.11)
                  poly=center.simplify(4)
                  features = json.dumps(shapely.geometry.mapping(poly))
                  json_string=json.dumps(features)
                  geom=json.loads(json_string)
                  comb_filter(geom=geom,item=item,local=local,start=start,end=end)
              elif things['importance']>=0.7:
                  lat=things['lat']
                  lon=things['lon']
                  center=Point(float(lon),float(lat)).buffer(0.11)
                  poly=center.simplify(4)
                  features = json.dumps(shapely.geometry.mapping(poly))
                  json_string=json.dumps(features)
                  geom=json.loads(json_string)
                  comb_filter(geom=geom,item=item,local=local,start=start,end=end)
          except Exception as e:
            print('Issue Getting Geometry'+str(e))

# fp(place="Raleigh,NC",
#   item='PSScene4Band',
#   local=r"C:\planet_demo\bangalore_fp.geojson",
#   start='2018-10-01',
#   end='2018-10-15')
