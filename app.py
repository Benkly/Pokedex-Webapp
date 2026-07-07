import streamlit as st
import requests
import random

# --- Page Config ---
st.set_page_config(
    page_title="Pokedex",
    page_icon="◓",
    layout="centered"
)

BASE_URL = "https://pokeapi.co/api/v2"

# --- Helper Functions ---
def get_pokemon(identifier):
    """Fetch Pokemon data by name or ID. Returns (data, error)."""
    url = f"{BASE_URL}/pokemon/{str(identifier).lower().strip()}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json(), None
        elif response.status_code == 404:
            return None, f"No Pokemon found for '{identifier}'. Check the name or ID and try again."
        else:
            return None, f"API error: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return None, "Could not connect to PokeAPI. Check your internet connection."
    except requests.exceptions.Timeout:
        return None, "Request timed out. Try again."

def get_species(pokemon_id):
    """Fetch species data for flavour text and other details."""
    url = f"{BASE_URL}/pokemon-species/{pokemon_id}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None

def get_flavour_text(species_data):
    """Extract the first English Pokedex entry."""
    if not species_data:
        return ""
    for entry in species_data.get("flavor_text_entries", []):
        if entry["language"]["name"] == "en":
            # Clean up newlines and form-feed characters
            return entry["flavor_text"].replace("\n", " ").replace("\f", " ")
    return ""

# Map PokeAPI generation keys to display name and origin region
GENERATION_INFO = {
    "generation-i":    {"label": "I",    "region": "Kanto"},
    "generation-ii":   {"label": "II",   "region": "Johto"},
    "generation-iii":  {"label": "III",  "region": "Hoenn"},
    "generation-iv":   {"label": "IV",   "region": "Sinnoh"},
    "generation-v":    {"label": "V",    "region": "Unova"},
    "generation-vi":   {"label": "VI",   "region": "Kalos"},
    "generation-vii":  {"label": "VII",  "region": "Alola"},
    "generation-viii": {"label": "VIII", "region": "Galar"},
    "generation-ix":   {"label": "IX",   "region": "Paldea"},
}

def get_generation_info(species_data):
    """Return (label, region) tuple for the Pokemon's generation, or (None, None)."""
    if not species_data:
        return None, None
    gen_key = species_data.get("generation", {}).get("name")
    info = GENERATION_INFO.get(gen_key)
    if info:
        return info["label"], info["region"]
    return None, None

def type_color(type_name):
    """Return a hex color for a given Pokemon type."""
    colors = {
        "fire": "#F08030", "water": "#6890F0", "grass": "#78C850",
        "electric": "#F8D030", "psychic": "#F85888", "ice": "#98D8D8",
        "dragon": "#7038F8", "dark": "#705848", "fairy": "#EE99AC",
        "normal": "#A8A878", "fighting": "#C03028", "flying": "#A890F0",
        "poison": "#A040A0", "ground": "#E0C068", "rock": "#B8A038",
        "bug": "#A8B820", "ghost": "#705898", "steel": "#B8B8D0",
    }
    return colors.get(type_name, "#68A090")

def stat_bar(stat_name, value, max_val=255):
    """Render a labelled stat bar using st.progress."""
    col1, col2, col3 = st.columns([2, 1, 5])
    col1.caption(stat_name.upper())
    col2.caption(str(value))
    col3.progress(value / max_val)

def display_pokemon(data, species_data=None):
    """Render a full Pokemon card."""
    name = data["name"].capitalize()
    poke_id = data["id"]
    types = [t["type"]["name"] for t in data["types"]]
    sprite_url = (
        (data["sprites"].get("other") or {})
        .get("official-artwork", {})
        .get("front_default")
        or data["sprites"].get("front_default")
    )

    # Header row
    col_img, col_info = st.columns([1, 2])

    with col_img:
        if sprite_url:
            st.image(sprite_url, width=200)
        else:
            st.write("No image available")

    with col_info:
        st.markdown(f"### #{poke_id:03d} — {name}")

        # Type badges
        type_badges = "  ".join(
            f'<span style="background-color:{type_color(t)};padding:3px 10px;border-radius:12px;color:white;font-weight:bold;font-size:0.85em">{t.capitalize()}</span>'
            for t in types
        )
        st.markdown(type_badges, unsafe_allow_html=True)
        st.write("")

        # Generation & region
        gen_label, region = get_generation_info(species_data)
        if gen_label:
            st.markdown(
                f"**Generation:** {gen_label} &nbsp;&nbsp; **Region:** {region}",
                unsafe_allow_html=True
            )

        # Flavour text
        if species_data:
            flavour = get_flavour_text(species_data)
            if flavour:
                st.markdown(f"*{flavour}*")

        # Physical stats
        height_m = data["height"] / 10
        weight_kg = data["weight"] / 10
        st.markdown(f"**Height:** {height_m} m &nbsp;&nbsp; **Weight:** {weight_kg} kg", unsafe_allow_html=True)

    # Base Stats
    st.markdown("#### Base Stats")
    stat_labels = {
        "hp": "HP", "attack": "Attack", "defense": "Defense",
        "special-attack": "Sp. Atk", "special-defense": "Sp. Def", "speed": "Speed"
    }
    for stat in data["stats"]:
        label = stat_labels.get(stat["stat"]["name"], stat["stat"]["name"])
        stat_bar(label, stat["base_stat"])

    # Abilities
    st.markdown("#### Abilities")
    for ability in data["abilities"]:
        ability_name = ability["ability"]["name"].replace("-", " ").title()
        hidden_tag = " *(Hidden)*" if ability["is_hidden"] else ""
        st.markdown(f"- {ability_name}{hidden_tag}")

    # Moves (first 10)
    with st.expander("Moves (first 10)"):
        moves = [m["move"]["name"].replace("-", " ").title() for m in data["moves"][:10]]
        st.write(", ".join(moves))


# --- Main App ---
st.title("◓ Pokédex")
st.markdown("Search for any Pokémon by name or National Pokédex number.")

search = st.text_input("Enter a Pokémon name or ID", placeholder="e.g., Pikachu or 25")

# Random Pokemon button
if st.button("Random Pokémon"):
    search = str(random.randint(1, 1025))

if search:
    with st.spinner("Fetching data..."):
        data, error = get_pokemon(search)

    if error:
        st.error(error)
    else:
        species_data = get_species(data["id"])
        display_pokemon(data, species_data)
else:
    st.info("👆 Type a Pokémon name or number above to get started. Use the sidebar to explore more features.")

# Sidebar navigation hint
with st.sidebar:
    st.markdown("## See More")
    st.page_link("pages/quiz.py", label="🧠 Test Yourself — Try the Pokémon Quiz")