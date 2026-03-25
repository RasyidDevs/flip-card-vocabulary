"""
parser.py — Modul untuk mem-parse teks terstruktur vocabulary menjadi list of dict.
"""

import re
from typing import List, Dict


def parse_vocabulary_text(text: str) -> List[Dict[str, str]]:
    """
    Parse teks terstruktur vocabulary menjadi list of dict.

    Setiap dict mengandung:
        - word: kata bahasa Inggris
        - pronunciation: cara pengucapan
        - explanation: penjelasan arti
        - example: contoh kalimat
        - indo: terjemahan bahasa Indonesia

    Args:
        text: Teks terstruktur yang mengikuti format:
            <nomor>). English: <word> --- <pronunciation>
            Explanation: <explanation>
            Example: <example>
            Indo: <indo>

    Returns:
        List of dict berisi data vocabulary.
    """
    cards = []

    # Pattern to match each vocabulary entry block
    pattern = re.compile(
        r'\d+\)\.\s*English:\s*(.+?)\s*---\s*(.+?)\s*\n'
        r'\s*Explanation:\s*(.+?)\s*\n'
        r'\s*Example:\s*(.+?)\s*\n'
        r'\s*Indo:\s*(.+?)(?:\n|$)',
        re.MULTILINE
    )

    for match in pattern.finditer(text):
        cards.append({
            "word": match.group(1).strip(),
            "pronunciation": match.group(2).strip(),
            "explanation": match.group(3).strip(),
            "example": match.group(4).strip(),
            "indo": match.group(5).strip(),
        })

    return cards
