import re
import unittest

from russian_g2p.Accentor import Accentor


class TestRussianAccentor1(unittest.TestCase):
    def setUp(self):
        self.__accentor = Accentor()

    def tearDown(self):
        del self.__accentor

    def test_do_accents_positive01(self):
        source_phrase = [['мама'], ['мыла'], ['раму']]
        target_variants = [
            ['ма+ма', 'мы+ла', 'ра+му']
        ]
        real_variants = self.__accentor.do_accents(source_phrase)
        self.assertEqual(target_variants, real_variants)

    def test_do_accents_positive02(self):
        source_phrase_n_morphotags = [['привет', 'NOUN Animacy=Inan|Case=Nom|Gender=Masc|Number=Sing'],
            ['кума', 'NOUN Animacy=Anim|Case=Nom|Gender=Fem|Number=Sing']]
        target_variants = [
            ['приве+т', 'кума+']
        ]
        real_variants = self.__accentor.do_accents(source_phrase_n_morphotags)
        self.assertEqual(target_variants, real_variants)

    def test_do_accents_positive03(self):
        source_phrase_n_morphotags = [['подарок', 'NOUN Animacy=Inan|Case=Nom|Gender=Masc|Number=Sing'],
            ['для', 'ADP _'],
            ['кума', 'NOUN Animacy=Anim|Case=Gen|Gender=Masc|Number=Sing']]
        target_variants = [
            ['пода+рок', 'для', 'ку+ма']
        ]
        real_variants = self.__accentor.do_accents(source_phrase_n_morphotags)
        self.assertEqual(target_variants, real_variants)

    def test_do_accents_positive04(self):
        source_phrase = [['оружие'], ['для'], ['кубы']]
        target_variants = [
            ['ору+жие', 'для', 'кубы']
        ]
        real_variants = self.__accentor.do_accents(source_phrase)
        self.assertEqual(target_variants, real_variants)

    def test_do_accents_positive05(self):
        source_phrase = [['машинисты'], ['любят'], ['кофе']]
        target_variants = [
            ['машини+сты', 'лю+бят', 'ко+фе']
        ]
        real_variants = self.__accentor.do_accents(source_phrase)
        self.assertEqual(target_variants, real_variants)

    def test_do_accents_positive06(self):
        source_phrase = [['во-первых'], ['кто-то'], ['вот-вот']]
        target_variants = [
            ['во-пе+рвых', 'кто+-то', 'вот-во+т']
        ]
        real_variants = self.__accentor.do_accents(source_phrase)
        self.assertEqual(target_variants, real_variants)

    def test_do_accents_positive07(self):
        source_phrase = [['хракозябр'], ['впулил'], ['куздру']]
        target_variants = [
            ['хракозябр', 'впулил', 'куздру']
        ]
        real_variants = self.__accentor.do_accents(source_phrase)
        self.assertEqual(target_variants, real_variants)

    def test_do_accents_positive08(self):
        accentor = Accentor(exception_for_unknown=True)
        source_phrase = [['хракозябр'], ['впулил'], ['куздру']]
        with self.assertRaises(ValueError):
            _ = accentor.do_accents(source_phrase)

    def test_do_accents_positive09(self):
        source_phrase = [['серебристо-белый'], ['цвет']]
        target_variants = [
            ['серебри+сто-бе+лый', 'цве+т']
        ]
        real_variants = self.__accentor.do_accents(source_phrase)
        self.assertEqual(target_variants, real_variants)

    def test_do_accents_positive10(self):
        source_phrase = [['озеро'], ['так'],['серебристо'], ['в'], ['свете'], ['солнца']]
        target_variants = [
            ['о+зеро', 'та+к', 'серебри+сто', 'в', 'све+те', 'со+лнца']
        ]
        real_variants = self.__accentor.do_accents(source_phrase)
        self.assertEqual(target_variants, real_variants)

    def test_do_accents_positive11(self):
        accentor = Accentor(exception_for_unknown=True)
        source_phrase = [['зеленого'], ['камня']]
        target_variants = [
            ['зелё+ного', 'ка+мня']
        ]
        real_variants = accentor.do_accents(source_phrase)
        self.assertEqual(target_variants, real_variants)

    def test_do_accents_negative01(self):
        source_phrase_n_morphotags = [['подарок', 'NOUN Animacy=Inan|Case=Nom|Gender=Masc|Number=Sing'],
            ['для', 'NOUN Animacy=Inan|Case=Nom|Gender=Masc|Number=Sing'],
            ['кума']]
        target_err_msg = re.escape('`подарок для кума`: morphotags do not correspond to words!')
        with self.assertRaisesRegex(AssertionError, target_err_msg):
            self.__accentor.do_accents(source_phrase_n_morphotags)

    def test_do_accents_negative02(self):
        source_phrase = [['подарок'], [''], ['кума']]
        target_err_msg = re.escape('`(\'подарок\', \'\', \'кума\')`: this phrase is wrong!')
        with self.assertRaisesRegex(AssertionError, target_err_msg):
            self.__accentor.do_accents(source_phrase)

    def test_do_accents_negative03(self):
        source_phrase = []
        target_err_msg = re.escape('Source phrase is empty!')
        with self.assertRaisesRegex(AssertionError, target_err_msg):
            self.__accentor.do_accents(source_phrase)

    def test_do_accents_negative04(self):
        source_phrase = [['а-зе']]
        target_err_msg = re.escape('Word `а-зе` is unknown!')
        accentor = Accentor(exception_for_unknown=True, use_wiki=False)
        with self.assertRaisesRegex(ValueError, target_err_msg):
            accentor.do_accents(source_phrase)

    def test_check_source_wordform_positive01(self):
        self.assertTrue(self.__accentor.check_source_wordform('абвг'))
        self.assertTrue(self.__accentor.check_source_wordform('аб-вг'))
        self.assertFalse(self.__accentor.check_source_wordform('-'))
        self.assertFalse(self.__accentor.check_source_wordform(''))
        self.assertFalse(self.__accentor.check_source_wordform('-абвг'))
        self.assertFalse(self.__accentor.check_source_wordform('аб--вг'))
        self.assertFalse(self.__accentor.check_source_wordform('abcабвг'))
        self.assertFalse(self.__accentor.check_source_wordform('abc'))
        self.assertFalse(self.__accentor.check_source_wordform('abcабвг123'))

    def test_check_accented_wordform_positive01(self):
        self.assertTrue(self.__accentor.check_accented_wordform('абвг'))
        self.assertTrue(self.__accentor.check_accented_wordform('аб-вг'))
        self.assertFalse(self.__accentor.check_accented_wordform('-'))
        self.assertFalse(self.__accentor.check_accented_wordform(''))
        self.assertFalse(self.__accentor.check_accented_wordform('-абвг'))
        self.assertFalse(self.__accentor.check_accented_wordform('аб--вг'))
        self.assertFalse(self.__accentor.check_accented_wordform('abcабвг'))
        self.assertFalse(self.__accentor.check_accented_wordform('abc'))
        self.assertFalse(self.__accentor.check_accented_wordform('abcабвг123'))
        self.assertTrue(self.__accentor.check_accented_wordform('а+бвг'))
        self.assertTrue(self.__accentor.check_accented_wordform('а+бвгде+жз'))
        self.assertTrue(self.__accentor.check_accented_wordform('а+б-вг'))
        self.assertFalse(self.__accentor.check_accented_wordform('-'))
        self.assertFalse(self.__accentor.check_accented_wordform('+-'))
        self.assertFalse(self.__accentor.check_accented_wordform('+'))
        self.assertFalse(self.__accentor.check_accented_wordform(''))
        self.assertFalse(self.__accentor.check_accented_wordform('-а+бвг'))
        self.assertFalse(self.__accentor.check_accented_wordform('а+б--вг'))
        self.assertFalse(self.__accentor.check_accented_wordform('a+bcа+бвг'))
        self.assertFalse(self.__accentor.check_accented_wordform('a+bc'))
        self.assertFalse(self.__accentor.check_accented_wordform('a+bcа+бвг123'))

    def test_check_morphotag_positive01(self):
        self.assertTrue(self.__accentor.check_morphotag('a,b c,d,e'))
        self.assertTrue(self.__accentor.check_morphotag('12'))
        self.assertTrue(self.__accentor.check_morphotag('a,b c,d,e(2)'))
        self.assertFalse(self.__accentor.check_morphotag('a,b c,d,e()'))
        self.assertFalse(self.__accentor.check_morphotag('a,b(1) c,d,e(2)'))
        self.assertFalse(self.__accentor.check_morphotag('a,1,b c,d,e'))
        self.assertFalse(self.__accentor.check_morphotag('a,&,b c,d,e'))
        self.assertTrue(self.__accentor.check_morphotag('a|b c|d|e'))
        self.assertTrue(self.__accentor.check_morphotag('a|b c|d|e(2)'))
        self.assertFalse(self.__accentor.check_morphotag('a|b c|d|e()'))
        self.assertFalse(self.__accentor.check_morphotag('a|b(1) c|d|e(2)'))
        self.assertFalse(self.__accentor.check_morphotag('a|1|b c|d|e'))
        self.assertFalse(self.__accentor.check_morphotag('a|&|b c|d|e'))
        self.assertTrue(
            self.__accentor.check_morphotag('VERB Aspect=Perf|Mood=Ind|Number=Sing|Person=3|Tense=Fut|VerbForm=Fin')
        )

    def test_prepare_morphotag_positive01(self):
        self.assertEqual('a,b c,d,e', self.__accentor.prepare_morphotag('a,b c,d,e(2)'))
        self.assertEqual('a,b c,d,e', self.__accentor.prepare_morphotag('a,b c,d,e'))
        self.assertNotEqual('a,b c,d,e', self.__accentor.prepare_morphotag('a,b c,d(2)'))
        self.assertNotEqual('a c,d,e', self.__accentor.prepare_morphotag('a,b c,d,e(2)'))

    def test_calculate_morpho_similarity_positive01(self):
        self.assertAlmostEqual(self.__accentor.calculate_morpho_similarity('1', 'a,b'), 0.0, places=7)
        self.assertAlmostEqual(self.__accentor.calculate_morpho_similarity('a,b c,d,e', 'a,b c,d,e'), 1.0, places=7)
        self.assertAlmostEqual(self.__accentor.calculate_morpho_similarity('a,b c,d,e', 'f,g h,i,j'), 0.0, places=7)
        self.assertAlmostEqual(self.__accentor.calculate_morpho_similarity('a,b c,d,e', 'f,b h,d,j'), 0.25, places=7)
        self.assertAlmostEqual(self.__accentor.calculate_morpho_similarity('1', 'a|b'), 0.0, places=7)
        self.assertAlmostEqual(self.__accentor.calculate_morpho_similarity('a|b c|d|e', 'a|b c|d|e'), 1.0, places=7)
        self.assertAlmostEqual(self.__accentor.calculate_morpho_similarity('a|b c|d|e', 'f|g h|i|j'), 0.0, places=7)
        self.assertAlmostEqual(self.__accentor.calculate_morpho_similarity('a|b c|d|e', 'f|b h|d|j'), 0.25, places=7)

class TestRussianAccentor2(unittest.TestCase):
    def setUp(self):
        self.__accentor = Accentor(mode='many')

    def tearDown(self):
        del self.__accentor

    def test_do_accents_positive01(self):
        source_phrase = [['оружие'], ['для'], ['кубы']]
        target_variants = [
            ['ору+жие', 'для', 'ку+бы'],
            ['ору+жие', 'для', 'кубы+']
        ]
        real_variants = self.__accentor.do_accents(source_phrase)
        self.assertEqual(target_variants, real_variants)


if __name__ == '__main__':
    unittest.main(verbosity=2)
