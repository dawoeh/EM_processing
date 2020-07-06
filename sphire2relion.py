##Python script to convert back from sphire to relion##

import sys
import os
import numpy as np


def is_number(s):   ##### definition to check for int
    try:
        int(s)
        return True
    except ValueError:
        return False

print('\nTaking sphire substack id list to convert back to relion!')

i = 1
while i <= len(sys.argv)-1:  ##### extract star file input
	if '-star' in sys.argv[i]:
		if sys.argv[i+1]:
			star_path = str(sys.argv[i+1])
		else:
			break
		break
	else:
		i+=1

i = 1
while i <= len(sys.argv)-1:  ##### extract id file input
	if '-id' in sys.argv[i]:
		if sys.argv[i+1]:
			id_list = str(sys.argv[i+1])
		else:
			break
		break
	else:
		i+=1

while i <= len(sys.argv)-1:  ##### extract star file output
	if '-out' in sys.argv[i]:
		if sys.argv[i+1]:
			star_out = str(sys.argv[i+1])
		else:
			break
		break
	else:
		i+=1

if star_path and id_list and star_out:
	pass
else:
	print("Please define STAR input (-star), sphire id file (-id) and STAR output (-out) properly and check for correct paths!\n")
	quit()


print('\nStar file input: %s' %star_path)
print('ID list: %s' %id_list)
print('Star output: %s' %star_out)

###remove output star file in case it exists already

try:
    os.remove(star_out)
except OSError:
    pass

#####check whether input files exist

if os.path.isfile(star_path):
	pass
else:
	print("\nCan't open input star file! Check path!\n")
	print("EXIT!\n")
	quit()

if os.path.isfile(id_list):
	pass
else:
	print("\nCan't open input id file from sphire substack! Check path!\n")
	print("EXIT!\n")
	quit()

####create star file output

part_id = np.loadtxt(id_list, dtype=int)

i=0

with open(star_out, 'a') as out_file:
	with open (star_path, 'rt') as in_file:
		for line in in_file:
			if line.find('.mrc') != -1:
				if i in part_id:
					out_file.write(line)
				i+=1
			else:
				out_file.write(line)
	
print('\nDONE!\n')
