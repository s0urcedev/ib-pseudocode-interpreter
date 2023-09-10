from functools import reduce
from re import search, findall, sub
try:
    from tools import adapt_condition, adapt_expression, __bitwise_not__, printify
    from data_structures import Array, Dictionary, Collection, Stack, Queue
except:
    from interpreter.legacy.tools import adapt_condition, adapt_expression, __bitwise_not__, printify
    from interpreter.legacy.data_structures import Array, Dictionary, Collection, Stack, Queue

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
        if text.find("=") != -1 and all([i not in text.lower() for i in self.INSTRUCTIONS]):
            instruction = "assign"
            content = (text[:text.find("=")].strip(), text[text.find("=") + 1:].strip())
        else:
            instruction = text[:text.find(" ")].lower()
            content = (text[text.find(" ") + 1:].strip(), "")
        if instruction in self.INSTRUCTIONS:
            self.instruction = instruction
            self.content = content
        else:
            self.instruction = "run"
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
        try:
            self.read_write[self.content[0]] = int(text)
        except:
            self.read_write[self.content[0]] = text

    def output(self):
        if "__stdout__" in self.read_only[0]:
            self.read_only[0]["__stdout__"].append(printify(self.content[0], dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write)))
        else:
            print(printify(self.content[0], dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write)))

    def assign(self):
        match_obj = search(r"\[.*\]", self.content[0])
        if match_obj != None:
            self.read_write[self.content[0][:match_obj.start()]][eval(adapt_expression(self.content[0][match_obj.start() + 1:match_obj.end() - 1]), dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write))] = eval(adapt_expression(self.content[1]), dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write))
        else:
            self.read_write[self.content[0]] = eval(adapt_expression(self.content[1]), dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write))

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
        loop_condition = ""
        current_loop_block = []
        function_statement = ""
        current_function_block = []
        procedure_statement = ""
        current_procedure_block = []
        state = ""
        text = text.replace("\r", "")
        text = sub(r"\W+then\W*\n", "\n", text)
        text = sub(r"loop\W+for\W+", "loop ", text)
        text = sub(r"//.*\n", "\n", text)
        counter = 0
        lines = text.split("\n")
        for t in lines:
            if search(r"^\W*//", t.strip()):
                continue
            elif search(r"^\W*end procedure\W*$", t.lower()) and procedure_statement != "" and len(t) - len(t.lstrip()) == len(procedure_statement) - len(procedure_statement.lstrip()):
                self.read_write[findall(r"(\w+)", procedure_statement)[1]] = Procedure(procedure_statement, "\n".join(current_procedure_block), self.read_only + [self.read_write]).execute
                procedure_statement = ""
                current_procedure_block = []
                state = ""
            elif search(r"^\W*procedure\W+", t.lower()) and state == "":
                state = "procedure"
                procedure_statement = adapt_condition(t)
            elif state == "procedure":
                current_procedure_block.append(t)
            elif search(r"^\W*end function\W*$", t.lower()) and function_statement != "" and len(t) - len(t.lstrip()) == len(function_statement) - len(function_statement.lstrip()):
                self.read_write[findall(r"(\w+)", function_statement)[1]] = Function(function_statement, "\n".join(current_function_block), self.read_only + [self.read_write]).execute
                function_statement = ""
                current_function_block = []
                state = ""
            elif search(r"^\W*function\W+", t.lower()) and state == "":
                state = "function"
                function_statement = adapt_condition(t)
            elif state == "function":
                current_function_block.append(t)
            elif search(r"^\W*end loop\W*$", t.lower()) and loop_condition != "" and len(t) - len(t.lstrip()) == len(loop_condition) - len(loop_condition.lstrip()):
                self.code.append(Loop(loop_condition, "\n".join(current_loop_block), self.read_only, self.read_write))
                loop_condition = ""
                current_loop_block = []
                state = ""
            elif search(r"^\W*loop\W+", t.lower()) and state == "":
                state = "loop"
                loop_condition = adapt_condition(t)
            elif state == "loop":
                current_loop_block.append(t)
            elif search(r"^\W*end if\W*$", t.lower()) and len(if_conditions) != 0 and len(t) - len(t.lstrip()) == len(if_conditions[-1]) - len(if_conditions[-1].lstrip()):
                if_blocks.append("\n".join(current_if_block))
                self.code.append(Condition(if_conditions, if_blocks, "\n".join(current_else_block), self.read_only, self.read_write))
                if_conditions = []
                current_if_block = []
                current_else_block = []
                if_blocks = []
                state = ""
            elif search(r"^\W*else if\W+", t.lower()) and len(if_conditions) != 0 and len(t) - len(t.lstrip()) == len(if_conditions[-1]) - len(if_conditions[-1].lstrip()):
                state = "if"
                if_blocks.append("\n".join(current_if_block))
                current_if_block = []
                if_conditions.append(adapt_condition(t))
            elif search(r"^\W*else\W*$", t.lower()) and len(if_conditions) != 0 and len(t) - len(t.lstrip()) == len(if_conditions[-1]) - len(if_conditions[-1].lstrip()):
                state = "else"
                if_blocks.append("\n".join(current_if_block))
                current_if_block = []
            elif state == "else":
                current_else_block.append(t)
            elif search(r"^\W*if\W+", t.lower()) and state == "":
                state = "if"
                if_conditions.append(adapt_condition(t))
            elif state == "if":
                current_if_block.append(t)
            elif t.strip() != "":
                self.code.append(Instruction(t.strip(), self.read_only, self.read_write))
            counter += 1

    def execute(self):
        for c in self.code:
            if isinstance(c, Instruction) and c.content[0].lower() == "continue":
                raise Exception("Unexpected continue")
            elif isinstance(c, Instruction) and c.content[0].lower() == "break":
                raise Exception("Unexpected break")
            elif isinstance(c, Instruction) and c.content[0].lower() == "return":
                return None
            elif isinstance(c, Instruction) and "return" in c.content[0].lower():
                return eval(adapt_expression(c.content[0][c.content[0].lower().find("return") + 6:]), dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write))
            res = c.execute()
            if res is not None:
                return res

    def __str__(self):
        return f"{'{'} code: {self.code} {'}'}"

class Code:

    def __init__(self, code):
        self.global_vars = {
            "__bitwise_not__": __bitwise_not__,
            "Array": Array,
            "Dictionary": Dictionary,
            "Collection": Collection,
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
            "Dictionary": Dictionary,
            "Collection": Collection,
            "Stack": Stack,
            "Queue": Queue,
            "__stdin__": stdin.replace("\r", "").split("\n")[::-1],
            "__stdout__": []
        }
        self.global_block = Block(code, [self.global_vars], {})

    def run(self):
        try:
            self.global_block.execute()
            return "\n".join(self.global_vars["__stdout__"])
        except Exception as exc:
            return str(exc)
    
    def __str__(self):
        return f"{'{'} global_vars: {self.global_vars}, global_blocks: {self.global_block} {'}'}"