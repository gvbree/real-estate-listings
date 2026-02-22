import json
import config
from shapely.geometry import shape
     
def generate_location_metadata():
    for adm_div in ["bundesland", "gemeinde", "bezirk"]:
        output_json = f"{adm_div}_centroids.json"
        
        with open(f"{config.BASE_PATH}/data/{adm_div}_999_geo.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
    
        metadata = {}
    
        for feature in data['features']:
            geom = shape(feature['geometry'])
            min_lon, min_lat, max_lon, max_lat = geom.bounds
            
            center = geom.representative_point() 
            
            iso = feature['properties']['iso']
            metadata[iso] = {
                "lat": center.y,
                "lon": center.x,
                "min_lat": min_lat,
                "max_lat": max_lat,
                "min_lon": min_lon,
                "max_lon": max_lon
            }
    
        with open(f"{config.BASE_PATH}/data/{output_json}", 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)
    
        print(f"Success! Created {output_json} with {len(metadata)} locations.")