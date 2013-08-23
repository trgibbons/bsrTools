#!/bin/bash

for i in {0..9}
do
  time nice mcl test.graph --abc -I 1.${i} -o test.I1${i}.mcl 2> test.I1${i}.err
done
