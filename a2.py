from curses.ascii import isdigit
from sys import set_coroutine_origin_tracking_depth
from a2_support import *
from typing import Optional

class Entity():
    """ Abstract class is composed of Item, Plant and Pot. """
    def get_class_name(self) -> str:
        """ Retrurn the name of entity's clsss. """
        return self.__class__.__name__
        
    def get_id(self) -> str:
        """ Return the single character id of this entity's class according to
            constants.py.
        """
        if self.__class__.__name__ == 'Entity':
            return 'E'
        if self.__class__.__name__ == 'Plant':
            return 'P'
        if self.__class__.__name__ == 'Pot':
            return 'U'
        if self.__class__.__name__ == 'Item':
            return 'I'
        if self.__class__.__name__ == 'Water':
            return "W"
        if self.__class__.__name__ == 'Fertiliser':
            return "F"
        if self.__class__.__name__ == 'PossumRepellent':
            return "R"
    
    def __str__(self) -> str:
        """ Return the id(string) representing the Entity. """ 
        return self.get_id()
        
    
    def __repr__(self) -> str:
        """ Return the text which could make a new instance of this class that 
            looks identical (where possible) to self.
        """
        return self.__class__.__name__ + "()"
        

class Plant(Entity):
    """ A plant Entity has water, health points (HP), age and repellent. 
        The drink rate and sun level are determined by the specific plant 
        according to constants.py.
    """

    def __init__(self, name: str):
        """ Set up the plant with a given plant name. 
        
        Parameters:
            name: str from constants.py
        """
        self.name = name
        self.health = 10
        self.water = 10.0
        self.age = 0
        self.repellent = False
    

    def get_name(self) -> str:
        """ Return name of the plant. """
        return self.name
    

    def get_health(self) -> int:
        """ Return the plant current HP. """
        return self.health
    

    def get_water(self) -> float:
        """ Return the current water levels of the plant. """
        return self.water
    

    def water_plant(self) -> None:
        """ Increase the plant water level by 1. """
        self.water = self.water + 1


    def get_drink_rate(self) -> float:	
        """ Return water drinking rate of the plant. """
        return PLANTS_DATA[self.name]['drink rate']
    

    def get_sun_levels(self) -> tuple[int, int]:	
        """ Return the acceptable sun level of the plant with the upper and
            lower range.
        """
        return (PLANTS_DATA[self.name]['sun-lower'], PLANTS_DATA[self.name]['sun-upper'])
    

    def decrease_water(self, amount: float):	
        """ Decrease the plants' water level by a specified amount.

        Parameters:
            amount: decreased given number
        """
        self.water = self.water - amount


    def drink_water(self):
        """Reduce water levels by plant drink rate. """
        self.water = self.water - self.get_drink_rate()
        if self.water < 0: # If water levels is zero the plant HP reduces by 1.
            self.health = self.health - 1
        

    def add_health(self, amount: int) -> None:
        """ Add to the plant health levels by a specified amount.

        Parameters:
            amount: increased given number health
        """
        self.health = self.health + amount
    

    def decrease_health(self, amount = 1):
        """ Decrease the plants health by 1(default) or given number.

        Parameters:
            amount: decreased given number health
        """
        self.health = self.health - amount

    def set_repellent(self, applied: bool) -> None:
        """ Apply or remove repellent from plant. 

        Parameters:
            applied: bool represents set or remove repellent
        """
        self.repellent = applied
    

    def has_repellent(self) -> bool:
        """ Return True if the plant has repellent, False otherwise. """
        return self.repellent
    

    def get_age(self) -> int:
        """ Return how many days this plant has been planted. """
        return self.age
    

    def increase_age(self):
        """ Increase the number of days this plant has been planted by 1. """
        self.age = self.age + 1
    

    def is_dead(self) -> bool:
        """ Return True if the plant health is less than or equals to zero,
            False otherwise.
        """
        if self.get_health() <= 0:
            return True
        else:
            return False
    

    def __repr__(self) -> str:
        """ Return the text which could make a new instance of this class. """
        return self.__class__.__name__ + f"('{self.name}')"
        

