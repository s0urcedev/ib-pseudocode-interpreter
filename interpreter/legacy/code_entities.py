from functools import reduce
from re import search, findall
try:
    from tools import adapt_condition, adapt_expression, __bitwise_not__, printify, replace_ignore_quotes
    from data_structures import Array, ArrayInternal, Dictionary, Collection, CollectionInternal, Stack, Queue
except:
    from interpreter.legacy.tools import adapt_condition, adapt_expression, __bitwise_not__, printify, replace_ignore_quotes
    from interpreter.legacy.data_structures import Array, ArrayInternal, Dictionary, Collection, CollectionInternal, Stack, Queue

class Instruction:

    def __init__(self, text, read_only = [{}], read_write = {}):
        self.read_only = read_only
        self.read_write = read_write
        self.INSTRUCTIONS = {
            "input": self.input,
            "output": self.output,
            "assign": self.assign,
            "create": self.create,
            "array": self.create_array,
            "dictionary": self.create_dictionary,
            "collection": self.create_collection,
            "stack": self.create_stack,
            "queue": self.create_queue,
            "boolean": self.create_boolean,
            "number": self.create_number,
            "string": self.create_string,
            "delete": self.delete,
            "run": self.run
        }
        instruction: str = text[:text.find(" ")].lower()
        if instruction in self.INSTRUCTIONS:
            self.instruction: str = instruction
            self.content = (text[text.find(" ") + 1:].strip(), "")
        elif text.find("=") != -1:
            self.instruction: str = "assign"
            self.content = (text[:text.find("=")].strip(), text[text.find("=") + 1:].strip())
        else:
            self.instruction: str = "run"
            self.content = (text.strip(), "")

    def input(self):
        if "__stdin__" in self.read_only[0]:
            try:
                while True:
                    text = self.read_only[0]["__stdin__"].pop()
                    if text != "":
                        break
            except:
                raise Exception("Not all inputs are given")
        else:
            try:
                while True:
                    text = input()
                    if text != "":
                        break
            except:
                raise Exception("Not all inputs are given")
        text = text.strip()
        value = None
        try:
            value = int(text)
        except:
            try:
                value = float(text)
            except:
                if text in ["true", "false"]:
                    value = (text == "true")
                elif text == "none":
                    value = None
                elif text[0] == "[" and text[-1] == "]":
                    value = ArrayInternal(text[1:-1])
                elif text[0] == "{" and text[-1] == "}":
                    value = CollectionInternal(text[1:-1])
                else:
                    value = text
        self.content = (self.content[0], value)
        self.assign(value_not_string=True)

    def output(self):
        if "__stdout__" in self.read_only[0]:
            self.read_only[0]["__stdout__"].append(printify(self.content[0], dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write)))
        else:
            print(printify(self.content[0], dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write)))

    def assign(self, value_not_string = False) -> None:
        variable_structure = self.read_write
        variable_indexes = [self.content[0] if self.content[0].find("[") == -1 else self.content[0][:self.content[0].find("[")]]
        if self.content[0].find("[") != -1:
            bracket_diff = 0
            current_index = ""
            for i in range(self.content[0].find("["), len(self.content[0])):
                if self.content[0][i] == "[":
                    bracket_diff += 1
                if self.content[0][i] == "]":
                    bracket_diff -= 1
                    if bracket_diff == 0:
                        variable_indexes.append(current_index)
                        current_index = ""
                if (bracket_diff >= 1 and self.content[0][i] != "[") or bracket_diff > 1:
                    current_index += self.content[0][i]
            if current_index != "":
                variable_indexes.append(current_index)
        for i in range(0, len(variable_indexes) - 1):
            if i > 0:
                index = eval(adapt_expression(variable_indexes[i]), dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write))
            else:
                index = variable_indexes[i]
            if variable_structure[index] is None:
                try:
                    next_index = eval(adapt_expression(variable_indexes[i + 1]), dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write))
                    if int(next_index) == next_index and next_index >= 0:
                        variable_structure[index] = Array([])
                    else:
                        variable_structure[index] = Dictionary({})
                except:
                    variable_structure[index] = Dictionary({})
            variable_structure = variable_structure[index]
        if len(variable_indexes) > 1:
            index = eval(adapt_expression(variable_indexes[-1]), dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write))
        else:
            index = variable_indexes[-1]
        if value_not_string:
            variable_structure[index] = self.content[1]
        else:
            variable_structure[index] = eval(adapt_expression(self.content[1]), dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write))

    def create(self):
        if "array" in self.content[0].lower():
            self.read_write[self.content[0][self.content[0].lower().find("array") + 6:].strip()] = Array([])
        elif "dictionary" in self.content[0].lower():
            self.read_write[self.content[0][self.content[0].lower().find("dictionary") + 11:].strip()] = Dictionary({})
        elif "collection" in self.content[0].lower():
            self.read_write[self.content[0][self.content[0].lower().find("collection") + 11:].strip()] = Collection([])
        elif "stack" in self.content[0].lower():
            self.read_write[self.content[0][self.content[0].lower().find("stack") + 6:].strip()] = Stack([])
        elif "queue" in self.content[0].lower():
            self.read_write[self.content[0][self.content[0].lower().find("queue") + 6:].strip()] = Queue([])
        elif "boolean" in self.content[0].lower():
            self.read_write[self.content[0][self.content[0].lower().find("boolean") + 8:].strip()] = False
        elif "number" in self.content[0].lower():
            self.read_write[self.content[0][self.content[0].lower().find("number") + 7:].strip()] = 0
        elif "string" in self.content[0].lower():
            self.read_write[self.content[0][self.content[0].lower().find("string") + 7:].strip()] = ""

    def create_array(self):
        self.read_write[self.content[0]] = Array([])

    def create_dictionary(self):
        self.read_write[self.content[0]] = Dictionary({})

    def create_collection(self):
        self.read_write[self.content[0]] = Collection([])

    def create_stack(self):
        self.read_write[self.content[0]] = Stack([])

    def create_queue(self):
        self.read_write[self.content[0]] = Queue([])

    def create_boolean(self):
        self.read_write[self.content[0]] = False

    def create_number(self):
        self.read_write[self.content[0]] = 0

    def create_string(self):
        self.read_write[self.content[0]] = ""

    def delete(self):
        del self.read_write[self.content[0]]

    def run(self):
        eval(adapt_expression(self.content[0]), dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write))

    def execute(self):
        self.INSTRUCTIONS[self.instruction]()

    def __str__(self):
        return f"{'{'} command: {self.instruction}, content: {self.content} {'}'}"

