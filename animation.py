import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
import matplotlib.animation as animation
import numpy as np

def make_plot(states, save = False):
    fig, ax = plt.subplots(figsize=(6.4, 6.4))
    #ax.set_axis_off()
    ax.grid(axis = 'y')
    ax.set_xlim([0,10])
    ax.set_ylim([0,100])
    ax.set_yticks(np.arange(0, 100, step=10))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(labelbottom=False)

    rect1 = mpatch.Rectangle(xy=(1,1), width = .5, height = 5)
    ax.add_patch(rect1)
    text_time = ax.text(0, 0, "")#, bbox=dict(facecolor='red', alpha=0.5)) 
    text_wanted_floors = ax.text(0, 90, "", bbox=dict(facecolor='red', alpha=0.5)) 
 

    def animate(i):
        rect1.set_xy((1 , states[i][0],))
        text_time.set_text(i)
        text_wanted_floors.set_text(states[i][2])
        return [rect1, text_time]

    ani = animation.FuncAnimation(fig, animate, range(len(states)), interval = 10, blit=False)
    if save:
        ani.save("test.mp4")
    else:
        plt.show()