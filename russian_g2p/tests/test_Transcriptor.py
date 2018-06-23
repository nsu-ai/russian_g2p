import unittest

from russian_g2p.Transcription import Transcription


class TestAll(unittest.TestCase):
    def setUp(self):
        self.__transcription = Transcription()

    def tearDown(self):
        del self.__transcription

    def test_normal(self):
        source_phrase = 'Мама мыла раму'
        target_variants = [['M', 'A0', 'M', 'A', 'M', 'Y0', 'L', 'A', 'R', 'A0', 'M', 'U']]
        real_variants = self.__transcription.transcribe([source_phrase])[0]
        self.assertEqual(target_variants, real_variants)

    def test_symbols(self):
        source_phrase = 'Мама мыла ра-му, а ты?! - Нет.'
        target_variants = [['M', 'A0', 'M', 'A', 'M', 'Y0', 'L', 'A', 'R', 'A0', 'M', 'U0'], ['A', 'T', 'Y0'],
                           ['N0', 'E0', 'T']]
        real_variants = self.__transcription.transcribe([source_phrase])[0]
        self.assertEqual(target_variants, real_variants)

    def test_nothing(self):
        source_phrase = '...'
        target_variants = []
        real_variants = self.__transcription.transcribe([source_phrase])[0]
        self.assertEqual(target_variants, real_variants)

    def test_begin(self):
        source_phrase = '- Ага'
        target_variants = [['A', 'G', 'A0']]
        real_variants = self.__transcription.transcribe([source_phrase])[0]
        self.assertEqual(target_variants, real_variants)

    def test_accented(self):
        source_phrase_1 = 'диалог был'
        real_variants_1 = self.__transcription.transcribe([source_phrase_1])[0]
        source_phrase_2 = 'диало+г бы+л'
        real_variants_2 = self.__transcription.transcribe([source_phrase_2])[0]
        self.assertEqual(real_variants_1, real_variants_2)

if __name__ == '__main__':
    unittest.main(verbosity=2)
