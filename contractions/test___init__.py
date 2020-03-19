import pytest
import contractions

def test_fix():
    assert contractions.fix("you're happy now")=="you are happy now"

def test_add():
    contractions.add('mychange', 'my change')
    assert contractions.fix('mychange')=='my change'
