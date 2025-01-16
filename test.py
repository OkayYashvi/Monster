'''
This is my own work as defined by the SAIBT Academic Integrity Policy.
I am fully aware of the consequences of academic misconduct as defined
by the SAIBT Academic Integrity Policy.

SAIBT ID:   43173
Name:       Yashvi Chetankumar Patel
Date:       13/01/2025
'''


import unittest
from main import GelatinousCube, Werewolf, Slime

class TestGelatinousCube(unittest.TestCase):
    '''
    Test cases for the GelatinousCube class.
    '''
    def test_power_absorption(self):
        '''
        Tests that the cube correctly absorbs power from killed monsters.
        '''
        cube = GelatinousCube()
        werewolf = Werewolf()
        werewolf.transform()
        
        initial_power = cube.get_power()
        werewolf.health = 1
        cube.attack(werewolf)
        
        self.assertEqual(cube.get_power(), initial_power + 5)

    def test_splitting(self):
        '''
        Tests that the cube correctly splits into its inner slimes.
        '''
        inner1 = Slime()
        inner2 = Slime()
        cube = GelatinousCube(inner1, inner2)
        
        split_slimes = cube.split()
        self.assertEqual(len(split_slimes), 2)
        self.assertIn(inner1, split_slimes)
        self.assertIn(inner2, split_slimes)

if __name__ == "__main__":
    unittest.main()