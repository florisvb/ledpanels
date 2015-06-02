

class LEDPanel_Configuration:
    def __init__(self):
    
        self.init_commands = [  ['set_pattern_id', 1, 0, 0, 0, 0, 0],
                                ['set_position', 165, 1, 0, 0, 0, 0],
                             ]
        
        self.localtime_start = 23
        self.intervals_hrs = [0,
                              .5,
                              .5,
                              .5,
                              ]
        self.commands= [  ['set_position', 165, 1, 0, 0, 0, 0],
                          ['set_position', 165, 1, 0, 0, 0, 0],
                          ['set_position', 165, 1, 0, 0, 0, 0],
                          ['set_position', 165, 1, 0, 0, 0, 0],
                       ]
