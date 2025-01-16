'''
This is my own work as defined by the SAIBT Academic Integrity Policy.
I am fully aware of the consequences of academic misconduct as defined
by the SAIBT Academic Integrity Policy.

SAIBT ID:   43173
Name:       Yashvi Chetankumar Patel
Date:       13/01/2025
'''

import abc
from typing import Optional

class NotAliveException(Exception):
    pass

class Monster(metaclass=abc.ABCMeta):
    '''
    Abstract base class of other Monsters.
    '''
    def __init__(self, health, base_power):
        '''
        Constructs a Monster with the provided health and base power.
        '''
        self._health = health
        self._base_power = base_power

    @property
    def health(self):
        '''
        Gets the monster's current health.
        '''
        return self._health

    @health.setter
    def health(self, value):
        '''
        Sets the monster's health to the specified value.
        '''
        self._health = value

    @property
    def base_power(self):
        '''
        Gets the monster's base power.
        '''
        return self._base_power

    @base_power.setter
    def base_power(self, value):
        '''
        Sets the monster's base power to the specified value.
        '''
        self._base_power = value

    @abc.abstractmethod
    def attack(self, monster):
        '''
        Attacks another monster, reducing its health by the monster's power.
        '''
        pass

    def is_alive(self):
        '''
        Returns True if the monster is alive (health > 0).
        '''
        return self._health > 0

    def get_power(self):
        '''
        Returns the monster's current power.
        '''
        return self._base_power

    def __str__(self):
        '''
        Returns a string representation of the monster.
        '''
        return f"{self.__class__.__name__} with {self._health} health and {self._base_power} power"

    def __repr__(self):
        '''
        Returns a detailed string representation of the monster.
        '''
        return f"{self.__class__.__name__}(health={self._health}, base_power={self._base_power})"

class Wolf(Monster):
    '''
    A Wolf is a monster that creates its own WolfPack and stays in that WolfPack.
    '''
    def __init__(self):
        super().__init__(5, 5)
        self._pack = None

    @property
    def pack(self):
        '''
        Gets the wolf's current pack.
        '''
        return self._pack

    @pack.setter
    def pack(self, new_pack):
        '''
        Sets the wolf's pack to the specified WolfPack.
        '''
        self._pack = new_pack

    def attack(self, monster):
        '''
        Attacks another monster if this wolf is alive.
        '''
        if not self.is_alive():
            raise NotAliveException("Wolf is dead and cannot attack.")
        if monster.is_alive():
            monster.health -= self.get_power()
            print(f"{self} attacks {monster}")
            if not monster.is_alive():
                print(f"{monster} has died")
        else:
            print(f"{monster} is already dead")

class WolfPack:
    '''
    A pack of wolves with a leader.
    '''
    def __init__(self, leader):
        '''
        Creates a new WolfPack with the specified leader.
        '''
        self._wolves = [leader]
        self._leader = leader
        leader.pack = self

    def add_wolf(self, wolf):
        '''
        Adds a wolf to the pack.
        '''
        self._wolves.append(wolf)
        wolf.pack = self

    def remove_wolf(self, wolf):
        '''
        Removes a wolf from the pack.
        '''
        if wolf in self._wolves:
            self._wolves.remove(wolf)
            wolf.pack = None
            if wolf == self._leader and self._wolves:
                self._leader = self._wolves[0]

    def get_living_wolves(self):
        '''
        Returns a list of all living wolves in the pack.
        '''
        return [wolf for wolf in self._wolves if wolf.is_alive()]

    def __str__(self):
        '''
        Returns a string representation of the wolf pack.
        '''
        return f"WolfPack with {len(self.get_living_wolves())} living wolves"

    def __repr__(self):
        '''
        Returns a detailed string representation of the wolf pack.
        '''
        return f"WolfPack(wolves={self._wolves})"

class Werewolf(Wolf):
    '''
    A Werewolf that can transform between human and wolf forms.
    '''
    def __init__(self):
        super().__init__()
        self._is_human = True
        self._base_power = 1

    def transform(self):
        '''
        Transforms between human and wolf form.
        '''
        self._is_human = not self._is_human
        self._base_power = 1 if self._is_human else 5

    def get_power(self):
        '''
        Returns the werewolf's current power based on its form.
        '''
        return self._base_power




class Slime(Monster):
    '''
    A Slime that can combine with other slimes.
    '''
    def __init__(self, inner_slime1=None, inner_slime2=None):
        base_power = 1
        base_health = 1
        
        if inner_slime1:
            base_power += inner_slime1.get_power() * 2
            base_health += inner_slime1.health * 2
        if inner_slime2:
            base_power += inner_slime2.get_power() * 2
            base_health += inner_slime2.health * 2
            
        super().__init__(base_health, base_power)
        self._inner_slime1 = inner_slime1
        self._inner_slime2 = inner_slime2

    def attack(self, monster):
        '''
        Attacks another monster if this slime is alive.
        '''
        if not self.is_alive():
            raise NotAliveException("Slime is dead and cannot attack.")
        if monster.is_alive():
            monster.health -= self.get_power()
            print(f"{self} attacks {monster}")
            if not monster.is_alive():
                print(f"{monster} has died")
        else:
            print(f"{monster} is already dead")

    def split(self):
        '''
        Returns the inner slimes when this slime dies.
        '''
        return [slime for slime in [self._inner_slime1, self._inner_slime2] if slime is not None]

    def join(self, other_slime):
        '''
        Creates a new slime by combining with another slime.
        '''
        return Slime(self, other_slime)

class GelatinousCube(Slime):
    '''
    A Gelatinous Cube that absorbs the power of monsters it kills.
    '''
    def __init__(self, inner_slime1=None, inner_slime2=None):
        super().__init__(inner_slime1, inner_slime2)
        self._absorbed_power = 0

    def get_power(self):
        '''
        Returns the cube's total power including absorbed power.
        '''
        return self._base_power + self._absorbed_power

    def attack(self, monster):
        '''
        Attacks another monster and absorbs its power if killed.
        '''
        if not self.is_alive():
            raise NotAliveException("Gelatinous Cube is dead and cannot attack.")
        if monster.is_alive():
            initial_health = monster.health
            monster.health -= self.get_power()
            print(f"{self} attacks {monster}")
            if not monster.is_alive():
                self._absorbed_power += monster.get_power()
                print(f"{monster} has died and its power was absorbed")
        else:
            print(f"{monster} is already dead")