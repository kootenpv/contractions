# contractions

This package is capable of resolving contractions (and slang), examples:

```
you're -> you are
i'm    -> I am
ima    -> I am going to
youll  -> you all
gotta  -> got to
```

Note that in ambigious cases it will revert to the most common case:

    he's -> he is (instead of he has)

## Usage

```python
import contractions
contractions.fix("you're happy now")
# "you are happy now"
contractions.fix("yall are happy now", slang=False) # default: true
# "yall are happy"
contractions.fix("yall are happy now")
# "you all are happy now"
```

## Installation

    pip install contractions
