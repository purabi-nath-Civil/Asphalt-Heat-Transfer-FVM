# ==================================================
# HEAT TRANSFER PROJECT
# 1D HEAT TRANSFER IN ASPHALT ROAD USING FVM
# ==================================================
# Student Name : PURABI RANI NATH
# ID : purabinath124@gmail.com
# Department : MATHEMATICS
# Version : L=0.1m, dt=0.2, Nx=50 (Fixed)
# ==================================================

import subprocess
import sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy", "pandas", "matplotlib"])

import numpy as np
import matplotlib.pyplot as plt

# 1. ROAD GEOMETRY AND GRID SETUP
L = 0.1       # Road thickness in meters = 10 cm
Nx = 50       # Number of grid points
dx = L / (Nx - 1) # Control volume width

# 2. TEMPERATURE AND TIME PARAMETERS
T_top_initial = 76.0  # Top surface temperature in C
T_bottom = 31.0       # Bottom boundary temperature in C
T_initial = 34.0      # Initial temperature of the whole road in C
dt = 0.2              # Time step in seconds
total_duration = 600  # Total simulation time in seconds (10 minutes)
Nt = int(total_duration / dt) # Total time steps (3000)

# 3. MATERIAL PROPERTIES OF ASPHALT
k = 0.75      # Thermal conductivity W/mK
rho = 2300.0  # Density kg/m3
Cp = 920.0    # Specific heat capacity J/kgK
alpha = k / (rho * Cp) # Thermal diffusivity

# 4. ADDITIONAL REAL-WORLD EFFECTS
CNG_EXHAUST_HEAT = 5.0 
RAIN_EFFECT = True     
RAIN_START_SEC = 150.0 # Rain starts after 2.5 minutes
RAIN_TEMP = 25.0       

# 5. INITIAL CONDITION SETUP
T = np.ones(Nx) * T_initial
T[0] = T_top_initial + CNG_EXHAUST_HEAT 
T[-1] = T_bottom 

# গ্রাফ সেভ করার নির্দিষ্ট সময়গুলো (সেকেন্ডে): ০, ২, ৪, ৬, ৮ এবং ১০ মিনিট
save_times_sec = [0.0, 120.0, 240.0, 360.0, 480.0, 600.0]

print("Simulation Started...")

# 6. MAIN FVM SIMULATION LOOP
for n in range(Nt + 1):
    Tn = T.copy()
    current_time = n * dt

    # Boundary Condition 1: Top Surface
    if RAIN_EFFECT and current_time > RAIN_START_SEC:
        T[0] = RAIN_TEMP 
    else:
        T[0] = T_top_initial + CNG_EXHAUST_HEAT

    # Boundary Condition 2: Bottom Surface
    T[-1] = T_bottom

    # FVM Heat Equation (Vectorized for fast performance)
    T[1:-1] = Tn[1:-1] + (alpha * dt / dx**2) * (Tn[2:] - 2 * Tn[1:-1] + Tn[:-2])

    # 7. SAVE GRAPH FOR EACH SELECTED TIME
    # np.isclose ব্যবহার করা হয়েছে দশমিকের ছোটখাটো গরমিল এড়াতে
    if any(np.isclose(current_time, t_save) for t_save in save_times_sec):
        minute = current_time / 60.0
        x = np.linspace(0, L * 100, Nx) # ০ সেমি (উপর) থেকে ১০ সেমি (নিচ) সঠিক বিন্যাস

        plt.figure(figsize=(8, 5))
        plt.plot(x, T, 'r-', linewidth=2.5)
        plt.xlabel('Depth from Surface (cm)')
        plt.ylabel('Temperature (°C)')
        plt.title(f'Temperature Profile at {minute:.1f} minutes - Road Depth 10cm')
        plt.grid(True, linestyle='--')
        plt.ylim(20, 90)

        filename = f'Graph-{minute:.1f}min-L10cm.png'
        plt.savefig(filename, dpi=200)
        plt.close()
        print(f"{filename} saved at simulation time {current_time}s")

print("\nSimulation Finished! All graphs saved correctly.")



