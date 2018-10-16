import os
import sys
import csv
import time
import ee
import json
import requests
import shapely
import shapely.geometry as geom
from requests.auth import HTTPBasicAuth
from planet.api.auth import find_api_key
from shapely.geometry import Point, box, Polygon, MultiPoint
os.chdir(os.path.dirname(os.path.realpath(__file__)))
path=os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, path)
try:
    ee.Initialize()
except Exception, e:
    print 'Authenticate Earth Engine first and rerun program'
    time.sleep(2)
    os.system('earthengine authenticate')
src=os.path.dirname(os.path.realpath(__file__))
try:
    api_key = find_api_key()
    os.environ['PLANET_API_KEY'] = find_api_key()
except:
    print 'Failed to get Planet Key'
    sys.exit()
l=[]

for items in os.listdir(src):
    if items.endswith('.csv'):
        input_file=csv.DictReader(open(os.path.join(src,items)))
        for rows in input_file:
            l.append(rows['id'])

def intersect(start,end,geometry,operator,output):
    with open(output, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['type', 'id','#items'],
                                delimiter=',')
        writer.writeheader()
    i=1
    for items in l:
        print('Processing '+str(i)+' of '+str(len(l)))
        i=i+1
        try:
            typ = ee.data.getInfo(items)['type']
            aoi_geom = ee.Geometry.Polygon(geometry)
            boundbox = aoi_geom.bounds()
        except Exception as e:
            print(e)
        if str(typ) == 'Image' and operator == 'bb':
            try:
                userCollection = \
                    ee.ImageCollection([items]).filterBounds(boundbox).filterDate(start,
                        end)
                length = userCollection.size().getInfo()
                if int(length) == 0:
                    pass
                    #print 'Geometry does not intersect collection '+str(items)
                else:
                    #print 'Total images in filtered collection: '+str(items) +' of size '+ str(length)
                    with open(output, 'a') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',',
                                lineterminator='\n')
                        writer.writerow([str(typ),str(items),str(length)])
                    csvfile.close()
            except Exception as e:
                print('Check on Collection failed becaused '+str(e))
        elif str(typ) == 'Image' and operator == None:

            try:
                userCollection =ee.ImageCollection([items]).filterBounds(aoi_geom).filterDate(start,
                        end)
                length = userCollection.size().getInfo()
                if int(length) == 0:
                    pass
                    #print 'Geometry does not intersect collection '+str(items)
                else:
                    #print 'Total images in filtered collection: '+str(items) +' of size '+ str(length)
                    with open(output, 'a') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',',
                                lineterminator='\n')
                        writer.writerow([str(typ),str(items),str(length)])
                    csvfile.close()
            except Exception as e:
                print('Check on Collection failed becaused '+str(e))
        elif typ == 'ImageCollection' and operator == 'bb':
            try:
                userCollection = \
                    ee.ImageCollection(items).filterBounds(boundbox).filterDate(start,
                        end)
                length = userCollection.size().getInfo()
                if int(length) == 0:
                    pass
                    #print 'Geometry does not intersect collection '+str(items)
                else:
                    #print 'Total images in filtered collection: '+str(items) +' of size '+ str(length)
                    with open(output, 'a') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',',
                                lineterminator='\n')
                        writer.writerow([str(typ),str(items),str(length)])
                    csvfile.close()
            except Exception as e:
                print('Check on Collection failed becaused '+str(e))
        elif typ == 'ImageCollection' and operator == None:
            try:
                userCollection = \
                    ee.ImageCollection(items).filterBounds(aoi_geom).filterDate(start,
                        end)
                length = userCollection.size().getInfo()
                if int(length) == 0:
                    pass
                    #print 'Geometry does not intersect collection '+str(items)
                else:
                    #print 'Total images in filtered collection: '+str(items) +' of size '+ str(length)
                    with open(output, 'a') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',',
                                lineterminator='\n')
                        writer.writerow([str(typ),str(items),str(length)])
                    csvfile.close()
            except Exception as e:
                print('Check on Collection failed becaused '+str(e))
    print('')
    print('Report with Intersects Exported to '+str(output))

def eefp(place,local,op,start,end):
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
                    geom=geom['coordinates']
                    intersect(geometry=geom,operator=op,output=local,start=start,end=end)
                else:
                    lat=things['lat']
                    lon=things['lon']
                    center=Point(float(lon),float(lat)).buffer(0.11)
                    poly=center.simplify(4)
                    features = shapely.geometry.mapping(poly)
                    json_string=json.dumps(features)
                    geom=json.loads(json_string)
                    geom=geom['coordinates']
                    intersect(geometry=geom,operator=op,output=local,start=start,end=end)
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
                  geom=json.loads(json_string)['coordinates']
                  intersect(geometry=geom,operator=op,output=local,start=start,end=end)
              elif things['importance']>=0.7:
                  lat=things['lat']
                  lon=things['lon']
                  center=Point(float(lon),float(lat)).buffer(0.11)
                  poly=center.simplify(4)
                  features = json.dumps(shapely.geometry.mapping(poly))
                  json_string=json.dumps(features)
                  geom=json.loads(json_string)['coordinates']
                  intersect(geometry=geom,operator=op,output=local,start=start,end=end)
          except Exception as e:
            print('Issue Getting Geometry'+str(e))

# fp(place="Raleigh,NC",
#   item='PSScene4Band',
#   local=r"C:\planet_demo\bangalore_fp.geojson",
#   start='2018-10-01',
#   end='2018-10-15')
