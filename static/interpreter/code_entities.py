from typing import Any, Callable
from functools import reduce
from re import search, findall, Match
from tools import adapt_condition, adapt_expression, bitwise_not
from data_structures import Array, Dictionary, Collection, Stack, Queue

class Instruction:

    def __init__(self, text: str, read_only: list[dict[str, Any]] = [{}], read_write: dict[str, Any] = {}) -> None:
        self.read_only: list[dict[str, Any]] = read_only
        self.read_write: dict[str, Any] = read_write
        self.INSTRUCTIONS: dict[str, Callable[[], None]] = {
            "input": self.input,
            "output": self.output,
            "assign": self.assign,
            "delete": self.delete,
            "run": self.run,
            "array": self.create_array,
            "dictionary": self.create_dictionary,
            "collection": self.create_collection,
            "stack": self.create_stack,
            "queue": self.create_queue
        }
        if text.find("=") != -1:
            instruction: str = "assign"
            content: tuple[str, str] = (text[:text.find("=")].strip(), text[text.find("=") + 2:].strip())
        else:
            instruction: str = text[:text.find(" ")]
            content: tuple[str, str] = (text[text.find(" ") + 1:].strip(), "")
        if instruction in self.INSTRUCTIONS:
            self.instruction: str = instruction
            self.content: tuple[str, str] = content
        else:
            self.instruction: str = "run"
            self.content: tuple[str, str] = (text.strip(), "")

    def input(self) -> None:
        text: str = input()
        try:
            self.read_write[self.content[0]] = int(text)
        except:
            self.read_write[self.content[0]] = text

    def output(self) -> None:
        print(eval(adapt_expression(self.content[0]), dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write)))

    def assign(self) -> None:
        match_obj: Match | None = search(r"\[.*\]", self.content[0])
        if match_obj != None:
            self.read_write[self.content[0][:match_obj.start()]][eval(self.content[0][match_obj.start() + 1:match_obj.end() - 1], dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write))] = eval(adapt_expression(self.content[1]), dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write))
        else:
            self.read_write[self.content[0]] = eval(adapt_expression(self.content[1]), dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write))

    def delete(self) -> None:
        del self.read_write[self.content[0]]

    def run(self) -> None:
        eval(adapt_expression(self.content[0]), dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write))

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

    def execute(self) -> None:
        self.INSTRUCTIONS[self.instruction]()

    def __str__(self) -> str:
        return f"{'{'} command: {self.instruction}, content: {self.content} {'}'}"

