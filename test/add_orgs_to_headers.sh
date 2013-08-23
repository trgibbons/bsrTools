#!/bin/bash

# Do not re-run this script!!

for file in rvt[12]seed.fasta
do
  sed -i "s/^>/>${file%.fasta}_/g" ${file}
done

