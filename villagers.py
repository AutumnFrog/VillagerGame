#
# Villager Game
# Villager Module
# Written by Madeline Autumn
# Last modified on 04/06/21
#

### Imports and Varibles ###
import config, professions
import random

with open("villager_names", 'r') as f:
    names = f.readlines()
names = [n.strip() for n in names] 

### Villager class ###

class Villager:
    '''Class the stores the data for each villager'''

    def __init__(self, name, profession):

        self.name = name
        self.profession = profession

        # Villagers initial stats
        self.hunger = 0
        self.health = config.health_max
        self.happiness = 0

        # Villager Logs
        self.log = [(f'Turn {config.turn}', 'white')]
        self.turn_log = []

        # Frame widget
        self.frame = None

    ## Turn functions ##
    def end_turn(self):

        # Run profession action and log the action
        action = self.profession.action(self)
        if action != None:
            self.append_villager_log(action[0], action[1])
        
        # Random attack villagers if unhappy
        if self.happiness < 0:
            if random.randint(1,48) <= self.happiness**2:
                self.attack_villager()
    
    def begin_turn(self):  
        '''Beginning of turn functions'''

        # Appends new turn line directly to villager log
        self.log.append((f'\nTurn {config.turn+1}', 'white'))

        # Reset the turn log
        self.turn_log = []

    def append_villager_log(self, line, colour='white'):
        '''Appends a line to the villager log and prints to main log'''

        if not(line in self.turn_log):
            self.turn_log.append(line)
            self.log.append((line, colour))
            self.frame.parent.append_log(line, colour=colour)

    ## Internal actions ##
    def feed_villager(self):
        '''Feed the villager and calculate stats'''
        # Only caluate food if needed
        if self.hunger > 0:
            if config.food > 0:
                init_food = config.food
                config.food -= self.hunger
                self.hunger = 0
                if config.food < 0:
                    # Add back food and hunger so that food > 0
                    self.hunger += config.food*-1
                    config.food += config.food*-1
                food_consumed = init_food - config.food
                # Add result to log
                result = config.get_response('consume_food')
                result = result.format(self.name, food_consumed)
                self.append_villager_log(result,'yellow')
                # Gain happiness from eating if below 0
                if self.happiness < 0:
                    self.gain_happiness(0,1)
            else:
                # Add result to log
                result = config.get_response('no_food_found').format(self.name)
                self.append_villager_log(result, 'red')
                # Add hunger if no food was consumed
                self.gain_hunger(True)

        else:
            # Add hunger if no food was consumed
            self.gain_hunger(False)
    
    def attack_villager(self):
        '''Function for dealing with villager combat'''

        target = random.choice(config.villagers)
        damage = random.randint(1,4)
        
        # Return result
        if target == self:
            result = config.get_response('attack_self')
            result = result.format(self.name, damage)
        else:
            result = config.get_response('attack_villager')
            result = result.format(self.name, target.name, damage)
            target_result = config.get_response('target_villager')
            target_result.format(self.name, target.name, damage)
            target.log.append((target_result, 'red2'))
        self.append_villager_log(result, 'red')
        
        target.lose_health(damage, damage)

    ## Hunger functions ##
    def gain_hunger(self, lose_happiness):
        '''Add hunger to villager and keep within bounds'''

        self.hunger += random.randint(config.hunger_range[0],
                                      config.hunger_range[1])
        
        # Check boundries
        if self.hunger > config.hunger_max:
            self.hunger = config.hunger_max
    
        self.return_hunger_log()

        # Lose happiness if requested
        if lose_happiness:
            self.lose_happiness(0,2)

    def return_hunger_log(self):
        '''Return an output to the logs depending on hunger level'''

        result = None
        if self.hunger >= config.hunger_log_boundry[0]:
            result = (config.get_response('starving').format(self.name), 'red')
        elif self.hunger >= config.hunger_log_boundry[1]:
            result = (config.get_response('hungry').format(self.name), 'yellow')

        if result != None:
            self.append_villager_log(result[0], result[1])

    ## Happiness functions ##
    def gain_happiness(self, min, max):
        '''Calculate happiness loss and keep within bounds'''

        self.happiness += random.randint(min, max)

        # Check boundries 
        if self.happiness > config.happiness_max:
            self.happiness = config.happiness_max

        self.return_happiness_log()


    def lose_happiness(self, min, max):
        '''Calculate happiness loss and keep within bounds'''

        self.happiness -= random.randint(min, max)

        # Check boundries
        if self.happiness < config.happiness_min:
            self.happiness = config.happiness_min

        self.return_happiness_log()

    def return_happiness_log(self):
        '''Return an output to the logs depending on happiness level'''

        result = None

        if self.happiness <= config.happiness_log_boundry[0]:
            result = (config.get_response('extremely_unhappy').format(self.name),
                      'medium orchid')
        elif self.happiness <= config.happiness_log_boundry[1]:
            result = (config.get_response('unhappy').format(self.name),
                      'medium orchid')
        elif self.happiness <= config.happiness_log_boundry[2]:
            result = (config.get_response('mildly_unhappy').format(self.name),
                      'medium orchid')
        elif self.happiness >= config.happiness_log_boundry[3]:
            result = (config.get_response('happy').format(self.name), 'cyan')
        elif self.happiness >= config.happiness_log_boundry[4]:
            result = (config.get_response('extremely_happy').format(self.name),
                      'cyan')

        if result != None:
            self.append_villager_log(result[0], result[1])

    ## Health functions ##
    def lose_health(self, min, max):
        '''Calculate health loss'''

        self.health -= random.randint(min, max) 

        self.return_health_log()

        # Kill if out of bounds
        if self.health <= 0:
            self.kill()
        else:
            # Lose happiness as result of injury
            self.lose_happiness(1,2)

    def return_health_log(self):
        '''Return output to the log based on health'''

        result = None

        if self.health <= config.health_log_boundry[0]:
            result = config.get_response('near_death').format(self.name)
        elif self.health <= config.health_log_boundry[1]:
            result = config.get_response('hurt_severe').format(self.name)
        elif self.health <= config.health_log_boundry[2]:
            result = config.get_response('hurt_moderate').format(self.name)
        elif self.health <= config.health_log_boundry[3]:
            result = config.get_response('hurt_mild').format(self.name)
        
        if result != None:
            self.append_villager_log(result, 'red')

    def kill(self):
        '''Kills the villager'''

        # Remove frame from screen
        self.frame.frame.grid_forget()
        self.frame.parent.villager_frames.remove(self.frame)

        # Add death to logs
        response = config.get_response('death').format(self.name)
        self.append_villager_log(response, 'red')

        # Remove self from villager list
        config.villagers.remove(self)

def create_villager():
    '''Creates a randomized villager and to the village'''

    config.villagers.append(Villager(random.choice(names), professions.Unemployed()))
