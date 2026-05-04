import numpy as np

class alocation:
    def __init__(self,coords,world,options=[],name=None):
        self.coords=coords if type(coords) is np.array else np.array(coords)
        if name is not None:
            self.name=name
        self.options=options
        self.world=world
    
    def __repr__(self):
        if hasattr(self,"name"):
            return self.name+' | '+f'({self.coords[0]:.2f},{self.coords[1]:.2f})'
        else:
            return f'({self.coords[0]:.2f},{self.coords[1]:.2f})'