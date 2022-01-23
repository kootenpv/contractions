import contractions


def test_fix():
    assert contractions.fix("you're happy now") == "you are happy now"


def test_insensitivity():
    assert contractions.fix("You're happier now") == "You are happier now"


def test_add():
    contractions.add('mychange', 'my change')
    assert contractions.fix('mychange') == 'my change'


def test_ill():
    txt = 'He is to step down at the end of the week due to ill health'
    assert contractions.fix(txt) == txt
    assert contractions.fix("I'll") == "I will"


def test_preview():
    text = "This's a simple test including two sentences. I'd use it to test preview()."
    preview_items = contractions.preview(text, flank=10)
    print(preview_items)
    assert len(preview_items) == 2
    assert preview_items[0]['match'] == "This's"
    assert preview_items[1]['match'] == "I'd"
    assert text[preview_items[0]['start']: preview_items[0]['end']] == "This's"
    assert text[preview_items[1]['start']: preview_items[1]['end']] == "I'd"
    assert "This's" in preview_items[0]["viewing_window"]
    assert "I'd" in preview_items[1]["viewing_window"]
    text2 = ""
    preview_items2 = contractions.preview(text2, flank=10)
    assert preview_items2 == []