class Item(Entity):
    """ Abstract subclass of Entity which provides base functionality for all 
        items in the game.
    """
    def apply(self, plant: 'Plant') -> None:
        """ Applies the items effect, if any, to the given plant. Raise 
            NotImplementedError.
        """
        self.plant  = plant
        if self.plant.get_id() == "P":
            raise NotImplementedError

class Water(Item):
    """ Adds to plant water level by 1 when applied. """
    def apply(self, plant: 'Plant') -> None:
        """ Water specific plant

        Parameters:
            plant: targeted plant to be watered
        """
        self.plant = plant
        plant.water_plant()

class Fertiliser(Item):
    """ Adds to plant health by 1 when applied. """
    def apply(self, plant: 'Plant') -> None:
        """ Set fertiliser to specific plant

        Parameters:
            plant: targeted plant to be set
        """
        self.plant = plant
        plant.add_health(1)

class PossumRepellent(Item):
    """ Cancel a possum attach when applied. """
    def apply(self, plant: 'Plant') -> None:
        """ Set repellent to specific plant

        Parameters:
            plant: targeted plant to be set
        """
        self.plant = plant
        plant.set_repellent(True)
    

class Inventory:
    """ An Inventory contains and manages a collection of items and plant. """
    def __init__(self, initial_items: Optional[list[Item]] = None, 
        initial_plants: Optional[list[Plant]] = None) -> None:
        """ Sets up initial inventory:
            1. If no initial_items or initial_plants are 
               provided, inventory starts with an empty dictionary for the entities. 
            2. Otherwise, the initial dictionary is set up from the initial_items and 
               initial_plants lists to be a dictionary mapping entity names to a list 
               of entity instances with that name. 

        Parameters:
            initial_items: list of class Item
            initial_plants: list of class Plant
        """
        self.initial_items = initial_items
        self.initial_plants = initial_plants
        if self.initial_items == None and self.initial_plants == None:
            self.initial_items = []
            self.initial_plants =  []
            inventory = {}
        else:
            inventory = {}
            inventory["Item"] = self.initial_items
            inventory["Plant"] = self.initial_plants
        self.inventory = inventory
    
    def add_entity(self, entity: Item | Plant) -> None:
        """ Adds the given item or plant to this inventory collection of entities.

        Parameters:
            entity: list of class Item or Plant
        """
        if entity.get_class_name() == "Plant":
            self.initial_plants.append(entity)
        else:
            self.initial_items.append(entity)

    def get_entities(self, entity_type: str) -> dict[str, list[Item | Plant]]:
        """ Returns the a dictionary mapping entity (item or plant) names to the 
            instances of the entity with that name in the inventory, respectively.
        
        Parameters:
            entity_type: The type can either be plant or item.
        """
        plant_dic = {}
        item_dic = {}
        item_data = ["W", "F", "R"]
        if entity_type == "Plant":
            for plant in self.initial_plants:
                for name in list(PLANTS_DATA):
                    if plant.get_name() == name:
                        if name in list(plant_dic):
                            plant_dic[name].append(plant)
                        else:
                            plant_dic[name] = [plant]
            return plant_dic
        if entity_type == "Item":
            for item in self.initial_items:
                for id in item_data:
                    if item.get_id() == id:
                        if id in item_dic:
                            item_dic[id].append(item)
                        else:
                            item_dic[id] = [item]
            return item_dic

    def remove_entity(self, entity_name: str) -> Optional[Item | Plant]:
        """ Removes one instance of the entity (item or plant) with the given name 
            from inventory,if one exists. If no entity exists in the inventory with 
            the given name, then this method returns None.

        Parameters:
            entity_name: The type can either be plant or item str name.

        >>> inventory.remove_entity('Rebutia')
        Plant('Rebutia')
        """
        m = 0
        del1 = 0
        del2 = 0
        if entity_name  in  list(PLANTS_DATA):                # Distinguish plant and item
            for m in range(len(self.initial_plants)):
                if entity_name == self.initial_plants[m].get_name():
                    while del1 in range(len(self.initial_plants)):
                        if self.initial_plants[del1].get_name() == entity_name:
                            temp1 = self.initial_plants[del1] # Store deleted plant contemporarily
                            del self.initial_plants[del1]     # Remove the plant with position
                        break
                return temp1
            else:
                return None
        else: 
            for n in range(len(self.initial_items)):
                if entity_name == self.initial_items[n].get_id():
                    while del2 in range(len(self.initial_items)):
                        if self.initial_items[del2].get_id() == entity_name:
                            temp2 = self.initial_items[del2]  # Store deleted item contemporarily
                            del self.initial_items[del2]      # Remove the item with position
                        break
                    return temp2
                else:
                    return None
    
    def get_inventory(self):   #OPTIONAL
        pass
    def __str__(self):
        item_list  = ""
        plant_list = ""
        inventory_list = ""
        for key1, value1 in self.get_entities("Plant").items():
            plant_list  =  plant_list + str(key1 + ": " + str(len(value1))) + "\n"
        for key2, value2 in self.get_entities("Item").items():
            item_list = item_list + str(key2 + ": " + str(len(value2))) + "\n"
        inventory_list = item_list + plant_list
        inventory_list = inventory_list.strip("\n")  # Delete the "\n" in the end
        return  inventory_list
    
    def __repr__(self):
        """ Returns a string that could be used to construct a new instance of 
            Inventory containing the same items as self currently contains.

            Note: the order of plant matters while items' not.
        """
        ordered_plant = []              # Set an empty list to get same plants together
        plant_entities = self.get_entities("Plant").values()
        for keys in plant_entities:   
            ordered_plant.append(keys)  # Append Plant in order
        return f"Inventory(initial_items={self.initial_items}, initial_plants={ordered_plant})"


