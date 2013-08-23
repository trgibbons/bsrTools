#!/usr/bin/env python

# Standard Python libraries
import sys
import argparse

# Third part libraries
import networkx as nx


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
  parser = argparse.ArgumentParser(description='Compute a set of Bit Score Ratios from either BLASTP or BLASTN hits')
 
  # Input files
  parser.add_argument('-s', '--self', dest='self', nargs='+',
                      help='Tab-delimited BLAST files containing')
  parser.add_argument('-c', '--cross', dest='cross', nargs='+',
                      help='Minimum protein length in amino acids (def=30, off=0)')
  parser.add_argument('-b', '--both', dest='both', nargs='+',
                      help='Fraction of the length of the longest ORF that subsequent ORFs much reach (def=0.50, off=0)')

  # Unidirectional vs. reciprocal Bit Score Ratio
  parser.add_argument('-r', '--reciprocal', dest='reciprocal', action='store_true', default=False,
                      help='Maximum number of translated ORFs to output from each sequence [def=false]')

  # Yet to be implemented options
  parser.add_argument('-i', '--ids', dest='ids', action='store',
                      help='Either a text file containing a list of organisms IDs, which must occur at the beginning of each sequence ID, or the character used to separate the organism IDs from the rest of sequence IDs (eg. "|")')
  parser.add_argument('-n', '--normalize', dest='normalize', action='store_true', default=False,
                      help='Normalize edge weights according to intra- and inter-organism averages (requires the "-i" option)')
  parser.add_argument('-m', '--merge', dest='merge', action='store_true', default=False,
                      help='Merge sequences from a single organism when they have non-overlapping alignments to the same target sequence (helpful for highly-fragmented assemblies, requires the "-i" option)')
  parser.add_argument('--bscol', dest='bscol', action='store', type=int, default=12,
                      help='One-indexed column containing pairwise bit scores (not required if files include standard header lines) [def=12]')
  parser.add_argument('-t', '--translated', action='store_true', default=False,
                      help='One or more of the data sets were bioinformatically translated by BLAST (requires the "-i" option be used with a file containing a second column specifying either "nuc" or "pro" for each organism ID listed in the first column')
  parser.add_argument('--hmmer', dest='hmmer', action='store_true', default=False,
                      help="Alignment files are in HMMer format, not BLAST (not required if files include standard header lines) -- Actually, I've decided to create separate BLAST and HMMer programs")

  args = parser.parse_args()

  catch_argument_errors(args)

  return args



# Get bit scores from full-length self-alignments
def get_self_bit_scores(BSRgraph, selfBlastFiles, bscol):
  for file in selfBlastFiles:
    for line in open(file, "r"):
      if line[0] == "#":
        continue
      temp = line.rstrip().split()
      if temp[0] == temp[1]:
        seqID = str(temp[0])
        bitScore = int(float(temp[bscol]))
        if not BSRgraph.has_node(seqID):
          BSRgraph.add_node(seqID, sbs=bitScore, org=None)
        elif bitScore > BSRgraph.node[seqID]['sbs']:
          BSRgraph.node[seqID]['sbs'] = bitScore



# Get bit scores from non-self alignments
def get_cross_bit_scores(BSRgraph, crossBlastFiles, bscol):
  for file in crossBlastFiles:
    for line in open(file, "r"):
      if line[0] == "#":
        continue
      temp = line.rstrip().split()
      if temp[0] != temp[1]:
        qID = str(temp[0])
        rID = str(temp[1])
        bitScore = int(float(temp[bscol]))
        if BSRgraph.has_node(qID) and BSRgraph.has_node(rID):
          if not BSRgraph.has_edge(qID, rID):
            BSRgraph.add_edge(qID, rID, weight=bitScore)
          elif bitScore > BSRgraph[qID][rID]['weight']:
            BSRgraph[qID][rID]['weight'] = bitScore



# Convert Bit Scores into Bit Score Ratios and account for intra-/inter- organism differences, if requested
def adjust_edge_weights(BSRgraph, ids, reciprocal, normalize):
  for u,v,edata in BSRgraph.edges(data=True):
    if reciprocal:
      BSRgraph[u][v]['weight'] = float(edata['weight']) / float(max(BSRgraph.node[u]['sbs'],BSRgraph.node[v]['sbs']))
    else:
      BSRgraph[u][v]['weight'] = float(edata['weight']) / float(min(BSRgraph.node[u]['sbs'],BSRgraph.node[v]['sbs']))



# Print graph for MCL
def print_mcl_input_file(BSRgraph):
  for line in nx.generate_edgelist(BSRgraph, delimiter='\t', data=['weight']):
    sys.stdout.write(line+'\n')





def main(argv=None):
  if argv == None:
    argv = sys.argv
 
  args = get_parsed_args() 

  BSRgraph = nx.Graph()

  if args.self and args.both:
    selfBlastFiles = args.self+args.both
  elif args.self:
    selfBlastFiles = args.self
  elif args.both:
    selfBlastFiles = args.both

  get_self_bit_scores(BSRgraph, selfBlastFiles, args.bscol-1)

  if args.cross and args.both:
    crossBlastFiles = args.cross+args.both
  elif args.cross:
    crossBlastFiles = args.cross
  elif args.both:
    crossBlastFiles = args.both

  get_cross_bit_scores(BSRgraph, crossBlastFiles, args.bscol-1)

  adjust_edge_weights(BSRgraph, args.ids, args.reciprocal, args.normalize)

  print_mcl_input_file(BSRgraph)





# Executing the main function this way allows the script to be called repeatedly
# in an interactive shell without closing the session
if __name__ == "__main__":
  sys.exit(main())

