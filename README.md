# russian_g2p
Accentor & Transcriptor for Russian Language

## Getting Started

### Prerequisites

You should have python3 installed on your machine (we recommend Anaconda3 package) and modules listed in requirements.txt. If you do not have them, run in Terminal

```
pip3 install -r requirements.txt
```

### Installing and Usage

#### Linux
To install this project on your local machine, you should run the following commands in Terminal:

```
cd YOUR_FOLDER
git init
git clone https://github.com/nsu-ai/russian_g2p.git
```

The project now is in YOUR_FOLDER.

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
>>> your_accentor.do_accents(['конференция', 'диалог'])  # you will see the accented words in the output
>>> your_accentor.do_accents(['новосибирский', 'государственный', 'университет'])

```

Examples of using Transcriptor:

```
>>> your_transcriptor = Grapheme2Phoneme()
>>> your_transcriptor.word_to_phonemes('конфере+нция')  # you will see the transcription in the output
>>> your_transcriptor.word_to_phonemes('диало+г')
```

```
>>> your_transcriptor = Grapheme2Phoneme()
>>> your_transcriptor.phrase_to_phonemes('конфере+нция диало+г')
>>> your_transcriptor.phrase_to_phonemes('новосиби+рский госуда+рственный университе+т')
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

See also the list of [contributors](https://github.com/russian_g2p/contributors) who participated in this project.

## License

---

## Acknowledgments

---
