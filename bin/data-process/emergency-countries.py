import sys, csv, os, traceback
import simplejson as json
from itertools import groupby

# -----------------------
# Process Emergency Country Polygons
# -----------------------
try: 
	os.chdir("../")
	data_file = csv.DictReader(open('data/update-data/unhcr-emergency-country.csv', 'rU'), delimiter= ',', quotechar = '"')
	data_sort = sorted(data_file, key=lambda x: x['isocode'])

	geo_file = open('data/process-data/world-full.geojson', "rb").read()
	geo = json.loads(geo_file)

	geodata = {"type": "FeatureCollection","features": []}
	rowid = 0
	for g in geo['features']:
	    for d in data_sort:
	        if d['isocode'] == g['properties']['ISO_A3']:
	        	rowid = rowid + 1
		    	data = {
		    		"type": "Feature", 
		    		"id": rowid, 
		    		"properties": {
		    			'isocode': d['isocode'],
		        		'host': d['host'],
		#        		'emergency': d['emergency'],
		#        		'refugee_pop': int(d['refugee_pop']) if d['refugee_pop'] != "" else 0,
		#        		'refugee_pop_str': "{:,}".format(int(d['refugee_pop'])) if d['refugee_pop'] != "" else "",
		#        		'refugee_pop_short': "{:,}".format(int(float(d['refugee_pop'])/1000)) if d['refugee_pop'] != "" else "",
		#       			'comment': d['comment'],
		#        		'date': d['date'],
		#        		'pct_male': int(float(d['pct_male'].rstrip("%"))) if d['pct_male'] != "" else "",
		#        		'pct_female': int(float(d['pct_female'].rstrip("%"))) if d['pct_female'] != "" else "",
		#        		'pct_under18': int(float(d['pct_under18'].rstrip("%"))) if d['pct_under18'] != "" else ""
		    		}, 
		    		"geometry": g['geometry']
		    		}
		        geodata['features'].append(data)

	data_writeout = json.dumps(geodata, sort_keys=True)
	f_out = open('data/geo/emergency-countries.geojson', 'wb')
	f_out.writelines(data_writeout)
	f_out.close()
except StandardError, err:
    print "Unexpected error"
    traceback.print_exc(file=sys.stdout)
