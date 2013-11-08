Synthetic test data set for Porthos
===================================

The synthetic blast results in this directory are for imaginary genes A & B, 
which were present at the base of imaginary organism tree ((1,2),3)

Alignments between two identical random sequences should generate a bit score 
of two per aligned base, on average.  I therefore specify all sequences to be 
100bp, that a full-length alignment exists between all copies of a gene, and 
that the bit score is two times the percent identity.  I do not bother making 
up values for the other fields because Porthos only uses the bit scores.

For each internal node separating two organisms, I subtract 10% from the 
percent identity of alignments between copies of seqA, 20% from the percent 
identity of alignments between copies of seqB.

Duplicated sequences, indicated by a number after the letter (eg. seqA1), are 
included so that they can be broken.  Each piece is indicated with a lowercase 
letter (eg. seqA1a, seqA1b).

If I start adding alignments between sequences of different families, I will 
likely use a 5% (plus a flat 50% penalty) from the percent identity of 
alignments crossed between copies of seqA & seqB, but I haven't gotten to it.