from skills import *

def scent_func(params):
    return lambda x, y, t: params['intensity']*np.exp( -(x-params['center'].coords[0])**2/(params['range']+1e-10) - (y-params['center'].coords[1])**2/(params['range']+1e-10))

class afield:
    def __init__(self,name:str,funct,parameters:dict,realm:str,is_perceptible:bool,is_transient:bool=True):
        self.name=name
        self.constructor=funct
        self.parameters=parameters
        self.realm=realm
        self.is_perceptible=is_perceptible
        self.is_transient=is_transient
    def __repr__(self):
        return self.name + "|r: "+ self.realm + '|p: ' + str(self.is_perceptible)
    def update_parameters(self,parameters):
        pass
    def evaluate(self,x,y,t):
        return self.constructor(self.parameters)(x,y,t)
    
class ascent(afield):
    def __init__(self, name:str, center:alocation, intensity, range, realm:str):
        super().__init__(name, scent_func, {'center':center,'intensity':intensity,'range':range}, realm, True)
    def update_parameters(self,extparameters):
        if type(extparameters) is alocation:
            self.parameters['center']=extparameters
            return
        self.parameters.update(extparameters)

NullField = afield('Null', lambda params: lambda x,y,t: 0,{},None,False,False)