class Condition:

    def __init__(self, conditions_text, if_blocks_text, else_block_text = "", read_only = [{}], read_write = {}):
        self.read_only = read_only
        self.read_write = read_write
        self.conditions = [ct[ct.lower().find("if") + 2:] for ct in conditions_text]
        self.if_blocks = [Block(bt, self.read_only, self.read_write) for bt in if_blocks_text]
        if else_block_text != "":
            self.else_block = Block(else_block_text, self.read_only, self.read_write)
        else:
            self.else_block = None

    def execute(self):
        for i in range(0, len(self.conditions)):
            if eval(self.conditions[i], dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write)):
                return self.if_blocks[i].execute()
        else: 
            if self.else_block != None:
                return self.else_block.execute()

    def __str__(self):
        return f"{'{'} conditions: {self.conditions}, if_blocks: {self.if_blocks}, else_block: {self.else_block} {'}'}"

class Loop:

    def __init__(self, condition, block, read_only = [{}], read_write = {}):
        self.read_only = read_only
        self.read_write = read_write
        if "while" in condition.lower():
            self.type = "while"
            self.condition = condition[condition.lower().find("while") + 5:]
        elif "until" in condition.lower():
            self.type = "until"
            self.condition = condition[condition.lower().find("until") + 5:]
        elif "from" in condition.lower() and "to" in condition.lower():
            self.type = "for"
            self.start_instruction = Instruction(f"{condition[condition.lower().find('loop') + 4:condition.lower().find('to')]}".replace("from", "="), self.read_only, self.read_write)
            self.iter_instruction = Instruction(f"{condition[condition.lower().find('loop') + 4:condition.lower().find('from') - 1]} = {condition[condition.lower().find('loop') + 4:condition.lower().find('from') - 1]} + 1", self.read_only, self.read_write)
            self.end_instruction = Instruction(f"delete {condition[condition.lower().find('loop') + 4:condition.lower().find('from') - 1]}", self.read_only, self.read_write)
            self.condition = f"{condition[condition.lower().find('loop') + 4:condition.lower().find('from')]} <= {condition[condition.lower().find('to') + 2:]}"
        else:
            self.type = "while"
            self.condition = condition[condition.lower().find("loop") + 4:]
        self.block = Block(block, self.read_only, self.read_write)

    def execute(self):
        if self.type == "while":
            while eval(self.condition, dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write)):
                try:
                    self.block.execute()
                except Exception as exc:
                    if str(exc) == "Unexpected break":
                        break
                    elif str(exc) != "Unexpected continue":
                        raise Exception(str(exc))
        elif self.type == "until":
            while not eval(self.condition, dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write)):
                try:
                    self.block.execute()
                except Exception as exc:
                    if str(exc) == "Unexpected break":
                        break
                    elif str(exc) != "Unexpected continue":
                        raise Exception(str(exc))
        elif self.type == "for":
            self.start_instruction.execute()
            while eval(self.condition, dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write)):
                try:
                    self.block.execute()
                except Exception as exc:
                    if str(exc) == "Unexpected break":
                        break
                    elif str(exc) != "Unexpected continue":
                        raise Exception(str(exc))
                self.iter_instruction.execute()
            self.end_instruction.execute()

    def __str__(self):
        if self.type == "for":
            return f"{'{'} type: {self.type} condition: {self.condition}, start_instruction: {self.start_instruction}, iter_instruction: {self.iter_instruction}, end_instruction: {self.end_instruction} block: {self.block} {'}'}"
        else:
            return f"{'{'} type: {self.type} condition: {self.condition}, block: {self.block} {'}'}"

