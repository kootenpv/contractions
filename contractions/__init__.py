from itertools import product
from textsearch import TextSearch

import json
import pkgutil

json_open = pkgutil.get_data("contractions", "data/contractions_dict.json")
contractions_dict = json.loads(json_open.decode("utf-8"))

json_open = pkgutil.get_data("contractions", "data/leftovers_dict.json")
leftovers_dict = json.loads(json_open.decode("utf-8"))

json_open = pkgutil.get_data("contractions", "data/slang_dict.json")
slang_dict = json.loads(json_open.decode("utf-8"))

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

leftovers_dict.update({k.replace("'", "’"): v for k, v in leftovers_dict.items()})

safety_keys = set(
    ["he's", "he'll", "we'll", "we'd", "it's", "i'd", "we'd", "we're", "i'll", "who're", "o'"]
)


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

slang_dict.update(unsafe_dict)

ts_leftovers = TextSearch("insensitive", "norm")
ts_leftovers.add(contractions_dict)
ts_leftovers.add(leftovers_dict)

ts_leftovers_slang = TextSearch("insensitive", "norm")
ts_leftovers_slang.add(contractions_dict)
ts_leftovers_slang.add(leftovers_dict)
ts_leftovers_slang.add(slang_dict)

ts_slang = TextSearch("insensitive", "norm")
ts_slang.add(contractions_dict)
ts_slang.add(slang_dict)

ts_basic = TextSearch("insensitive", "norm")
ts_basic.add(contractions_dict)

ts_view_window = TextSearch("insensitive", "object")
ts_view_window.add(list(contractions_dict.keys()))
ts_view_window.add(list(leftovers_dict.keys()))
ts_view_window.add(list(slang_dict.keys()))

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


def preview(text, flank):
    """
    Return all contractions and their location before fix for manual check. Also provide a viewing window to quickly
    preview the contractions in the text.
    :param text: texture.
    :param flank: int number, control the size of the preview window. The window would be "flank-contraction-flank".
    :return: preview_items, a list includes all matched contractions and their locations.
    """
    try:
        int(flank)
    except Exception as e:
        print(e)
        raise Exception("Argument flank must be integer!")
    ts = ts_view_window
    results = ts.findall(text)
    preview_items = []
    for result in results:
        window_start = result.start - flank
        window_end = result.end + flank
        if window_start < 0:
            window_start = 0
        if window_end > len(text):
            window_end = len(text)
        preview_items.append({"match": result.match, "start": result.start, "end": result.end,
                             "viewing_window": text[window_start: window_end]})
    return preview_items
