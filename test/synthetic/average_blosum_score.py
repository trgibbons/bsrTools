#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 13:46:05 2013

@author: tgibbons
"""

import sys
import pandas as pd


def main(argv=None):
  if argv == None:
    argv = sys.argv

  bl62 = pd.read_table("BLOSUM62.txt", sep=r'\s+',
                       header=0, index_col=0, skiprows=6)

  pos_cnt = 0
  pos_sum = 0
  neg_cnt = 0
  neg_sum = 0

  for aa1 in bl62.index:
    for aa2 in bl62.index:
      if bl62[aa1][aa2] < 0:
        neg_cnt += 1
        neg_sum += bl62[aa1][aa2]
      else:
        pos_cnt += 1
        pos_sum += bl62[aa1][aa2]
      if aa1 == aa2:
        break

  pos_avg = float(pos_sum) / float(pos_cnt)
  neg_avg = float(neg_sum) / float(neg_cnt)
  ttl_cnt = pos_cnt + neg_cnt
  ttl_sum = pos_sum + neg_sum
  ttl_avg = float(ttl_sum) / float(ttl_cnt)

  sys.stdout.write("Positive score count: \t%s\n" % (pos_cnt))
  sys.stdout.write("Positive score sum:   \t%s\n" % (pos_sum))
  sys.stdout.write("Positive score mean:  \t%.2f\n" % (pos_avg))
  sys.stdout.write("Negative score count: \t%s\n" % (neg_cnt))
  sys.stdout.write("Negative score sum:   \t%s\n" % (neg_sum))
  sys.stdout.write("Negative score mean:  \t%.2f\n" % (neg_avg))
  sys.stdout.write("Total score count: \t%s\n" % (ttl_cnt))
  sys.stdout.write("Total score sum:   \t%s\n" % (ttl_sum))
  sys.stdout.write("Total score mean:  \t%.2f\n" % (ttl_avg))


if __name__ == "__main__":
  sys.exit(main())