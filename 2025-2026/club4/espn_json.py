# chatgpt
# write python program that downloads nfl scores from espn using json
# google search took me to
# https://zuplo.com/learning-center/espn-hidden-api-guide

import requests
import json

def get_nfl_scores():
    # ESPN NFL scoreboard JSON endpoint
    # this didn't work
    url = "https://site.api.espn.com/apis/v2/sports/football/nfl/scoreboard"
    # but this did
    url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    # another way to see it
    # https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard

    response = requests.get(url, timeout=10)
    data = response.json()

    # see everything it downloads
    #print(data)
    
    # see everything in nice json format
    print(json.stringify(data))

    # Loop through events (games)
    for event in data.get("events", []):
        competition = event["competitions"][0]

        home = competition["competitors"][0]
        away = competition["competitors"][1]

        home_team = home["team"]["displayName"]
        away_team = away["team"]["displayName"]

        home_score = home.get("score", "0")
        away_score = away.get("score", "0")

        status = competition["status"]["type"]["description"]

        print(f"{away_team} {away_score} @ {home_team} {home_score}  —  {status}")

if __name__ == "__main__":
    get_nfl_scores()

# helpful if you run apart from IDLE
print("press ENTER to exit")
input()
