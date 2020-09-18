import numpy as np
import matplotlib.pyplot as plt
import csv

plt.style.use('ggplot')

timesteps = ['20.0', '10.0', '5.0', '1.0', '0.5'] # fs

euler_data = []
verlet_data = []

for t in timesteps:
    euler_data.append( np.loadtxt('./data/_euler-' + t + 'fs-ts.txt', delimiter=',', unpack=True) )
    verlet_data.append( np.loadtxt('./data/_verlet-' + t + 'fs-ts.txt', delimiter=',', unpack=True) )    

# EXPLICIT EULER - ENERGY DIFFERENCE
# for i in range(0, len(timesteps)):
#     plt.plot(euler_data[i][0], euler_data[i][1], label=timesteps[i] + str(' fs'))
# plt.title("Explicit Euler: Total Energy Difference")
# plt.xlabel("Time (seconds)")
# plt.ylabel("(H-H0)/kb")
# plt.legend(bbox_to_anchor=(1.04, 0.5), loc='center left', borderaxespad=0)
# plt.savefig('./plots/euler_energy', dpi=1200, bbox_inches='tight')


# EXPLICIT EULER - TEMPERATURE DIFFERENCE
# for i in range(0, len(timesteps)):
#     plt.plot(euler_data[i][0], euler_data[i][2], label=timesteps[i] + str(' fs'))
# plt.title("Explicit Euler: Temperature Difference")
# plt.xlabel("Time (seconds)")
# plt.ylabel("T - T0")
# plt.legend(bbox_to_anchor=(1.04, 0.5), loc='center left', borderaxespad=0)
# plt.savefig('./plots/euler_temp', dpi=1200, bbox_inches='tight')


# VERLET - ENERGY DIFFERENCE
# for i in range(0, len(timesteps)):
#     plt.plot(verlet_data[i][0], verlet_data[i][1], label=timesteps[i] + str(' fs'))
# plt.title("Verlet Method: Total Energy Difference")
# plt.xlabel("Time (seconds)")
# plt.ylabel("(H-H0)/kb")
# plt.legend(bbox_to_anchor=(1.04, 0.5), loc='center left', borderaxespad=0)
# plt.savefig('./plots/verlet_energy', dpi=1200, bbox_inches='tight')


# VERLET - TEMPERATURE DIFFERENCE
# fig, ax = plt.subplots(3, sharex=True, sharey = True, gridspec_kw={'hspace': 0})
# a1 = ax[0].plot(verlet_data[0][0], verlet_data[0][2], label='20.0 fs', color='#E24A33')[0]
# a2 = ax[1].plot(verlet_data[2][0], verlet_data[2][2], label='5.0 fs', color='#348ABD')[0]
# a3 = ax[2].plot(verlet_data[4][0], verlet_data[4][2], label='0.5 fs', color='#988ED5')[0]
# ax[2].set_xlabel("Time (seconds)")
# ax[1].set_ylabel("T - T0")
# ax[0].set_title("Verlet Method: Temperature Difference")
# fig.legend([a1, a2, a3], ['20.0 fs', '5.0 fs', '0.5 fs'], bbox_to_anchor=(.92, 0.5), loc='center left', borderaxespad=0)
# plt.savefig('./plots/verlet_temp', dpi=1200, bbox_inches='tight')

# VERLET vs EULER - ENERGY DIFFERENCE
# plt.plot(euler_data[4][0], euler_data[4][1], label='0.5 fs - Euler')
# plt.plot(verlet_data[0][0], verlet_data[0][1], label='20.0 fs - Verlet')
# plt.title("Explicit Euler vs. Verlet Method - Energy Difference")
# plt.xlabel("Time (seconds)")
# plt.ylabel("(H-H0)/kb")
# plt.legend(bbox_to_anchor=(1.04, 0.5), loc='center left', borderaxespad=0)
# plt.savefig('./plots/euler_vs_verlet_energy', dpi=1200, bbox_inches='tight')

plt.show()