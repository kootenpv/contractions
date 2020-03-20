# contractions

**Update**: highly advised to use a `contractions>0.0.18` as it is 50x faster.

This package is capable of resolving contractions (and slang), examples:

```
you're -> you are
i'm    -> I am
# uses \b boundaries for "unsafe"
ima    -> I am going to
yall  -> you all
gotta  -> got to
```

Note that in ambigious cases it will revert to the most common case:

    he's -> he is (instead of he has)

## Usage

```python
import contractions
contractions.fix("you're happy now")
# "you are happy now"
contractions.fix("yall're happy now", slang=False) # default: true
# "yall are happy"
contractions.fix("yall're happy now")
# "you all are happy now"
```

## Easy to add your own!

Since `contractions>0.0.18`, you can easily add your own:

```python
import contractions
contractions.add('mychange', 'my change')
```

## Installation

```shell
pip install contractions
```
