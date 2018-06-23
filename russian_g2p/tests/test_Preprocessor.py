import unittest

from russian_g2p.Preprocessor import Preprocessor


class TestPrep(unittest.TestCase):
    def setUp(self):
        self.__prep = Preprocessor()

    def tearDown(self):
        del self.__prep

    def test_tags(self):
        source_phrase = ' - Нет, - сказал он (звали его Андреем Николаевичем).'
        target_variants = [['<sil>', 'SIL _'], ['нет', 'PART _'], ['<sil>', 'SIL _'],
                           ['сказал', 'VERB Gender=Masc|Mood=Ind|Number=Sing|Tense=Past|VerbForm=Fin|Voice=Act'],
                           ['он', 'PRON Case=Nom|Gender=Masc|Number=Sing|Person=3'],
                           ['<sil>', 'SIL _'], ['звали', 'VERB Mood=Ind|Number=Plur|Tense=Past|VerbForm=Fin|Voice=Act'],
                           ['его', 'PRON Case=Acc|Gender=Masc|Number=Sing|Person=3'],
                           ['андреем', 'NOUN Case=Ins|Gender=Masc|Number=Sing'],
                           ['николаевичем', 'NOUN Case=Ins|Gender=Masc|Number=Sing'],
                           ['<sil>', 'SIL _']]
        real_variants = self.__prep.preprocessing([source_phrase])[0]
        self.assertEqual(target_variants, real_variants)

    def test_hyphen(self):
        source_phrase = 'Кто-нибудь выучил фразео-, нео- и прочие измы? Я - нет.'
        target_variants = [['<sil>', 'SIL _'], ['кто-нибудь', 'PRON Case=Nom|Gender=Masc|Number=Sing'],
                           ['выучил', 'VERB Gender=Masc|Mood=Ind|Number=Sing|Tense=Past|VerbForm=Fin|Voice=Act'],
                           ['фразео-', 'ADV Degree=Cmp'], ['<sil>', 'SIL _'], ['нео-', 'ADV Degree=Pos'],
                           ['и', 'CONJ _'], ['прочие', 'DET Case=Acc|Number=Plur'],
                           ['измы', 'NOUN Case=Acc|Gender=Masc|Number=Plur'], ['<sil>', 'SIL _'],
                           ['я', 'PRON Case=Nom|Number=Sing|Person=1'], ['<sil>', 'SIL _'],
                           ['нет', 'VERB Mood=Ind|Number=Sing|Person=3|Tense=Notpast|VerbForm=Fin'],
                           ['<sil>', 'SIL _']]

        real_variants = self.__prep.preprocessing([source_phrase])[0]
        self.assertEqual(target_variants, real_variants)

    def test_nothing(self):
        source_phrase = '...'
        target_variants = [['<sil>', 'SIL _']]
        real_variants = self.__prep.preprocessing([source_phrase])[0]
        self.assertEqual(target_variants, real_variants)


if __name__ == '__main__':
    unittest.main(verbosity=2)
