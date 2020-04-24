import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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
    def __init__(self, num_floors, default_floor=1, acceleration=1, max_speed=5, floor_size=10, rate=.05, open_rate=1):
        self.default_floor = default_floor
        self.current_floor = self.default_floor
        self.max_floor = num_floors
        self.wanted_floors = [[] for _ in range(self.max_floor)]
        self.acceleration = acceleration
        self.max_speed = max_speed
        self.speed = 0
        self.position = (self.current_floor - 1) * floor_size
        self.floor_size = floor_size
        self.rate = rate
        self.open_rate = open_rate
        self.temp_desired_pos = 0
        self.time_elapsed = 0
    
    @staticmethod
    def distance_to_stop(initial_speed, acceleration, position, desired_position):
        #acceleration *= -1 if desired_position > position else 1
        difference = (initial_speed ** 2) / acceleration / 2
        return position + difference if desired_position > position else position - difference

    def approach(self, desired_floor):
        self.time_elapsed+=self.rate
        desired_position = (desired_floor - 1) * self.floor_size
        self.temp_desired_pos = desired_position
        thresh = self.floor_size * self.rate / 5
        if desired_floor == self.current_floor:  # if on the floor
            self.speed = 0
            self.position = desired_position  # setting position
            return self.open()
        else:
            """
            2 main cases, 2 sub cases within each
            - elevator is close to desired_position
                - elevator is below desired_position
                - elevator is above desired_position
            - elevator is not close to desired_position
                - elevator is below desired_position
                - elevator is above desired_position
            """
            stop_distance = Elevator.distance_to_stop(self.speed, self.acceleration, self.position, desired_position)
            if desired_position > self.position: #elevator is below
                if stop_distance >= desired_position: #elevator is close and elevator is below
                    acc = -1 * self.acceleration
                else:
                    acc = 0 if self.speed >= self.max_speed else self.acceleration
            else: #elevator is above
                if stop_distance <= desired_position: #elevator is close and elevator is above
                    acc = self.acceleration
                else:
                    acc = 0 if self.speed <= -1 * self.max_speed else -1 * self.acceleration
            
            self.temp_desired_pos = stop_distance

            initial_speed = self.speed
            final_speed = self.speed + acc * self.rate
            final_speed = self.max_speed if final_speed > 5 else self.max_speed * -1 if final_speed < -5 else final_speed

            diff = (initial_speed + final_speed) / 2 * self.rate
            self.position = self.position + diff

            self.speed = round(final_speed, 5)
            self.position = round(self.position, 5)
            
            #close_to_floor = abs(self.floor_size/2 - (self.position % self.floor_size)) > thresh
            close_to_floor = (self.position + thresh) % self.floor_size < thresh * 2
            if close_to_floor and abs(self.speed) < self.max_speed/2: #if its close and slow enough
                self.current_floor = round(self.position / self.floor_size + 1)
        return False

    def open(self):
        return True
    
    def add_in_elevator(self, wanted_floor):
        for _ in range(int(1/self.rate)):
            self.wanted_floors.append(wanted_floor)

    def output(self):
        return (self.position, self.speed)

    def __repr__(self):
        return "Desired Position: {}\nSpeed: {}\nPosition: {}\nAcceleration: {}\nFloor: {}\n"\
            .format(self.temp_desired_pos, self.speed, self.position, self.acceleration, self.current_floor)


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
    def __init__(self, animation=True):
        self.elevators = []
        self.floors = [[]]
        self.max_floor = None
        self.animation = animation
        if(animation):
            self.floors_states = []
            #self.fig = plt.figure(figsize=(10,10))

    def add_elevator(self, elev):
        """
        arguments: elev is a list of Elevator objects
        """
        for e in elev:
            self.elevators.append(e)
        self.max_floor = max([e.num_floors for e in self.elevators])
        self.floors = [[] for floor in range(self.max_floor)]

    def generate(self, rate=.25):
        """
        arguments: rate is proportion of successful generation
        """
        # cond - elevators has to have the same num_floors
        if self.max_floor:
            if np.random.uniform() < rate:
                choices = [i for i in range(self.max_floor)]
                # finding which floor people are on
                index_of_floor = choices.pop(np.random.choice(choices))
                # selecting a random floor from the floors left
                self.floors[index_of_floor].append(np.random.choice(choices))
            if(self.animation):
                self.floors_states.append(self.floors)

    def move_elevators(self):
        if len(self.elevators) > 0:
            pass

    def make_frame(self, x_list):
        pass

    def make_animation(self):
        pass

    def simulate(self):
        # represents 1 unit of time
        self.generate(.1)
        self.move_elevators()


if __name__ == '__main__':

    #print(Elevator.distance_to_stop(initial_speed = -10, acceleration = 10, position = 100, desired_position = 90))


    # e1 = Elevator(num_floors = 10, rate=1, default_floor=8)
    # i = 1
    # print(i, ":\n", e1)
    # while not e1.approach(2):
    #     i+=1
    #     print(i, ":\n", e1)
    # print(i * e1.rate)
    elevator_states = []
    # def tester(rate, floor):
    #     e1 = Elevator(num_floors = 10, rate=rate, default_floor=1)
    #     i = 1
    #     while not e1.approach(floor):
    #         i+=1
    #     print(rate, " seconds: ", i * rate, floor)
    # tester(1, 8)
    # tester(.5, 8)
    # tester(.2, 8)
    # tester(.1, 8)
    # tester(.01, 8)
    # tester(1, 8)
    e1 = Elevator(num_floors=10, default_floor=1)
    floor = 4
    while not e1.approach(floor):
        elevator_states.append(e1.output())
    floor = 7
    while not e1.approach(floor):
        elevator_states.append(e1.output())
    print(elevator_states)
    floor = 5
    while not e1.approach(floor):
        elevator_states.append(e1.output())
    print(elevator_states)
    from animation import make_plot
    make_plot(elevator_states)

    


    """
Number of Floors: 10
Speed: 5.0
Position: 5.750000000000001
Acceleration: 2.5
    """
