import numpy as np
import matplotlib
matplotlib.use('Agg')  # This is needed to save image on server
import matplotlib.pyplot as plt

print("Starting simulation...")

# Create data for graph
x = np.linspace(0, 10, 100)  # 100 points from 0 to 10
y = np.sin(x)                # sin(x) values

# Plot the graph
plt.plot(x, y)
plt.title("My First Simulation")
plt.xlabel("X axis")
plt.ylabel("sin(X)")
plt.grid(True)

# Save as image
plt.savefig("result.png")
print("Done. File saved as result.png")