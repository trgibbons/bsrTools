#!/usr/bin/env python

'''
Usage:
  ./chop_seqs.py [num_pieces] < input.fasta > output.fasta
'''

import sys
import argparse

from Bio import SeqIO



# Attempt to catch errors with inputs
def catch_argument_errors(args):
  kill = 0

  if not len(args.both) > 0:
    if not len(args.self)>0 and len(args.cross)>0:
      sys.stderr.write('Must have at least one file flagged as "both", or at least one each flagged as "self" and "cross", repectively.\n')
      kill += 1

  if not args.ids:
    if args.normalize:
      sys.stderr.write('The "--normalize" option requires the "--ids" option.\n')
      kill += 1
    if args.merge:
      sys.stderr.write('The "--merge" option requires the "--ids" option.\n')
      kill += 1
    if args.translated:
      sys.stderr.write('The "--translated" option requires the "--ids" option.\n')
      kill += 1

  if kill > 0:
    sys.exit()



# Parse the commandline arguments 
def get_parsed_args():
 
  # Initialize argument parser
  parser = argparse.ArgumentParser(description='Chop FASTA-formatted sequences into a specified number of subsequences of equal or random length, or an unspecified number of subsequences of a specified length',
                                   epilog='For additional help, visit the bsrTools wiki https://github.com/trgibbons/bsrTools/wiki')
 
  # Input files
  parser.add_argument('-i', '--inputs', dest='inputs', action='append', nargs='+',
                      help='One or more FASTA-formatted input files')
  parser.add_argument('-o', '--output', dest='output',
                      help='Output file name')

  parser.add_argument('-e', '--even', dest='even', action='store', type=int,
                      help='Split sequences into INT subsequences of equal length')
  parser.add_argument('-r', '--random', dest='random', action='store', type=int,
                      help='Split sequences into INT subsequences of (pseudo)random length')
  parser.add_argument('-l', '--length', dest='length', action='store', type=int,
                      help='Split sequences into subsequences of length INT')

  args = parser.parse_args()

  catch_argument_errors(args)

  return args



fragCount = int(sys.argv[1])

for record in SeqIO.parse(sys.stdin, "fasta"):
  #sys.stderr.write('>'+str(record.description)+'\n'+str(record.seq)+'\n')
  seqLen = len(str(record.seq))
  fragLen = int(seqLen/fragCount)
  for i in range(fragCount):
    fragHead = '>'+str(record.description)+'-'+str(i+1)+'of'+str(fragCount)
    if i == fragCount-1:
      fragSeq = str(record.seq)[fragLen*i:]
    else:
      fragSeq = str(record.seq)[fragLen*i:fragLen*(i+1)]
    #sys.stderr.write(' '*fragLen*i+fragHead+'\n'+' '*fragLen*i+fragSeq+'\n')
    sys.stdout.write(fragHead+'\n'+fragSeq+'\n')

