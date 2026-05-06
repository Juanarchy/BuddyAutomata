from skills import *

####### CONSTRUCTORS OF FIELD FUNCTIONS ########

#A constructor of a field function is a function that takes the parameters dictionary of
# the Field and returns a *function* of coordinates x and y, and time t which, when 
# evaluated at some coordinates and time, returns a scalar.

#Not to be confused with Field constructors, which are tuples used by Dudes to
# construct Field *objects*.

#In mathematical notation, if the reader shall allow:

# - Field constructor: (f,str): Tuple

#                            f: alocation x float x any ---> afield
#                                          (loc,t,data) |--> f(loc,t,data) = afield(...)

# - Constructor of field function: F: funct

#                                F: dict ---> funct
#                                     D  |--> F(D) = f: float x float x float ---> float
#                                                               (x,y,t)       |--> f(x,y,t) = result

#For example, the scent function:

def scent_func(params):
    return lambda x, y, t: params['intensity']*np.exp( -(x-params['center'].coords[0])**2/(params['range']+1e-10) - (y-params['center'].coords[1])**2/(params['range']+1e-10))

#Takes in a dictionary that contains keys 'intensity', 'center', and 'range'
# and returns a real valued function of 3 variables which is a 2 dimensional Gaussian distribution
# centered at 'center' (a Location object), modulated by the 'intensity', and shaped by the 'range', i.e.,
# it attains its max=params['intensity'] at x=params['center'].coords[0], y=params['center'].coords[1],
# and has variance sigma^2=(params[range]+1e-10)/2 (the small residual is used to control division by zero).

################################################

class afield:
    #A Field is an object that represents a mathematical field in a world.
    def __init__(self,name:str,funct:function,parameters:dict,realm:str,is_perceptible:bool,is_transient:bool=True):
        self.name=name                      #It has a name
        self.constructor=funct              #a function constructor (as described above)
        self.parameters=parameters          #a dictionary of parameters
        self.realm=realm                    #a string that defines its 'realm' (like sweetness, odor, etc.)
        self.is_perceptible=is_perceptible  #a boolean that conveys if it should be perceptible
        self.is_transient=is_transient      #and a boolean representing if it's transient (deprecated)
    def __repr__(self):
        return self.name + "|r: "+ self.realm + '|p: ' + str(self.is_perceptible) #it's represented as 'Name|r: realm|p: is_perceptible'
    def update_parameters(self,parameters):     #it has a method that updates the parameters dictionary
        self.parameters.update(parameters)

    def evaluate(self,x,y,t):                               #and  a method that returns the field function evaluated at x,y,t
        return self.constructor(self.parameters)(x,y,t)
    
class ascent(afield):
    #A Scent is a perceptible Field of some realm that has a function constructor given by scent_funct and parameters 'center', 'intensity' and 'range'.
    def __init__(self, name:str, center:alocation, intensity, range, realm:str):
        super().__init__(name, scent_func, {'center':center,'intensity':intensity,'range':range}, realm, True)
    def update_parameters(self,extparameters):
        #it has a simplified way of updating if given a location
        if type(extparameters) is alocation:
            self.parameters['center']=extparameters
            return
        self.parameters.update(extparameters)

#The null field is an imperceptible Field that's 0 everywhere, always.
NullField = afield('Null', lambda params: lambda x,y,t: 0,{},None,False,False)

#Note the way to easily create a field function constructor: lambda params: lambda x,y,t: (some expression depending on x,y,t).
#This means an equivalent definition for scent_func would be

#scent_func = lambda parameters: lambda x,y,t: params['intensity']*...