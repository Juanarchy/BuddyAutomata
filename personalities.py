from needs import *
from actors import *

class apersonality:
    def __init__(self,name:str,specific_gauges:dict={},specific_skills:list=[],specific_needs:list=[]):
        self.name=name
        self.state_word='new'
        self.gauges={}
        self.specific_gauges=specific_gauges
        self.skills=[]
        self.specific_skills=specific_skills
        self.needs=[]
        self.specific_needs=specific_needs
    def attach_specifics_higher(self):

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
    
    
    def attach_specifics_lower(self):

        self.skills.extend(self.specific_skills)
        
        self.needs.extend(self.specific_needs)

        self.gauges.update(self.specific_gauges)

    def default_state(self):
        return self.state_word
    def add_permanent(self,buddy:adude):
        pass

class Glutton(apersonality):
    def __init__(self, name):
        super().__init__(name)
        self.specific_gauges={'Sweetness':0}
        self.specific_skills=[SearchNearbyEat('Search and eat',{'eat_radius':1,'eatable_types':[Food],'appetizing_realms':['Sweetness']}),Radius2DSearch('Search Sweeter',{'realm':'Sweetness','radius':1,'nsamples':32,'maximize':True})]
        self.specific_needs=[aneed('Hunger','fuller',Fullness(50,'hungry'),Fullness(90,'full'),Fullness(10,'starving'),Fullness(50,'actual'),'eaten',['Fortify'])]
        self.attach_specifics_higher()
    
class Cannibal(Glutton):
    def __init__(self, name):
        super().__init__(name)
        self.specific_gauges={'Cannibalism':15,'Buddy Scent':0}
        self.specific_skills=[Radius2DSearch('Search Buddy',{'realm':'Buddy Scent','radius':1,'nsamples':32,'maximize':True})]
        self.specific_needs=[]
        self.skills[0].update_parameters({'eatable_types':[Food,adude],'appetizing_realms':['Sweetness','Buddy Scent']})
        self.attach_specifics_lower()

class Vampire(Glutton):
    def __init__(self, vampiric_desire:str,yearn:str):
        super().__init__(vampiric_desire+' Vampire')
        self.vampiric_desire=vampiric_desire
        self.yearn = yearn
        self.specific_gauges={vampiric_desire+'lust':15,vampiric_desire+' Scent':0,vampiric_desire:0}
        self.specific_skills=[Radius2DSearch('Search '+vampiric_desire,{'realm':vampiric_desire+' Scent','radius':1,'nsamples':32,'maximize':True}),SearchNearbyDrain('Search and drain '+vampiric_desire,{'drainable_types':[adude],'desired_gauge':vampiric_desire,'drain_radius':1})][::-1]
        self.specific_needs=[adecayneed(vampiric_desire+' vampirism',yearn,Fullness(50,'thirsty for '+vampiric_desire),Fullness(90,'full of '+vampiric_desire),Fullness(10,vampiric_desire+'-deprived'),Fullness(80,'actual'),vampiric_desire+'_drained',[vampiric_desire+'lust'],10,'a greater thirst for '+vampiric_desire+'!',1)]
        self.state_word='thirsty for '+vampiric_desire
        self.attach_specifics_higher()
    def add_permanent(self, buddy):
        buddy.permanent_personalities.append(self)

class Gooner(apersonality):
    def __init__(self, name, specific_gauges = {}, specific_skills = [], specific_needs = []):
        super().__init__(name, specific_gauges, specific_skills, specific_needs)
        self.specific_gauges={'Gooning':10}
        self.specific_skills=[Goon('Goon',0)]
        self.specific_needs=[adecayneed('Arousal', 'aroused',Fullness(50,'triggered'),Fullness(90,'about to cum'),Fullness(10,'urged'),Fullness(50,'actual'),'goon',['Gooning'],1,'like gooning',5)]
        self.state_word='the absence of its Waifu'
        self.attach_specifics_higher()
    def add_permanent(self, buddy):
        buddy.permanent_personalities.append(self)