import csv
import math
import numpy as np
import matplotlib.pyplot as plt
import random
import os.path

class Settings:
    def __init__(self, r_det, branching, sample_thickness, distance, generate_new):
        self.r_det = r_det
        self.branching = branching
        self.sample_thickness = sample_thickness
        self.distance = distance
        self.generate_new = generate_new
        

# Program that checks if the final position of a particle (or in the sample) is on the detector to apply the FNM
# Takes settings, and filenames (inputs in easyread)
def in_system(save_path, filename_alpha, filename_recoil, distribution_file, settings):
    completename_alpha = os.path.join(save_path, filename_alpha)
    completename_recoil = os.path.join(save_path, filename_recoil)
    completename_out = os.path.join(save_path, distribution_file)

    r_det = settings.r_det
    branching = settings.branching
    sample_thickness = settings.sample_thickness
    distance = settings.distance
    generate_new = settings.generate_new

    N_alpha = 0
    N_recoil = 0
    N_tot = 0

    h = open(completename_out, 'w')

    with open(completename_alpha, 'r') as f:
        reader = csv.reader(f, delimiter = ' ')
        
        for row in reader:
            N_tot += 1
            if float(row[1]) >= sample_thickness + distance:                                # Reaches the detector position
                if float(row[2])**2 + float(row[3])**2 <= r_det**2:                         # Inside detection surface
                    N_alpha += 1

    with open(completename_recoil, 'r') as g:
        reader = csv.reader(g, delimiter = ' ')

        for row in reader:
            if float(row[1]) >= sample_thickness + distance:                                # Reaches the detector position
                if float(row[2])**2 + float(row[3])**2 <= r_det**2:                         # Inside detection surface
                    N_recoil += 1
                    if generate_new == True:
                        h.write(row[0] + ' ' + row[1] + ' ' + row[2] + ' ' + row[3] + '\n')
            elif float(row[1]) <= sample_thickness:                                         # Stays in the sample
                if generate_new == True:
                    h.write(row[0] + ' ' + row[1] + ' ' + row[2] + ' ' + row[3] + '\n')

    f.close()
    g.close()
    h.close()

    efficiency_alpha = 10**(-3) * N_alpha * branching/float(N_tot)
    efficiency_recoil = 10**(-3) * N_recoil * branching/float(N_tot)
    
    return [efficiency_alpha, efficiency_recoil]
        


save_path = "/mnt/ksf9/H2/user/u0148069/share/my.public/SRIM_scripts/"
filename_alpha = "output/easyread_Ac_alpha.txt"
filename_recoil = "output/easyread_Fr_recoil.txt"
distribution_file = "output/Francium_positions.dat"

r_det = math.sqrt(300/math.pi) * 10**7
branching = 1
sample_thickness = 0.25 * 10**7 + 5 * 10**3
distance = 20.285 * 10**7
generate_new = True
settings = Settings(r_det, branching, sample_thickness, distance, generate_new)

efficiencies = in_system(save_path, filename_alpha, filename_recoil, distribution_file, settings)
print(str(efficiencies) + "%")
