from __future__ import division
import urllib, json, requests

TZ_API_KEY = 'QWLU5Z73POKS'

def get_tz_for_city(city,state):
	gmap_api_url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % urllib.quote(city + ", " + state)
	resp = requests.get(gmap_api_url)
	try:
		json_resp = json.loads(resp.text)
		if 'results' in json_resp and len(json_resp['results']) > 0:
			lat = json_resp['results'][0]['geometry']['location']['lat']
			lng = json_resp['results'][0]['geometry']['location']['lng']
			tz_api_url = "http://api.timezonedb.com/?lat=%s&lng=%s&key=%s&format=json" % (lat,lng,TZ_API_KEY)
			resp = requests.get(tz_api_url)
			json_resp = json.loads(resp.text)
			print json_resp
			print json_resp['gmtOffset']
			return int(json_resp['gmtOffset'])/(60*60)

	except KeyError:
		print "Key Error in get_tz_for_city"
		return None

if __name__ == "__main__":
	print get_tz_for_city('San Jose','CA')