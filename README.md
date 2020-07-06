# EM processing scripts
This repository contains a few Python scripts for cryo EM processing.

# clean_star_ctf.py
Python2.7 script to read and clear a star file after CTF correction. txt files will be written with micrograph names that either do not fulfill the defocus (bad_focus.txt) or resolution criterion (bad_ctf_res.txt). A file with good mircographs (good_micrographs.txt) will be written out too.

Essential arguments: -min (minimal defocus) -max (maximal defocus) -res (resolution cutoff)

USAGE:
python clean_star_ctf.py -star micrographs_ctf.star -min 10000 -max 25000 -res 4.0

# regroup_star.py
The script regroups particles according to micrograph names. A txt file list with sorted micrograph names is required.

Essential arguments: -star (input star file) -txt (list of ordered micrographs) -split (how many micrographs to group) -star_out (output file name)

USAGE:
python regroup_star.py -star particles.star -txt files.txt -split 3 -star_out particles_regrouped.star

# sphire2relion.py

The script converts a particle stack back from SPHIRE to RELION star format.

Essential arguments: -star (initial star file used for import to SPHIRE) -id (SPHIRE id file of particles) -out (output name for star file)

USAGE:
python sphire2relion.py -star particles.star -id isac_substack_particle_id_list.txt -out particles_reimport.star 
