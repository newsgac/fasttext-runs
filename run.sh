#!/bin/bash
# run.sh: run 10cv fasttext experiment
# usage: run.sh
# 20171124 erikt(at)xs4all.nl

FILE=randomizeText.out
TMPFILE=run.$$.$RANDOM
TRAIN=$TMPFILE.train
TEST=$TMPFILE.test
MODEL=$TMPFILE.model
SCORES=$TMPFILE.scores
LABELS=$TMPFILE.labels
FASTTEXT=$HOME/software/fastText/fasttext
BINDIR=$HOME/projects/online-behaviour/machine-learning

for N in 0 1 2 3 4 5 6 7 8 9; do
   cp $FILE.$N $TEST
   for M in 0 1 2 3 4 5 6 7 8 9; do
      if [ $M != $N ]; then cat $FILE.$M; fi
   done  > $TRAIN
   $FASTTEXT supervised -input $TRAIN -output $MODEL -dim 300 -minCount 5 \
      > /dev/null 2> /dev/null
   $FASTTEXT predict $MODEL.bin $TEST >> $LABELS 
   $FASTTEXT predict $MODEL.bin $TEST | paste -d' ' - $TEST |\
      cut -d' ' -f1,2 | $BINDIR/eval.py | head -1 |\
      rev | sed 's/^ *//' | cut -d' ' -f1 | rev
done | tee $SCORES

cat $SCORES | (tr '\n' +;echo 0) | bc | sed 's/\([0-9]\)\./\.\1/' |\
   sed 's/^/average: /'
sort $LABELS | uniq -c

rm -f $TMPFILE.*

exit 0
