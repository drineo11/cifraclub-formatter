import pytest
from lib.cifra_logic import (
    is_chord_line,
    is_header_line,
    transpose_note,
    transpose_chord,
    sanitize_text_for_pdf,
    deduplicate_sections,
)


class TestIsChordLine:
    def test_bold_line_is_chord(self):
        line = [{"text": "C G Am F", "bold": True}]
        assert is_chord_line(line) is True

    def test_chord_chars_only(self):
        line = [{"text": "C G Am7 Dm/F", "bold": False}]
        assert is_chord_line(line) is True

    def test_lyrics_not_chord(self):
        line = [{"text": "Esta é a letra da música", "bold": False}]
        assert is_chord_line(line) is False

    def test_empty_line(self):
        line = [{"text": "", "bold": False}]
        assert is_chord_line(line) is False

    def test_mixed_content(self):
        line = [{"text": "Olá C mundo G", "bold": False}]
        assert is_chord_line(line) is False


class TestIsHeaderLine:
    def test_header_with_brackets(self):
        line = [{"text": "[Intro]", "bold": False}]
        assert is_header_line(line) is True

    def test_header_with_spaces(self):
        line = [{"text": "  [Verso]  ", "bold": False}]
        assert is_header_line(line) is True

    def test_not_header_without_brackets(self):
        line = [{"text": "C G Am F", "bold": False}]
        assert is_header_line(line) is False

    def test_empty_line(self):
        line = [{"text": "", "bold": False}]
        assert is_header_line(line) is False


class TestTransposeNote:
    def test_transpose_c_to_d(self):
        assert transpose_note("C", 2) == "D"

    def test_transpose_c_to_f(self):
        assert transpose_note("C", 5) == "F"

    def test_transpose_a_sharp_to_b(self):
        assert transpose_note("A#", 1) == "B"

    def test_transpose_with_flats(self):
        assert transpose_note("A", 1, use_flats=True) == "Bb"

    def test_transpose_octave(self):
        assert transpose_note("C", 12) == "C"


class TestTransposeChord:
    def test_simple_chord(self):
        assert transpose_chord("C", 2) == "D"

    def test_chord_with_minor(self):
        assert transpose_chord("Am", 2) == "Bm"

    def test_chord_with_seventh(self):
        assert transpose_chord("G7", -2) == "F7"

    def test_chord_with_sharp(self):
        assert transpose_chord("F#", 1) == "G"

    def test_chord_with_bass(self):
        assert transpose_chord("C/G", 2) == "D/A"

    def test_chord_with_flat(self):
        assert transpose_chord("Bb", 1) == "B"


class TestSanitizeTextForPdf:
    def test_en_dash_converted(self):
        assert sanitize_text_for_pdf("\u2013") == "-"

    def test_em_dash_converted(self):
        assert sanitize_text_for_pdf("\u2014") == "-"

    def test_single_quotes_converted(self):
        assert sanitize_text_for_pdf("\u2018") == "'"

    def test_non_breaking_space_converted(self):
        assert sanitize_text_for_pdf("\u00a0") == " "

    def test_unicode_chars_preserved(self):
        assert sanitize_text_for_pdf("C G Am F") == "C G Am F"


class TestDeduplicateSections:
    def test_no_duplicates(self):
        lines = [
            [{"text": "[Intro]", "bold": False}],
            [{"text": "C G", "bold": True}],
            [{"text": " letra ", "bold": False}],
            [{"text": "[Verso]", "bold": False}],
            [{"text": "D A", "bold": True}],
            [{"text": " letra2 ", "bold": False}],
        ]
        result = deduplicate_sections(lines)
        assert len(result) == 6

    def test_duplicate_section_marked_with_2x(self):
        lines = [
            [{"text": "[Refrão]", "bold": False}],
            [{"text": "C G", "bold": True}],
            [{"text": " letra ", "bold": False}],
            [{"text": "[Refrão]", "bold": False}],
            [{"text": "C G", "bold": True}],
            [{"text": " letra ", "bold": False}],
        ]
        result = deduplicate_sections(lines)
        assert result[0] == [{"text": "[Refrão]", "bold": False}]
        assert result[3] == [{"text": "[Refrão] 2x", "bold": False, "italic": True}]
        assert result[4] == [{"text": "C G", "bold": True}]
        assert result[5] == [{"text": " letra ", "bold": False}]

    def test_three_repetitions(self):
        lines = [
            [{"text": "[Refrão]", "bold": False}],
            [{"text": "C G", "bold": True}],
            [{"text": " letra ", "bold": False}],
            [{"text": "[Refrão]", "bold": False}],
            [{"text": "C G", "bold": True}],
            [{"text": " letra ", "bold": False}],
            [{"text": "[Refrão]", "bold": False}],
            [{"text": "C G", "bold": True}],
            [{"text": " letra ", "bold": False}],
        ]
        result = deduplicate_sections(lines)
        assert result[0] == [{"text": "[Refrão]", "bold": False}]
        assert result[3] == [{"text": "[Refrão] 2x", "bold": False, "italic": True}]
        assert result[6] == [{"text": "[Refrão] 3x", "bold": False, "italic": True}]

    def test_different_body_not_marked_duplicate(self):
        lines = [
            [{"text": "[Verso]", "bold": False}],
            [{"text": "C G", "bold": True}],
            [{"text": " letra1 ", "bold": False}],
            [{"text": "[Verso]", "bold": False}],
            [{"text": "D A", "bold": True}],
            [{"text": " letra2 ", "bold": False}],
        ]
        result = deduplicate_sections(lines)
        assert len(result) == 6
        assert result[0] == [{"text": "[Verso]", "bold": False}]
        assert result[3] == [{"text": "[Verso]", "bold": False}]
        assert "italic" not in result[3][0]

    def test_no_header_always_kept(self):
        lines = [
            [{"text": "C G", "bold": True}],
            [{"text": " letra ", "bold": False}],
            [{"text": "C G", "bold": True}],
            [{"text": " letra ", "bold": False}],
        ]
        result = deduplicate_sections(lines)
        assert len(result) == 4
