from locations import *
import winsound as ws
from copy import deepcopy
rng = np.random.default_rng()

class askill:
    #A skill is a parametrized object that can be available to actors and is related to how they act.
    def __init__(self,name:str,parameters:dict):
        self.name=name                  #it has a name string
        self.parameters=parameters      #and a dictionary of parameters
    def action(self,buddy,top=True):    #It has a method that determines how an actor acts when performing the skill
        pass
    def update_parameters(self, parameters): #And a way to update the parameters dictionary.
        self.parameters.update(parameters)

class Goon(askill):
    #A simple skill that satisfies needs looking for the 'goon' keyword
    def __init__(self, name, parameters):
        super().__init__(name, parameters)
    def action(self, buddy, top=True):
        buddy.satisfy_needs_automatic('goon')
        print('Buddy '+buddy.name+' gooned for a while.')
        return True

class asensing(askill):
    #A Sensing is a Skill which, on action, returns some data related to an actor.
    def __init__(self, name, parameters):
        super().__init__(name, parameters)
    def action(self, buddy, top=True):
        data:any
        return data

class asearch(asensing):
    #A search is a Sensing that, on action, returns a position with a desirable quality.
    def __init__(self, name, parameters):
        super().__init__(name, parameters)
    def action(self, buddy, top=True):
        quality:any
        return buddy.position,quality
    
class Radius2DSearch(asearch):
    #On action returns a position maximizing or minimizing the superposition of fields of some realm via random search of with a number nsamples^2 of samples in a circle of some radius.
    def __init__(self, name, parameters={'realm':None,'radius':0,'nsamples':10,'maximize':True}):
        super().__init__(name, parameters)
    def action(self,buddy,top=True):
        interest = self.parameters['realm']

        #Failing to detect field of chosen realm
        if interest not in [field.realm for field in buddy.percieves]:
            print("Buddy " +buddy.name+" can't feel any "+interest)
            return buddy.position,0
        
        #Collecting percieved fields of chosen realm
        interesting_fields = [field for field in buddy.percieves if field.realm==interest]

        #Random circular search centered at buddy
        center = buddy.position.coords
        radius = self.parameters['radius']
        nsamples = self.parameters['nsamples']
        mat=rng.random((nsamples,2))
        theta=2*np.pi*mat[:,0]
        r=mat[:,1]*radius
        deltax=r*np.cos(theta)
        deltay=r*np.sin(theta)
        xlines=center[0]+deltax
        ylines=center[1]+deltay
        #Build intersection mesh for lines x=xlines, y=ylines, to be used as evaluation coordinates
        xsearch,ysearch = np.meshgrid(xlines,ylines,indexing='xy')
        xsearch,ysearch = xsearch.flatten(),ysearch.flatten()
        #Evaluate sum of fields if there's more than one
        evalu=np.sum(np.array([field.evaluate(xsearch,ysearch,buddy.world.time) for field in interesting_fields]),axis=0) if len(interesting_fields)>1 else interesting_fields[0].evaluate(xsearch,ysearch,buddy.world.time)
        #Location of most optimal place in sample
        ind = np.argmax(evalu) if self.parameters['maximize'] else np.argmin(evalu)
        xfound = xsearch[ind]
        yfound = ysearch[ind]
        newl = alocation((xfound,yfound),buddy.world)

        return newl,evalu[ind]

class aconcreteskill(askill):
    #A ConcreteSkill is a Skill that, on an action considered successful, has results requiring a world upkeep. Returns a boolean representing if it succeeded.
    def __init__(self, name, parameters):
        super().__init__(name, parameters)
    def action(self, buddy, top=True):
        worked:bool

        #Stuff

        if worked:
            buddy.world.upkeep()
        
        return worked

