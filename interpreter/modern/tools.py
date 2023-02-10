from re import sub
from typing import Any

def adapt_condition(s: str) -> str:
    s = sub(r"([\s\w]=)", r"\1=", s)
    s = sub("<>", "!=", s)
    s = sub(" mod ", "%", s)
    s = sub(" div ", "//", s)
    s = sub(" NOT ", " not ", s)
    s = sub(" AND", " and ", s)
    s = sub(" OR ", " or ", s)
    s = sub(" XOR ", " ^ ", s)
    s = sub("addItem", "add_item", s)
    s = sub("getNext", "get_next", s)
    s = sub("resetNext", "reset_next", s)
    s = sub("hasNext", "has_next", s)
    s = sub("isEmpty", "is_empty", s)
    return s

def adapt_expression(s: str) -> str:
    s = sub(r"([\s\w]=)", r"\1=", s)
    s = sub("<>", "!=", s)
    s = sub(" mod ", " % ", s)
    s = sub(" div ", " // ", s)
    s = sub(r" NOT (.*)", r" __bitwise_not__(\1)", s)
    s = sub(" AND ", " & ", s)
    s = sub(" OR ", " | ", s)
    s = sub(" XOR ", " ^ ", s)
    s = sub(r"^\s*\[(.*)\]", r"Array([\1])", s)
    s = sub(r"^\s*\{(.*)\}", r"Dictionary({\1})", s)
    s = sub("addItem", "add_item", s)
    s = sub("getNext", "get_next", s)
    s = sub("resetNext", "reset_next", s)
    s = sub("hasNext", "has_next", s)
    s = sub("isEmpty", "is_empty", s)
    return s

def __bitwise_not__(n: int) -> int:
    return int("0b" + str(bin(n))[1:].replace('0', 'a').replace('1', '0').replace('a', '1'))

def printify(args: str, vars: dict[Any, Any]) -> str:
    res: str = ""
    for a in args.split(","):
        try:
            res += str(eval(a, vars))
        except:
            res += str(eval(adapt_expression(a), vars))
    return res