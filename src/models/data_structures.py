from collections import deque

class Stack:
    def __init__(self):
        self._data = deque()

    def push(self, item):
        self._data.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._data.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)

    def get_all(self):
        # Retorna una lista en orden LIFO (último en entrar, primero en salir)
        return list(reversed(self._data))

class Queue:
    def __init__(self):
        self._data = deque()

    def enqueue(self, item):
        self._data.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._data.popleft()

    def peek(self):
        if self.is_empty():
            return None
        return self._data[0]

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)

    def get_all(self):
        # Retorna una lista en orden FIFO
        return list(self._data)

class CustomList:
    def __init__(self):
        self._data = []

    def append(self, item):
        self._data.append(item)

    def remove(self, item):
        if item in self._data:
            self._data.remove(item)
            return True
        return False

    def remove_by_id(self, identification_number):
        for i, affiliate in enumerate(self._data):
            if affiliate.identification_number == identification_number:
                del self._data[i]
                return True
        return False

    def find_by_id(self, identification_number):
        for affiliate in self._data:
            if affiliate.identification_number == identification_number:
                return affiliate
        return None

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)

    def get_all(self):
        return list(self._data)