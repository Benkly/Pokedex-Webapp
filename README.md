# ◓ Pokédex

A Streamlit powered web app for browsing Pokémon and testing your type matchup knowledge. 

>Powered by [PokéAPI](https://pokeapi.co/).

>**[Access the App](https://pokedex-benkly.streamlit.app)**

---

## Data Source

All Pokémon data is fetched live from [PokéAPI](https://pokeapi.co/) — no local database required. An internet connection is needed to use the Pokédex search. The quiz runs entirely offline using a built-in type chart.

## Key Features

### Pokédex (`app.py`)
- Search any Pokémon by name or National Pokédex number
- **Random Pokémon** button for discovery
- Base stats with visual progress bars
- Abilities (with hidden ability indicator)
- First 10 learnable moves

### Type Matchup Quiz (`pages/quiz.py`)
- Random type matchup questions — single and dual-type defenders
- 6 answer options covering all possible outcomes:
  - Immune (0×)
  - Not Very Effective (0.25× and 0.5×)
  - Neutral (1×)
  - Super Effective (2× and 4×)

- Feedback after a question is answered
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