class Pot(Entity):
    """ Pot is an Entity that has growing conditions information and an instance of plant. """
    def __init__(self) -> None:
        """ Sets up an empty pot and attributes. """     
        self.plant = None
        self.sun_range = None
        self.evaporation = None

    def set_sun_range(self, sun_range: tuple[int, int]) -> None:
        self.sun_range = sun_range

    def get_sun_range(self) -> tuple[int, int]:
        if self.sun_range == None:
            return None
        else:
            return self.sun_range

    def set_evaporation(self, evaporation: float) -> None:
        """ Set the evaporation rate of the pot.

        Parameters:
            evaporation: The evaporation rate of the pot.
        """
        self.evaporation = evaporation

    def get_evaporation(self) -> float:
        """ Returns the evaporation rate of the pot. """
        if self.evaporation != None:       
            return self.evaporation

    def put_plant(self, plant: Plant) -> None:
        """ Adds an instance of a plant to the pot. """
        self.plant = plant

    def look_at_plant(self) -> Optional[Plant]:
        """ Returns the plant in the pot and without removing it. """
        if self.plant != None:
            return self.plant

    def remove_plant(self) -> Optional[Plant]:
        """ Returns the plant in the pot and removes it from the pot. """
        temp = self.plant          # Save the plant to delete temporarily.
        self.plant = None
        return temp                # Return deleted plant.

    def progress(self) -> None: 
        """ Progress the state of the plant and check if the current plant 
            is suitable in the given conditions. Decrease the plant water 
            levels based on the evaporation. The health of the plant should 
            decrease by 1:

            Check: water level, sun range, and HP.
        """
        if self.evaporation != None:
            water_decrease =  self.evaporation + self.plant.get_drink_rate()
            self.plant.decrease_water(water_decrease)
            
        if self.sun_range[0] > self.plant.get_sun_levels()[1] or self.sun_range[1] < self.\
            plant.get_sun_levels()[0]:           # Decrease health when current sun level is\  
            self.plant.decrease_health()         # out of range of standard level
            if self.plant.is_dead():
                print(f"{self.plant.get_name()} is dead")
            else:
                print(f"Poor {self.plant.get_name()} dislikes the sun levels.")
        if self.plant.get_water() < 0:
            self.plant.decrease_health()         
            if self.plant.is_dead():
                print(f"{self.plant.get_name()} is dead")

    def animal_attack(self) -> None:
        """ Decreases the health of the plant by the animal attack damage dealt 
            if a plant is in the pot. Do nothing otherwise.
        """
        if self.plant != None:            # Ignore if there is no plant.
            if self.plant.has_repellent():
                print(f"There has been an animal attack! But luckily \
the {self.plant.get_name()} has repellent.") 
            else:
                self.plant.decrease_health(ANIMAL_ATTACK_DAMAGE)
                print(f"There has been an animal attack! Poor {self.plant.get_name()}.")

    def __str__(self) -> str:
        return self.get_class_name()
    
    def __repr__(self):
        return f"{self}()"


