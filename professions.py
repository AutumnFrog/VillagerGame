#
# Villager Game
# Professions Module
# Written by Madeline Autumn
# Last modified on 03/06/21
#

### Imports and variables ###
import config
import random

### Professions ###

class Unemployed:
    '''Unemployed villagers provide no materials or bonuses but can build buildings'''

    def action(self, villager):
        pass

class Farmer:
    '''The farmer provides foods for the village at farming buildings'''

    def action(self, villager):
        # Collect food
        
        food_produced = random.randint(2,5)
        config.food += food_produced
