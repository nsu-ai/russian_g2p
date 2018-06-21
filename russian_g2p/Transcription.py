from russian_g2p.Preprocessor import Preprocessor
from russian_g2p.Accentor import Accentor
from russian_g2p.Grapheme2Phoneme import Grapheme2Phoneme


class Transcription:
    def __init__(self, exception_for_unknown: bool=False, batch_size: int=64):
        self.__preprocessor = Preprocessor(batch_size=batch_size)
        self.__accentor = Accentor(exception_for_unknown=exception_for_unknown)
        self.__g2p = Grapheme2Phoneme()

    def transcribe(self, texts: list):
        all_words_and_tags = self.__preprocessor.preprocessing(texts)
        total_result = []
        for cur_words_and_tags in all_words_and_tags:
            accented_text = self.__accentor.do_accents(cur_words_and_tags)
            tmp = ' '.join(accented_text[0])
            tmp = ' ' + tmp
            phonetic_words = tmp.split(' <sil>')
            result = []
            for phonetic_word in phonetic_words:
                if len(phonetic_word) != 0:
                    phonemes = self.__g2p.phrase_to_phonemes(phonetic_word)
                    result.append(phonemes)
            total_result.append(result)
        return total_result
