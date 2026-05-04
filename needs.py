from states import *
from winsound import Beep

class aneed:
    def __init__(self,name:str, yearns:str,default:astate,optimal:astate,critical:astate,actual:astate,satisfy_keyword:str,parameter_names:list):
        self.name=name
        self.yearns=yearns
        self.default_state=default
        self.optimal_state=optimal
        self.critical_state=critical
        self.actual_state=actual
        self.satisfy_keyword=satisfy_keyword
        self.parameter_names=parameter_names
    def __repr__(self):
        return self.name + ': ' + self.actual_state + ' (Optimal: ' + self.optimal_state + ')'
    def feel(self):
        if self.actual_state.is_inferior_to(self.critical_state):
            return self.critical_state.name
        elif self.actual_state.is_inferior_to(self.optimal_state):
            return self.default_state.name
        else:
            return self.optimal_state.name
    def is_satisfied(self):
        return self.actual_state.is_superior_to(self.optimal_state) or self.actual_state.is_equal_to(self.optimal_state)
    def satisfy(self,kw:str,times:int):
        if self.satisfy_keyword in kw:
            for n in range(times):
                self.actual_state.upgrade(1) 

class adecayneed(aneed):
    def __init__(self, name:str, yearns:str, default:astate, optimal:astate, critical:astate, actual:astate,satisfy_keyword:str,parameter_names:list, times4decay:int,decay_msg:str,decay_data):
        super().__init__(name, yearns, default, optimal, critical, actual,satisfy_keyword,parameter_names)
        self.deltadecay=times4decay
        self.decay_counter=0
        self.decay_msg=decay_msg
        self.decay_data=decay_data
    def feel(self):
        self.decay_counter+=1
        if self.decay_counter>=self.deltadecay:
            self.decay_counter=0
            self.actual_state.decay(self.decay_data)
            print('It feels '+self.decay_msg)
            Beep(440,250)
        return super().feel()
