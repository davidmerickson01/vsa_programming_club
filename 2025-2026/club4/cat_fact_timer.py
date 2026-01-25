import time
import requests

API_URL = "https://meowfacts.herokuapp.com/"

def get_cat_fact():
    try:
        resp = requests.get(API_URL, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        # According to the API, JSON has a "data" list with strings
        fact = data.get("data", [])[0] if data.get("data") else None
        return fact
    except Exception as e:
        print("Error fetching cat fact:", e)
        return None

def main():
    while True:
        fact = get_cat_fact()
        if fact:
            print("🐱 Cat fact:", fact)
        else:
            print("No fact available this time.")
        time.sleep(5)

if __name__ == "__main__":
    main()