class SearchNearbyDrain(aconcreteskill):
    #On success, buddy either drains a target, or moves closer to where it thinks there could be one.
    def __init__(self, name, parameters:dict={'drainable_types':[],'desired_gauge':'','drain_radius':0.0}):
        super().__init__(name, parameters)

    def action(self, buddy, top=True):
        worked=False
        #Buddy looks at actors that are drainable. If there's one inside its eat radius, buddy drains it and converts actor to buddy's relevant vampirism
        for actor in buddy.world.actors:
            if actor is not buddy and isinstance(actor,tuple(self.parameters['drainable_types'])) and hasattr(actor,'gauges') and self.parameters['desired_gauge'] in actor.gauges.keys() and actor.gauges[self.parameters['desired_gauge']]>0 and buddy.distance_to(actor)<=self.parameters['drain_radius']:
                print('Buddy '+buddy.name+' spots '+actor.name)
                print('Buddy '+buddy.name+' bites '+actor.name+' and drains its '+self.parameters['desired_gauge']+'!')
                buddy.satisfy_needs_specific(self.parameters['desired_gauge']+'drained_eaten',actor.gauges[self.parameters['desired_gauge']])
                actor.gauges[self.parameters['desired_gauge']]=0
                new_vampirism=next((personality for personality in buddy.permanent_personalities if (hasattr(personality,'vampiric_desire') and personality.vampiric_desire==self.parameters['desired_gauge'])),buddy.personality)
                print(actor.name+' becomes a '+ new_vampirism.name+'!')
                actor.new_personality(type(new_vampirism)(new_vampirism.vampiric_desire))
                ws.Beep(220,500)
                buddy.world.upkeep()
                worked=True
                return worked
        print('Buddy '+buddy.name+ " tries to move closer to "+self.parameters['desired_gauge'].lower()+".")
        maxscent=0
        chosenloc=buddy.position

        #Using each search skill in the relevant realm, it chooses the one producing the highest intensity
        for skill in buddy.skills:
            if isinstance(skill,asearch) and 'realm' in skill.parameters.keys() and self.parameters['desired_gauge'].lower()+' scent' in skill.parameters['realm'].lower():
                potloc,potscent=skill.action(buddy,False)
                if potscent>=maxscent:
                    maxscent=potscent
                    chosenloc=potloc
        
        if maxscent>0:
            buddy.move(chosenloc)
            buddy.world.upkeep()
            worked=True
        
        return worked

class SearchNearbyEat(aconcreteskill):
    #On success, buddy either eats a target, or moves closer to where it thinks there could be one.
    def __init__(self, name, parameters:dict={'eatable_types':[],'eat_radius':0.0,'appetizing_realms':[]}):
        super().__init__(name, parameters)
    def action(self,buddy,top=True):
        worked=False
        #Buddy looks at actors that are eatable. If there's one inside its eat radius, it eats it and the action is considered successful.
        for actor in buddy.world.actors:
            if actor is not buddy and isinstance(actor,tuple(self.parameters['eatable_types'])) and buddy.distance_to(actor)<=self.parameters['eat_radius']:
                print('Buddy '+buddy.name+' spots '+actor.name)
                actor.get_eaten(buddy)
                ws.Beep(880,500)
                buddy.world.remove_actor(actor)
                buddy.world.upkeep()
                worked=True
                return worked
        #Buddy uses its search skills to move closer to food
        print('Buddy '+buddy.name+ " tries to move closer to food.")
        maxscent=0
        chosenloc=buddy.position

        #Using each search skill, it chooses the one producing the highest intensity
        for skill in buddy.skills:
            if isinstance(skill,asearch) and 'realm' in skill.parameters.keys() and skill.parameters['realm'] in self.parameters['appetizing_realms']:
                potloc,potscent=skill.action(buddy,False)
                if potscent>=maxscent:
                    maxscent=potscent
                    chosenloc=potloc
        
        #If the max field value found is significantly nonzero, the action is considered successful and buddy moves to the chosen location.
        if abs(maxscent)>1e-15:
            buddy.move(chosenloc)
            buddy.world.upkeep()
            worked=True
        
        return worked
    
class alogic(askill):
    #A Logic is a Skill that links Needs to other Skills (deduce_skill), filters skills to perform (apply_logic), and evaluates performed skills.
    def __init__(self, name, parameters):
        super().__init__(name, parameters)
    def action(self,buddy,top=True):
        pass
    def deduce_skill(self,buddy,need):
        return buddy.skills[0]
    def evaluate_result(self,buddy,skill):
        return skill.action(buddy)
    def apply_logic(self,considering):
        if len(considering)>0:
            return [considering[0]]
        else:
            return []
    
class SimpleLogic(alogic):
    #The simplest possible Logic; always chooses first Skill in Skill list.
    def __init__(self):
        super().__init__('Choose First', 0)

