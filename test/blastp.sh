#!/bin/bash

# Format each test file as a BLASTp database
for file in rvt[12]seed.fasta
do
  makeblastdb -in $file -dbtype prot
done

# Generate all-v-all BLASTp alignments
for file1 in rvt[12]seed.fasta
do
  for file2 in rvt[12]seed.fasta
  do
    nice blastp \
    -query ${file1} \
    -db ${file2} \
    -out ${file1%.fasta}-v-${file2%.fasta}.blastp \
    -evalue 1e-3 \
    -outfmt '7 std qlen slen' \
    -soft_masking true &
  done
done

