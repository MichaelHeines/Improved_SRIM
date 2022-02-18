# Code is horribly inefficient, unclear and has a bad form  --> I should really try to improve this.
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
import random
import os.path

# Program that calculates the efficiency and energy spectrum of using reformed SRIM output files

save_path = 'C:/Users/micha/OneDrive/Documenten/school/Master 2e jaar/Masterproef/Data_calculations/Full_numerical/easyread/'

#input: distance, energy secondary/tertiary recoil alpha, possible second decay path alpha energy, file name alpha/recoil file, save path
# start with Ac alpha, Fr recoils, At 2recoils
# start with Fr alpha, At recoils, Bi 2recoils
# start with At alpha, Bi recoils (2.2% Bi, 97.8% Po), none
# start with Bi alpha (2.2%), none, none
# start with Po alpha from location of Bi (98%), none, none

def spectrum_efficiency(det_source, r_det, E_arecoil1, E_arecoil2, E_extra, b1, b2, b3, file_name_alpha, file_name_recoil, save_path):
# returns the energy spectrum and the amount of counts in the detector for both alpha decay from the primary atoms as fraction coming from decaying recoils caught on the detector
    complete_name_alpha = os.path.join(save_path, file_name_alpha + '.txt')
    complete_name_recoil = os.path.join(save_path, file_name_recoil + '.txt')
    E = []                  # values of the energy for counts
    counts_1 = 0            # counts for the primary atom decay
    counts_2 = 0            # counts for the transmitted recoil particles that decay on the detector
    counts_3 = 0            # counts for alpha from secondary recoil after accepted primary
    counts_4 = 0            # counts for alpha from secondary recoil after rejected primary
    counts_5 = 0            # counts for possible second decay path
    counts_6 = 0            # counts for Bi in Ac-decay
    counts_7 = 0            # counts for Po in Ac-decay
    e_geo_ps = (1 - (det_source)/(math.sqrt(det_source**2 + r_det**2)))/2   # point source approximation for geometric efficiency considering particles moving in the right direction

    with open(complete_name_alpha, 'r') as f:       # counts for the primary decay and their energies
        reader = csv.reader(f, delimiter = ' ')
        for row in reader:
            if row[0] == "T":                
                path_length = det_source/float(row[7])
                angle_y = float(row[8])
                angle_z = float(row[9])
                y_det = float(row[5]) + path_length * angle_y
                z_det = float(row[6]) + path_length * angle_z
                
                if (math.sqrt(y_det**2 + z_det**2) < r_det):
                    if random.random() <= b1: 
                        counts_1 += 1
                        E.append(float(row[3]))
    
    with open(complete_name_recoil, 'r') as g:      # counts for the recoil decay
        reader = csv.reader(g, delimiter = ' ')
        for row in reader:
            if row[0] == "T":
                path_length = det_source/float(row[7])
                angle_y = float(row[8])
                angle_z = float(row[9])
                y_det = float(row[5]) + path_length * angle_y                   # y extrapolation
                z_det = float(row[6]) + path_length * angle_z                   # z extrapolation
              
                
                if (math.sqrt(y_det**2 + z_det**2) < r_det):                    # recoil in detector
                    if random.random() < 0.5 and E_arecoil1 != 0:                        # 1/2 acceptance of alpha
                        if random.random() <= b2:
                            counts_2 += 1
                            E.append(E_arecoil1)
                        else:
                            counts_5 += 1
                            E.append(E_extra)
                        
                        if random.random() <= 2 * e_geo_ps and E_arecoil2 != 0:       # point source approximation of secondary recoil going back to the foil and return an alpha to the detector /2 because of isotropy
                            rnum = random.random()
                            if rnum <= 0.5:
                                if rnum <= 2 * e_geo_ps:
                                    if random.random() <= b3:
                                        counts_3 += 1
                                        E.append(E_arecoil2)
                                    else:
                                        counts_5 +=1
                                        E.append(E_extra)
                            
                            else:
                                if rnum <= 2 * e_geo_ps and E_arecoil1 == 6.45847*10**6: # don't accept ping pong -> accept Bi/Po with 0.5
                                    if random.random() < 0.022:
                                        counts_6 += 1
                                        E.append(5.988*10**6)
                                    else:
                                        counts_7 += 1
                                        E.append(8.536*10**6)
                    
                    elif E_arecoil2 != 0 and E_arecoil1 != 0 and random.random() < 0.5:     # reject primary alpha but accept secondary
                        if random.random() <= b3:
                            counts_4 += 1
                            E.append(E_arecoil2)
                            if E_arecoil1 == 6.45847*10**6 and random.random() <= 2* e_geo_ps**2:
                                if random.random() < 0.022:
                                    counts_6 += 1
                                    E.append(5.988*10**6)
                                else:
                                    counts_7 += 1
                                    E.append(8.536*10**6)
                        else:
                            counts_5 += 1
                            E.append(E_extra)
                            
                    elif E_arecoil1 == 6.45847*10**6 and random.random() <= 0.5:
                        if random.random() < 0.022:
                            counts_6 += 1
                            E.append(5.988*10**6)
                        else:
                            counts_7 += 1
                            E.append(8.536*10**6)
                    
    return [counts_1, counts_2, counts_3, counts_4, counts_5, counts_6, counts_7, E]
