from re import sub
from typing import Any

def replace_internal(x: Any) -> Any:
    if x.group(1):
        return x.group(1)
    else:
        return x.group(2)

def replace_ignore_quotes(pattern: str, replacement: str, string: str) -> str:
    return sub(r"(\"[^\"]*\")|" + pattern, lambda x: x.group(1) if x.group(1) else replacement.replace("\\1", "" if len(x.groups()) < 2 else x.group(2)).replace("\\2", "" if len(x.groups()) < 3 else x.group(3)), string)

def adapt_condition(string: str) -> str:
    string = replace_ignore_quotes(r"([\sa-zA-Z0-9\]})]=)", r"\1=", string)
    string = replace_ignore_quotes(r"([\sa-zA-Z0-9\]})])<>", r"\1!=", string)
    string = replace_ignore_quotes(" mod ", "%", string)
    string = replace_ignore_quotes(" div ", "//", string)
    string = replace_ignore_quotes(r"([^a-zA-Z0-9\]})+\-*/_\"\'])+NOT ", r"\1not ", string)
    string = replace_ignore_quotes(r"^NOT ", "not ", string)
    string = replace_ignore_quotes(" AND", " and ", string)
    string = replace_ignore_quotes(" OR ", " or ", string)
    string = replace_ignore_quotes(" XOR ", " ^ ", string)
    string = replace_ignore_quotes(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)true([^a-zA-Z0-9\[{(+\-*/_\"\']+)", r"\1True\2", string)
    string = replace_ignore_quotes(r"^true([^a-zA-Z0-9\]})+\-*/_\"\']+)", r"True\1", string)
    string = replace_ignore_quotes(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)true$", r"\1True", string)
    string = replace_ignore_quotes(r"^true$", "True", string)
    string = replace_ignore_quotes(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)false([^a-zA-Z0-9\[{(+\-*/_\"\']+)", r"\1False\2", string)
    string = replace_ignore_quotes(r"^false([^a-zA-Z0-9\]})+\-*/_\"\']+)", r"False\1", string)
    string = replace_ignore_quotes(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)false$", r"\1False", string)
    string = replace_ignore_quotes(r"^false$", "False", string)
    string = replace_ignore_quotes(r"^\s*\[(.*)\]", r"Array([\1])", string)
    string = replace_ignore_quotes(r"^\s*\{(.*)\}", r"Collection([\1])", string)
    return string

def adapt_expression(string: str) -> str:
    string = replace_ignore_quotes(r"([\sa-zA-Z0-9\]})]=)", r"\1=", string)
    string = replace_ignore_quotes(r"([\sa-zA-Z0-9\]})])<>", r"\1!=", string)
    string = replace_ignore_quotes(" mod ", " % ", string)
    string = replace_ignore_quotes(" div ", " // ", string)
    string = replace_ignore_quotes(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)NOT (.*)", r"\1__bitwise_not__(\2)", string)
    string = replace_ignore_quotes(r"^NOT (.*)", r"__bitwise_not__(\1)", string)
    string = replace_ignore_quotes(" AND ", " & ", string)
    string = replace_ignore_quotes(" OR ", " | ", string)
    string = replace_ignore_quotes(" XOR ", " ^ ", string)
    string = replace_ignore_quotes(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)true([^a-zA-Z0-9\[{(+\-*/_\"\']+)", r"\1True\2", string)
    string = replace_ignore_quotes(r"^true([^a-zA-Z0-9\]})+\-*/_\"\']+)", r"True\1", string)
    string = replace_ignore_quotes(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)true$", r"\1True", string)
    string = replace_ignore_quotes(r"^true$", "True", string)
    string = replace_ignore_quotes(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)false([^a-zA-Z0-9\[{(+\-*/_\"\']+)", r"\1False\2", string)
    string = replace_ignore_quotes(r"^false([^a-zA-Z0-9\]})+\-*/_\"\']+)", r"False\1", string)
    string = replace_ignore_quotes(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)false$", r"\1False", string)
    string = replace_ignore_quotes(r"^false$", "False", string)
    string = replace_ignore_quotes(r"^\s*\[(.*)\]", r"Array([\1])", string)
    string = replace_ignore_quotes(r"^\s*\{(.*)\}", r"Collection([\1])", string)
    return string

def __bitwise_not__(number: int) -> int:
    return int("0b" + str(bin(number))[2:].replace('0', 'a').replace('1', '0').replace('a', '1'), 2)

def printify(args: str, vars: dict[Any, Any]) -> str:
    comma_indexes: list[int] = []
    state: str = ""
    for index in range(0, len(args)):
        if args[index] in state:
            state = ""
        elif args[index] == '"' and state == "":
            state = '""'
        elif args[index] == '(' and state == "":
            state = '()'
        elif args[index] == '[' and state == "":
            state = '[]'
        elif args[index] == '{' and state == "":
            state = '{}'
        elif args[index] == "," and state == "":
            comma_indexes.append(index)
    res: str = ""
    current: Any = ""
    for arg in ([args] if len(comma_indexes) == 0 else [args[:comma_indexes[i]] if i == 0 else args[comma_indexes[i - 1] + 1:] if i == len(comma_indexes) else args[comma_indexes[i - 1] + 1:comma_indexes[i]] for i in range(0, len(comma_indexes) + 1)]):
        try:
            current = eval(arg, vars)
        except:
            current = eval(adapt_expression(arg), vars)
        if isinstance(current, bool):
            if current:
                res += "true"
            else:
                res += "false"
        else:
            res += str(current)
    return res