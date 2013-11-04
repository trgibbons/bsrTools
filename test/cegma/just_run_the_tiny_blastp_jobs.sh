#!/bin/bash

outDir=~/Dropbox/github/bsrTools/test/cegma/by_org/blastp
e=5

for fasta1 in ~/Dropbox/github/bsrTools/test/cegma/by_org/*.fasta
do
  base1=`basename ${fasta1%.fasta}`

  for fasta2 in ~/Dropbox/github/bsrTools/test/cegma/by_org/*.fasta
  do
    base2=`basename ${fasta2%.fasta}`

    # Avoid aligning sequences from the same organism that differ only in the number of times they've been fragmented
    if [[ ${base1:0:5} == ${base2:0:5} && ${base1} != ${base2} ]]
    then
      continue
    else
      time nice blastp \
      -query ${fasta1} \
      -db ${fasta2} \
      -out ${outDir}/${base1}-v-${base2}_1e-${e}.blastp \
      -evalue 1e-${e} \
      -outfmt '7 std qlen slen' \
      -soft_masking true
    fi
  done 
done

