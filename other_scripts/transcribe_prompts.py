from russian_g2p import Grapheme2Phoneme
import codecs
import csv
from os.path import isfile

prompts_file = open('corpus/corpus_FAS_short_only')
prompts_lines = prompts_file.readlines()
g2p = Grapheme2Phoneme()
with codecs.open('corpus/transcribed_voxforge_fragment.csv', mode='wb', encoding='utf-8') as f:
	wr = csv.writer(f)
	for prompts_line in prompts_lines:
		prompts_line_clean = prompts_line.strip().lower()
		id_name = prompts_line.split()[0].replace('/mfc/', '/wav/')
		prompts_words = ' '.join(prompts_line_clean.split()[1:])
		try:
			transcription = g2p.phrase_to_phonemes(prompts_words)
			if isfile('/media/dino/DATA/corpus/voxforge/repository/downloads/Russian/Trunk/Audio/Main/8kHz_16bit/' + id_name + '.wav'):
				with open('corpus/dict_voxforge_fragment', 'a') as f:
					for word in prompts_words.split():
						f.writelines('{}\t{}\n'.format(word.replace('+', ''), ' '.join(g2p.word_to_phonemes(word))))
				wr.writerow([id_name,
					prompts_words.replace('+', ''),
					' '.join([' '.join(word) for word in transcription])])
		except AssertionError:
			continue

