from typing import Any, Callable
from functools import reduce
from re import search, findall, Match
try:
    from tools import adapt_condition, adapt_expression, __bitwise_not__, printify, replace_ignore_quotes
    from data_structures import Array, Dictionary, Collection, Stack, Queue
except:
    from interpreter.modern.tools import adapt_condition, adapt_expression, __bitwise_not__, printify, replace_ignore_quotes
    from interpreter.modern.data_structures import Array, Dictionary, Collection, Stack, Queue

class Instruction:

    def __init__(self, text: str, read_only: list[dict[str, Any]] = [{}], read_write: dict[str, Any] = {}) -> None:
        self.read_only: list[dict[str, Any]] = read_only
        self.read_write: dict[str, Any] = read_write
        self.INSTRUCTIONS: dict[str, Callable[[], None]] = {
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
            instruction: str = "assign"
            content: tuple[str, str] = (text[:text.find("=")].strip(), text[text.find("=") + 1:].strip())
        else:
            instruction: str = text[:text.find(" ")].lower()
            content: tuple[str, str] = (text[text.find(" ") + 1:].strip(), "")
        if instruction in self.INSTRUCTIONS:
            self.instruction: str = instruction
            self.content: tuple[str, str] = content
        else:
            self.instruction: str = "run"
            self.content: tuple[str, str] = (text.strip(), "")

    def input(self) -> None:
        text: str
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
        value: Any = None
        try:
            value = int(text)
        except:
            if text in ["true", "false"]:
                value = (text == "true")
            elif text[0] == "[" and text[-1] == "]":
                value = Array(eval(text))
            elif text[0] == "{" and text[-1] == "}":
                value = Collection(eval(f"[{text[1:-1]}]"))
            else:
                value = text
        match_obj: Match[str] | None = search(r"\[.*\]", self.content[0])
        if match_obj != None:
            self.read_write[self.content[0][:match_obj.start()]][eval(adapt_expression(self.content[0][match_obj.start() + 1:match_obj.end() - 1]), dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write))] = value
        else:
            self.read_write[self.content[0]] = value

    def output(self) -> None:
        if "__stdout__" in self.read_only[0]:
            self.read_only[0]["__stdout__"].append(printify(self.content[0], dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write)))
        else:
            print(printify(self.content[0], dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write)))

    def assign(self) -> None:
        match_obj: Match[str] | None = search(r"\[.*\]", self.content[0])
        if match_obj != None:
            self.read_write[self.content[0][:match_obj.start()]][eval(adapt_expression(self.content[0][match_obj.start() + 1:match_obj.end() - 1]), dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write))] = eval(adapt_expression(self.content[1]), dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write))
        else:
            self.read_write[self.content[0]] = eval(adapt_expression(self.content[1]), dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write))

    def create(self) -> None:
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

    def create_array(self) -> None:
        self.read_write[self.content[0]] = Array([])

    def create_dictionary(self) -> None:
        self.read_write[self.content[0]] = Dictionary({})

    def create_collection(self) -> None:
        self.read_write[self.content[0]] = Collection([])

    def create_stack(self) -> None:
        self.read_write[self.content[0]] = Stack([])

    def create_queue(self) -> None:
        self.read_write[self.content[0]] = Queue([])

    def create_boolean(self) -> None:
        self.read_write[self.content[0]] = False

    def create_number(self) -> None:
        self.read_write[self.content[0]] = 0

    def create_string(self) -> None:
        self.read_write[self.content[0]] = ""

    def delete(self) -> None:
        del self.read_write[self.content[0]]

    def run(self) -> None:
        eval(adapt_expression(self.content[0]), dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write))

    def execute(self) -> None:
        self.INSTRUCTIONS[self.instruction]()

    def __str__(self) -> str:
        return f"{'{'} command: {self.instruction}, content: {self.content} {'}'}"

class Condition:

    def __init__(self, conditions_text: list[str], if_blocks_text: list[str], else_block_text: str = "", read_only: list[dict[str, Any]] = [{}], read_write: dict[str, Any] = {}) -> None:
        self.read_only: list[dict[str, Any]] = read_only
        self.read_write: dict[str, Any] = read_write
        self.conditions: list[str] = [ct[ct.lower().find("if") + 2:] for ct in conditions_text]
        self.if_blocks: list[Block] = [Block(bt, self.read_only, self.read_write) for bt in if_blocks_text]
        if else_block_text != "":
            self.else_block: Block | None = Block(else_block_text, self.read_only, self.read_write)
        else:
            self.else_block: Block | None = None

    def execute(self) -> Any | None:
        for i in range(0, len(self.conditions)):
            if eval(self.conditions[i], dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write)):
                return self.if_blocks[i].execute()
        else: 
            if self.else_block != None:
                return self.else_block.execute()

    def __str__(self) -> str:
        return f"{'{'} conditions: {self.conditions}, if_blocks: {self.if_blocks}, else_block: {self.else_block} {'}'}"

