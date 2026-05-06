class astate:
    #A State is an object that represents a state of something, it was designed to be as abstract a representation could be.
    def __init__(self,data,name):
        self.data=data              #It has some data,
        self.name=name              #and a name.
    def is_inferior_to(self,other): #It has methods to determine if the state is inferior,
        pass
    def is_superior_to(self,other): #superior,
        pass
    def is_equal_to(self,other):    #or equal to another.
        pass
    def update(self,actor):         #It has a method to update the state it represents,
        pass
    def decay(self):                #to downgrade it,
        pass
    def upgrade(self,data):         #or to upgrade it.
        pass

class anumstate(astate):                #A NumState is a State represented by a number.
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

class Fullness(anumstate):             #A Fullness is a NumState that represents how full something is.
    def __init__(self, data, name):
        super().__init__(data,name)
    def __repr__(self):
        return '['+str(self.data)+'] '+self.name
    def fill(self,amount):
        self.data+=amount