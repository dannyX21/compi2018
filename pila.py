class Pila():
    def __init__ (self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if len(self.items) > 0:
            return self.items.pop()
        
        raise IndexError("La pila esta vacia")

    def __len__(self):
        return len(self.items)