#!/usr/bin/env python

# Standard Python libraries
import sys
import os
import argparse

# Third-party libraries
import networkx as nx


def catch_argument_errors(args):
  """Attempt to catch argument and file format errors

  Args:
    args: The argparse.Namespace object returned by get_parse_args

  Returns:
    None (hopefully)

  Raises:
    TODO: Implement proper Python exception handling
  """
  kill_switch = 0

  if os.fstat(args.both.fileno()).st_size == 0:
    args.both = False
    if not len(args.self)>0 and len(args.cross)>0:
      sys.stderr.write(
        'Must have at least one file flagged as "both", or at least one each '+
        'flagged as "self" and "cross", repectively.\n')
      kill_switch += 1

  if not args.idchar or args.idlist:
    if args.normalize:
      sys.stderr.write(
        'The "--normalize" option requires the "--idchar" and/or "--idlist" '+
        'option(s).\n')
      kill_switch += 1
    if args.translated:
      sys.stderr.write(
        'The "--translated" option requires the "--idchar" and/or "--idlist" '+
        'option(s).\n')
      kill_switch += 1
    if args.merge:
      sys.stderr.write(
        'The "--merge" option requires the "--idchar" and/or "--idlist" '+
        'option(s).\n')
      kill_switch += 1

  if kill_switch > 0:
    sys.exit()


def get_parsed_args():
  """Parse the command line arguments

  Parses command line arguments using the argparse package, which is a standard
  Python module starting with version 2.7.

  Args:
    None, argparse fetches them from user input

  Returns:
    args: An argparse.Namespace object containing the parsed arguments

  Raises:
    None
  """
  parser = argparse.ArgumentParser(
             description='Compute a set of Bit Score Ratios from either '+
                         'BLASTP or BLASTN hits')

  # Group: IO options
  parser.add_argument('-s', '--self', dest='self', nargs='+',
                      type=argparse.FileType('r'),
                      help='Tab-delimited BLAST file(s) containing self '+
                           'alignments (non-self alignments will be ignored)')
  parser.add_argument('-c', '--cross', dest='cross', nargs='+',
                      type=argparse.FileType('r'),
                      help='Tab-delimited BLAST file(s) containing non-self '+
                           'alignments (self alignments will be ignored)')
  parser.add_argument('-b', '--both', dest='both', nargs='?',
                      type=argparse.FileType('r'), default=sys.stdin,
                      help='Tab-delimited BLAST file containing a combination '+
                           'of self and non-self alignments [def=stdin]')
  parser.add_argument('-o', '--out', dest='out', nargs='?',
                      type=argparse.FileType('w'), default=sys.stdout,
                      help='Name for MCL-formatted graph output file '+
                           '[def=stdout]')
  parser.add_argument('-d', '--debug', dest='debug',
                      type=argparse.FileType('w'), default=False,
                      help='File for capturing debug messages')

  # Group: Formatting options
  parser.add_argument('--bscol', dest='bscol',
                      action='store', type=int, default=12,
                      help='One-indexed column containing pairwise bit scores '+
                           '(not required if files include standard header '+
                           'lines) [def=12]')
  parser.add_argument('--idchar', dest='idchar', action='store',
                      help='The character used to separate the organism ID '+
                           'from the rest of the sequence header (eg. "|")]')
  parser.add_argument('--idlist', dest='idlist', action='store',
                      help='Text file containing a list of organisms IDs, '+
                           'which must occur at the beginning of each '+
                           'sequence ID ("--idchar" option must also be '+
                           'provided if any IDs are prefixes of other IDs)')

  # Group: Behavioral options
  parser.add_argument('-n', '--normalize', dest='normalize',
                      action='store_true', default=False,
                      help='Normalize edge weights according to intra- and '+
                           'inter-organism averages (requires the "-i" option)')
  parser.add_argument('-r', '--reciprocal', dest='reciprocal',
                      action='store_true', default=False,
                      help='Divide alignment bit score by max(self1,self2) '+
                      'instead of min(self1,self2) for increased stringency '+
                      '[def=false]')

  # Group: TODO
  parser.add_argument('-t', '--translated', action='store_true', default=False,
                      help='One or more of the data sets were '+
                           'bioinformatically translated by BLAST (requires '+
                           'the "--idchar" and/or "--idlist" option(s) be '+
                           'used with a file containing a second column '+
                           'specifying either "nuc" or "pro" for each '+
                           'organism ID listed in the first column')
  parser.add_argument('-m', '--merge', dest='merge',
                      action='store_true', default=False,
                      help='Merge sequences from a single organism when they '+
                           'have non-overlapping alignments to the same '+
                           'target sequence (helpful for highly-fragmented '+
                           'assemblies, requires the "-i" option)')

  args = parser.parse_args()

  catch_argument_errors(args)

  return args


