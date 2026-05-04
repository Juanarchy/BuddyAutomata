from fields import *

class aworld:
    def __init__(self,name:str,fields:list,grid:dict,time=0):
        self.name=name
        self.fields=fields
        self.grid=grid
        self.time=time
        self.perceptibles=[]
        self.actors=[]
        for field in fields:
            if field.is_perceptible:
                self.perceptibles.append(field)
    
    def add_actor(self,actor):
        self.actors.append(actor)
        for field in actor.fields:
            if field != NullField:
                self.fields.append(field)

    def update_perceptibles(self):
        result=[]
        for field in self.fields:
            if field.is_perceptible:
                result.append(field)
        self.perceptibles=result

    def remove_actor(self,actor):
        self.actors.remove(actor)
        for field in actor.fields:
            if field in self.fields:
                self.fields.remove(field)
        self.update_perceptibles()

    def give_perceptibles(self,gauge_name):
        self.update_perceptibles()
        return [field for field in self.perceptibles if field.realm == gauge_name]
    
    def upkeep(self):
        newfields=[]
        for actor in self.actors:
            for field in actor.fields:
                self.fields.remove(field)
            actor.upkeep()
            for field in actor.fields:
                newfields.append(field)
        for field in self.fields:
            field.update_parameters({'time':self.time})
            newfields.append(field)
        self.fields=newfields
        self.update_perceptibles()
    
