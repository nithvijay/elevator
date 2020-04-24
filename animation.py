import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
import matplotlib.animation as animation

def make_plot(states):
    fig, ax = plt.subplots()
    ax.set_axis_off()
    ax.set_xlim([0,10])
    ax.set_ylim([0,100])
    rect1 = mpatch.Rectangle(xy=(1,1), width = 3, height = 3)
    ax.add_patch(rect1)  
    def animate(i):
        rect1.set_xy((5 , states[i][0],))
        return [rect1]

    ani = animation.FuncAnimation(fig, animate, range(len(states)), interval = 10)
    plt.show()