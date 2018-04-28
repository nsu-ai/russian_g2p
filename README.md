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
cd YOUR_FOLDER
git init
git clone https://github.com/nsu-ai/russian_g2p.git
```

The project is now in YOUR_FOLDER.

To use this project, run
```
cd russian_g2p
python3 __init__.py
python3
>>> from russian_g2p import *
```

Examples of using Accentor:

```
>>> your_accentor = Accentor()
>>> your_accentor.do_accents([['конференция'], ['диалог']])
[['конфере+нция', 'диало+г']]
>>> your_accentor.do_accents([['ноги', 'NOUN Case=Gen|Gender=Fem|Number=Sing'], ['ноги', 'NOUN Case=Acc|Gender=Fem|Number=Plur']])
[['ноги+', 'но+ги']]

```

Examples of using Transcriptor:

```
>>> your_transcriptor = Grapheme2Phoneme()
>>> your_transcriptor.word_to_phonemes('диало+г')
['D0', 'I', 'A', 'L', 'O0', 'K']
>>> your_transcriptor.phrase_to_phonemes('диало+г бы+л')
['D0', 'I', 'A', 'L', 'O0', 'G', 'B', 'Y0', 'L']
```

Examples of using the whole system:

```
>>> your_transcriptor = Transcription()
>>> Transcription().transcribe('диало+г')
['D0', 'I', 'A', 'L', 'O0', 'K']
>>> Transcription().transcribe('диало+г бы+л')
['D0', 'I', 'A', 'L', 'O0', 'G', 'B', 'Y0', 'L']
>>> Transcription().transcribe('Я иду, а ты - нет.')
[['J0', 'A0', 'I', 'D', 'U0'], ['A', 'T', 'Y0'], ['N0', 'E0', 'T']]
```


## Running the tests

To run the automated tests for this system (may take some time), use a command

```
python3 test.py
```

## Contributing

...

## Authors

* **Ivan Bondarenko** - *The initial version of Accentor & Transcriptor* - [bond005](https://github.com/bond005)

* **Olga Yakovenko** - *Analyzing the results of work of Accentor on corpus Voxforge.org/ru* - [DinoTheDinosaur](https://github.com/DinoTheDinosaur)

* **Maria Borovikova** - *Reworking Transcriptor taking into account the modern rules of phonetics* - [project178](https://github.com/project178)

* **Daniil Vodolazsky** - *Systematization of rules for Transcriptor and refactoring of code* - [s231644](https://github.com/s231644)

See also the list of [contributors](https://github.com/nsu-ai/russian_g2p/contributors) who participated in this project.

## License

---

## Acknowledgments

---
