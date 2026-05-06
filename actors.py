from worlds import *

class anactor:
    #An Actor is an object that represents something physical in a world.
    def __init__(self,name: str,position: alocation,world:aworld,fields:list=[NullField]):
        self.name=name          #It has a name,
        self.position=position  #a Location object position,
        self.fields=fields      #possibly fields for which it is their source
        self.world = world      #and the world it's inside.
    def __repr__(self):
        return self.name+' at '+self.position.__repr__()        #It's represented as  'Name at position'
    
    #It has a method that calculates its distance to other actors,
    def distance_to(self,other):
        return np.sqrt((self.position.coords[0]-other.position.coords[0])**2+(self.position.coords[1]-other.position.coords[1])**2)
    def upkeep(self): #a method that dictates how its upkept in time,
        pass
    def act(self):  #and a method that defines how it acts.
        pass

class anobject(anactor):
    #An Object is a type of actor
    def __init__(self, name:str, position:alocation, world:aworld, fields:list=[NullField]):
        super().__init__(name, position, world, fields)

class Food(anobject):
    #A Food is an Object that emits a particular Scent Field.
    def __init__(self, name: str, position: alocation, realm: str,feed:int, intensity: float, range:float, world:aworld):
        super().__init__(name, position, world, [ascent(name+"'s "+realm,position,intensity,range,realm)])
        self.feed=feed
    def get_eaten(self,buddy):                                      #It has a particular method that is executed when it is eaten, which
        print('Buddy ' + buddy.name + ' ate the ' + self.name+'!')
        amount=self.feed                                            
        if 'Fortify' in buddy.gauges.keys():
            amount+=buddy.gauges['Fortify']                         #determines an amount based on its 'feed' attribute and the 'Fortify' gauge of an actor,
        for need in buddy.needs:
            need.satisfy('food_eaten',amount)                       #sand satisfies needs with keywords contained in the string "food_eaten" by that amount.

