from re import sub

from rnnmorph.predictor import RNNMorphPredictor


class Preprocessor():
    def __init__(self):
        self.predictor = RNNMorphPredictor()

    def __del__(self):
        if hasattr(self, 'predictor'):
            del self.predictor

    def gettags(self, text):
        if not isinstance(text, list):
            raise ValueError('Expected `{0}`, but got `{1}`.'.format(type([1, 2]), type(text)))
        if len(text) == 0:
            return []
        analysis = self.predictor.predict_sentence_tags(text)
        words_and_tags = []
        for word in analysis:
            word_and_tag = []
            word_and_tag.append(word.word)
            word_and_tag.append(word.pos + ' ' + word.tag)
            words_and_tags.append(word_and_tag)
        return words_and_tags

    def preprocessing(self, text):
        text = sub(r'[.,?!();:]+', ' <sil>', text)
        text = sub(r' [–-] |\n', ' <sil> ', text)
        text = sub(r'\s{2,}', ' ', text)
        text = sub(r'^\s|[\\/@#~¬`£€$%^&*–_=+\'\"|«»-]+', '', text)
        words_and_tags = self.gettags(text.split())
        return words_and_tags

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
