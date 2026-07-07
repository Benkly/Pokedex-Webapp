import streamlit as st
import random

# --- Page Config ---
st.set_page_config(
    page_title="Type Quiz | Pokédex",
    page_icon="◓",
    layout="centered"
)

# ---------------------------------------------------------------------------
# Type Effectiveness Chart
# Outer key = attacking type, inner key = defending type, value = multiplier
# 0 = immune (0x), 0.5 = not very effective, 1 = neutral, 2 = super effective
# ---------------------------------------------------------------------------
TYPE_CHART: dict[str, dict[str, float]] = {
    "normal": {
        "rock": 0.5, "ghost": 0, "steel": 0.5,
    },
    "fire": {
        "fire": 0.5, "water": 0.5, "grass": 2, "ice": 2,
        "bug": 2, "rock": 0.5, "dragon": 0.5, "steel": 2,
    },
    "water": {
        "fire": 2, "water": 0.5, "grass": 0.5, "ground": 2,
        "rock": 2, "dragon": 0.5,
    },
    "electric": {
        "water": 2, "electric": 0.5, "grass": 0.5, "ground": 0,
        "flying": 2, "dragon": 0.5,
    },
    "grass": {
        "fire": 0.5, "water": 2, "grass": 0.5, "poison": 0.5,
        "ground": 2, "flying": 0.5, "bug": 0.5, "rock": 2,
        "dragon": 0.5, "steel": 0.5,
    },
    "ice": {
        "fire": 0.5, "water": 0.5, "grass": 2, "ice": 0.5,
        "ground": 2, "flying": 2, "dragon": 2, "steel": 0.5,
    },
    "fighting": {
        "normal": 2, "ice": 2, "poison": 0.5, "flying": 0.5,
        "psychic": 0.5, "bug": 0.5, "rock": 2, "ghost": 0,
        "dark": 2, "steel": 2, "fairy": 0.5,
    },
    "poison": {
        "grass": 2, "poison": 0.5, "ground": 0.5, "rock": 0.5,
        "ghost": 0.5, "steel": 0, "fairy": 2,
    },
    "ground": {
        "fire": 2, "electric": 2, "grass": 0.5, "poison": 2,
        "flying": 0, "bug": 0.5, "rock": 2, "steel": 2,
    },
    "flying": {
        "electric": 0.5, "grass": 2, "fighting": 2, "bug": 2,
        "rock": 0.5, "steel": 0.5,
    },
    "psychic": {
        "fighting": 2, "poison": 2, "psychic": 0.5, "dark": 0,
        "steel": 0.5,
    },
    "bug": {
        "fire": 0.5, "grass": 2, "fighting": 0.5, "poison": 0.5,
        "flying": 0.5, "psychic": 2, "ghost": 0.5, "dark": 2,
        "steel": 0.5, "fairy": 0.5,
    },
    "rock": {
        "fire": 2, "ice": 2, "fighting": 0.5, "ground": 0.5,
        "flying": 2, "bug": 2, "steel": 0.5,
    },
    "ghost": {
        "normal": 0, "psychic": 2, "ghost": 2, "dark": 0.5,
    },
    "dragon": {
        "dragon": 2, "steel": 0.5, "fairy": 0,
    },
    "dark": {
        "fighting": 0.5, "psychic": 2, "ghost": 2, "dark": 0.5,
        "fairy": 0.5,
    },
    "steel": {
        "fire": 0.5, "water": 0.5, "electric": 0.5, "ice": 2,
        "rock": 2, "steel": 0.5, "fairy": 2,
    },
    "fairy": {
        "fire": 0.5, "fighting": 2, "poison": 0.5, "dragon": 2,
        "dark": 2, "steel": 0.5,
    },
}

ALL_TYPES = sorted(TYPE_CHART.keys())

