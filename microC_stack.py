class Stack(object):
    def __init__(self):
        self.items = []

    def empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.empty() is False:
            return self.items.pop()
        else:
            print('Error: pop from empty stack')
            return None

    def top(self):
        if self.empty() is False:
            return self.items[len(self.items) - 1]
        else:
            print('Error: top from empty stack')
            return None

    def find(self, name, t):
        for i in range(len(self.items)):
            temp = self.items[-(i + 1)]  # notice: i start from 0 !!!
            if temp.get(name) and temp.get(name)[0] == t:
                return temp.get(name)
        return False

    def findInCurScope(self, name):
        temp = self.top()
        if temp.get(name) and temp.get(name)[0] == 'Var':
            return True
        return False

    def get_static_scope(self):
        return self.items[0]
