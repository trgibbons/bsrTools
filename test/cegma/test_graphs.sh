#!/bin/bash

e=3

# All sequences complete
time nice blast2bsrGraph.py \
-n -i '|' \
-s by_org/blastp/Athal-v-Athal_1e-${e}.blastp \
   by_org/blastp/Celeg-v-Celeg_1e-${e}.blastp \
   by_org/blastp/Dmela-v-Dmela_1e-${e}.blastp \
   by_org/blastp/Hsapa-v-Hsapa_1e-${e}.blastp \
   by_org/blastp/Scere-v-Scere_1e-${e}.blastp \
   by_org/blastp/Spomb-v-Spomb_1e-${e}.blastp \
-c by_org/blastp/Athal-v-[CDHS]????_1e-${e}.blastp \
   by_org/blastp/[CDHS]????-v-Athal_1e-${e}.blastp \
   by_org/blastp/Celeg-v-[ADHS]????_1e-${e}.blastp \
   by_org/blastp/[ADHS]????-v-Celeg_1e-${e}.blastp \