# Type badge colours (shared with app.py palette)
TYPE_COLORS = {
    "fire": "#F08030", "water": "#6890F0", "grass": "#78C850",
    "electric": "#F8D030", "psychic": "#F85888", "ice": "#98D8D8",
    "dragon": "#7038F8", "dark": "#705848", "fairy": "#EE99AC",
    "normal": "#A8A878", "fighting": "#C03028", "flying": "#A890F0",
    "poison": "#A040A0", "ground": "#E0C068", "rock": "#B8A038",
    "bug": "#A8B820", "ghost": "#705898", "steel": "#B8B8D0",
}

MULTIPLIER_LABELS = {
    0.0: "Immune (0×)",
    0.25: "Not Very Effective (0.25×)",
    0.5: "Not Very Effective (0.5×)",
    1.0: "Neutral (1×)",
    2.0: "Super Effective (2×)",
    4.0: "Super Effective (4×)",
}

# Answer options shown to the user (ascending order of effectiveness)
ANSWER_OPTIONS = [
    "Immune (0×)",
    "Not Very Effective (0.25×)",
    "Not Very Effective (0.5×)",
    "Neutral (1×)",
    "Super Effective (2×)",
    "Super Effective (4×)",
]

# Map precise multiplier → answer option label
def multiplier_to_bucket(m: float) -> str:
    if m == 0:
        return "Immune (0×)"
    elif m == 0.25:
        return "Not Very Effective (0.25×)"
    elif m == 0.5:
        return "Not Very Effective (0.5×)"
    elif m == 1:
        return "Neutral (1×)"
    elif m == 2:
        return "Super Effective (2×)"
    else:  # 4×
        return "Super Effective (4×)"


def calculate_effectiveness(attack_type: str, defend_types: list[str]) -> float:
    """Multiply effectiveness across all defender types. Missing = 1x."""
    result = 1.0
    for d in defend_types:
        result *= TYPE_CHART[attack_type].get(d, 1.0)
    return result


def type_badge(type_name: str) -> str:
    color = TYPE_COLORS.get(type_name, "#68A090")
    return (
        f'<span style="background-color:{color};padding:4px 14px;'
        f'border-radius:12px;color:white;font-weight:bold;'
        f'font-size:1em;margin:2px">{type_name.capitalize()}</span>'
    )


def generate_question() -> dict:
    """Pick a random attacker and 1–2 random defender types."""
    attack_type = random.choice(ALL_TYPES)

    # 40% chance of a dual-type defender to keep things interesting
    if random.random() < 0.4:
        defend_types = random.sample(ALL_TYPES, 2)
    else:
        defend_types = [random.choice(ALL_TYPES)]

    multiplier = calculate_effectiveness(attack_type, defend_types)
    correct_bucket = multiplier_to_bucket(multiplier)

    return {
        "attack_type": attack_type,
        "defend_types": defend_types,
        "multiplier": multiplier,
        "correct_bucket": correct_bucket,
    }


# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------
def init_state():
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
    if "quiz_total" not in st.session_state:
        st.session_state.quiz_total = 0
    if "quiz_streak" not in st.session_state:
        st.session_state.quiz_streak = 0
    if "best_streak" not in st.session_state:
        st.session_state.best_streak = 0
    if "question" not in st.session_state:
        st.session_state.question = generate_question()
    if "answered" not in st.session_state:
        st.session_state.answered = False
    if "last_correct" not in st.session_state:
        st.session_state.last_correct = None
    if "history" not in st.session_state:
        st.session_state.history = []  # list of (attack, defenders, correct, chosen)


init_state()

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## Navigation")
    st.page_link("app.py", label="◓ Home — Pokédex")

# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
st.title("◓ Type Matchup Quiz")
st.markdown("How well do you know your type matchups? Pick the correct effectiveness for the attacking move.")