class Room:
    def __init__(self, name):
        """ A Room instance represents the space in which plants can be planted and the
            instances of plants within the room.
        
        Parameters:
            name: name str for rooms.
        """
        self.pots = {0: Pot(), 1: Pot(), 2: Pot(), 3: Pot()}
        self.name = name
        for i in list(ROOM_LAYOUTS):
            if self.name == i:
                self.layout = ROOM_LAYOUTS[i]["layout"]
                self.positions = ROOM_LAYOUTS[i]["positions"]
                self.room_type = ROOM_LAYOUTS[i]["room_type"]
        
    def init_positions(self): #OPTIONAL
        return self.positions
        
    def get_plants(self) -> dict[int, Plant | None]:
        """ Return the Plant instances in this room. with the keys being the positions and 
            value being the corresponding plant, None if no plant is in the position.
        """
        dict_plants = {}
        for p in range(4):
            if self.pots[p].look_at_plant() == None:
                dict_plants[p] = None
            else:
                dict_plants[p] = self.pots[p].look_at_plant()
        return dict_plants

    def get_number_of_plants(self) -> int:
        """ Return the total number of live plants in the room. """
        count = 0
        for n in range(4):
            if self.get_plants()[n] != None:
                count += 1
        return count

        
    def add_pots(self, pots: dict[int, Pot]) -> None: 	
        """ Add a pots to the room. Each key corresponds to a position in the room, 
            with each value being an instance of a pot.
        
        Parameters:
            pots: 4 instance of pots
        """
        for p in range(len(list(pots))):
            self.pots[p] = pots[p]

    def get_pots(self) -> dict[int, Pot]:	
        return self.pots

    def get_pot(self, position: int) -> Pot:
        return self.pots[position]

    def add_plant(self, position: int, plant: Plant):
        if self.pots[position].look_at_plant() == None:
            self.pots[position].put_plant(plant)

        
    def get_name(self) -> str:
        return self.name
        
    def remove_plant(self, position: int) -> Plant | None:
        if self.pots[position].look_at_plant() != None:
            temp = self.pots[position].look_at_plant() # Temporarily save the deleted plant
            self.pots[position].remove_plant()
            return temp

    def progress_plant(self, pot: Pot) -> bool:
        if pot.look_at_plant() == None:                # Check if the pot is empty
            return False
        else:
            pot.look_at_plant().increase_age()         # Let plant to age
            pot.progress()
            if pot.look_at_plant().get_health() <= 0:
                pot.remove_plant()
            return True
        
    def progress_plants(self) -> None:
        """ Implement progress to all the plants in a room. """
        for k in self.pots:
            if self.pots[k].look_at_plant() != None:
                self.progress_plant(self.pots[k])

    def __str__(self) -> str:
        return self.get_name()
        
    def __repr__(self) -> str:
        return f"{self.room_type}('{self.get_name()}')"

class OutDoor(Room): 
    def progress_plant(self, pot: Pot) -> bool:
        """ Returns True if pot is not empty and triggers a given pot to check on plant 
            condition and plant to age. False if pot is empty. Checks to see if an animal 
            attack has occured. 

        Parameters:
            pot: specific pot to be  progressed.
        """
        super().progress_plant(pot)
        if pot.look_at_plant() == None:     
            return False
        else:
            if pot.look_at_plant().get_health() > 0:
                if dice_roll():     
                    if pot.look_at_plant().has_repellent():
                        print(f"There has been an animal attack! But luckily \
the {pot.plant.get_name()} has repellent.")
                    else:
                        pot.look_at_plant().decrease_health(ANIMAL_ATTACK_DAMAGE)
                        if pot.look_at_plant().is_dead():
                            print(f"There has been an animal attack! \
{pot.plant.get_name()} is dead.")
                        else:
                            print(f"There has been an animal attack! Poor \
{pot.plant.get_name()}.")
            return True

