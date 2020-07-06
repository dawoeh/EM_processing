##Python script to regroup particles in star file##

import sys
import os
import re
import numpy as np


def is_number(s):   ##### definition to check for floats
    try:
        float(s)
        return True
    except ValueError:
        return False

print('\nTaking Relion3 star file and regroup particles according to txt file input!')

i = 1
while i <= len(sys.argv)-1:  ##### check for minimal defocus argument
	if '-txt' in sys.argv[i]:
		if (sys.argv[i+1]):
			txt_input = sys.argv[i+1]
		else:
			break
		break
	else:
		i+=1

i=1
while i <= len(sys.argv)-1:  ##### check for minimal defocus argument
	if '-star' in sys.argv[i]:
		if (sys.argv[i+1]):
			star_input = sys.argv[i+1]
		else:
			break
		break
	else:
		i+=1

i=1
while i <= len(sys.argv)-1:  ##### check for minimal defocus argument
	if '-star_out' in sys.argv[i]:
		if (sys.argv[i+1]):
			star_out = sys.argv[i+1]
		else:
			break
		break
	else:
		i+=1

i = 1
while i <= len(sys.argv)-1:  ##### check for minimal defocus argument
	if '-split' in sys.argv[i]:
		if is_number(sys.argv[i+1]):
			split_micro = int(sys.argv[i+1])
		else:
			break
		break
	else:
		i+=1

try: 
	if txt_input and star_input and split_micro and star_out:
		pass
except NameError:
	print("\nPlease define input/output files (-txt -star -star_out) and split for micrographs (-split) properly!\n")
	print("Example: python2.7 clean_ctf_star.py -txt test.star -star particles.star \n")
	print("EXIT!")
	quit()

print('\nInput star file: %s' %star_input)
print('Input txt file: %s' %txt_input)
print('Regroup every micrographs: %d' %split_micro)
print('Output star file: %s' %star_out)

if len(star_input)==0:
	print("No files to process! Define star file properly!\n")
	quit()

count = 0

with open (star_input, 'rt') as in_file:
	for line in in_file:
		if line.find('.mrc') != -1:
			break
		else:
			if line.find('_rln') != -1:
				splitline = line.split()
				if splitline[0] ==  '_rlnMicrographName':
					column = re.findall(r'\d+', splitline[1])
					for i in column:
						if is_number(i):
							star_name = int(i) - 1
				if splitline[0] ==  '_rlnGroupNumber':
					column = re.findall(r'\d+', splitline[1])
					for i in column:
						if is_number(i):
							star_group = int(i) - 1

try: 
	if star_name and star_group:
		print('\nFound defocus in column %d and maximal resolution in column %d of input star file!' %(star_name, star_group))
except NameError:
	print("\nCould not find defocus column (_rlnMicrographName) or resolution estimate (_rlnGroupNumber) in input star file!\n")
	print("EXIT!")
	quit()

name_group=np.array([]).reshape(0,2)

with open (txt_input, 'rt') as in_file:
	k = 0
	group = 1
	for line in in_file:
		if k < split_micro:
			splitline = line.split()
			head, tail = os.path.split(splitline[0])
			name_group = np.vstack([name_group,[tail,group]])
			k += 1
		if k == split_micro:
			k = 0
			group += 1

try:
    os.remove(star_out)
except OSError:
    pass

with open (star_out, 'a') as out_file:
	with open (star_input, 'rt') as in_file:
		for line in in_file:
			if line.find('.mrc') != -1:
				splitline = []
				splitline = line.split()
				head, tail = os.path.split(splitline[star_name])
				x,y = np.where(name_group==tail)
				splitline[star_group] = str(int(name_group[x,1]))
				joinline = ' '.join(splitline)
				out_file.write(joinline)
				out_file.write('\n')
			else:
				out_file.write(line)


print('\nDONE!')
