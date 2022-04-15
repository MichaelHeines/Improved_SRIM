import csv
import math
import numpy as np
import os.path

# Define the settings class
class Settings:
    def __init__(self, alpha_energy, atomic_number_p1, atomic_number_p2, mass_fraction, sample_width, sample_thickness, first_step):
        self.alpha_energy = alpha_energy                        # Energy of alpha particle
        self.atomic_number_p1 = atomic_number_p1                # Atomic number of emitted particle
        self.atomic_number_p2 = atomic_number_p2                # Atomic number of recoil particle
        self.mass_fraction = mass_fraction                      # Mass of emitted/recoil
        self.sample_width = sample_width                        # Width of the sample
        self.sample_thickness = sample_thickness                # Total thickness of the sample
        self.first_step = first_step                            # Is it the first decay occuring (in that case flip the sample)

# Generates information lines
def generate_toptext(string_alpha, string_recoil):
    line1 = "=========== TRIM with various Incident Ion Energies/Angles and Depths ========= \n"
    line2 = "= This file tabulates the kinetics of incident ions or atoms.                 = \n"
    line3 = "= Col.#1: Ion Number, Col.#2: Z of atom leaving, Col.#3: Atom energy (eV).    = \n"
    line4 = "= Col.#4-6: Last location:  Col.#4: X= Depth into target.                     = \n"
    line5 = "= Col.#7-9: Cosines of final trajectory.                                      = \n"
    line6 = "================ Typical Data File is shown below  ============================ \n"
    line7_1 = string_alpha
    line7_2 = string_recoil
    line8 = "Event  Atom  Energy  Depth   Lateral-Position   ----- Atom Direction ---- \n"
    line9 = "Name   Numb   (eV)    _X_(A)   _Y_(A)  _Z_(A)   Cos(X)   Cos(Y)   Cos(Z) \n"
    line10 = "\n"

    text_alpha = line1+line2+line3+line4+line5+line6+line7_1+line8+line9+line10
    text_recoil = line1+line2+line3+line4+line5+line6+line7_2+line8+line9+line10
    
    return [text_alpha, text_recoil]


# Program that takes a reformed SRIM output to generate new .dat files to be used as input for SRIM again
def srim_out_to_in(settings, save_path, file_name_in, file_name_out_p1, file_name_out_p2):
    alpha_energy = settings.alpha_energy
    atomic_number_p1 = settings.atomic_number_p1
    atomic_number_p2 = settings.atomic_number_p2
    mass_fraction = settings.mass_fraction
    sample_width = settings.sample_width
    sample_thickness = settings.sample_thickness
    first_step = settings.first_step

    ion_number = []
    x = []
    y = []
    z = []
    complete_name_in = os.path.join(save_path, file_name_in)
    complete_name_out_p1 = os.path.join(save_path, file_name_out_p1)
    complete_name_out_p2 = os.path.join(save_path, file_name_out_p2)
    
    # Open and read input file
    with open(complete_name_in, 'r') as f:
        reader = csv.reader(f, delimiter = ' ')
        
        for row in reader:
            # Check if the particle is still on the sample
            if -sample_width/2 < float(row[2]) < sample_width/2 and -sample_width/2 < float(row[3]) < sample_width/2 and float(row[1]) < sample_thickness:
                # Add position to output arrays
                ion = row[0].lstrip("0")
                while len(ion) < 5:
                    ion = "0" + ion
                ion_number.append(ion)
                y.append(float(row[2]))
                z.append(float(row[3]))

                if (first_step == True):
                    x.append(sample_thickness - float(row[1]))
                else:
                    x.append(abs(float(row[1])))
    
    N = len(ion_number)
    # Generate isotropic distribution
    phi = np.random.uniform(0, 2 * math.pi, N)
    theta = np.arccos(1 - 2 * np.random.random(N))
    energy_p1 = [alpha_energy]*N
    vec_x = np.cos(phi) * np.sin(theta)
    vec_y = np.sin(phi) * np.sin(theta)
    vec_z = np.cos(theta)
    
    g = open(complete_name_out_p1, 'w')
    h = open(complete_name_out_p2, 'w')
    
    text = generate_toptext("alpha particles", "recoiling particles")
    g.write(text[0])
    h.write(text[1])
    
    # For all events still in the system write dat file entry
    for i in range(N):   
        line_p1 = ion_number[i] + "\t" + atomic_number_p1 + "\t" + str("{:e}".format(energy_p1[i])) + "\t" + str("{:e}".format(x[i])) + "\t" + str("{:e}".format(y[i])) + "\t" + str("{:e}".format(z[i])) + "\t" + str(vec_x[i]) + "\t" + str(vec_y[i]) + "\t" + str(vec_z[i]) + "\n"
        line_p2 = ion_number[i] + "\t" + atomic_number_p2 + "\t" + str("{:e}".format(energy_p1[i] * mass_fraction)) + "\t" + str("{:e}".format(x[i])) + "\t" + str("{:e}".format(y[i])) + "\t" + str("{:e}".format(z[i])) + "\t" + str(- vec_x[i]) + "\t" + str(- vec_y[i]) + "\t" + str(- vec_z[i]) + "\n"
        g.write(line_p1)
        h.write(line_p2)

    f.close()
    g.close()
    h.close()

    print("Created .dat files for alphas and recoils")


alpha_energy = 5.9351 * 10**6                                                                               # Ac: 5.9351, Fr: 6.4577, At: 7.2013, Bi: 2.2% 5.9883, Po: 8.5361
atomic_number_p1 = "2"
atomic_number_p2 = "82"                                                                                     #Ac89 - Fr87 - At85 - Bi83 - Tl81 - Pb82
mass_fraction = 4.0/221.0                                                                                   #Ac225 - Fr221 - At217 - Bi213 - Tl209 - Pb209
sample_width = 10**8
sample_thickness = 5 * 10**3 + 25*10**5
first_step = True
settings = Settings(alpha_energy, atomic_number_p1, atomic_number_p2, mass_fraction, sample_width, sample_thickness, first_step)

save_path = "/mnt/ksf9/H2/user/u0148069/share/my.public/SRIM_scripts/"
file_name_in = "output/easyread_range_test.txt"
file_name_out_p1 = "output/Ac_alphas.dat"
file_name_out_p2 = "output/Fr_recoils.dat"

srim_out_to_in(settings, save_path, file_name_in, file_name_out_p1, file_name_out_p2)
