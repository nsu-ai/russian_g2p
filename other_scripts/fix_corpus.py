import codecs
import json
import re
from copy import deepcopy

corpus = open('fixed_corpus_inamb').read()
'''
corpus_true = deepcopy(corpus)

with codecs.open('data/Accents.json', mode='r', encoding='utf-8', errors='ignore') as fp:
	accents = json.load(fp)

for accent in accents[1]:
	if (accent.find('ё') != -1) and (accent.replace('ё', 'е') not in accents[1]) and (accent.replace('+', '').replace('ё', 'е') not in accents[0].keys()):
		raw_word = accent.replace('+', '').replace('ё', 'е')
		if corpus.find(' {} '.format(raw_word)) != -1:
			corpus = corpus.replace(' {} '.format(raw_word), ' {} '.format(accent))
			print(accent)
'''
with open('bad_words') as f:
	lines = f.readlines()
	pairs = []
	for line in lines:
		pairs.append((line.split('\t')[0], line.split('\t')[1].strip()))
fix_dic = dict(pairs)

for i, pair in enumerate(fix_dic):
	if corpus.find(pair) != -1:
		print(i)
		word = re.compile(r'(?<!\w){}(?!\w)'.format(pair))
		corpus = re.sub(word, '{}'.format(fix_dic[pair]), corpus)

with open('fixed_corpus_inamb_full', 'w') as f:
	f.write(corpus)