from fields import *

class aworld:
    #A World is an object which contains all of the simulation's relevant data.
    def __init__(self,name:str,fields:list,grid:dict,time=0):
        self.name=name                                  #It has a name
        self.fields=fields                              #A list of inherent Fields
        self.grid=grid                                  #A grid object. Not yet implemented. Intended for use in physics simulation coupling (SWEpy for example).
        self.time=time                                  #A number representing time.
        self.perceptibles=[]                            #A list of perceptible Fields.
        self.actors=[]                                  #A list of actors.
        #When initialized, it populates the perceptibles list according to the Fields' perceptibility flags.
        for field in fields:
            if field.is_perceptible:
                self.perceptibles.append(field)

    def update_perceptibles(self):
        #Method to populate the list of perceptibles
        result=[]
        for field in self.fields:
            if field.is_perceptible:
                result.append(field)
        self.perceptibles=result
    
    def add_actor(self,actor):
        #Method to add an actor to the World
        self.actors.append(actor)
        for field in actor.fields:
            if field != NullField:
                #and its Fields to the World's Fields list.
                self.fields.append(field)
        #And update the perceptibles.
        self.update_perceptibles()

    def remove_actor(self,actor):
        #Method to remove an actor.
        self.actors.remove(actor)
        for field in actor.fields:
            if field in self.fields:
                self.fields.remove(field)
        self.update_perceptibles()

    def give_perceptibles(self,gauge_name):
        #Method that returns a list of perceptible Fields of a given realm.
        self.update_perceptibles()
        return [field for field in self.perceptibles if field.realm == gauge_name]
    
    def upkeep(self):
        #Method that performs an upkeep on the World, updating all of its actors and data.
        #It is intended to be used after an action that significantly affects the world, like a ConcreteSkill.
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
    
