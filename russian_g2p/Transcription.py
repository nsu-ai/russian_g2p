from russian_g2p.Preprocessor import Preprocessor
from russian_g2p.Accentor import Accentor
from russian_g2p.Grapheme2Phoneme import Grapheme2Phoneme


class Transcription:
    def __init__(self, exception_for_unknown: bool=False):
        self.__preprocessor = Preprocessor()
        self.__accentor = Accentor(exception_for_unknown=exception_for_unknown)
        self.__g2p = Grapheme2Phoneme()

    def transcribe(self, text: str):
        words_and_tags = self.__preprocessor.preprocessing(text)
        accented_text = self.__accentor.do_accents(words_and_tags)
        tmp = ' '.join(accented_text[0])
        tmp = ' ' + tmp
        phonetic_words = tmp.split(' <sil>')
        result = []
        for phonetic_word in phonetic_words:
            if len(phonetic_word) != 0:
                phonemes = self.__g2p.phrase_to_phonemes(phonetic_word)
                result.append(phonemes)
        return result
