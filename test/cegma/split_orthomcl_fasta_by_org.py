#!/usr/bin/env python

import sys

outHandles = dict()

currentOrg = ''
for line in sys.stdin:
  if line[0] == '>':
    currentOrg = line.lstrip('>').split('|')[0]
    if not currentOrg in outHandles:
      outHandles[currentOrg] = open('cegma_kogs-'+currentOrg+'.fasta', 'w')
    outHandles[currentOrg].write(line)
  else:
    outHandles[currentOrg].write(line)

