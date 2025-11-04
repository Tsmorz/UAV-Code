import numpy as np
import matplotlib.pyplot as plt


def airfoil(c, t, a, b):
    steps = 100
    x = np.linspace(0, c, steps)
    T = t/0.2*(0.2969*np.sqrt(x)-0.1260*x-0.3516*x**2+0.2843*x**3-0.1015*x**4)
    Z = a*((b-1)*x**3-b*x**2+x)
    Z_upper = Z + 0.5*T
    Z_lower = Z - 0.5*T
    return Z_upper, Z_lower, x


c = 1
t = 0.12
a = 0.1
b = 0.1

Z_upper, Z_lower, x = airfoil(c, t, a, b)
plt.plot(x, Z_upper)
plt.plot(x, Z_lower)
plt.show()
