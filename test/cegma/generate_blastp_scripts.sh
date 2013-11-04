#!/bin/bash

outDir=/N/dc/scratch/trgibbon/clustering/cegma

for fasta1 in /N/u/trgibbon/Mason/clustering/cegma/by_org/*.fasta
do
  base1=`basename ${fasta1%.fasta}`
  for fasta2 in /N/u/trgibbon/Mason/clustering/cegma/by_org/*.fasta
  do
    base2=`basename ${fasta2%.fasta}`

cat > /N/u/trgibbon/Mason/clustering/cegma/by_org//blastp/blastp_${base1}-v-${base2}.pbs << FILE1-v-FILE2_SCRIPT
#!/bin/bash

#PBS -q shared
#PBS -l nodes=1:ppn=1,vmem=1gb,walltime=1:00:00
#PBS -m abe -M ted.codes@gmail.com
#PBS -N clustering/cegma/by_org/blastp/blastp_${base1}-v-${base2}

blastp \\
-query ${fasta1} \\
-db ${fasta2} \\
-out ${outDir}/${base1}-v-${base2}.blastp \\
-evalue 1e-3 \\
-outfmt '7 std qlen slen' \\
-soft_masking true

exit 0;
FILE1-v-FILE2_SCRIPT

  done 
done

