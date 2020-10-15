class Table:
    def __init__(self, l, w, h):
        print('call table')
        self.length = l
        self.width = w
        self.height = h
 
class KitchenTable(Table):
    def __init__ (self, a,b):
        print('KT')
        self.a = a
        self.b =b

    def setPlaces(self, p):
        self.places = p
 
class DeskTable(Table):
    def square(self):
        return self.width * self.length

t = KitchenTable(123, 22)

print(t.__dict__)