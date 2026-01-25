import requests

COLORMIND_LIST_URL = "http://colormind.io/list/"
COLORMIND_API_URL = "http://colormind.io/api/"

def get_available_models():
    response = requests.get(COLORMIND_LIST_URL)
    response.raise_for_status()
    return response.json()["result"]

def get_palette(model="default"):
    payload = {
        "model": model
    }
    response = requests.post(COLORMIND_API_URL, json=payload)
    response.raise_for_status()
    return response.json()["result"]

def rgb_to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(*rgb)

def main():
    print("Fetching available Colormind models...")
    models = get_available_models()
    print("Available models:")
    for m in models:
        print(" -", m)

    print("\nGenerating a color palette...\n")
    palette = get_palette(model=models[0])

    for i, color in enumerate(palette, 1):
        print(f"Color {i}: RGB={color}, HEX={rgb_to_hex(color)}")

if __name__ == "__main__":
    main()
