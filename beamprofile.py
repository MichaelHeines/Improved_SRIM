import csv
import math
import numpy as np
import os.path

# This program generates a realistic beam profile for SRIM .dat input
class beam_parameters:
    def __init__(self, y_offset, z_offset, y_std, z_std, nr_particles, atomic_number, energy, energy_std_fractional):
        self.y_offset = y_offset
        self.z_offset = z_offset
        self.y_std = y_std
        self.z_std = z_std
        self.nr_particles = nr_particles
        self.atomic_number = atomic_number
        self.energy = energy                                    # Requested energy
        self.energy_std_fractional = energy_std_fractional      # Energy deviation (not properly implemented)


def generate_toptext(string_dat):
    line1 = "=========== TRIM with various Incident Ion Energies/Angles and Depths ========= \n"
    line2 = "= This file tabulates the kinetics of incident ions or atoms.                 = \n"
    line3 = "= Col.#1: Ion Number, Col.#2: Z of atom leaving, Col.#3: Atom energy (eV).    = \n"
    line4 = "= Col.#4-6: Last location:  Col.#4: X= Depth into target.                     = \n"
    line5 = "= Col.#7-9: Cosines of final trajectory.                                      = \n"
    line6 = "================ Typical Data File is shown below  ============================ \n"
    line7 = string_dat
    line8 = "Event  Atom  Energy  Depth   Lateral-Position   ----- Atom Direction ---- \n"
    line9 = "Name   Numb   (eV)    _X_(A)   _Y_(A)  _Z_(A)   Cos(X)   Cos(Y)   Cos(Z) \n"
    line10 = "\n"

    text_dat = line1+line2+line3+line4+line5+line6+line7+line8+line9+line10
    return text_dat


def generate_numbers(nr_particles):
    N_space = np.linspace(1, nr_particles, nr_particles)
    N_string = []
    
    for i in range(len(N_space)):
        N_string.append(str(int(N_space[i])))
    
    for i in range(len(N_string)):
        while (len(N_string[i])) < 5:
            N_string[i] = '0' + N_string[i]                                                         # Stupid SRIM only allows 5char STRINGS here. Do not use regular numbers, because it won't work
            
    return N_string


def generate_dat(beam_parameters, save_path, file_name):
    print(beam_parameters)
    y_offset = beam_parameters.y_offset
    z_offset = beam_parameters.z_offset
    y_std = beam_parameters.y_std
    z_std = beam_parameters.z_std
    nr_particles = beam_parameters.nr_particles
    atomic_number = beam_parameters.atomic_number
    energy = beam_parameters.energy
    energy_std_fractional = beam_parameters.energy_std_fractional

    complete_name_out = os.path.join(save_path, file_name)

    Ion_number = generate_numbers(nr_particles)
    E = np.random.normal(energy, energy*energy_std_fractional, nr_particles)
    x = np.zeros(nr_particles)
    y = np.random.normal(y_offset, y_std, nr_particles)
    z = np.random.normal(z_offset, z_std, nr_particles)
    
    phi = np.random.uniform(0, 2 * math.pi, nr_particles)
    theta = np.zeros(nr_particles)
    x_vec = np.cos(theta)                                           # x in SRIM is beam direction --> theta azimuthal x angle
    y_vec = np.cos(phi) * np.sin(theta)
    z_vec = np.sin(phi) * np.sin(theta)
    
    g = open(complete_name_out, 'w')
    text = generate_toptext("Beam profile" + file_name)
    g.write(text)
    
    for i in range(nr_particles):
        line = str(Ion_number[i]) + "\t" + str(atomic_number) + "\t" + str("{:e}".format(E[i]) + "\t" + str("{:e}".format(x[i])) + "\t" + str("{:e}".format(y[i])) + "\t" + str("{:e}".format(z[i])) + "\t" + str("{:e}".format(x_vec[i])) + "\t" + str("{:e}".format(y_vec[i])) + "\t" + str("{:e}".format(z_vec[i])) + "\n")
        g.write(line)



# Inputs and default values
parameters = beam_parameters(0, 0, 0, 0, 10**5, 19, 60 * 10**3, 0)
save_path = '/mnt/ksf9/H2/user/u0148069/share/my.public/SRIM_scripts/beam_profiles/'
file_name = 'Potassium_60keV.txt'

generate_dat(parameters, save_path, file_name)



# Work in progress: beam divergence, need to determine distribution of theta for an energy spread

