data: data2fasttext.out
	tr '\r' '\n' < ../data/data.txt | ./data2fasttext.py > data2fasttext.out

random: randomizeText.out.0
	./randomizeText.py < data2fasttext.out > randomizeText.out
	./splitFile.py -f randomizeText.out

run:
	./run.sh

tscores:
	./tscore.py __label__NIE __label__COL < randomizeText.out | less

tf-idf:
	jupyter notebook exploreData.ipynb

