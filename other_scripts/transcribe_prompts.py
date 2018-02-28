from russian_g2p import Grapheme2Phoneme
import codecs
import csv
from os.path import isfile

prompts_file = open('corpus/fixed_corpus_with_punct+acc+sil')
prompts_lines = prompts_file.readlines()
g2p = Grapheme2Phoneme()
with codecs.open('corpus/transcribed_voxforge_fragment_PUNCT.csv', mode='wb', encoding='utf-8') as f:
	wr = csv.writer(f)
	for prompts_line in prompts_lines:
		prompts_line_clean = prompts_line.strip().lower()
		id_name = prompts_line.split()[0].replace('/mfc/', '/wav/')
		prompts_words = ' '.join(prompts_line_clean.split()[1:])
		try:
			transcription = g2p.phrase_to_phonemes(prompts_words)
			with open('corpus/dict_voxforge_fragment_PUNCT', 'a') as f:
				for word in prompts_words.split():
					if word != 'sil':
						f.writelines('{}\t{}\n'.format(word.replace('+', ''), ' '.join(g2p.word_to_phonemes(word))))
			wr.writerow([id_name,
				prompts_words.replace('+', ''),
				' '.join(transcription)])
		except AssertionError:
			continue

