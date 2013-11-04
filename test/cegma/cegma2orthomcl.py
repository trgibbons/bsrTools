#!/usr/bin/env python

import sys

for line in sys.stdin:
  # Case: Drosophila melanogaster
  if line[0:2] == ">7":
     sys.stdout.write(">Dmela|"+line[1:])
  # Case: Arabidopsis thaliana
  elif line[0:2] == ">A":
     sys.stdout.write(">Athal|"+line[1:])
  # Case: Caenorhabditis elegans
  elif line[0:2] == ">C":
     sys.stdout.write(">Celeg|"+line[1:])
  # Case: Homo sapiens
  elif line[0:2] == ">H":
     sys.stdout.write(">Hsapa|"+line[1:])
  # Case: Schizosaccharomyces pombe
  elif line[0:2] == ">S":
     sys.stdout.write(">Spomb|"+line[1:])
  # Case: Saccharomyces cerevisiae
  elif line[0:2] == ">Y":
     sys.stdout.write(">Scere|"+line[1:])
  else:
     sys.stdout.write(line)