class RandomMemoryLogic(alogic):
    #Logic that keeps a record of Needs that have been satisfied by a Skill and wether those Skills worked last time they were performed.
    #Prioritizes Skills known to work, over random unknown Skills, over Skills known not to work.
    #If a Need is satisfied, it doesn't suggest its known useful Skill.
    #When a random Skill is selected, it focuses on testing it.

    #IMPORTANT DISCLAIMER: this Logic saves Skill objects in its memory. A more future-proof way of doing this would be to save Skill name strings to search among the actor's
    # Skills. This way it would be 100% compatible with skills that might change their parameters. I haven't tested wether this Logic's memory is truly dynamic or not.
    # Perhaps it could have a way to update its memory using the buddy's Skills list.
    def __init__(self, name, parameters):
        super().__init__(name, parameters)
        self.memory={}
        self.target_skill=None
    def deduce_skill(self, buddy, need):
        #When deducing a Skill based on a need:
        #If Need is satisfied, returns None
        if need.is_satisfied():
            print("It doesn't think it should do anything about that.")
            return None
        #If it knows a Skill that worked, returns that
        if need.name in self.memory.keys() and self.memory[need.name][1]:
            skill=self.memory[need.name][0]
            print('It recalls doing '+skill.name+' worked.')
            return skill
        #Otherwise returns a skill it's testing, a random unknown skill if there's any left, or a random one if there isn't
        else:
            if self.target_skill is not None:
                skill = self.target_skill
                print("It's trying to see if "+skill.name+' works for something.')
                return skill
            
            knowns=[row[0] for row in self.memory.values()]
            unknowns=[skill for skill in buddy.skills if isinstance(skill,(aconcreteskill)) and skill not in knowns]
            if len(unknowns)>0 and self.target_skill is None:
                skill=rng.choice(unknowns,shuffle=False)
                print("It hasn't tried doing "+skill.name+", maybe that'll work.")
                self.target_skill=skill
                return skill
            else:
                skill=rng.choice(knowns)
                print("Nothing has worked, maybe doing "+skill.name+" will work.")
                return skill
    def evaluate_result(self,buddy,skill):
        #If skill is known, it executes and saves wether it worked
        for tup in self.memory.values():
            if skill==tup[0]:
                worked = skill.action(buddy)
                tup[1] = worked
                return worked
        #otherwise, checks if needs after execution are more satisfied
        needs_before=deepcopy({need.name:need.actual_state for need in buddy.needs}) #dictionary with keys=names of needs before execution, values=state of need before execution
        worked=skill.action(buddy)
        needs_after=deepcopy({need.name:need.actual_state for need in buddy.needs if need.name in needs_before.keys()}) #dictionary with keys=names of needs before execution, values=state of need after (could have more needs after execution of skill)
        for key in needs_before.keys():
            if needs_after[key].is_superior_to(needs_before[key]):
                self.memory[key]=[skill,worked] #If need is more satisfied, save need and skill that makes it more satisfied
                if skill==self.target_skill:
                    self.target_skill=None #If it was the target skill, clear it up
        return worked
    def apply_logic(self, considering):
        #Prioritizes resuts that it knows worked last time.
        result=[]
        for key in self.memory.keys():
            entry=self.memory[key]
            if entry[0] in considering and entry[1]:
                result.append(entry[0])
                considering.remove(entry[0])
        result.extend(considering)
        if len(result)<1:
            print("There's nothing it thinks it should do...")
        return result

class astrategy(askill):
    #A Strategy is a Skill that determines how the action queue is to be performed.
    def __init__(self, name, parameters):
        super().__init__(name, parameters)
    def action(self, buddy, top=True):
        skill=buddy.queue.pop(0)
        buddy.logic.evaluate_result(buddy,skill)
        pass

class DefaultStrategy(astrategy):
    #A Strategy that performs the first skill of a queue
    def __init__(self):
        super().__init__('Perform most important', 0)
    
class MultiSkill(astrategy):
    #A Strategy that performs multiple Skills in sequence from the queue depending on the Buddy's remaining Stamina.
    #DISCLAIMER: This doesn't currently support actions that result in new needs, the queue is locked in during the feel phase and not updated inbetween steps of the Strategy.
    def __init__(self, name, parameters):
        super().__init__(name, parameters)
    def action(self,buddy):
        stamina_idxs=[]
        idx=0
        for need in buddy.needs:
            if 'Stamina' in need.name:
                stamina_idxs.append(idx)
            idx+=1
        del(idx)
        has_stamina=True
        if len(stamina_idxs) <1:
            print('Buddy '+buddy.name+" can't do multiple things!")
            chosen_stamina=1
            has_stamina=False
        else:
            chosen_idx=None
            for idx in stamina_idxs:
                actual_state=buddy.needs[idx].actual_state
                critical_state=buddy.needs[idx].critical_state
                if actual_state.is_superior_to(critical_state):
                    chosen_idx=idx
                    break
            if chosen_idx is None:
                chosen_idx=stamina_idxs[-1]
            chosen_stamina=buddy.needs[chosen_idx].data
            if chosen_stamina<1:
                print('Buddy '+buddy.name+" doesn't have stamina left!")
                chosen_stamina=1
                has_stamina=False
        
        if len(buddy.queue) > chosen_stamina:
            print('Buddy '+buddy.name+" doesn't have enough energy to do all that it wants!")
            number=chosen_stamina
        else:
            number=len(buddy.queue)

        for i in range(number):
            skill=buddy.queue.pop(0)
            buddy.logic.evaluate_result(buddy,skill)
            if has_stamina:
                buddy.needs[chosen_idx].decay()
                if buddy.needs[chosen_idx].data<1:
                    print('Buddy '+buddy.name+" has run out of "+buddy.needs[chosen_idx].name+"!")
                    break
        
        return