import requests
import json

'''
json API treasure trove

https://github.com/public-apis/public-apis

https://bible-api.com/?john%203:16
https://disneyapi.dev/

https://sunrise-sunset.org/api
https://api.sunrise-sunset.org/json?lat=36.7201600&lng=-4.4203400
'''

# from chatgpt
# write python to get my current latitude and longitude

def get_location():
    # Free API endpoint (does not require an API key)
    url = "https://ipinfo.io/json"
    response = requests.get(url)
    data = response.json()

    # "loc" is returned as "latitude,longitude"
    lat, lon = data['loc'].split(',')
    return float(lat), float(lon)

latitude, longitude = get_location()
print("Latitude:", latitude)
print("Longitude:", longitude)

# hardcoded lat and long
url = "https://api.sunrise-sunset.org/json?lat=36.7201600&lng=-4.4203400"

# UTC
url = "https://api.sunrise-sunset.org/json?lat="+str(latitude)+"&lng="+str(longitude)
print(url)

# pacific time
url = "https://api.sunrise-sunset.org/json?tzid=America/Los_Angeles&lat="+str(latitude)+"&lng="+str(longitude)
print(url)

response = requests.get(url, timeout=10)
data = response.json()

print("Your sunrise will be at ",data['results']['sunrise'],"today")
