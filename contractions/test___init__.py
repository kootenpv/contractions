import pytest
import contractions


def test_fix():
    assert contractions.fix("you're happy now") == "you are happy now"


def test_add():
    contractions.add('mychange', 'my change')
    assert contractions.fix('mychange') == 'my change'


def test_ill():
    txt = 'He is to step down at the end of the week due to ill health'
    assert contractions.fix(txt) == txt
    assert contractions.fix("I'll") == "I will"
