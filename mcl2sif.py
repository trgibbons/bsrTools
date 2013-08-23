#!/usr/bin/env python

# Standard libraries
import sys
import argparse

# Third-party libraries
import networkx as nx



# Parse the commandline arguments 
def get_parsed_args():
   
  # Initialize argument parser
  parser = argparse.ArgumentParser(description='Compute a set of Bit Score Ratios from either BLASTP or BLASTN hits')
   
  # Input options
  parser.add_argument('-c', '--clusters', dest='clusters', nargs='+',
                      help='One or more files containing rows of sequence IDs corresponding to clusters')
  parser.add_argument('-g', '--graphs', dest='graphs', nargs='+',
                      help='One or more files containing edge information')

  # Output options
  parser.add_argument('-o', '--out', dest='out',
                      help='Prefix for output files')
  parser.add_argument('-l', '--label', dest='label',
                      help='Label for Cytoscape edge type')

  # Unimplemented options
  parser.add_argument('--cluster_ids', dest='cluster_ids', action='store_true', default=False,
                      help='If true, then the first column of each cluster file is assumed to contain cluster IDs instead of sequence IDs [def=false]')

  args = parser.parse_args()
   
  return args





def main(argv=None):
  if argv == None:
    argv = sys.argv
   
  args = get_parsed_args()

  clusters = nx.Graph()
  for file in args.clusters:
    for line in open(file, "r"):
      temp = line.rstrip().split()
      for u in temp:
        for v in temp:
          if u != v:
            clusters.add_edge(u,v)

  sifOut = open(args.out+'.sif', "w")
  #for component in nx.connected_components(clusters):
  #  if len(component) > 1:
  #    nodeList = sorted(component)
  #    sifOut.write(str(nodeList[0])+'\t'+str(args.label)+'\t'+'\t'.join(nodeList[1:])+'\n')

  propsOut = open(args.out+'.props', "w")
  for file in args.graphs:
    for line in open(file, "r"):
      temp = line.rstrip().split()
      if clusters.has_edge(temp[0], temp[1]):
        sifOut.write(str(temp[0])+'\t'+str(args.label)+'\t'+str(temp[1])+'\n')
        propsOut.write(str(temp[0])+'\t('+str(args.label)+')\t'+str(temp[1])+'\t'+'\t'.join(temp[2:])+'\n')
  propsOut.close()
  sifOut.close()





# Executing the main function this way allows the script to be called repeatedly
# in an interactive shell without closing the session
if __name__ == "__main__":
  sys.exit(main())