# Scoreboard
c1, c2, c3, c4 = st.columns(4)
c1.metric("Score", f"{st.session_state.quiz_score}/{st.session_state.quiz_total}")
accuracy = (
    round(st.session_state.quiz_score / st.session_state.quiz_total * 100)
    if st.session_state.quiz_total > 0 else 0
)
c2.metric("Accuracy", f"{accuracy}%")
c3.metric("Streak", f"🔥 {st.session_state.quiz_streak}")
c4.metric("Best Streak", f"⭐ {st.session_state.best_streak}")

st.divider()

q = st.session_state.question

# Question card
attack_badge = type_badge(q["attack_type"])
defend_badges = " + ".join(type_badge(t) for t in q["defend_types"])

st.markdown("#### The Question")
st.markdown(
    f"A &nbsp;{attack_badge}&nbsp; move hits a &nbsp;{defend_badges}&nbsp; type Pokémon.",
    unsafe_allow_html=True,
)
st.markdown("**How effective is it?**")
st.write("")

# Answer buttons — 3 columns, 2 rows (disabled once answered)
if not st.session_state.answered:
    cols = st.columns(3)
    for i, option in enumerate(ANSWER_OPTIONS):
        col = cols[i % 3]
        if col.button(option, key=f"opt_{i}", use_container_width=True):
            correct = option == q["correct_bucket"]
            st.session_state.answered = True
            st.session_state.last_correct = correct
            st.session_state.quiz_total += 1

            if correct:
                st.session_state.quiz_score += 1
                st.session_state.quiz_streak += 1
                if st.session_state.quiz_streak > st.session_state.best_streak:
                    st.session_state.best_streak = st.session_state.quiz_streak
            else:
                st.session_state.quiz_streak = 0

            st.session_state.history.append({
                "attack": q["attack_type"],
                "defenders": q["defend_types"],
                "correct_answer": q["correct_bucket"],
                "chosen_answer": option,
                "result": "✅" if correct else "❌",
            })
            st.rerun()

# Feedback after answering
if st.session_state.answered:
    multiplier = q["multiplier"]
    correct_label = MULTIPLIER_LABELS.get(multiplier, f"{multiplier}×")

    if st.session_state.last_correct:
        st.success(f"✅ Correct! {q['attack_type'].capitalize()} → {' / '.join(t.capitalize() for t in q['defend_types'])} is **{correct_label}**.")
    else:
        st.error(
            f"❌ Not quite. {q['attack_type'].capitalize()} → "
            f"{' / '.join(t.capitalize() for t in q['defend_types'])} is **{correct_label}**."
        )

    # Show breakdown for dual types
    if len(q["defend_types"]) == 2:
        t1, t2 = q["defend_types"]
        m1 = TYPE_CHART[q["attack_type"]].get(t1, 1.0)
        m2 = TYPE_CHART[q["attack_type"]].get(t2, 1.0)
        st.caption(
            f"Breakdown: {q['attack_type'].capitalize()} vs {t1.capitalize()} = {m1}× "
            f"| {q['attack_type'].capitalize()} vs {t2.capitalize()} = {m2}× "
            f"| Combined = {multiplier}×"
        )

    st.write("")
    if st.button("Next Question →", type="primary", use_container_width=True):
        st.session_state.question = generate_question()
        st.session_state.answered = False
        st.session_state.last_correct = None
        st.rerun()

st.divider()

# Reset button
if st.button("Reset Score", use_container_width=False):
    for key in ["quiz_score", "quiz_total", "quiz_streak", "best_streak", "history"]:
        del st.session_state[key]
    st.session_state.question = generate_question()
    st.session_state.answered = False
    st.session_state.last_correct = None
    st.rerun()

# Recent history expander
if st.session_state.history:
    with st.expander(f"Recent answers ({len(st.session_state.history)})"):
        for entry in reversed(st.session_state.history[-20:]):
            defenders_str = " / ".join(t.capitalize() for t in entry["defenders"])
            st.markdown(
                f"{entry['result']} **{entry['attack'].capitalize()}** → **{defenders_str}** "
                f"— you chose *{entry['chosen_answer']}*, answer was *{entry['correct_answer']}*"
            )
