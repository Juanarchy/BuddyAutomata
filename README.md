# Buddy Automata

Buddy Automata is a lightweight artificial life simulation framework built in Python as an excercise in object oriented programming. It provides a modular environment where autonomous actors ("Buddies") interact, perceive their surroundings, and act upon their internal needs and unique personalities. 

## Some features

* **Needs & Logic Engine**: Actors evaluate internal states (needs, stamina, gauges) and select actions using interchangeable logic systems, from simple queues to memory-based decision making.
* **Sensory Perception (Fields System)**: Entities emit scalar fields (e.g., "Food Scent", "Blood Scent") into the environment. Other actors can perceive these fields within a radius and track them to find resources or prey.
* **Dynamic Personalities**: Built-in support for different behavior profiles like `Vampire`, `Glutton`, and `Cannibal` that dictate the needs and skills a Buddy possesses. Actors can even adopt new personalities dynamically (e.g., getting bitten by a vampire).
* **Skills & Actions**: A flexible skill system where actors can search the environment, consume objects, or perform custom actions that affect the world state.

## Possible future work

* A visual representation of the world, and data related to the simulation.
* File based configuration, loading and saving simulations.
* Real-time/run-time interaction with the simulation, modifying actor parameters, positions, skills etc.
* More complex actor interaction, such as reproduction.
* Evolution, communication.
* Obstacles, terrain, physics. Field dynamics and interaction.
* More complex needs system.
* Spatial hashing, quadtrees, or similar methods to optimize performance.

## Example script

The sample simulation provided in `main.py` initializes a 2D world with various Buddies and periodic food drops.

The simulation will print the status of each actor turn-by-turn. Press `Enter` to advance the simulation steps.

## File descriptions

* `main.py`: Sample entry point setting up a world and populating it with actors.
* `worlds.py`: Defines the simulated environment, tracking actors, grid parameters, and global time.
* `actors.py`: Core classes for entities (`adude`, `SmartDude`, `Food`) detailing their physiology, needs, and action loop.
* `skills.py`: Defines the actions actors can take, including sensory searches (`Radius2DSearch`), feeding, and the logic frameworks (`SimpleLogic`, `RandomMemoryLogic`).
* `fields.py`: Implementation of the scalar fields used for the sensory perception system.
* `personalities.py`: Modules defining different character types and their specific needs and abilities.
* `needs.py` & `states.py`: Classes representing the internal states and desires driving actor behavior.
* `locations.py`: Classes for coordinate and positional tracking.

## License

This project is open-source and released under the **GNU General Public License v3.0**. See the `LICENSE` file for more details.
