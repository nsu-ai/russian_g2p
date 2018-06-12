from re import sub

from rnnmorph.predictor import RNNMorphPredictor


class Preprocessor():

    def __init__(self):
        self.predictor = RNNMorphPredictor()

    def __del__(self):
        if hasattr(self, 'predictor'):
            del self.predictor

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.predictor = self.predictor
        return result

    def __deepcopy__(self, memodict={}):
        cls = self.__class__
        result = cls.__new__(cls)
        result.predictor = self.predictor
        return result

    def gettags(self, text):
        if not isinstance(text, list):
            raise ValueError('Expected `{0}`, but got `{1}`.'.format(type([1, 2]), type(text)))
        if len(text) == 0:
            return []
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