# russian_g2p
Accentor & Transcriptor for Russian Language

## Getting Started

### Prerequisites

You should have python3 installed on your machine (we recommend Anaconda3 package) and modules listed in requirements.txt. If you do not have them, run in Terminal

```
pip3 install -r requirements.txt
```

### Installing and Usage

#### Linux / MacOS
To install this project on your local machine, you should run the following commands in Terminal:

```
git init
git clone https://github.com/nsu-ai/russian_g2p.git\
cd russian_g2p
```

Examples of using Accentor:

```
>>> from russian_g2p.Accentor import Accentor
>>> your_accentor = Accentor()
>>> your_accentor.do_accents([['конференция'], ['диалог']])
[['конфере+нция', 'диало+г']]
>>> your_accentor.do_accents([['ноги', 'NOUN Case=Gen|Gender=Fem|Number=Sing'], ['ноги', 'NOUN Case=Acc|Gender=Fem|Number=Plur']])
[['ноги+', 'но+ги']]

```

Examples of using Transcriptor:

```
>>> from russian_g2p.Grapheme2Phoneme import Grapheme2Phoneme
>>> your_transcriptor = Grapheme2Phoneme()
>>> your_transcriptor.word_to_phonemes('диало+г')
['D0', 'I', 'A', 'L', 'O0', 'K']
>>> your_transcriptor.phrase_to_phonemes('диало+г бы+л')
['D0', 'I', 'A', 'L', 'O0', 'G', 'B', 'Y0', 'L']
```

Examples of using the whole system:

```
>>> from russian_g2p.Transcription import Transcription
>>> your_transcriptor = Transcription()
>>> for it in your_transcriptor.transcribe(['диало+г', 'диало+г бы+л', 'Я иду, а ты - нет.']): print(it)
[['D0', 'I', 'A', 'L', 'O0', 'K']]
[['D0', 'I', 'A', 'L', 'O0', 'G', 'B', 'Y0', 'L']]
[['J0', 'A0', 'I', 'D', 'U0'], ['A', 'T', 'Y0'], ['N0', 'E0', 'T']]
```


## Running the tests

To run the automated tests for this system (may take some time), use a command

```
python3 test.py
```

## Using for a phonetic dictionary generating

Phonetic dictionary is necessary for speech recognition system based on the CMU Sphinx (see https://cmusphinx.github.io/wiki/tutorialam/#data-preparation). You can use our Python script `create_phonetic_dict.py` to generate new phonetic dictionary. For example:

```
python create_phonetic_dict.py --src source_vocabulary.txt --dst 'created_phonetic_dictionary.dic' --bad 'unknown_words.txt'
```

The `source_vocabulary.txt` is a simple text file, and it has to contain all words, for which we want to generate phonetic transcriptions (each word in a single line).

All generated pairs "a word" - "its transcription" will be generated and saved into the file `created_phonetic_dictionary.dic`:

- each pair will be placed in a single line;

- word in this pair will be separated from transcription by the space character;

- phonemes in transcription also will be separated apart each other by the space characters.

Finally, "bad words", which are unknown for our system, will be written into the `unknown_words.txt`. You will have the opportunity to transcribe these words manually.


## Generating phonetic transcriptions not only for words but also for phrases

Also you can automatically create phonetical transcriptions for whole phrases. In this case the coarctication and other phenomenons at the words junction can be taken into account.

For this, you have to use the `demo.py` script in the following way, for example:

```
python demo.py --src source_phrases.txt --dst transcribed_phrases.txt --order pronunciation-text
```

The `source_phrases.txt` is a simple text file contained source phrases (of course, in Russian). Our system will be transcribe these phrases and save all pairs "a phrase" - "a phonetic transcritpion" into the `transcribed_phrases.txt` file. Order in such pairs can be various: the source phrase from the beginning, and then the transcription, if you specify `--order text-pronunciation`, or the transcription from the beginning, and then the corresponding phrase, if you specify `--order pronunciation-text`.

Number of lines in the `transcribed_phrases.txt` can be less then number of lines in the `source_phrases.txt`, because some phrases cannot be transcribed by our system (usually, over the incompleteness of thesaurus using for accentuation).

## Citation

If you use russian_g2p in your projects, please feel free to cite the work as follows:

```
@inproceedings{yakovenko2018algorithms,
  title={Algorithms for automatic accentuation and transcription of russian texts in speech recognition systems},
  author={Yakovenko, Olga and Bondarenko, Ivan and Borovikova, Mariya and Vodolazsky, Daniil},
  booktitle={International Conference on Speech and Computer},
  pages={768--777},
  year={2018},
  organization={Springer}
}
```

## Authors

* **Ivan Bondarenko** - *The initial version of Accentor & Transcriptor* - [bond005](https://github.com/bond005)

* **Olga Yakovenko** - *Analyzing the results of work of Accentor on corpus Voxforge.org/ru* - [DinoTheDinosaur](https://github.com/DinoTheDinosaur)

* **Maria Borovikova** - *Reworking Transcriptor taking into account the modern rules of phonetics* - [project178](https://github.com/project178)

* **Daniil Vodolazsky** - *Systematization of rules for Transcriptor and refactoring of code* - [s231644](https://github.com/s231644)

See also the list of [contributors](https://github.com/nsu-ai/russian_g2p/contributors) who participated in this project.

## Contributing

* **Konstantin Dorichev** [kdorichev](https://github.com/kdorichev)

## License

MIT

## Acknowledgments

---
