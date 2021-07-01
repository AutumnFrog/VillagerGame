#
# Villager Game
# Main Module
# Written by Madeline Autumn
#

### Importants and Varibles ###
import config
import mapUI
import random

# Initialize the globals
config.init()

init_villagers = 3
offset_max = (7, 5)

total_ponds = random.randint(3,6)

### Functions ###
def get_offset(x_offset, y_offset):
    '''Return a randomized offset and position for initital buildings'''

    # Get offset in relation to center pos and set pos
    offset = (random.randint(x_offset*-1, x_offset), 
              random.randint(y_offset*-1, y_offset))
    pos = (init_pos[0] + offset[0], init_pos[1] + offset[1])

    return pos

### Main Game Loop ###

if __name__ == '__main__':

    config.init_app()

    # Add ponds to the map
    config.map.create_ponds(5)
    
    # Get the starting position
    init_pos = None
    while init_pos == None:
        
        x = random.randint(24, config.map.width-24)
        y = random.randint(16, config.map.height-16)

        pos = ((y-1)*config.map.width)
        
        if config.map.terrain_map[pos] == 'Grass':
            init_pos = (x, y)

    # Create the innitial houses and villagers
    for i in range(init_villagers):

        config.seed += 1

        # Add wooden huts and adjust max villagers accordingly
        build_hut = False
        while build_hut == False:
            pos = get_offset(offset_max[0], offset_max[1])
            build_hut = config.map.build_building(config.get_building('Wooden Hut'), 
                                                  pos[0], pos[1], 
                                                  False, True)
        config.max_villagers += 1

        # Add farms
        build_farm = False
        while build_farm == False: 
            pos = get_offset(offset_max[0]+2, offset_max[1]+2)
            build_farm = config.map.build_building(config.get_building('Farm'), 
                                                   pos[0], pos[1], 
                                                   False, True)
        
        # Create inital villagers
        config.create_villager()

    
    # Update the map
    mapUI.draw_map(config.map.frame)

    # Set the scrollbar to center on the map
    map_frame = config.main_app.map

    x = init_pos[0] / ( config.map.width + ( map_frame.map_size[0]*1.5 ) )
    y = init_pos[1] / ( config.map.height + ( map_frame.map_size[1]*1.5 ) )

    map_frame.map_box.xview_moveto(x)
    map_frame.map_box.yview_moveto(y)

    # Run the main loop
    config.main_app.root.mainloop()
    
    # Save upon game closing
    config.save()