class adude(anactor):
    #A Dude is an Actor representing a 'Buddy'. It's the main type of actor in the program.
    def  __init__(self,name: str,position: alocation,world:aworld,fields:list,personality,gauges={},skills=(),needs=()):
        super().__init__(name,position,world,fields)
        #Intrinsic Buddy Values
        self.personality=personality                                #It is initialized with a user-given Personality,
        self.gauges=gauges                                          #a user-given dictionary of Gauges; entries that represent the Buddy's 'intrinsic' data, like abilities, senses, and physiology.
        self.skills=list(skills)                                    #a user-given list of Skills
        self.needs=list(needs)                                      #a user-given list of Needs
        self.permanent_personalities=[]                             #a list of permanent personalities
        self.field_constructors=[]                                  #a list of Field constructors; tuples in the form (function of position, time, and Y that returns a Field object associated to that data; name of the Gauge that contains Y)
                                                                    # Field constructors are necessary because a Field's parameters dictionary is static.
        self.logic = SimpleLogic()                                  #a Logic that defaults to SimpleLogic
        self.strategy = DefaultStrategy()       #a Strategy that defaults to MultiSkill

        #Transient Buddy Data
        self.percieves=[]                                           #a list of Fields the Buddy can percieve
        self.queue=[]                                               #a queue of skills the Buddy wants to use, in most- to least-mportant order.
        
        #Buddy physiology init
        #The buddy is initialized with a Self Odor level of 10, and a field constructor used to construct a Scent Field centered in that position, with a range and intensity equal to the Self Odor gauge.
        self.gauges['Self Odor']=10
        self.field_constructors.append((lambda pos,t,y: ascent('Buddy '+self.name+"'s Scent",pos,y,y,'Buddy Scent'),'Self Odor'))
        #And a Blood amount of 10, with a field constructor that makes the associated Blood Scent field.
        self.gauges['Blood']=10
        self.field_constructors.append((lambda pos,t,y: ascent('Buddy '+self.name+"'s Blood's Scent", pos,y,y,'Blood Scent'),'Blood'))

        #Then its list of fields is populated by constructing those fields.
        for constructor in self.field_constructors:
            self.fields.append(constructor[0](self.position,self.world.time,self.gauges[constructor[1]]))

        #Personality inheritance
        #Lastly, the relevant fields are populated with data contained in the Buddy's personality.
        self.gauges.update(self.personality.gauges)
        self.needs+=personality.needs                   #It is important to note that the Needs list order is important: it is assumed to be highest to lowest priority.
        self.feeling=personality.default_state()
        self.skills += personality.skills
        personality.add_permanent(self)

    def __repr__(self):
        return "Buddy " + self.name + " at " + str(self.position) + " feeling " + self.feeling + " in " + self.world.name + "."
        #Buddies are represented as "Buddy Name at Position feeling X in world name"
    
    def new_personality(self,newper):
        #Buddies have a method that updates them when they acquire a new personality.
        self.personality=newper

        self.skills.reverse()
        newper.specific_skills.reverse()
        self.skills.extend(newper.specific_skills)
        self.skills.reverse()
        newper.specific_skills.reverse()
        
        self.needs.reverse()
        newper.specific_needs.reverse()
        self.needs.extend(newper.specific_needs)
        self.needs.reverse()
        newper.specific_needs.reverse()

        self.gauges.update(newper.specific_gauges)

        newper.add_permanent(self)

        self.feeling=newper.default_state()
        
    
    def upkeep(self):
        #Their upkeep function updates their list of Fields based on their constructors.
        #  Note that the list of Fields is cleared, so buddies can only have Fields provided by constructors.
        self.fields=[]
        for constructor in self.field_constructors:
            self.fields.append(constructor[0](self.position,self.world.time,self.gauges[constructor[1]]))
    
    def move(self,newp: alocation):
        #Method that moves Buddy to a Location and announces it.
        self.position=newp
        print("Buddy " +self.name+' moved to '+newp.__repr__())

    def queue_action(self,skill):
        #Method that queues a skill action
        self.queue.insert(0,skill)

    def feel(self):
        #Method that performs the feel method for each of the Buddy's Needs, deduces a Skill according to their Logic to be considered if the Need is not satisified, 
        # chooses which Skills to perform according to their Logic, and queues them. The Needs list is ran in order, so the first Skill in the considering list is 
        # always related to the highest priorty unsatisfied need.
        considering=[]
        for need in self.needs:
            feeling=need.feel()
            print("Buddy " +self.name+' feels '+feeling+'.')
            self.feeling=feeling
            if not need.is_satisfied():
                print("Buddy " +self.name+' wants to be '+ need.yearns+'.')
                skill=self.logic.deduce_skill(self,need)
                if skill is not None:
                    print('Buddy '+self.name+' thinks it should '+skill.name+'.')
                    considering.append(skill)
        chosen=self.logic.apply_logic(considering)
        for skill in chosen:
            self.queue_action(skill)

    def sense(self):
        #Method that populates the percieved Fields list based on the buddy's gauge that represents the threshold over which a field is considered to be percieved.
        percieved=[]
        for gauge_name in self.gauges.keys(): #for each of the Buddy's gauges
            #print(gauge_name)
            for field in self.world.give_perceptibles(gauge_name): #and for each perceptible field in the world
                #print(field)
                #if the field is not own, and the evaluation of the field at the Buddy's position and time is greater than the Buddy's threshold to that field's realm
                if field not in self.fields and field.evaluate(self.position.coords[0],self.position.coords[1],self.world.time)>self.gauges[field.realm]:
                    print("Buddy " +self.name+' percieves '+field.name)
                    percieved.append(field) #the field is added to the percieved fields list.
        self.percieves=percieved

    def act(self):
        #Method that applies the Buddy's Strategy to the Buddy's queue, performing a number of skills in it, and clears it (regardless of its contents afterwards).
        #Note that the default strategy is to only perform the first skill of the queue.
        self.strategy.action(self)
        self.queue=[]

    def satisfy_needs_automatic(self,kw:str):
        #Satisfies needs automatically based on need's associated gauge, given a keyword.
        for need in self.needs:
            for param in need.parameter_names:
                if param in self.gauges.keys():
                    need.satisfy(kw,self.gauges[param])
    def satisfy_needs_specific(self,kw:str,times:int):
        #Satisfies needs a specific amount of times, using given keyword
        for need in self.needs:
            need.satisfy(kw,times)

    def get_eaten(self,buddy):
        #method to be performed when Buddy becomes eaten by some actor (usually another Buddy).
        print('Buddy ' + buddy.name + ' ate ' + self.name+'!')
        for need in buddy.needs:
            for param in need.parameter_names:
                if param in buddy.gauges.keys():
                    need.satisfy('buddy_eaten',buddy.gauges[param])

class SmartDude(adude):
    #A smart dude is a dude whose Logic is RandomMemoryLogic, and Strategy is MultiSkill. This should really be reworked to depend on personality...
    def __init__(self, name, position, world, fields, personality, gauges={}, skills=(), needs=()):
        super().__init__(name, position, world, fields, personality, gauges, skills, needs)
        self.logic=RandomMemoryLogic('Skill that worked from memory',0)
        self.strategy=MultiSkill('Do multiple based on stamina',0)