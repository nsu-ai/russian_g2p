from re import sub

from rnnmorph.predictor import RNNMorphPredictor


class Preprocessor():

    def __init__(self):
        self.predictor = RNNMorphPredictor()

    def gettags(self, text):
        analysis = self.predictor.predict_sentence_tags(text)
        words_and_tags = []
        for word in analysis:
            word_and_tag = []
            word_and_tag.append(word.word)
            word_and_tag.append(word.pos + ' ' + word.tag)
            words_and_tags.append(word_and_tag)
        return words_and_tags

    def preprocessing(self, text):
        text = sub('[\.\,\?\!\(\);:]+', ' <sil>', text)
        text = sub(' [–-] |\n', ' <sil> ', text)
        text = sub('\s{2,}', ' ', text)
        text = sub('^\s|[\\\/@#~¬`£€\$%\^\&\*–_=+\'\"\|«»–-]+', '', text)
        words_and_tags = self.gettags(text.split(' '))
        return words_and_tags