def load_house(filename: str) -> tuple[list[tuple[Room, str]], dict[str, int]]:
    """ Reads a file and creates a dictionary of all the Rooms.
    
    Parameters:
        filename: The path to the file
    
    Return:
        A tuple containing 
            - a list of all Room instances amd their room name,
            - and a dictionary containing plant names and number of plants
    """
    rooms = []
    plants = {}
    items = {}
    room_count = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('Room'):
                _, _, room = line.partition(' - ')
                name, room_number = room.split(' ')
                room_number = int(room_number)
                if room_count.get(name) is None:
                    room_count[name] = 0
                room_count[name] += 1
                if ROOM_LAYOUTS.get(name).get('room_type') == 'Room':
                    room = Room(name)
                elif ROOM_LAYOUTS.get(name).get('room_type') == 'OutDoor':
                    room = OutDoor(name)
                rooms.append((room, name[:3] + str(room_count[name])))
                row_index = 0

            elif line.startswith('Plants'):
                _, _, plant_names = line.partition(' - ')
                plant_names = plant_names.split(',')
                for plant in plant_names:
                    plant = plant.split(' ')
                    plants[plant[0]] = int(plant[1])

            elif line.startswith('Items'):
                _, _, item_names = line.partition(' - ')
                item_names = item_names.split(',')
                for item in item_names:
                    item = item.split(' ')
                    items[item[0]] = int(item[1])

            elif len(line) > 0 and len(rooms) > 0:
                pots = line.split(',')
                positions = {}
                for index, pot in enumerate(pots):
                    sun_range, evaporation_rate, plant_name = pot.split('_')
                    pot = Pot()
                    if plant_name != 'None':
                        pot.put_plant(Plant(plant_name))
                    sun_lower, sun_upper = sun_range.split('.')
                    pot.set_evaporation(float(evaporation_rate))
                    pot.set_sun_range((int(sun_lower), int(sun_upper)))
                    positions[index] = pot
                rooms[-1][0].add_pots(positions)
                row_index += 1

    return rooms, plants, items

