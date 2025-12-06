# from gemini.google.com
# write a python program that uses pokeapi

import requests

def get_pokemon_data(pokemon_name):
    """
    Fetches data for a specific Pokémon from the PokeAPI.
    
    Args:
        pokemon_name (str): The name of the Pokémon (e.g., 'pikachu').
        
    Returns:
        dict: A dictionary containing the Pokémon's data, or None if an error occurs.
    """
    
    # 1. Construct the API URL
    base_url = "https://pokeapi.co/api/v2/pokemon/"
    # The name is converted to lowercase as API URLs are usually case-sensitive
    url = f"{base_url}{pokemon_name.lower()}"
    
    print(f"Attempting to fetch data from: {url}")
    
    try:
        # 2. Make the GET request to the API
        response = requests.get(url)
        
        # 3. Check if the request was successful (status code 200)
        if response.status_code == 200:
            # 4. Parse the JSON response body into a Python dictionary
            data = response.json()
            return data
        elif response.status_code == 404:
            print(f"Error: Pokémon '{pokemon_name}' not found.")
            return None
        else:
            print(f"Error: API request failed with status code {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        # Handle network or connection errors
        print(f"An error occurred during the request: {e}")
        return None

def display_pokemon_info(data):
    """
    Prints key information extracted from the Pokémon data dictionary.
    """
    if not data:
        return
    
    print("\n--- Pokémon Data Summary ---")
    
    # Extracting basic information
    name = data.get("name").capitalize()
    pokedex_id = data.get("id")
    height = data.get("height") / 10  # Convert from decimetres to meters
    weight = data.get("weight") / 10  # Convert from hectograms to kilograms
    
    print(f"**Name:** {name}")
    print(f"**Pokedex ID:** {pokedex_id}")
    print(f"**Height:** {height:.1f} m")
    print(f"**Weight:** {weight:.1f} kg")
    
    # Extracting abilities
    abilities = [ability['ability']['name'] for ability in data.get('abilities', [])]
    print(f"**Abilities:** {', '.join(abilities).capitalize()}")
    
    # Extracting types
    types = [type_slot['type']['name'] for type_slot in data.get('types', [])]
    print(f"**Types:** {', '.join(types).capitalize()}")
    
    # Extracting base stats
    print("\n**Base Stats:**")
    for stat in data.get('stats', []):
        stat_name = stat['stat']['name'].replace('-', ' ').title()
        base_value = stat['base_stat']
        print(f"  - {stat_name}: {base_value}")
        
# --- Main Execution ---
if __name__ == "__main__":
    # Choose the Pokémon you want to look up
    pokemon_to_find = "Pikachu"
    
    pokemon_data = get_pokemon_data(pokemon_to_find)
    
    if pokemon_data:
        display_pokemon_info(pokemon_data)
