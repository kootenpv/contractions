from itertools import product
from textsearch import TextSearch


contractions_dict = {
    "ain't": "are not",
    "aren't": "are not",
    "can't": "can not",
    "can't've": "can not have",
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
    "how're": "how are",
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
}

for month in [
    "january",
    "february",
    "march",
    "april",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
]:
    contractions_dict[month[:3] + "."] = month

contractions_dict.update({k.replace("'", "’"): v for k, v in contractions_dict.items()})


leftovers_dict = {
    "'all": '',
    "'am": '',
    "'cause": 'because',
    "'d": " would",
    "'ll": " will",
    "'re": " are",
    "'em": " them",
    "doin'": "doing",
    "goin'": "going",
    "nothin'": "nothing",
    "somethin'": "something",
    "havin'": "having",
    "doin'": "doing",
    "lovin'": "loving",
    "'coz": "because",
    "thats": "that is",
    "whats": "what is",
}

leftovers_dict.update({k.replace("'", "’"): v for k, v in leftovers_dict.items()})

safety_keys = set(["he's", "he'll", "we'll", "we'd", "it's", "i'd", "we'd", "we're", "i'll"])


def get_combinations(tokens, joiners):
    combs = []
    combs.append(tokens)
    results = []
    for option in combs:
        option = [[x] for x in option]
        option = intersperse(option, joiners)
        for c in product(*option):
            results.append("".join(c))
    return results


def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result


# have to create all the possibilities of ' and nothing
unsafe_dict = {}
for k, v in contractions_dict.items():  # contractions_dict.items():
    if k.lower() in safety_keys:
        continue
    if "'" not in k:
        continue
    tokens = k.split("'")
    for comb in get_combinations(tokens, ["", "'"]):
        unsafe_dict[comb] = v


slang_dict = {
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

slang_dict.update(unsafe_dict)

ts_leftovers = TextSearch("ignore", "norm")
ts_leftovers.add(contractions_dict)
ts_leftovers.add(leftovers_dict)

ts_leftovers_slang = TextSearch("ignore", "norm")
ts_leftovers_slang.add(contractions_dict)
ts_leftovers_slang.add(leftovers_dict)
ts_leftovers_slang.add(slang_dict)

ts_slang = TextSearch("ignore", "norm")
ts_slang.add(contractions_dict)
ts_slang.add(slang_dict)

ts_basic = TextSearch("ignore", "norm")
ts_basic.add(contractions_dict)

replacers = {
    (True, False): ts_leftovers,
    (True, True): ts_leftovers_slang,
    (False, True): ts_slang,
    (False, False): ts_basic,
}


def fix(s, leftovers=True, slang=True):
    ts = replacers[(leftovers, slang)]
    return ts.replace(s)


def add(key, value):
    for ts in replacers.values():
        ts.add(key, value)
