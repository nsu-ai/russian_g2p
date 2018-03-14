from russian_g2p.Preprocessor import Preprocessor
from russian_g2p.Accentor import Accentor
from russian_g2p.Grapheme2Phoneme import Grapheme2Phoneme

class Transcription:
    def transcribe(self, text: str):
        words_and_tags = Preprocessor().preprocessing(text)
        accented_text = Accentor().do_accents(words_and_tags)
        tmp = ' '.join(accented_text[0])
        tmp = ' ' + tmp
        phonetic_words = tmp.split(' <sil>')
        result = []
        for phonetic_word in phonetic_words:
            if len(phonetic_word) != 0:
                phonemes = Grapheme2Phoneme().phrase_to_phonemes(phonetic_word)
                result.append(phonemes)
        return result