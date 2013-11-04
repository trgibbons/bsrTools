#!/usr/bin/env python

import os
import sys
from Bio import SeqIO

# Usage message
if len(sys.argv) < 2:
  print "Usage:"
  print "\tsplit_cegma_into_kogs.py <cegma/data/kogs.fa>"
  sys.exit()

kog_dir = "cegma_kogs"
if not os.path.exists(kog_dir):
  os.makedirs(kog_dir)

kog_file = {}

for record in SeqIO.parse(open(sys.argv[1], "r"), "fasta"):
  kog = str(record.id).split('___')[1]
  if kog in kog_file:
    kog_file[kog].write(">"+str(record.id)+"\n"+str(record.seq)+"\n")
  else:
    kog_file[kog] = open(kog_dir+"/"+kog+".fa", "w")
    kog_file[kog].write(">"+str(record.id)+"\n"+str(record.seq)+"\n")

for handle in kog_file:
  kog_file[handle].close()

sys.exit()

