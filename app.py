"""
app.py — Main entry point untuk Flipcard Vocabulary App.
"""

import random
import streamlit as st
from parser import parse_vocabulary_text
from components import render_flipcard, render_progress, render_hint, render_keyboard_listener


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
        "ragu_ragu": set(),
        "review_mode": False,
        "review_order": [],
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
    st.session_state["ragu_ragu"] = set()
    st.session_state["review_mode"] = False
    st.session_state["review_order"] = []
    st.session_state["game_started"] = True


def flip_card():
    """Toggle flip state and mark card as opened."""
    st.session_state["flipped"] = not st.session_state["flipped"]
    if st.session_state["flipped"]:
        active_order = st.session_state["review_order"] if st.session_state["review_mode"] else st.session_state["order"]
        idx = active_order[st.session_state["current_pos"]]
        st.session_state["opened"].add(idx)


def go_prev():
    """Navigate to previous card."""
    if st.session_state["current_pos"] > 0:
        st.session_state["current_pos"] -= 1
        st.session_state["flipped"] = False
        st.session_state["show_hint"] = False


def go_next():
    """Navigate to next card."""
    active_order = st.session_state["review_order"] if st.session_state["review_mode"] else st.session_state["order"]
    if st.session_state["current_pos"] < len(active_order) - 1:
        st.session_state["current_pos"] += 1
        st.session_state["flipped"] = False
        st.session_state["show_hint"] = False


def toggle_hint():
    """Toggle hint visibility."""
    st.session_state["show_hint"] = not st.session_state["show_hint"]


def toggle_ragu():
    """Toggle current card's ragu-ragu status."""
    active_order = st.session_state["review_order"] if st.session_state["review_mode"] else st.session_state["order"]
    idx = active_order[st.session_state["current_pos"]]
    if idx in st.session_state["ragu_ragu"]:
        st.session_state["ragu_ragu"].discard(idx)
    else:
        st.session_state["ragu_ragu"].add(idx)


def start_review_ragu():
    """Enter review mode showing only ragu-ragu cards."""
    ragu = st.session_state["ragu_ragu"]
    if not ragu:
        return
    review_order = [i for i in st.session_state["order"] if i in ragu]
    st.session_state["review_order"] = review_order
    st.session_state["review_mode"] = True
    st.session_state["current_pos"] = 0
    st.session_state["flipped"] = False
    st.session_state["show_hint"] = False


def exit_review_ragu():
    """Exit review mode and return to normal."""
    st.session_state["review_mode"] = False
    st.session_state["current_pos"] = 0
    st.session_state["flipped"] = False
    st.session_state["show_hint"] = False


def back_to_setup():
    """Go back to setup page."""
    st.session_state["game_started"] = False
    st.session_state["flipped"] = False
    st.session_state["show_hint"] = False
    st.session_state["review_mode"] = False


def reset_game():
    """Reset progress but keep the same card order."""
    st.session_state["current_pos"] = 0
    st.session_state["flipped"] = False
    st.session_state["opened"] = set()
    st.session_state["ragu_ragu"] = set()
    st.session_state["show_hint"] = False


def reset_modulo_50():
    """Reset last N cards where N = (current_pos+1) % 50 (or 50 if multiple of 50)."""
    pos = st.session_state["current_pos"]
    active_order = st.session_state["review_order"] if st.session_state["review_mode"] else st.session_state["order"]
    total_seen = pos + 1
    n = total_seen % 50
    if n == 0:
        n = 50
    # n = jumlah kartu terakhir yang akan direset
    start = total_seen - n  # posisi awal range reset
    for i in range(start, total_seen):
        if i < len(active_order):
            card_idx = active_order[i]
            st.session_state["opened"].discard(card_idx)
            st.session_state["ragu_ragu"].discard(card_idx)
    st.session_state["current_pos"] = start
    st.session_state["flipped"] = False
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
    # Keyboard listener for arrow key navigation
    render_keyboard_listener()
    cards = st.session_state["cards"]
    is_review = st.session_state["review_mode"]
    active_order = st.session_state["review_order"] if is_review else st.session_state["order"]
    pos = st.session_state["current_pos"]

    # Safety check: clamp pos if order changed
    if pos >= len(active_order):
        pos = max(0, len(active_order) - 1)
        st.session_state["current_pos"] = pos

    if len(active_order) == 0:
        st.warning("Tidak ada kartu untuk ditampilkan.")
        if is_review:
            st.button("🔙 Kembali ke Normal", on_click=exit_review_ragu, use_container_width=True)
        return

    card_idx = active_order[pos]
    card = cards[card_idx]
    total = len(active_order)

    # Header
    if is_review:
        st.markdown(f"### 🤔 Review Ragu-ragu — Kartu {pos + 1} dari {total}")
    else:
        st.markdown(f"### 🃏 Kartu {pos + 1} dari {total}")

    # Progress
    render_progress(total, card_idx, st.session_state["opened"], st.session_state["ragu_ragu"])

    # Flipcard
    is_ragu = card_idx in st.session_state["ragu_ragu"]
    render_flipcard(card, st.session_state["flipped"], card_idx in st.session_state["opened"], is_ragu)

    # Controls row
    col_prev, col_flip, col_hint, col_ragu, col_next = st.columns(5)

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

    with col_ragu:
        if is_ragu:
            st.button("✅ Yakin", on_click=toggle_ragu, use_container_width=True)
        else:
            st.button("🤔 Ragu", on_click=toggle_ragu, use_container_width=True)

    with col_next:
        st.button(
            "➡️ Next",
            on_click=go_next,
            disabled=(pos == total - 1),
            use_container_width=True,
        )

    # Hint area
    render_hint(card["explanation"], st.session_state["show_hint"])

    # Bottom buttons
    st.markdown("---")
    if is_review:
        col_back, col_reset = st.columns(2)
        with col_back:
            st.button("🔙 Kembali ke Normal", on_click=exit_review_ragu, use_container_width=True)
        with col_reset:
            st.button("🔄 Reset Mod 50", on_click=reset_modulo_50, use_container_width=True)
    else:
        col_back, col_review, col_reset, col_mod = st.columns(4)
        with col_back:
            st.button("🔙 Setup", on_click=back_to_setup, use_container_width=True)
        with col_review:
            ragu_count = len(st.session_state["ragu_ragu"])
            st.button(
                f"📋 Review Ragu ({ragu_count})",
                on_click=start_review_ragu,
                disabled=(ragu_count == 0),
                use_container_width=True,
            )
        with col_reset:
            st.button("🔄 Reset", on_click=reset_game, use_container_width=True)
        with col_mod:
            st.button("🔄 Reset Mod 50", on_click=reset_modulo_50, use_container_width=True)


# ── Main ─────────────────────────────────────────────────────────────────────
if st.session_state["game_started"]:
    render_game_page()
else:
    render_setup_page()
