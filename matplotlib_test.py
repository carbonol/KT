# Matplotlib documentation
# https://matplotlib.org/

# https://matplotlib.org/stable/users/getting_started/

import matplotlib.pyplot as plt
import numpy as np

# x = np.linspace(0, 2 * np.pi, 200)
# y = np.sin(x)

x = np.array([0, 1, 2])
y = np.array([1, 2, 3])

# x = np.array(list(range(1, 51)))
# y = np.array(list(range(10, 510, 10)))

# N = 3
# x = np.linspace(1, N, N)
# y = np.linspace(2, N*2, N)

fig, ax = plt.subplots()
ax.plot(x, y, 'go--', linewidth=2, markersize=12)
plt.show()