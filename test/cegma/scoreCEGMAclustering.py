#!/usr/bin/env python

import sys
import re

cluster_handle = open(sys.argv[1], 'r')

for line in cluster_handle:
  seqs = line.strip().split()
  kog_counts = dict()

  for seq in seqs:
    kog = re.search('KOG\d+', seq).group()
    try:
      kog_counts[kog] += 1
    except KeyError:
      kog_counts[kog] = 1

  out_line = ''
  for k, v in sorted(kog_counts.iteritems()):
    out_line += str(k)+':'+str(v)+'\t'
  print out_line.rstrip()