class Condition:

    def __init__(self, conditions_text: list[str], if_blocks_text: list[str], else_block_text: str = "", read_only: list[dict[str, Any]] = [{}], read_write: dict[str, Any] = {}) -> None:
        self.read_only: list[dict[str, Any]] = read_only
        self.read_write: dict[str, Any] = read_write
        self.conditions: list[str] = [ct[ct.find("if") + 2:] for ct in conditions_text]
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
        if "while" in condition:
            self.type: str = "while"
            self.condition: str = condition[condition.find("while") + 5:]
        elif "until" in condition:
            self.type: str = "until"
            self.condition: str = condition[condition.find("until") + 5:]
        elif "from" in condition and "to" in condition:
            self.type = "for"
            self.start_instruction: Instruction = Instruction(f"{condition[condition.find('loop') + 4:condition.find('to')]}".replace("from", "="), self.read_only, self.read_write)
            self.iter_instruction: Instruction = Instruction(f"{condition[condition.find('loop') + 4:condition.find('from') - 1]} = {condition[condition.find('loop') + 4:condition.find('from') - 1]} + 1", self.read_only, self.read_write)
            self.end_instruction: Instruction = Instruction(f"delete {condition[condition.find('loop') + 4:condition.find('from') - 1]}", self.read_only, self.read_write)
            self.condition: str = f"{condition[condition.find('loop') + 4:condition.find('from')]} <= {condition[condition.find('to') + 2:]}"
        else:
            self.type: str = "while"
            self.condition: str = condition[condition.find("loop") + 4:]
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
        loop_condition: str = ""
        current_loop_block: list[str] = []
        function_statement: str = ""
        current_function_block: list[str] = []
        procedure_statement: str = ""
        current_procedure_block: list[str] = []
        state: str = ""
        text = text.replace("\r", "").replace("then", "")
        counter = 0
        lines = text.split("\n")
        for t in lines:
            if search(r"^//", t.strip()):
                continue
            elif "end procedure" in t and procedure_statement != "" and len(t) - len(t.lstrip()) == len(procedure_statement) - len(procedure_statement.lstrip()):
                self.read_write[findall(r"(\w+)", procedure_statement)[1]] = Procedure(procedure_statement, "\n".join(current_procedure_block), self.read_only + [self.read_write]).execute
                procedure_statement = ""
                current_procedure_block = []
                state = ""
            elif "procedure" in t and state == "":
                state = "procedure"
                procedure_statement = adapt_condition(t)
            elif state == "procedure":
                current_procedure_block.append(t)
            elif "end function" in t and function_statement != "" and len(t) - len(t.lstrip()) == len(function_statement) - len(function_statement.lstrip()):
                self.read_write[findall(r"(\w+)", function_statement)[1]] = Function(function_statement, "\n".join(current_function_block), self.read_only + [self.read_write]).execute
                function_statement = ""
                current_function_block = []
                state = ""
            elif "function" in t and state == "":
                state = "function"
                function_statement = adapt_condition(t)
            elif state == "function":
                current_function_block.append(t)
            elif "end loop" in t and loop_condition != "" and len(t) - len(t.lstrip()) == len(loop_condition) - len(loop_condition.lstrip()):
                self.code.append(Loop(loop_condition, "\n".join(current_loop_block), self.read_only, self.read_write))
                loop_condition = ""
                current_loop_block = []
                state = ""
            elif "loop" in t and state == "":
                state = "loop"
                loop_condition = adapt_condition(t)
            elif state == "loop":
                current_loop_block.append(t)
            elif "end if" in t and len(if_conditions) != 0 and len(t) - len(t.lstrip()) == len(if_conditions[-1]) - len(if_conditions[-1].lstrip()):
                if_blocks.append("\n".join(current_if_block))
                self.code.append(Condition(if_conditions, if_blocks, "\n".join(current_else_block), self.read_only, self.read_write))
                if_conditions = []
                current_if_block = []
                current_else_block = []
                if_blocks = []
                state = ""
            elif "else if" in t and len(if_conditions) != 0 and len(t) - len(t.lstrip()) == len(if_conditions[-1]) - len(if_conditions[-1].lstrip()):
                state = "if"
                if_blocks.append("\n".join(current_if_block))
                current_if_block = []
                if_conditions.append(adapt_condition(t))
            elif "else" in t and len(if_conditions) != 0 and len(t) - len(t.lstrip()) == len(if_conditions[-1]) - len(if_conditions[-1].lstrip()):
                state = "else"
                if_blocks.append("\n".join(current_if_block))
                current_if_block = []
            elif state == "else":
                current_else_block.append(t)
            elif "if" in t and state == "":
                state = "if"
                if_conditions.append(adapt_condition(t))
            elif state == "if":
                current_if_block.append(t)
            elif t.strip() != "":
                self.code.append(Instruction(t.strip(), self.read_only, self.read_write))
            counter += 1

    def execute(self) -> Any | None:
        for c in self.code:
            if isinstance(c, Instruction) and c.content[0] == "continue":
                raise Exception("Unexpected continue")
            elif isinstance(c, Instruction) and c.content[0] == "break":
                raise Exception("Unexpected break")
            elif isinstance(c, Instruction) and c.content[0] == "return":
                return None
            elif isinstance(c, Instruction) and "return" in c.content[0]:
                return eval(adapt_expression(c.content[0][c.content[0].find("return") + 6:]), dict(reduce(lambda x, y: dict(x, **y), self.read_only), **self.read_write))
            res: Any | None = c.execute()
            if res is not None:
                return res

    def __str__(self) -> str:
        return f"{'{'} code: {self.code} {'}'}"

class Code:

    def __init__(self, code: str) -> None:
        self.global_vars: dict[str, Any] = {
            "bitwise_not": bitwise_not,
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