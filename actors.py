from worlds import *

class anactor:
    def __init__(self,name: str,position: alocation,world:aworld,fields:list=[NullField]):
        self.name=name
        self.position=position
        self.fields=fields
        self.world = world
    def __repr__(self):
        return self.name+' at '+self.position.__repr__()
    def distance_to(self,other):
        return np.sqrt((self.position.coords[0]-other.position.coords[0])**2+(self.position.coords[1]-other.position.coords[1])**2)
    def upkeep(self):
        pass
    def act(self):
        pass

class anobject(anactor):
    def __init__(self, name:str, position:alocation, world:aworld, fields:list=[NullField]):
        super().__init__(name, position, world, fields)

class Food(anobject):
    def __init__(self, name: str, position: alocation, realm: str,feed:int, intensity: float, range:float, world:aworld):
        super().__init__(name, position, world, [ascent(name+"'s "+realm,position,intensity,range,realm)])
        self.feed=feed
    def get_eaten(self,buddy):
        print('Buddy ' + buddy.name + ' ate the ' + self.name+'!')
        for need in buddy.needs:
            need.satisfy('food_eaten',self.feed)

class adude(anactor):
    def  __init__(self,name: str,position: alocation,world:aworld,fields:list,personality,gauges={},skills=(),needs=()):
        super().__init__(name,position,world,fields)
        #Intrinsic Buddy Values
        self.personality=personality
        self.gauges=gauges
        self.skills=list(skills)
        self.needs=list(needs)
        self.permanent_personalities=[]
        self.field_constructors=[]
        self.logic = SimpleLogic()
        self.strategy = MultiSkill('Doing multiple things',0)

        #Transient Buddy Data
        self.percieves=[]
        self.queue=[]
        
        #Buddy physiology init
        self.gauges['Self Odor']=10
        self.field_constructors.append((lambda pos,t,y: ascent('Buddy '+self.name+"'s Scent",pos,y,y,'Buddy Scent'),'Self Odor'))
        self.gauges['Blood']=10
        self.field_constructors.append((lambda pos,t,y: ascent('Buddy '+self.name+"'s Blood's Scent", pos,y,y,'Blood Scent'),'Blood'))

        for constructor in self.field_constructors:
            self.fields.append(constructor[0](self.position,self.world.time,self.gauges[constructor[1]]))

        #Personality inheritance
        self.gauges.update(self.personality.gauges)
        self.needs+=personality.needs
        self.feeling=personality.default_state()
        self.skills += personality.skills
        personality.add_permanent(self)

    def __repr__(self):
        return "Buddy " + self.name + " at " + str(self.position) + " feeling " + self.feeling + " in " + self.world.name + "."
    
    def new_personality(self,newper):
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
        self.fields=[]
        for constructor in self.field_constructors:
            self.fields.append(constructor[0](self.position,self.world.time,self.gauges[constructor[1]]))
    
    def move(self,newp: alocation):
        self.position=newp
        print("Buddy " +self.name+' moved to '+newp.__repr__())

    def queue_action(self,skill):
        self.queue.insert(0,skill)

    def feel(self):
        considering=[]
        for need in self.needs[::-1]:
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
        percieved=[]
        for gauge_name in self.gauges.keys():
            #print(gauge_name)
            for field in self.world.give_perceptibles(gauge_name):
                #print(field)
                if field not in self.fields and field.evaluate(self.position.coords[0],self.position.coords[1],self.world.time)>self.gauges[field.realm]:
                    print("Buddy " +self.name+' percieves '+field.name)
                    percieved.append(field)
        self.percieves=percieved

    def act(self):
        self.strategy.action(self)
        self.queue=[]

    def satisfy_needs_automatic(self,kw:str):
        #Satisfies needs automatically based on need's associated gauge
        for need in self.needs:
            for param in need.parameter_names:
                if param in self.gauges.keys():
                    need.satisfy(kw,self.gauges[param])
    def satisfy_needs_specific(self,kw:str,times:int):
        #Satisfies needs a specific amount of times
        for need in self.needs:
            need.satisfy(kw,times)

    def get_eaten(self,buddy):
        print('Buddy ' + buddy.name + ' ate ' + self.name+'!')
        for need in buddy.needs:
            for param in need.parameter_names:
                if param in buddy.gauges.keys():
                    need.satisfy('buddy_eaten',buddy.gauges[param])

class SmartDude(adude):
    def __init__(self, name, position, world, fields, personality, gauges={}, skills=(), needs=()):
        super().__init__(name, position, world, fields, personality, gauges, skills, needs)
        self.logic=RandomMemoryLogic('Skill that worked from memory',0)