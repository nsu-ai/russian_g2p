from re import sub

from rnnmorph.predictor import RNNMorphPredictor


class Preprocessor():

    def __init__(self):
        self.predictor = RNNMorphPredictor()

    def gettags(self, text):
        phonetic_phrases = ' '.join(text).split('<sil>')
        words_and_tags = [['<sil>', 'SIL _']]
        for phonetic_phrase in phonetic_phrases:
            phonetic_phrase = phonetic_phrase.strip()
            if phonetic_phrase != '':
                analysis = self.predictor.predict_sentence_tags(phonetic_phrase.split(' '))
                for word in analysis:
                    word_and_tag = []
                    word_and_tag.append(word.word)
                    word_and_tag.append(word.pos + ' ' + word.tag)
                    words_and_tags.append(word_and_tag)
                words_and_tags.append(['<sil>', 'SIL _'])
        return words_and_tags

    def preprocessing(self, text):
        text = sub('[\.\,\?\!\(\);:]+', ' <sil>', text.lower())
        text = sub(' [–-] |\n', ' <sil> ', text)
        text = sub('\s{2,}', ' ', text)
        text = sub('^\s|(?<!\w)[\\\/@#~¬`£€\$%\^\&\*–_=+\'\"\|«»–-]+', '', text)
        text = text.strip()
        words_and_tags = self.gettags(text.split(' '))
        return words_and_tags