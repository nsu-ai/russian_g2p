from re import sub

from rnnmorph.predictor import RNNMorphPredictor


class Preprocessor():

    def __init__(self, batch_size=1):
        self.batch_size = batch_size
        self.predictor = RNNMorphPredictor(language="ru")

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

    def gettags(self, texts):
        if not isinstance(texts, list):
            raise ValueError(f'Expected `{type([1, 2])}`, but got `{type(texts)}`.')
        if len(texts) == 0:
            return []
        all_phonetic_phrases = []
        all_phrases_for_rnnmorph = []
        for cur_text in texts:
            list_of_phonetic_phrases = [cur.strip() for cur in ' '.join(cur_text).split('<sil>')]
            united_phrase_for_rnnmorph = []
            for phonetic_phrase in list_of_phonetic_phrases:
                if len(phonetic_phrase) > 0:
                    united_phrase_for_rnnmorph += phonetic_phrase.split()
            if len(united_phrase_for_rnnmorph) > 0:
                all_phrases_for_rnnmorph.append(united_phrase_for_rnnmorph)
                all_phonetic_phrases.append(list_of_phonetic_phrases)
            else:
                all_phonetic_phrases.append([])
        if len(all_phrases_for_rnnmorph) > 0:
            all_forms = self.predictor.predict_sentences(all_phrases_for_rnnmorph, batch_size=self.batch_size)
        else:
            all_forms = []
        all_words_and_tags = []
        phrase_ind = 0
        for cur in all_phonetic_phrases:
            words_and_tags = [['<sil>', 'SIL _']]
            if len(cur) > 0:
                token_ind = 0
                for phonetic_phrase in cur:
                    if len(phonetic_phrase) > 0:
                        n = len(phonetic_phrase.split(' '))
                        analysis = all_forms[phrase_ind][token_ind:(token_ind + n)]
                        for word in analysis:
                            word_and_tag = []
                            word_and_tag.append(word.word)
                            word_and_tag.append(word.pos + ' ' + word.tag)
                            words_and_tags.append(word_and_tag)
                        words_and_tags.append(['<sil>', 'SIL _'])
                        token_ind += n
                phrase_ind += 1
            all_words_and_tags.append(words_and_tags)
        return all_words_and_tags

    def preprocessing(self, texts):

        def prepare(src):
            dst = sub('[\.\,\?\!\(\);:]+', ' <sil>', src.lower())
            dst = sub(' [–-] |\n', ' <sil> ', dst)
            dst = sub('\s{2,}', ' ', dst)
            dst = sub('^\s|(?<!\w)[\\\/@#~¬`£€\$%\^\&\*–_=+\'\"\|«»–-]+', '', dst)
            return dst.strip().split(' ')

        words_and_tags = self.gettags([prepare(cur) for cur in texts])
        return words_and_tags