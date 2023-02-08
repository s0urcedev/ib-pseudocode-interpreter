class Array:

    def __init__(self, body):
        if hasattr(body, "body"):
            self.body = list(body.body)
        else:
            self.body = body

    def __getitem__(self, index):
        return self.body[index]

    def __setitem__(self, index, value):
        while index >= len(self.body):
            self.body.append(None)
        self.body[index] = value

    def length(self) -> int:
        return len(self.body)

    def __str__(self):
        return str(self.body)

class Dictionary:

    def __init__(self, body):
        self.body = body

    def __getitem__(self, key):
        return self.body[key]

    def __setitem__(self, key, value):
        self.body[key] = value

    def __str__(self):
        return str(self.body)

class Collection:

    def __init__(self, body):
        if hasattr(body, "body"):
            self.body = list(body.body)
        else:
            self.body = body
        self.index = 0

    def add_item(self, item):
        self.body.append(item)

    def get_next(self):
        self.index += 1
        return self.body[self.index - 1]

    def reset_next(self):
        self.index = 0

    def has_next(self):
        return self.index < len(self.body)

    def is_empty(self):
        return len(self.body) == 0
    
    def __str__(self):
        return str(self.body)

class Stack:

    def __init__(self, body):
        if hasattr(body, "body"):
            self.body = list(body.body)
        else:
            self.body = body
    
    def push(self, element):
        self.body.append(element)

    def pop(self):
        return self.body.pop()

    def is_empty(self):
        return not len(self.body)

    def __str__(self):
        return str(self.body)
    
class Queue:

    def __init__(self, body):
        if hasattr(body, "body"):
            self.body = list(body.body)
        else:
            self.body = body
        self.end_index = 0
    
    def enqueue(self, element):
        self.body.append(element)

    def dequeue(self):
        self.end_index += 1
        return self.body[self.end_index - 1]

    def is_empty(self):
        return (len(self.body) - self.end_index) <= 0

    def __str__(self):
        return str(self.body)