# counts_1 = direct alpha
# counts_2 = primary recoil alpha
# counts_3 = secondary recoil alpha after accepted primary
# counts_4 = secondary recoil alpha after rejected primary
# counts_5 = other branching counts
# counts_6 = for Ac decay Bi
# counts_7 = for Ac decay Po

#det_source = 1.7*10**8                                # distance between the detector and the source in °Angstrom
substrate_depth = 5000                              # depth of the implantation substrate in °Angstrom
dist = 0*(1.785 + 0.15 + 0.1) * 10**8
#0.19455076458356202
r_det = math.sqrt(300/math.pi) * 10**7              # radius of the detector in °Angstrom
E_Fr = 6.45847*10**6                          # energy of the alpha decay of the recoil particle in eV
E_At = 7.2013*10**6
E_Bi = 5.988*10**6
E_Po = 8.536*10**6
E_0 = 0
N = 10**2
Ac_total = 0
Fr_total = 0
At_total = 0
Bi_total = 0
Po_total = 0

Ac_direct = 0
Fr_1recoil = 0
At_2recoil1 = 0
At_2recoil2 = 0
Bi_extra = 0
Po_extra = 0

Fr_direct = 0
At_1recoil = 0
Bi_2recoil1 = 0
Bi_2recoil2 = 0
Po_2recoil = 0

At_direct = 0
Bi_1recoil = 0
Po_1recoil = 0
Po_direct = 0
Bi_direct = 0


E = []

for i in range(N):
    print(i)
    file_name_alpha_Ac = 'easyread_Ac_alpha_60realbeam'
    file_name_recoil_Fr = 'easyread_Fr_recoil_60realbeam'
    results1 = spectrum_efficiency(dist, r_det, E_Fr, E_At, E_0, 1, 1, 1, file_name_alpha_Ac, file_name_recoil_Fr, save_path)
    Ac_direct += results1[0]/N
    Fr_1recoil += results1[1]/N
    At_2recoil1 += results1[2]/N
    At_2recoil2 += results1[3]/N
    Bi_extra += results1[5]/N
    Po_extra += results1[6]/N
    
    file_name_alpha_Fr = 'easyread_Fr_alpha_60realbeam'
    file_name_recoil_At = 'easyread_At_recoil_60realbeam'
    results2 = spectrum_efficiency(dist, r_det, E_At, E_Bi, E_Po, 1, 1, 0.022, file_name_alpha_Fr, file_name_recoil_At, save_path)
    Fr_direct += results2[0]/N
    At_1recoil += results2[1]/N
    Bi_2recoil1 += results2[2]/N
    Bi_2recoil2 += results2[3]/N
    Po_2recoil += results2[4]/N
    
    
    file_name_alpha_At = 'easyread_At_alpha_60realbeam'
    file_name_recoil_Bi = 'easyread_Bi_recoil_60realbeam'
    results3 = spectrum_efficiency(dist, r_det, E_Bi, E_0, E_Po, 1, 0.022, 1, file_name_alpha_At, file_name_recoil_Bi, save_path)
    At_direct += results3[0]/N
    Bi_1recoil += results3[1]/N
    Po_1recoil += results3[4]/N
    
    file_name_alpha_Bi = 'easyread_Bi_alpha_60realbeam'
    file_name_recoil_0 = 'easyread_0_recoil_60realbeam'
    results4 = spectrum_efficiency(dist, r_det, E_0, E_0, E_0, 0.022, 1, 1, file_name_alpha_Bi, file_name_recoil_0, save_path)
    Bi_direct += results4[0]/N
    
    file_name_alpha_Po = 'easyread_Po_alpha_60realbeam'
    results5 = spectrum_efficiency(dist, r_det, E_0, E_0, E_0, 0.978, 1, 1, file_name_alpha_Po, file_name_recoil_0, save_path)
    Po_direct += results5[0]/N
    
    for i in results1[7]:
        E.append(i*10**-6)
    for j in results2[7]:
        E.append(j*10**-6)
    for k in results3[7]:
        E.append(k*10**-6)
    for l in results4[7]:
        E.append(l*10**-6)
    for m in results5[7]:
        E.append(m*10**-6)
        
