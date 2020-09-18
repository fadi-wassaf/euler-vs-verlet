import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

n_atoms = 7

methods = ['Euler', 'Verlet']
timesteps = ['20.0', '10.0', '5.0', '1.0', '0.5'] # fs

# Extract position information for each timestep
cols = [x for x in range(0, 2 * n_atoms)]

# Do process for all methods and timesteps
for method in methods:
    for t in timesteps:

        method_l = method.lower()
        positions = np.loadtxt('./data/_' + method_l + '-' + t + 'fs-ts-pos.txt', delimiter=',', unpack=True, usecols=cols)

        # Calculate frame interval for timesteps using desired playtime
        playtime = 10 # s
        num_pos = len(positions[0])
        num_frames = playtime*60
        frame_interval = int(num_pos/(playtime*60))

        # Setup figure used for plotting
        fig = plt.figure()
        ax = plt.axes(xlim=(-1e-9,1e-9), ylim=(-1e-9,1e-9))
        plt.title(method + ' Method: ' + t +' fs timestep for 0.1 ns')
        pts, = ax.plot([], [], 'o')

        def init():
            pts.set_data([], [])
            return pts,

        # Plots atom positions for an index i in the list of positions
        def animate(i):
            x = []
            y = []
            for j in range(0, n_atoms):
                x.append(positions[2*j][i])
                y.append(positions[2*j + 1][i])
            pts.set_data(x, y)
            return pts,

        anim = FuncAnimation(fig, animate, init_func=init, frames=num_frames, interval=frame_interval, blit=True)
        anim.save('./animations/' + method_l + '_' + t + 'fs.gif', writer='imagemagick', fps=60)
