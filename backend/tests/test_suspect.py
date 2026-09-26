import pytest

from app.ai.suspect.rules import enforce_word_limit


def test_word_limit():
    text = "word " * 150
    assert len(enforce_word_limit(text).split()) <= 100
