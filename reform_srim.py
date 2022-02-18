import os.path
import re

# this function reforms ion range SRIM output to a more convenient form for processing
def reform_R(save_path, name_in, name_out):
    complete_name_in = os.path.join(save_path, name_in) 
    complete_name_out = os.path.join(save_path, name_out) 
    fin = open(complete_name_in, "r")
    fout = open(complete_name_out, "w")

    start_data = False
    for line in fin:
        if start_data:
            fout.write(re.sub(',', '.', re.sub('\s+', ' ', re.sub('E', 'e', line))) + "\n")
        elif line.startswith("-------"):
            start_data = True

    print("reformed SRIM file with single space separation: ion x y z")
    fin.close()
    fout.close()

# this function reforms transmission SRIM output to a more convenient form for processing --> Should also work for backscattering files (I think)
def reform_T(save_path, name_in, name_out):
    complete_name_in = os.path.join(save_path, name_in) 
    complete_name_out = os.path.join(save_path, name_out) 
    fin = open(complete_name_in, "r")
    fout = open(complete_name_out, "w")

    start_data = False
    for line in fin:
        if start_data:
            fout.write(re.sub(',', '.', re.sub('\s+', ' ', re.sub('E', 'e', re.sub('T', 'T ' ,line)))) + "\n")
        elif line.startswith(" Numb"):
            start_data = True

    print("reformed SRIM file with: T ion atom E xyz dir(xyz)")
    fin.close()
    fout.close()


save_path = '/mnt/ksf9/H2/user/u0148069/share/my.public/SRIM_scripts/output/'

name_in = "range_Ac_implant_test.txt"
name_out = "easyread_range_test.txt"
reform_R(save_path, name_in, name_out)

name_in = "transmission_Ac_alpha_test.txt"
name_out = "easyread_transmission_test.txt"
reform_T(save_path, name_in, name_out)

