"""
components.py — UI components untuk flipcard app.
"""

import streamlit as st
import streamlit.components.v1 as components


def render_flipcard(card_data: dict, is_flipped: bool, is_opened: bool, is_ragu: bool = False):
    """
    Render flipcard dengan CSS 3D flip animation menggunakan iframe component.

    Args:
        card_data: Dict berisi word, pronunciation, explanation, example, indo.
        is_flipped: Apakah kartu sedang dalam keadaan terbalik.
        is_opened: Apakah kartu sudah pernah dibuka.
        is_ragu: Apakah kartu ditandai ragu-ragu.
    """
    flipped_class = "flipped" if is_flipped else ""
    opened_badge = '<div class="opened-badge">✅ Sudah dibuka</div>' if is_opened else ''
    ragu_badge = '<div class="ragu-badge">🤔 Ragu-ragu</div>' if is_ragu else ''

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: transparent;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            font-family: 'Inter', sans-serif;
        }}

        .flip-container {{
            perspective: 1200px;
            width: 100%;
            max-width: 520px;
            height: 300px;
            cursor: pointer;
        }}

        .flip-card {{
            width: 100%;
            height: 100%;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .flip-card.flipped {{
            transform: rotateY(180deg);
        }}

        .flip-card-front, .flip-card-back {{
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            -webkit-backface-visibility: hidden;
            border-radius: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 2rem 2.5rem;
            box-sizing: border-box;
        }}

        .flip-card-front {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        }}

        .word {{
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-align: center;
            letter-spacing: -0.02em;
        }}

        .pronunciation {{
            font-size: 1.15rem;
            font-weight: 300;
            opacity: 0.85;
            font-style: italic;
        }}

        .tap-hint {{
            position: absolute;
            bottom: 1.2rem;
            font-size: 0.75rem;
            opacity: 0.5;
            font-weight: 400;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }}

        .opened-badge {{
            position: absolute;
            top: 1rem;
            right: 1.2rem;
            background: rgba(0, 230, 118, 0.25);
            border: 1px solid rgba(0, 230, 118, 0.5);
            color: #b9f6ca;
            font-size: 0.7rem;
            font-weight: 600;
            padding: 0.25rem 0.7rem;
            border-radius: 20px;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }}

        .ragu-badge {{
            position: absolute;
            top: 1rem;
            left: 1.2rem;
            background: rgba(255, 152, 0, 0.3);
            border: 1px solid rgba(255, 152, 0, 0.6);
            color: #ffe0b2;
            font-size: 0.7rem;
            font-weight: 600;
            padding: 0.25rem 0.7rem;
            border-radius: 20px;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }}

        .flip-card-back {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            transform: rotateY(180deg);
            box-shadow: 0 20px 60px rgba(245, 87, 108, 0.3);
            align-items: flex-start;
            justify-content: center;
            gap: 0.6rem;
        }}

        .back-label {{
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            opacity: 0.7;
        }}

        .back-value {{
            font-size: 0.95rem;
            font-weight: 400;
            line-height: 1.5;
            margin-bottom: 0.5rem;
        }}

        .back-value.indo {{
            font-weight: 600;
            font-size: 1.1rem;
        }}
    </style>
    </head>
    <body>
        <div class="flip-container">
            <div class="flip-card {flipped_class}">
                <div class="flip-card-front">
                    {opened_badge}
                    {ragu_badge}
                    <div class="word">{card_data['word']}</div>
                    <div class="pronunciation">{card_data['pronunciation']}</div>
                    <div class="tap-hint">Klik "Flip" untuk membalik</div>
                </div>
                <div class="flip-card-back">
                    <div class="back-label">Explanation</div>
                    <div class="back-value">{card_data['explanation']}</div>
                    <div class="back-label">Example</div>
                    <div class="back-value">{card_data['example']}</div>
                    <div class="back-label">Bahasa Indonesia</div>
                    <div class="back-value indo">{card_data['indo']}</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    components.html(html, height=340)


def render_progress(total: int, current_index: int, opened_set: set, ragu_set: set = None):
    """
    Render progress dots menunjukkan card mana yang sudah dibuka.

    Args:
        total: Jumlah total kartu.
        current_index: Index kartu saat ini.
        opened_set: Set berisi index kartu yang sudah dibuka.
        ragu_set: Set berisi index kartu yang ditandai ragu-ragu.
    """
    if ragu_set is None:
        ragu_set = set()
    dots = []
    for i in range(total):
        if i == current_index:
            style = "background:#ffea00;border:2px solid #ffea00;box-shadow:0 0 12px rgba(255,234,0,0.5);transform:scale(1.3);"
        elif i in ragu_set:
            style = "background:#ff9800;border:2px solid #ff9800;box-shadow:0 0 8px rgba(255,152,0,0.4);"
        elif i in opened_set:
            style = "background:#00e676;border:2px solid #00e676;box-shadow:0 0 8px rgba(0,230,118,0.4);"
        else:
            style = "background:#e0e0e0;border:2px solid #bdbdbd;"
        dots.append(f'<div style="width:12px;height:12px;border-radius:50%;display:inline-block;margin:0 4px;transition:all 0.3s ease;{style}"></div>')

    opened_count = len(opened_set)
    ragu_count = len(ragu_set)

    html = f"""<div style="text-align:center;font-family:Inter,sans-serif;margin-bottom:0.5rem;">
        <div style="font-size:0.9rem;color:#555;margin-bottom:0.5rem;"><strong style="color:#222;">{opened_count}</strong> / {total} kartu sudah dibuka | <strong style="color:#ff9800;">{ragu_count}</strong> ragu-ragu</div>
        <div style="display:flex;flex-wrap:wrap;gap:4px;justify-content:center;">{''.join(dots)}</div>
    </div>"""

    if opened_count == total:
        html += '<div style="max-width:520px;margin:0.5rem auto;padding:0.8rem 1.2rem;background:rgba(0,230,118,0.1);border:1px solid rgba(0,230,118,0.3);border-radius:10px;text-align:center;font-family:Inter,sans-serif;color:#00c853;font-size:0.9rem;font-weight:500;">🎉 Semua kartu sudah dibuka! Selamat!</div>'

    st.markdown(html, unsafe_allow_html=True)


def render_hint(explanation: str, show: bool):
    """
    Render hint box yang menampilkan explanation.

    Args:
        explanation: Teks explanation dari card.
        show: Apakah hint sedang ditampilkan.
    """
    if show:
        st.markdown(
            f"""<div style="max-width:520px;margin:0.5rem auto;background:linear-gradient(135deg,#1e1e2e,#2d2b55);border:1px solid rgba(102,126,234,0.4);border-radius:12px;padding:1rem 1.5rem;font-family:Inter,sans-serif;color:#f0f0f5;font-size:0.95rem;line-height:1.6;box-shadow:0 8px 24px rgba(0,0,0,0.2);">
                <div style="font-size:0.7rem;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;opacity:0.6;margin-bottom:0.3rem;">💡 Hint</div>
                {explanation}
            </div>""",
            unsafe_allow_html=True,
        )
