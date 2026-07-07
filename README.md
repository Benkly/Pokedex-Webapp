# ◓ Pokédex

A Streamlit web app for looking up Pokémon and testing your type matchup knowledge, powered by [PokéAPI](https://pokeapi.co/).

## Features

### Pokédex (`app.py`)
- Search any Pokémon by name or National Pokédex number
- **Random Pokémon** button for discovery
- Official artwork sprite
- Coloured type badges
- Generation number and origin region (e.g. Generation I — Kanto)
- Pokédex flavour text entry
- Height and weight
- Base stats with visual progress bars
- Abilities (with hidden ability indicator)
- First 10 learnable moves

### Type Matchup Quiz (`pages/quiz.py`)
- Random type matchup questions — single and dual-type defenders
- 6 answer options covering all possible outcomes:
  - Immune (0×)
  - Not Very Effective (0.25×)
  - Not Very Effective (0.5×)
  - Neutral (1×)
  - Super Effective (2×)
  - Super Effective (4×)
- Per-question breakdown showing individual type multipliers for dual-type matchups
- Live scoreboard — score, accuracy %, current streak, and best streak
- Answer history (last 20 questions)
- Reset score at any time

## Project Structure

```
pokedex/
├── app.py              # Main Pokédex page
├── pages/
│   └── quiz.py         # Type Matchup Quiz page
├── pokedex-webapp/     # Python virtual environment
└── README.md
```

## Setup

### Prerequisites
- Python 3.10+

### Installation

1. Activate the virtual environment:

   ```bash
   # Windows
   pokedex-webapp\Scripts\activate
   ```

2. Install dependencies (if not already installed):

   ```bash
   pip install streamlit requests
   ```

3. Run the app:

   ```bash
   streamlit run app.py
   ```

The app will open in your browser at `http://localhost:8501`. The quiz is accessible from the sidebar under **Pages**.

## Data Source

All Pokémon data is fetched live from [PokéAPI](https://pokeapi.co/) — no local database required. An internet connection is needed to use the Pokédex search. The quiz runs entirely offline using a built-in type chart.