Ac_total += Ac_direct
Fr_total += Fr_direct + Fr_1recoil
At_total += At_direct + At_1recoil + At_2recoil1 + At_2recoil2
Bi_total += Bi_direct + Bi_1recoil + Bi_2recoil1 + Bi_2recoil2 + Bi_extra
Po_total += Po_direct + Po_1recoil + Po_2recoil + Po_extra

print("Ac " + str(Ac_total/10**3) + "%")
print("Fr " + str(Fr_total/10**3) + "%")
print("At " + str(At_total/10**3) + "%")
print("Bi " + str(Bi_total/10**3/0.022) + "%")
print("Po " + str(Po_total/10**3/0.978) + "%")
print("Ac direct " + str(Ac_direct/Ac_total))
print("Fr direct " + str(Fr_direct/Fr_total))
print("At direct " + str(At_direct/At_total))
print("Bi direct " + str(Bi_direct/Bi_total))
print("Po direct " + str(Po_direct/Po_total))

print("Fr primary " + str(Fr_1recoil/Fr_total))
print("At primary " + str(At_1recoil/At_total))
print("Bi primary " + str(Bi_1recoil/Bi_total))
print("Po primary " + str(Po_1recoil/Po_total))

print("At pp second " + str(At_2recoil1/At_total))
print("Bi pp second " + str(Bi_2recoil1/Bi_total))
print("Po second " + str(Po_2recoil/Po_total))
print("At rej second " + str(At_2recoil2/At_total))
print("Bi rej second " + str(Bi_2recoil2/Bi_total))

print("Bi extra " + str(Bi_extra/Bi_total))
print("Po extra " + str(Po_extra/Po_total))


print("Bi direct " + str(Bi_direct/10**3/0.022))
print("Po direct " + str(Po_direct/10**3/0.978))


print("Bi " + str((Bi_total-Bi_extra)/10**3/0.022) + "%")
print("Po " + str((Po_total-Po_extra)/10**3/0.978) + "%")
print("Bi direct low " + str(Bi_direct/(Bi_total-Bi_extra)))
print("Po direct low " + str(Po_direct/(Po_total-Po_extra)))


counts = Ac_total + Fr_total + At_total + Bi_total + Po_total
print("Total " + str(counts/10**3) + "%")
print(str(counts/10**2) + " kHz/MBq(Ac)")
    

FWHM = 17 * 10**-3
sigma = FWHM/2.355
fluctuation = sigma * np.random.randn(len(E))
E_det = []
log_E = []

for i in range(len(fluctuation)):
    E_det.append(E[i] + fluctuation[i])




#plt.hist(results1[2], bins = np.linspace(5*10**6, 7* 10**6, 1000), histtype = u'step', color = 'Blue')
#plt.hist(results2[2], bins = np.linspace(5*10**6, 7* 10**6, 1000), histtype = u'step', color = 'Blue')
plt.hist(E_det, bins = np.linspace(5.5, 9, 200), color = 'Blue', density = True)
plt.xlabel("Energy (MeV)", fontsize = 16)
plt.ylabel("Normalised Count rate", fontsize = 16)
plt.xticks(size = 12)
plt.yticks(size = 12)
plt.grid()
plt.show()
