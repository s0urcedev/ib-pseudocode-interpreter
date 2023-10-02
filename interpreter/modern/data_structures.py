from typing import Any

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
        return str(self.body)

class Dictionary:

    def __init__(self, body: dict[Any, Any]) -> None:
        self.body: dict[Any, Any] = body

    def __getitem__(self, key: Any) -> Any:
        return self.body[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        self.body[key] = value

    def __str__(self) -> str:
        return str(self.body)

class Collection:

    def __init__(self, body: Any) -> None:
        if hasattr(body, "body"):
            self.body: list[Any] = list(body.body)
        else:
            self.body: list[Any] = body
        self.index: int = 0

    def add_item(self, item: Any) -> None:
        self.body.append(item)

    def get_next(self) -> Any:
        self.index += 1
        return self.body[self.index - 1]

    def reset_next(self) -> None:
        self.index = 0

    def has_next(self) -> bool:
        return self.index < len(self.body)

    def is_empty(self) -> bool:
        return len(self.body) == 0

    def size(self) -> int:
        return len(self.body)

    def length(self) -> int:
        return len(self.body)
    
    def __str__(self) -> str:
        return str(self.body)

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

    def is_empty(self) -> bool:
        return not len(self.body)

    def size(self) -> int:
        return len(self.body)

    def length(self) -> int:
        return len(self.body)

    def __str__(self) -> str:
        return str(self.body)
    
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

    def is_empty(self) -> bool:
        return (len(self.body) - self.end_index) <= 0

    def size(self) -> int:
        return len(self.body) - self.end_index

    def length(self) -> int:
        return len(self.body) - self.end_index

    def __str__(self) -> str:
        return str(self.body)