from re import sub

def adapt_condition(s):
    s = sub(r"([\s\w]=)", r"\1=", s)
    s = sub(" <> ", " != ", s)
    s = sub(" mod ", "%", s)
    s = sub(" div ", "//", s)
    s = sub(r"([^[^a-zA-Z0-9\[\]{}()+\-*/_])+NOT ", r"\1not ", s)
    s = sub(r"^NOT ", "not ", s)
    s = sub(" AND", " and ", s)
    s = sub(" OR ", " or ", s)
    s = sub(" XOR ", " ^ ", s)
    s = sub(r"([^[^a-zA-Z0-9\[\]{}()+\-*/_]+)true([^[^a-zA-Z0-9\[\]{}()+\-*/_]+)", r"\1True\2", s)
    s = sub(r"^true([^[^a-zA-Z0-9\[\]{}()+\-*/_]+)", r"True\1", s)
    s = sub(r"([^[^a-zA-Z0-9\[\]{}()+\-*/_]+)true$", r"\1True", s)
    s = sub(r"^true$", "True", s)
    s = sub(r"([^[^a-zA-Z0-9\[\]{}()+\-*/_]+)false([^[^a-zA-Z0-9\[\]{}()+\-*/_]+)", r"\1False\2", s)
    s = sub(r"^false([^[^a-zA-Z0-9\[\]{}()+\-*/_]+)", r"False\1", s)
    s = sub(r"([^[^a-zA-Z0-9\[\]{}()+\-*/_]+)false$", r"\1False", s)
    s = sub(r"^false$", "False", s)
    s = sub(r"^\s*\[(.*)\]", r"Array([\1])", s)
    s = sub(r"^\s*\{(.*)\}", r"Dictionary({\1})", s)
    s = sub(".addItem", ".add_item", s)
    s = sub(".getNext", ".get_next", s)
    s = sub(".resetNext", ".reset_next", s)
    s = sub(".hasNext", ".has_next", s)
    s = sub(".isEmpty", ".is_empty", s)
    return s

def adapt_expression(s):
    s = sub(r"([\s\w]=)", r"\1=", s)
    s = sub(" <> ", " != ", s)
    s = sub(" mod ", " % ", s)
    s = sub(" div ", " // ", s)
    s = sub(r"([^[^a-zA-Z0-9\[\]{}()+\-*/_]+)NOT (.*)", r"\1__bitwise_not__(\2)", s)
    s = sub(r"^NOT (.*)", r"__bitwise_not__(\1)", s)
    s = sub(" AND ", " & ", s)
    s = sub(" OR ", " | ", s)
    s = sub(" XOR ", " ^ ", s)
    s = sub(r"([^[^a-zA-Z0-9\[\]{}()+\-*/_]+)true([^[^a-zA-Z0-9\[\]{}()+\-*/_]+)", r"\1True\2", s)
    s = sub(r"^true([^[^a-zA-Z0-9\[\]{}()+\-*/_]+)", r"True\1", s)
    s = sub(r"([^[^a-zA-Z0-9\[\]{}()+\-*/_]+)true$", r"\1True", s)
    s = sub(r"^true$", "True", s)
    s = sub(r"([^[^a-zA-Z0-9\[\]{}()+\-*/_]+)false([^[^a-zA-Z0-9\[\]{}()+\-*/_]+)", r"\1False\2", s)
    s = sub(r"^false([^[^a-zA-Z0-9\[\]{}()+\-*/_]+)", r"False\1", s)
    s = sub(r"([^[^a-zA-Z0-9\[\]{}()+\-*/_]+)false$", r"\1False", s)
    s = sub(r"^false$", "False", s)
    s = sub(r"^\s*\[(.*)\]", r"Array([\1])", s)
    s = sub(r"^\s*\{(.*)\}", r"Dictionary({\1})", s)
    s = sub(".addItem", ".add_item", s)
    s = sub(".getNext", ".get_next", s)
    s = sub(".resetNext", ".reset_next", s)
    s = sub(".hasNext", ".has_next", s)
    s = sub(".isEmpty", ".is_empty", s)
    return s

def __bitwise_not__(n):
    return int("0b" + str(bin(n))[2:].replace('0', 'a').replace('1', '0').replace('a', '1'), 2)

def printify(args, vars):
    res = ""
    current = ""
    for a in args.split(","):
        try:
            current = eval(a, vars)
        except:
            current = eval(adapt_expression(a), vars)
        if isinstance(current, bool):
            if current:
                res += "true"
            else:
                res += "false"
        else:
            res += str(current)
    return res