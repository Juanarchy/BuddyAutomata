class astate:
    def __init__(self,data,name):
        self.data=data
        self.name=name
    def is_inferior_to(self,other):
        pass
    def is_superior_to(self,other):
        pass
    def is_equal_to(self,other):
        pass
    def update(self,actor):
        pass
    def decay(self):
        pass
    def upgrade(self,data):
        pass

class anumstate(astate):
    def __init__(self, data,name):
        super().__init__(data,name)
    def is_inferior_to(self,other):
        return self.data < other.data
    def is_superior_to(self,other):
        return self.data > other.data
    def is_equal_to(self,other):
        return self.data == other.data
    def upgrade(self,data):
        self.data+=data
    def decay(self,data):
        self.data-=data

class Fullness(anumstate):
    def __init__(self, data, name):
        super().__init__(data,name)
    def __repr__(self):
        return '['+str(self.data)+'] '+self.name
    def fill(self,amount):
        self.data+=amount