class Model:
    """ The controller uses Model to understand and mutate the house state.
        The model keeps track of multiple Room instances and an inventory.
    """
    def __init__(self, house_file: str):
        """ Exploit load_house function to build a Model. """
        self.days = 1
        self.house_file = house_file
        self.house = load_house(self.house_file)
        
    def get_rooms(self) -> dict[str, Room]: 
        """ Returns all rooms with room name as keys with a corresponding room instance. """
        room_list = self.house[0]
        room_dict = {}
        for r in range(len(room_list)):
            room_dict[room_list[r][1]] = room_list[r][0]
        return room_dict

    def get_all_rooms(self) -> list[Room]:
        """ Returns a list of all the room instances. """
        all_room_list = self.get_rooms().values()
        return list(all_room_list)
        
    def get_inventory(self) -> Inventory:
        """ Get inventoey from house file. """
        plants = []
        items = []
        i = p = q = r = 0
        for k in list(self.house[1]):       # Iterate plant in house file
            if self.house[1][k] == 1:
                plants.append(Plant(k))
            else:
                while i < self.house[1][k]:
                    plants.append(Plant(k))
                    i += 1
        for m in list(self.house[2]):       # Iterate item in house file
            if m == "F":
                if self.house[2][m] == 1:
                    items.append(Fertiliser())
                else: 
                    while p < self.house[2][m]:
                        items.append(Fertiliser())
                        p += 1
            elif m == "W":
                if self.house[2][m] == 1:
                    items.append(Water())
                else: 
                    while q < self.house[2][m]:
                        items.append(Water())
                        q += 1
            elif m == "R":
                if self.house[2][m] == 1:
                    items.append(PossumRepellent())
                else: 
                    while r < self.house[2][m]:
                        items.append(PossumRepellent())
                        r += 1
        inventory = Inventory(items, plants)
        return inventory
        
    def get_days_past(self) -> int:
        return self.days
        
    def next(self, applied_items: list[tuple[str, int, Item]]) -> None:
        """ Move to the next day, if there are items in the list of applied items (room name,
            position, item to be applied) then apply all affects. Add fertiliser and possum
            repellent to the inventory every 3 days. Progress all plants in all rooms.

        Parameters:
            applied_items: accumulated items to be set.
        """
        if applied_items == []:
            for i in range(len(self.get_all_rooms())):
                self.get_all_rooms()[i].progress_plants()
        else: 
            for k in range(len(applied_items)):
                if applied_items[k][2].get_id() == "F":
                    applied_items[k][2].apply(self.get_rooms()[applied_items[k][0]].get_pot\
                        (applied_items[k][1]).look_at_plant())
                if applied_items[k][2].get_id() == "R":
                    applied_items[k][2].apply(self.get_rooms()[applied_items[k][0]].get_pot\
                        (applied_items[k][1]).look_at_plant())
            for j in range(len(self.get_all_rooms())):
                self.get_all_rooms()[j].progress_plants()
            applied_items = []          # Empty the applied_items after implementation
        if self.get_days_past()%3 == 0: # Add fertiliser and possum repellent to the inventory\
            self.house[2]["F"] += 1     # every 3 days.
            self.house[2]["R"] += 1
        self.days += 1
        
    def move_plant(self, from_room_name: str, from_position: int, 
        to_room_name: str, to_position: int) -> None: 
        """ Move a plant from a room at a given position to a room with the given position.
              
        Parameters:
            from_room_name: room contains the targeted plant
            from_position: targeted position
            to_room_name: destination room
            to_position: destination position
        """
        for r1 in list(self.get_rooms()):
            if r1 == from_room_name:
                remove_plant = self.get_rooms()[r1].remove_plant(from_position)

        for r2 in list(self.get_rooms()):
            if r2 == to_room_name:
                self.get_rooms()[r2].add_plant(to_position, remove_plant)
        
    def plant_plant(self, plant_name: str, room_name: str, 
        position: int) -> None:
        if self.get_rooms()[room_name].get_pot(position).look_at_plant() != None:
            self.get_rooms()[room_name].remove_plant(position)
            self.get_rooms()[room_name].add_plant(position, Plant(plant_name))
        else:
            self.get_rooms()[room_name].add_plant(position, Plant(plant_name))
        for p in list(self.house[1]):
            if p == plant_name:
                self.house[1][p] -= 1

    def swap_plant(self, from_room_name: str, from_position: int, 
        to_room_name: str, to_position: int) -> None:
        """ Swap the two plants from a room at a given position to a room with the given position. """
        remove_plant_1 = self.get_rooms()[from_room_name].remove_plant(from_position)
        remove_plant_2 = self.get_rooms()[to_room_name].remove_plant(to_position)
        if remove_plant_1 == None and remove_plant_2 != None:   # Check if from plant is None
            self.get_rooms()[from_room_name].add_plant(from_position, remove_plant_2)
        elif remove_plant_1 != None and remove_plant_2 == None: # Check if to plant is None
            self.get_rooms()[to_room_name].add_plant(to_position, remove_plant_1)
        elif remove_plant_1 != None and remove_plant_2 != None: # Check if both from and to plants are not None
            self.get_rooms()[from_room_name].add_plant(from_position, remove_plant_2)
            self.get_rooms()[to_room_name].add_plant(to_position, remove_plant_1)
        
    def get_number_of_plants_alive(self) -> int:
        count = 0
        for room in self.get_all_rooms():
            for i in range(4):
                if room.get_plants()[i] != None:
                    if not room.get_plants()[i].is_dead():
                        count += 1
        return count

    def has_won(self) -> bool:
        """ Return True if number of plants alive > 50% of number from start of the 15 day
            period. And 15 days has passed.
        """
        total_alive = 0
        if self.days >= 15: # Check days
            for m in range(len(self.get_all_rooms())):
                part_alive = self.get_all_rooms()[m].get_number_of_plants()
                total_alive += part_alive
            if self.get_number_of_plants_alive() >= total_alive/2: # Check alive number
                return True
        else:
            return False
    
    def has_lost(self) -> bool:
        if self.has_won():
            return False
        else:
            return True

    def __str__(self) -> str:
        return f"Model('{self.house_file}')"

    def __repr__(self) -> str:
        return f"Model('{self.house_file}')"


