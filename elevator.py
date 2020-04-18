import numpy as np
"""
class:
    Elevator

attributes:
    current_floor       int     floors
    num_floors          int     the max number of floors    
    default_floor       int     default floor to go
    wanted_floors[]     int     which floors people want to go
    direction           bool    true is up

methods:
    move_up
    move_down
    open
"""
class Elevator:
    def __init__(self, num_floors, default_floor = 1):
        self.num_floors = num_floors
        if (default_floor > num_floors):
            self.default_floor = 1
        else:
            self.default_floor = default_floor
        self.current_floor = self.default_floor
        self.direction = True #going up 
        self.wanted_floors = []

    def move_up(self):
        if self.current_floor < self.num_floors:
            self.current_floor += 1

    def move_down(self):
        if self.current_floor > 0:
            self.current_floor -= 1
    
    def open(self):
        for _ in range(self.wanted_floors.count(self.current_floor)):
            self.wanted_floors.remove(self.current_floor)

    def __repr__(self):
        return "Number of Floors: {}\nDefault Floor: {}\nPosition: {}\n".format(self.num_floors, self.default_floor, self.current_floor)

"""
class: ElevatorRunner

attributes:
    elevators[]     Elevator    list of Elevator Objects
    floors[[]]      int         floors and what floors people want to go to


methods:
    simulate    the main function to progress; calls generate and move_elevators
    generate  
    add_elevator
    move_elevators  

"""
class ElevatorRunner:
    def __init__(self):
        self.elevators = []
        self.floors = [[]]
        self.max_floor = None

    def add_elevator(self, elev):
        """
        arguments: elev is a list of Elevator objects
        """
        for e in elev:
            self.elevators.append(e)
        self.max_floor = max([e.num_floors for e in self.elevators])
        self.floors = [[] for floor in range(self.max_floor)]
    
    def generate(self, rate = .25):
        """
        arguments: rate is proportion of successful generation
        """
        #cond - elevators has to have the same num_floors
        if self.max_floor:
            if np.random.uniform() < rate:
                choices = [i for i in range(self.max_floor)]
                index_of_floor = choices.pop(np.random.choice(choices)) #finding which floor people are on
                self.floors[index_of_floor].append(np.random.choice(choices)) #selecting a random floor from the floors left



    def move_elevators(self):
        pass

    def simulate(self):
        #represents 1 unit of time
        self.generate(.1)
        self.move_elevators()


    
    

        


if __name__ == '__main__':
    e1 = Elevator(4)
    e2 = Elevator(4)

    runner = ElevatorRunner()
    runner.add_elevator([e1, e2])
    runner.generate(rate = 1)
    print(runner.floors)

