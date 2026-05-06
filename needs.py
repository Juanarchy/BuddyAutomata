from states import *
from winsound import Beep

class aneed:
    #A Need is an object that actors carry and usually want to satisfy.
    def __init__(self,name:str, yearns:str,default:astate,optimal:astate,critical:astate,actual:astate,satisfy_keyword:str,parameter_names:list):
        self.name=name                          #It has a name,
        self.yearns=yearns                      #a string that's passed when an actor with the need isn't in a state considered optimal,
        self.default_state=default              #a State object representing a default state,
        self.optimal_state=optimal              #a State object representing an optimal state,
        self.critical_state=critical            #a State object representing a critical state,
        self.actual_state=actual                #a State object representing the state of the actor that carries this need,
        self.satisfy_keyword=satisfy_keyword    #a keyword string used to identify actions which satisfy it,
        self.parameter_names=parameter_names    #and a list of gauge names that can be used when satisfying the need.
    def __repr__(self):
        return self.name + ': ' + self.actual_state + ' (Optimal: ' + self.optimal_state + ')' #It is represented as 'Name: actual_state (Optimal: optimal_state)
    
    def feel(self):                                                 #It has a method used by actors to feel the need.
        if self.actual_state.is_inferior_to(self.critical_state):   #If the actual state is considered inferior to the critical state, 
            return self.critical_state.name                         #it returns the name of the critical state.
        elif self.actual_state.is_inferior_to(self.optimal_state):  #And so on with the others...
            return self.default_state.name
        else:
            return self.optimal_state.name
        
    def is_satisfied(self):                                         #A method that returns true if the actual state is superior or equal to the optimal.
        return self.actual_state.is_superior_to(self.optimal_state) or self.actual_state.is_equal_to(self.optimal_state)
    def satisfy(self,kw:str,times:int):                             #And a method that, given a keyword string and a number of times,
        if self.satisfy_keyword in kw:                              #checks if the Need's keyword is contained in the given keyword
            for n in range(times):                                  
                self.actual_state.upgrade(1)                        #and upgrades the actual state the given number of times.

class adecayneed(aneed):
    #A Decay Need is a Need whose current state is downgraded a certain way (decay_data), when it is felt for a number of times (deltadecay)
    def __init__(self, name:str, yearns:str, default:astate, optimal:astate, critical:astate, actual:astate,satisfy_keyword:str,parameter_names:list, times4decay:int,decay_msg:str,decay_data):
        super().__init__(name, yearns, default, optimal, critical, actual,satisfy_keyword,parameter_names)
        self.deltadecay=times4decay
        self.decay_counter=0
        self.decay_msg=decay_msg
        self.decay_data=decay_data
    def feel(self):
        self.decay_counter+=1                           #Whenever the need is felt, it adds one to a counter.
        if self.decay_counter>=self.deltadecay:         #If the counter reaches the number needed for it to decay,
            self.decay_counter=0                        #the counter is reset,
            self.actual_state.decay(self.decay_data)    #the state is decayed,
            print('It feels '+self.decay_msg)           #prints a message representing the actor feels the state degrade,
            Beep(440,250)                               #and a beep is played.
        return super().feel()
    def satisfy(self, kw:str, times:int):
        self.decay_counter=0                            #Whenever the need is satisfied, the decay counter is also reset.
        return super().satisfy(kw, times)
