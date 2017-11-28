#!/bin/bash
# run.sh: run 10cv fasttext experiment
# usage: run.sh [-b] [-v]
# 20171124 erikt(at)xs4all.nl

COMMAND=$0
FILE=randomizeText.out
TMPFILE=run.$$.$RANDOM
TRAIN=$TMPFILE.train
TEST=$TMPFILE.test
MODEL=$TMPFILE.model
SCORES=$TMPFILE.scores
LABELS=$TMPFILE.labels
VECTORS=$TMPFILE.vectors
FASTTEXT=$HOME/software/fastText/fasttext
BINDIR=$HOME/projects/online-behaviour/machine-learning
EXTRADATA=getMoreData.out.txt
DIM=1
MINCOUNT=5
USEBINARY=""
USEVECTORS=""
while getopts bv FLAG; do
case $FLAG in
b) USEBINARY="TRUE"
   ;;
v) USEVECTORS="-pretrainedVectors $VECTORS.vec"
   ;;
\?) exit 1
   ;;
esac
done

function makeBinary {
   if [ -z "$USEBINARY" ]
   then
      cat
   else
      sed 's/^__label__NIE/FILLER/' |\
         sed 's/^__label__.../__label__OTH/' |\
         sed 's/^FILLER/__label__NIE/'
   fi
}

# tests:
# add label to text: sed 's/__\(...\) /__\1 \1 /'
# remove majority label: grep -v __label__NIE 
# use binary labels: makeBinary

if [ -n "$USEVECTORS" ]
then
   cat $FILE.? | cut -d' ' -f2- > $TRAIN
   cat $EXTRADATA >> $TRAIN
   $FASTTEXT skipgram -input $TRAIN -output $VECTORS \
      -dim $DIM -minCount $MINCOUNT > /dev/null 2>/dev/null
fi

for N in 0 1 2 3 4 5 6 7 8 9; do
   cat $FILE.$N | makeBinary > $TEST
   for M in 0 1 2 3 4 5 6 7 8 9; do
      if [ $M != $N ]; then cat $FILE.$M; fi
   done | makeBinary > $TRAIN
   $FASTTEXT supervised -input $TRAIN -output $MODEL \
      -dim $DIM -minCount $MINCOUNT $USEVECTORS > /dev/null 2> /dev/null
   $FASTTEXT predict $MODEL.bin $TEST >> $LABELS 
   $FASTTEXT predict $MODEL.bin $TEST | paste -d' ' - $TEST |\
      cut -d' ' -f1,2 | $BINDIR/eval.py | head -1 |\
      rev | sed 's/^ *//' | cut -d' ' -f1 | rev
done | tee $SCORES

cat $SCORES | (tr '\n' +;echo 0) | bc | sed 's/\([0-9]\)\./\.\1/' |\
   sed 's/^/average: /'
if [ -z "$USEBINARY" ]
then
   sort $LABELS | uniq -c
else
   cat $FILE.[0-9] | makeBinary |\
      paste -d' ' $LABELS - | cut -d' ' -f1,2 | sort | uniq -c
fi

rm -f $TMPFILE.*

exit 0
