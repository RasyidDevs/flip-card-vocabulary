"""
app.py — Main entry point untuk Flipcard Vocabulary App.
"""

import random
import streamlit as st
from parser import parse_vocabulary_text
from components import render_flipcard, render_progress, render_hint


# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Flipcard Vocabulary",
    page_icon="🃏",
    layout="centered",
)

# ── Sample text for placeholder ──────────────────────────────────────────────
SAMPLE_TEXT = """I) 50 WORDS
1). English: Aberration --- /ˌæbəˈreɪʃn/
Explanation: A departure from what is normal, usual, or expected, typically one that is unwelcome.
Example: The sudden drop in temperature was a climatic aberration.
Indo: Kelainan/Penyimpangan
2). English: Acquiesce --- /ˌækwiˈes/
Explanation: To accept something reluctantly but without protest.
Example: He decided to acquiesce to his manager's demands.
Indo: Menyetujui (dengan terpaksa)"""


# ── Session State Initialization ─────────────────────────────────────────────
def init_state():
    """Initialize session state defaults."""
    defaults = {
        "game_started": False,
        "cards": [],
        "order": [],
        "current_pos": 0,
        "flipped": False,
        "opened": set(),
        "show_hint": False,
        "input_text": "",
        "order_mode": "Urut",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()


# ── Callbacks ────────────────────────────────────────────────────────────────
def start_game():
    """Parse text, build card order, and start game."""
    text = st.session_state.get("input_text_area", "")
    cards = parse_vocabulary_text(text)
    if not cards:
        st.session_state["parse_error"] = True
        return

    st.session_state["parse_error"] = False
    st.session_state["cards"] = cards
    order = list(range(len(cards)))
    if st.session_state["order_mode"] == "Random":
        random.shuffle(order)
    st.session_state["order"] = order
    st.session_state["current_pos"] = 0
    st.session_state["flipped"] = False
    st.session_state["opened"] = set()
    st.session_state["show_hint"] = False
    st.session_state["game_started"] = True


def flip_card():
    """Toggle flip state and mark card as opened."""
    st.session_state["flipped"] = not st.session_state["flipped"]
    if st.session_state["flipped"]:
        idx = st.session_state["order"][st.session_state["current_pos"]]
        st.session_state["opened"].add(idx)


def go_prev():
    """Navigate to previous card."""
    if st.session_state["current_pos"] > 0:
        st.session_state["current_pos"] -= 1
        st.session_state["flipped"] = False
        st.session_state["show_hint"] = False


def go_next():
    """Navigate to next card."""
    if st.session_state["current_pos"] < len(st.session_state["order"]) - 1:
        st.session_state["current_pos"] += 1
        st.session_state["flipped"] = False
        st.session_state["show_hint"] = False


def toggle_hint():
    """Toggle hint visibility."""
    st.session_state["show_hint"] = not st.session_state["show_hint"]


def back_to_setup():
    """Go back to setup page."""
    st.session_state["game_started"] = False
    st.session_state["flipped"] = False
    st.session_state["show_hint"] = False


def reset_game():
    """Reset progress but keep the same card order."""
    st.session_state["current_pos"] = 0
    st.session_state["flipped"] = False
    st.session_state["opened"] = set()
    st.session_state["show_hint"] = False


# ── Pages ────────────────────────────────────────────────────────────────────
def render_setup_page():
    """Render the setup / input page."""
    st.markdown("# 🃏 Flipcard Vocabulary")
    st.markdown(
        "Masukkan teks vocabulary terstruktur, pilih urutan, dan mulai belajar!"
    )

    st.text_area(
        "📝 Teks Vocabulary",
        height=300,
        placeholder=SAMPLE_TEXT,
        key="input_text_area",
    )

    col1, col2 = st.columns([1, 2])
    with col1:
        st.radio(
            "📋 Urutan Kartu",
            options=["Urut", "Random"],
            key="order_mode",
            horizontal=True,
        )
    with col2:
        st.markdown("")  # spacer

    st.button("🚀 Mulai Belajar", on_click=start_game, use_container_width=True, type="primary")

    if st.session_state.get("parse_error"):
        st.error("⚠️ Tidak ditemukan vocabulary dalam teks. Pastikan format sesuai.")


def render_game_page():
    """Render the flipcard game page."""
    cards = st.session_state["cards"]
    order = st.session_state["order"]
    pos = st.session_state["current_pos"]
    card_idx = order[pos]
    card = cards[card_idx]
    total = len(order)

    # Header
    st.markdown(f"### 🃏 Kartu {pos + 1} dari {total}")

    # Progress
    render_progress(total, card_idx, st.session_state["opened"])

    # Flipcard
    render_flipcard(card, st.session_state["flipped"], card_idx in st.session_state["opened"])

    # Controls row
    col_prev, col_flip, col_hint, col_next = st.columns(4)

    with col_prev:
        st.button(
            "⬅️ Prev",
            on_click=go_prev,
            disabled=(pos == 0),
            use_container_width=True,
        )

    with col_flip:
        flip_label = "🔄 Balik" if not st.session_state["flipped"] else "🔄 Depan"
        st.button(flip_label, on_click=flip_card, use_container_width=True, type="primary")

    with col_hint:
        hint_label = "💡 Hint" if not st.session_state["show_hint"] else "💡 Tutup"
        st.button(hint_label, on_click=toggle_hint, use_container_width=True)

    with col_next:
        st.button(
            "➡️ Next",
            on_click=go_next,
            disabled=(pos == total - 1),
            use_container_width=True,
        )

    # Hint area
    render_hint(card["explanation"], st.session_state["show_hint"])

    # Back & Reset buttons
    st.markdown("---")
    col_back, col_reset = st.columns(2)
    with col_back:
        st.button("🔙 Kembali ke Setup", on_click=back_to_setup, use_container_width=True)
    with col_reset:
        st.button("🔄 Reset (Urutan Sama)", on_click=reset_game, use_container_width=True)


# ── Main ─────────────────────────────────────────────────────────────────────
if st.session_state["game_started"]:
    render_game_page()
else:
    render_setup_page()
