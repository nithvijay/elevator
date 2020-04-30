import numpy as np

settings = {}
settings['dt'] = 0.1
settings['acceleration'] = 1
settings['max_speed'] = 5

class Elevator:
    def __init__(self, num_floors, default_floor=1, floor_size=10, open_rate=1):
        self.default_floor = default_floor
        self.current_floor = self.default_floor
        self.max_floor = num_floors
        self.wanted_floors = []  # [[] for _ in range(self.max_floor)]
        self.speed = 0
        self.position = (self.current_floor - 1) * floor_size
        self.floor_size = floor_size
        self.open_rate_var = 0
        self.fitness = 0

    @staticmethod
    def distance_to_stop(initial_speed, position, desired_position):
        difference = (initial_speed ** 2) / settings['acceleration'] / 2
        return position + difference if desired_position > position else position - difference

    def approach(self, d_floor):
        if d_floor is None:
            return False
        desired_floor = d_floor[0]
        desired_position = (desired_floor - 1) * self.floor_size
        thresh = self.floor_size * settings['dt'] / 5

        if desired_floor == self.current_floor:  # if on the floor
            self.speed = 0
            self.position = desired_position  # setting position
            return self.open(d_floor)
        else:
            """
            2 main cases, 2 sub cases within each
            - elevator is below desired position
                - elevator is close to desired_position
                - elevator is not close to desired_position
            - elevator is above desired position
                - elevator is close to desired position
                - elevator is not close to desired_position
            """
            stop_distance = Elevator.distance_to_stop(
                self.speed, self.position, desired_position)
            if desired_position > self.position:  # elevator is below
                if stop_distance >= desired_position:  # elevator is close and elevator is below
                    acc = -1 * settings['acceleration']
                else:
                    acc = 0 if self.speed >= settings['max_speed'] else settings['acceleration']
            else:  # elevator is above
                if stop_distance <= desired_position:  # and stop_distance >= 0: #elevator is close and elevator is above
                    acc = settings['acceleration']
                else:
                    acc = 0 if self.speed <= -1 * \
                        settings['max_speed'] else -1 * settings['acceleration']

            self.update_position(acc)

            close_to_floor = (
                self.position + thresh) % self.floor_size < thresh * 2
            # if its close and slow enough
            if close_to_floor and abs(self.speed) < settings['max_speed']/2:
                self.current_floor = round(self.position / self.floor_size + 1)
        return False

    def update_position(self, acc):
        initial_speed = self.speed
        self.speed = self.speed + acc * settings['dt']
        self.speed = settings['max_speed'] if self.speed > 5 else settings['max_speed'] * - \
            1 if self.speed < -5 else self.speed
        self.position = self.position + \
            (initial_speed + self.speed) / 2 * settings['dt']

        self.speed = round(self.speed, 5)
        self.position = round(self.position, 5)

    def open(self, wanted_floor):
        # case 1 - someone in elevator wants to get out
        # case 2 - someone wants to get in the elevator
        rate_check = self.open_rate_var == int(1/settings['dt'])
        # if people want to leave
        if rate_check and ([self.current_floor, False] in self.wanted_floors):
            self.wanted_floors.remove([self.current_floor, False])
            self.open_rate_var = 0
            self.fitness+=1
        elif rate_check and (wanted_floor[1]):
            self.wanted_floors.append([wanted_floor[2], False])
            wanted_floor[1] = False
            self.open_rate_var = 0
            self.fitness+=1
        else:
            self.open_rate_var += 1
        return (self.wanted_floors.count([self.current_floor, False]) == 0) and not wanted_floor[1]

    def output(self):
        return [self.position, self.speed, self.wanted_floors.copy()]

    def __repr__(self):
        return "Speed: {}\nPosition: {}\nAcceleration: {}\nFloor: {}\n"\
            .format(self.speed, self.position, settings['acceleration'], self.current_floor)

class ElevatorRunner:
    def __init__(self, elevators, animation=False):
        self.elevators = elevators
        self.max_floor = elevators[0].max_floor
        self.floors = []
        self.next_floor_indexer = 0
        self.animation = animation
        if self.animation:
            self.elevator_states = []

    def generate(self, gen_rate):
        """
        arguments: rate is proportion of successful generation
        """
        # cond - elevators has to have the same num_floors
        if self.max_floor:
            if np.random.uniform() < gen_rate:
                # print("anything")
                choices = [i + 1 for i in range(self.max_floor)]
                two_floors = np.random.choice(choices, 2, replace=False)
                self.floors.append([two_floors[0], True, two_floors[1]])

    def move_elevators(self, next_floor):
        pass

    def next_floor1(self):
        if len(self.floors) > 0:
            return self.floors.pop(0)
        elif len(self.elevators[0].wanted_floors) > 0:
            return self.elevators[0].wanted_floors[0]
        else:
            return None
    
    def next_floor(self):
        if len(self.elevators[0].wanted_floors) > 0:
            return self.elevators[0].wanted_floors[0]
        elif len(self.floors) > 0:
            return self.floors.pop(0)
        else:
            return None

    def simulate(self, time, gen_rate):
        # represents 1 unit of time
        next_floor = self.next_floor()
        for _ in range(int(time/settings['dt'])):
            self.generate(settings['dt'] * gen_rate)
            # print(next_floor)
            if next_floor == None:
                next_floor = self.next_floor()
            if self.elevators[0].approach(next_floor):
                next_floor = self.next_floor()
            if self.animation:
                self.elevator_states.append(self.elevators[0].output())
        return self.elevators[0].fitness