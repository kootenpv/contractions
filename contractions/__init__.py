import re


contractions_dict = {
    "ain't": "are not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "I'd": "I would",
    "I'd've": "I would have",
    "I'll": "I will",
    "I'll've": "I will have",
    "I'm": "I am",
    "I've": "I have",
    "isn't": "is not",
    "it'd": "it would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so is",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you would",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you shall have",
    "you're": "you are",
    "you've": "you have",
    "doin'": "doing",
    "goin'": "going",
    "nothin'": "nothing",
    "somethin'": "something",
}


contractions_re_keys = [x.replace("'", "['’]") for x in contractions_dict]
contractions_dict.update({k.replace("'", "’"): v for k, v in contractions_dict.items()})


leftovers_dict = {
    "'all": '',
    "'am": '',
    "'cause": 'because',
    "'d": " would",
    "'ll": " will",
    "'re": " are",
    "'em": " them",
}

leftovers_dict.update({k.replace("'", "’"): v for k, v in leftovers_dict.items()})

safety_keys = set(["he's", "he'll", "we'll", "we'd", "it's", "i'd", "we'd", "we're"])

unsafe_dict = {
    k.replace("'", ""): v for k, v in contractions_dict.items() if k.lower() not in safety_keys
}

slang = {
    "ima": "I am going to",
    "gonna": "going to",
    "gotta": "got to",
    "wanna": "want to",
    "woulda": "would have",
    "gimme": "give me",
    "asap": "as soon as possible",
    "u": "you",
    "r ": "are ",
}

unsafe_dict.update(slang)

leftovers_re = re.compile('|'.join(sorted(leftovers_dict.keys())), re.IGNORECASE)
contractions_re = re.compile('|'.join(sorted(contractions_re_keys)), re.IGNORECASE)
unsafe_re = re.compile(r"\b" + r"\b|\b".join(sorted(unsafe_dict)) + r"\b", re.IGNORECASE)


def _replacer(dc):
    def replace(match):
        v = match.group()
        if v in dc:
            return dc[v]
        v = v.lower()
        if v in dc:
            return dc[v]
        return v

    return replace


slang_re = re.compile(
    r"\b" + r"\b|\b".join(sorted(list(slang) + list(unsafe_dict))) + r"\b", re.IGNORECASE
)

LIM_RE = re.compile("['’]")

rc = _replacer(contractions_dict)
rl = _replacer(leftovers_dict)
ru = _replacer(unsafe_dict)


def fix(s, leftovers=True, slang=True):
    # when not expecting a lot of matches, this will be 30x faster
    # otherwise not noticeably slower even in benchmarks
    if not LIM_RE.search(s):
        if slang and slang_re.search(s):
            pass
        else:
            # ensure str like expected from re.sub
            return str(s)
    s = contractions_re.sub(rc, s)
    if leftovers:
        s = leftovers_re.sub(rl, s)
    if slang:
        s = unsafe_re.sub(ru, s)

    return s