def get_self_bit_scores(bsr_graph, self_handle, bscol):
  """Get bit scores from full-length self-alignments

  Searches an open file for tab-delimited BLAST hit records where the query and
  reference IDs are identical.  It is important that BLAST is run with option
  "--soft_masking true" or the self-alignments are unlikely to be full length.

  Args:
    bsr_graph: A NetworkX graph data structure (does not need to be empty)
    self_handle: An open file handle containing self-alignments (can contain
      other alignments and/or comment lines beginning with a hash '#' character)
    bscol: Column containing the bit scores

  Returns:
    Nothing, the NetworkX graph is edited in place

  Raises:
    None
  """
  for line in self_handle:
    if line[0] == "#":
      continue
    temp = line.rstrip().split()

    if temp[0] == temp[1]:
      seq_id = str(temp[0])
      bitscore = int(temp[bscol])

      if not bsr_graph.has_node(seq_id):
        bsr_graph.add_node(seq_id, sbs=bitscore, org=None)
      elif bitscore > bsr_graph.node[seq_id]['sbs']:
        bsr_graph.node[seq_id]['sbs'] = bitscore


def get_cross_bit_scores(bsr_graph, cross_handle, bscol):
  """Get bit scores from full-length non-self-alignments

  Searches an open file for tab-delimited BLAST hit records where the query and
  reference IDs are not identical. It is important that BLAST is run with option
  "--soft_masking true" or the self-alignments are unlikely to be full length.

  Args:
    bsr_graph: A NetworkX graph data structure containing self-alignment scores
    self_handle: An open file handle containing non-self-alignments (can contain
      other alignments and/or comment lines beginning with a hash '#' character)
    bscol: Column containing the bit scores

  Returns:
    Nothing, the NetworkX graph is edited in place

  Raises:
    None
  """
  for line in cross_handle:
    if line[0] == "#":
      continue
    temp = line.rstrip().split()

    if temp[0] != temp[1]:
      qry_id = str(temp[0])
      ref_id = str(temp[1])
      bitscore = int(float(temp[bscol]))
      if bsr_graph.has_node(qry_id) and bsr_graph.has_node(ref_id):
        if not bsr_graph.has_edge(qry_id, ref_id):
          bsr_graph.add_edge(qry_id, ref_id, weight=bitscore)
        elif bitscore > bsr_graph[qry_id][ref_id]['weight']:
          bsr_graph[qry_id][ref_id]['weight'] = bitscore


def adjust_edge_weights(bsr_graph, reciprocal, normalize, org_ids):
  """Convert Bit Scores into Bit Score Ratios

  Iterates through the edges in a NetworkX graph, dividing all cross-alignment
  scores by either the smaller or larger of the two self-alignment scores

  Convert Bit Scores into Bit Score Ratios and account for intra-/inter- 
  organism differences, if requested
  """
  for u,v,edata in bsr_graph.edges(data=True):
    if reciprocal:
      denom = float(max(bsr_graph.node[u]['sbs'],bsr_graph.node[v]['sbs']))
    else:
      denom = float(min(bsr_graph.node[u]['sbs'],bsr_graph.node[v]['sbs']))

    numer = float(edata['weight'])
    bsr_graph[u][v]['weight'] = numer / denom


# Print graph for MCL
def print_mcl_input_file(bsr_graph, out_handle):
  for line in nx.generate_edgelist(bsr_graph, delimiter='\t', data=['weight']):
    out_handle.write(line+'\n')


# Print debug info
def print_nodes(bsr_graph, debug_handle):
  for node, data in bsr_graph.nodes(data=True):
    debug_handle.write(str(node)+"\t"+repr(data)+"\n")


def main(argv=None):
  if argv == None:
    argv = sys.argv

  args = get_parsed_args() 

  bsr_graph = nx.Graph()
  org_ids = set()

  if args.self:
    for self_handle in args.self:
      get_self_bit_scores(bsr_graph, self_handle, args.bscol-1)

  if args.both:
    get_self_bit_scores(bsr_graph, args.both, args.bscol-1)
    args.both.seek(0)
    get_cross_bit_scores(bsr_graph, args.both, args.bscol-1)

  if args.debug:
    print_nodes(bsr_graph, args.debug)

  if args.cross:
    for cross_handle in args.cross:
      get_cross_bit_scores(bsr_graph, cross_handle, args.bscol-1)

  # TODO: This program will accept either organism IDs, or an organism ID 
  # separator character, but this function will requie that the IDs have 
  # already been determined before this point
  adjust_edge_weights(bsr_graph, args.reciprocal, args.normalize, org_ids)

  print_mcl_input_file(bsr_graph, args.out)


if __name__ == "__main__":
  sys.exit(main())

