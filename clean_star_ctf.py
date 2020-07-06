##Python script to clean Relion CtfFind output star file##
##Usage: run script in folder with micrographs_ctf.star file or use -star argument##
##Essential arguments: -min (minimal defocus) -max (maximal defocus) -res (resolution cutoff)##

import sys
import os
import re
import numpy as np


def is_number(s):   ##### def to check for floats
    try:
        float(s)
        return True
    except ValueError:
        return False

print('\nTaking Relion3 CtfFind output star file (i.e. micrographs_ctf.star) and clean it from bad micrographs!')

i = 1
while i <= len(sys.argv)-1:  ##### check star file input, if not supplied then take micrographs_ctf.star
	if '-star' in sys.argv[i]:
		if sys.argv[i+1]:
			star_path = str(sys.argv[i+1])
		else:
			break
		break
	else:
		i+=1

i = 1
while i <= len(sys.argv)-1:  ##### check for minimal defocus argument
	if '-min' in sys.argv[i]:
		if is_number(sys.argv[i+1]):
			defocus_min = float(sys.argv[i+1])
		else:
			break
		break
	else:
		i+=1

i = 1
while i <= len(sys.argv)-1:  ##### check for maximal defocus argument
	if '-max' in sys.argv[i]:
		if is_number(sys.argv[i+1]):
			defocus_max = float(sys.argv[i+1])
		else:
			break
		break
	else:
		i+=1

i = 1
while i <= len(sys.argv)-1:  ##### check for resolution cutoff argument
	if '-res' in sys.argv[i]:
		if is_number(sys.argv[i+1]):
			ctf_res = float(sys.argv[i+1])
		else:
			break
		break
	else:
		i+=1

try: 
	if defocus_min and defocus_max and ctf_res:
		pass
except NameError:
	print("\nPlease define defocus range (-min and -max) as well as the resolution cutoff (-res) properly!\n")
	print("Example: python2.7 clean_ctf_star.py -res 4.0 -min 10000 -max 30000\n")
	print("EXIT!")
	quit()

print('\nMinimal defocus: %d' %defocus_min)
print('Maximal defocus: %d' %defocus_max)
print('CTF Resolution cutoff: %0.1f' %ctf_res)

try:
	if star_path:
		print("\nWill use %s as star file input" %star_path) #### use star file provided by user
except NameError:
	print("\nWill use micrographs_ctf.star from execution folder as star file input!")
	star_path = 'micrographs_ctf.star' ##### use micrographs_ctf.star file instead

if os.path.isfile(star_path):
	pass
else:
	print("\nCan't open input star file! Check path!\n")
	print("EXIT!\n")
	quit()

with open (star_path, 'rt') as in_file:
	for line in in_file:
		if line.find('.mrc') != -1:
			break
		else:
			if line.find('_rln') != -1:
				splitline = line.split()
				if splitline[0] ==  '_rlnDefocusU':
					star_defocus_list = re.findall(r'\d+', splitline[1])
					for i in star_defocus_list:
						if is_number(i):
							star_defocus = int(i) - 1
				if splitline[0] ==  '_rlnCtfMaxResolution':
					star_res_list = re.findall(r'\d+', splitline[1])
					for i in star_res_list:
						if is_number(i):
							star_res = int(i) - 1

try: 
	if star_res and star_defocus:
		print('Found defocus in column %d and maximal resolution in column %d of input star file!' %(star_defocus, star_res))
except NameError:
	print("\nCould not find defocus column (_rlnDefocusU) or resolution estimate (_rlnCtfMaxResolution) in star file!\n")
	print("EXIT!")
	quit()

count = 0
micrographs=[]
micrographs_focus=[]
micrographs_ctfres=[]

with open (star_path, 'rt') as in_file:
	for line in in_file:
		if line.find('.mrc') != -1:
			splitline = line.split()
			head, tail = os.path.split(splitline[0])
			if defocus_min < float(splitline[star_defocus]) < defocus_max:  #####star file entry #3 corresponds to defocus
				if float(splitline[star_res]) < ctf_res:				######star file entry #13 corresponds to 
high-resolution estimate
					micrographs = np.append(micrographs, tail)
				else:
					micrographs_ctfres = np.append(micrographs_ctfres, tail)
			else:
				micrographs_focus = np.append(micrographs_focus, tail)
			count+=1

print('\nNumber of micrographs within defocus and resolution estimate cutoff: %d' %len(micrographs))
print('Rejected micrographs: %d' %(count - len(micrographs)))

try:
    os.remove('micrographs_ctf_cleaned.star')
except OSError:
    pass

with open('micrographs_ctf_cleaned.star', 'a') as out_file:
	with open (star_path, 'rt') as in_file:
		for line in in_file:
			if line.find('.mrc') != -1:
				splitline = line.split()
				head, tail = os.path.split(splitline[0])
				if tail in micrographs:
					out_file.write(line)
			else:
				out_file.write(line)

np.savetxt('bad_focus.txt',micrographs_focus,fmt="%s")
np.savetxt('bad_ctf_res.txt',micrographs_ctfres,fmt="%s")
np.savetxt('good_micrographs.txt',micrographs,fmt="%s")

print('\nFinished writing of txt files with micrograph names and micrographs_ctf_cleaned.star!')

print('\nDONE!')
