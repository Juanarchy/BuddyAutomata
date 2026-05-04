from imports import *

my_world = aworld('my world', [], [], 0)

my_world.add_actor(Food('Wumpa fruit', alocation((10,10),my_world),"Sweetness",10,10,5,my_world))
my_world.add_actor(SmartDude('Vampire',alocation((rng.integers(0,20),rng.integers(0,20)),my_world),my_world,[],Vampire('Blood','bloodier'),{},[]))
my_world.add_actor(SmartDude('Foo 1',alocation((rng.integers(0,20),rng.integers(0,20)),my_world),my_world,[],Glutton('Glutton'),{},[]))
my_world.add_actor(SmartDude('Cannibal',alocation((10,0),my_world,[]),my_world,[],Cannibal('Cannibal'),{},[]))
my_world.add_actor(SmartDude('Foo 2',alocation((rng.integers(0,20),rng.integers(0,20)),my_world),my_world,[],Glutton('Glutton'),{},[]))
my_world.add_actor(SmartDude('Foo 3',alocation((rng.integers(0,20),rng.integers(0,20)),my_world),my_world,[],Glutton('Glutton'),{},[]))
my_world.add_actor(SmartDude('Foo 4',alocation((rng.integers(0,20),rng.integers(0,20)),my_world),my_world,[],Glutton('Glutton'),{},[]))

i=0
while True:
    i+=1
    print('Instant '+str(i)+', actors: '+str(len(my_world.actors))+'\n')
    for actor in my_world.actors:
        print(actor)
        if isinstance(actor,adude):
            actor.feel()
            actor.sense()
            actor.act()
        print()
    if len(my_world.actors)<8:
        place=alocation((rng.integers(0,20),rng.integers(0,20)),my_world)
        my_world.add_actor(Food('Wumpa fruit', place,"Sweetness",10,10,10,my_world))
        print('A fruit appeared at '+ place.__repr__()+'!')
        input("Press enter to advance.")
        print()