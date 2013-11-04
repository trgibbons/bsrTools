#!/bin/bash

inDir=~/Dropbox/github/bsrTools/test/cegma/by_org/blastp
outDir=~/Dropbox/github/bsrTools/test/cegma
e=5

consolidate() {
  orgs=("${@}")
  outFile=${outDir}/$(printf "%s" "${orgs[@]}")_1e-${e}.blastp
  > $outFile
  for org1 in ${orgs[@]}
  do
    for org2 in ${orgs[@]}
    do
      cat ${inDir}/${org1}-v-${org2}_1e-${e}.blastp >> $outFile
    done
  done
}




# All complete
orgs111111=(Athal1f Dmela1f Celeg1f Hsapa1f Scere1f Spomb1f)
consolidate "${orgs111111[@]}"

# Yeast halved
orgs111122=(Athal1f Dmela1f Celeg1f Hsapa1f Scere2e Spomb2e)
consolidate "${orgs111122[@]}"

# Yeast whole
orgs222211=(Athal2e Dmela2e Celeg2e Hsapa2e Scere1f Spomb1f)
consolidate "${orgs222211[@]}"

# 123
orgs112233=(Athal1f Dmela1f Celeg2e Hsapa2e Scere3e Spomb3e)
consolidate "${orgs112233[@]}"


#cat ~/Dropbox/github/bsrTools/test/cegma/by_org/blastp/*1f-v-*1f_1e-5.blastp > ~/Dropbox/github/bsrTools/test/cegma/Athal1fDmela1fCeleg1fHsapa1fScere1fSpomb1f_1e-5.blastp





<<:ORIGINALATTEMPT

################################################################################
#
# This script didn't work the way I expected
# I opted to take a different approach, rather than debug it
#
################################################################################

# Create test files for full-length sequences
for e in 3 5
do
  # Specify output file names
  selfBlastp=AtCeDmHsScSp_self_1e-${e}.blastp
  crossBlastp=AtCeDmHsScSp_cross_1e-${e}.blastp
  bothBlastp=AtCeDmHsScSp_both_1e-${e}.blastp
  # Empty output files
  cat /dev/null > $selfBlastp
  cat /dev/null > $crossBlastp
  cat /dev/null > $bothBlastp
  for org1 in At Ce Dm Hs Sc Sp
  do
    for org2 in At Ce Dm Hs Sc Sp
    do
      if [[ $org1 == $org2 ]]
      then
        # Put self hits in one file...
        cat by_org/blastp/${org1}-v-${org2}_1e-${e}.blastp >> $selfBlastp
      else
        # ...and cross hits in another
        cat by_org/blastp/${org1}-v-${org2}_1e-${e}.blastp >> $crossBlastp
      fi
      cat by_org/blastp/${org1}-v-${org2}_1e-${e}.blastp >> $bothBlastp
    done
  done
done

# Create test files for S.pombe sequences being halved and all others being complete
for e in 3 5
do
  # Specify output file names
  selfBlastp=AtCeDmHsScSp2e_self_1e-${e}.blastp
  crossBlastp=AtCeDmHsScSp2e_cross_1e-${e}.blastp
  bothBlastp=AtCeDmHsScSp2e_both_1e-${e}.blastp
  # Empty output files
  cat /dev/null > $selfBlastp
  cat /dev/null > $crossBlastp
  cat /dev/null > $bothBlastp
  for org1 in At Ce Dm Hs Sc Sp2e
  do
    for org2 in At Ce Dm Hs Sc Sp2e
    do
      if [[ $org1 == $org2 ]]
      then
        # Put self hits in one file...
        cat by_org/blastp/${org1}-v-${org2}_1e-${e}.blastp >> $selfBlastp
      else
        # ...and cross hits in another
        cat by_org/blastp/${org1}-v-${org2}_1e-${e}.blastp >> $crossBlastp
      fi
      cat by_org/blastp/${org1}-v-${org2}_1e-${e}.blastp >> $bothBlastp
    done
  done
done

# Create test files for half the sequences being halved
for e in 3 5
do
  # Specify output file names
  selfBlastp=AtCeDmHs2eSc2eSp2e_self_1e-${e}.blastp
  crossBlastp=AtCeDmHs2eSc2eSp2e_cross_1e-${e}.blastp
  bothBlastp=AtCeDmHs2eSc2eSp2e_both_1e-${e}.blastp
  # Empty output files
  cat /dev/null > $selfBlastp
  cat /dev/null > $crossBlastp
  cat /dev/null > $bothBlastp
  for org1 in At Ce Dm Hs2e Sc2e Sp2e
  do
    for org2 in At Ce Dm Hs2e Sc2e Sp2e
    do
      if [[ $org1 == $org2 ]]
      then
        # Put self hits in one file...
        cat by_org/blastp/${org1}-v-${org2}_1e-${e}.blastp >> $selfBlastp
      else
        # ...and cross hits in another
        cat by_org/blastp/${org1}-v-${org2}_1e-${e}.blastp >> $crossBlastp
      fi
      cat by_org/blastp/${org1}-v-${org2}_1e-${e}.blastp >> $bothBlastp
    done
  done
done

# Create test files for 1/3 of the sequences being in thirds, 1/3 of the sequences being halved, and 1/3 being full length
for e in 3 5
do
  # Specify output file names
  selfBlastp=AtCeDm2eHs2eSc3eSp3e_self_1e-${e}.blastp
  crossBlastp=AtCeDm2eHs2eSc3eSp3e_cross_1e-${e}.blastp
  bothBlastp=AtCeDm2eHs2eSc3eSp3e_both_1e-${e}.blastp
  # Empty output files
  cat /dev/null > $selfBlastp
  cat /dev/null > $crossBlastp
  cat /dev/null > $bothBlastp
  for org1 in At Ce Dm2e Hs2e Sc3e Sp3e
  do
    for org2 in At Ce Dm2e Hs2e Sc3e Sp3e
    do
      if [[ $org1 == $org2 ]]
      then
        # Put self hits in one file...
        cat by_org/blastp/${org1}-v-${org2}_1e-${e}.blastp >> $selfBlastp
      else
        # ...and cross hits in another
        cat by_org/blastp/${org1}-v-${org2}_1e-${e}.blastp >> $crossBlastp
      fi
      cat by_org/blastp/${org1}-v-${org2}_1e-${e}.blastp >> $bothBlastp
    done
  done
done

ORIGINALATTEMPT

