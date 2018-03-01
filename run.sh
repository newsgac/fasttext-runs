#!/bin/bash
# run.sh: run 10cv fasttext experiment
# usage: run.sh [-b] [-d dimension] [-e article-file] [ -m minCount ] [-v]
# options: -b: use binary labels: news articles vs rest
#          -d: dimension (size) of word vectors
#          -e: use extra data for building word vectors
#          -m: minimum count of word in data to enter lexicon
#          -v: exteral word vector file
# 20171124 erikt(at)xs4all.nl

COMMAND=$0
FILE=randomizeText.out.nodates
TMPFILE=run.$$.$RANDOM
TRAIN=$TMPFILE.train
TEST=$TMPFILE.test
MODEL=$TMPFILE.model
SCORES=$TMPFILE.scores
LABELS=$TMPFILE.labels
VECTORS=$TMPFILE.vectors
FASTTEXT=$HOME/software/fastText/fasttext
BINDIR=$HOME/projects/online-behaviour/machine-learning
DIM=300
MINCOUNT=5
USEBINARY=""
USEVECTORS=""
EXTRATEXT=""
while getopts be:d:m:v: FLAG; do
case $FLAG in
b) USEBINARY="TRUE"
   ;;
d) DIM=$OPTARG
   ;;
e) EXTRATEXT=$OPTARG
   ;;
m) MINCOUNT=$OPTARG
   ;;
v) USEVECTORS="-pretrainedVectors $OPTARG"
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
         sed 's/^__label__[^ ]*/__label__OTH/' |\
         sed 's/^FILLER/__label__NIE/'
   fi
}

if [ -n "$EXTRATEXT" ]
then
   # create word vectors from training file AND extra data
   if [ -n "$USEVECTORS" ]
   then
      echo "warning: ignoring vector file in $USEVECTORS" >&2
   fi
   USEVECTORS="-pretrainedVectors $VECTORS.vec"
   cat $FILE.? | cut -d' ' -f2- > $TRAIN
   cat $EXTRATEXT >> $TRAIN
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
   wc -l $LABELS
else
   cat $FILE.[0-9] | makeBinary |\
      paste -d' ' $LABELS - | cut -d' ' -f1,2 | sort | uniq -c
fi

rm -f $TMPFILE.*

exit 0
