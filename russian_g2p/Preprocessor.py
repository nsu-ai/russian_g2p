from re import sub

import treetaggerwrapper


class Preprocessor():

    def __init__(self):
        self.__tagger = treetaggerwrapper.TreeTagger(TAGLANG='ru')

    def gettags(self, text):
        words_and_tags = treetaggerwrapper.make_tags(self.__tagger.tag_text(text))
        words = []
        tags = []
        for word_and_tag in words_and_tags:
            try:
                tags.append(word_and_tag.pos)
                words.append(word_and_tag.word)
            except AttributeError:
                words.append(word_and_tag.what)
                tags.append('uknown')
        return words, tags

    def preprocessing(self, text):
        text = sub('[\.\,\?\!\(\);:]+', '<sil>', text)
        text = sub(' [–-] ', '<sil>', text)
        text = sub('[\\\/@#\$%\^\&\*–_=+\'\"\|«»–-]+', '', text)
        words, tags = self.gettags(text)
        return words, tags