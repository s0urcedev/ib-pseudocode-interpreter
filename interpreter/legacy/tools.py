from re import sub

def replace_internal(x):
    if x.group(1):
        return x.group(1)
    else:
        return x.group(2)

def replace_ignore_quotes(pattern, replacement, string):
    return sub(r"(\"[^\"]*\")|" + pattern, lambda x: x.group(1) if x.group(1) else replacement.replace("\\1", "" if len(x.groups()) < 2 else x.group(2)).replace("\\2", "" if len(x.groups()) < 3 else x.group(3)), string)

def adapt_condition(string):
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
    string = replace_ignore_quotes(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)none([^a-zA-Z0-9\[{(+\-*/_\"\']+)", r"\1None\2", string)
    string = replace_ignore_quotes(r"^none([^a-zA-Z0-9\]})+\-*/_\"\']+)", r"None\1", string)
    string = replace_ignore_quotes(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)none$", r"\1None", string)
    string = replace_ignore_quotes(r"^none$", "None", string)
    string = replace_ignore_quotes(r"^\s*\[(.*)\]", r"ArrayInternal('\1')", string)
    string = replace_ignore_quotes(r"^\s*\{(.*)\}", r"CollectionInternal('\1')", string)
    return string

def adapt_expression(string):
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
    string = replace_ignore_quotes(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)none([^a-zA-Z0-9\[{(+\-*/_\"\']+)", r"\1None\2", string)
    string = replace_ignore_quotes(r"^none([^a-zA-Z0-9\]})+\-*/_\"\']+)", r"None\1", string)
    string = replace_ignore_quotes(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)none$", r"\1None", string)
    string = replace_ignore_quotes(r"^none$", "None", string)
    string = replace_ignore_quotes(r"^\s*\[(.*)\]", r"ArrayInternal('\1')", string)
    string = replace_ignore_quotes(r"^\s*\{(.*)\}", r"CollectionInternal('\1')", string)
    return string

def __bitwise_not__(number):
    return int("0b" + str(bin(number))[2:].replace('0', 'a').replace('1', '0').replace('a', '1'), 2)

def divide_by_commas(string):
    comma_indexes = []
    state = ""
    state_diff = 0
    for index in range(0, len(string)):
        if state != "" and string[index] == state[0] and string[index] != state[1]:
            state_diff += 1
        elif state != "" and string[index] == state[1]:
            if state_diff == 0 or string[index] == state[0]:
                state = ""
                state_diff = 0
            else:
                state_diff -= 1
        elif string[index] == '"' and state == "":
            state = '""'
        elif string[index] == '(' and state == "":
            state = '()'
        elif string[index] == '[' and state == "":
            state = '[]'
        elif string[index] == '{' and state == "":
            state = '{}'
        elif string[index] == "," and state == "":
            comma_indexes.append(index)
    return [string] if len(comma_indexes) == 0 else [string[:comma_indexes[i]] if i == 0 else string[comma_indexes[i - 1] + 1:] if i == len(comma_indexes) else string[comma_indexes[i - 1] + 1:comma_indexes[i]] for i in range(0, len(comma_indexes) + 1)]

def printify(args, vars):
    res = ""
    current = ""
    for arg in divide_by_commas(args):
        try:
            current = eval(arg, vars)
        except:
            current = eval(adapt_expression(arg), vars)
        if isinstance(current, bool):
            if current:
                res += "true"
            else:
                res += "false"
        elif current is None:
            res += "none"
        else:
            res += str(current)
    return res