class GardenSim:
    """ Controller class maintain instances of the model and view, collecting user input and
        facilitate communication between the model and view. 
    """

    def __init__(self, game_file: str, view: View):
        """ Creates a new GardenSim house with the given view and a new Model instantiated 
            using the given house_file.

        Parameters:
            game_file: given file from player
            view: class that presents status of the game 
        """
        self.game_file = game_file
        self.model = Model(self.game_file)
        self.view = view
        self.applied_item = []

    def play(self):
        """ Executes the entire game until a win or loss occurs. 
        
        >>> Enter a move: m
        move not found: m
        >>> Enter a move: rm Bal1 2
        Cereus has been removed.
        """
        self.view.draw(self.model.get_all_rooms())
        while 1:                                    # Infinite loop until the results showed
            step = input("\nEnter a move: ")        # Take input from player
            if step != "n" and step != "ls" and len(step) < 8:  # Detect invalid input
                print(INVALID_MOVE + step)
                self.view.draw(self.model.get_all_rooms())
            else:
                if step[0] == "l":
                    if len(step) == 2:
                        self.view.display_rooms(self.model.get_rooms())
                        self.view.display_inventory(self.model.get_inventory().get_entities\
                            ('Plant'), "Plant")
                        self.view.display_inventory(self.model.get_inventory().get_entities\
                            ('Item'), "Item")
                        self.view.draw(self.model.get_all_rooms())

                    elif step[-1].isdigit():
                        ls_room_name = step[3:7]
                        ls_position = int(step[-1])
                        ls_plant = self.model.get_rooms()[ls_room_name].get_pot(ls_position).\
                            look_at_plant()
                        self.view.display_room_position_information(self.model.get_rooms()\
                            [ls_room_name], ls_position, ls_plant)
                        self.view.draw(self.model.get_all_rooms())

                if step[0] == "m":
                    m_from_room_name = step[2:6]
                    m_from_position = int(step[7])
                    m_to_room_name = step[9:13]
                    m_to_position = int(step[-1])
                    self.model.move_plant(m_from_room_name, m_from_position, m_to_room_name, \
                        m_to_position)
                    self.view.draw(self.model.get_all_rooms())

                if step[0] == "p" and len(step[0]) == 16:
                    p_plant_name = step[2:9]
                    p_room_name = step[10:14]
                    p_position = int(step[-1])
                    self.model.plant_plant(p_plant_name, p_room_name, p_position)
                    self.view.draw(self.model.get_all_rooms())

                if step[0] == "w":
                    w_room_name = step[2:6]
                    w_position = int(step[-1])
                    self.model.get_rooms()[w_room_name].get_pot(w_position).look_at_plant().\
                        water_plant()
                    self.view.draw(self.model.get_all_rooms())

                if step[0] == "a":
                    a_room_name = step[2:6]
                    a_position = int(step[7])
                    item_id = step[-1]
                    if item_id == "F":
                        self.applied_item.append((a_room_name, a_position, Fertiliser()))
                        self.model.house[2]["F"] -= 1                   # Decrease inventory after adding\
                        self.view.draw(self.model.get_all_rooms())      # item to applied item.
                    if item_id == "R":
                        self.applied_item.append((a_room_name, a_position, PossumRepellent()))
                        self.model.house[2]["R"] -= 1          
                        self.view.draw(self.model.get_all_rooms())

                if step[0] == "s":
                    from_room_name = step[2:6]
                    from_position = int(step[7])
                    to_room_name = step[9:13]
                    to_position = int(step[-1])
                    self.model.swap_plant(from_room_name, from_position, to_room_name, to_position)
                    self.view.draw(self.model.get_all_rooms())
                
                if step[0] == "r":
                    room_name_r = step[3:7]
                    position_r = int(step[-1])
                    temp = self.model.get_rooms()[room_name_r].remove_plant(position_r)
                    print(f"{temp} has been removed.")
                    self.view.draw(self.model.get_all_rooms())

                if step == "n":
                    self.model.next(self.applied_item)
                    self.applied_item = []               # Empty applied item after implementation.
                    if self.model.get_days_past() >= 15: # Check the results after 15 days.
                        if self.model.has_won():
                            print(WIN_MESSAGE)
                            break                        
                        elif self.model.has_lost():
                            print(LOSS_MESSAGE)
                            break
                    self.view.draw(self.model.get_all_rooms())

def main():
    """ Entry-point to gameplay """
    view = View()
    house_file = input('Enter house file: ')
    garden_gnome = GardenSim(house_file, view)
    garden_gnome.play()

if __name__ == '__main__':
    main()