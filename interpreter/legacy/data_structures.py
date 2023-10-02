from re import sub

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

    def size(self):
        return len(self.body)

    def length(self):
        return len(self.body)

    def __str__(self):
        s = str(self.body)
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

    def __init__(self, body):
        self.body = body

    def __getitem__(self, key):
        return self.body[key]

    def __setitem__(self, key, value):
        self.body[key] = value

    def __str__(self):
        s = str(self.body)
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

    def __init__(self, body):
        if hasattr(body, "body"):
            self.body = list(body.body)
        else:
            self.body = body
        self.index = 0

    def addItem(self, item):
        self.body.append(item)

    def getNext(self):
        self.index += 1
        return self.body[self.index - 1]

    def resetNext(self):
        self.index = 0

    def hasNext(self):
        return self.index < len(self.body)

    def isEmpty(self):
        return len(self.body) == 0

    def size(self):
        return len(self.body)

    def length(self):
        return len(self.body)
    
    def __str__(self):
        s = str(self.body)
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

    def __init__(self, body):
        if hasattr(body, "body"):
            self.body = list(body.body)
        else:
            self.body = body
    
    def push(self, element):
        self.body.append(element)

    def pop(self):
        return self.body.pop()

    def isEmpty(self):
        return not len(self.body)
    
    def size(self):
        return len(self.body)
    
    def length(self):
        return len(self.body)

    def __str__(self):
        s = str(self.body)
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

    def isEmpty(self):
        return (len(self.body) - self.end_index) <= 0
    
    def size(self):
        return len(self.body) - self.end_index
    
    def length(self):
        return len(self.body) - self.end_index

    def __str__(self):
        s = str(self.body)
        s = sub(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)True([^a-zA-Z0-9\[{(+\-*/_\"\']+)", r"\1true\2", s)
        s = sub(r"^True([^a-zA-Z0-9\]})+\-*/_\"\']+)", r"true\1", s)
        s = sub(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)True$", r"\1true", s)
        s = sub(r"^True$", "true", s)
        s = sub(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)False([^a-zA-Z0-9\[{(+\-*/_\"\']+)", r"\1false\2", s)
        s = sub(r"^False([^a-zA-Z0-9\]})+\-*/_\"\']+)", r"false\1", s)
        s = sub(r"([^a-zA-Z0-9\]})+\-*/_\"\']+)False$", r"\1false", s)
        s = sub(r"^False$", "false", s)
        return s