class Function:

    def __init__(self, statement, block_text, read_only = [{}]):
        self.read_only = read_only
        statement_list = findall(r"(\w+)", statement)
        self.name = statement_list[1]
        self.arguments = statement_list[2:]
        self.block_text = block_text

    def execute(self, *args):
        return Block(self.block_text, self.read_only, dict(zip(self.arguments, args))).execute()

class Procedure(Function):

    def execute(self, *args):
        Block(self.block_text, self.read_only, dict(zip(self.arguments, args))).execute()

class Block:

    def __init__(self, text, read_only = [{}], read_write = {}):
        self.read_only = read_only
        self.read_write = read_write
        self.code = []
        current_if_block = []
        current_else_block = []
        if_conditions = []
        if_blocks = []
        current_statement = ""
        current_block = []
        state = ""
        state_difference = 0
        text = text.replace("\r", "")
        text = replace_ignore_quotes(r"[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+then[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*\n", "\n", text)
        text = replace_ignore_quotes(r"loop[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+for[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+", "loop ", text)
        text = replace_ignore_quotes(r"//.*\n", "\n", text)
        counter = 0
        lines = text.split("\n")
        for line in lines:
            if search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*//", line.strip()):
                continue
            elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*end procedure[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()) and state == "procedure" and state_difference == 0:
                self.read_write[findall(r"(\w+)", current_statement)[1]] = Procedure(current_statement, "\n".join(current_block), self.read_only + [self.read_write]).execute
                current_statement = ""
                current_block = []
                state = ""
            elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*procedure[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+", line.lower()) and state == "":
                state = "procedure"
                current_statement = adapt_condition(line)
            elif state == "procedure":
                if search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*end procedure[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()):
                    state_difference -= 1
                elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*procedure[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+", line.lower()):
                    state_difference += 1
                current_block.append(line)
            elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*end function[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()) and state == "function" and state_difference == 0:
                self.read_write[findall(r"(\w+)", current_statement)[1]] = Function(current_statement, "\n".join(current_block), self.read_only + [self.read_write]).execute
                current_statement = ""
                current_block = []
                state = ""
            elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*function[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+", line.lower()) and state == "":
                state = "function"
                current_statement = adapt_condition(line)
            elif state == "function":
                if search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*end function[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()):
                    state_difference -= 1
                elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*function[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+", line.lower()):
                    state_difference += 1
                current_block.append(line)
            elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*end loop[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()) and state == "loop" and state_difference == 0:
                self.code.append(Loop(current_statement, "\n".join(current_block), self.read_only, self.read_write))
                current_statement = ""
                current_block = []
                state = ""
            elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*loop[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+", line.lower()) and state == "":
                state = "loop"
                current_statement = adapt_condition(line)
            elif state == "loop":
                if search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*end loop[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()):
                    state_difference -= 1
                elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*loop[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+", line.lower()):
                    state_difference += 1
                current_block.append(line)
            elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*end if[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()) and (state == "if" or state == "else") and state_difference == 0:
                if_blocks.append("\n".join(current_if_block))
                self.code.append(Condition(if_conditions, if_blocks, "\n".join(current_else_block), self.read_only, self.read_write))
                if_conditions = []
                current_if_block = []
                current_else_block = []
                if_blocks = []
                state = ""
            elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*else if[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+", line.lower()) and state == "if" and state_difference == 0:
                state = "if"
                if_blocks.append("\n".join(current_if_block))
                current_if_block = []
                if_conditions.append(adapt_condition(line))
            elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*else[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()) and state == "if" and state_difference == 0:
                state = "else"
                if_blocks.append("\n".join(current_if_block))
                current_if_block = []
            elif state == "else":
                if search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*end if[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()):
                    state_difference -= 1
                elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*else[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()):
                    state_difference += 1
                current_else_block.append(line)
            elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*if[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+", line.lower()) and state == "":
                state = "if"
                if_conditions.append(adapt_condition(line))
            elif state == "if":
                if search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*end if[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()):
                    state_difference -= 1
                elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*if[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+", line.lower()):
                    state_difference += 1
                current_if_block.append(line)
            elif line.strip() != "":
                self.code.append(Instruction(line.strip(), self.read_only, self.read_write))
            counter += 1
        if state != "":
            raise Exception(f"Some end {state if state != 'else' else 'if'} is missed")

    def execute(self):
        for entity in self.code:
            if isinstance(entity, Instruction) and entity.content[0].lower() == "continue":
                raise Exception("Unexpected continue")
            elif isinstance(entity, Instruction) and entity.content[0].lower() == "break":
                raise Exception("Unexpected break")
            elif isinstance(entity, Instruction) and entity.content[0].lower() == "return":
                return None
            elif isinstance(entity, Instruction) and "return" in entity.content[0].lower():
                return eval(adapt_expression(entity.content[0][entity.content[0].lower().find("return") + 6:]), dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write))
            res = entity.execute()
            if res is not None:
                return res

    def __str__(self):
        return f"{'{'} code: {self.code} {'}'}"

class Code:

    def __init__(self, code):
        self.global_vars = {
            "__bitwise_not__": __bitwise_not__,
            "Array": Array,
            "ArrayInternal": ArrayInternal,
            "Dictionary": Dictionary,
            "Collection": Collection,
            "CollectionInternal": CollectionInternal,
            "Stack": Stack,
            "Queue": Queue
        }
        self.global_block = Block(code, [self.global_vars], {})

    def run(self):
        self.global_block.execute()
    
    def __str__(self):
        return f"{'{'} global_vars: {self.global_vars}, global_blocks: {self.global_block} {'}'}"

class CodeInternal:

    def __init__(self, code, stdin):
        self.global_vars = {
            "__bitwise_not__": __bitwise_not__,
            "Array": Array,
            "ArrayInternal": ArrayInternal,
            "Dictionary": Dictionary,
            "Collection": Collection,
            "CollectionInternal": CollectionInternal,
            "Stack": Stack,
            "Queue": Queue,
            "__stdin__": stdin.replace("\r", "").split("\n")[::-1],
            "__stdout__": []
        }
        self.parsing_err = ""
        try:
            self.global_block = Block(code, [self.global_vars], {})
        except Exception as exc:
            self.parsing_err = str(exc).replace(" (<string>, line 1)", "")

    def run(self):
        if self.parsing_err == "":
            try:
                self.global_block.execute()
                return "\n".join(self.global_vars["__stdout__"])
            except Exception as exc:
                return str(exc).replace(" (<string>, line 1)", "")
        else:
            return self.parsing_err
    
    def __str__(self):
        return f"{'{'} global_vars: {self.global_vars}, global_blocks: {self.global_block} {'}'}"