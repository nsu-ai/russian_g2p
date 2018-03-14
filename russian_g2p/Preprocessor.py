from re import sub

import treetaggerwrapper


class Preprocessor():

    def __init__(self):
        self.__tagger = treetaggerwrapper.TreeTagger(TAGLANG='ru')

    def gettags(self, text):
        analysis = treetaggerwrapper.make_tags(self.__tagger.tag_text(text))
        words_and_tags= []
        for word in analysis:
            word_and_tag = []
            try:
                word_and_tag.append(word.word)
                word_and_tag.append(word.pos)
            except AttributeError:
                word_and_tag.append(word.what)
                word_and_tag.append('uknown')
            words_and_tags.append(word_and_tag)
        return words_and_tags

    def preprocessing(self, text):
        text = sub('[\.\,\?\!\(\);:]+', '<sil>', text)
        text = sub(' [–-] ', '<sil>', text)
        text = sub('[\\\/@#\$%\^\&\*–_=+\'\"\|«»–-]+', '', text)
        words_and_tags = self.gettags(text)
        return words_and_tags