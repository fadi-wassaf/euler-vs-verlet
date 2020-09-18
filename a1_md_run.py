from dataclasses import dataclass
import numpy as np
from progress.bar import IncrementalBar
import time
import matplotlib.pyplot as plt
import copy

# Constants
mi     =  66.34e-27      # kg
mi_sq  =  mi ** 2        # kg^2
sij    =  0.341e-9       # m
kb     =  1.380658e-23   # J/K
eij    =  119.8 * kb     # J

# Multipliers to help to keep track of units
fs = 1e-15
ns = 1e-9

# Atoms positions (nm) and velocities (nm/ns)
n_atoms = 7
positions = [ (0., 0.), (.02, .39), (.34, .17), (.36, -.21), (-.02, -.4), (-.35, -.16), (-.31, .21) ]
velocities = [ (-30., -20.), (50., -90.), (-70., -60.), (90., 40.), (80., 90.), (-40., 100.0), (-80., -60.) ]

@dataclass
class Atom:
    q : np.array
    p : np.array

# Setup each atom as a tuple of two vectors: one for velocity and one for position.
# Units for position are nm and units for velocity are nm/ns.
atoms = []
for n in range(0, n_atoms):
    q = 1e-9 * np.array([positions[n][0], positions[n][1]])
    p = mi * np.array([velocities[n][0], velocities[n][1]])
    atoms.append(Atom(q, p))

def unit_vec(v):
    return v / np.linalg.norm(v)

def dqdt(p):
    return p/mi

# Note: this function only calculates the component of dp/dt from the interaction
# between atom i and j. Used later to get the total magnitude of dp/dt by combining all
# the relevant interactions from neighboring atoms.
def dpdt(qi, qj):
    # Get distance and unit vector between the two atom positions
    d = np.linalg.norm(qi - qj)
    u_vec_q = unit_vec(qi - qj)

    dpdt_mag = -4 * eij * ( ((6*sij**6)/(d**7)) - ((12*sij**12)/(d**13)) )
    return dpdt_mag * u_vec_q 

# Calculates the potential energy between two atoms
def U(qi, qj):
    # Get distance and unit vector between the two atom positions
    d = np.linalg.norm(qi - qj)

    # Calculate rest of LJ potential
    potential_term = (sij/d)**6
    return 4 * eij * ( potential_term**2 - potential_term )

# Calculates the current value of the Hamiltonian for the set of atoms
def H(a):
    E = 0.
    # Add the kinetic energy contribution from each atom
    for i in range(0, n_atoms):
        E += (.5 * np.dot(a[i].p, a[i].p))/mi

    # Add the potential energy contributions for the system
    i = 1
    while i < n_atoms:
        for j in range(0, i):
            E += U(a[i].q, a[j].q)
        i += 1

    return E

def T(a):
    temp = 0

    # Go through the atoms to add up each contribution to the temperature
    for i in range(0, n_atoms):
        temp += np.linalg.norm(a[i].p) ** 2

    return (1.0/(n_atoms * kb * 2 * mi)) * temp

# Move one step through the explicit euler process
# a: list of atoms; h: timestep
def step_euler(a, h):
    # Loop through each atom to update its q and p
    for i in range(0, n_atoms):

        # Get change in q from explicit euler method
        delta_q = h * dqdt(a[i].p)

        # Loop through atom interactions to get change in p from explicit euler method
        delta_p = np.array([0., 0.])
        for j in range(0, n_atoms):
            if i != j:
                delta_p += h * dpdt(a[i].q, a[j].q)

        # Update q and p for atom i
        a[i].q += delta_q
        a[i].p += delta_p

# Move one step through the verlet process
# a: list of atoms; h: timestep
def step_verlet(a, h):
    # Loop through each atom to update its q and p
    for i in range(0, n_atoms):

        # Get change in p for a half step using verlet method
        delta_p_half = np.array([0., 0.])
        for j in range(0, n_atoms):
            if i != j:
                delta_p_half += (h/2) * dpdt(a[i].q, a[j].q)

        # Update p by a half step 
        a[i].p += delta_p_half

        # Get the next full step for q
        delta_q = h * a[i].p/mi
        a[i].q += delta_q

        # Update the full step for p
        delta_p = np.array([0., 0.])
        for j in range(0, n_atoms):
            if i != j:
                delta_p += (h/2) * dpdt(a[i].q, a[j].q)
        a[i].p += delta_p

end_time = .1 * ns
timesteps = [20*fs, 10*fs, 5*fs, 1*fs, .5*fs]

# Get intial energy and temperature for the system
E0 = H(atoms)
T0 = T(atoms)

record_positions = True

print("Initial Energy = " + str(E0/kb) + "kb\n")

# Run Euler and Verlet methods for the various timesteps
for h in timesteps:

    # Normal file format - Time, (E-E0)/kb, Temp
    # Position file format - x0, y0, x1, y1, ... , x6, y6
    euler_file = open("./data/_euler-" + str(h/fs) + "fs-ts.txt", "w+")
    euler_file_pos = open("./data/_euler-" + str(h/fs) + "fs-ts-pos.txt", "w+")    
    verlet_file = open("./data/_verlet-" + str(h/fs) + "fs-ts.txt", "w+")
    verlet_file_pos = open("./data/_verlet-" + str(h/fs) + "fs-ts-pos.txt", "w+")

    # Create copy of the initial state of the system
    atoms_euler = copy.deepcopy(atoms)
    atoms_verlet = copy.deepcopy(atoms)

    # Setup progress bar
    bar = IncrementalBar('Timestep ' + str(h/fs) + "fs", max=end_time/h, suffix='%(percent)d%% [%(elapsed_td)s / %(eta_td)s]')

    current_time = 0
    while current_time < end_time:

        # Calculate differences in energy and temperature for each set of atoms
        deltaE_euler = (H(atoms_euler) - E0)/kb
        deltaE_verlet = (H(atoms_verlet) - E0)/kb
        deltaT_euler = T(atoms_euler) - T0
        deltaT_verlet = T(atoms_verlet) - T0

        # Write data to files
        euler_file.write('%e, %f, %f\n' % (current_time, deltaE_euler, deltaT_euler))
        verlet_file.write('%e, %f, %f\n' % (current_time, deltaE_verlet, deltaT_verlet))
        if record_positions:
            for a in atoms_euler:
                euler_file_pos.write('%e, %e, ' % (a.q[0], a.q[1]))
            euler_file_pos.write('\n')
            for a in atoms_verlet:
                verlet_file_pos.write('%e, %e, ' % (a.q[0], a.q[1]))
            verlet_file_pos.write('\n')

        # Go through one timestep for the euler and verlet process
        step_euler(atoms_euler, h)
        step_verlet(atoms_verlet, h)

        current_time += h
        bar.next()
    bar.finish()

    euler_file.close()
    euler_file_pos.close()
    verlet_file.close()
    verlet_file_pos.close()
