
import sys
import pytest

from word_counter import count_word
from wordstat import main


# Test 1: Basic word frequency
def test_basic_word_count():
    text = "apple banana apple apple banana"

    result = count_word(text, 2)

    assert result == [
        ("apple", 3),
        ("banana", 2)
    ]


# Test 2: Return only the top N words
def test_top_n():
    text = "python python python java java sql"

    result = count_word(text, 1)

    assert result == [("python", 3)]


# Test 3: Case-insensitive counting
def test_case_insensitive():
    text = "Python PYTHON python"

    result = count_word(text, 1)

    assert result == [("python", 3)]


# Test 4: Punctuation handling
def test_punctuation():
    text = "Hello, hello! world?"

    result = count_word(text, 2)

    assert result == [
        ("hello", 2),
        ("world", 1)
    ]


# Test 5: Empty file
def test_empty_file(tmp_path, monkeypatch, capsys):
    file = tmp_path / "empty.txt"
    file.write_text("", encoding="utf-8")

    monkeypatch.setattr(
        sys, "argv",
        ["wordstat", "-r", str(file), "-t", "3"]
    )

    main()

    output = capsys.readouterr().out

    assert output.strip() == ""


# Test 6: Unicode text
def test_unicode(tmp_path, monkeypatch, capsys):
    file = tmp_path / "unicode.txt"
    file.write_text("café CAFÉ naïve", encoding="utf-8")

    monkeypatch.setattr(
        sys, "argv",
        ["wordstat", "-r", str(file), "-t", "2"]
    )

    main()

    output = capsys.readouterr().out

    assert "café" in output
    assert "2" in output
    assert "naïve" in output


# Test 7: Very long line
def test_very_long_line(tmp_path, monkeypatch, capsys):
    file = tmp_path / "long.txt"
    file.write_text(
        "python " * 10000 + "java",
        encoding="utf-8"
    )

    monkeypatch.setattr(
        sys, "argv",
        ["wordstat", "-r", str(file), "-t", "1"]
    )

    main()

    output = capsys.readouterr().out

    assert "python" in output
    assert "10000" in output


# Test 8: Missing file
def test_missing_file(tmp_path, monkeypatch, capsys):
    missing_file = tmp_path / "missing.txt"

    monkeypatch.setattr(
        sys, "argv",
        ["wordstat", "-r", str(missing_file), "-t", "3"]
    )

    with pytest.raises(SystemExit) as error:
        main()

    captured = capsys.readouterr()

    assert error.value.code == 2
    assert "File not found" in captured.err
