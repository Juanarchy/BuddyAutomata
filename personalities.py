from needs import *
from actors import *

class apersonality:
    #A Personality is an object actors use that grants them needs and skills.
    #Their attributes and methods are:
    def __init__(self,name:str,specific_gauges:dict={},specific_skills:list=[],specific_needs:list=[]):
        self.name=name                          #its name, a string
        self.state_word='new'                   #its state word, a string representing the feeling of a new actor with the personality
        self.gauges={}                          #a dictionary of its final associated gauges, composed of its specific gauges and all that it inherits
        self.specific_gauges=specific_gauges    #a dictionari of its specific associated gauges as a subclass
        self.skills=[]                          #a list of its final associated skills
        self.specific_skills=specific_skills    #its specific skills as a subclass
        self.needs=[]                           #its final associated needs
        self.specific_needs=specific_needs      #its specific skills as a subclass

    def attach_specifics_higher(self):          #a method used by subclasses used during initialization to attach their specifics to their final attributes at a higher priority

        self.skills.reverse()
        self.specific_skills.reverse()
        self.skills.extend(self.specific_skills)
        self.skills.reverse()
        self.specific_skills.reverse()
        
        self.needs.reverse()
        self.specific_needs.reverse()
        self.needs.extend(self.specific_needs)
        self.needs.reverse()
        self.specific_needs.reverse()

        self.gauges.update(self.specific_gauges)
    
    
    def attach_specifics_lower(self):           #analogous, but at a lower priority

        self.skills.extend(self.specific_skills)
        
        self.needs.extend(self.specific_needs)

        self.gauges.update(self.specific_gauges)

    def default_state(self):                    #a method that returns a personality's state word (kinda useless tbh)
        return self.state_word
    def add_permanent(self,buddy:adude):        #a method that does nothing if the personality isn't permanent, and adds it if it is, used during actor initialization
        pass

class Glutton(apersonality):
    #A Glutton is a personality that provides an actor with: 
    # - a 'Sweetness' gauge that determines the threshold over which the actor can detect a 'Sweetness' field.
    # - a search-based Concrete Skill that makes the user move closer to and try to eat foods that emit a Sweetness field, and its associated search skill.
    # - a Need called 'Hunger' that improves when the user completes an action that includes the keyword 'eaten', whose...
    #   ... satisfaction is enhanced if the user has the 'Fortify' gauge by its amount.
    def __init__(self, name):
        super().__init__(name)
        self.specific_gauges={'Sweetness':0}
        self.specific_skills=[SearchNearbyEat('Search and eat',{'eat_radius':1,'eatable_types':[Food],'appetizing_realms':['Sweetness']}),Radius2DSearch('Search Sweeter',{'realm':'Sweetness','radius':1,'nsamples':32,'maximize':True})]
        self.specific_needs=[aneed('Hunger','fuller',Fullness(50,'hungry'),Fullness(90,'full'),Fullness(10,'starving'),Fullness(50,'actual'),'eaten',['Fortify'])]
        self.attach_specifics_higher()
    
class Cannibal(Glutton):
    #A Cannibal is a Glutton who can percieve Buddies' scents based on the threshold given by a gauge, and eat them, filling its hunger an amount determined by its 'Cannibalism' gauge.
    def __init__(self, name):
        super().__init__(name)
        self.specific_gauges={'Cannibalism':15,'Buddy Scent':0}
        self.specific_skills=[Radius2DSearch('Search Buddy',{'realm':'Buddy Scent','radius':1,'nsamples':32,'maximize':True})]
        self.specific_needs=[]
        self.needs[0].parameter_names.append('Cannibalism')
        self.skills[0].update_parameters({'eatable_types':[Food,adude],'appetizing_realms':['Sweetness','Buddy Scent']})
        self.attach_specifics_lower()

class Vampire(Glutton):
    #An actor who is a Vampire is a Glutton with a particular desire who:
    # - Can percieve the scent of their desire emanating from other actors, such as blood from buddies.
    # - Can search and try to get closer to sources of their desire.
    # - Can drain actors of what they desire and turn them into the same kind of vampire they are.
    # - Has a decaying need that is satisfied when they drain others of their desire, by an amount related to their 'vampiric_desire lust' gauge.
    # - Has its vampirism as a permanent personality, meaning that if change personality, the vampirism will persist.
    def __init__(self, vampiric_desire:str):
        super().__init__(vampiric_desire+' Vampire')
        self.vampiric_desire=vampiric_desire
        self.specific_gauges={vampiric_desire+'lust':15,vampiric_desire+' Scent':0,vampiric_desire:0}
        self.specific_skills=[Radius2DSearch('Search '+vampiric_desire,{'realm':vampiric_desire+' Scent','radius':1,'nsamples':32,'maximize':True}),SearchNearbyDrain('Search and drain '+vampiric_desire,{'drainable_types':[adude],'desired_gauge':vampiric_desire,'drain_radius':1})][::-1]
        self.specific_needs=[adecayneed(vampiric_desire+' vampirism','more full of '+vampiric_desire,Fullness(50,'thirsty for '+vampiric_desire),Fullness(90,'full of '+vampiric_desire),Fullness(10,vampiric_desire+'-deprived'),Fullness(80,'actual'),vampiric_desire+'_drained',[vampiric_desire+'lust'],10,'a greater thirst for '+vampiric_desire+'!',1)]
        self.state_word='thirsty for '+vampiric_desire
        self.attach_specifics_higher()
    def add_permanent(self, buddy):
        buddy.permanent_personalities.append(self)

class Gooner(apersonality):
    #An actor who is a Gooner has a need called 'Arousal' that improves when the user performs an action containing the 'goon' keyword, and has a skill to do that.
    #This is a joke personality requested by my friend Soni.
    def __init__(self, name, specific_gauges = {}, specific_skills = [], specific_needs = []):
        super().__init__(name, specific_gauges, specific_skills, specific_needs)
        self.specific_gauges={'Gooning':10}
        self.specific_skills=[Goon('Goon',0)]
        self.specific_needs=[adecayneed('Arousal', 'aroused',Fullness(50,'triggered'),Fullness(90,'about to cum'),Fullness(10,'urged'),Fullness(50,'actual'),'goon',['Gooning'],1,'like gooning',5)]
        self.state_word='the absence of its Waifu'
        self.attach_specifics_higher()
    def add_permanent(self, buddy):
        buddy.permanent_personalities.append(self)