class Loop:

    def __init__(self, condition: str, block: str, read_only: list[dict[str, Any]] = [{}], read_write: dict[str, Any] = {}) -> None:
        self.read_only: list[dict[str, Any]] = read_only
        self.read_write: dict[str, Any] = read_write
        if "while" in condition.lower():
            self.type: str = "while"
            self.condition: str = condition[condition.lower().find("while") + 5:]
        elif "until" in condition.lower():
            self.type: str = "until"
            self.condition: str = condition[condition.lower().find("until") + 5:]
        elif "from" in condition.lower() and "to" in condition.lower():
            self.type = "for"
            self.start_instruction: Instruction = Instruction(f"{condition[condition.lower().find('loop') + 4:condition.lower().find('to')]}".replace("from", "="), self.read_only, self.read_write)
            self.iter_instruction: Instruction = Instruction(f"{condition[condition.lower().find('loop') + 4:condition.lower().find('from') - 1]} = {condition[condition.lower().find('loop') + 4:condition.lower().find('from') - 1]} + 1", self.read_only, self.read_write)
            self.end_instruction: Instruction = Instruction(f"delete {condition[condition.lower().find('loop') + 4:condition.lower().find('from') - 1]}", self.read_only, self.read_write)
            self.condition: str = f"{condition[condition.lower().find('loop') + 4:condition.lower().find('from')]} <= {condition[condition.lower().find('to') + 2:]}"
        else:
            self.type: str = "while"
            self.condition: str = condition[condition.lower().find("loop") + 4:]
        self.block: Block = Block(block, self.read_only, self.read_write)

    def execute(self) -> None:
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

    def __str__(self) -> str:
        if self.type == "for":
            return f"{'{'} type: {self.type} condition: {self.condition}, start_instruction: {self.start_instruction}, iter_instruction: {self.iter_instruction}, end_instruction: {self.end_instruction} block: {self.block} {'}'}"
        else:
            return f"{'{'} type: {self.type} condition: {self.condition}, block: {self.block} {'}'}"

class Function:

    def __init__(self, statement: str, block_text: str, read_only: list[dict[str, Any]] = [{}]) -> None:
        self.read_only: list[dict[str, Any]] = read_only
        statement_list: list[str] = findall(r"(\w+)", statement)
        self.name: str = statement_list[1]
        self.arguments: list[str] = statement_list[2:]
        self.block_text: str = block_text

    def execute(self, *args: list[Any]) -> Any | None:
        return Block(self.block_text, self.read_only, dict(zip(self.arguments, args))).execute()

class Procedure(Function):

    def execute(self, *args: list[Any]) -> None:
        Block(self.block_text, self.read_only, dict(zip(self.arguments, args))).execute()

class Block:

    def __init__(self, text: str, read_only: list[dict[str, Any]] = [{}], read_write: dict[str, Any] = {}) -> None:
        self.read_only: list[dict[str, Any]] = read_only
        self.read_write: dict[str, Any] = read_write
        self.code: list[Instruction | Condition | Loop] = []
        current_if_block: list[str] = []
        current_else_block: list[str] = []
        if_conditions: list[str] = []
        if_blocks: list[str] = []
        current_statement: str = ""
        current_block: list[str] = []
        state: str = ""
        state_difference: int = 0
        text = text.replace("\r", "")
        text = replace_ignore_quotes(r"[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+then[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*\n", "\n", text)
        text = replace_ignore_quotes(r"loop[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+for[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+", "loop ", text)
        text = replace_ignore_quotes(r"//.*\n", "\n", text)
        counter: int = 0
        lines: list[str] = text.split("\n")
        line: str
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

    def execute(self) -> Any | None:
        for entity in self.code:
            if isinstance(entity, Instruction) and entity.content[0].lower() == "continue":
                raise Exception("Unexpected continue")
            elif isinstance(entity, Instruction) and entity.content[0].lower() == "break":
                raise Exception("Unexpected break")
            elif isinstance(entity, Instruction) and entity.content[0].lower() == "return":
                return None
            elif isinstance(entity, Instruction) and "return" in entity.content[0].lower():
                return eval(adapt_expression(entity.content[0][entity.content[0].lower().find("return") + 6:]), dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write))
            res: Any | None = entity.execute()
            if res is not None:
                return res

    def __str__(self) -> str:
        return f"{'{'} code: {self.code} {'}'}"

class Code:

    def __init__(self, code: str) -> None:
        self.global_vars: dict[str, Any] = {
            "bitwise_not": __bitwise_not__,
            "Array": Array,
            "Dictionary": Dictionary,
            "Collection": Collection,
            "Stack": Stack,
            "Queue": Queue
        }
        self.global_block: Block = Block(code, [self.global_vars], {})

    def run(self) -> None:
        self.global_block.execute()
    
    def __str__(self) -> str:
        return f"{'{'} global_vars: {self.global_vars}, global_blocks: {self.global_block} {'}'}"

class CodeInternal:

    def __init__(self, code: str, stdin: str) -> None:
        self.global_vars: dict[str, Any] = {
            "bitwise_not": __bitwise_not__,
            "Array": Array,
            "Dictionary": Dictionary,
            "Collection": Collection,
            "Stack": Stack,
            "Queue": Queue,
            "__stdin__": stdin.replace("\r", "").split("\n")[::-1],
            "__stdout__": []
        }
        self.parsing_err: str = ""
        try:
            self.global_block: Block = Block(code, [self.global_vars], {})
        except Exception as exc:
            self.parsing_err = str(exc)

    def run(self) -> str:
        if self.parsing_err == "":
            try:
                self.global_block.execute()
                return "\n".join(self.global_vars["__stdout__"])
            except Exception as exc:
                return str(exc)
        else:
            return self.parsing_err
    
    def __str__(self) -> str:
        return f"{'{'} global_vars: {self.global_vars}, global_blocks: {self.global_block} {'}'}"