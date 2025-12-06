import requests
import json

# URL of the NHL's public JSON standings API
url = "https://api-web.nhle.com/v1/standings/now"

# Fetch the JSON data
response = requests.get(url)
response.raise_for_status()  # stop if there was an HTTP error
data = response.json()

print(json.dumps(data, indent=4))

# Separate teams by conference
eastern = []
western = []

for team in data["standings"]:
    if team["conferenceName"] == "Eastern":
        eastern.append(team)
    elif team["conferenceName"] == "Western":
        western.append(team)

# Sort each list by points (descending)
eastern.sort(key=lambda x: x["points"], reverse=True)
western.sort(key=lambda x: x["points"], reverse=True)

# Get the leaders
east_leader = eastern[0]
west_leader = western[0]

# Print results
print("Eastern Conference Leader:")
print(f"{east_leader['teamName']['default']} - {east_leader['points']} points")

print("\nWestern Conference Leader:")
print(f"{west_leader['teamName']['default']} - {west_leader['points']} points")
