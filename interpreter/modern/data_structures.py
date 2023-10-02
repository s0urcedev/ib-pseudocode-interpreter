from typing import Any
from re import sub

class Array:

    def __init__(self, body: Any) -> None:
        if hasattr(body, "body"):
            self.body: list[Any] = list(body.body)
        else:
            self.body: list[Any] = body

    def __getitem__(self, index: int) -> Any:
        return self.body[index]

    def __setitem__(self, index: int, value: Any) -> None:
        while index >= len(self.body):
            self.body.append(None)
        self.body[index] = value

    def size(self) -> int:
        return len(self.body)

    def length(self) -> int:
        return len(self.body)

    def __str__(self) -> str:
        s: str = str(self.body)
        s = sub(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)True([^a-zA-Z0-9\[{(+\-*/_\"\']+)", r"\1true\2", s)
        s = sub(r"^True([^a-zA-Z0-9\]})+\-*/_\"\']+)", r"true\1", s)
        s = sub(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)True$", r"\1true", s)
        s = sub(r"^True$", "true", s)
        s = sub(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)False([^a-zA-Z0-9\[{(+\-*/_\"\']+)", r"\1false\2", s)
        s = sub(r"^False([^a-zA-Z0-9\]})+\-*/_\"\']+)", r"false\1", s)
        s = sub(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)False$", r"\1false", s)
        s = sub(r"^False$", "false", s)
        return s

class Dictionary:

    def __init__(self, body: dict[Any, Any]) -> None:
        self.body: dict[Any, Any] = body

    def __getitem__(self, key: Any) -> Any:
        return self.body[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        self.body[key] = value

    def __str__(self) -> str:
        s: str = str(self.body)
        s = sub(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)True([^a-zA-Z0-9\[{(+\-*/_\"\']+)", r"\1true\2", s)
        s = sub(r"^True([^a-zA-Z0-9\]})+\-*/_\"\']+)", r"true\1", s)
        s = sub(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)True$", r"\1true", s)
        s = sub(r"^True$", "true", s)
        s = sub(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)False([^a-zA-Z0-9\[{(+\-*/_\"\']+)", r"\1false\2", s)
        s = sub(r"^False([^a-zA-Z0-9\]})+\-*/_\"\']+)", r"false\1", s)
        s = sub(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)False$", r"\1false", s)
        s = sub(r"^False$", "false", s)
        return s

class Collection:

    def __init__(self, body: Any) -> None:
        if hasattr(body, "body"):
            self.body: list[Any] = list(body.body)
        else:
            self.body: list[Any] = body
        self.index: int = 0

    def addItem(self, item: Any) -> None:
        self.body.append(item)

    def getNext(self) -> Any:
        self.index += 1
        return self.body[self.index - 1]

    def resetNext(self) -> None:
        self.index = 0

    def hasNext(self) -> bool:
        return self.index < len(self.body)

    def isEmpty(self) -> bool:
        return len(self.body) == 0

    def size(self) -> int:
        return len(self.body)

    def length(self) -> int:
        return len(self.body)
    
    def __str__(self) -> str:
        s: str = str(self.body)
        s = sub(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)True([^a-zA-Z0-9\[{(+\-*/_\"\']+)", r"\1true\2", s)
        s = sub(r"^True([^a-zA-Z0-9\]})+\-*/_\"\']+)", r"true\1", s)
        s = sub(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)True$", r"\1true", s)
        s = sub(r"^True$", "true", s)
        s = sub(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)False([^a-zA-Z0-9\[{(+\-*/_\"\']+)", r"\1false\2", s)
        s = sub(r"^False([^a-zA-Z0-9\]})+\-*/_\"\']+)", r"false\1", s)
        s = sub(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)False$", r"\1false", s)
        s = sub(r"^False$", "false", s)
        s = sub(r"^\s*\[(.*)\]", r"{\1}", s)
        return s

class Stack:

    def __init__(self, body: Any) -> None:
        if hasattr(body, "body"):
            self.body: list[Any] = list(body.body)
        else:
            self.body: list[Any] = body
    
    def push(self, element) -> None:
        self.body.append(element)

    def pop(self) -> Any:
        return self.body.pop()

    def isEmpty(self) -> bool:
        return not len(self.body)

    def size(self) -> int:
        return len(self.body)

    def length(self) -> int:
        return len(self.body)

    def __str__(self) -> str:
        s: str = str(self.body)
        s = sub(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)True([^a-zA-Z0-9\[{(+\-*/_\"\']+)", r"\1true\2", s)
        s = sub(r"^True([^a-zA-Z0-9\]})+\-*/_\"\']+)", r"true\1", s)
        s = sub(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)True$", r"\1true", s)
        s = sub(r"^True$", "true", s)
        s = sub(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)False([^a-zA-Z0-9\[{(+\-*/_\"\']+)", r"\1false\2", s)
        s = sub(r"^False([^a-zA-Z0-9\]})+\-*/_\"\']+)", r"false\1", s)
        s = sub(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)False$", r"\1false", s)
        s = sub(r"^False$", "false", s)
        return s
    
class Queue:

    def __init__(self, body: Any) -> None:
        if hasattr(body, "body"):
            self.body: list[Any] = list(body.body)
        else:
            self.body: list[Any] = body
        self.end_index: int = 0
    
    def enqueue(self, element) -> None:
        self.body.append(element)

    def dequeue(self) -> Any:
        self.end_index += 1
        return self.body[self.end_index - 1]

    def isEmpty(self) -> bool:
        return (len(self.body) - self.end_index) <= 0

    def size(self) -> int:
        return len(self.body) - self.end_index

    def length(self) -> int:
        return len(self.body) - self.end_index

    def __str__(self) -> str:
        s: str = str(self.body)
        s = sub(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)True([^a-zA-Z0-9\[{(+\-*/_\"\']+)", r"\1true\2", s)
        s = sub(r"^True([^a-zA-Z0-9\]})+\-*/_\"\']+)", r"true\1", s)
        s = sub(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)True$", r"\1true", s)
        s = sub(r"^True$", "true", s)
        s = sub(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)False([^a-zA-Z0-9\[{(+\-*/_\"\']+)", r"\1false\2", s)
        s = sub(r"^False([^a-zA-Z0-9\]})+\-*/_\"\']+)", r"false\1", s)
        s = sub(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)False$", r"\1false", s)
        s = sub(r"^False$", "false", s)
        return s