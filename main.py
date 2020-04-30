from elevator import Elevator, ElevatorRunner
from time import time
import numpy as np

if __name__ == "__main__":
    t1 = time()
    #np.random.seed(0)
    e1 = Elevator(num_floors=10, default_floor=1)
    er1 = ElevatorRunner([e1], animation=True)
    er1.simulate(1000, .05)
    #from animation import make_plot
    #make_plot(er1.elevator_states, save=False)
    # print(er1.elevator_states)
    print(time() - t1)
    pass